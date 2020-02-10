IMAGE="mwyczalkowski/varscan_vcf_remap:20200210"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
