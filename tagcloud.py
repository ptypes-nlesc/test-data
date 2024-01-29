from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the sorted tags file
with open('tags_counts_sorted.txt', 'r') as f:
    lines = f.readlines()

tags_counts = {}
for line in lines[:200]:
    tag, count = line.strip().split('\t')
    tags_counts[tag] = int(count)

# Create the word cloud
wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(tags_counts)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()