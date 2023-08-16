import numpy as np
import pandas as pd
import unicodedata
from sklearn.preprocessing import OrdinalEncoder



def preprocessing(all_data: pd.DataFrame):
    """
    train, testデータで共通の前処理のコード
    
    ・yearの異常値を直す
    ・manufacturerの表記を統一する
    ・sizeの表記を統一する
    ・regionの欠損値をtrain dataの(state, region)の組み合わせから補完する。残った欠損値は調べて補完する。
    ・title_statusとtypeの欠損値処理はとりあえず放置

    Args:
        all_data (pd.DataFrame): pd.concat([train, test], ignore_index=True)
    """
    # year
    year_dict = {
        2999:1999,
        3008:2008,
        3011:2011,
        3015:2015,
        3017:2017,
        3019:2019,
    }
    all_data["year"] = all_data["year"].replace(year_dict)
    
    
    # manufacturer
    all_data["manufacturer"] = all_data["manufacturer"].str.lower().apply(lambda x: unicodedata.normalize('NFKC', x))
    manufacturer_map = {
        'niѕsan':'nissan',
        'nisѕan':'nissan',
        'subαru':'subaru',
        'toyotа':'toyota',
        'sαturn':'saturn',
        'аcura':'acura',
        'vоlkswagen':'volkswagen',
        'lexuѕ':'lexus',
        'ᴄhrysler':'chrysler',
    }
    all_data["manufacturer"] = all_data["manufacturer"].replace(manufacturer_map)
    
    
    # size
    size_dict = {
        "fullーsize":"full-size",
        "midーsize":"mid-size",
        "subーcompact":"sub-compact",
        "full−size":"full-size",
        "mid−size":"mid-size"
    }
    all_data["size"] = all_data["size"].replace(size_dict)
        
    
    # 地域
    ## region -> stateが一意に定まることを確認
    region_state = {region:{} for region in all_data[all_data["flag"]=="train"]['region'].unique()}
    for row, value in all_data[all_data["flag"]=="train"].iterrows():
        if not pd.isna(value['state']):
            if value['state'] not in region_state[value['region']]:
                region_state[value['region']][value['state']] = 1
            else:
                region_state[value['region']][value['state']] += 1
    for region, state_dict in region_state.items():
        if len(state_dict) > 1 or state_dict == {}:
            region_state[region] = pd.NA
        else:
            region_state[region] = list(state_dict.keys())[0]

    ## regionからstateを決定
    all_data['state'] = [region_state[region] if pd.isna(state) else state for region, state in zip(all_data['region'], all_data['state'])]
    all_data.loc[all_data["region"] == "northwest KS", "state"] = "ks"
    all_data.loc[all_data["region"] == "ashtabula", "state"] = "oh"
    all_data.loc[all_data["region"] == "southern WV", "state"] = "wv"
    
    # type
    ## 欠損値 train: 456, test: 229
    
    # title_status
    ## 欠損値 train: 456, test: 229
    
    # fuel
    ## 欠損値 train: 1239, test: 1495
    
    
    all_data["elapsed_years"] = 2023 - all_data["year"]
    all_data["log_elapsed_years"] = np.log(all_data["elapsed_years"])
    all_data["sqrt_elapsed_years"] = np.sqrt(all_data["elapsed_years"])
    
    return all_data



