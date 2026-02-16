import pandas as pd
from sqlalchemy import create_engine

# Connect
engine = create_engine('mysql+pymysql://root:Gingka007pegasus@localhost/logistics_db')

# Load Shipments and Rates
shipments = pd.read_sql("SELECT * FROM shipments", engine)
rates = pd.read_sql("SELECT * FROM carrier_rates", engine)

# Create a 'Route' column in shipments to match the rates table
shipments['Route'] = shipments['OriginCity'] + "-" + shipments['DestinationCity']

# Merge data to see the cost for each shipment
# (Assuming a standard weight of 5KG for this simulation)
merged_df = pd.merge(shipments, rates, on=['CarrierName', 'Route'], how='left')
merged_df['TotalCost'] = merged_df['RatePerKG'] * 5 

# Find the Cheapest Carrier for Delhi-Bangalore
cheapest = rates[rates['Route'] == 'Delhi-Bangalore'].sort_values('RatePerKG').iloc[0]

print(f"--- Cost Analysis ---")
print(f"Recommended Carrier for Delhi-Bangalore: {cheapest['CarrierName']} (₹{cheapest['RatePerKG']}/KG)")

# Export Cost Report
merged_df.to_csv('shipping_cost_audit.csv', index=False)