import numpy as np
import pandas as pd

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

# detect possible type
def detect_col_type(df_sample_col, category_threshold):

    # Attempt to convert to complex
    try:
        df_converted = df_sample_col.str.replace("i","j").apply(complex)
        if not df_converted.isna().all(): 
           return "complex"
    except (ValueError, TypeError):
        pass

    # Attempt to convert to numeric
    try:
        df_converted = pd.to_numeric(df_sample_col, errors='coerce')
        if not df_converted.isna().all():
            if can_convert_to_int(df_converted):
                return "int64"
            else:
                return "float64"
    except (ValueError, TypeError):
        pass

    # Attempt to convert to datetime
    try:
        df_converted = pd.to_datetime(df_sample_col, errors='coerce')
        if not df_converted.isna().all():
            return 'datetime64[ns]'
    except (ValueError, TypeError):
        pass

    # Attempt to convert to timedelta
    try:
        df_converted = pd.to_timedelta(df_sample_col, errors='coerce')
        if not df_converted.isna().all():
            return 'timedelta64[ns]'
    except (ValueError, TypeError):
        pass

    # Check if the column should be categorical
    if len(df_sample_col.unique()) / len(df_sample_col) < category_threshold:
        return "category"

    # Check if col should be boolean
    if df_sample_col.dropna().isin([True, False, 'True', 'False']).all():
        return "bool"
            
    return "object"

def detect_type(df_sample):

    category_threshold = 0.5
    # detect type of column from sample
    column_types = {col: detect_col_type(df_sample[col], category_threshold) for col in df_sample.columns}
    
    return column_types

#assign type 
def infer_type(df,column_types):
    for col in df.columns:
        try:
            # replace 'Not Available' with np.nan
            df[col] = df[col].replace('Not Available', np.nan).astype(column_types[col])
            continue
        except:
            df[col] = df[col].str.replace("i","j").astype(column_types[col])
            continue

    return df