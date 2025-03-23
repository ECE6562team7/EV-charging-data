import pandas as pd 
csv_file_path = '/Users/siddharthjawahar/Documents/Data Analysis/EV charging/alt_fuel_stations (Mar 23 2025).csv'
db = pd.read_csv(csv_file_path)
print(db.head())
excel_file_path = '/Users/siddharthjawahar/Documents/Data Analysis/EV charging/alt_fuel_stations (Mar 23 2025).xlsx'
db.to_excel(excel_file_path, index=False)
print('Conversion successful')