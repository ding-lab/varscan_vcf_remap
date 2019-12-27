IMAGE="mwyczalkowski/varscan_vcf_remap:20191227"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
