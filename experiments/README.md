TODO: Neural Network  
TODO: transformers(fine-tuning) model  
TODO: transformers baseのembeddingを利用したmodel  
TODO: ensemble(Weighted Average: optuna?, Stacking, [Hill Climbing](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609), [Nelder-Mead](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369538))  
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
| exp014 | 43.966795960812284 | - | greedy->optuna, n_splits=8, ver0 **(n_splits=5->8)** | 
| exp015 | 44.11063297972305 | - | greedy->optuna, n_splits=8, ver1 | 
| exp016 | 44.06125663376067 | - | greedy->optuna, n_splits=8, ver2 | 
| exp017 | 44.12841111907897 | - | greedy->optuna, n_splits=8, ver3 | 
| exp018 | 44.01755664381658 | - | greedy->optuna, n_splits=8, ver4 | 
| exp019 | 43.98915506706626 | - | greedy->optuna, n_splits=8, ver5 | 
| exp020 | 44.052070379194966 | - | greedy->optuna, n_splits=8, ver6 | 
| exp021 | 43.979683002688965 | - | greedy->optuna, n_splits=8, ver7 | 
| exp022 | 44.02074386662909 | - | greedy->optuna, n_splits=8, ver8 | 
| exp023 | 44.111543299653434 | - | greedy->optuna, n_splits=8, ver9 | 
| exp024 | 43.885207515251004  | 43.4107321  | ensemble (exp14~exp023) |
| exp025 | 43.87820413829381  | 43.4288652  | ensemble (exp14~exp023+kun4qi:exp038~exp040) |
| exp026 | 43.85695527186413 | 43.4045397 | greedy->optuna, n_splits=8, ver10 | 
| exp027 | 43.94810422364445 | - | greedy->optuna, n_splits=8, ver11 | 
| exp028 | 43.805041424202756 | 43.5306013 | greedy->optuna, n_splits=8, ver12 | 
| exp029 | 43.98296206957362 | - | greedy->optuna, n_splits=8, ver13 | 
| exp030 | 43.87890169196959 | - | greedy->optuna, n_splits=8, ver14 | 
| exp031 | 43.94966528280684 | - | greedy->optuna, n_splits=8, ver15 | 
| exp032 | 43.9866490416345 | - | greedy->optuna, n_splits=8, ver16 | 
| exp033 | 43.90702260712451 | - | greedy->optuna, n_splits=8, ver17 | 
| exp034 | 44.00234699503871 | - | greedy->optuna, n_splits=8, ver18 |
| exp035 | 44.00072184877421 | - | greedy->optuna, n_splits=8, ver19 |
| exp036 | **43.707553358225496** | 43.3956187 | ensemble(exp026~035)(seed=42) |
| exp037 | 43.71498987687226 | 43.4082446 | ensemble(exp026~035)(seed=43) |
| exp038 | 43.723440087378485 | **43.3202885** | ensemble(exp026~035)(seed=44) |
| exp039 | 44.052603595706614 | - | greedy->optuna, n_splits=8, ver20 |
| exp040 | 43.97334761799733 | - | greedy->optuna, n_splits=8, ver21 |
| exp041 | 43.92495216461714 | - | greedy->optuna, n_splits=8, ver22 |
| exp042 | 43.96098462821153 | - | greedy->optuna, n_splits=8, ver23 |
| exp043 | 43.880146795910825 | - | greedy->optuna, n_splits=8, ver24 |
| exp044 | 43.9921719388979 | - | greedy->optuna, n_splits=8, ver25 |
| exp045 | 45.04930871968063 | - | greedy->optuna, n_splits=8, ver26 |
| exp046 | 44.70696228280802 | - | greedy->optuna, n_splits=8, ver27 |
| exp047 | 43.88715221105957 | - | greedy->optuna, n_splits=8, ver28 |
| exp048 | 43.82720801614026 | - | greedy->optuna, n_splits=8, ver29 |
| exp049 | 43.69660836605411 | 43.2657786 | ensemble(exp039~048)(seed=42) |
| exp050 | - | - | fileを集約 |
| exp051 | 43.56925636218776 | 43.2500502 | exp50に対してHill Climbingを適用 |
| exp052 | 43.572764461334195 | 43.2432630 | exp50に対してSimple Greedy Forward Selectionを適用(1) |
| exp053 | 43.581332152377506 | 43.2406218 | exp50に対してSimple Greedy Forward Selectionを適用(2) |
| exp054 | 43.58019939649411 | 43.2620733 | exp50に対してSimple Greedy Forward Selectionを適用(3) |
| exp055 | 43.97979077815365 | - | greedy->optuna, n_splits=8, ver30 |
| exp056 | 44.02700513287697 | - | greedy->optuna, n_splits=8, ver31 |
| exp057 | 44.01000090608199  | - | greedy->optuna, n_splits=8, ver32 |
| exp058 | 43.88155550572779 | - | greedy->optuna, n_splits=8, ver33 |
| exp059 | 44.017131070289715 | - | greedy->optuna, n_splits=8, ver34 |
| exp060 | 44.21214679361081 | - | greedy->optuna, n_splits=8, ver35 |
| exp061 | 43.92204486548245 | - | greedy->optuna, n_splits=8, ver36 |
| exp062 | 44.00450581631167 | - | greedy->optuna, n_splits=8, ver37 |
| exp063 | 44.21383091797129 | - | greedy->optuna, n_splits=8, ver38 |
| exp064 | 44.09007864149579 | - | greedy->optuna, n_splits=8, ver39 |
| exp065 | - | - | fileを集約 |
| exp066 | 43.56453307604806 | | exp65に対してHill Climbingを適用 |
| exp067 | 43.58216667876671 | | exp65に対してSimple Greedy Forward Selectionを適用(1) |
| exp068 | 43.583016983994256 | | exp65に対してSimple Greedy Forward Selectionを適用(2) |
| exp069 | 43.58368909587582 | | exp65に対してSimple Greedy Forward Selectionを適用(3) |
| exp070 | 43.5824156325436 | | exp65に対してSimple Greedy Forward Selectionを適用(4) |
| exp071 | 43.582951599388245 | | exp65に対してSimple Greedy Forward Selectionを適用(5) |
| exp072 | 43.500996476403245 |  | exp051~054+kun4qi(exp055, exp056)に対してOptunaを適用 |
| exp073 | 43.49803242660311 |  | exp051~054+kun4qi(exp055, exp056)に対してHill Climbingを適用 |
| exp074 | 43.49763793970716 |  | exp051~054+kun4qi(exp055, exp056)に対してSimple Greedy Forward Selectionを適用(1) |
| exp075 | 43.49799517555315 |  | exp051~054+kun4qi(exp055, exp056)に対してSimple Greedy Forward Selectionを適用(2) |
| exp076 | 43.49790678952483 |  | exp051~054+kun4qi(exp055, exp056)に対してSimple Greedy Forward Selectionを適用(3) |
| exp077 | 43.61044144258124 |  | exp051~054+kun4qi(exp055, exp056)に対してstacking_lgb |
| exp078 | 43.512634988062615 |  | exp060シリーズ2段階目に対してSimple Greedy Forward Selectionを適用(1) |
| exp079 | 43.511237476304665 |  | exp060シリーズ2段階目に対してSimple Greedy Forward Selectionを適用(2) |
| exp080 | 43.51222899019721 |  | exp060シリーズ2段階目に対してSimple Greedy Forward Selectionを適用(3) |
| exp081 | 43.512610839373686 |  | exp060シリーズ2段階目に対してHill Climbing |
| exp082 | 43.525503530105766 |  | exp060シリーズ2段階目に対してoptuna |
| 暫定目標 | 43.5? | 43.00 |  |



