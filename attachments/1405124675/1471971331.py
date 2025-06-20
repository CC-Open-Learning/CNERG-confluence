from influxdb_client import InfluxDBClient
import pandas as pd

# Configure InfluxDB 2.x client
client = InfluxDBClient(
    org="VARLab",
    token="CDj8Q2q6CJlReX7vYUfdXqbC2lKdJvJ4YogZnUVRYHTPDKxmvTHT0qlKQH52O_eY-CBx_3j5C9hBsQy64hk-dA==",
    url="http://cnerg-data.canadacentral.cloudapp.azure.com:8086"
)

query = 'from(bucket:"foot_traffic_db") |> range(start: 0)'

tables = client.query_api().query(query)

data = []
for table in tables:
    for record in table.records:
        data.append({
            "time": record.get_time(),
            "field": record.get_field(),
            "value": record.get_value(),
            "door_id": record.values.get("door_id"),
            "room_id": record.values.get("room_id"),
        })


df = pd.DataFrame(data)

df.to_csv("all_foot_traffic_data.csv", index=False)

print("Data download complete. File saved as 'all_foot_traffic_data.csv'.")

client.close()
