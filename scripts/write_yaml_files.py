import massdatasets


if __name__ == '__main__':

    print('Writing MSD100 dataset')
    ds = massdatasets.creators.msd100('/vol/vssp/datasets/audio/MSD100')
    ds.write('./massdatasets/data/MSD100')

    print('Writing DSD100 dataset')
    ds = massdatasets.creators.dsd100('/vol/vssp/maruss/data2/DSD100')
    ds.write('./massdatasets/data/DSD100')

    print('Writing MUS2016 dataset')
    ds = massdatasets.creators.mus2016('/vol/vssp/maruss/data2/MUS2017')
    ds.write('./massdatasets/data/MUS2016')
