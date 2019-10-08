import sys
from Bio import SeqIO

# 指定長さ未満の配列を除いた後、
# Usage
# python fasta_length_filter.py input.fasta threshold > output.fasta
# example
# python fasta_length_filter.py ../common/s288c.protein.faa 1000 > output.fasta

fasta_file = sys.argv[1]
threshold = int(sys.argv[2])

records = list(SeqIO.parse(fasta_file, "fasta")) 

# 指定長さ未満の配列を除く
records = [r for r in records if len(r)<threshold]
# recordsを降順にソートする
records = sorted(records, key=len, reverse=True)

for r in records:
    print(r.format("fasta"), end="")  # 最後の改行は不要なのでend=""を指定している。
