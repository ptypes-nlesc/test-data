import matplotlib.pyplot as plt
import pandas as pd


class DataVisualiser:
    def __init__(self, df):
        self.df = df

    def plot_word_count_over_time(self, date_col, text_col):
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        self.df[text_col+'_wordcount'] = self.df[text_col].apply(lambda x: len(str(x).split()))
        df_grouped = self.df.groupby(date_col)[text_col+'_wordcount'].sum().reset_index()

        plt.figure(figsize=(10,6))
        plt.plot(df_grouped[date_col], df_grouped[text_col+'_wordcount'])
        plt.xlabel('Date')
        plt.ylabel('Count of Words in '+text_col)
        plt.title('Count of Words in '+text_col+' Over Time')
        plt.show()

if __name__ == "__main__":
    # Usage
    df = pd.read_csv('xnxx.csv.tar.gz')
    visualizer = DataVisualiser(df)
    visualizer.plot_word_count_over_time('upload_date', 'title')