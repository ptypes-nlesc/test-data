from collections import Counter

import pandas as pd
from sweetviz.sv_public import analyze


def my_split(s, counter=None):
    counter.update(s.replace("[u", "").replace("']", "'").replace("u'", "'").split(", "))


if __name__ == "__main__":
    # df = pd.read_csv('xhamster.csv.tar.gz')

    # analyze_report = analyze(df)
    # analyze_report.show_html('xhamster.html', open_browser=True)

    # df = pd.read_csv('xnxx.csv.tar.gz')
    # df['n_tags'] = df['tags'].apply(len)

    # counter = Counter()
    # df['tags'].apply(my_split, counter=counter)

    # with open('tags_counts.txt', 'w') as f:
    #     for l in zip(counter.keys(), counter.values()):
    #         f.write("%s\t%i\n" % (l[0], l[1]))

    # analyze_report = analyze(df)
    # analyze_report.show_html('xnxx.html', open_browser=True)
    
    # pornohub
    df = pd.read_csv('porn-with-dates-2022.csv')
    df['n_tags'] = df['categories'].apply(len)

    counter = Counter()
    df['categories'].apply(my_split, counter=counter)

    with open('pornohub_tags_counts.txt', 'w') as f:
        for l in zip(counter.keys(), counter.values()):
            f.write("%s\t%i\n" % (l[0], l[1]))
