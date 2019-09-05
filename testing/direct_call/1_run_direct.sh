# Example command to run within docker.  Typically, start docker first with 0_start_docker.sh

VCF="/data/merged.filtered.vcf"
BAM="/data/test.bam"
THRESHOLD=0.5
OUT="DNP_combined.vcf"

python /opt/dnp_filter/src/DNP_filter.py --input $VCF --bam $BAM --threshold $THRESHOLD --output $OUT

echo Written to $OUT
