# Example command to run within docker.  Typically, start docker first with 0_start_docker.sh

VCF="/data/merged.filtered_for_test_DNP_TNP_QNP.vcf"
BAM="/data/synthetic.BWA.bam"
OUT="mnp_combined.vcf"

python /opt/mnp_filter/src/mnp_filter.py --input $VCF --bam $BAM --output $OUT

echo Written to $OUT
