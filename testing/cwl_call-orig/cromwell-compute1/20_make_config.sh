# Generate cromwell config file

CONFIG_TEMPLATE="config/cromwell-config-db.template.dat"


# local storage, for testing only
#WORKFLOW_ROOT="/home/m.wyczalkowski/Projects/dat/cromwell-data"

# write to /storage1
#WORKFLOW_ROOT="/storage1/fs1/m.wyczalkowski/Active/cromwell-data"

# write to /scratch1
WORKFLOW_ROOT="/scratch1/fs1/lding/cromwell-data"
CONFIG_FILE="dat/cromwell-config-db.dat"

>&2 echo Writing Cromwell config file to $CONFIG_FILE

mkdir -p $(dirname $CONFIG_FILE)
src/make_config.sh $CONFIG_TEMPLATE $WORKFLOW_ROOT > $CONFIG_FILE
