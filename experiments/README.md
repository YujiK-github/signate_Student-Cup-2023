TODO: Neural Network  
TODO: transformers(fine-tuning) model  
TODO: transformers baseのembeddingを利用したmodel  
TODO: ensemble(Weighted Average: optuna?, Stacking)  
TODO: seed average  
TODO: catboost  
TODO: xgboost  
TODO: fold増やす  
exp008では

| n_splits | CV |
| - | - |
| 5 | 45.49498124624943 |
| 6 | 45.44400005088631 |
| 8 | 45.40235319953471 |
| 10 | 45.38139862504485 |
| 12 | 45.38716269497497 |
| 15 | 45.41241921140207 |

TODO: 値段帯で分ける？？  
TODO: 重複あるかも？？ -> 重複なかった  
TODO: feature_selectionのgreedy_seedの種類を増やす(5 -> ??)  
TODO: yearやodometerの集約特徴量を加えてgreedy? -> あまり改善しなかった  
TODO: StackingするときにMSEベースの特徴量くわえてみる？ 


| file | CV | LB | description |
| - | - | - | - |
| exp001 | 66.11899904620047 | 64.5174611 | baseline_lgb<br>yearとpriceのMultilabelStratifiedKFold |
| exp002 | 64.72120662038989 | 63.4342250 | baseline_cat<br>yearとpriceのMultilabelStratifiedKFold |
| exp003 | 45.84279120500015 | 45.1154626 | baseline_ensemble(cat+lgb)<br>yearとpriceのMultilabelStratifiedKFold |
| exp004 | 44.6154644289379 | 44.0886434 | baseline_lgbから変更<br>**price_mapでのStratifiedKFold**<br>odometerの補完や色々なencodingを追加<br>with optuna |
| exp005 | 44.20309555007229 | 43.6297815 | exp004からパラメータ変更<br>**price_mapでのStratifiedKFold**<br>odometerの補完や色々なencodingを追加<br>with optuna |
| exp006 | 44.16365041018153 | 43.7463188 | simple greedy selectionを使って特徴量選択した5個のモデルのアンサンブル(evaluate hold-out)<br>**price_mapでのStratifiedKFold**<br> with optuna |
| exp007 | 44.118156031444954 | 43.7711997 | simple greedy selectionを使って特徴量選択した5個のモデルのアンサンブル(evaluate CV)<br>**price_mapでのStratifiedKFold**<br> with optuna |
| exp008 | 45.49498124624943 | 44.7311468 | 新しくCross Validationのやり方を設定したsimpleなlgbのbaseline |
| exp009 |  |  | 新しくCross Validationのやり方を設定したsimpleなlgbでsimple greedy selectionを使って特徴量選択した5個のモデルのアンサンブル(evaluate CV)を試してみた<br>しかし、特徴量の選択の方法が良くなかったので変更する |
| exp010_0 | 44.364568837517524 | 43.7384163 | 新しくCross Validationのやり方を設定したsimpleなlgbでrule based greedy selectionを使って特徴量選択した5個のモデル(1)_seed42 |
| exp010_1 | 44.706570976834534 | 44.0149739 | 新しくCross Validationのやり方を設定したsimpleなlgbでrule based greedy selectionを使って特徴量選択した5個のモデル(2)_seed2023 |
| exp010_2 | 44.33097999776283 | 43.7719024 | 新しくCross Validationのやり方を設定したsimpleなlgbでrule based greedy selectionを使って特徴量選択した5個のモデル(3)_seed3 |
| exp010_3 | 44.33737773847836 | 43.7822822 | 新しくCross Validationのやり方を設定したsimpleなlgbでrule based greedy selectionを使って特徴量選択した5個のモデル(4)_seed2 |
| exp010_4 | 44.43327055384885 |  | 新しくCross Validationのやり方を設定したsimpleなlgbでrule based greedy selectionを使って特徴量選択した5個のモデル(5)_seed1 |
| exp010 | 44.19084497334044 | 43.6761545 | 新しくCross Validationのやり方を設定したsimpleなlgbでrule based greedy selectionを使って特徴量選択した5個のモデルのアンサンブル(evaluate CV)を試してみた |
| exp011 | 44.15693790827101 | 43.6017463 | simple greedy selectionした後にoptunaでparameter tuningした(1) |
| exp012 | 44.17021540173626 | 43.6111546 | simple greedy selectionした後にoptunaでparameter tuningした(2) |
| exp013 | 44.00756302577998 | 43.5427417 | exp011とexp012のアンサンブル |
| exp014 | 43.966795960812284 | - | greedy->optuna, n_splits=8, ver0 | 
| exp015 | 44.11063297972305 | - | **greedy->optuna, n_splits=8, ver1** | 
| exp016 | 44.06125663376067 | - | **greedy->optuna, n_splits=8, ver2** | 
| exp017 | 44.12841111907897 | - | greedy->optuna, n_splits=8, ver3 | 
| exp018 | 44.01755664381658 | - | **greedy->optuna, n_splits=8, ver4** | 
| exp019 | 43.98915506706626 | - | greedy->optuna, n_splits=8, ver5 | 
| exp020 | 44.052070379194966 | - | **greedy->optuna, n_splits=8, ver6** | 
| exp021 | 43.979683002688965 | - | **greedy->optuna, n_splits=8, ver7** | 
| exp022 | 44.02074386662909 | - | **greedy->optuna, n_splits=8, ver8** | 
| exp023 | 44.111543299653434 | - | **greedy->optuna, n_splits=8, ver9** | 
| exp024 | 43.885207515251004  | 43.4107321  | ensemble (exp14~exp023) |
| exp025 |  | - | **greedy**->optuna, n_splits=8, ver10 | 
| exp026 |  | - | **greedy**->optuna, n_splits=8, ver11 | 
| exp027 |  | - | **greedy**->optuna, n_splits=8, ver12 | 
| exp028 |  | - | **greedy**->optuna, n_splits=8, ver13 | 
| exp029 |  | - | **greedy**->optuna, n_splits=8, ver14 | 
| exp030 |  | - | **greedy**->optuna, n_splits=8, ver15 | 
| exp031 |  | - | **greedy**->optuna, n_splits=8, ver16 | 
| exp032 |  | - | **greedy**->optuna, n_splits=8, ver17 | 
| exp033 |  | - | **greedy**->optuna, n_splits=8, ver18 | 
| exp034 |  | - | greedy->optuna, n_splits=8, ver19 | 
| exp035 |  | | ensemble (exp25~exp034) |
| exp036 |  | - | greedy->optuna, n_splits=8, ver20 | 
| exp037 |  | - | greedy->optuna, n_splits=8, ver21 | 
| exp038 |  | - | greedy->optuna, n_splits=8, ver22 | 
| exp039 |  | - | greedy->optuna, n_splits=8, ver23 | 
| exp040 |  | - | greedy->optuna, n_splits=8, ver24 | 
| exp041 |  | - | greedy->optuna, n_splits=8, ver25 | 
| exp042 |  | - | greedy->optuna, n_splits=8, ver26 | 
| exp043 |  | - | greedy->optuna, n_splits=8, ver27 | 
| exp044 |  | - | greedy->optuna, n_splits=8, ver28 | 
| exp045 |  | - | greedy->optuna, n_splits=8, ver29 | 
| exp046 |  | | ensemble (~exp045) |
| 暫定目標 | 43.5? | 43.00 |  |