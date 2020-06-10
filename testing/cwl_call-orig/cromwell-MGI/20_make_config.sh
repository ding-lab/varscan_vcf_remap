# Generate cromwell config file

CONFIG_TEMPLATE="../cromwell.resources/cromwell-config-db.MGI.template.dat"

WORKFLOW_ROOT="/gscmnt/gc2541/cptac3_analysis"
CONFIG_FILE="dat/cromwell-config-db.dat"

>&2 echo Writing Cromwell config file to $CONFIG_FILE

mkdir -p $(dirname $CONFIG_FILE)
../cromwell.resources/make_config.sh $CONFIG_TEMPLATE $WORKFLOW_ROOT > $CONFIG_FILE
