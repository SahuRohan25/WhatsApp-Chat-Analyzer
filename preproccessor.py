import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    senders = []
    texts = []

    for msg in messages:
        split_msg = msg.split(': ', 1)
        if len(split_msg) == 2:
            senders.append(split_msg[0])
            texts.append(split_msg[1])
        else:
            senders.append("System")
            texts.append(split_msg[0])  # system message like "You added XYZ"

    # Build the DataFrame
    df = pd.DataFrame({
        'DateTime': [d.strip(' -') for d in dates],
        'Sender': senders,
        'Message': texts
    })

    # Convert DateTime to proper datetime format
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%m/%d/%y, %H:%M', errors='coerce')

    # Optional: drop invalid datetime rows
    df.dropna(subset=['DateTime'], inplace=True)

    # Final view
    df

    df['Year'] = df['DateTime'].dt.year
    df['Month'] = df['DateTime'].dt.month_name()
    df['Month_num'] = df['DateTime'].dt.month
    df['Day'] = df['DateTime'].dt.day
    df['day_name'] = df['DateTime'].dt.day_name()
    df['date'] = df['DateTime'].dt.date
    df['Hour'] = df['DateTime'].dt.hour
    df['Minute'] = df['DateTime'].dt.minute

    period = []

    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + '00')
        elif hour == 0:
            period.append('00' + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['Period'] = period

    return df
