cd ../../..
CWL="cwl/varscan_vcf_remap.cwl"
YAML="testing/cwl_call/yaml/demo_germline.yaml"

mkdir -p results
RABIX_ARGS="--basedir testing/results"

rabix $RABIX_ARGS $CWL $YAML
