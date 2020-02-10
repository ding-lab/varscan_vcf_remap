# Create YAML file by replacing string DAT in template with passed value
# Usage:
#   bash make_yaml.sh TEMPLATE DAT

# Usage is same as make_config.sh


if [ "$#" -ne 2 ]; then
    >&2 echo Error: Wrong number of arguments
    exit 1
fi

TEMPLATE=$1
DAT=$2

if [ ! -e $TEMPLATE ]; then
    >&2 echo ERROR: $TEMPLATE does not exist
    exit 1
fi

if [ ! -e $DAT ]; then
    >&2 echo ERROR: $DAT does not exist
    exit 1
fi

# This is printed to STDOUT
sed "s|DAT|$DAT|g" $TEMPLATE 
