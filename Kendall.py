import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load the CSV dataset into a Pandas DataFrame
df = pd.read_csv('data/merged_dataset.csv')

df = df[(df['MONTH'] > '2021-01-01')] #use this to keep data that is before a given date


# Calculate the Kendall correlation matrix
corr = df.corr(method='kendall')

# Generate a heatmap of the correlation matrix using Seaborn
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.show()