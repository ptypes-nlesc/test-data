import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.stats import linregress

# Read the CSV file
df = pd.read_csv('porn-with-dates-2022.csv')

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Determine the unique tags in the dataset
unique_tags = set()
for categories in df['categories']:
    unique_tags.update(eval(categories))

# Determine the unique years in the dataset
unique_years = sorted(df['date'].dt.year.unique())

# Initialize a dictionary to store the p-values of linear regression for each tag
tag_stats = {}

# Iterate over each tag
for tag in unique_tags:
    # Initialize lists to store years and normalized views
    years = []
    normalized_views = []
    
    # Iterate over each year
    for year in unique_years:
        # Print out progress for the researchers own sanity
        print(f'Running on tag "{tag}" in year {year}')
        
        # Filter data for the current year
        total_year_data = df[(df['date'].dt.year == year)]
        
        # Calculate total views for the current year
        total_year_views = total_year_data['views'].sum()
        
        # Filter data for the current tag and year
        tag_year_data = df[(df['date'].dt.year == year) & df['categories'].apply(lambda x: tag in eval(x))]
        
        # Calculate total views for current tag in current year
        tag_year_views = tag_year_data['views'].sum()
        
        # Append the year
        years.append(year)
        
        # Append the normalized views for the current year
        normalized_views.append(tag_year_views / total_year_views if total_year_views != 0 else 0)
    
    # Perform linear regression on years and normalized views
    slope, _, r_value, p_value, _ = linregress(years, normalized_views)
    
    # Store the statistics of linear regression for the current tag
    tag_stats[tag] = {'slope': slope, 'r_value': r_value, 'p_value': p_value}


# Save the list of significant tags along with their statistics to a tab-delimited file
significant_tags = []
with open('significant_tags.txt', 'w') as file:
    file.write('Tag\tSlope\tR Value\tP Value\n')
    for tag, stats in tag_stats.items():
        if stats['p_value'] < 0.05:
            file.write(f"{tag}\t{stats['slope']}\t{stats['r_value']}\t{stats['p_value']}\n")
            significant_tags.append(tag)

print("Tags with significant changes in view count over years:")
for tag in significant_tags:
    print(tag)
