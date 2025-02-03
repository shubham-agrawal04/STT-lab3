import pandas as pd

# Reading CSV and printing initial first 5 rows
df = pd.read_csv('CLI11_results\\commits_info.csv')
print("CSV Initially")
print(df.columns)
pd.set_option('display.max_columns', None)
print(df.head())

# Add the 'match' column
df['Matches'] = df.apply(lambda row: 'Yes' if row['Diff-Myers'] == row['Diff-Hist'] else 'No', axis=1)


# Printing first 5 rows after updating
print("\nCSV after update")
print(df.columns)
pd.set_option('display.max_columns', None)
print(df.head())


# Getting the counts of 'same' and 'different'
match_counts = df['Matches'].value_counts()
print("Match Column Stats: \n", match_counts)

# Saving the updated DataFrame back to a CSV file
df.to_csv('CLI11_results\\updated_commits_info.csv', index=False)
print('Updated CSV saved to \'CLI11_results\\updated_commits_info.csv\'')


