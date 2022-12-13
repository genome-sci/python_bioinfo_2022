# pandasの基本操作

実験医学別冊　独習Pythonバイオ情報解析　第6章　(2021年、先進ゲノム解析研究推進プラットフォーム編、羊土社、ISBN978-4-7581-2249-8) のまとめ

- pandas はデータ解析用のライブラリで, 主な対象は二次元の表形式データ (DataFrame)
- 行列・多次元配列を扱う数値計算ライブラリ numpy が使われている
- 時系列データや文字データなどを含んだ様々な表形式ファイルを扱うことができる

## 1. 準備

pandasとnumpyをimport
```
import pandas as pd
import numpy as np
```

## 2. Series

一次元データのデータオブジェクト

```
# Seriesの作成
L1 = [100, 200, 300, 400, 500]
s1 = pd.Series(L1)

# 任意のindexをつける
s1 = pd.Series(L1,index=["geneA", "geneB", "geneC", "geneD", "geneE"])

# 四則計算
s2 = s1 / 10

# SeriesとSeriesのかけ算では, 同じ位置にある要素同士が計算される
s1 * s2

# 単独の要素の取得(例:左から4番目の要素)
s1[3]

# スライスを使う
s1[2:5]

# 複数の位置の指定(リストを使う)
targets = [0, 2, 4]
s1[targets]

# 同じ結果になる
s1[[0, 2, 4]]

# indexを使ったデータの切り出し
s1["geneA"]

# 辞書を使ったindexでSeriesを作成
D = {'Chlamydomonas': 'reinhardtii','Volvox': 'carteri', 'Coccomyxa': 'subellipsoidea', 'Coffea': ' arabica'}
s2 = pd.Series(D)

# indexは重複していても使える
data= [ 'reinhardtii', 'carteri',  'subellipsoidea_C_169', ' arabica', 'canephora']
index = ['Chlamydomonas',  'Volvox', 'Coccomyxa', 'Coffea', 'Coffea']
s3 = pd.Series(data=data, index=index)

#indexの取り出し
s3.index

# データの取り出し
s3.values

# データ形式の確認（numpy.ndarray）　
type(s3.values)
```
**練習**　indexが Chlamydomonas, Volvox である値の取り出し
```
# ヒント:取りたいindexをリストにします
s3[ (この中を書いてください) ]
```

**練習** 次の出力を比べてみよう
```
s3['Coffea']　# 値が複数ある
s3['Chlamydomonas']　# 値は1つだけ
```

## 3. DataFrame
二次元の表を扱うためのデータオブジェクト

DataFrameの作成<br>
`pd.DataFrame(data, index, columns, ....)`

