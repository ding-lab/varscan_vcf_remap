FROM python:3

WORKDIR /opt

# newer versions of pysam seem to crash on build.
# alternative is to start with Bioconductor images, e.g., https://quay.io/repository/biocontainers/pysam?tab=info
RUN pip install PyVCF argparse pysam==0.15.1
#RUN pip install argparse
#pip install Cython
#RUN pip install pysam
#pip install pysam==0.15.1

RUN apt-get update && apt-get install -y \
    vim

COPY . /opt/varscan_vcf_remap
