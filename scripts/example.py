import mass_datasets


if __name__ == '__main__':

    ds = mass_datasets.DSD100('/vol/vssp/datasets/audio/DSD100')
    ds.write()

    # Read yaml back in
    ds = mass_datasets.Dataset.read('DSD100.yaml')
    print(ds.dump())

    # Convert document to pandas DataFrame
    df = ds.to_pandas_df()
    print(df.head())
