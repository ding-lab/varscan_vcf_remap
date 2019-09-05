import vcf
import re
import argparse
import pysam
import sys

def search_2_snp(vcf_file):
    vcf_reader = vcf.Reader(open(vcf_file, 'r'))
    chrom_pre = pos_pre = ref_pre = alt_pre = ""
    snps_list = list()
    for record in vcf_reader: #for loop each line in the VCF file excluding headers
        if re.fullmatch("[ATCG]", str(record.REF)) and re.fullmatch("\[[ATCG]\]", str(record.ALT)): #check if both ref and alt is one base
            if record.CHROM == chrom_pre and record.POS == pos_pre + 1: #check if the two snps are adjacent
                alt_pre_base = re.fullmatch("\[([ATCG])\]", str(alt_pre)).group(1)
                alt_base = re.fullmatch("\[([ATCG])\]", str(record.ALT)).group(1)
                two_snps = (chrom_pre, pos_pre, ref_pre, alt_pre_base, record.CHROM, record.POS, record.REF, alt_base)
                snps_list.append(two_snps)
                print("{} are two adjacent SNPs found from the input VCF file {}.".format(two_snps, vcf_file), file=sys.stderr)
                chrom_pre, pos_pre, ref_pre, alt_pre = record.CHROM, record.POS, record.REF, record.ALT
            else:
                chrom_pre, pos_pre, ref_pre, alt_pre = record.CHROM, record.POS, record.REF, record.ALT
    return snps_list

def validate_2_snp(bam_file, chrom, snp1_pos, snp1_ref, snp1_alt, snp2_pos, snp2_ref, snp2_alt, threshold_value):
    samfile = pysam.AlignmentFile(bam_file, "rb")
    forward_NN = forward_NM = forward_MN = forward_MM = forward_OT = reverse_NN = reverse_NM = reverse_MN = reverse_MM = reverse_OT = 0
    iter = samfile.fetch(chrom, snp1_pos-1, snp2_pos) #fechch all the reads in the bam file covering the chrom and two adjacent positions
    for x in iter:
        if x.reference_end == snp1_pos or x.reference_start + 1 == snp2_pos: #exclude the reads only cover one position at the end or at the beginning
            pass
        else:
            query_sequence = x.query_sequence
            aligned_pairs = x.get_aligned_pairs(matches_only=False, with_seq=False)
            read_index1 = read_index2 = 0;
            for t in aligned_pairs:
                if (t[1] == snp1_pos - 1):
                    read_index1 = t[0]
                if (t[1] == snp2_pos - 1):
                    read_index2 = t[0]
            if x.is_reverse: #check if the read is in the reverse strand
                if read_index1 != "None" and read_index2 != "None":
                    two_bases = query_sequence[read_index1] + query_sequence[read_index2]
                    if two_bases == snp1_ref + snp2_ref:
                        reverse_NN = reverse_NN + 1
                    elif two_bases == snp1_ref + snp2_alt:
                        reverse_NM = reverse_NM + 1
                    elif two_bases == snp1_alt + snp2_ref:
                        reverse_MN = reverse_MN + 1
                    elif two_bases == snp1_alt + snp2_alt:
                        reverse_MM = reverse_MM + 1
                    else:
                        reverse_OT = reverse_OT + 1
                else:
                    reverse_OT = reverse_OT + 1
            else:
                if read_index1 != "None" and read_index2 != "None":
                    two_bases = query_sequence[read_index1] + query_sequence[read_index2]
                    if two_bases == snp1_ref + snp2_ref:
                        forward_NN = forward_NN + 1
                    elif two_bases == snp1_ref + snp2_alt:
                        forward_NM = forward_NM + 1
                    elif two_bases == snp1_alt + snp2_ref:
                        forward_MN = forward_MN + 1
                    elif two_bases == snp1_alt + snp2_alt:
                        forward_MM = forward_MM + 1
                    else:
                        forward_OT = forward_OT + 1
                else:
                    forward_OT = forward_OT + 1
    dnp_read_num = forward_NN + forward_MM + reverse_NN + reverse_MM
    total_read_num = forward_NN + forward_NM + forward_MN + forward_MM + forward_OT + reverse_NN + reverse_NM + reverse_MN + reverse_MM + reverse_OT
    if total_read_num != 0 and dnp_read_num/total_read_num > threshold_value:
        dnp = (chrom, snp1_pos, snp2_pos)
        print("{} passed the DNP threshold: {} with supported DNP reads number: {} and total reads number: {}.".format(dnp, threshold_value, dnp_read_num, total_read_num), file=sys.stderr)
        return dnp
    else:
        dnp = (chrom, snp1_pos, snp2_pos)
        print("{} did not pass the DNP threshold: {} with supported DNP reads number: {} and total reads number: {}.".format(dnp, threshold_value, dnp_read_num, total_read_num), file=sys.stderr)
        return

