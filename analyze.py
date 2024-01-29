import pandas as pd
from sweetviz.sv_public import analyze


if __name__ == "__main__":
    df = pd.read_csv('xhamster.csv.tar.gz')
    df['n_tags'] = df['tags'].apply(len)

    analyze_report = analyze(df)
    analyze_report.show_html('xhamster.html', open_browser=True)

    df = pd.read_csv('xnxx.csv.tar.gz')

    analyze_report = analyze(df)
    analyze_report.show_html('xnxx.html', open_browser=True)
