'''
Script to generate the data files that are shipped with the package.
Should be run from the root directory of the repository.
'''
import massdatasets


if __name__ == '__main__':

    ds = massdatasets.datasets.msd100('/vol/vssp/datasets/audio/MSD100',
                                      create=True)
    ds.base_path = None
    ds.write('./massdatasets/data/MSD100')

    ds = massdatasets.datasets.dsd100('/vol/vssp/maruss/data2/DSD100',
                                      create=True)
    ds.base_path = None
    ds.write('./massdatasets/data/MSD100')

    ds = massdatasets.datasets.mus2016('/vol/vssp/maruss/data2/MUS2017',
                                       create=True)
    ds.base_path = None
    ds.write('./massdatasets/data/MUS2016')
