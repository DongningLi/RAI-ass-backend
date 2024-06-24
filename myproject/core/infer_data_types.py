import re
import numpy as np
import pandas as pd
from requests import Response
from rest_framework import status

def read_file(df, sample_size):

    # total rows of file
    total_rows = len(df)

    # if file too large, return random sample_size rows
    if total_rows <= sample_size:
        return df
    else:
        return df.sample(n=sample_size, random_state=1)

# detect if a number could be converted to integer
def can_convert_to_int(df_sample_col):
    # Drop NA values and check if any remaining value is a float
    return df_sample_col.dropna().apply(lambda x: float(x).is_integer()).all()

# detect if a number could be converted to timedelta
def convert_single_duration(duration):
    
    match = re.match(r'(\d+)\s*(days?|hours?|minutes?|seconds?|weeks?|months?|years?)', duration)

    if not match:
        return np.nan
    value, unit = match.groups()
    value = int(value)
    
    # Convert to the corresponding timedelta format
    if unit == 'days':
        return pd.to_timedelta(value, unit='days')
    elif unit == 'hours':
        return pd.to_timedelta(value, unit='hours')
    elif unit == 'minutes':
        return pd.to_timedelta(value, unit='minutes')
    elif unit == 'seconds':
        return pd.to_timedelta(value, unit='seconds')
    elif unit == 'weeks':
        return pd.to_timedelta(value, unit='W')
    elif unit == 'months':
        # Approximate a month as 30 days
        return pd.to_timedelta(value * 30, unit='days')
    elif unit == 'years':
        # Approximate a year as 365 days
        return pd.to_timedelta(value * 365, unit='days')
    else:
        return np.nan
    

# detect possible type
def detect_col_type(df_sample_col, category_threshold, belief_threshold):
    
    # Check if col should be boolean
    if df_sample_col.dropna().isin([True, False, 'True', 'False', 'TRUE', 'FALSE', 'yes', 'no', 'T', 'F', 't', 'f', '1', '0']).all():
        return "bool"

    # Check if the column should be categorical
    if len(df_sample_col.unique()) / len(df_sample_col) < category_threshold:
        return "category"


    # Attempt to convert to numeric
    try:
        df_converted = pd.to_numeric(df_sample_col.str.replace(',', ''), errors='raise')
        if df_converted.isna().sum().sum() <= belief_threshold * df_converted.size:
            if can_convert_to_int(df_converted):
                return "int64"
            else:
                return "float64"
    except :
        try:
            df_converted = pd.to_numeric(df_sample_col, errors='raise')
            if df_converted.isna().sum().sum() <= belief_threshold * df_converted.size:
                if can_convert_to_int(df_converted):
                    return "int64"
                else:
                    return "float64"
        except:
            pass

    # Attempt to convert to complex
    try:
        df_converted = df_sample_col.apply(complex)
        if df_converted.isna().sum().sum() <= belief_threshold * df_converted.size:
           return "complex"
    except :
        pass

    # Attempt to convert to datetime
    try:
        df_converted = pd.to_datetime(df_sample_col, errors='coerce')
        if df_converted.isna().sum().sum() <= belief_threshold * df_converted.size:
           return 'datetime64[ns]'
    except:
        pass
        
    # Attempt to convert to timedelta
    try:
        df_converted= df_sample_col.apply(convert_single_duration)
        if df_converted.isna().sum().sum() <= belief_threshold * df_converted.size:
            return 'timedelta64[ns]'
    except :
        pass
            
    return "object"


def detect_type(df_sample):

    category_threshold = 0.5
    belief_threshold = 0.5
    # detect type of column from sample
    column_types = {col: detect_col_type(df_sample[col], category_threshold, belief_threshold) for col in df_sample.columns}
    
    return column_types

#assign type 
def infer_type(df,column_types):

    for col in df.columns:
        if (column_types[col] == "bool"):
            df[col] = df[col].replace({'true': True, 'false': False, 'yes': True, 'no': False, 't': True, 'f': False, '1': True, '0': False, 'T': True, 'F': False,})
            df[col] = df[col].astype(column_types[col])
            continue

        if (column_types[col] == "timedelta64[ns]" or "complex"):
            continue
    
        try:
            df[col] = df[col].str.astype(column_types[col])
            continue
        except:

            try:
                df[col] = df[col].str.replace(',', '').fillna(0).astype(column_types[col])
                continue
            except:
                try:
                    df[col] = df[col].apply(convert_single_duration)
                    continue
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return df