import sys
import csv
from pydriller import Repository
import os

# Define the CSV columns
columns = [
    'Old file path', 'New file path', 'SHA', 'Parent SHA', 'Message',
    'Diff-Myers', 'Diff-Hist'
]

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    output_dir = f"{repo_path}_results"
    os.makedirs(output_dir, exist_ok=True)

    # Define the number of commits to process
    last_n = 500

    # Collect the last_n commits for both diff algorithms
    print("Collecting commits for Myers algorithm...")
    commits = list(Repository(repo_path, only_no_merge=True, order='reverse').traverse_commits())
    print("Collecting commits for Histogram algorithm...")
    commits_histogram = list(Repository(repo_path, only_no_merge=True, order='reverse', histogram_diff=True).traverse_commits())

    # Process the last_n commits in chronological order
    commits = commits[:last_n][::-1]
    commits_histogram = commits_histogram[:last_n][::-1]

    rows = []

    for i, (commit, commit_histogram) in enumerate(zip(commits, commits_histogram)):
        print(f"[{i+1}/{len(commits)}] Processing commit {commit.hash}...")

        for modified_file, modified_file_histogram in zip(commit.modified_files, commit_histogram.modified_files):
            # Get diffs for Myers and Histogram algorithms
            diff_myers = modified_file.diff
            diff_histogram = modified_file_histogram.diff

            # Append a row for each modified file
            rows.append([
                modified_file.old_path,  # Old file path
                modified_file.new_path,  # New file path
                commit.hash,  # SHA
                commit.parents[0] if commit.parents else None,  # Parent SHA
                commit.msg,  # Commit message
                diff_myers,  # Diff using Myers
                diff_histogram,  # Diff using Histogram
            ])

    # Write results to a CSV file
    output_file = os.path.join(output_dir, 'commits_info.csv')
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)  # Write header
        writer.writerows(rows)  # Write rows

    print(f"CSV file saved at: {output_file}")

if __name__ == "__main__":
    main()