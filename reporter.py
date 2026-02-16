import pandas as pd
from sqlalchemy import create_engine
from datetime import date

# 1. Connect to MySQL
# Format: mysql+pymysql://user:password@host/database_name
engine = create_engine('mysql+pymysql://root:Gingka007pegasus@localhost/logistics_db')

# 2. Pull the data into a Dataframe
df = pd.read_sql_query("SELECT * FROM Shipments", engine)
print("Data successfully loaded from MySQL!")





# A. Flag Late Shipments (Already delivered but arrived after expected date)
df['is_late'] = df['ActualDeliveryDate'] > df['ExpectedDeliveryDate']

# B. Identify "Stuck" Shipments (Still in-transit but expected date has passed)
today = date.today()
stuck_shipments = df[(df['Status'] == 'In-Transit') & (df['ExpectedDeliveryDate'] < today)]

# C. Identify Cancelled Shipments
cancelled_shipments = df[df['Status'] == 'Cancelled']





# 4. Generate the Automated Excel Report
with pd.ExcelWriter('Daily_Exception_Report.xlsx', engine='openpyxl') as writer:
    # Tab 1: Action Required (Stuck and Cancelled)
    action_items = pd.concat([stuck_shipments, cancelled_shipments])
    action_items.to_excel(writer, sheet_name='Action_Required', index=False)
    
    # Tab 2: Performance Tracking (Late Shipments)
    late_shipments = df[df['is_late'] == True]
    late_shipments.to_excel(writer, sheet_name='Late_Deliveries', index=False)
    
    # Tab 3: Full Data Audit
    df.to_excel(writer, sheet_name='All_Shipments', index=False)

print("Process Complete! Look for 'Daily_Exception_Report.xlsx' in your folder.")