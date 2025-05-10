import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Load the Excel file
file_path = 'Datalog.xlsx'
df = pd.read_excel(file_path, sheet_name='ShiftNotes')

# Display basic info about the dataset
print(f"Dataset shape: {df.shape}")
print("\nColumns in the dataset:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# Convert date columns to datetime
df['_1ShiftDetails_ShiftStartDate'] = pd.to_datetime(df['_1ShiftDetails_ShiftStartDate'])
df['Entry_DateCreated'] = pd.to_datetime(df['Entry_DateCreated'])

# Extract date and time components
df['ShiftDate'] = df['_1ShiftDetails_ShiftStartDate'].dt.date
df['ShiftDay'] = df['_1ShiftDetails_ShiftStartDate'].dt.day_name()
df['ShiftHour'] = pd.to_datetime(df['_1ShiftDetails_ShiftStartTime']).dt.hour

# Create a proper shift duration column
df['ShiftStart'] = pd.to_datetime(df['_1ShiftDetails_ShiftStartDate'].astype(str) + ' ' + 
                                 df['_1ShiftDetails_ShiftStartTime'].astype(str))
df['ShiftEnd'] = pd.to_datetime(df['_1ShiftDetails_ShiftEndDate'].astype(str) + ' ' + 
                               df['_1ShiftDetails_ShiftEndTime'].astype(str))
df['ShiftDuration'] = (df['ShiftEnd'] - df['ShiftStart']).dt.total_seconds() / 3600

# Basic statistics
print("\nBasic statistics:")
print(f"Time period covered: {df['ShiftDate'].min()} to {df['ShiftDate'].max()}")
print(f"Number of shifts: {len(df)}")
print(f"Average shift duration: {df['ShiftDuration'].mean():.2f} hours")

# Set up visualization style
plt.style.use('ggplot')  # Changed from 'seaborn' to 'ggplot'
sns.set_palette("pastel")

# 1. Shift Distribution by Type
plt.figure(figsize=(10, 6))
shift_type_counts = df['_1ShiftDetails_TimingOfTheShift'].value_counts()
shift_type_counts.plot(kind='bar')
plt.title('Distribution of Shift Types')
plt.xlabel('Shift Type')
plt.ylabel('Number of Shifts')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Shift Duration Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['ShiftDuration'], bins=20, kde=True)
plt.title('Distribution of Shift Durations')
plt.xlabel('Shift Duration (hours)')
plt.ylabel('Frequency')
plt.show()

# 3. Daily Shift Patterns
plt.figure(figsize=(12, 6))
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_shifts = df['ShiftDay'].value_counts().reindex(day_order)
daily_shifts.plot(kind='bar')
plt.title('Shifts by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Number of Shifts')
plt.xticks(rotation=45)
plt.show()

# 4. Hourly Shift Start Patterns
plt.figure(figsize=(12, 6))
hourly_shifts = df['ShiftHour'].value_counts().sort_index()
hourly_shifts.plot(kind='bar')
plt.title('Shift Start Times by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Shifts')
plt.xticks(rotation=0)
plt.show()

# 5. Hygiene Concerns Analysis (if column exists)
hygiene_col = '_6HygieneConcerns_WhichOfTheFollowingHygieneConcernWereNoticedOnTheClient'
if hygiene_col in df.columns:
    # Split multiple entries and count occurrences
    hygiene_data = df[hygiene_col].dropna().str.split(', ').explode().value_counts().head(10)
    plt.figure(figsize=(12, 6))
    hygiene_data.plot(kind='barh')
    plt.title('Top Hygiene Concerns Noticed')
    plt.xlabel('Frequency')
    plt.ylabel('Hygiene Concern')
    plt.tight_layout()
    plt.show()

# 6. Medication Administration
if '_3MedicationAdministration_WasTheClientsMedicationAdministeredByStaff' in df.columns:
    med_admin = df['_3MedicationAdministration_WasTheClientsMedicationAdministeredByStaff'].value_counts()
    plt.figure(figsize=(8, 6))
    med_admin.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Was Medication Administered by Staff?')
    plt.ylabel('')
    plt.show()

# 7. Staff Shift Satisfaction
if '_11StaffsShiftSatisfaction_HowDidTheStaffFeelAboutTheShift' in df.columns:
    satisfaction = df['_11StaffsShiftSatisfaction_HowDidTheStaffFeelAboutTheShift'].value_counts()
    plt.figure(figsize=(10, 6))
    satisfaction.plot(kind='bar')
    plt.title('Staff Shift Satisfaction Ratings')
    plt.xlabel('Satisfaction Level')
    plt.ylabel('Number of Shifts')
    plt.xticks(rotation=45)
    plt.show()

# 8. Activities Analysis
if '_7ScheduledPlansAndActivities_ScheduledAppointmentPlansOrActivity_WhatWasTheScheduledPlanForTheDay' in df.columns:
    activities_data = df['_7ScheduledPlansAndActivities_ScheduledAppointmentPlansOrActivity_WhatWasTheScheduledPlanForTheDay'].dropna().str.split(', ').explode().value_counts().head(10)
    plt.figure(figsize=(12, 6))
    activities_data.plot(kind='barh')
    plt.title('Top 10 Scheduled Activities')
    plt.xlabel('Frequency')
    plt.ylabel('Activity')
    plt.tight_layout()
    plt.show()

# 9. Food Analysis (if columns exist)
food_cols = ['_10FoodAndMealPreparation_FoodEaten', '_10FoodAndMealPreparation_BeveragesDrank']
for col in food_cols:
    if col in df.columns:
        items = df[col].dropna().str.split(',').explode().str.strip()
        top_items = items.value_counts().head(10)
        plt.figure(figsize=(12, 6))
        top_items.plot(kind='barh')
        plt.title(f'Top 10 {col.split("_")[-1]} Items')
        plt.xlabel('Frequency')
        plt.ylabel('Item')
        plt.tight_layout()
        plt.show()

# 10. Trend of Shift Notes Over Time
plt.figure(figsize=(14, 6))
daily_notes = df.groupby('ShiftDate').size()
daily_notes.plot(kind='line', marker='o')
plt.title('Number of Shift Notes Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Notes')
plt.grid(True)
plt.tight_layout()
plt.show()

# 11. Correlation between shift duration and satisfaction (if columns exist)
if '_11StaffsShiftSatisfaction_HowDidTheStaffFeelAboutTheShift' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='_11StaffsShiftSatisfaction_HowDidTheStaffFeelAboutTheShift', y='ShiftDuration', data=df)
    plt.title('Shift Duration by Satisfaction Level')
    plt.xlabel('Satisfaction Level')
    plt.ylabel('Shift Duration (hours)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 12. Visitors Analysis
if '_4VisitorsForClient_WereThereAnyVisitorsForTheClientDuringThisShift' in df.columns:
    visitors_data = df['_4VisitorsForClient_WereThereAnyVisitorsForTheClientDuringThisShift'].value_counts()
    plt.figure(figsize=(8, 6))
    visitors_data.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Were There Any Visitors During Shifts?')
    plt.ylabel('')
    plt.show()

# 13. Behavior of Concerns Analysis
if '_5BehaviorOfConcernsLog_DidFormClientDetailsClientShowAnyBehaviorOfConcern' in df.columns:
    boc_data = df['_5BehaviorOfConcernsLog_DidFormClientDetailsClientShowAnyBehaviorOfConcern'].value_counts()
    plt.figure(figsize=(8, 6))
    boc_data.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Did the Client Show Any Behavior of Concern?')
    plt.ylabel('')
    plt.show()