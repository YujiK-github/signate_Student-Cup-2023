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
            print(f"Score: {best_score:.5f} -> {b_score:.5f}"+f' &   selected: {b_feature}')
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
            CFG.candidate_features.append(col+f"_{agg_}_odometer_encoding")
            CFG.candidate_features.append(col+f"_{agg_}_elapsed_years_encoding")
            if agg_ == "median" or agg_ == "mean":
                CFG.candidate_features.append(col+f"_{agg_}_odometer_encoding_diff")
                CFG.candidate_features.append(col+f"_{agg_}_elapsed_years_encoding_diff")
    for col in ["log_odometer", "sqrt_odometer", "elapsed_years*odometer", "elapsed_years*log_odometer", "elapsed_years*sqrt_odometer", 
                "log_elapsed_years*odometer", "log_elapsed_years*log_odometer", "log_elapsed_years*sqrt_odometer", "sqrt_elapsed_years*odometer", 
                "sqrt_elapsed_years*log_odometer", "sqrt_elapsed_years*sqrt_odometer"]:
        CFG.candidate_features.append(col)
    
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
            print(f"[{i+1}/{len(candidates)}]Score: {best_score:.5f} -> {score:.5f}"+f' &   selected: {feature}')
            best_score = score
        else:
            print(f"[{i+1}/{len(candidates)}]Score: {best_score:.5f} -> {score:.5f}"+f' & unselected: {feature}') 

    
    selected = list(selected) + CFG.base_features
    
    print('\033[32m'+f'selected features: {selected}'+'\033[0m')
    print('\033[32m'+f"best_score: {best_score}"+'\033[0m')
    
    # 選ばれた特徴量を保存
    with open(CFG.save_dir+f'selected_features_for_{CFG.filename}_seed{CFG.greedy_seed}.pickle', mode='wb') as f:
        pickle.dump(selected, f)
    print(f"Saved to {CFG.save_dir}selected_features_for_{CFG.filename}_seed{CFG.greedy_seed}.pickle!")
    
    
    
def rule_base_greedy_selection(CFG, all_data: pd.DataFrame):
    """
    greedy forward selection by rule base
    
    
    < Rule >
    * base_features: ['year', 'odometer', 'fuel_category', 'title_status_category', 'type_category', 'state_category', 'region_category', 'manufacturer_category', 
                      'condition_category', 'cylinders_category', 'transmission_category', 'drive_category', 'size_category', 'paint_color_category']
                      
    * categorical_features: ['fuel_category', 'title_status_category', 'type_category', 'state_category', 'region_category', 'manufacturer_category', 
                             'condition_category', 'cylinders_category', 'transmission_category', 'drive_category', 'size_category', 'paint_color_category']
    において、
    1. categorical_featuresから1つ選ぶ <- featureとする
    2. featureの集約特徴量(min, max, median, mean, std, count)をそれぞれ加えたときのモデルのスコアと元々のスコアを比較して、最もスコアが改善したものを採用する。
       改善しなければcategoryのままにする
    3. 最もスコアが良いものがcategoryではない場合、最もスコアが改善したカラムを加えた上でさらに2番目にスコアが改善したカラムを追加して結果が改善すれば加えて、悪化すれば次のfeatureへ
       進む
    4. categorical_featuresから全通り試す
    
    ref: 
        https://github.com/ghmagazine/kagglebook/blob/3d8509d1c1b41a765e3f4744ba1fb226188e2b15/ch06/ch06-06-wrapper.py

    Args:
        CFG : config        
        all_data (pd.DataFrame): 全データ
    """    
    print('\033[32m'+"start simple selection"+'\033[0m')
    print("base features: ", CFG.base_features)
    
    # baseline
    best_score = evaluate(CFG, CFG.base_features, all_data)    
    print(f"[{0}/{len(CFG.categorical_features)}]Base Score: {best_score:.3f}")
    
    # categorical_featuresの順番を入れ替える
    CFG.categorical_features = np.random.RandomState(CFG.greedy_seed).permutation(CFG.categorical_features)
    for i, col in enumerate(CFG.categorical_features):
        print('\033[34m'+f"[{i+1}/{len(CFG.categorical_features)}]Start Feature selection about {col}"+'\033[0m')
        scores = dict()
        scores[col+"_category"] = best_score # defaultのセッティングのスコア
        print(f" {col}_category -> {best_score:.5f}")
        CFG.base_features.remove(col+"_category") # f"{col}_category"は除く
        
        # 集約特徴量たち
        candidate_features = []
        candidate_features.append(col+"_count_encoding")
        for agg_ in ["mean", "std", "max", "min", "median"]:
            candidate_features.append(col+f"_{agg_}_encoding")
            
        # 集約特徴量の順番を入れ替える
        candidate_features = np.random.RandomState(CFG.greedy_seed).permutation(candidate_features)
        
        # 各集約特徴量で評価する
        for feature in candidate_features:
            fs = [feature] + CFG.base_features
            score = evaluate(CFG, fs, all_data)
            print(f" {feature} -> {score:.5f}")
            scores[feature] = score
            
        # 各集約特徴量で最もスコアが改善するものを選択する
        best_score = min(scores.values())
        best_key = min(scores, key=scores.get)
        print(f"    Selected :{best_key} -> {best_score:.5f}")
        # best_keyを加える
        CFG.base_features.append(best_key)
        
        # 2番目に改善したカラムを加えて良くなるかどうか試す
        if best_key != col+"_category":
            # 下から2番目の値に対応するキーを検索
            second_key = [key for key, value in scores.items() if value == sorted(scores.values())[-2]][0]
            fs = [second_key] + CFG.base_features
            score = evaluate(CFG, fs, all_data)
            if score < best_score:
                print(f"        Selected {second_key}: {best_score:5f} -> {score:.5f}")
                CFG.base_features.append(second_key)
                best_score = score
            else:
                print(f"        Unselected {second_key}: {best_score:5f} -> {score:.5f}")
        
     
    print('\033[32m'+f'selected features: {CFG.base_features}'+'\033[0m')
    print('\033[32m'+f"best_score: {best_score}"+'\033[0m')
    
    # 選ばれた特徴量を保存
    with open(CFG.save_dir+f'selected_features_for_{CFG.filename}_seed{CFG.greedy_seed}.pickle', mode='wb') as f:
        pickle.dump(CFG.base_features, f)
    print(f"Saved to {CFG.save_dir}selected_features_for_{CFG.filename}_seed{CFG.greedy_seed}.pickle!")