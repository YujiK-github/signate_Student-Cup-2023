## 解法の概要

### Cross Validationの設定
* 今回の目的変数の分布は多峰性を持っていた。
* 連続変数のStratifiedKFoldは連続変数をビニングして層にしてから行う。Binningには[pd.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html)が用いられるが、これは最大値(96818)と最小値(1004)のrangeをbins個に均等に分割する。それぞれ分割されたrangeに含まれる個数を考慮されない。
* カテゴリ変数の特徴量はtrainとtestで同じような分布をしていた。
  
以上の点からbinningするのではなく、priceを小さい順にそれぞれのfoldに振り分けることにした。

```python
train.sort_values(by="price", ignore_index=True, inplace=True)
train["fold"] = [i for i in range(CFG.n_splits)] * (train.shape[0] // CFG.n_splits) + [i for i in range(train.shape[0] % CFG.n_splits)]
```

### データの前処理
* yearの異常値の訂正
* manufacturer, sizeの表記揺れの統一
* stateの欠損値をregionから補完する
* odometerの異常値をregionを用いて補完する

### 特徴量エンジニアリング
今回は有用な特徴量を作成することが難しかった。そのため、各カテゴリカル変数をさまざまな形にエンコーディングし、連続変数に関しては交互作用を作った。さらに、複数のカテゴリカル変数でグルーピングしたtarget encodingを行うことで特徴量を大量に作成した。それらをgreedy forward selection(計算量を落としたver.)を用いて特徴量選択を行った。greedy forward selection(計算量を落としたver.)は特徴量の順番をseedで決めているため複数回行った。

### モデル
NN, lightGBM, XGBoost, CatBoostを試したがlightGBM以外は精度が低く、アンサンブルに加えてもほとんど精度の向上が見られなかった。objectiveはMAPE, metricはMAPEを使用した。

### アンサンブル
greedy forward selection(計算量を落としたver.)を行ったモデルをアンサンブルした。Optuna, [Nelder-Mead](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html), [Hill Climbing](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609), Stackingなどを行い、それらを2層目と3層目で試した。

## 他の参加者の解法
### [pan_yori_gohan](https://signate.jp/users/30823)  
>public 4位、private 4位の解法の主に自分が担当した部分です。
自分は2nd stage制で取り組んで1st stageをcatboost, 2nd stageをlightgbmで予測しました。
まず、catboostで予測を出した後に、lightgbmでの予測ではcatboostの予測も特徴量として加えて学習させました。
catboost単体の予測精度はCVが0.444程度でしたが、
lgbmでの学習時に特徴量としてその予測を加えるとCVが0.439、リーダボードスコアが43.19、プライベートスコアが43.11になりました。
catboostでは普通に予測すると精度があまり上がらなかったのですが、targetの対数をとって、その対数を直接mapeで予測し、その予測値の指数をとって0.7をかけるとかなりスコアが上がりました。
チームを組んでいたので、他のメンバーがxgboostも組み合わせたstackingと、tabnetを使用した予測を作成してくれたので、それらをアンサンブルすることで、リーダーボードスコアが43.089、プライベートスコアが43.064になりました。
特徴量の工夫としては他の方がやってくれていたregionからstateを補完や、odmeterをyearで割った特徴量などを加えました。
非常に勉強になりました。ありがとうございました。何か解法に関してご質問等ありましたらお気軽にご質問ください。


### [macky](https://signate.jp/users/55058)
>Publicが9位（大体）、Privateが3位、審査で最終順位が2位になりましたmackyです。
今年は解法のプレゼンが1位のみとのことですので、こちらに私の解法を記載させていただきます。
今回行ったことでスコア向上に効いたのは、大きく3つでした。
①odometerの欠損値処理：
テストデータのodometerが欠損している部分をlightgbmでRMSE予測しました。
訓練データにもodometerに欠損している箇所はありましたが、以降の②ではdropnaしています。
②2段階学習：
1段目はlightgbmでHuber lossでpriceを予測し、その予測結果を2段目のlightgbmの特徴量に加えました。
2段目のlightgbmはMAPEで予測しています。
③外れ値の除去：
CVの中で最もMAPEが高かった3つの行を削除しました。
特徴量エンジニアリングについて：
カテゴリ変数についてはtarget encoding、数値に関してはそのまま特徴量として使っています。
stateはregionとの組み合わせで埋めました。組み合わせがないものは手動で埋めました。
その他欠損値については、欠損値以外のカラムが同じ値の行を抜き出して、その最頻値で埋めました。
他にも色々試しましたが、スコアが上がらなかったので特徴量の数はほぼデフォルトです。
私自身改めて勉強になることが多くありました。運営及び参加者の皆様ありがとうございました。
解法についてはお気軽にご質問ください。

### [UTG_limp](https://signate.jp/users/82270)
目的変数がおおよそ二峰性を持っていたため、まずは二峰性のうちのどちらかに属するのかclassificationを行い、そのoutputを2段階目のregressionで特徴量として加えた。


## 個人的な反省
* 一位の方の発想は[私にもあった](https://github.com/YujiK-github/signate_StudentCup2023/blob/main/memo/split_price.ipynb)。しかし、私はclassificationのoutputを特徴量として用いるのではなく、それらを元にモデルを二つに分割することを考えていた。そしてf2 scoreが0.7885262049522774程度で断念した。
* 損失関数や評価指標を変えるのを忘れていた。
* チームでコンペに参加するのは初めてだった。自分の中にある発想をチームメンバーに話すことで別の切り口での考えを聞くことができ、また、思考が凝り固まらずに様々なことを実験できたのでソロでの参加に比べて学びのあるコンペとなった。可能な限りチームでコンペに参加しようと考えた。
