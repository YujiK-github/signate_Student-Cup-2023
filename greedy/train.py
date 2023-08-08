from typing import List
import lightgbm as lgb
import pandas as pd
from utils import get_score

import warnings
warnings.simplefilter("ignore")

def evaluate(CFG, fs: List[str], X_train: pd.DataFrame, X_valid: pd.DataFrame):
    """特徴量選択のための評価関数

    Args:
        CFG: config
        fs (List[str]): 学習に用いる特徴量
        X_train (pd.DataFrame): 学習用データ
        X_valid (pd.DataFrame): 評価データ

    Returns:
        score (int)
    """
    # params
    ## max_depthをxgboostとcatboostに合わせて6にした
    lgb_param = {
        "task":"train",
        "objective": "mape",
        "boosting":"gbdt",
        "num_boost_round": CFG.num_boost_round,
        "learning_rate":0.1, # default: 0.1
        "num_leaves":31, # max number of leaves in one tree ###
        "max_depth":6, # default -1, int: limit the max depth for tree model ##
        "min_child_weight":1e-3, # double: minimal sum hessian in one leaf
        "min_data_in_leaf":20, # minimal number of data in one leaf
        "alpha":0.9, # double, constraints, alpha > 0.0: 
        "colsample_bytree":1.0, # 0 < "colsample_bytree" < 1
        #: LightGBM will randomly select a subset of features on each iteration (tree) if feature_fraction is smaller than 1.0
        "lambda": 0, #lambda_l2 >= 0.0: L2 regularization
        "subsample":1, #0.0 < bagging_fraction <= 1.0
        "num_threads": CFG.num_cores,
        "metric": 'mape',
        "seed" : CFG.seed,
        "verbosity": -1, 
    }
    categorical_features = [col for col in fs if "_category" in col]
    lgb_train = lgb.Dataset(X_train[fs], X_train["price"], categorical_feature = categorical_features)
    lgb_valid = lgb.Dataset(X_valid[fs], X_valid["price"], categorical_feature = categorical_features)
    model = lgb.train(
                    lgb_param, 
                    lgb_train, 
                    num_boost_round=CFG.num_boost_round, 
                    valid_sets=[lgb_valid],
                    categorical_feature = categorical_features,
                    callbacks=[lgb.early_stopping(stopping_rounds=CFG.stopping_rounds, verbose=False),],
                    )
    
    X_valid[f"pred"] = model.predict(X_valid[fs], num_iteration=model.best_iteration)
    score = get_score(y_true=X_valid["price"], y_pred=X_valid["pred"])
    return score