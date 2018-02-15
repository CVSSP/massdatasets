import re
import os
import pandas as pd
import yaml
from . import utilities

try:
    Loader = yaml.CLoader
except:
    Loader = yaml.Loader


class Dataset(yaml.YAMLObject):
    '''
    Class for creating yaml files for indexing common multitrack audio
    datasets.
    '''

    def __init__(self, name=None, base_path=None):

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

        temp = {'artist': artist,
                'title': title,
                'style': style,
                'audio_filepath': audio_filepath}

        temp.update(kwargs)

        self.songs.append(temp)

    def to_pandas_df(self, include_features=True):
        '''
        Compiles the yaml document to a pandas DataFrame.
        audio_filepath are complete (prefixed by base_path).
        '''

        long_format = True
        features = []
        frames = []
        songs = list(self.songs)

        for song in songs:
            if 'feature' in song:
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


def msd100(base_path=None, create=False):

    if not create:

        dataset = Dataset.read(utilities.get_data_file('MSD100.yaml'))
        dataset.base_path = base_path
        return dataset

    else:

        print('Creating MSD100 dataset')

        dataset = Dataset('MSD100', base_path)

        xlsx_name = 'msd100.xlsx'
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

        source_paths = [_.replace('Mixtures', 'Sources')
                        for _ in mix_paths]
        test_set = [0] * 50 + [1] * 50

        for row in excel.iterrows():

            artist_title = row[1]['Name']
            artist, title = artist_title.split(' - ')
            style = row[1]['Style']
            idx = [i for i, _ in enumerate(
                mix_paths) if artist_title in _][0]

            audio = {}
            audio['mixture'] = mix_paths[idx] + '/mixture.wav'

            for key in ['bass', 'drums', 'vocals', 'other']:
                audio[key] = '{0}/{1}.wav'.format(source_paths[idx], key)

            dataset.add_song(artist,
                             title,
                             style,
                             audio,
                             test_set=test_set[idx])
        return dataset


def dsd100(base_path=None, create=False):

    if not create:

        dataset = Dataset.read(utilities.get_data_file('DSD100.yaml'))
        dataset.base_path = base_path
        return dataset

    else:

        print('Creating DSD100 dataset')

        dataset = Dataset('DSD100')

        base_path = os.path.abspath(base_path)

        xlsx_name = 'dsd100.xlsx'
        excel = pd.read_excel(os.path.join(base_path, xlsx_name),
                              'Sheet1')

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

            artist_title = row[1]['Name']
            artist, title = artist_title.split(' - ')
            style = row[1]['Style']
            idx = [i for i, _ in enumerate(mix_paths) if artist_title in _][0]

            # Add `track_id` from filename
            m = re.search('(Sources|Mixtures)/(Dev|Test)/(\d{3})',
                          mix_paths[idx])

            track_id = int(m.group(3))

            audio = {}
            audio['mixture'] = mix_paths[idx] + '/mixture.wav'

            for key in ['bass', 'drums', 'vocals', 'other']:
                audio[key] = '{0}/{1}.wav'.format(source_paths[idx], key)

            dataset.add_song(artist,
                             title,
                             style,
                             audio,
                             test_set=test_set[idx],
                             track_id=track_id)

        return dataset


def mus2016(base_path=None, create=False):
    '''
    MUS2016

    The naming conventions are strange I know.
    Basically MUS2016 is correct, but the data files we have received and are
    available for download use 2017.
    '''

    if not create:

        dataset = Dataset.read(utilities.get_data_file('MUS2016.yaml'))
        dataset.base_path = base_path
        return dataset

    else:

        print('Creating MUS2016 dataset')

        dataset = Dataset('MUS2016')

        base_path = os.path.abspath(base_path)
        results_filename = 'sisec_mus_2017_full.csv'

        results = pd.read_csv(os.path.join(base_path,
                                           results_filename))

        # Tracks 36, 37, 43, and 44 should be excluded (due to corrupt data)
        results = results[~results.track_id.isin([36, 37, 43, 44])]
        results = results.sort_values(
            ['method', 'track_id', 'metric']
        ).reset_index()

        # Track 23 has an error in its artist entry
        results.loc[results.track_id == 23, 'title'] = \
            'Jokers, Jacks & Kings - Sea Of Leaves'

        for group, data in results.groupby(['method', 'track_id']):

            row = data.iloc[0]
            artist_title = row['title']
            artist, title = artist_title.split(' - ')
            style = row['genre']
            method = group[0]
            track_id = "{:03d}".format(group[1])
            test_set = 1 - int(row['is_dev'])
            test_or_dev = 'Test' if test_set else 'Dev'

            # The folder names are incorrect for the IBM, so we fix it here
            if method == 'IBM':
                if track_id == '077':
                    artist_title = 'Lyndsey Ollard - CatchingUp'
                elif track_id == '089':
                    artist_title = 'St Vitus - Words Gets Around'
                elif track_id == '090':
                    artist_title = 'Doppler Shift - Atrophy'

            # Relative-to-base file path
            path = os.path.join(method,
                                test_or_dev,
                                ' - '.join((track_id, artist_title)),
                                )
            audio = {}
            for target in data['target']:
                audio[target] = '{0}/{1}.wav'.format(path, target)

            # BSS Eval measures
            feature = {}
            for metric in pd.unique(data['metric']):
                feature[metric] = {}

                for target in data['target']:

                    sub = data.loc[(data.metric == metric) &
                                   (data.target == target)]
                    feature[metric][target] = float(sub['score'])

            dataset.add_song(artist,
                             title,
                             style,
                             audio,
                             test_set=test_set,
                             method=method,
                             track_id=int(group[1]),
                             feature=feature)

        return dataset
