import argparse, collections as co, json, os
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from boost_gm.data import combineAllData, getBox, getDailyURLS #, processData
from boost_gm.model import train_model, evaluate_model
# from boost_gm.util import import_module, get_config_path

# CONFIG = import_module(get_config_path())

if __name__ == "__main__":

    print('starting ... ')

    parser = argparse.ArgumentParser(description='Process arguments for Data Scraping NBA player stats from wwww.basketballreference.com.')
    parser.add_argument('--data-path', default='data', type=str, help='Path to save all data. Default = data')
    args = parser.parse_args()

    data_path = Path(args.data_path)
    csv_str = str(data_path / 'to_download' / 'master_box_scores.csv')

    yesterday = date.today() - timedelta(days=1)
    # date = yesterday.strftime('%m-%d-%Y')

    x = getDailyURLS(yesterday.strftime('%m-%d-%Y'), data_path)
    # data = pd.read_csv(csv_str)

    # Assume 'y' is the target variable
    y = pd.read_csv(csv_str)['+/-']

    for i in range(len(x)):
        getBox(yesterday.strftime('%m-%d-%Y'), x[i][0], x[i][1][0].upper(), x[i][1][1].upper())

    # Data Preprocessing
    # X_scaled = processData(pd.read_csv(csv_str))
    # from sklearn.preprocessing import StandardScaler
    # Error Handling: Data Inconsistencies (e.g., duplicate rows)
    # X_scaled = pd.DataFrame(X_scaled).drop_duplicates().values
    X_scaled = StandardScaler().fit_transform(pd.read_csv(csv_str))
    X_transformed = pd.DataFrame(X_scaled).drop_duplicates().values

    os.chdir(data_path)
    posdict = json.load(open('posdict.json'))
    # namechange = json.load(open('playernamechange.json'))

    print('combining data!')
    combineAllData(posdict) #, namechange)

    # Train-Validation Split
    X_train, X_val, y_train, y_val = train_test_split(X_transformed, y, test_size=0.2, random_state=42, shuffle=False)

    # Model Training
    best_model = train_model(X_train, y_train)
    
    # Model Evaluation
    rmse = evaluate_model(best_model, X_val, y_val)
    print(f"Model RMSE: {rmse}")
    
    # Feature Importance
    feature_importance = best_model.feature_importances_
    print(f"Feature Importance: {feature_importance}")

    print('... finished')
