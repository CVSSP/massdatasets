import massdatasets


if __name__ == '__main__':

    print('Writing MSD100 dataset')
    ds = massdatasets.MSD100('/vol/vssp/datasets/audio/MSD100')
    ds.write('../data/MSD100')

    print('Writing DSD100 dataset')
    ds = massdatasets.DSD100('/vol/vssp/maruss/data2/DSD100')
    ds.write('../data/DSD100')

    print('Writing MUS2016 dataset')
    ds = massdatasets.MUS2016('/vol/vssp/maruss/data2/MUS2017')
    ds.write('../data/MUS2016')
