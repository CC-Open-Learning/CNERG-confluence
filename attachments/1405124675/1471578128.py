import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Read CSV file
df = pd.read_csv("datas_nov_8_435pm.csv")

# Convert time format and localize to UTC
df['Time'] = pd.to_datetime(df['Time'], format='%Y%m%d%H').dt.tz_localize('UTC')

# Verify the time column for debugging
print(df[['Time', 'Enter', 'Out']])  # This line prints the time to check for correct conversion

# Add Door ID and Room ID
df['Door ID'] = 0  # Set desired Door ID value
df['Room ID'] = '3G26-4'  # Set desired Room ID value

# Configure InfluxDB 2.x client
client = InfluxDBClient(
    org="VARLab",
    token="CDj8Q2q6CJlReX7vYUfdXqbC2lKdJvJ4YogZnUVRYHTPDKxmvTHT0qlKQH52O_eY-CBx_3j5C9hBsQy64hk-dA==",
    url="http://cnerg-data.canadacentral.cloudapp.azure.com:8086"
)

# Use Write API to upload data
write_api = client.write_api(write_options=SYNCHRONOUS)

# Upload data
for _, row in df.iterrows():
    point = (
        Point("foot_traffic")
        .time(row['Time'], WritePrecision.S)  # Set to second precision without formatting
        .tag("Door_id", str(row['Door ID']))
        .tag("Room_id", row['Room ID'])
        .field("In", row['Out'])
        .field("Out", row['Enter'])
    )
    write_api.write(bucket="foot_traffic_db", org="VARLab", record=point)

print("Data upload complete.")

# Close client
client.close()
