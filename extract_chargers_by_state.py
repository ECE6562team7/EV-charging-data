import pandas as pd 
import re #need this module for regular expressions
csv_file_path = '/Users/siddharthjawahar/Documents/Data Analysis/EV charging/alt_fuel_stations (Mar 23 2025).csv'
db = pd.read_csv(csv_file_path)

print(db.head()) #Checking if the file loads properly

# We extract columns of interest
db = db[['State','EV Level1 EVSE Num','EV Level2 EVSE Num','EV DC Fast Count','EV Other Info']]

# Converting the state abbreviations to actual state names
# Mapping dictionary from abbreviation to full state name
us_state_to_full = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "DC": "District of Columbia"
}

# Apply the mapping to create a new column
db['State Full'] = db['State'].map(us_state_to_full)

#EV other info has text input from which we extract the number of charging stations

def extract_numbers(text):
    if pd.isnull(text):
        return 0
    numbers = re.findall(r'\d+','text')
    return sum(int(num) for num in numbers)

# We will apply the above function to the 'EV Other Info' column
db['EV Other Info Count'] = db['EV Other Info'].apply(extract_numbers)

# With the text sorted out we now add the number of chargers for each rows
db.fillna(0, inplace=True)
db['Total EVSEs'] = (
    db['EV Level1 EVSE Num'].astype(int) + 
    db['EV Level2 EVSE Num'].astype(int) + 
    db['EV DC Fast Count'].astype(int) + 
    db['EV Other Info Count'].astype(int)
)

#Aggregate counts by state  
db_summary = db.groupby('State Full')['Total EVSEs'].sum().reset_index()
#Rename columns
db_summary.columns = ['State','Total EVSEs']
#Test print
print(db_summary.head())

#Save the summary to a new excel file
db_summary.to_excel('EVSE_Stations_By_State.xlsx', index=False)
print("Excel file saved successfully!")
