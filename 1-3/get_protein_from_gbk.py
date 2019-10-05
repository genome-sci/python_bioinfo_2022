# GenBankファイルからCDS配列を取得するスクリプト

import sys
import os
from Bio import SeqIO

gbk_file_name = sys.argv[1]
if not os.path.exists(gbk_file_name):
    sys.stderr.write(f"File not found. [{gbk_file_nam}]\n")
    exit(1)

for record in SeqIO.parse(gbk_file_name, "genbank"):
    for feature in record.features:
        if feature.type != "CDS":
            continue  # CDS以外のfeatureでは処理をスキップする
        if "pseudo" in feature.qualifiers:
            continue  # "pseudo"クオリファイアが存在する場合処理をskip
        sequence = feature.location.extract(record.seq)
        aa = sequence.translate(cds=True)
        locus_tag = feature.qualifiers.get("locus_tag", ["undefined"])[0]
        product = feature.qualifiers.get("product", ["unknown protein"])[0]       
        print(f">{locus_tag} {product}")
        print(aa)