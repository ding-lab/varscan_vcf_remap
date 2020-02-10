# NOTE: on compute1 this appears to map ./* to docker container, so to retain home directory for e.g. development,
# run this from home directory
# Note that we are not able to mount /scratch1/fs1/lding as /scratch

echo Reminder: please invoke the following prior to starting docker
echo "     export LSF_DOCKER_NETWORK=host"

echo Current working directory:
pwd
cd

# was 32
mem=8
SELECT="select[mem>$(( mem * 1000 ))] rusage[mem=$(( mem * 1000 ))]";
QUEUE="general-interactive"
IMAGE="docker(mwyczalkowski/cromwell-runner)"


# Important: LSF_DOCKER_VOLUMES must map to same path if calling bsub within bsub (which is what we do)
#export LSF_DOCKER_VOLUMES="/storage1/fs1/m.wyczalkowski:/data /scratch1/fs1/lding:/scratch"
export LSF_DOCKER_VOLUMES="/storage1/fs1/m.wyczalkowski:/storage1/fs1/m.wyczalkowski /scratch1/fs1/lding:/scratch1/fs1/lding"
bsub -Is -M $(( $mem * 1000 )) -R "$SELECT" -q $QUEUE -a "$IMAGE" /bin/bash -l