def preprocessing_per_fold(CFG, train:pd.DataFrame, test:pd.DataFrame = None, fold:int = 0, predict:bool = False):
    """foldごとの前処理: leakageを防ぐ

    Args:
        CFG :config
        train (pd.DataFrame): 学習データ
        test (pd.DataFrame, optional): test data Defaults to None.
        fold (int, optional): Defaults to 0.
        predict (bool, optional): 予測するか否か. Defaults to False.
    """
    X_train = train[train["fold"] != fold].reset_index(drop=True)
    X_valid = train[train["fold"] == fold].reset_index(drop=True)    
    if predict:
        test_df = test.copy()

    # odometerの補正
    ## odometerが100以下or400000以上を異常値と考えて補完する
    ## year_mapがodometerの分散が大きくなる特徴量だったのでこれを利用してodometerを補完する
    fillna_map = X_train[(X_train["odometer"] > 100)&(X_train["odometer"] < 400000)].groupby(["region"])["odometer"].mean().reset_index()
    
    def replace_odometer(df: pd.DataFrame, fillna_map: pd.DataFrame)-> pd.DataFrame:
        """odometerの異常値をfillna_mapを利用して補完する

        Args:
            df (pd.DataFrame): 補完前のデータ
            fillna_map (pd.DataFrame): 補完するデータ

        Returns:
            pd.DataFrame: 補完後のデータ
        """
        df_1 = df[(df["odometer"] < 100)|(df["odometer"] > 400000)].reset_index(drop=True)
        df_2 = df[(df["odometer"] >= 100)&(df["odometer"] <= 400000)].reset_index(drop=True)
        df_1.drop("odometer", inplace=True, axis=1)
        df_1 = pd.merge(df_1, fillna_map, on="region", how="left")
        df = pd.concat([df_1, df_2])
        return df.sort_values("id", ignore_index=True)
    
    
    X_train = replace_odometer(X_train, fillna_map)
    X_valid = replace_odometer(X_valid, fillna_map)
    if predict:
        test_df = replace_odometer(test_df, fillna_map)
        test_df["odometer"].fillna(X_train["odometer"].mean(), inplace=True)
    X_train["odometer"].fillna(X_train["odometer"].mean(), inplace=True)
    X_valid["odometer"].fillna(X_train["odometer"].mean(), inplace=True)
        

    # 交互作用
    def apply_fe(df: pd.DataFrame) -> pd.DataFrame:
        """foldごとの特徴量作成

        Args:
            df (pd.DataFrame)

        Returns:
            pd.DataFrame: 特徴量作成後のdf
        """
        df["log_odometer"] = np.log(df["odometer"])
        df["sqrt_odometer"] = np.sqrt(df["odometer"])
        
        df["elapsed_years*odometer"] = df["elapsed_years"] * df["odometer"]
        df["elapsed_years*log_odometer"] = df["elapsed_years"] * df["log_odometer"]
        df["elapsed_years*sqrt_odometer"] = df["elapsed_years"] * df["sqrt_odometer"]
        
        df["log_elapsed_years*odometer"] = df["log_elapsed_years"] * df["odometer"]
        df["log_elapsed_years*log_odometer"] = df["log_elapsed_years"] * df["log_odometer"]
        df["log_elapsed_years*sqrt_odometer"] = df["log_elapsed_years"] * df["sqrt_odometer"]
        
        df["sqrt_elapsed_years*odometer"] = df["sqrt_elapsed_years"] * df["odometer"]
        df["sqrt_elapsed_years*log_odometer"] = df["sqrt_elapsed_years"] * df["log_odometer"]
        df["sqrt_elapsed_years*sqrt_odometer"] = df["sqrt_elapsed_years"] * df["sqrt_odometer"]
        return df
    X_train = apply_fe(X_train)
    X_valid = apply_fe(X_valid)
    if predict:
        test_df = apply_fe(test_df)
        
        
    # カウントエンコーディング
    for col in CFG.categorical_features:
        count_map = X_train[col].value_counts().to_dict()
        X_train[col+"_count_encoding"] = X_train[col].map(count_map)
        X_valid[col+"_count_encoding"] = X_valid[col].map(count_map)
        if predict:
            test_df[col+"_count_encoding"] = test_df[col].map(count_map)
        
        
    # 集約特徴量を用いたエンコーディング
    for col in CFG.categorical_features:
        for agg_ in ["mean", "std", "max", "min", "median"]:
            fillna_map = X_train.groupby(col)["price"].agg(agg_)
            X_train[col+f"_{agg_}_encoding"] = X_train[col].map(fillna_map)
            X_valid[col+f"_{agg_}_encoding"] = X_valid[col].map(fillna_map)
            if predict:
                test_df[col+f"_{agg_}_encoding"] = test_df[col].map(fillna_map)
                
    # 集約特徴量を用いたエンコーディング
    for col in CFG.categorical_features:
        for agg_ in ["mean", "std", "max", "min", "median"]:
            fillna_map = X_train.groupby(col)["odometer"].agg(agg_)
            X_train[col+f"_{agg_}_odometer_encoding"] = X_train[col].map(fillna_map)
            X_valid[col+f"_{agg_}_odometer_encoding"] = X_valid[col].map(fillna_map)
            if predict:
                test_df[col+f"_{agg_}_odometer_encoding"] = test_df[col].map(fillna_map)
            #CFG.candidate_features.append(col+f"_{agg_}_encoding")
            if agg_ == "median" or agg_ == "mean":
                X_train[col+f"_{agg_}_odometer_encoding_diff"] = X_train[col+f"_{agg_}_odometer_encoding"] - X_train["odometer"]
                X_valid[col+f"_{agg_}_odometer_encoding_diff"] = X_valid[col+f"_{agg_}_odometer_encoding"] - X_valid["odometer"]
                if predict:
                    test_df[col+f"_{agg_}_odometer_encoding_diff"] = test_df[col+f"_{agg_}_odometer_encoding"] - test_df["odometer"]
                    
                    
    # 集約特徴量を用いたエンコーディング
    for col in CFG.categorical_features:
        for agg_ in ["mean", "std", "max", "min", "median"]:
            fillna_map = X_train.groupby(col)["elapsed_years"].agg(agg_)
            X_train[col+f"_{agg_}_elapsed_years_encoding"] = X_train[col].map(fillna_map)
            X_valid[col+f"_{agg_}_elapsed_years_encoding"] = X_valid[col].map(fillna_map)
            if predict:
                test_df[col+f"_{agg_}_elapsed_years_encoding"] = test_df[col].map(fillna_map)
            #CFG.candidate_features.append(col+f"_{agg_}_encoding")
            if agg_ == "median" or agg_ == "mean":
                X_train[col+f"_{agg_}_elapsed_years_encoding_diff"] = X_train[col+f"_{agg_}_elapsed_years_encoding"] - X_train["elapsed_years"]
                X_valid[col+f"_{agg_}_elapsed_years_encoding_diff"] = X_valid[col+f"_{agg_}_elapsed_years_encoding"] - X_valid["elapsed_years"]
                if predict:
                    test_df[col+f"_{agg_}_elapsed_years_encoding_diff"] = test_df[col+f"_{agg_}_elapsed_years_encoding"] - test_df["elapsed_years"]
            
            
    # OrdinalEncoder: これはfoldごとではなくともよい
    oe = OrdinalEncoder(categories="auto",
                        handle_unknown="use_encoded_value",
                        unknown_value=999,
                        encoded_missing_value=np.nan, # QUESTION: 欠損値は-1に変換する -> NaNに??
                        )
    CFG.categorical_features_ = [feature + "_category" for feature in CFG.categorical_features]
    X_train[CFG.categorical_features_] = oe.fit_transform(X_train[CFG.categorical_features].values)
    X_valid[CFG.categorical_features_] = oe.transform(X_valid[CFG.categorical_features].values)
    if predict:
        test_df[CFG.categorical_features_] = oe.transform(test_df[CFG.categorical_features].values)
    
    if predict:
        return X_train, X_valid, test_df
    else:
        return X_train, X_valid