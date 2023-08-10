TODO: Neural Network  
TODO: transformers(fine-tuning) model  
TODO: transformers baseのembeddingを利用したmodel  
TODO: ensemble  
TODO: seed average  
TODO: catboost  
TODO: xgboost  
TODO: fold増やす  
TODO: 値段帯で分ける？？
TODO: 重複あるかも？？ -> 重複なかった


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
| 暫定目標 | 40 | 40 |  |