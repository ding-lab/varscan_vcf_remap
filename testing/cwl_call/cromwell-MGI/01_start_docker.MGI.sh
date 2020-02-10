# Launch docker environment at MGI before running cromwell.
# command based on CromwellRunner/docker/start_docker.MGI.sh
#   from https://github.com/ding-lab/CromwellRunner
mem=8

SELECT="select[mem>$(( mem * 1000 ))] rusage[mem=$(( mem * 1000 ))]";
QUEUE="research-hpc"
IMAGE="mwyczalkowski/cromwell-runner"

CMD="bsub -Is -M $(( $mem * 1000000 )) -R \"$SELECT\" -q $QUEUE -a \"docker($IMAGE)\" /bin/bash -l"
>&2 echo Running: $CMD
eval $CMD
