from datetime import date
import pandas as pd
from send_email import send_email

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (make google sheet private)
current_dir = Path(__file__).resolve().parent
envars = current_dir / ".env"
load_dotenv(envars)

# google sheet details
sheet_id = os.getenv("SHEET_ID")
sheet_name = "Rentals"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

def load_df(url):
    df = pd.read_csv(url) # read google sheet as csv using pandas

    # Split the 'Timestamp' string and keep only the date
    df['Timestamp'] = df['Timestamp'].apply(lambda x: x.split()[0])
    
    # Convert the string to a datetime object, now containing only the date
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

def query_data_and_send_emails(df):
    present = date.today() # get today's date
    email_counter = 0 # count how many outstanding rentals are due

    for index, row in df.iterrows(): # itterate through every row in data frame
        duration = present - row['Timestamp'].date() # calculate how long the rental has been out
        days = duration.days # convert to days
        if (days >= 14) and (row['Returned'] == "no"): # if the rental is overdue and not returned
            send_email(
                subject = "Outstanding Rental",
                name = row['Name'],
                to = row['Email'],
            ) # send email with their name
            email_counter += 1
    return f"Reminders sent: {email_counter}"

df = load_df(url) # load google sheet as data frame
result = query_data_and_send_emails(df) # query data and send emails
print(result)