import datasets


if __name__ == '__main__':

    ds = datasets.DSD100('/vol/vssp/datasets/audio/DSD100')
    ds.write()
    ds = datasets.MSD100('/vol/vssp/datasets/audio/MSD100')
    ds.write()
