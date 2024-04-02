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
tags_to_analyze = ["Latina", "Big Ass"]

# Initialize an empty dictionary to store results for each year
yearly_results = {}

# Iterate over each year
for year, year_df in df.groupby("year"):
    # Filter videos with the "Latina" tag for the current year
    df_Latina_yearly = year_df[year_df["tags"].apply(lambda tags: "Latina" in tags)]

    # Calculate total views for videos with the "Latina" tag only for the current year
    total_views_Latina_yearly = df_Latina_yearly["views"].sum()
    
    # Calculate total number of videos with the "Latina" tag only for the current year
    total_videos_Latina_yearly = len(df_Latina_yearly)
    
    # Calculate average views per video for "Latina" tag only
    if total_videos_Latina_yearly != 0:
        average_views_Latina_yearly = total_views_Latina_yearly / total_videos_Latina_yearly
    else:
        average_views_Latina_yearly = 0

    # Filter videos with both "Latina" and "Big Ass" tags for the current year
    df_Latina_big_Ass_yearly = year_df[year_df["tags"].apply(lambda tags: all(tag in tags for tag in tags_to_analyze))]

    # Calculate total views for videos with both "Latina" and "Big Ass" tags for the current year
    total_views_Latina_big_Ass_yearly = df_Latina_big_Ass_yearly["views"].sum()
    
    # Calculate total number of videos with both "Latina" and "Big Ass" tags for the current year
    total_videos_Latina_big_Ass_yearly = len(df_Latina_big_Ass_yearly)
    
    # Calculate average views per video for "Latina" and "Big Ass" tags
    if total_videos_Latina_big_Ass_yearly != 0:
        average_views_Latina_big_Ass_yearly = total_views_Latina_big_Ass_yearly / total_videos_Latina_big_Ass_yearly
    else:
        average_views_Latina_big_Ass_yearly = 0

    # Store results for the current year
    yearly_results[year] = {
        "Latina Only": average_views_Latina_yearly,
        "Latina & Big Ass": average_views_Latina_big_Ass_yearly
    }

# Convert the results to a DataFrame for easy plotting
results_df = pd.DataFrame(yearly_results).transpose()

# Plot barplot to visualize the comparison for each year
results_df.plot(kind="bar", figsize=(10, 6))
plt.title("Average Views Comparison for Videos with 'Latina' and 'Big Ass' Tags")
plt.xlabel("Year")
plt.ylabel("Average Views")
plt.xticks(rotation=45)
plt.legend(title="Tag Combination")
plt.savefig("tag_Latina_BigAss_views.png")
plt.show()
