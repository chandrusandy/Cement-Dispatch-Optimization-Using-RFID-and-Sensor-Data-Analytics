import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
truck_loading_events = pd.read_csv(r"C:\Users\Chandru\OneDrive\Desktop\project\Data Set\truck_loading_events.csv")
truck_master = pd.read_csv(r"C:\Users\Chandru\OneDrive\Desktop\project\Data Set\truck_master.csv")
truck_weight_logs = pd.read_csv(r"C:\Users\Chandru\OneDrive\Desktop\project\Data Set\truck_weight_logs.csv")

print(truck_loading_events.shape)
print(truck_master.shape)
print(truck_weight_logs.shape)

df1 = pd.merge(truck_loading_events, truck_master, on='truck_id', how='left')

final_df = pd.merge(df1, truck_weight_logs, on='truck_id', how='left')

print(final_df.head())


# Univariate: distribution of cement loaded
final_df['cement_loaded_kg'].hist(bins=30)
plt.title('Distribution of Cement Loaded (kg)')
plt.show()

# Bivariate: cement_loaded_kg by truck_type boxplot
sns.boxplot(x='truck_type', y='cement_loaded_kg', data=final_df)
plt.title('Cement Loaded by Truck Type')
plt.show()

# Multivariate: correlation heatmap of numeric columns
numeric_cols = ['cement_loaded_kg', 'weight_before_kg', 'weight_after_kg']
sns.heatmap(final_df[numeric_cols].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

from scipy import stats

numeric_cols = ['cement_loaded_kg', 'weight_before_kg', 'weight_after_kg']

for col in numeric_cols:
    print(f"--- Analysis for {col} ---")

    data = final_df[col].dropna()
    
    # 1st Moment: Mean, Median, Mode
    mean = data.mean()
    median = data.median()
    mode = data.mode()
    mode_val = mode.iloc[0] if not mode.empty else 'No mode'
    
    # 2nd Moment: Variance, Std Dev, Range
    variance = data.var()
    std_dev = data.std()
    data_range = data.max() - data.min()
    
    # 3rd Moment: Skewness
    skewness = data.skew()
    
    # 4th Moment: Kurtosis
    kurtosis = data.kurtosis()
    
    print(f"Mean: {mean:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Mode: {mode_val}")
    print(f"Variance: {variance:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")
    print(f"Range: {data_range:.2f}")
    print(f"Skewness: {skewness:.2f}")
    print(f"Kurtosis: {kurtosis:.2f}")
    print("\n")




