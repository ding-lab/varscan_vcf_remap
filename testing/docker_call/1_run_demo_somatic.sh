source ../../docker/docker_image.sh

function launch_varscan_vcf_remap {

    VCF_C=$1
    OUT_C=$2

    # This is what we want to run in docker
    CMD_INNER="/bin/bash /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh $VCF_C $OUT_C"

    #
    # Launch stuff, keep as is
    #
    SYSTEM=docker   # docker MGI or compute1
    START_DOCKERD="../../docker/WUDocker"  # https://github.com/ding-lab/WUDocker.git

    VOLUME_MAPPING="$DATA_H:/data $OUTD_H:/results"

    >&2 echo Launching $IMAGE on $SYSTEM
    CMD_OUTER="bash $START_DOCKERD/start_docker.sh -I $IMAGE -M $SYSTEM -c \"$CMD_INNER\" $VOLUME_MAPPING "
    echo Running: $CMD_OUTER
    eval $CMD_OUTER

    >&2 echo Written to $OUT_C 

}

# this should be read-only.  Maps to /data
# katmai - for somatic call
DATA_H="/home/mwyczalk_test/Projects/TinDaisy/testing/C3L-00908-data/dat"
# ./results will map to /results
OUTD_H="./results"
mkdir -p $OUTD_H

VCF_INDEL_C="/data/call-parse_varscan_indel/execution/results/varscan/filter_indel_out/varscan.out.som_indel.Somatic.hc.vcf"
VCF_SNV_C="/data/call-parse_varscan_snv/execution/results/varscan/filter_snv_out/varscan.out.som_snv.Somatic.hc.somfilter_pass.vcf"

OUT_INDEL="/results/varscan.indel.vcf-remapped.vcf"  
OUT_SNV="/results/varscan.snv.vcf-remapped.vcf"

launch_varscan_vcf_remap $VCF_INDEL_C $OUT_INDEL
launch_varscan_vcf_remap $VCF_SNV_C $OUT_SNV