def is_snp1(dnp_list, chrom, pos):
    if len(dnp_list) == 0:
        return False
    else:
        flag = ""
        for dnps in dnp_list:
            if str(chrom) == str(dnps[0]) and int(pos) == int(dnps[1]):
                flag = "snp1"
                break
            else:
                flag = "not_snp1"
        if flag == "snp1":
            return True
        else:
            return False

 
def is_snp2(dnp_list, chrom, pos):
    if len(dnp_list) == 0:
        return False
    else: 
        flag = ""  
        for dnps in dnp_list:
            if str(chrom) == str(dnps[0]) and int(pos) == int(dnps[2]):
                flag = "snp2"
                break
            else:
                flag = "not_snp2"
        if flag == "snp2":
            return True
        else:
            return False           

def combine_2_snp(dnp_list, vcf_file, output_file, threshold_value):
    snp1_chrom = snp1_pos = snp1_id = snp1_ref = snp1_alt = snp1_qual = snp1_filter = snp1_info = snp2_ref = snp2_alt = snp2_set_value = ""
    with open(vcf_file, 'r', encoding = 'utf-8') as vcf_file:
        vcf_content = vcf_file.readlines()
    with open(output_file, 'w', encoding = 'utf-8') as combined_vcf_file:
        for line in vcf_content:
            if re.match("#", line):
                if re.match("##INFO=<ID=DB", line):
                    combined_vcf_file.write(line)
                    DNP_INFO_header = "##INFO=<ID=DNP,Number=0,Type=Flag,Description=\"Validated DNP\">"
                    combined_vcf_file.write(DNP_INFO_header + "\n")
                elif re.match("##FILTER=<ID=LowDepth", line):
                    DNP_FILTER_header = "##FILTER=<ID=DNP,Description=\"Combine 2 SNPs to 1 DNP if greater than the threshold {}\">".format(threshold_value)
                    combined_vcf_file.write(DNP_FILTER_header + "\n")
                    combined_vcf_file.write(line)

                else:
                    combined_vcf_file.write(line)
            else:
                line = line.rstrip()
                snp_info = re.split("\t", line)
                if is_snp1(dnp_list, snp_info[0], snp_info[1]):
                    snp1_chrom, snp1_pos, snp1_id, snp1_ref, snp1_alt, snp1_qual, snp1_filter, snp1_info = snp_info[0], snp_info[1], snp_info[2], snp_info[3], snp_info[4], snp_info[5], snp_info[6], snp_info[7]
                elif is_snp2(dnp_list, snp_info[0], snp_info[1]):
                    snp2_ref, snp2_alt = snp_info[3], snp_info[4]
                    snp2_info_list = re.split(";", snp_info[7])
                    snp2_set = snp2_info_list[-1]
                    snp2_set_list = re.split("=", snp2_set)
                    snp2_set_value = snp2_set_list[-1]
                    dnp_line = snp1_chrom + "\t" + snp1_pos + "\t" + snp1_id + "\t" + snp1_ref + snp2_ref + "\t" + snp1_alt + snp2_alt + "\t" + snp1_qual + "\t" + snp1_filter + "\t" + snp1_info + "," + snp2_set_value + ";" + "DNP" + "\t" + "." + "\t" + "." + "\t" + "." + "\n"
                    combined_vcf_file.write(dnp_line)
                    snp1_chrom = snp1_pos = snp1_id = snp1_ref = snp1_alt = snp1_qual = snp1_filter = snp1_info = snp2_ref = snp2_alt = snp2_set_value = ""
                else:
                    combined_vcf_file.write(line + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect DNP from a vcf file")
    parser.add_argument("-i", "--input", type=str, dest="vcf_file", help="input vcf file name")
    parser.add_argument("-b", "--bam", type=str, dest="bam_file", help="input bam file name")
    parser.add_argument("-t", "--threshold", type=float, dest="threshold_value", default=0.5, help="set threshold value for validating DNP")
    parser.add_argument("-o", "--output", type=str, dest="output_file", help="output file name")
    args = parser.parse_args()

    snps_list = search_2_snp(args.vcf_file)

    if len(snps_list) == 0:
        combine_2_snp([], args.vcf_file, args.output_file, args.threshold_value)
        print("There is no two adjacent SNPs in the input VCF file {}.\nNo DNP combination was did, but DNP INFO and FILTER headers were added to the output file: {}".format(args.vcf_file, args.output_file), file=sys.stderr)

    else:
        dnps_list = list()
        for element in snps_list:
            dnp = validate_2_snp(args.bam_file, element[0], int(element[1]), element[2], element[3], int(element[5]), element[6], element[7], args.threshold_value)
            if dnp != None:
                dnps_list.append(dnp)
        if len(dnps_list) == 0:      
            combine_2_snp([], args.vcf_file, args.output_file, args.threshold_value)
            print("No DNP combination was did, but DNP INFO and FILTER headers were added to the output file: {}".format(args.output_file), file=sys.stderr)
        else:
            combine_2_snp(dnps_list, args.vcf_file, args.output_file, args.threshold_value)
            print("Passed two adjacent SNPs are combined to DNPs, and DNP INFO and FILTER headers were added to the output file: {}".format(args.output_file), file=sys.stderr)
