import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt



# 1. Connect to your database
engine = create_engine('mysql+pymysql://root:Gingka007pegasus@localhost/logistics_db')

# 2. Pull only 'Delivered' shipments to calculate performance
df = pd.read_sql_query("SELECT * FROM shipments WHERE Status = 'Delivered'", engine)

# 3. Convert dates to a format Python understands
df['ActualDeliveryDate'] = pd.to_datetime(df['ActualDeliveryDate'])
df['ExpectedDeliveryDate'] = pd.to_datetime(df['ExpectedDeliveryDate'])

# 4. Calculate if a shipment was on time
df['is_on_time'] = df['ActualDeliveryDate'] <= df['ExpectedDeliveryDate']

# 5. Group by 'Route' (Origin to Destination) to see which path is slowest
route_perf = df.groupby(['OriginCity', 'DestinationCity']).agg(
    total_shipments=('ShipmentID', 'count'),
    on_time_count=('is_on_time', 'sum')
).reset_index()

# 6. Calculate OTD Percentage
route_perf['OTD_Percent'] = (route_perf['on_time_count'] / route_perf['total_shipments']) * 100

print("--- Route Performance Summary ---")
print(route_perf)

# 7. Save this for your Dashboard
route_perf.to_csv('route_performance.csv', index=False)



# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(route_perf['DestinationCity'], route_perf['OTD_Percent'], color='skyblue')
plt.axhline(y=90, color='red', linestyle='--', label='Target OTD (90%)') # Target Line

plt.title('On-Time Delivery % by Destination')
plt.xlabel('Destination City')
plt.ylabel('OTD %')
plt.ylim(0, 100)
plt.legend()

# Save the chart as an image for your GitHub
plt.savefig('route_efficiency_chart.png')
print("Chart saved as 'route_efficiency_chart.png'!")