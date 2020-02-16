# Example command to run within docker.  Typically, start docker first with 0_start_docker.sh

VCF="/data/Varscan.indel.Final.vcf.gz"
OUT="/data/foo/varscan.indel.vcf-remapped.vcf"

bash /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh $VCF $OUT

echo Written to $OUT

VCF="/data/Varscan.snp.Final.vcf.gz"
OUT="/data/foo/varscan.snp.vcf-remapped.vcf"

bash /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh $VCF $OUT

echo Written to $OUT
