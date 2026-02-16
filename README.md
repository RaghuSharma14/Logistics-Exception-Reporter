# Automated Shipment Exception Reporter
**Technical Solution for Supply Chain Monitoring**

## Overview
This project automates the identification of delivery exceptions (delays, stuck shipments, and cancellations) using **Python** and **SQL**. It pulls real-time transit data from a MySQL backend and generates actionable Excel reports for Transportation Specialists.

## Key Features
- **Stuck Shipment Logic:** Identifies packages in-transit past their expected delivery date.
- **Automated Reporting:** Generates a multi-tab Excel report with prioritized "Action Required" items.
- **Data Integration:** Built using SQLAlchemy to bridge SQL databases with Python Pandas for analysis.

## Tech Stack
- **Languages:** Python, SQL
- **Libraries:** Pandas, SQLAlchemy, OpenPyXL
- **Database:** MySQL