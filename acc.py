# prints a list of unique assets in a csv file that has been exported from Octav

import csv

data_file = "data/2022-row.csv"
asset_in_name_column = 14
asset_out_name_column = 29
in_nft_id_column = 16

with open(data_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    # print(sum(1 for row in reader))
    next(reader)  # Skip the first line (header)
    unique_strings = sorted(set(row[asset_in_name_column] for row in reader if row[asset_in_name_column].strip() and not row[in_nft_id_column].strip()))

print(unique_strings)

