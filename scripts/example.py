import massdatasets


if __name__ == '__main__':

    ds = massdatasets.DSD100('/vol/vssp/datasets/audio/DSD100')
    ds.write()

    # Read yaml back in
    ds = massdatasets.Dataset.read('DSD100.yaml')
    print(ds.dump())

    # Convert document to pandas DataFrame
    df = ds.to_pandas_df()
    print(df.head())
