import pandas as pd
import matplotlib.pyplot as plt
import calendar
import os

# Read the CSV file
df = pd.read_csv('xhamster.csv')

# Filter out non-date values from the 'date' column
df = df.loc[pd.to_datetime(df['upload_date'], errors='coerce').notnull()]

# # Convert the 'date' column to datetime
# df.loc[:, 'upload_date'] = pd.to_datetime(df['upload_date'])

# Assuming the date format is in YYYY-MM-DD
df['upload_date'] = pd.to_datetime(df['upload_date'], format='%Y-%m-%d')

# Group the data by month and year and calculate the total views for each month
monthly_views = df.groupby([df['upload_date'].dt.year.rename('year'), df['upload_date'].dt.month.rename('month')])['nb_views'].sum().reset_index()

# Reset the index to have separate columns for year and month
monthly_views = monthly_views.reset_index()

# Drop the duplicate index column
monthly_views = monthly_views.drop(columns=['index'])

# Rename the columns for clarity
monthly_views.columns = ['Year', 'Month', 'Total Views']

# Create a pivot table to have months as columns and years as rows
pivot_monthly_views = monthly_views.pivot(index='Year', columns='Month', values='Total Views')

# Plot the total views for each month, with each year represented as a different colored line
plt.figure(figsize=(12, 8))
for year in pivot_monthly_views.index:
    plt.plot(pivot_monthly_views.columns, pivot_monthly_views.loc[year], label=str(year))

plt.xlabel('Month')
plt.ylabel('Total Views')
plt.title('Total Views of Each Month Across Years')
plt.legend()
plt.grid(True)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# # Specify the directory path
# save_dir = os.path.join('..', 'reports')  # Goes one level above and into 'reports' directory

# # Create the directory if it doesn't exist
# os.makedirs(save_dir, exist_ok=True)

# # Save the plot in the specified directory
# plt.savefig(os.path.join(save_dir, 'xhamster_views_over_years_lineplot.png'))

plt.show()