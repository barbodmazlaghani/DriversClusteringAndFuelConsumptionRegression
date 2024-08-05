import pandas as pd
from scipy.stats import pearsonr
from sklearn.feature_selection import mutual_info_regression
import numpy as np

def calculate_mutual_information(df):
    mutual_info = []
    columns = df.columns
    for col1 in columns:
        mi_row = []
        for col2 in columns:
            if df[col1].dtype == 'object' or df[col2].dtype == 'object':
                mi_row.append(np.nan)  # Mutual information can't be calculated for categorical data directly
            else:
                mi = mutual_info_regression(df[[col1]], df[col2])
                mi_row.append(mi[0])
        mutual_info.append(mi_row)
    return pd.DataFrame(mutual_info, columns=columns, index=columns)

# Load the data
file_path = 'drivers_mean_base.xlsx'  # Update this to your Excel file path
df = pd.read_excel(file_path)

# Compute the correlation matrix
correlation_matrix = df.corr()

# Compute the mutual information matrix
mutual_information_matrix = calculate_mutual_information(df)

# Create a Pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter('output_metrics.xlsx', engine='xlsxwriter')

# Write each DataFrame to a specific sheet
correlation_matrix.to_excel(writer, sheet_name='Correlation Matrix')
mutual_information_matrix.to_excel(writer, sheet_name='Mutual Information Matrix')

# Close the Pandas Excel writer and output the Excel file
writer.save()
