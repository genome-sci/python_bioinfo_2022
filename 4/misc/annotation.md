# annotationデータ作成

## transcript IDとgene nameの対応表作成
2022-11-28

こんな感じの表を作りたい

|transcript_id        | transcript_name | gene_id           |
|---------------------|-----------------|-------------------|
|ENSMUST00000070533.5 | Xkr4-201        | ENSMUSG00000051951|

gffからmRNAの行を抽出

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/mRNA/{print}'|head -1
```
出力
```
1	ensembl_havana	mRNA	3284705	3741721	.	-	.	ID=transcript:ENSMUST00000070533;Parent=gene:ENSMUSG00000051951;Name=Xkr4-201;biotype=protein_coding;ccdsid=CCDS14803.1;tag=basic,Ensembl_canonical;transcript_id=ENSMUST00000070533;transcript_support_level=1 (assigned to previous version 4);version=5
```

最終列（attributes）を抽出

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/mRNA/{print}'|awk -F"\t" '{print $NF}'|head -1
```
出力
```
ID=transcript:ENSMUST00000070533;Parent=gene:ENSMUSG00000051951;Name=Xkr4-201;biotype=protein_coding;ccdsid=CCDS14803.1;tag=basic,Ensembl_canonical;transcript_id=ENSMUST00000070533;transcript_support_level=1 (assigned to previous version 4);version=5
```

`;` で列を分割、`ID=`, `Parent=`, `Name=` と `version=` の列を抽出、列の区切りを `=` にする

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/mRNA/{print}'|awk -F"\t" '{print $NF}'|awk -F";" '{print $1"="$2"="$3"="$NF}'|head -1
```
出力
```
ID=transcript:ENSMUST00000070533=Parent=gene:ENSMUSG00000051951=Name=Xkr4-201=version=5
```

余分な列を除いて一気に最終形にする

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/mRNA/{print}'|awk -F"\t" '{print $NF}'|awk -F";" '{print $1"="$2"="$3"="$NF}'|tr ":" "="|awk -F"=" '{print $3"."$NF"\t"$(NF-2)"\t"$6}'|head -1
```
出力
```
ENSMUST00000070533.5	Xkr4-201	ENSMUSG00000051951
```

`gene_id`（3列目）で`sort`して完成

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/mRNA/{print}'|awk -F"\t" '{print $NF}'|awk -F";" '{print $1"="$2"="$3"="$NF}'|tr ":" "="|awk -F"=" '{print $3"."$NF"\t"$(NF-2)"\t"$6}' |sort -k 3,3 > transcript_name.tsv
```

エントリの数

```sh
wc -l transcript_name.tsv
```
出力
```
66511 transcript_name.tsv
```

## gene idとdescriptionの対応表
2022-11-28

こんな表を作りたい

|gene_id           | gene name | description |
|------------------|-----------|-------------|
|ENSMUSG00000051951|Xkr4       |X-linked Kx blood group related 4 [Source:MGI Symbol%3BAcc:MGI:3528744]

gffからgeneの行を抽出（ncRNA_geneなどと区別する）

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/^gene/{print}'|awk -F"\t" '{print $NF}'|head -1
```
出力
```
ID=gene:ENSMUSG00000102693;Name=4933401J01Rik;biotype=TEC;description=RIKEN cDNA 4933401J01 gene [Source:MGI Symbol%3BAcc:MGI:1918292];gene_id=ENSMUSG00000102693;logic_name=havana_mus_musculus;version=2
```

`;`で列を分割、`gene_id=`, `Name=`,`description=`の列を抽出

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/^gene/{print}'|awk -F"\t" '{print $NF}'|awk -F";" '{print $5"="$2"="$4}'|head -1
```
出力
```
gene_id=ENSMUSG00000102693=Name=4933401J01Rik=description=RIKEN cDNA 4933401J01 gene [Source:MGI Symbol%3BAcc:MGI:1918292]
```

余分な列をのぞく

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/^gene/{print}'|awk -F"\t" '{print $NF}'|awk -F";" '{print $5"="$2"="$4}'|awk -F"=" '{print $2"\t"$4"\t"$6}'|head -1
```
出力
```
ENSMUSG00000102693	4933401J01Rik	RIKEN cDNA 4933401J01 gene [Source:MGI Symbol%3BAcc:MGI:1918292]
```

`gene_id`（1列目）でsortして完成

```sh
more Mus_musculus.GRCm39.108.gff3|awk '$3~/^gene/{print}'|awk -F"\t" '{print $NF}'|awk -F";" '{print $5"="$2"="$4}'|awk -F"=" '{print $2"\t"$4"\t"$6}' |sort -k 1,1 > description.tsv
```

エントリの数

```sh
wc -l description.tsv
```
出力
```
25694 description.tsv
```

## 合体させる
2022-11-30

`transcription_name`列は除く

|transcript_id | gene_id| gene name | description |
|--------------|--------|-----------|-------------|
|ENSMUST00000070533.5 | ENSMUSG00000051951|Xkr4 |X-linked Kx blood group related 4 [Source:MGI Symbol%3BAcc:MGI:3528744]

`join`コマンドでタブ区切りを使う場合は　`-t "(タブキーを押す)"` または　`-t "$(printf '\011')"` とする

```sh
join -t "$(printf '\011')" -1 3 -2 1 -a 1 transcript_name.tsv description.tsv |head -1
```
出力
```
ENSMUSG00000000001	ENSMUST00000000001.5	Gnai3-201	Gnai3	guanine nucleotide binding protein (G protein)%2C alpha inhibiting 3 [Source:MGI Symbol%3BAcc:MGI:95773]
```

keyとした`gene_id`列が先頭に来ているので、`transcript_id`列を1列目にして、`transcript_name`列は削除

```sh
join -t "$(printf '\011')" -1 3 -2 1 -a 1 transcript_name.tsv description.tsv |awk -F"\t" '{print $2"\t"$1"\t"$4"\t"$5}'|head -1
```
出力
```
ENSMUST00000000001.5	ENSMUSG00000000001	Gnai3	guanine nucleotide binding protein (G protein)%2C alpha inhibiting 3 [Source:MGI Symbol%3BAcc:MGI:95773]
```

`transcript_id`列で`sort`、URLエンコード文字ををデコードして完成

```sh
join -t "$(printf '\011')" -1 3 -2 1 -a 1 transcript_name.tsv description.tsv |awk -F"\t" '{print $2"\t"$1"\t"$4"\t"$5}'|sort -k 1,1 |sed 's/%3B/;/g'|sed 's/%2C/,/g'> annotation.tsv
```

エントリの数

```sh
wc -l annotation.tsv
```
出力
```
66511 annotation.tsv
```

