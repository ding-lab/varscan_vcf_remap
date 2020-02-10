# Example command to run within docker.  Typically, start docker first with 0_start_docker.sh

VCF="/data/varscan_snv_vcf.vcf"
OUT="/data/foo/varscan_snv_vcf-remapped.vcf"

bash /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh $VCF $OUT

echo Written to $OUT
