# RNA-seqカウントデータ作成手順

- トリミングとフィルタリング: fastp v0.23.2
- リードカウント: kallisto v0.48.0
- リファレンス配列: Ensembl(release 108) GRCm39 http://asia.ensembl.org/Mus_musculus/Info/Index
からcDNA配列 Mus_musculus.GRCm39.cdna.all.faを入手

## index作成

```
% kallisto index -i GRCm39_kallisto_index Mus_musculus.GRCm39.cdna.all.fa
```

## RNA-seqデータセット取得
2022-11-28

Impaired KDM2B-mediated PRC1 recruitment to chromatin causes defective neural stem cell self-renewal and ASD/ID-like behaviors [RNA-Seq]<br>
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190806

BioProject	PRJNA788503 <br>
SRA	SRP350646; SRR17223720-SRR17223725 <br>
SRR17223720-2 Neural progenitor cells(C57BL/6J由来), wild-type <br>
SRR17223723-5 Neural progenitor cells(C57BL/6J由来), Kdm2b one allele mutant <br>

SRA Run selector
https://www.ncbi.nlm.nih.gov/Traces/study/?acc=PRJNA788503&o=acc_s%3Aa

Data accessタブから、AWSのリンクを取得

```sh
wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR17223720/SRR17223720
wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR17223721/SRR17223721
wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR17223722/SRR17223722
wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR17223723/SRR17223723
wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR17223724/SRR17223724
wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR17223725/SRR17223725
```

Accessionリスト　`SRR_Acc_List.txt` も上記ページから取得する

ダウンロードした `SRRxxxxxxxx` に拡張子.sraをつける（または./SRRxxxxxxxxでファイル指定しないとwebに読みに行ってしまう）

```sh
% ./fq_dump.sh >fq_dump.sh.log 2>&1 &
```

トリミングとフィルタリング `trimming.sh`

```sh
#!/bin/sh

SEQLIBS=(SRR17223720 SRR17223721 SRR17223722 SRR17223723 SRR17223724 SRR17223725)

for seqlib in ${SEQLIBS[@]}; do
    fastp --cut_front --cut_tail \
          -i ${seqlib}.fastq.gz\
          -o ${seqlib}.trimmed.fastq.gz\
          -h ${seqlib}_report.html -j ${seqlib}_report.json
done
```

実行

```sh
chmod +x trimming.sh
./trimming.sh >trimming.sh.log 2>&1 &
```

kallistoによるリードカウント `run_kallisto.sh`

SRAのメタデータでは平均フラグメント長 165, sd 92.8だったのでkallistoのオプションを調整

```sh
#!/bin/sh

SEQLIBS=(SRR17223720 SRR17223721 SRR17223722 SRR17223723 SRR17223724 SRR17223725)

for seqlib in ${SEQLIBS[@]}; do
  result_dir=${seqlib}_exp_kallisto
  kallisto quant -i GRCm39_kallisto_index \
                 -o ${result_dir} \
                 --single -l 165 -s 92.8 -b 100 \
                 ${seqlib}.trimmed.fastq.gz
done
```

実行

```sh
chmod +x run_kallisto.sh
./run_kallisto.sh >run_kallisto.sh.log 2>&1 &
```

effective_lengthとestimate_countでTPMを算出するため、まとめて`estimate_count`と`tpm`を残す

## 参考
- 次世代シーケンサーデータの解析手法 第15回 RNA-seq 解析(その3) https://www.iu.a.u-tokyo.ac.jp/~kadota/JSLAB_15_kadota.pdf
- kallisto を用いた A. thaliana paired-end リードの転写産物の定量 https://bi.biopapyrus.jp/rnaseq/mapping/kallisto/kallisto-paired.html
- Quasi-Mappingによって高速にRNA seqの定量を行う Kallisto https://kazumaxneo.hatenablog.com/entry/2018/07/14/180503
- kallisto Manual http://pachterlab.github.io/kallisto/manual.html

