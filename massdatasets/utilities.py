import re
import pandas as pd


def join_dsd100_and_mus2016_dataframes(df_dsd, df_mus):
    "Combine DSD100 and MUS2016 pandas data frames"

    df_dsd = dsd100_with_method_and_trackid(df_dsd)

    # Remove songs from DSD100 not included in MUS2016
    track_ids = df_mus['track_id'].unique()
    idx = df_dsd['track_id'].isin(track_ids)
    df_dsd = df_dsd[idx]

    df = pd.concat([df_mus, df_dsd])
    ordered_columns = pd.unique(list(df_mus.columns) + list(df_dsd.columns))
    df = df[ordered_columns]
    df = df.sort_values(by=['track_id', 'method'])
    df = df.reset_index(drop=True)
    return df


def dsd100_with_method_and_trackid(df):
    "Add missing `method` and `track_id` to DSD100"

    df['method'] = 'ref'
    df['track_id'] = 0
    for idx, row in df.iterrows():
        m = re.search('DSD100/(Sources|Mixtures)/(Dev|Test)/(\d{3})',
                      row['audio_filepath'])
        df.at[idx, 'track_id'] = int(m.group(3))
    return df
