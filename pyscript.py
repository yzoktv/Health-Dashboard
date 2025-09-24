import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict

tree = ET.parse("export.xml")
root = tree.getroot()
records = root.findall('Record')

# --- Daily steps ---
steps = []

for rec in records:
    if rec.attrib['type'] == "HKQuantityTypeIdentifierStepCount":
        steps.append({
            'start_time': rec.attrib['startDate'],
            'end_time': rec.attrib['endDate'],
            'value': float(rec.attrib['value']),
            'source_id': source_map.get(rec.attrib.get('sourceName'))
        })

df_steps = pd.DataFrame(steps)
df_steps['start_time'] = pd.to_datetime(df_steps['start_time'])
df_steps['end_time'] = pd.to_datetime(df_steps['end_time'])

df_steps['date'] = df_steps['start_time'].dt.date
daily_steps = df_steps.groupby('date')['value'].sum().reset_index()
daily_steps.columns = ['date', 'total_steps']

from sqlalchemy import create_engine
import pymysql

# Replace with your actual values
user = 'root'
password = 'Yzoktv1130!'  # Replace this with your actual password
host = 'localhost'
port = 3306
database = 'apple_health' # Must create this database first

# Create engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
daily_steps.to_sql("daily_steps", con=engine, if_exists="replace", index=False)

# --- Sleep ---
sleep = []

sleep_stage_map = {
    'HKCategoryValueSleepAnalysisAsleepCore': 'core',
    'HKCategoryValueSleepAnalysisAsleepDeep': 'deep',
    'HKCategoryValueSleepAnalysisAsleepREM': 'rem',
    'HKCategoryValueSleepAnalysisAsleepUnspecified': 'asleep',
    'HKCategoryValueSleepAnalysisAwake': 'awake',
    'HKCategoryValueSleepAnalysisInBed': 'inBed'
}

for rec in records:
    if rec.attrib['type'] == "HKCategoryTypeIdentifierSleepAnalysis":
        raw_value = rec.attrib.get('value')
        mapped_stage = sleep_stage_map.get(raw_value, 'unknown')
        sleep.append({
            'start_time': rec.attrib['startDate'],
            'end_time': rec.attrib['endDate'],
            'state': mapped_stage,
            'source_id': source_map.get(rec.attrib.get('sourceName'))
        })

df_sleep = pd.DataFrame(sleep)
df_sleep['start_time'] = pd.to_datetime(df_sleep['start_time'])
df_sleep['end_time'] = pd.to_datetime(df_sleep['end_time'])
df_sleep["sleep_date"] = df_sleep["start_time"].apply(
    lambda dt: (dt - pd.Timedelta(days=1)).date() if dt.hour < 12 else dt.date()
)
# 1. Create duration column in seconds or minutes
df_sleep["duration"] = df_sleep["end_time"] - df_sleep["start_time"]
df_sleep["duration"] = df_sleep["duration"].dt.total_seconds() / 3600  # in hours

# 2. Aggregate duration by sleep_date and state
df_sleep_summary = df_sleep.groupby(['sleep_date', 'state'])['duration'].sum().reset_index()

sleep_totals = (
    df_sleep_summary[df_sleep_summary['state'].isin(['deep', 'rem', 'core'])]
    .groupby('sleep_date')['duration']
    .sum()
    .reset_index(name='total')
)

# Step 2: Merge total sleep duration back to the original dataframe
df_sleep_summary = df_sleep_summary.merge(sleep_totals, on='sleep_date', how='left')

df_sleep_summary.to_sql("sleep", con=engine, if_exists="replace", index=False)

# --- Workout ---
workouts = []

for rec in root.findall('Workout'):
    workouts.append({
        'start_time': rec.attrib['startDate'],
        'end_time': rec.attrib['endDate'],
        'workout_type': rec.attrib['workoutActivityType'],
        'duration_min': float(rec.attrib.get('duration', 0)),
        'source_id': source_map.get(rec.attrib.get('sourceName'))
    })

df_workouts = pd.DataFrame(workouts)
df_workouts['start_time'] = pd.to_datetime(df_workouts['start_time'])
df_workouts['end_time'] = pd.to_datetime(df_workouts['end_time'])
df_workouts['workout_type'] = df_workouts['workout_type'].str.replace('HKWorkoutActivityType','')

df_workouts.head()
df_workouts.to_sql("workout", con=engine, if_exists="replace", index=False)

# --- Calories ---
calories = []

for rec in records:
    type_ = rec.attrib['type']
    if type_ in ['HKQuantityTypeIdentifierBasalEnergyBurned', 'HKQuantityTypeIdentifierActiveEnergyBurned']:
        calories.append({
            'datetime': rec.attrib['startDate'],
            'type': type_,
            'kcal': float(rec.attrib['value']),
            'source_id': source_map.get(rec.attrib.get('sourceName'))
        })

df_cal = pd.DataFrame(calories)

# Parse datetime and extract date + hour
df_cal['datetime'] = pd.to_datetime(df_cal['datetime'])
df_cal['date'] = df_cal['datetime'].dt.date
df_cal['hour'] = df_cal['datetime'].dt.hour  # 0–23 as integer

# Group by date + hour + type
df_hourly = df_cal.groupby(['date', 'hour', 'type'])['kcal'].sum().reset_index()

# Pivot to get one row per date-hour
df_merged = df_hourly.pivot(index=['date', 'hour'], columns='type', values='kcal').reset_index()

# Rename columns
df_merged.columns.name = None
df_merged = df_merged.rename(columns={
    'HKQuantityTypeIdentifierBasalEnergyBurned': 'basal_kcal',
    'HKQuantityTypeIdentifierActiveEnergyBurned': 'active_kcal'
})

df_merged.to_sql("calories", con=engine, if_exists="replace", index=False)

## --- Overall score ---
cal_summary = df_cal[df_cal['type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned'].groupby('date').sum('kcal').reset_index()
cal_summary = cal_summary[["date", "kcal"]]

sleep_summary = df_sleep_summary[df_sleep_summary['state'].isin(["core", "deep", "rem"])].groupby('sleep_date').sum('duration').reset_index()

# 1. Rename to match column names
sleep_summary = sleep_summary.rename(columns={'sleep_date': 'date'})

# 2. Merge all data sources on 'date'
df_merged = pd.merge(cal_summary, sleep_summary, on='date', how='outer')
df_merged = pd.merge(df_merged, daily_steps, on='date', how='outer')

# 3. Convert date, sort, drop rows with any missing values
df_merged['date'] = pd.to_datetime(df_merged['date'])
df_merged = df_merged.sort_values('date').dropna().reset_index(drop=True)

# 4. Check the final clean dataset
df_merged.head()
df_merged.to_sql("score", con=engine, if_exists="replace", index=False)

