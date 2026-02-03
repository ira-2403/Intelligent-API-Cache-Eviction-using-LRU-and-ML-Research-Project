import pandas as pd 
def create_features(df: pd.DataFrame)->pd.DataFrame:
    df["timestamp"]=pd.to_datetime(df["timestamp"])
    df["url_freq"]=df.groupby("url").cumcount()
    df["time_diff"]=(
        df.groupby("url")["timestamp"]
        .diff()
        .dt.total_seconds()
    )
    df["time_diff"]=df["time_diff"].fillna(999999)
    df["cache_hit"]=(df["cache_status"]=="HIT").astype(int)
    df=df.fillna(0)
    return df