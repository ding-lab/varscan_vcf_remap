# DNP Filter CWL Tool

Simple CWL wrapper for DNP filter for use with TinDaisy.

The algorithm mainly includes three steps:
- Search all the two adjacent SNPs in the VCF file
- Validate if the two adjacent SNPs are from the same molecule using the BAM file
- Merge the two adjacent SNP calls to one DNP call in the VCF file

For development and testing purposes, this project ships with test data and
demonstration scripts for running directly (in docker container), by calling
docker image, and by calling CWL tool. See ./testing for details.

Docker image: dinglab2/dnp\_filter:20190905

Contact: Matt Wyczalkowski (m.wyczalkowski@wustl.edu), Houxiang Zhu (houxiang.zhu@wustl.edu)
