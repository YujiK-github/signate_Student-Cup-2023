import os
import torch
import random

import numpy as np
import pandas as pd

import warnings
warnings.simplefilter("ignore")

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import mean_absolute_percentage_error


def seed_everything(seed: int):
    """fix random factors"""
    random.seed(seed)
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    try:
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
    except:
        pass
    
    
def get_score(y_true, y_pred):
    """get MAPE score
    
    \text{MAPE}(y, \hat{y}) = \frac{100\%}{N} \sum_{i=1}^{N} \frac{|y_i - \hat{y}_i|}{y_i}
    
    """
    score = mean_absolute_percentage_error(y_true, y_pred)
    return score * 100


def load_data(CFG):
    """load data"""
    train = pd.read_csv(CFG.data_dir+"train.csv")
    test = pd.read_csv(CFG.data_dir+"test.csv")
    train["flag"] = "train"
    test["flag"] = "test"
    all_data = pd.concat([train, test], ignore_index=True)
    return all_data


def kfold(CFG, all_data: pd.DataFrame):
    """kfold

    Args:
        CFG : config
        all_data (pd.DataFrame)

    Returns:
        train, test
    """
    train = all_data[all_data["flag"] == "train"].reset_index(drop=True)
    test = all_data[all_data["flag"] == "test"].reset_index(drop=True)

    train.sort_values(by="id", ignore_index=True, inplace=True)

    train["year_map"], bins = pd.cut(train["year"], bins=20, labels=False, retbins=True)
    test["year_map"] = pd.cut(test["year"], bins=bins, labels=False)
    train["price_map"] = pd.cut(train["price"], bins=CFG.target_bins, labels=False)

    skf = StratifiedKFold(n_splits=CFG.n_splits, shuffle=True, random_state=CFG.seed)
    for i, (_, val) in enumerate(skf.split(X=train, y=train["price_map"])):
        train.loc[val, "fold"] = i
    print(train["fold"].value_counts())
    print("Variance between folds' means", train.groupby("fold")["price"].mean().std())
    return train