import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('porn-with-dates-2022.csv')

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Determine the latest year in the dataset
latest_year = int(df['date'].dt.year.max())

# Initialize a dictionary to store the popularity of top tags for the latest year
popularity_latest_year = {}
popularity_latest_year_raw = {}

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
    popularity_latest_year_raw[tag] = count
    popularity_latest_year[tag] = percentage

# Get the top 10 tags for the latest year
top_tags_latest_year = pd.Series(popularity_latest_year).nlargest(10)
top_tags_latest_year_raw = pd.Series(popularity_latest_year_raw).nlargest(10)


# Print distribution of views among the top tags in the latest year
print(f"Top 10 tags in {latest_year}:")
top_tags = []
top_views = []
other_views = 0

# Iterate over (tag, views) pairs in the top tags Series
for tag, views in top_tags_latest_year_raw.items():
    percentage = (views / total_views_latest_year) * 100
    print(f"{tag}: {views} views ({percentage:.2f}% of total)")
    top_tags.append(tag)
    top_views.append(percentage)

# Initialize a set to store video IDs associated with top 10 tags
videos_with_top_tags = set()

# Iterate over the top tags to collect video IDs
for tag in top_tags_latest_year_raw.index:
    # Get the DataFrame rows where the tag appears
    rows_with_tag = df_latest_year[df_latest_year['categories'].str.contains(tag)]
    # Add the IDs of these rows to the set
    videos_with_top_tags.update(rows_with_tag['url'])

# Calculate the total views for 'other' tags
other_views = df_latest_year[~df_latest_year['url'].isin(videos_with_top_tags)]['views'].sum()

top_tags.append('Other')
percentage_other = (other_views / total_views_latest_year) * 100
top_views.append(percentage_other)
print(f"Other: {other_views} views ({percentage_other:.2f}% of total)")

# Plot distribution of views among the top tags in the latest year
plt.figure(figsize=(10, 6))
plt.bar(top_tags, top_views)
plt.xlabel('Tags')
plt.ylabel('Number of Views (%)')
plt.title(f'Distribution of Views Among Top Tags in {latest_year}')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
