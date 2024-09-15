import csv

# File paths
input_file = 'data/all-time.csv'
output_file = 'data/SAI_bridged.csv'

# Conditions for filtering rows
target_assets_out = ['SAI', 'DAI']
target_to_address = '0x4aa42145aa6ebf72e164c9bbc74fbd3788045016'


# Function to search for specific bridge transfers and write the output to a new CSV file
def search_and_create_output(input_file, output_file, target_assets, target_to_address):
    # Open the input CSV file
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # Prepare the output CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            # Use the same columns as the input CSV
            output_columns = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=output_columns)
            writer.writeheader()

            # Iterate through rows in the input file
            for row in reader:
                # Check if the row meets the conditions
                if row['Asset OUT - Asset'] in target_assets and row['Asset OUT - To Address'] == target_to_address:
                    new_row = {key: '' for key in reader.fieldnames}  # Initialize all fields to empty
                    new_row['Asset IN  - Asset'] = 'XDAI'
                    new_row['Network'] = 'Gnosis'
                    new_row['Asset IN  - Quantity'] = row['Asset OUT - Quantity']
                    new_row['Address'] = row['Address']
                    new_row['Date'] = row['Date']
                    new_row['Tx hash'] = row['Tx hash']

                    writer.writerow(new_row)

    print(f"Filtered rows have been written to {output_file}")


# Main function to orchestrate the process
def main():
    # Define assets and addresses to search for
    search_and_create_output(input_file, output_file, target_assets_out, target_to_address)


# Call the main function
if __name__ == "__main__":
    main()

