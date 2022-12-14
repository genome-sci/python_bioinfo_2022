# 事前準備

講習で用いる Python 実行環境を用意する。  
minicondaをインストールし、condaコマンドを使って仮想環境下にインストールすることを推奨。
Mac (Intel CPU) および Linux (Ubuntu) での動作を確認しているが、WindowsやM1 Macではインストールがうまくいかない可能性がある。

- Windowsで実行する場合  
一部のソフトがインストールできない可能性があるので、WSL2 を使って実行環境を構築すると良い。また、「Pythonを使ったシングルセルRNA-seq解析」の単元については本文書末尾の「トラブルシューティング」を参照。

- M1 Macで実行する場合
一部のソフトがインストールできない可能性がある。「Pythonを使ったシングルセルRNA-seq解析」の単元については本文書末尾の「トラブルシューティング」を参照。それ以外の単元についてはM1 Macでもおそらく動作可能。


### 実行環境の構築

minicondaインストール後、下記を実行する。
```
# 仮想環境作成
conda create -n pags2022 python=3.9
# 仮想環境に切り替え
conda activate pags2022
conda install -c conda-forge jupyter
conda install -c bioconda biopython bcbiogff
conda install -c conda-forge matplotlib-venn
conda install -c conda-forge scanpy python-igraph leidenalg
conda install -c conda-forge scvi-tools
conda install -c bioconda scvelo
conda install -c conda-forge -c bioconda cellrank
conda install -c conda-forge scikit-misc
conda install -c conda-forge joypy
```

また、本ディレクトリに含まれる `env.yaml` ファイルを使って
```
conda env create -f env.yml
```
としても良い。

仮想環境から抜けるには
```
conda deactivate
```
を行う。

### トラブルシューティング

「Pythonを使ったシングルセルRNA-seq解析」の単元で使用する scanpy, scvi-tools, scvelo, cellrank, scikit-misc といったライブラリは環境によってはインストールに失敗することがある。
その場合には、https://github.com/khigashi1987/scRNAseq_handson のページに記載されている Google Colaboratory で実行する方法、または、Docker で実行する方法のいずれかで講習に参加することができる。
