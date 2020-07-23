# Example command to run within docker.  Typically, start docker first with 0_start_docker.sh

OUTD="./results"
mkdir -p $OUTD

VCF="/data/call-parse_varscan_indel/execution/results/varscan/filter_indel_out/varscan.out.som_indel.Somatic.hc.vcf"
OUT="$OUTD/varscan.indel.vcf-remapped.vcf"
CMD="bash /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh $VCF $OUT $ARG"
>&2 echo Running: $CMD
eval $CMD

VCF="/data/call-parse_varscan_snv/execution/results/varscan/filter_snv_out/varscan.out.som_snv.Somatic.hc.somfilter_pass.vcf"
OUT="$OUTD/varscan.snp.vcf-remapped.vcf"
CMD="bash /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh $VCF $OUT $ARG"

>&2 echo Running: $CMD
eval $CMD
