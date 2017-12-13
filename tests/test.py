import pandas as pd
import massdatasets


def test_mus2016():

    ref_frame = pd.read_csv(
        '../data/sisec_mus_2017_full.csv'
    )

    frame = massdatasets.Dataset.read('../data/MUS2016.yaml').to_pandas_df()

    frame = frame.sample(10)

    for idx, row in frame.iterrows():

        sub_ref = ref_frame[(ref_frame.track_id == row['track_id']) &
                            (ref_frame.metric == row['feature']) &
                            (ref_frame.method == row['method']) &
                            (ref_frame.target == row['source'])]

        assert(sub_ref['score'].values[0] == row['value'])