引数
- `data` :二次元リストや辞書などを指定
- `index`:行ラベル
- `columns`:列ラベル(デフォルトでは 0, 1, 2, .. ）

ファイルから読み込む場合
- `pd.read_table()`
- `pd.read_csv()`
- `pd.read_clipboard()` # クリップボードから読み込む
- `pd.read_excel()`

```
# 例
data = [[1, 3, 2],
        [10, 20, 30],
        [100, 200, 300],
        [1000, 2000, 3000]]
columns = ['sample1', 'sample2', 'sample3']
df1 = pd.DataFrame(data, columns=columns)

# 任意のインデックスをつける
df1.index = ['geneA','geneB','geneC','geneD']

# 辞書データからDataFrameを作る
D = {'generic_name': ['Chlamydomonas', 'Volvox','Ostreococcus' ,'Coccomyxa', 'Marchantia','Thalassiosira'],
     'specific_name': ['reinhardtii', 'carteri','lucimarinus', 'subellipsoidea C-169', 'polymorpha','pseudonana'],
     'assemble_version': ['v5.5','v2.1','v2.0','v2.0','v3.1','V3.0'],
     'genome_size': [111.1,131.2,13.2,49,225.8,34],
     'common_name':['green algae','green algae','green algae','green algae','liverwort','diatom'],
     'unicellular': [True,False,True,True,False,True]
     }
df2 = pd.DataFrame(D)

# カラム名（列ラベル）の参照
df2.columns

# index（行ラベル）の参照
df2.index
```

DataFrameを使った計算
```
# 四則演算
df1 * 10 # df1は変更されないことに注意（df1 = df1*10のように代入）

# リストやSeriesとの計算
L = [1, 2, 3]
df1 + L

# 各行の要素数とリストの要素数が合わないとエラーになる
L = [1, 2, 3, 4]
df1 + L 　

# 横方向にブロードキャスト
L = [1, 2, 3, 4]
(df1.T + L).T # 行と列を転置させて計算し, 再び転置
```
集計
```
df1.sum()  # 列ごとの合計 (axis=0)
df1.sum(axis=1) # 行ごとの合計
df1.mean() # 平均
df1.cumsum(axis=0) # 累積 (上で紹介した他の集計関数と異なり, 結果はDataFrameとして返る)
```
ソート
```
# インデックスでソート
df1.sort_index(ascending=False) # 降順でソート(デフォルトは昇順)

# 要素の値でのソート
# 列の値でソート
df2.sort_values(by='genome_size', na_position='first') # df2は変更なし

df2.sort_values(by='generic_name', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last') # df2を書き換える（破壊的変更）

# indexでソート
df2.sort_index(ascending=True, inplace=True)

# 列の順序を変える
df1.sort_values(by="geneA", axis=1).head(2) # geneAの行の値で、左から昇順( 1 → 2 → 3 )に並べ替える, 行なのでaxis=1を指定
```

## 4. DataFrameの行・列・要素の抽出

列の抽出
```
df['A'] # 列名で指定
df.A
```
複数列の場合にはリストで指定する（`[ ]` が二重 `[[ ]]` になることに注意）
```
df[['A', 'B']]
```

行の抽出 ( loc or ilocを使う )
```
df.loc[row_index]
df.iloc[row_position]
```
複数行の場合には、
```
df.loc[[row_index1, row_index2]]
df.iloc[[row_position1, row_position2]]
df.iloc[row_position1:row_position2]
```

範囲の抽出 ( loc or ilocを使う )
```
df.loc[[row_index1, row_index2], [col_index1, col_index2]]
df.iloc[[row_position1, row_position2], [col_position1, col_position2]]
df.iloc[row_position1:row_position2, col_position1:col_position2]
```

値の抽出 ( at or iatを使う;loc or ilocよりも速い )
```
df.at[row_index, col_index]
df.iat[row_position, col_position]
```

条件を指定して抽出 ( boolean indexing )
```
# 抽出対象をbool値（TrueまたはFalse）のリストで指定
targets = [True, True, False, False, True, False]
df2[targets]

# df2から `unicellular=True` のデータのみを抽出
df2[df2.unicellular]

# unicellularではないものを抽出
df2[~df2.unicellular]

# genome_size 列の値が100以上のものを抽出
df2[df2.genome_size >= 100]

# common_name 列の値が green algae であるものを抽出
df2[df2['common_name'] == 'green algae']
```

**練習**　df2 のcommon_name 列の値が diatom であるものを抽出
```
# 以下を埋めてください
df2[df2[ 　　　　　] 　　　　　　]
```

## 5. 行・列の追加と編集

列の追加
```
df1['sample4'] = [4, 40, 400, 4000]  # すでにsample4列が存在している場合には上書きされる
```

列の編集
```
# sample3列の値を10倍に
df1['sample3'] = df1['sample3'] * 10

# sample4列を全て入れ替え
df1['sample4'] = [4, 44, 444, 4444]　# 入れ替えたい値をリストで指定

# sample1 ~ sample4 の平均をAVERAGE列として追加
df1['AVERAGE'] = (df1['sample1'] + df1['sample2'] + df1['sample3'] + df1['sample4']) / #

# `mean()` 関数を使う場合
df1['AVERAGE2'] = df1[['sample1', 'sample2', 'sample3', 'sample4']].mean(axis=1)
```

列の削除
```
# 列の削除はaxis=1,デフォルト(axis=0)は行の削除
df1.drop('AVERAGE', axis=1)

# 複数列の指定
df1.drop(['AVERAGE', 'AVERAGE2'], axis=1)
```
`drop()`は非破壊的変更なので,`df`を変更するためには, `df = df.drop('AVERAGE', axis=1)`と代入します。<br>
`del` を使っても削除可能です。ただし, 破壊的変更なので代入なしで即座に反映
```
del df1['AVERAGE'], df1['AVERAGE2'],  df1['sample4']
```
`del df1[['AVERAGE', 'AVERAGE2', 'sample4']]` はエラーになる<br><br>

行の追加
```
# 追加したい行データをSeriesとして作成<br>
geneE = pd.Series([9,99,999], index = df1.columns, name = 'geneE')

# 行を追加
df1 = df1.append(geneE)
```

行の編集<br>
`loc` または `iloc` を使って行を指定
```
# 4行目の値を10倍に
df1.iloc[4] = df1.iloc[4]*10

# ４行目（indexはgeneE）を1/10に
df1.loc['geneE'] = df1.loc['geneE'] / 10

# 要素の値を指定する
df1.loc['geneA', 'sample1'] = 0
```

行の削除
```
df1 = df1.drop('geneE')
```

## 6. 欠損値・重複の扱い

```
# テストデータの読み込み  <br>
df3 = pd.read_table('test_matrix_data.tsv', index_col=0)

# データの大きさを確認
df3.shape # 30行 x 7列
```

欠損値の削除
```
# データに欠損値（ NaN ）がある行すべてを削除
df3.dropna() # data_12 の E列に NaN があるため削除される
```
上記ではdf3自体は変わっていない<br>
df3を変更するには `df3 = df3.dropna()`または, `df3.dropna(inplace=True)`とする<br>

```
# 何行削除されたか確認
df3.dropna().shape  # 26行×7列(4行削除)
```
デフォルト(`axis=0`)では欠損値を含む`行`を削除<br>
欠損値を含む`列`を削除する場合、`axis=1`とする<br>

その他のオプション
- `subset` 特定の行に欠損値が含まれている場合を削除対象にする
- `thresh` 欠損値の数の閾値を指定する

欠損値の補完
```
# 欠損値を 0 で補完
df3.fillna(0)

# C列を0, E列を1で補完
Dic = {"C": 0, "E": 1}
df3.fillna(Dic)

# 各列の平均で補完
df3.fillna(df3.mean())

# 前後の値による補完
df3.interpolate()
```

重複の除去

デフォルトでは、行全体の値が重複していた場合に削除<br>
`subset='列名'` でその列に重複値がある場合に削除

デフォルトでは、先頭の行のみ残して以後の行を削除(`keep="first"`)<br>
`keep=False`で重複している行すべてを削除する

```
df3.drop_duplicates(subset='D') # data_10が残る
```

**参考**

- pandasでは、DataFrameに対する操作の多くは __非破壊的変更__ (自分自身を変更させるのではなく、新しいDataFrameを返す）
- このため、複数のメソッドを連結して使用できる（メソッドチェイン）
```
df3.dropna().drop_duplicates(subset="D").sort_index().head()
```

## 7. DataFrame、または行・列に対しての関数の適用

DataFrameの集計メソッド
```
df3.sum()
df2.sum()
```
numpyの関数を利用 <br>
numpyのユニバーサル関数(行列の要素ごとに処理を行う関数)
```
# 常用対数
np.log10(df1)
```

特定の列や行に対してnumpyのユニバーサル関数を実行
```
# 平方根
np.sqrt(df1['sample2'])

df1["sample2"] = np.sqrt(df1["sample2"]) # 値を更新する場合

# 四捨五入
np.round(df3.iloc[1])

# 集計関数の利用
# 分散を求める
np.var(df3)
np.var(df1, axis=1) # 行方向に適用
np.var(df1, ddof=1) # 不偏分散（N-1で割る）
```
pandas.DataFrameの`var()`は デフォルトで `ddof=1` として計算
```
df1.var()
```
```
# 標準偏差
np.std(df1) # numpy
df1.std() # pandas.DataFrame
```

map, apply, applymapで関数をDataFrameや行・列に適用

(ただし、numpy やDataFrameのメソッドに定義されている場合は、それを使用した方が処理が早い)
```
# テスト用関数1:
# 引数xが文字列であれば小文字に変換、そうでなければ "-" を返す

def my_lower(x):
    if isinstance(x, str):
        return x.lower()
    else:
        return "-"
```

`map()` でSeries（DataFrameの行・列）の各要素に関数を適用
```
df2['generic_name'].map(my_lower)
```

`applymap()`でDataFrameの各要素に関数を適用
```
df2.applymap(my_lower)
```

`pandas.Series.apply()`でより複雑な関数をSeries（DataFrameの行・列）の各要素に適用
```
# テスト用関数2:
# 第一引数xが数値であれば、小数第n位までの概数にする(nは負の値も可)

def my_round(x, n):
    if isinstance(x, int) or isinstance(x, float):
        return round(x, n)
    else:
        return np.NaN
```
```
test_s = pd.Series([3.89, 2.192, 15.3921, 43.903, 390.083, 239.622])
test_s.apply(my_round, args=(2,)) # 'args=' に第2引数以降をtupleとして与える
```

`pandas.DataFrame.apply()`でDataFrameの行または列ごとに関数を適用<br>
(`pandas.DataFrame.apply()` と `pandas.Series.apply()` は使い方が異なる)
```
# テスト用集計関数3:
# Series (DataFrameの行 or 列)を受け取りthresholdより値が大きいものの個数を返す

def count_larger_than(S, threshold=0):
    assert isinstance(S, pd.core.series.Series)  # SがSeriesであるかチェックを行っている
    return len([x for x in S if x > threshold])
```
```
# 関数の動作確認
s_test = pd.Series([1,3,5,6,8])
count_larger_than(s_test, 5)

# 関数を列に適用
df1.apply(count_larger_than, args=(10,))

# 関数を行に適用（axis = 1)
df1.apply(count_larger_than, args=(10,), axis=1)
```

**練習** <br>
Zscore（平均値を引いた後、標準偏差で割る）を計算する関数を作る
```
# Seriesを引数として受け取り, Zscoreに変換してSeriesとして返す

def zscore(S):
    mean =   　　　# 平均を求める
    stdev =   　　　# 標準偏差を求める
    return (S - mean) / stdev

# 関数の適用
df1.apply(zscore)
```

参考<br>
`apply()` を使わずにZscoreを計算
```
mean = df1.mean()
stdev = df1.std()
df_z = (df1-mean)/stdev
```

## 8. 行・列のループ処理

DataFrameをそのままループで回す
```
for x in df1:
    print(x, type(x))
```

`iterrows()`で1行ずつ取り出す<br>
indexと行データ(Series)がtupleとして取り出せる
```
for index, row in df1.iterrows():
    print("INDEX =", index)
    print(list(row))
    print("-----")
```
`items( )`で1列ずつ取り出す<br>
各列の列名および列データ(Series)がtupleとして取り出せる<br>
なお、`iteritems()`は、pandas1.5.0で廃止
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iteritems.html
```
for col_name, col in df1.items():
    print("Column name =", col_name)
    print(list(col))
    print("-----")
```
### forループを使う場合の注意点

N行x100列のテストデータの各要素を四捨五入した値に書き換える処理にかかる時間を、ループ処理と`applymap()` を使った処理で比較<br>
```
# テストデータを作る
N=100
test_df = pd.DataFrame(np.random.rand(N, 100) * 10)　# 0~10のランダムな小数
```
```
%%time
# locを使う
for row_index, row in test_df.iterrows():
    for column_index in row.index:
        test_df.loc[row_index, column_index] = round(test_df.loc[row_index, column_index])
        # test_df.at[row_index, column_index] = round(test_df.at[row_index, column_index])
```

`loc` のかわりに `at` を使うと0.2秒程度まで改善される
```
%%time
# atを使う
for row_index, row in test_df.iterrows():
    for column_index in row.index:
        test_df.at[row_index, column_index] = round(test_df.at[row_index, column_index])
```
applymapを使う
```
%%time
test_df = test_df.applymap(round)
```

forループの中で時間のかかる処理を行うと遅くなる<br>
以下の場合、処理速度は 1 < 2 < 3
1. numpy や pandas の関数・メソッドを使用
2. apply や applymap で行・列・DataFrame全体に関数を適用する
3. for ループを回して処理する

## 9. DataFrameの結合

`concat( )`<br>
2つ（またはそれ以上）のDataFrameを縦・横方向に連結<br>
共通するindexや列ラベルがあれば, それらを利用して結び付けられる
```
df_A = pd.DataFrame([['A0','A1','A2'],
                     ['B0','B1','B2'],
                     ['C0','C1','C2'],
                     ['D0','D1','D2']],
                    columns=[0,1,2],
                    index=['A','B','C','D'])
df_B = pd.DataFrame([['E0','E1','E2','E3'],
                     ['F0','F1','F2','F3'],
                     ['G0','G1','G2','G3'],
                     ['H0','H1','H2','H3']],
                    columns=[0,1,2,3],
                    index=['E','F','G','H'])
df_C = pd.DataFrame([['A3','A4','A5'],
                     ['B3','B4','B5'],
                     ['C3','C4','C5'],
                     ['D3','D4','D5']],
                    columns=[3,4,5],
                    index=['A','B','C','D'])

# 縦に連結
pd.concat([df_A, df_B])

# 横方向に(axis=1), 共通する行ラベルで連結
pd.concat([df_A, df_C], axis=1)

# pandas.DataFrame.append( )で縦方向に結合
df_A.append(df_B)
```

`join( )` <br>
index（行ラベル）をkeyとして連結するときに便利
```
# テスト用データ
df_L = pd.DataFrame([1.2, 0.8, 2.3, 3.5, 2.2, 0.3],
                    index=['gene_1', 'gene_2', 'gene_3', 'gene_4', 'gene_5', 'gene_6'],
                    columns=['DE'])

df_R = pd.DataFrame(['50S ribosome-binding GTPase','Surface antigen',
                     'Elongation factor Tu GTP binding domain','Ring finger domain'],
                    index=['gene_1', 'gene_2', 'gene_4', 'gene_6'],
                    columns=['definition'])

# 左のDataFrame（df_L）の行はすべて出力 (how="left")
df_L.join(df_R)

# 両方のDataFrameに共通して存在するもののみ出力
df_L.join(df_R, how='inner')

# pd.concat()でも同じ
pd.concat([df_L, df_R], axis=1,sort=False)
```

`merge( )`<br>
index以外をkeyとして連結するときに便利<br>
多くのオプションがあるので詳細はpandas公式を参照
```
df_L = pd.DataFrame([['gene_1','PF00009'],
                     ['gene_2','PF01103'],
                     ['gene_3','PF01926'],
                     ['gene_4','PF01926'],
                     ['gene_5','PF13639'],
                     ['gene_6','PF02225']],
                    columns=['gene_id', 'PFAM_id',])
df_R = pd.DataFrame([['PF01926','50S ribosome-binding GTPase'],
                     ['PF01103','Surface antigen'],
                     ['PF00009','Elongation factor Tu GTP binding domain'],
                     ['PF13639', 'Ring finger domain']],
                    columns=['PFAM_id', 'definition'])
```
この例では, 共通する列ラベル `PFAM_id` をkeyとして結合<br>
keyは、`on` , `left_on` , `right_on` で指定<br>
indexの値をkeyとする場合は `left_index` 、`right_index` <br>

デフォルトでは __innerjoin__ (`how='inner'`)、両方のデータに共通して存在するものが返る<br>
```
# 右側のDataFrame（df_R）にないPF02225が削除される
pd.merge(df_L, df_R)
```
__leftjoin__  (`how='left'`)では、左側のDataFrame（df_L）にあるものはすべて返る<br>
```
pd.merge(df_L, df_R, how='left')
```

```
# indexをkeyとして結合
pd.merge(df_A, df_C, left_index=True, right_index=True)

# 同じ
pd.concat([df_A, df_C], axis=1)

# pandas.DataFrameのメソッドとして
df_L.merge(df_R)
```

## 10. その他の機能

`multiindex`<br>
```
# 複数の列をindexにする
df2_multiindex = df2.set_index([df2.common_name, df2.generic_name])

# indexの指定
df2_multiindex.loc['green algae']

# tupleで複数indexの指定
df2_multiindex.loc[('green algae', 'Chlamydomonas')]
```

`groupby( )`<br>
```
# データをグルーピングして扱う
df2.groupby('common_name').count()
```

`pivot_table( )`<br>
```
# common_nameでグルーピングしgenome_sizeの平均を計算
df2.pivot_table(index='common_name', values='genome_size', aggfunc='mean')
```

### 2-11. DataFrameの書き出し

```
# indexに名前をつける(無くても良いが、無いとindex列が空欄になる)
df1.index.name = 'INDEX'

# outputフォルダに書き出し
df1.to_csv('output/dataframe1.tsv', sep='\t', header=True, index=True)
```

## 参考
- 実験医学別冊　独習Pythonバイオ情報解析　第6、7章　(2021年、先進ゲノム解析研究推進プラットフォーム編、羊土社、ISBN978-4-7581-2249-8)
- pandas 公式サイト　https://pandas.pydata.org
- note.nknk.me pandas関連記事まとめ　https://note.nkmk.me/python-pandas-post-summary/
- 10 Minutes to pandas https://pandas.pydata.org/pandas-docs/stable/10min.html <br>
- Pythonによるデータ分析入門~Numpy,pandasを使ったデータ処理~（Wes Mckinney著、小林儀匡ら訳、オライリージャパン、ISBN978-4-87311-655-6）<br>
