'''
Data analyser
'''
import tarfile
from io import StringIO

import pandas as pd


class DataAnalyser:
    def __init__(self, tar_file):
        with tarfile.open(tar_file, 'r:gz') as tar:
            csv_file = tar.getnames()[0]
            f = tar.extractfile(csv_file).read().decode('utf-8')
            self.df = pd.read_csv(StringIO(f))

    def print_summary(self):
        print(f"Shape of a dataset {self.df.shape}")
        print(self.df.head())
        print(self.df.describe())

    def print_missing_values(self):
        for col in self.df.columns:
            print(f"{col}: {self.df[col].isna().mean() * 100:.2f}% missing values")

    def print_unique_values(self):
        for col in self.df.select_dtypes(include=['object']).columns:
            print(f"{col}: {self.df[col].nunique()} unique values")
            print(f"{col}: Most common: {self.df[col].mode()[0]}, Least common: {self.df[col].value_counts().idxmin()}")

    def print_word_counts(self):
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].astype(str)
            self.df[col+'_wordcount'] = self.df[col].apply(lambda x: len(str(x).split()))
            print(f"{col}: {self.df[col+'_wordcount'].sum()} words")

# Usage
# analyzer = DataAnalyser('xhamster.csv.tar.gz')
analyzer = DataAnalyser('xnxx.csv.tar.gz')
analyzer.print_summary()
analyzer.print_missing_values()
analyzer.print_unique_values()
analyzer.print_word_counts()
