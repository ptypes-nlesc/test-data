import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read the CSV file with proper date parsing
df = pd.read_csv("porn-with-dates-2022.csv", parse_dates=["date"], infer_datetime_format=True)

# Create 'tags' column from categories
df["tags"] = df.categories.apply(
    lambda x: x.replace("['", "").replace("']", "").replace("'", "").split(", ")
)

# Flatten out tags
df_flat_tag = pd.DataFrame(
    [
        tag
        for tag_list in df.tags
        for tag in tag_list
    ],
    columns=["tag"],
)

# Count of appearances of each hashtag
popular_tags = (
    df_flat_tag.groupby("tag")
    .size()
    .reset_index(name="counts")
    .sort_values("counts", ascending=False)
    .reset_index(drop=True)
)

# Number of times each hashtag appears
counts = df_flat_tag.groupby(["tag"]).size().reset_index(name="counts").counts

# Take 3rd quantile to find popular tags
min_appearance = counts.quantile(0.70)

# Find popular tags
popular_tags_set = set(popular_tags[popular_tags.counts >= min_appearance]["tag"])

# Make a new column with only the popular tags
df["popular_tags"] = df.tags.apply(
    lambda tag_list: [tag for tag in tag_list if tag in popular_tags_set]
)

# Drop rows without popular hashtag
df_popular_tags = df.loc[df.popular_tags.apply(lambda tag_list: tag_list != [])]

# Extract unique years from the date column
unique_years = df_popular_tags["date"].dt.year.unique()

# Iterate over each year and create correlation matrix and heatmap
for year in unique_years:
    df_year = df_popular_tags[df_popular_tags["date"].dt.year == year]
    
    df_tags_vector = df_year.loc[:, ["popular_tags"]]

    for tag in popular_tags_set:
        # Make columns to encode presence of hashtags
        df_tags_vector["{}".format(tag)] = df_tags_vector.popular_tags.apply(
            lambda tag_list: int(tag in tag_list)
        )

    # Create a matrix of tags
    tag_matrix = df_tags_vector.drop("popular_tags", axis=1)

    # Calculate the correlation matrix
    correlations = tag_matrix.corr()

    # Plot the correlation matrix
    plt.figure(figsize=(10, 10))
    sns.heatmap(
        correlations,
        cmap="RdBu",
        vmin=-0.5,
        vmax=0.5,
        square=True,
        cbar_kws={"label": "correlation"},
    )
    plt.title(f"Correlation Matrix for Popular Tags in {year}")
    plt.savefig(f"tag_correlation_{year}.png")
    plt.close()
