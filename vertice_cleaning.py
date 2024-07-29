import pandas as pd
import re

# Load the CSV file into a DataFrame
df = pd.read_csv('your_file.csv')

# Rename columns
df.rename(columns={'n.labels': '~label', 'n.id': '~id'}, inplace=True)

# Function to clean the values in the n.labels column
def clean_label(label):
    # Extract the value from ["value"] to value
    match = re.match(r'\["(.*)"\]', label)
    return match.group(1) if match else label

# Apply the function to the ~label column
df['~label'] = df['~label'].apply(clean_label)

# Save the modified DataFrame back to a CSV file
df.to_csv('modified_file.csv', index=False)

print("CSV file has been modified and saved as 'modified_file.csv'")
