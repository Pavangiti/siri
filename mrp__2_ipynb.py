# -*- coding: utf-8 -*-
"""MRP_-2. ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16T92_xwDovHVUOC6KR1Y3dtIR-2HSEH0
"""

# Import necessary libraries
import pandas as pd
from google.colab import files

# Upload multiple files at once
uploaded = files.upload()

# Load datasets
df_patient = pd.read_csv("patients (4).csv")
df_immunization = pd.read_csv("immunizations (2).csv")

print(df_patient['STATE'].value_counts())

# Ensuring Referential Integrity: Every Patient ID in immunization must exist in patient dataset
missing_patients = df_immunization[~df_immunization['PATIENT'].isin(df_patient['Id'])]

if missing_patients.empty:
    print("✅ Referential integrity is maintained.")
else:
    print("⚠️ Missing Patient_IDs in Patient table:", missing_patients['PATIENT'].unique())

# Convert date columns to datetime format
df_patient['BIRTHDATE'] = pd.to_datetime(df_patient['BIRTHDATE'], errors='coerce')
df_patient['DEATHDATE'] = pd.to_datetime(df_patient['DEATHDATE'], errors='coerce')
df_immunization['DATE'] = pd.to_datetime(df_immunization['DATE'], errors='coerce')

# Check for invalid birthdates (Future dates)
invalid_birthdates = df_patient[df_patient['BIRTHDATE'] > pd.to_datetime('today')]
if not invalid_birthdates.empty:
    print(" Invalid birthdates found:", invalid_birthdates)

# Calculate Age (Handling both living and deceased patients)
current_date = pd.to_datetime('2025-02-09')  # Change to today's date
df_patient['Age'] = df_patient.apply(
    lambda row: (row['DEATHDATE'] - row['BIRTHDATE']).days // 365 if pd.notnull(row['DEATHDATE'])
    else (current_date - row['BIRTHDATE']).days // 365,
    axis=1
)
print(" Patient ages calculated successfully.")

# Define target vaccines as a set of exact string values
target_vaccines = {
    'Influenza  seasonal  injectable  preservative free',
    'COVID-19 vaccine  vector-nr  rS-Ad26  PF  0.5 mL',
    'Hib (PRP-OMP)',
    'MMR',
    'DTaP',
    'meningococcal MCV4P',
    "COVID-19 mRNA LNP-S PF 30 mcg/0.3 mL dose",
    "COVID-19 mRNA LNP-S PF 100 mcg/0.5mL dose or 50 mcg/0.25mL dose"
}

# Define target vaccines as a set of numeric values from your dataset
target_vaccines = {88, 118, 135, 140, 150, 155, 160, 165}

# Identify patients who have received at least one of the target vaccines
df_immunization['Vaccinated'] = df_immunization['CODE'].apply(lambda x: 'Yes' if x in target_vaccines else 'No')

# Display updated immunization table
print(df_immunization.head())

df_immunization.to_csv('/content/immunizations_with_vaccination_status.csv', index=False)

print("Updated immunizations dataset saved.")

# Ensure DATE column has no timezone issues
df_immunization['DATE'] = df_immunization['DATE'].dt.tz_localize(None)

# Define a reference date for forecasting
comparison_date = pd.to_datetime('2022-12-31')

# Filter for recent vaccination records (last 3 years)
recent_vaccination_records = df_immunization[df_immunization['DATE'] > comparison_date - pd.DateOffset(years=3)]
print(f" {len(recent_vaccination_records)} recent vaccination records found.")

# Convert dates to proper format
df_patient['BIRTHDATE'] = pd.to_datetime(df_patient['BIRTHDATE'])
df_patient['DEATHDATE'] = pd.to_datetime(df_patient['DEATHDATE'])
df_immunization['DATE'] = pd.to_datetime(df_immunization['DATE'])

# Check for invalid birthdates (future dates)
invalid_birthdates = df_patient[df_patient['BIRTHDATE'] > pd.to_datetime('2025-02-09')]
if not invalid_birthdates.empty:
    print("Invalid birthdates found:", invalid_birthdates)

