import os
import pandas as pd
import yaml


class Dataset(yaml.YAMLObject):
    '''
    Class for creating yaml files for indexing common multitrack audio
    datasets.
    '''

    def __init__(self, base_path):

        self.dataset = self.__class__.__name__
        self.base_path = base_path
        self.songs = []

    def write(self, filename=None):
        if filename is None:
            filename = self.dataset
        else:
            filename, ext = os.path.splitext(filename)
        with open(filename + '.yml', 'w') as f:
            yaml.dump(self, f, default_flow_style=False)

    def add_song(self, artist, title, style, mixture, stems, **kwargs):
        self.songs.append(
            {'artist': artist,
             'title': title,
             'style': style,
             'mixture': mixture,
             'stems': stems,
             **kwargs}
        )


class DSD100(Dataset):

    def __init__(self,
                 base_path='/vol/vssp/datasets/audio/DSD100',
                 xlsx_name='dsd100.xlsx'):
        super(DSD100, self).__init__(base_path)

        base_path = os.path.abspath(base_path)

        excel = pd.read_excel(os.path.join(base_path, xlsx_name), 'Sheet1')

        # Fix typo in xlsx file
        excel.ix[excel.Name == 'Patrick Talbot - Set Free Me', 'Name'] = (
            'Patrick Talbot - Set Me Free')

        # relative paths to each song
        mix_paths = ['Mixtures/Dev/' + _
                     for _ in sorted(os.listdir(
                        os.path.join(base_path, 'Mixtures/Dev')))]

        mix_paths += ['Mixtures/Test/' + _
                      for _ in sorted(os.listdir(
                            os.path.join(base_path, 'Mixtures/Test')))]

        source_paths = [_.replace('Mixtures', 'Sources') for _ in mix_paths]
        test_set = [0] * 50 + [1] * 50

        for row in excel.iterrows():

            artist, title = row[1]['Name'].split(' - ')
            style = row[1]['Style']
            idx = [i for i, _ in enumerate(mix_paths) if title in _][0]
            mixture = mix_paths[idx] + '/mixture.wav'

            stems = {}
            for key in ['bass', 'drums', 'vocal', 'other']:
                stems[key] = '{0}/{1}.wav'.format(source_paths[idx], key)

            self.add_song(artist,
                          title,
                          style,
                          mixture,
                          stems,
                          test_set=test_set[idx])


class MSD100(DSD100):

    def __init__(self,
                 base_path='/vol/vssp/datasets/audio/MSD100',
                 xlsx_name='msd100.xlsx'):
        super(MSD100, self).__init__(base_path, xlsx_name)
