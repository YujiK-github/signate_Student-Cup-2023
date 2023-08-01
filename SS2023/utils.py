import os
import numpy as np
import random
import torch
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