# Calculate age (handling both living and deceased patients)
today = pd.Timestamp("2025-02-09")  # Considering today's date as Feb 9, 2025
df_patient['Age'] = df_patient.apply(
    lambda row: (row['DEATHDATE'] - row['BIRTHDATE']).days // 365 if pd.notnull(row['DEATHDATE'])
    else (today - row['BIRTHDATE']).days // 365, axis=1
)

print("Patient ages calculated successfully.")

df_patient.loc[df_patient['BIRTHDATE'] > pd.to_datetime('2025-02-09'), 'BIRTHDATE'] = pd.NaT

invalid_birthdates_before = df_patient[df_patient['BIRTHDATE'] > pd.to_datetime('2025-02-09')]
print(f"Invalid birthdates before replacing: {len(invalid_birthdates_before)}")

print(df_patient['BIRTHDATE'].head())  # Check the first few rows to ensure they're in the correct datetime format

# Data Cleaning: Validating and replacing invalid values
valid_genders = {"M", "F"}
valid_ethnicities = {"hispanic", "nonhispanic"}
valid_races = {"white", "black", "asian", "hawaiian", "native", "other"}

# Normalize text: strip spaces & convert to lowercase
df_patient['GENDER'] = df_patient['GENDER'].str.strip().str.upper()
df_patient['ETHNICITY'] = df_patient['ETHNICITY'].str.strip().str.lower()
df_patient['RACE'] = df_patient['RACE'].str.strip().str.lower()

# Replace invalid values
df_patient['GENDER'] = df_patient['GENDER'].apply(lambda x: x if x in valid_genders else "NA")
df_patient['ETHNICITY'] = df_patient['ETHNICITY'].apply(lambda x: x if x in valid_ethnicities else "NA")
df_patient['RACE'] = df_patient['RACE'].apply(lambda x: x if x in valid_races else "NA")

# Print unique values after cleaning
print("Unique Gender Values After:", df_patient['GENDER'].unique())
print("Unique Ethnicity Values After:", df_patient['ETHNICITY'].unique())
print("Unique Race Values After:", df_patient['RACE'].unique())

print(df_patient.head())  # Check the first few rows to ensure 'Age' is in the DataFrame

print(df_patient.shape)  # Compare row count before and after cleaning

import pandas as pd

# Replace invalid age entries (-1) with NaN
df_patient['Age'] = df_patient['Age'].replace(-1, pd.NA)
df_patient['Age'] = df_patient['Age'].apply(lambda x: pd.NA if pd.notna(x) and x > 110 else x)

# Define meaningful age bins and labels for analysis
age_bins = [0, 18, 30, 50, 70, 110]
age_labels = ['0-17', '18-29', '30-49', '50-69', '70+']
df_patient['AGE_GROUP'] = pd.cut(df_patient['Age'].dropna(), bins=age_bins, labels=age_labels, right=False)

# Debug: Print unique immunization codes to verify
print("Unique immunization codes:", df_immunization['CODE'].unique())

# Update target vaccines with new numeric codes
# Define target vaccines as a set of numeric values from your dataset
target_vaccines = {88, 118, 135, 140, 150, 155, 160, 165}  # Use correct numeric values from your dataset

# Identify patients who received at least one of the target vaccines
vaccinated_patients = df_immunization[df_immunization['CODE'].isin(target_vaccines)]['PATIENT'].unique()

# Add "VACCINATED" column to df_patient (Yes/No)
df_patient['VACCINATED'] = df_patient['Id'].apply(lambda x: 'Yes' if x in vaccinated_patients else 'No')

# Identify unvaccinated groups (those with no target vaccine records)
unvaccinated_groups = df_patient[df_patient['VACCINATED'] == 'No']
unvaccinated_counts = unvaccinated_groups.groupby(['AGE_GROUP', 'GENDER', 'RACE', 'ETHNICITY']).size().reset_index(name='Count')

# Grouping by demographics and vaccination status for percentages
age_vaccination = df_patient.groupby('AGE_GROUP')['VACCINATED'].value_counts().unstack().fillna(0)
# (Similarly for gender_vaccination, race_vaccination, etc.)

