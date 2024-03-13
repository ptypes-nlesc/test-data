"""
This scipt calculates correlation between the most popular tags (count number > 75% quantile).
It then plots the correlation matrix as a heatmap.
"""

# Adapted from https://ourcodingclub.github.io/tutorials/topic-modelling-python/

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# if __name__ == "__main__":
df = pd.read_csv("porn-with-dates-2022.csv")

# Create 'tags' column from categories
df["tags"] = df.categories.apply(
    lambda x: x.replace("['", "").replace("']", "").replace("'", "").split(", ")
)

# confirm it is a list
# df.tags.apply(lambda tag_list: isinstance(tag_list, list))

# flatten out tags
df_flat_tag = pd.DataFrame(
    [
        tag
        for tag_list in df.tags
        # split single strings into words
        for tag in tag_list
    ],
    columns=["tag"],
)

# number of unique hashtags
df_flat_tag["tag"].unique().size
# 109 unique tags

# count of appearances of each hashtag
popular_tags = (
    df_flat_tag.groupby("tag")
    .size()
    .reset_index(name="counts")
    .sort_values("counts", ascending=False)
    .reset_index(drop=True)
)

# TODO save this plot
popular_tags.head(30).plot(kind="bar", x="tag", y="counts")

# number of times each hashtag appears
counts = df_flat_tag.groupby(["tag"]).size().reset_index(name="counts").counts

# take 3rd quantile to find popular tags
min_appearance = counts.quantile(0.70)

# find popular tags - make into python set for efficiency
popular_tags_set = set(popular_tags[popular_tags.counts >= min_appearance]["tag"])
len(popular_tags_set)
# 28

# make a new column with only the popular tags
df["popular_tags"] = df.tags.apply(
    lambda tag_list: [tag for tag in tag_list if tag in popular_tags_set]
)
len(df)
# 218004

# drop rows without popular hashtag
df_popular_tags = df.loc[df.popular_tags.apply(lambda tag_list: tag_list != [])]

len(df_popular_tags)
# 216801

# still using 99.4% of the data even after dropping rows with tag counts less than 75%
# len(df_popular_tags)/len(df)
# 0.994

df_tags_vector = df_popular_tags.loc[:, ["popular_tags"]]

for tag in popular_tags_set:
    # make columns to encode presence of hashtags
    df_tags_vector["{}".format(tag)] = df_tags_vector.popular_tags.apply(
        lambda tag_list: int(tag in tag_list)
    )

# create a matrix of tags
tag_matrix = df_tags_vector.drop("popular_tags", axis=1)

# calculate the correlation matrix
correlations = tag_matrix.corr()

# plot the correlation matrix
plt.figure(figsize=(10, 10))
sns.heatmap(
    correlations,
    cmap="RdBu",
    vmin=-1,
    vmax=1,
    square=True,
    cbar_kws={"label": "correlation"},
)
plt.savefig("tag_correlation.png")
