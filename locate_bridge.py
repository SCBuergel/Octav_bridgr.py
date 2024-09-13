# Loads an Octav Snapshot CSV report file and locates addresses which have OUTgoing asset transfers before they received the same asset on the same network. That is a way to identify bridge transfers which Octav didn't catch

"""
ANSATZ:
    1.  Identify dangling OUTgoing transfers that cannot make sense as they are missing a prior funding transaction. That can be done from the output of this script, you can see the first OUTgoing tx of an asset, e.g. an XDAI transfer. e.g.: https://gnosisscan.io/tx/0x5a50c24005dd6db031ac62cb36968b776b41db1e570323f2de0bef0f2b608799
    2. Find the last OUTgoing transaction of that account (most likely but not necessarily!) on mainnet and with the corresponding asset (e.g. DAI or SAI correspond to XDAI). E.g.: https://etherscan.io/tx/0x9e7686152e3dee08ad33e0a63b49f4c13d90547656342a10574f4d132648d4d8/
    2. Identify outgoing bridge contract on mainnet by looking at the transaction that was identified above. The recipient smart contract address is listed in column `Asset OUT - To Address` on the Octav CSV. E.g.: 0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016
    3. Understand bridge logic on mainnet side. E.g. how is the recipient encoded from the transaction payload? For SAI on mainnet going into the xDAI bridge, it's normal ERC20 transfers that are issued to the same address on Gnosis Chain
    4. Automate the bridge transaction loading. E.g. for SAI, parse all SAI transfers going into the xDAI bridge on Ethereum mainnet and create new entries which are compatible with the Octav CSV format.
    5. Prepend all these bridge transactions into a copy of the original Octav CSV.
    6. Repeat from step (1) for the next bridge.
"""

import csv

# File path
csv_file = 'data/all-time.csv'

# Dictionary to keep track of asset transfers IN
address_asset_in = {}

# Open and read the CSV file
with open(csv_file, mode='r') as file:
    reader = csv.DictReader(file)
    
    row_number = 0
    
    # Loop through each row in the CSV
    for row in reader:
        row_number += 1
        
        # Extract relevant columns
        address = row['Address']
        network = row['Network']
        asset_in_quantity = row['Asset IN  - Quantity']
        asset_in_asset = row['Asset IN  - Asset']
        asset_out_quantity = row['Asset OUT - Quantity']
        asset_out_asset = row['Asset OUT - Asset']
        
        # Only process rows with valid address, network, and asset data
        if not address or not network:
            continue
        
        # Check if this row is an OUT transfer
        if asset_out_quantity and asset_out_asset:
            # Check if the same address and network has a previous IN transfer of the same asset
            key = (address, network, asset_out_asset)
            if key not in address_asset_in:
                print(f"Line {row_number}: Asset OUT transfer of {asset_out_asset} before an IN transfer for the same asset.")
        
        # Store the IN transfer for this address, network, and asset
        if asset_in_quantity and asset_in_asset:
            key = (address, network, asset_in_asset)
            address_asset_in[key] = row_number

