# Adapted from https://ourcodingclub.github.io/tutorials/topic-modelling-python/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# if __name__ == "__main__":
df = pd.read_csv('porn-with-dates-2022.csv')

# tags
# create tags column as a list
# Create 'tags' column as a list
df['tags'] = df.categories.apply(lambda x: x.replace("['", "").replace("']", "").replace("'", "").split(", "))
# check it is a list
# df.tags.apply(lambda tag_list: isinstance(tag_list, list))

# flatten out tags
df_flat_tag = pd.DataFrame(
    [tag for tag_list in df.tags
     # split single strings into words
    for tag in tag_list],
    columns=['tag'])


# number of unique hashtags
df_flat_tag['tag'].unique().size

# count of appearances of each hashtag
popular_tags = df_flat_tag.groupby('tag').size().reset_index(name='counts').sort_values('counts', ascending=False).reset_index(drop=True)
popular_tags.head(10)
###

# number of times each hashtag appears
counts = df_flat_tag.groupby(['tag']).size().reset_index(name='counts').counts

# plot distribution of populr tags
# define bins for histogram
# TODO redefine bins                              
# my_bins = np.arange(0,counts.max()+2, 5)-0.5

# # plot histogram of tweet counts
# plt.figure()
# plt.hist(counts, bins = my_bins)
# plt.xlabel = np.arange(1,counts.max()+1, 1)
# plt.xlabel('hashtag number of appearances')
# plt.ylabel('frequency')
# plt.yscale('log')
# plt.show()


#####
# take hashtags which appear at least this amount of times
# 30 tags with 10000, 
min_appearance = 10000

# find popular tags - make into python set for efficiency
popular_tags_set = set(popular_tags[
                           popular_tags.counts>=min_appearance
                           ]['tag'])
len(popular_tags_set)

# make a new column with only the popular tags
df['popular_tags'] = df.tags.apply(
            lambda tag_list: [tag for tag in tag_list
                                  if tag in popular_tags_set])
len(df)
# 218004

# drop rows without popular hashtag
df_popular_tags = df.loc[df.popular_tags.apply(lambda tag_list: tag_list !=[])]

len(df_popular_tags)
# 216976

# len(df_popular_tags)/len(df)
#0.995

df_tags_vector = df_popular_tags.loc[:, ['popular_tags']]

for tag in popular_tags_set:
    # make columns to encode presence of hashtags
    df_tags_vector['{}'.format(tag)] = df_tags_vector.popular_tags.apply(
        lambda hashtag_list: int(tag in hashtag_list))
    
tag_matrix = df_tags_vector.drop('popular_tags', axis=1)

# calculate the correlation matrix
correlations = tag_matrix.corr()

# plot the correlation matrix
plt.figure(figsize=(10,10))
sns.heatmap(correlations,
    cmap='RdBu',
    vmin=-1,
    vmax=1,
    square = True,
    cbar_kws={'label':'correlation'})
plt.show()

# title
