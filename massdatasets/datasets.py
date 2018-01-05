import os
import pandas as pd
import yaml

try:
    Loader = yaml.CLoader
except:
    Loader = yaml.Loader


class Dataset(yaml.YAMLObject):
    '''
    Class for creating yaml files for indexing common multitrack audio
    datasets.
    '''

    def __init__(self, name, base_path=None):

        self.dataset = name
        if base_path is None:
            self.base_path = ''
        else:
            self.base_path = os.path.abspath(base_path)
        self.songs = []

    @staticmethod
    def read(filename=None):

        with open(filename, 'r') as f:
            instance = yaml.load(f, Loader=Loader)

        return instance

    def write(self, filename=None):
        if filename is None:
            filename = self.dataset
        else:
            filename, ext = os.path.splitext(filename)
        with open(filename + '.yaml', 'w') as f:
            yaml.dump(self, f, default_flow_style=False)

    def dump(self):
        return yaml.dump(self, default_flow_style=False)

    def add_song(self, artist, title, style, audio_filepath, **kwargs):
        self.songs.append(
            {'artist': artist,
             'title': title,
             'style': style,
             'audio_filepath': audio_filepath,
             **kwargs}
        )

    def to_pandas_df(self, include_features=True):
        '''
        Compiles the yaml document to a pandas DataFrame.
        audio_filepath are complete (prefixed by base_path).
        '''

        long_format = True
        features = []
        frames = []
        songs = self.songs.copy()

        for song in songs:
            if 'feature' in song and include_features:
                features.append(pd.DataFrame.from_dict(song.pop('feature')))
            frames.append(pd.DataFrame.from_dict(song))

        frame = pd.concat(frames, copy=False).reset_index()
        frame.rename(columns={'index': 'source'}, inplace=True)

        frame['audio_filepath'] = ['/'.join((self.base_path, _))
                                   for _ in frame['audio_filepath']]
        frame['dataset'] = self.dataset

        # This is clunky way to add features in long format
        if features and include_features:

            features = pd.concat(features, copy=False)

            frame_with_features = pd.concat(
                [frame, features.reset_index(drop=True)],
                axis=1,
                copy=False,
            )

            if long_format:

                frame_with_features = pd.melt(frame_with_features,
                                              id_vars=frame.columns,
                                              value_vars=features.columns,
                                              var_name='feature',
                                              value_name='value')

            return frame_with_features

        else:

            return frame


'''
MSD100
'''


def msd100(base_path):
    dataset = Dataset.read('MSD100.yaml')
    dataset.base_path = base_path
    return dataset


def dsd100(base_path):
    dataset = Dataset.read('DSD100.yaml')
    dataset.base_path = base_path
    return dataset


def mus2016(base_path):
    dataset = Dataset.read('MUS2016.yaml')
    dataset.base_path = base_path
    return dataset
