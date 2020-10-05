# start docker image with ../demo_data mapped to /data,
# unless another path is passed on command line.  uses
# the start_docker.sh script in /docker

source ../../docker/docker_image.sh

# katmai - for somatic call
DATA_ROOT="/home/mwyczalk_test/Projects/TinDaisy/testing/C3L-00908-data/dat"


# MGI
# Mounting cromwell-executions
#CE_ROOT="/gscmnt/gc2541/cptac3_analysis/cromwell-workdir/cromwell-executions"
#MOUNT="$CE_ROOT:/cromwell-executions"

# below on MGI for germline calls

#DATA_ROOT="/gscmnt/gc2508/dinglab/mwyczalk/GermlineCaller.Testing/C3L-00001"
#VEP_ROOT="/gscmnt/gc7202/dinglab/common/databases/VEP"
#REF_ROOT="/gscmnt/gc7202/dinglab/common/Reference/A_Reference"
#ARGS="-M MGI -P"

MOUNT="$DATA_ROOT:/data"

cd ../.. && bash docker/WUDocker/start_docker.sh $ARGS $@ -I $IMAGE $MOUNT