# Function to calculate under-immunized percentages
def calculate_under_immunized_percent(vaccination_df, threshold):
    if 'No' in vaccination_df.columns and 'Yes' in vaccination_df.columns:
        vaccination_df['Under-immunized %'] = (vaccination_df['No'] / (vaccination_df['No'] + vaccination_df['Yes'])) * 100
    elif 'No' in vaccination_df.columns:
        vaccination_df['Under-immunized %'] = 100.0
    elif 'Yes' in vaccination_df.columns:
        vaccination_df['Under-immunized %'] = 0.0
    else:
        vaccination_df['Under-immunized %'] = 0.0

"""Our analysis revealed that a large proportion of patients from the datset remain under-immunized for the targeted vaccines. where 60% of children under 18 have received at least one target vaccine, nearly 100% of patients in the 18-29 and 30-49 age groups are under-immunized. Even in older groups, under-immunization is high (83% for ages 50-69 and 70% for ages 70+). So this clearly indicatea that there are significant gaps in vaccine coverage that need to be addressed through targeted public health initiatives."""

print(df_immunization['CODE'].unique())

"""These numbers are unique identifiers used in the Synthea immunizations dataset to represent different vaccines. Instead of text names, the dataset uses these numeric codes to maintain consistency and simplicity in data storage and processing. When analyzing the data, we reference these codes to identify which vaccine was administered"""

# Drop unnecessary columns efficiently
columns_to_drop = ['SSN', 'DRIVERS', 'PASSPORT', 'PREFIX', 'SUFFIX', 'FIRST', 'MIDDLE', 'LAST',
                   'MAIDEN', 'MARITAL', 'ADDRESS', 'FIPS', 'ZIP', 'LAT', 'LON',
                   'HEALTHCARE_EXPENSES', 'HEALTHCARE_COVERAGE', 'INCOME', 'ENCOUNTER', 'BASE_COST']

"""Here we have aalysed under-vaccinated groups based on demographics. For 0-17 age group we can see the highest under-immunization rate (3.55%), while older groups show near 0% under-vaccination. Males (1.09%) are slightly more under-vaccinated than females (0.89%). Among racial groups, Black (1.32%) and White (1.01%) populations have higher under-immunization rates, while other races remain below 1%. Non-Hispanics (1.04%) are slightly more under-vaccinated than Hispanics (0.90%). City-level analysis shows most locations have 0% under-immunization, indicating high vaccination coverage in most areas.

**I analyzed under-vaccination based on demographics, including age, gender, race, ethnicity, and city. I checked whether patients received at least one of the target vaccines and calculated the percentage of people who were not vaccinated in each group. This helped identify which groups have higher under-immunization rates.**
"""

print(df_immunization.columns)  # Check available columns
print(df_immunization.head())   # View sample data

# Ensure 'DESCRIPTION' is included in the merge
under_vaccinated = df_patient.merge(
    df_immunization[['PATIENT', 'CODE', 'DESCRIPTION', 'DATE']],  # Explicit selection
    left_on='Id',
    right_on='PATIENT',
    how='left',
    indicator=True
)

# Extract YEAR from DATE column
under_vaccinated['YEAR'] = pd.to_datetime(under_vaccinated['DATE'], errors='coerce').dt.year


# Display the first few rows to verify the merge
print(under_vaccinated[['Id', 'DESCRIPTION', 'YEAR']].head())

print(under_vaccinated[['Id', 'DESCRIPTION', 'CODE', 'YEAR']].head())



under_vaccinated['YEAR'] = pd.to_datetime(under_vaccinated['DATE'], errors='coerce').dt.year
print(under_vaccinated[['DATE', 'YEAR']].dropna().head())  # Check DATE and extracted YEAR

print("Final Merged Columns:", under_vaccinated.columns)

import pandas as pd

# Replace invalid age entries (-1) with NaN
df_patient['Age'] = df_patient['Age'].replace(-1, pd.NA)

# Handle any other invalid outliers (ages above 110)
df_patient['Age'] = df_patient['Age'].apply(lambda x: pd.NA if pd.notna(x) and x > 110 else x)

