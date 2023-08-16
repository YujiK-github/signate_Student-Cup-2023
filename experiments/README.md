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
| 10 | 45.38139862504485 |
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
| 暫定目標 | 43.5? | 43.00 |  |