import mass_datasets


if __name__ == '__main__':

    ds = mass_datasets.DSD100('/vol/vssp/datasets/audio/DSD100')
    ds.write('../data/DSD100')
    ds = mass_datasets.MSD100('/vol/vssp/datasets/audio/MSD100')
    ds.write('../data/MSD100')