# Define meaningful age bins and labels for analysis
age_bins = [0, 18, 30, 50, 70, 110]
age_labels = ['0-17', '18-29', '30-49', '50-69', '70+']
df_patient['AGE_GROUP'] = pd.cut(df_patient['Age'].dropna(), bins=age_bins, labels=age_labels, right=False)

# Debugging: Check unique immunization codes
print("Unique immunization codes:", df_immunization['CODE'].unique())

# Define the specific target vaccines
target_vaccines = {88, 118, 135, 140, 150, 155, 160, 165}

# Identify patients who received at least one of the target vaccines
vaccinated_patients = df_immunization[df_immunization['CODE'].isin(target_vaccines)]['PATIENT'].unique()

# Add "VACCINATED" column to df_patient
df_patient['VACCINATED'] = df_patient['Id'].isin(vaccinated_patients)

# Merge to include DESCRIPTION, CODE, and YEAR
df_patient = df_patient.merge(
    df_immunization[['PATIENT', 'CODE', 'DESCRIPTION', 'DATE']],
    left_on='Id',
    right_on='PATIENT',
    how='left'
)

# Extract YEAR from DATE
df_patient['YEAR'] = pd.to_datetime(df_patient['DATE'], errors='coerce').dt.year

# Debugging: Verify the columns exist
print("\nColumns in df_patient after merging:", df_patient.columns.tolist())
print("\nSample merged dataset:\n", df_patient[['Id', 'DESCRIPTION', 'CODE', 'YEAR']].dropna().head())


# Identify unvaccinated groups (those with no target vaccine records)
unvaccinated_groups = under_vaccinated[under_vaccinated['_merge'] == 'left_only']
unvaccinated_counts = unvaccinated_groups.groupby(['AGE_GROUP', 'GENDER', 'RACE', 'ETHNICITY']).size().reset_index(name='Count')

# Grouping by demographics and vaccination status for percentages
age_vaccination = df_patient.groupby('AGE_GROUP')['VACCINATED'].value_counts().unstack().fillna(0)
gender_vaccination = df_patient.groupby('GENDER')['VACCINATED'].value_counts().unstack().fillna(0)
race_vaccination = df_patient.groupby('RACE')['VACCINATED'].value_counts().unstack().fillna(0)
ethnicity_vaccination = df_patient.groupby('ETHNICITY')['VACCINATED'].value_counts().unstack().fillna(0)
city_vaccination = df_patient.groupby('CITY')['VACCINATED'].value_counts().unstack().fillna(0)

# Function to calculate under-immunized percentages
def calculate_under_immunized_percent(vaccination_df):
    if False in vaccination_df.columns and True in vaccination_df.columns:
        vaccination_df['Under-immunized %'] = (vaccination_df[False] / (vaccination_df[False] + vaccination_df[True])) * 100
    elif False in vaccination_df.columns:
        vaccination_df['Under-immunized %'] = 100.0
    elif True in vaccination_df.columns:
        vaccination_df['Under-immunized %'] = 0.0
    else:
        vaccination_df['Under-immunized %'] = 0.0
    return vaccination_df[['Under-immunized %']].round(2)

age_vaccination = calculate_under_immunized_percent(age_vaccination)
gender_vaccination = calculate_under_immunized_percent(gender_vaccination)
race_vaccination = calculate_under_immunized_percent(race_vaccination)
ethnicity_vaccination = calculate_under_immunized_percent(ethnicity_vaccination)
city_vaccination = calculate_under_immunized_percent(city_vaccination)

# Display results
print("Under-vaccinated patient counts by Age, Gender, Race, and Ethnicity:\n", unvaccinated_counts)

print("\nUnder-immunized groups by Age:")
print(age_vaccination)

print("\nUnder-immunized groups by Gender:")
print(gender_vaccination)

print("\nUnder-immunized groups by Race:")
print(race_vaccination)

print("\nUnder-immunized groups by Ethnicity:")
print(ethnicity_vaccination)

print("\nUnder-immunized groups by City:")
print(city_vaccination)

# 🔹 Debugging check to ensure DESCRIPTION, CODE, and YEAR exist after merging
print("\nFinal merged dataset columns:", under_vaccinated.columns)
print("\nSample merged dataset:\n", under_vaccinated[['Id', 'DESCRIPTION', 'CODE', 'YEAR']].dropna().head())

