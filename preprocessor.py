import re
import pandas as pd
import numpy as np

def preprocess(data):
    data = data.translate({ord('\u200e'): None, ord('\ufeff'): None}).strip()
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},?\s\d{1,2}:\d{2}\s?[APap][Mm]\s-\s)'
    messages = re.split(pattern, data)
    
    if len(messages) < 3:
        return pd.DataFrame() 

    dates = [d.strip(' -') for d in messages[1::2]]
    messages_raw = messages[2::2]
    
    df = pd.DataFrame({'user_message': messages_raw, 'message_date': dates})
    df['date'] = pd.to_datetime(
        df['message_date'], 
        format='mixed', 
        dayfirst=True,
        errors='coerce'
    )
    
    df.drop(columns=['message_date'], inplace=True)
    df.dropna(subset=['date'], inplace=True)
    if df.empty:
        return pd.DataFrame()

    pattern_user_msg = r'^([^:]+?):\s(.*)$'
    extracted = df['user_message'].str.extract(pattern_user_msg, expand=True)

    df['user'] = extracted[0].fillna('group_notification').str.strip()
    df['message'] = extracted[1].fillna(df['user_message']).str.strip()
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year.astype('Int64')
    df['month_num'] = df['date'].dt.month.astype('Int64')
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day.astype('Int64')
    df['hour'] = df['date'].dt.hour.astype('Int64')
    df['minute'] = df['date'].dt.minute.astype('Int64')
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    df['period'] = np.where(
        pd.isna(df['hour']),
        "Unknown",
        df['hour'].astype(str).str.zfill(2) + '-' + 
        ((df['hour'] + 1) % 24).astype(str).str.zfill(2)
    )
    return df.reset_index(drop=True)