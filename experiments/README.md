TODO: Neural Network  
TODO: transformers(fine-tuning) model  
TODO: transformers baseのembeddingを利用したmodel  
TODO: ensemble  
TODO: seed average  
TODO: catboost  
TODO: xgboost  
TODO: fold増やす

| file | CV | LB | description |
| - | - | - | - |
| exp001 | 66.11899904620047 | 64.5174611 | baseline_lgb<br>yearとpriceのMultilabelStratifiedKFold |
| exp002 | 64.72120662038989 | 63.4342250 | baseline_cat<br>yearとpriceのMultilabelStratifiedKFold |
| exp003 | 45.84279120500015 | 45.1154626 | baseline_ensemble(cat+lgb)<br>yearとpriceのMultilabelStratifiedKFold |
| exp004 | 44.6154644289379 | 44.0886434 | baseline_lgbから変更<br>**price_mapでのStratifiedKFold**<br>odometerの補完や色々なencodingを追加<br>with optuna |
| exp005 | 44.20309555007229 | 43.6297815 | exp004からパラメータ変更<br>**price_mapでのStratifiedKFold**<br>odometerの補完や色々なencodingを追加<br>with optuna |
| exp006 | 44.16365041018153 | 43.7463188 | simple greedy selectionを使って特徴量選択した5個のモデルのアンサンブル<br>**price_mapでのStratifiedKFold**<br> with optuna |
| 暫定目標 | 40 | 40 |  |