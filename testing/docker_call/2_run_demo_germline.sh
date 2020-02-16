source ../../docker/docker_image.sh
DATD="/home/mwyczalk_test/Projects/GermlineCaller/C3L-00001"

# Using python to get absolute path of DATD.  On Linux `readlink -f` works, but on Mac this is not always available
# see https://stackoverflow.com/questions/1055671/how-can-i-get-the-behavior-of-gnus-readlink-f-on-a-mac
ADATD=$(python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' $DATD)

VCF="/data/Varscan.indel.Final.vcf.gz"
OUT="/data/out/Varscan.indel.Final-remapped.vcf"

#CMD="python /opt/varscan_vcf_remap/src/varscan_vcf_remap.py --input $VCF --output $OUT"
CMD="/bin/bash /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh $VCF $OUT --germline"

docker run -v $ADATD:/data -it $IMAGE $CMD

