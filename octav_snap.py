# creates a snapshot of wallet assets that were held at the end of the range of the Octav CSV report

import pandas as pd

# Octav CSV reports encode `12345` as `"12,345" so numbers need to be cleaned by removing commas and quotes
def clean_number(val):
    # Remove commas and quotes from the string and convert it to a float
    try:
        return float(val.replace(',', '').replace('"', ''))
    except ValueError:
        return val  # If it's not a valid number, return the value as is (e.g., for non-numeric data)


# Load the CSV file
df = pd.read_csv('data/all-time.csv', nrows=100000, converters={'Asset IN  - Quantity': clean_number, 'Asset OUT - Quantity': clean_number})
df['Asset IN  - Quantity'] = pd.to_numeric(df['Asset IN  - Quantity'], errors='coerce')
df['Asset OUT - Quantity'] = pd.to_numeric(df['Asset OUT - Quantity'], errors='coerce')

# Set display option to show all rows
pd.set_option('display.max_rows', None)

# Group incoming assets and sum quantities
incoming_totals = df.groupby('Asset IN  - Asset')['Asset IN  - Quantity'].sum()

# Group outgoing assets and sum quantities
outgoing_totals = df.groupby('Asset OUT - Asset')['Asset OUT - Quantity'].sum()
"""
print("Incoming assets and quantities:")
print(df[['Asset IN  - Asset', 'Asset IN  - Quantity']])

print("Outgoing assets and quantities:")
print(df[['Asset OUT - Asset', 'Asset OUT - Quantity']])

print("Incoming totals:")
print(incoming_totals)

print("Outgoing totals:")
print(outgoing_totals)
"""
# Combine both by subtracting outgoing from incoming
all_assets = pd.concat([incoming_totals, outgoing_totals], axis=1, keys=['Incoming', 'Outgoing']).fillna(0)
all_assets['Balance'] = all_assets['Incoming'] - all_assets['Outgoing']

# Filter out rows where 'Balance' is zero
filtered_assets = all_assets[all_assets['Balance'] != 0]

# Set the float format to display numbers with two decimal places (you can adjust this as needed)
pd.options.display.float_format = '{:,.2f}'.format

# Display the final balance per asset
print(filtered_assets[['Balance']])

"""

# Filter rows where there's an OUT transaction for a specific asset
out_asset = 'XDAI'  # Replace with the actual asset name
out_df = df[df['Asset OUT - Asset'] == out_asset]

# Now for each row in the OUT dataframe, check if there's a corresponding IN transaction for the same address
# Get all addresses involved in the OUT transactions
addresses_with_out = out_df['Address'].unique()

# Filter rows where those addresses appear in an IN transaction
in_df = df[(df['Address'].isin(addresses_with_out)) & (df['Asset IN  - Asset'] == out_asset)]

# Now merge or join these two DataFrames based on the Address column (to find matching addresses)
result_df = pd.merge(out_df, in_df, on='Address', suffixes=('_OUT', '_IN'))
result_df = result_df.drop_duplicates(subset=['Address'])
pd.set_option('display.max_columns', None)

# Show the result
print(result_df[['Address', 'Tx url_OUT', 'Network_OUT', 'Date_OUT']])
#print(result_df.columns)
"""
