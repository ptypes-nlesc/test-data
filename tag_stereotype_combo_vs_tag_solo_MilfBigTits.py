import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file with proper date parsing
df = pd.read_csv("porn-with-dates-2022.csv", parse_dates=["date"], infer_datetime_format=True)

# Create 'tags' column from categories
df["tags"] = df.categories.apply(
    lambda x: x.replace("['", "").replace("']", "").replace("'", "").split(", ")
)

# Extract year from the date column
df["year"] = df["date"].dt.year

# Define the tags to analyze
tags_to_analyze = ["MILF", "Big Tits"]

# Initialize an empty dictionary to store results for each year
yearly_results = {}

# Iterate over each year
for year, year_df in df.groupby("year"):
    # Filter videos with the "MILF" tag for the current year
    df_MILF_yearly = year_df[year_df["tags"].apply(lambda tags: "MILF" in tags)]

    # Calculate total views for videos with the "MILF" tag only for the current year
    total_views_MILF_yearly = df_MILF_yearly["views"].sum()
    
    # Calculate total number of videos with the "MILF" tag only for the current year
    total_videos_MILF_yearly = len(df_MILF_yearly)
    
    # Calculate average views per video for "MILF" tag only
    if total_videos_MILF_yearly != 0:
        average_views_MILF_yearly = total_views_MILF_yearly / total_videos_MILF_yearly
    else:
        average_views_MILF_yearly = 0

    # Filter videos with both "MILF" and "Big Tits" tags for the current year
    df_MILF_big_tits_yearly = year_df[year_df["tags"].apply(lambda tags: all(tag in tags for tag in tags_to_analyze))]

    # Calculate total views for videos with both "MILF" and "Big Tits" tags for the current year
    total_views_MILF_big_tits_yearly = df_MILF_big_tits_yearly["views"].sum()
    
    # Calculate total number of videos with both "MILF" and "Big Tits" tags for the current year
    total_videos_MILF_big_tits_yearly = len(df_MILF_big_tits_yearly)
    
    # Calculate average views per video for "MILF" and "Big Tits" tags
    if total_videos_MILF_big_tits_yearly != 0:
        average_views_MILF_big_tits_yearly = total_views_MILF_big_tits_yearly / total_videos_MILF_big_tits_yearly
    else:
        average_views_MILF_big_tits_yearly = 0

    # Store results for the current year
    yearly_results[year] = {
        "MILF Only": average_views_MILF_yearly,
        "MILF & Big Tits": average_views_MILF_big_tits_yearly
    }

# Convert the results to a DataFrame for easy plotting
results_df = pd.DataFrame(yearly_results).transpose()

# Plot barplot to visualize the comparison for each year
results_df.plot(kind="bar", figsize=(10, 6))
plt.title("Average Views Comparison for Videos with 'MILF' and 'Big Tits' Tags")
plt.xlabel("Year")
plt.ylabel("Average Views")
plt.xticks(rotation=45)
plt.legend(title="Tag Combination")
plt.savefig("tag_MILF_BigTits_views.png")
plt.show()
