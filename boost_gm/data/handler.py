import os

import pandas as pd
from sklearn.preprocessing import StandardScaler

from boost_gm.util import import_module, get_config_path


CONFIG = import_module(get_config_path())


def combineAllData(pos_dict):#, name_change):

    master = pd.DataFrame(columns=CONFIG.og_stats)

    for team in CONFIG.teams:
        team_str = f'box_scores/{team}'
        print(team, os.path.exists(team_str))
        if not os.path.exists(team_str):
            os.makedirs(team_str)
        print(team, os.path.exists(team_str))

        # os.chdir(team_str)
        for team_box in os.listdir(team_str):
            df = pd.read_csv(team_box)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            master = pd.concat([master, df])

    master['Player'] = master['Player']#.replace(name_change)
    master['Player'] = master['Player'].str.lower()
    master['Pos'] = master['Player'].map(pos_dict)
    master['Team'] = master['Team'].str.lower()
    # master = master[CONFIG.newer_stats]
    # master['FPPM'] = master['FP'] / master['MP']
    master.to_csv(str('to_download/master_box_scores.csv'))

    def_master = pd.DataFrame(columns=CONFIG.newest_stats)

    for team in CONFIG.teams:
        print(team)
        team_def_str = f'box_scores/defense/{team}'
        if not os.path.exists(team_def_str):
            os.makedirs(team_def_str)
        # os.chdir(team_def_str)
        for team_def_game in  os.listdir(team_def_str):
            df = pd.read_csv(team_def_game)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            def_master = pd.concat([def_master, df])

    def_master = def_master[CONFIG.newest_stats]
    def_master.to_csv(str('to_download/master_def.csv'))


    off_master = pd.DataFrame(columns=CONFIG.newest_stats)
    for team in CONFIG.teams:
        print(team)
        team_def_str = f'box_scores/offense/{team}'
        if not os.path.exists(team_def_str):
            os.makedirs(team_def_str)
        # os.chdir(team_def_str)
        for team_off_game in os.listdir(team_def_str):
            df = pd.read_csv(team_off_game)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            off_master = pd.concat([off_master, df])
    off_master = off_master[CONFIG.newest_stats]
    off_master.to_csv(str('to_download/master_off.csv'))

def dubDub(df):
    if df['PTS'] > 9 and df['TRB'] > 9:
        return 1.5
    elif df['PTS'] > 9 and df['AST'] > 9:
        return 1.5
    elif df['AST'] > 9 and df['TRB'] > 9:
        return 1.5
    else:
        return 0

def tripDub(df):
    if df['PTS'] > 9 and df['TRB'] > 9 and df['AST'] > 9:
        return 3
    else:
        return 0

def processData(data):
    # Replace with actual feature names to be used (excluding player names, team names, etc.)
    selected_features = ['feature1', 'feature2', 'feature3']
    data = data[selected_features]
    
    # Data Transformation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)
    
    return X_scaled, scaler