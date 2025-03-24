import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from shapely import affinity
import matplotlib as mpl

# --- STEP 1: Set Font to Arial ---
mpl.rcParams['font.family'] = 'Arial'

# --- STEP 2: Load Data ---
df = pd.read_excel('EVSE_Stations_By_State.xlsx')
usa_states = gpd.read_file('us-states.json')

# --- STEP 3: Merge Data ---
merged = usa_states.set_index('name').join(df.set_index('State'))

# --- STEP 4: Define Colors ---
def get_color(val):
    if pd.isnull(val):
        return '#f0f0f0'  # Light grey for missing data
    elif val < 1:
        return '#d73027'  # Red
    elif 1 <= val <= 5:
        return '#fee08b'  # Light yellow
    elif 5 < val <= 10:
        return '#a6d96a'  # Lighter green
    else:
        return '#1a9850'  # Dark green

merged['color'] = merged['EVSEs/100 miles'].apply(get_color)

# --- STEP 5: Transform Alaska & Hawaii ---
alaska_geom = merged.loc['Alaska', 'geometry']
alaska_geom = affinity.scale(alaska_geom, xfact=0.35, yfact=0.35, origin='center')
alaska_geom = affinity.translate(alaska_geom, xoff=20, yoff=-20)
merged.loc['Alaska', 'geometry'] = alaska_geom

hawaii_geom = merged.loc['Hawaii', 'geometry']
hawaii_geom = affinity.scale(hawaii_geom, xfact=1.5, yfact=1.5, origin='center')
hawaii_geom = affinity.translate(hawaii_geom, xoff=30, yoff=10)
merged.loc['Hawaii', 'geometry'] = hawaii_geom

# --- STEP 6: Plot the Map ---
fig, ax = plt.subplots(figsize=(15, 10))
merged.plot(color=merged['color'], linewidth=0.8, edgecolor='black', ax=ax)
ax.axis('off')
# --- STEP 7: Add State Abbreviations ---
state_abbreviations = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

# Loop through states to place text
for idx, row in merged.iterrows():
    if idx in state_abbreviations:
        centroid = row['geometry'].centroid  # Find the center of each state
        ax.text(centroid.x, centroid.y, state_abbreviations[idx],
                fontsize=10, ha='center', va='center', color='black', fontweight='bold')

# --- STEP 8: Add Title and Legend ---
ax.set_title('Public EV Charger Station Density in the U.S. (2024)',
             fontdict={'fontsize': 18, 'fontweight': 'bold', 'color': '#333333'},
             pad=20)
fig.text(
    0.5, 0.83,  # Adjust Y-coordinate to move it below title
    "(Stations per 100 miles of public road lanes)", 
    fontsize=14, color='gray', ha='center'
)

legend_patches = [
    mpatches.Patch(color='#d73027', label='< 1 Charger'),
    mpatches.Patch(color='#fee08b', label='1-5 Chargers'),
    mpatches.Patch(color='#a6d96a', label='5-10 Chargers'),
    mpatches.Patch(color='#1a9850', label='10+ Chargers'),
    #mpatches.Patch(color='#f0f0f0', label='No Data')
]

ax.legend(handles=legend_patches, loc='best', fontsize=10, title='Public EV Charger Density')
fig.text(
    0.1, 0.3,  
    "Source: U.S. Department of Energy & Department of Transportation",
    fontsize=10, color='gray', ha='left', va='center'
)

# --- STEP 9: Save and Show Map ---
fig.set_facecolor('#f7f7f7')
plt.tight_layout()
plt.savefig('EVSE_Stations_Map_with_Labels.png', dpi=300)
plt.show()