df_patient.drop(columns=columns_to_drop, errors='ignore', inplace=True)


# Drop unnecessary columns efficiently
columns_to_drop = ['SSN', 'DRIVERS', 'PASSPORT', 'PREFIX', 'SUFFIX', 'FIRST', 'MIDDLE', 'LAST',
                   'MAIDEN', 'MARITAL', 'ADDRESS', 'FIPS', 'ZIP', 'LAT', 'LON',
                   'HEALTHCARE_EXPENSES', 'HEALTHCARE_COVERAGE', 'INCOME', 'ENCOUNTER', 'BASE_COST']

print(df_patient.columns.tolist())

# Import necessary libraries
import pandas as pd
import numpy as np  # Ensure numpy is imported
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Reset index and drop the existing index column (if any)
df_immunization = df_immunization.reset_index(drop=True)

# Convert 'DATE' to datetime
df_immunization['DATE'] = pd.to_datetime(df_immunization['DATE'])

# Ensure timezone consistency (localize if naive, then remove timezone)
if df_immunization['DATE'].dt.tz is None:
    df_immunization['DATE'] = df_immunization['DATE'].dt.tz_localize('UTC')

df_immunization['DATE'] = df_immunization['DATE'].dt.tz_convert(None)

# Filter records from 2020 to 2024
start_date = pd.Timestamp("2020-01-01")
end_date = pd.Timestamp("2024-12-31")

vaccination_records = df_immunization[
    (df_immunization['DATE'] >= start_date) &
    (df_immunization['DATE'] <= end_date)
]

# Group by year and count the number of patients (vaccination trends)
vaccination_trends = vaccination_records.groupby(vaccination_records['DATE'].dt.year)['PATIENT'].count()

# Print summary
print(f"{len(vaccination_records)} vaccination records found between 2020-2024.")
print("Vaccination trends from 2020 to 2024:\n", vaccination_trends)

# ------------------- Forecasting Next 5 Years (2025-2029) -------------------

# Convert trends to time series format
years = vaccination_trends.index.astype(int)  # Extracting years as integers
values = vaccination_trends.values  # Vaccination counts

# Create a time series DataFrame with proper datetime index
ts_data = pd.DataFrame({'Year': years, 'Vaccinations': values})
ts_data['Date'] = pd.to_datetime(ts_data['Year'], format='%Y')
ts_data.set_index('Date', inplace=True)

# Apply Exponential Smoothing for forecasting
model = ExponentialSmoothing(ts_data['Vaccinations'], trend='add', seasonal=None, seasonal_periods=None)
fit_model = model.fit()

# Forecast for the next 5 years (2025-2029)
forecast_values = fit_model.forecast(steps=5)

# Ensure that the forecast years match the length of forecast values
future_years = np.arange(2025, 2025 + len(forecast_values))

# Create a DataFrame for the forecasted values
forecast_df = pd.DataFrame({'Year': future_years, 'Forecasted_Vaccinations': forecast_values})
forecast_df['Date'] = pd.to_datetime(forecast_df['Year'], format='%Y')
forecast_df.set_index('Date', inplace=True)

# Plot past trends and future forecast
plt.figure(figsize=(10, 5))
plt.plot(ts_data.index, ts_data['Vaccinations'], marker='o', label='Actual Vaccinations (2020-2024)')
plt.plot(forecast_df.index, forecast_df['Forecasted_Vaccinations'], marker='o', linestyle='dashed', color='red', label='Forecasted Vaccinations (2025-2029)')
plt.xlabel("Year")
plt.ylabel("Number of Vaccinations")
plt.title("Vaccination Trends & Forecast (2020-2029)")
plt.legend()
plt.grid(True)
plt.show()

# Save the merged DataFrame to a CSV file
df_patient.to_csv("under_vaccinated_analysis.csv", index=False)

print("CSV file saved successfully!")

from google.colab import files

# Save the DataFrame to CSV
df_patient.to_csv("under_vaccinated_analysis.csv", index=False)

# Download the file
files.download("under_vaccinated_analysis.csv")