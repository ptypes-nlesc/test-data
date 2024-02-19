"""
Check whether there is at least one video a day
"""

import pandas as pd

def calculate_consecutive_upload(file_path):
    """
    Calculate the percentage of videos uploaded on consecutive days.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    float: The percentage of videos uploaded on consecutive days.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return  
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Calculate the difference between consecutive dates and convert to days
    df['date_diff'] = df['date'].diff().dt.days
    percentage_consecutive = 1 - len(df[df['date_diff'] != 0]) / len(df)

    print(f"{percentage_consecutive:.2%} videos were uploaded on consecutive days")

calculate_consecutive_upload('porn-with-dates-2022.csv')
