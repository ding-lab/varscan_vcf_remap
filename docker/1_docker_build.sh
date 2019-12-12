IMAGE="dinglab2/mnp_filter:20191211"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
