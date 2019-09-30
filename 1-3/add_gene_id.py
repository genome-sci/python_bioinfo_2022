import sys
from BCBio import GFF

# BCBio.GFF is required. 
# Install it by "pip install bcbio-gff"
# usage
# python add_gene_id.py input.gff output.gff

file_name = sys.argv[1]
out_file_name = sys.argv[2]

records = list(GFF.parse(open(file_name)))

gene_cnt = 0
for r in records:
    for f in r.features:
        if f.type == "gene" or f.type == "pseudogene":
            gene_cnt += 1
            gene_id = "gene_" + str(gene_cnt).zfill(4)
            f.qualifiers["gene_id"] = [gene_id]
            for sf in f.sub_features:
                sf.qualifiers["gene_id"] = [gene_id]
                for ssf in sf.sub_features:
                    ssf.qualifiers["gene_id"] = [gene_id]

with open(out_file_name, "w") as fh:
    GFF.write(records, fh)
