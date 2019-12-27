# Example command to run within docker.  Typically, start docker first with 0_start_docker.sh

VCF="/data/varscan_snv_vcf.vcf"
mkdir -p /data/out
OUT="/data/out/varscan_snv_vcf-remapped.vcf"

python /opt/varscan_vcf_remap/src/varscan_vcf_remap.py $@ --input $VCF --output $OUT

echo Written to $OUT
