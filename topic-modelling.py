import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# if __name__ == "__main__":
df = pd.read_csv('porn-with-dates-2022.csv')

# create tags column
df['tags'] = df.categories.apply(lambda x: x.replace("['", "").replace("']", "").replace("'", ""))

# flatten out tags
df_flat_tag = pd.DataFrame(
    [tag for tag_list in df.tags
     # split single strings into words
    for tag in tag_list.split(", ")],
    columns=['tag'])


# number of unique hashtags
df_flat_tag['tag'].unique().size

# count of appearances of each hashtag
popular_tags = df_flat_tag.groupby('tag').size().reset_index(name='counts').sort_values('counts', ascending=False).reset_index(drop=True)


# take hashtags which appear at least this amount of times
min_appearance = 5000

# find popular tags - make into python set for efficiency
popular_tags_set = set(popular_tags[
                           popular_tags.counts>=min_appearance
                           ]['tag'])
len(popular_tags_set)

# make a new column with only the popular tags
df['popular_tags'] = df.tags.apply(
            lambda tag_list: [tag for tag in tag_list
                                  if tag in popular_tags_set])