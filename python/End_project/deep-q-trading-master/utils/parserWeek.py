import pandas as pd
from datetime import datetime, timedelta

# Read the daily data
spTimeserie = pd.read_csv('datasets/daxDay.csv')

# Create/open the weekly file for writing
with open("datasets/daxWeek.csv", "w") as file:
    file.write("Date,Time,Open,High,Low,Close\n")
    
    # Extract columns
    Date = spTimeserie['Date'].tolist()
    Time = spTimeserie['Time'].tolist()
    Open = spTimeserie['Open'].tolist()
    High = spTimeserie['High'].tolist()
    Low = spTimeserie['Low'].tolist()
    Close = spTimeserie['Close'].tolist()
    Volume = spTimeserie['Volume'].tolist()

    # Create records
    records = []
    for i in range(len(Open)):
        records.append({
            'Date': Date[i],
            'Time': Time[i],
            'Open': Open[i],
            'High': High[i],
            'Low': Low[i],
            'Close': Close[i],
            'Volume': Volume[i]
        })

    # Initialize variables for the first week
    currentDate = datetime.strptime(records[0]['Date'], '%m/%d/%Y')
    delta = timedelta(days=7)
    open_ = records[0]['Open']
    high = records[0]['High']
    low = records[0]['Low']
    close = records[0]['Close']
    volume = records[0]['Volume']

    # Loop through records and aggregate weekly data
    for record in records:
        nextDate = datetime.strptime(record['Date'], '%m/%d/%Y')

        # Update high and low for the week
        high = max(high, record['High'])
        low = min(low, record['Low'])
        close = record['Close']  # Update closing price to the latest for the week
        volume += record['Volume']  # Aggregate volume

        # Check if we have reached or passed a week's time
        if nextDate >= currentDate + delta:
            # Write the weekly summary to the file
            file.write(f"{currentDate.strftime('%m/%d/%Y')},00:00,{open_},{high},{low},{close}\n")
            
            # Reset for the next week
            currentDate = nextDate
            open_ = record['Open']
            high = record['High']
            low = record['Low']
            volume = record['Volume']  # Reset volume for the new week

    # Write the last week's data after the loop finishes
    file.write(f"{currentDate.strftime('%m/%d/%Y')},00:00,{open_},{high},{low},{close}\n")

print("Done")
