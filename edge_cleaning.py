import pandas as pd
df = pd.read_csv('your_file.csv')

df.rename(columns={'node_1': '~from', 'node_2': '~to', 'rel_type': '~label'}, inplace=True)

df['~id'] = range(1, len(df) + 1)

df.to_csv('modified_file.csv', index=False)

print("CSV file has been modified and saved as 'modified_file.csv'")
