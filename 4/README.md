# RNA-seqカウントデータの前処理
本講義では、pandasを用いてRNA-seqカウントデータの処理を行います。

## RNA-seqとは
RNA-seqとは, mRNAやmiRNAの配列をシーケンスして、発現量の定量や新規転写産物の同定を行う手法です。<br>
シーケンスで得られたデータ（リード）は, 以下のようなステップで解析します。<br>
1. リードのトリミング
2. ゲノム配列へのマッピング
3. マッピングされたリード数を数える
4. サンプル毎の総リード数の違いや、遺伝子配列長の違いを補正（正規化）
5. 遺伝子毎の発現量を同定、比較

本講義では上記ステップのうち4以降を扱います。

##  本講義で用いるRNA-seqデータについて
本講義では, 疾患モデルマウスのRNA-seqデータセット（GSE190806）を使用します。<br>

Impaired KDM2B-mediated PRC1 recruitment to chromatin causes defective neural stem cell self-renewal and ASD/ID-like behaviors [RNA-Seq]<br>
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190806<br>
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190807<br>
（GSE190806とGSE190807のRNA-seqは同じSRAアクセッション）

このRNA-seqデータはINSDCのSRAデータベースにアクセッション番号 SRR17223720-SRR17223725 としてアーカイブされています。<br>
SRR17223720-SRR17223722 Neural progenitor cells(C57BL/6J由来), wild-type<br>
SRR17223723-SRR17223725 Neural progenitor cells(C57BL/6J由来), Kdm2b one allele mutant<br>
このほか, サンプルの詳細は以下の論文を参照してください。<br>

Impaired KDM2B-mediated PRC1 recruitment to chromatin causes defective neural stem cell self- renewal and ASD/ID-like behaviors<br>
DOI:https://doi.org/10.1016/j.isci.2022.103742


アーカイブされたデータをダウンロードして遺伝子ごとのカウントデータにするまでの手順と, 使用したソフトウェアは以下の通りです。<br>

1. シークエンスデータの取得 fasterq-dump v3.0.0 ( https://github.com/ncbi/sra-tools )
2. リファレンス:GRCm39のcDNA配列（ Mus_musculus.GRCm39.cdna.all.fa, http://asia.ensembl.org/Mus_musculus/Info/Index )
3. リードの前処理 (リードトリミング、クオリティフィルタリングなど) fastp v0.23.2 ( https://github.com/OpenGene/fastp )
4. 転写産物の定量 kallisto v0.48.0 ( https://github.com/pachterlab/kallisto )

これらの処理の詳しい内容については本講習会では扱いませんが、<br>
手順を[kallisto_count.md](misc/kallisto_count.md)にまとめました。

## 本講義で行うRNA-seqデータの処理

- サンプルごとのカウントデータを1つのカウントテーブルにまとめる
- データの読み込み
- カウントデータの正規化（ RPM/FPM, FPKM, TPM)
- サンプル間のクラスタリング　
- 遺伝子のアノテーション( transcript_idとgene_idの対応、gene_idに対応したdescriptionの付与 )
- 発現量比 ( fold-change )の計算