### exp050
#### 1段階目  
純粋な予測モデル(30+10個)

#### 2段階目
| method | CV | LB | filename |
| - | - | - | - |
| Nelder-Mead | 43.57204422204847 | 43.2521041 | kun4qi exp55 |
| stacking_lgb | 43.60 |  | kun4qi exp56 |
| Hill Climbing | 43.56925636218776 | 43.2500502 | Yuji.K exp051 |
| Simple Greedy1 | 43.56925636218776 | 43.2432630 | Yuji.K exp052 |
| Simple Greedy2 | 43.56925636218776 | 43.2406218 | Yuji.K exp053 |
| Simple Greedy3 | 43.56925636218776 | 43.2620733 | Yuji.K exp054 |

#### 3段階目
| method | CV | LB | filename |
| - | - | - | - |
| Nelder-Mead | 43.496076310831896 | 43.1864741 | kun4qi exp61 |
| stacking_lgb | 43.54 |  | kun4qi exp62 |
| Optuna | 43.501541457142345 |  | Yuji.K exp072 | 
| Hill Climbing | 43.500996476403245 | 43.1851463 | Yuji.K exp073 |
| Simple Greedy1 | 43.49803242660311 | 43.1838002 | Yuji.K exp074 |
| Simple Greedy2 | 43.49799517555315 | 43.1832022 | Yuji.K exp075 |
| Simple Greedy3 | 43.49790678952483 | 43.1836722 | Yuji.K exp076 |


#### 4段目
| method | CV | LB | filename | 
| - | - | - | - |
| Nelder-Mead | 43.47638114611345 | | kun4qi exp065 | 
| Optuna | 43.47844292303129 |  | exp083 |
| Hill Climbing | 43.47778313918253 | |  exp084 |
| Simple Greedy1 | 43.47776380559784 | 43.1874960	 | exp085 |
| Simple Greedy2 | 43.477767793581286 |  | exp086 |
| Simple Greedy3 | 43.477758376378624 | 43.1874610 | exp087 |


### exp065
#### 1段階目  
純粋な予測モデル(40+10個)

#### 2段階目
| method | CV | LB | filename |
| - | - | - | - |
| Nelder-Mead | 43.56340118610674 | | kun4qi exp60 |
| stacking_lgb | 43.61044144258124 |  | Yuji.K exp077 |
| Hill Climbing | 43.56453307604806 | | Yuji.K exp066 |
| Simple Greedy1 | 43.58216667876671 | | Yuji.K exp067 |
| Simple Greedy2 | 43.583016983994256 | | Yuji.K exp068 |
| Simple Greedy3 | 43.58368909587582 | | Yuji.K exp069 |
| Simple Greedy4 | 43.5824156325436 | | Yuji.K exp070 |
| Simple Greedy5 | 43.582951599388245 | | Yuji.K exp071 |

#### 3段階目
| method | CV | LB | filename |
| - | - | - | - |
| Nelder-Mead | 43.5075 | | |
| stacking_lgb | |  | |
| Optuna | 43.525503530105766 |  | Yuji.exp082 | 
| Hill Climbing | 43.512610839373686 |  | Yuji.K exp081 |
| Simple Greedy1 | 43.512634988062615 |  | Yuji.K exp078 |
| Simple Greedy2 | 43.511237476304665 |  | Yuji.K exp079 |
| Simple Greedy3 | 43.51222899019721 |  | Yuji.K exp080 |