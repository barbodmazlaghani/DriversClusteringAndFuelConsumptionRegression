import pandas as pd
import os
import numpy as np

driver_data = pd.read_excel('E:\علم داده\Project_01\drivers_refined\driver-data.xlsx')

results = pd.DataFrame(
    columns=['driver','driver_n' , 'speed_avg','speed_var','speed_tv', 'acc_pedal_avg', 'acc_pedal_var', 'acc_mean', 'acc_var', 'dec_mean',
             'dec_var','voltage_avg'])
folder_path = 'E:\علم داده\Project_01\drivers_refined\80 Drivers'
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        index_start = df[df['maneuver'] == 'DEPART'].index[0]
        index_end = df[df['maneuver'] == 'ARRIVE'].index[0]
        df = df.loc[index_start:index_end]

        df["acc"] = (1000 * df["Speed"].diff()) / (3.6 * df["Time"].diff())
        df["accc"] = (1000 * df["acc"].diff()) / (3.6 * df["Time"].diff())
        df["dec"] = df["acc"].apply(lambda x: abs(x) if x < 0 else np.nan)
        df["acc"] = df["acc"].apply(lambda x: x if x > 0 else np.nan)
        df["accc"] = df["accc"].apply(lambda x: x if x > 0 else np.nan)
        filename = filename.replace("_refined", "")
        driver_row = driver_data[driver_data['fileName'] == filename]
        df["Current gear shift position"].replace("N", 0, inplace=True)
        df["Current gear shift position"].replace("1", 1, inplace=True)
        df["Current gear shift position"].replace("2", 2, inplace=True)
        df["Current gear shift position"].replace("3", 3, inplace=True)
        df["Current gear shift position"].replace("4", 4, inplace=True)
        df["Current gear shift position"].replace("5", 5, inplace=True)
        df["Current gear shift position"].replace("6", 6, inplace=True)
        column_values = df["Current gear shift position"]
        zero_count = len(column_values[column_values == 0])
        one_count = len(column_values[column_values == 1])
        two_count = len(column_values[column_values == 2])
        three_count = len(column_values[column_values == 3])
        four_count = len(column_values[column_values == 4])
        five_count = len(column_values[column_values == 5])
        six_count = len(column_values[column_values == 6])
        total_count = len(column_values)

        zero_percentage = (zero_count / total_count) * 100
        one_percentage = (one_count / total_count) * 100
        two_percentage = (two_count / total_count) * 100
        three_percentage = (three_count / total_count) * 100
        four_percentage = (four_count / total_count) * 100
        five_percentage = (five_count / total_count) * 100
        six_percentage = (six_count / total_count) * 100
        if df["Cumulative mileage"].max() - df["Cumulative mileage"].min() > 1000 or df["Cumulative mileage"].max() - \
                df["Cumulative mileage"].min() < 5:
            continue
        # if (df["Trip fuel consumption"].max() - df[
        #     "Trip fuel consumption"].min()) / (10000 * (
        #         df["Cumulative mileage"].max() - df["Cumulative mileage"].min())) < 7.5 :
        #     continue,'driver': driver_row['fileName'].values[0],
        results = results.append({'driver': driver_row['driver_name_english'].values[0],
                                  'driver_n': driver_row['fileName'].values[0],
                                  'speed_avg': df["Speed"].mean(),
                                  'speed_var': df["Speed"].var(),
                                  'speed_tv': df['Speed'].diff().abs().sum() / df['Speed'].size,
                                  'voltage_avg':df["Battery voltage"].mean(),
                                  # 'fuel_cor': df["Fuel correction zone"].mean(),
                                  'target_air' :df["Target air-fuel ratio"].mean(),
                                  'coolant_avg': df["Coolant temperature"].mean(),
                                  'acc_mean': df["acc"].mean(),
                                  'acc_max': df["acc"].max(),
                                  'acc_var': df["acc"].var(),
                                  'accc_mean': df["accc"].mean,
                                  'accc_max': df["accc"].max,
                                  'dec_mean': df["dec"].mean(),
                                  'dec_max': df["dec"].max(),
                                  'dec_var': df["dec"].var(),
                                  # 'time_dur': df["Timestamp"].max() - df["Timestamp"].min(),
                                  'cum_mil_max_min': df["Cumulative mileage"].max() - df[
                                      "Cumulative mileage"].min(),
                                  'acc_pedal_avg': df["Accelerator pedal position"].mean(),
                                  'acc_pedal_var': df["Accelerator pedal position"].var(),
                                  'eng_speed_avg':df["Engine speed"].mean(),
                                  'eng_speed_var':df["Engine speed"].var(),
                                  'zero_gear_percentage': zero_percentage,
                                  'one_gear_percentage': one_percentage,
                                  'two_gear_percentage': two_percentage,
                                  'three_gear_percentage': three_percentage,
                                  'four_gear_percentage': four_percentage,
                                  'five_gear_percentage': five_percentage,
                                  'six_gear_percentage': six_percentage,

                                  # 'acc_tv': df["acceleration"].diff().abs().sum() / df['acceleration'].size,
                                  # 'electrical_load': df["Electrical load"].mean(),
                                  'fuel_consumption_avg': (df["Trip fuel consumption"].max() - df[
                                      "Trip fuel consumption"].min()) / (10000 * (
                                          df["Cumulative mileage"].max() - df["Cumulative mileage"].min()))
                                  }
                                 , ignore_index=True)
        # print(driver_row['driver_name_english'].values[0])
        # driver_row['driver_name_english'].values[0]
results.to_excel('drivers_mean_base.xlsx', index=False)