import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file extensions that are considered code files
code_extensions = ['.py', '.java', '.js', '.cpp', '.h', '.c', '.rb', '.go']

# Read the updated CSV file
df = pd.read_csv('CLI11_results\\updated_commits_info.csv')

# Function to categorize based on file extension
def is_code(file_path):
    if type(file_path) == float:
        return False
    return any(file_path.lower().endswith(ext) for ext in code_extensions)

# Prepare data for plotting
match_counts = []

# Count matches and no matches for code artifacts
code_matches = df[df['Matches'] == 'Yes'][df['New file path'].apply(is_code)].shape[0]
code_no_matches = df[df['Matches'] == 'No'][df['New file path'].apply(is_code)].shape[0]
match_counts.append(('Code', 'Matches', code_matches))
match_counts.append(('Code', 'No Matches', code_no_matches))

# Count matches and no matches for non-code artifacts
non_code_matches = df[df['Matches'] == 'Yes'][df['New file path'].apply(lambda x: not is_code(x))].shape[0]
non_code_no_matches = df[df['Matches'] == 'No'][df['New file path'].apply(lambda x: not is_code(x))].shape[0]
match_counts.append(('Non-Code', 'Matches', non_code_matches))
match_counts.append(('Non-Code', 'No Matches', non_code_no_matches))

# Print results
print(f"Code Artifacts - Matches: {code_matches}, No Matches: {code_no_matches}")
print(f"Non-Code Artifacts - Matches: {non_code_matches}, No Matches: {non_code_no_matches}")


# Create a DataFrame for the plotting
plot_df = pd.DataFrame(match_counts, columns=['Artifact Type', 'Match Type', 'Count'])

# Plot the results
plt.figure(figsize=(8, 6))
ax = sns.barplot(x='Artifact Type', y='Count', hue='Match Type', data=plot_df, dodge=True)
plt.title('Matches for Code and Non-Code Artifacts')
plt.ylabel('Count')
plt.xlabel('Artifact Type')

# Add the values on top of the bars
for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', fontsize=12, color='black', fontweight='bold', xytext=(0, 8), textcoords='offset points')


plt.show()
