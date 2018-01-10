import pandas as pd
import massdatasets


def test_mus2016():

    ref_frame = pd.read_csv(
        './data/sisec_mus_2017_full.csv'
    )

    frame = massdatasets.mus2016().to_pandas_df()

    frame = frame.sample(10)

    for idx, row in frame.iterrows():

        sub_ref = ref_frame[(ref_frame.track_id == row['track_id']) &
                            (ref_frame.metric == row['feature']) &
                            (ref_frame.method == row['method']) &
                            (ref_frame.target == row['source'])]

        assert(sub_ref['score'].values[0] == row['value'])


def test_join_dsd100_and_mus2016_dataframes():

    ref_cols = ['source', 'artist', 'audio_filepath', 'method', 'style',
                'test_set', 'title', 'track_id', 'dataset', 'feature', 'value']

    df_dsd = massdatasets.dsd100().to_pandas_df()
    df_mus = massdatasets.mus2016().to_pandas_df()
    df = massdatasets.utilities.join_dsd100_and_mus2016_dataframes(df_dsd,
                                                                   df_mus)

    assert(all(ref_cols == df.columns.values))
