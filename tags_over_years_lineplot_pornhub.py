import pandas as pd
import matplotlib.pyplot as plt
import os

# # Enable interactive mode
# plt.ion()

# Read the CSV file
df = pd.read_csv('/Users/michaelgiffin/Dropbox/Rotterdam_PornTypes/github/MRG/data/porn-with-dates-2022.csv')

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Determine the latest year in the dataset
latest_year = int(df['date'].dt.year.max())

# Initialize a dictionary to store the popularity of top tags for the latest year
popularity_latest_year = {}

# Filter data for the latest year
df_latest_year = df[df['date'].dt.year == latest_year]

# Get the total number of views for the latest year
total_views_latest_year = df_latest_year['views'].sum()


# Initialize an empty dictionary to store the total views for each tag
tag_views_latest_year = {}

# Iterate over each row in the latest year DataFrame
for index, row in df_latest_year.iterrows():
    # Convert the string representation of tags to a list
    tags = eval(row['categories'])
    
    # Iterate over each tag in the list
    for tag in tags:
        # Add the number of views associated with the tag to the dictionary
        tag_views_latest_year[tag] = tag_views_latest_year.get(tag, 0) + row['views']

# Convert the dictionary to a pandas Series
tag_views_latest_year = pd.Series(tag_views_latest_year)

# Sort the Series by the total views in descending order
tag_views_latest_year = tag_views_latest_year.sort_values(ascending=False)


# Calculate the percentage of total views for each tag in the latest year
for tag, count in tag_views_latest_year.items():
    percentage = (count / total_views_latest_year) * 100
    popularity_latest_year[tag] = percentage

# Get the top 10 tags for the latest year
top_tags_latest_year = pd.Series(popularity_latest_year).nlargest(10)

# Initialize a dictionary to store the popularity of top tags over all years
popularity_over_years = {}

# Iterate over each tag in the top 10 for the latest year
for tag in top_tags_latest_year.index:
    # Initialize a list to store the popularity of the tag over all years
    popularity_over_years[tag] = []
    
    # Iterate over each year
    for year in range(int(df['date'].dt.year.min()), latest_year + 1):
        # Filter data for the current year
        df_year = df[df['date'].dt.year == year]
        
        # Filter videos that contain the current tag
        videos_with_tag = df_year[df_year['categories'].apply(lambda x: tag in eval(x))]
        
        # Calculate the total number of views for the current tag in the current year
        total_views_year = videos_with_tag['views'].sum()
        
        # Calculate the percentage of total views for the current tag in the current year
        total_views_for_year = df_year['views'].sum()
        tag_percentage_year = (total_views_year / total_views_for_year) * 100
        
        # Append the tag's popularity for the current year to the list
        popularity_over_years[tag].append(tag_percentage_year)

# Plot the popularity of top tags over all years
plt.figure(figsize=(12, 8))
for tag in popularity_over_years:
    plt.plot(range(int(df['date'].dt.year.min()), latest_year + 1), popularity_over_years[tag], label=tag)

plt.xlabel('Year')
plt.ylabel('Percentage of Total Views')
plt.title('Popularity of Top Tags Over Years')
plt.legend()
plt.grid(True)
# Specify the directory path
save_dir = os.path.join('..', 'reports')  # Goes one level above and into 'reports' directory

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# Save the plot in the specified directory
plt.savefig(os.path.join(save_dir, 'pornhub_lineplot.png'))

plt.show()