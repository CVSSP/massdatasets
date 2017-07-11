import massdatasets


if __name__ == '__main__':

    ds = massdatasets.DSD100('/vol/vssp/datasets/audio/DSD100')
    ds.write('../data/DSD100')
    ds = massdatasets.MSD100('/vol/vssp/datasets/audio/MSD100')
    ds.write('../data/MSD100')
