import pickle
import numpy as np
import pandas as pd
from train import evaluate
import warnings
warnings.simplefilter("ignore")



def greedy_forward_selection(CFG, all_data: pd.DataFrame):
    """
    greedy forward selection
    
    ref: 
        https://github.com/ghmagazine/kagglebook/blob/3d8509d1c1b41a765e3f4744ba1fb226188e2b15/ch06/ch06-06-wrapper.py

    Args:
        CFG : config
        all_data (pd.DataFrame): 全データ
    """
    best_score = np.inf
    selected = set([])

    print("start greedy forward selection")

    while True:

        if len(selected) == len(CFG.learnable_features):
            # すべての特徴が選ばれて終了
            break

        scores = []
        for feature in CFG.learnable_features:
            if feature not in selected:
                fs = list(selected) + [feature]
                score = evaluate(CFG, fs, all_data)
                scores.append((feature, score))

        b_feature, b_score = sorted(scores, key=lambda tpl: tpl[1])[0]
        if b_score < best_score:
            print(f"Score: {best_score:.3f} -> {b_score:.3f}"+f' &   selected: {b_feature}')
            selected.add(b_feature)
            best_score = b_score
        else:
            break
    print('\033[32m'+f'selected features: {selected}'+'\033[0m')
    print('\033[32m'+f"best_score: {best_score}"+'\033[0m')
    
    # 選ばれた特徴量を保存
    with open(CFG.save_dir+f'selected_features_{CFG.greedy_seed}seed.pickle', mode='wb') as f:
        pickle.dump(selected, f)
    print("Saved selected features!")




def simple_greedy_selection(CFG, all_data: pd.DataFrame):
    """
    simple greedy forward selection
    
    ref: 
        https://github.com/ghmagazine/kagglebook/blob/3d8509d1c1b41a765e3f4744ba1fb226188e2b15/ch06/ch06-06-wrapper.py

    Args:
        CFG : config        
        all_data (pd.DataFrame): 全データ
    """
    for col in CFG.categorical_features:
        CFG.candidate_features.append(col+"_count_encoding")
    for col in CFG.categorical_features:
        for agg_ in ["mean", "std", "max", "min", "median"]:
            CFG.candidate_features.append(col+f"_{agg_}_encoding")
    CFG.categorical_features_ = [feature + "_category" for feature in CFG.categorical_features]
    CFG.candidate_features += CFG.categorical_features_
            
    
    # 特徴量の順番を入れ替える
    candidates = np.random.RandomState(CFG.greedy_seed).permutation(CFG.candidate_features)
    selected = set([])

    print('\033[32m'+"start simple selection"+'\033[0m')
    print("base features: ", CFG.base_features)
    
    # baseline
    best_score = evaluate(CFG, CFG.base_features, all_data)
    print(f"[{0}/{len(candidates)}]Base Score: {best_score:.3f}")


    for i, feature in enumerate(candidates):
        fs = list(selected) + [feature] + CFG.base_features
        # 選んだ特徴量を用いて学習・評価を行う
        score = evaluate(CFG, fs, all_data)
        if score < best_score:
            selected.add(feature)
            print(f"[{i+1}/{len(candidates)}]Score: {best_score:.3f} -> {score:.3f}"+f' &   selected: {feature}')
            best_score = score
        else:
            print(f"[{i+1}/{len(candidates)}]Score: {best_score:.3f} -> {score:.3f}"+f' & unselected: {feature}') 

    
    selected = list(selected) + CFG.base_features
    
    print('\033[32m'+f'selected features: {selected}'+'\033[0m')
    print('\033[32m'+f"best_score: {best_score}"+'\033[0m')
    
    # 選ばれた特徴量を保存
    with open(CFG.save_dir+f'selected_features_seed{CFG.greedy_seed}.pickle', mode='wb') as f:
        pickle.dump(selected, f)
    print("Saved selected features!")