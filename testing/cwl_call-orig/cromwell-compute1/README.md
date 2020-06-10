# Testing on compute1

Based on part on TinDaisy testing on compute1 here: /home/m.wyczalkowski/Projects/TinDaisy/TinDaisy/demo/MutectDemo/compute1-dev
Successful run 1/23/20

## Overview

Test cromwell functionality on WU RIS compute1 system with cromwell output to either /storage1 or /scratch1,
along with subsequent queries to Cromwel database to get run status.  Note that we are launching cromwell
from within a docker container, to simulate environment used for [CromwellRunner](https://github.com/ding-lab/CromwellRunner)

## Getting started

To run demo dataset, first uncompress reference located in `../../demo_data`:
```
tar -xvjf Homo_sapiens_assembly19.COST16011_region.fa.tar.bz2
```

Testing of runs proceeds sequentially through a series of numbered scripts.
* `00_set_LSF_DOCKER_NETWORK.sh` - reminder to set environment variables
* `01_start_docker.compute1.sh` - Mounts volumes and launches mwyczalkowski/cromwell-runner docker image
* `05_start_server.sh` - starts local instance of cromwell database server.  This is currently requires for database queries
* `20_make_config.sh` - creates configuration file. `WORKFLOW_ROOT` is defined here, which determines where cromwell output goes
* `30_start_run.sh` - Launches `GATK_GermlineCaller` workflow on test dataset, run as one whole region
* `35_start_run_parallel.sh` - Launches `GATK_GermlineCaller` workflow on test dataset, but uses `chrlist.dat` to break
  genome into 4 pieces, run each one individually, then merge into one result.  Finalize run upon completion by compressing
  intermediate results

## Cromwell database queries

We can use cromwell database to query status of runs.  This is basis for a lot
of [CromwellRunner](https://github.com/ding-lab/CromwellRunner) functionality.
Provided that we are running a local instance of cromwell database server, basic 
query looks like,
```
WID="d1534412-a8b4-4c01-87d5-a4704aa51442"
curl -k -s -X GET http://localhost:8000/api/workflows/v1/$WID/status -H "accept: application/json"
{"status":"Succeeded","id":"32814174-62c6-410c-81dc-f73898f0ec59"}
```

# Testing of writing to /storage1

Preliminary testing of having `WORKFLOW_ROOT` in /storage1 or /scratch1 led to several lessons learned:
* Must set `export LSF_DOCKER_NETWORK=host` before starting CromwellRunner container
* Must map paths to same path when starting docker container for bsub-within-bsub to work, i.e.,
    `LSF_DOCKER_VOLUMES="/storage1/fs1/m.wyczalkowski:/storage1/fs1/m.wyczalkowski"`
  (as opposed to "/storage1/fs1/m.wyczalkowski:/data")

These requirements are incorporated into the workflow and may eventually go away
