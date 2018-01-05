import datasets
import os
import re
import pandas as pd


def msd100(base_path=None, xlsx_name='msd100.xlsx'):

    dataset = datasets.Dataset('MSD100')

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

        artist_title = row[1]['Name']
        artist, title = artist_title.split(' - ')
        style = row[1]['Style']
        idx = [i for i, _ in enumerate(mix_paths) if artist_title in _][0]

        audio = {}
        audio['mixture'] = mix_paths[idx] + '/mixture.wav'

        for key in ['bass', 'drums', 'vocals', 'other']:
            audio[key] = '{0}/{1}.wav'.format(source_paths[idx], key)

        dataset.add_song(artist,
                         title,
                         style,
                         audio,
                         test_set=test_set[idx])

    dataset.write()


def dsd100(base_path=None, xlsx_name='dsd100.xlsx'):

    dataset = datasets.Dataset('DSD100')

    base_path = os.path.abspath(base_path)

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

    dataset.write()


def mus2016(base_path, results_filename='sisec_mus_2017_full.csv'):
    '''
    MUS2016

    The naming conventions are strange I know.
    Basically MUS2016 is correct, but the data files we have received and are
    available for download use 2017.
    '''

    dataset = datasets.Dataset('MUS2016')

    base_path = os.path.abspath(base_path)

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
    dataset.write()
