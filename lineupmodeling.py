# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 10:31:07 2025

@author: natha
"""
import pandas as pd
whitesoxnames = [
    'Lee, Korey',
    'Thaiss, Matt',
    'Quero, Edgar',
    'Teel, Kyle',
    'Vaughn, Andrew',
    'Elko, Tim',
    'Drury, Brandon',
    'Rojas, Josh',
    'Amaya, Jacob',
    'Montgomery, Colson',
    'Baldwin, Brooks',
    'Meidroth, Chase',
    'Vargas, Miguel',
    'Sosa, Lenyn',
    'Ramos, Bryan',
    'Tauchman, Mike',
    'Robert, Luis',
    'Jankowski, Travis',
    'Benintendi, Andrew',
    'Slater, Austin',
    'Fletcher, Dominic',
    'Taylor, Michael',
    'Colas, Oscar'
]
savant24 = pd.read_csv("C:/Users/natha/Documents/BGA/Competitions/WhiteSoxModeling/stats24.csv")
merged = pd.read_csv("C:/Users/natha/Documents/BGA/Competitions/WhiteSoxModeling/merged_data (2).csv")
merged.drop('Unnamed: 0')
print(merged_cleaned.info())
merged_cleaned = merged.copy()
#-----------------------------------------------
"Weighting multi-season data 70 percent towards 2024"
# Set weights
weights = {2023: 0.3, 2024: 0.7}

# Function to apply weighted averaging
def weighted_avg(group):
    if len(group) == 1:
        return group.iloc[0].to_dict()
    
    weighted = {}
    
    for col in ['pa', 'obp', 'woba', 'ba', 'mlb', 'ops', 'xwoba', 'xba', 'xslg', 'k_percent', 'bb_percent']:
        weighted_sum = 0
        total_weight = 0
        for _, row in group.iterrows():
            year = row['year']
            weight = weights.get(year, 0)
            weighted_sum += row[col] * weight
            total_weight += weight
        weighted[col] = weighted_sum / total_weight if total_weight else None
    
    # Add back identifier columns
    weighted['last_name, first_name'] = group.iloc[0]['last_name, first_name']
    weighted['player_id'] = group.iloc[0]['player_id']
    
    return weighted

# Apply the weighted averaging and return a list of dictionaries
weighted_rows = []
for _, group in merged_cleaned.groupby('last_name, first_name'):
    weighted_rows.append(weighted_avg(group))

# Create DataFrame from the weighted rows
merged_weighted = pd.DataFrame(weighted_rows)

# Reorder columns (optional)
cols = ['last_name, first_name', 'player_id'] + [col for col in merged_weighted.columns if col not in ['last_name, first_name', 'player_id']]
merged_weighted = merged_weighted[cols]

# Inspect the result
merged_weighted.info()
merged_weighted.head()

merged_weighted.to_csv(r'C:\Users\natha\Documents\BGA\Competitions\WhiteSoxModeling\merged_weighted.csv', index=False)
#-----------------------------------------------
"Generating rankings"
# Drop the unnecessary columns
merged_cleaned = merged.drop(columns=['last_name, first_name.1'])

# List of columns to rank
rank_columns = [
    'pa', 'obp', 'woba', 'ba', 'mlb', 'ops', 'xwoba', 'xba', 'xslg', 
    'k_percent', 'bb_percent'
]

# Create a rankings DataFrame by ranking each column
rankings = merged_weighted[['last_name, first_name']].copy()

for col in rank_columns:
    if col == 'k_percent':
        # Lower is better
        rankings[col + '_rank'] = merged_weighted[col].rank(ascending=True, method='min')
    else:
        # Higher is better
        rankings[col + '_rank'] = merged_weighted[col].rank(ascending=False, method='min')

# Display rankings
rankings.head()
#------------------------------------------------
# Get a list of just the rank columns (everything except the player name)
rank_cols = [col for col in rankings.columns if col.endswith('_rank')]

# Calculate the average rank across all categories for each player
rankings['average_rank'] = rankings[rank_cols].mean(axis=1)

# Create a new dataframe with just player names and their average rank
average_rankings = rankings[['last_name, first_name', 'average_rank']].copy()

# Optional: sort by average rank (lower is better)
average_rankings = average_rankings.sort_values(by='average_rank').reset_index(drop=True)

# Display the results
average_rankings.head()
# Define your file path
output_path = r'C:\Users\natha\Documents\BGA\Competitions\WhiteSoxModeling\average_rankings.csv'

# Save the dataframe to CSV
average_rankings.to_csv(output_path, index=False)
print(average_rankings)
