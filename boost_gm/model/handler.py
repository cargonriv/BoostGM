import numpy as np
# import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor

def train_model(X, y):
    # Model Initialization
    # base_estimator = DecisionTreeRegressor(max_depth=4)
    ada_model = AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=4))
    
    # Hyperparameter Tuning with Grid Search
    param_grid = {'n_estimators': [30, 50, 70], 'learning_rate': [0.01, 0.1, 1]}
    grid_search = GridSearchCV(ada_model, param_grid, cv=5)
    grid_search.fit(X, y)
    
    # Train the model with best parameters
    best_model = grid_search.best_estimator_
    return best_model

def evaluate_model(model, X_val, y_val):
    # Model Evaluation
    y_pred = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    return rmse