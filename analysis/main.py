from boto3 import client
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dynamoDB_client = client('dynamodb')

scan_args={
    "TableName": "house-metrics",
    "ProjectionExpression": "#timestamp,#temperature,#humidity",
    "ExpressionAttributeNames": {
        "#timestamp": "timestamp",
        "#temperature": "temperature",
        "#humidity": "humidity",
    }
}

res = dynamoDB_client.scan(**scan_args)


def convert_item_to_dict(item):
    return {
        "timestamp": pd.Timestamp(item["timestamp"]["S"]),
        "temperature": int(item["temperature"]["N"]), 
        "humidity": int(item["humidity"]["N"]),
        } 

items = [convert_item_to_dict(item) for item in res["Items"]]

df = pd.DataFrame(items)

# info
print(df.info())

# 10 first rows of the data frame
print(df.head(10))

# Cleaning & Sorting
df.dropna(inplace=True)
df.sort_values(by=["timestamp"], inplace = True)

temp=df["temperature"]
humidity=df["humidity"]
timestamp=df["timestamp"]
temp_df=pd.DataFrame(temp)
humidity_df=pd.DataFrame(humidity)

# Boxplots
plt.subplot(1,2,1)
plt.title("Temperature Boxplot")
temp_df.boxplot()
plt.ylabel("Degrees (°C)")
plt.subplot(1,2,2)
plt.title("Humidity Boxplot")
humidity_df.boxplot()
plt.ylabel("Percentage (%)")
plt.show()

# Histograms
histograms_fig = plt.figure()

histograms_temp_ax = histograms_fig.add_subplot(2,1,1)
histograms_temp_ax.set_title("Probability Density Function - Temperature")

histograms_temp_ax.set_xlabel("Degrees (°C)")
histograms_temp_ax.set_ylabel("Probability")
histograms_temp_ax.hist(temp, density=True, align='mid', bins='scott')

histograms_humidity_ax = histograms_fig.add_subplot(2,1,2)
histograms_humidity_ax.set_title("Probability Density Function - Humidity")
histograms_humidity_ax.set_xlabel("Percentage (%)")
histograms_humidity_ax.set_ylabel("Probability")
histograms_humidity_ax.hist(humidity_df,density=True, align='mid', bins='scott')

histograms_fig.tight_layout()
plt.show()

# Timeseries
timeseries_fig = plt.figure()
temp_timeseries_ax = timeseries_fig.add_subplot(2,1,1)

temp_timeseries_ax.set_xticks(timestamp)
temp_timeseries_ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y %H:%M'))
temp_timeseries_ax.set_title("Temperature Time-series")
temp_timeseries_ax.plot_date(timestamp, temp, ls='-', marker='o')
temp_timeseries_ax.set_ylabel("Degrees (°C)")
temp_timeseries_ax.grid(True)

humidity_timeseries_ax = timeseries_fig.add_subplot(2,1,2)
humidity_timeseries_ax.set_xticks(timestamp)
humidity_timeseries_ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y %H:%M'))
humidity_timeseries_ax.set_title("Humidity Time-series")
humidity_timeseries_ax.plot_date(timestamp, humidity_df, ls='-', marker='o')
humidity_timeseries_ax.set_ylabel("Percentage (%)")
humidity_timeseries_ax.grid(True)

timeseries_fig.autofmt_xdate(rotation=45)
timeseries_fig.tight_layout()
plt.show()

# Correlation Matrix
print(df.corr())

temp_humidity_linear_fig = plt.figure()
temp_humidity_linear_axes = temp_humidity_linear_fig.add_subplot(1,1,1) 

temp_humidity_linear_axes.grid(True)
temp_humidity_linear_axes.set_axisbelow(True)
temp_humidity_linear_axes.set_title('Scatterplot - Temperature vs Humidity')
temp_humidity_linear_axes.scatter(temp,humidity, marker='o')
temp_humidity_linear_axes.set_xlabel("Degrees (°C)")
temp_humidity_linear_axes.set_ylabel("Percentage (%)")
plt.show()

