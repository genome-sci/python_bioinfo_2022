import gzip
import urllib.parse
from BCBio import GFF

# Download gff file by `curl -O https://ftp.ensembl.org/pub/release-108/gff3/mus_musculus/Mus_musculus.GRCm39.108.gff3.gz`
gff_file_name = "Mus_musculus.GRCm39.108.gff3.gz"

for record in GFF.parse(gzip.open(gff_file_name, "rt")):
    for f in record.features:
        if f.type == "gene":
            gene_id = f.qualifiers["ID"][0].replace("gene:", "")
            # Name と description 属性を持たない場合があるので get を使って値を取得する。
            gene_name = f.qualifiers.get("Name", ["NO_NAME"])[0]
            description = urllib.parse.unquote(f.qualifiers.get("description", ["-"])[0])
            for sf in f.sub_features:
                if sf.type == "mRNA":
                    transcript_id = sf.qualifiers["ID"][0].replace("transcript:", "")
                    version = sf.qualifiers["version"][0]
                    print("\t".join([transcript_id + "." + version, gene_id, gene_name, description]))
