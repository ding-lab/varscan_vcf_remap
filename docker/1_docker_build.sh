IMAGE="mwyczalkowski/varscan_vcf_remap:germline"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
