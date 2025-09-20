
import mysql.connector
import pandas as pd

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="chandru",
        database="cement_dispatch_v2",
        use_pure=True  # use pure Python connector to avoid crashes
    )
    
    query = "SELECT * FROM cleaned_truck_data;"
    df = pd.read_sql(query, conn)
    print("Data loaded successfully!")
    print(df.head())
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    
finally:
    if conn.is_connected():
        conn.close()



import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def clean_data(df):
    print("\n--- Data Cleaning ---")
    print("Missing values per column:")
    print(df.isnull().sum())

    print("\nDropping duplicates...")
    df.drop_duplicates(inplace=True)

    date_cols = ['registration_date', 'assignment_timestamp', 'detection_timestamp',
                 'timestamp_before', 'timestamp_after', 'loading_start_time', 'loading_end_time']

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            missing_dates = df[col].isnull().sum()
            print(f"{col}: Converted to datetime with {missing_dates} missing values")

    return df

def univariate_analysis(df):
    print("\n--- Univariate Analysis ---")
    print("Summary Statistics:")
    print(df.describe())

    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        print(f"\nValue counts for {col}:")
        print(df[col].value_counts())

    if 'cement_loaded_kg' in df.columns:
        sns.histplot(df['cement_loaded_kg'], kde=True, bins=30, color='blue')
        plt.title('Distribution of Cement Loaded (kg)')
        plt.tight_layout()
        plt.show()

    if 'truck_type' in df.columns:
        sns.countplot(x='truck_type', data=df, palette="Set2")
        plt.title('Truck Type Frequency')
        plt.tight_layout()
        plt.show()

def bivariate_analysis(df):
    print("\n--- Bivariate Analysis ---")
    if {'weight_before_kg', 'cement_loaded_kg', 'truck_type'}.issubset(df.columns):
        sns.scatterplot(x='weight_before_kg', y='cement_loaded_kg', data=df, hue='truck_type', alpha=0.7)
        plt.title('Weight Before vs Cement Loaded')
        plt.tight_layout()
        plt.show()

    if {'truck_type', 'cement_loaded_kg'}.issubset(df.columns):
        sns.boxplot(x='truck_type', y='cement_loaded_kg', data=df, palette="Set3")
        plt.title('Cement Load by Truck Type')
        plt.tight_layout()
        plt.show()

    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()

def multivariate_analysis(df):
    print("\n--- Multivariate Analysis ---")
    cols = ['weight_before_kg', 'weight_after_kg', 'cement_loaded_kg', 'truck_type']
    if all(col in df.columns for col in cols):
        sns.pairplot(df[cols], hue='truck_type')
        plt.tight_layout()
        plt.show()

    if {'truck_type', 'silo_id', 'cement_loaded_kg'}.issubset(df.columns):
        pivot = df.pivot_table(index='truck_type', columns='silo_id', values='cement_loaded_kg', aggfunc='mean').fillna(0)
        sns.heatmap(pivot, annot=True, cmap="YlGnBu")
        plt.title('Avg Cement Load by Truck Type & Silo')
        plt.tight_layout()
        plt.show()

def time_series_analysis(df):
    print("\n--- Time Series & Trend Analysis ---")
    if 'loading_start_time' in df.columns:
        df['dispatch_day'] = df['loading_start_time'].dt.date

        daily_trips = df.groupby('dispatch_day').size()
        daily_trips.plot(kind='line', marker='o', title='Trips Per Day')
        plt.xlabel("Date")
        plt.ylabel("Number of Trips")
        plt.tight_layout()
        plt.show()

        daily_load = df.groupby('dispatch_day')['cement_loaded_kg'].sum()
        daily_load.plot(kind='line', marker='o', title='Total Cement Loaded Per Day', color='green')
        plt.xlabel("Date")
        plt.ylabel("Cement Loaded (kg)")
        plt.tight_layout()
        plt.show()

def anomaly_detection(df):
    print("\n--- Anomaly Detection ---")
    if 'cement_loaded_kg' in df.columns:
        outliers = df[(df['cement_loaded_kg'] > 50000) | (df['cement_loaded_kg'] < 5000)]
        print(f"Found {len(outliers)} anomalous records (cement load too high/low):")
        print(outliers)

        # Optional: Visualize outliers on boxplot
        sns.boxplot(x=df['cement_loaded_kg'])
        plt.title("Cement Loaded (kg) - Boxplot to visualize outliers")
        plt.tight_layout()
        plt.show()

def save_cleaned_data(df, filename="cement_dispatch_cleaned.csv"):
    df.to_csv(filename, index=False)
    print(f"\nCleaned dataset saved as '{filename}'")

# === Main runner function ===
def run_full_eda(df):
    df = clean_data(df)
    univariate_analysis(df)
    bivariate_analysis(df)
    multivariate_analysis(df)
    time_series_analysis(df)
    anomaly_detection(df)
    save_cleaned_data(df)

run_full_eda(df)

