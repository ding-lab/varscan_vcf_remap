# MNP Filter CWL Tool

Simple CWL wrapper for MNP filter for use with TinDaisy.

The algorithm mainly includes three steps (here we call DNP, TNP, or ONP as MNP):
1. Search all the multiple adjacent SNPs in the VCF file
        - Scan all the SNPs with one base of ref and alt
        - Compare the chromsome and positon information of each SNP to make sure they are adjacent
        - Output all the multiple adjacent SNPs to a list
2. Validate if the multiple adjacent SNPs are from the same molecule using the tumor BAM file
        - Use pysam to fetch all the reads in the bam file covering the positions of all the multiple adjacent SNPs
        - Exclue the reads only covering partially
        - Count the numbers for different base compositions of the region
        - If the number of reads supporting MNP is greater than the number of reads not supporting MNP, we count it as a MNP
        - Output the MNP info to a tuple
3. Combine the multiple adjacent SNP calls to one MNP call in the VCF file
        - Open the initial VCF file for reading
        - Open an output VCF file for writing
        - Adding the MNP filter information to the headers of the output VCF file
        - Combine the validated adjacent SNPs to one MNP call in the output VCF file. Specifically, for CHROM, POS, ID, QUAL, FILTER, FORMAT, NORMAL, and TUMOR fields, we use the information of the first SNP. For REF and ALT fields, we just combine the bases of the adjacent SNPs, respecitively. The INFO field taken from the first SNP with the following changes: (1) List all the set values of the SNPs; (2) Add the value “DNP”, "TNP" or "ONP" to indicate it consists of multiple merged SNPs

For development and testing purposes, this project ships with test data and
demonstration scripts for running directly (in docker container), by calling
docker image, and by calling CWL tool. See ./testing for details.

Docker image: dinglab2/dnp\_filter:20190916

Contact: Matt Wyczalkowski (m.wyczalkowski@wustl.edu), Houxiang Zhu (houxiang.zhu@wustl.edu)
