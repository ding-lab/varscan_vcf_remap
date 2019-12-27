
# Matthew Wyczalkowski
# m.wyczalkowski@wustl.edu
# Washington University School of Medicine

import vcf
import re
import argparse
import pysam
import sys
import os

def search_multiple_snp(vcf_file):
    vcf_reader = vcf.Reader(open(vcf_file, 'r'))
    chrom_pre = pos_pre = ref_pre = alt_pre = ""
    current_list = list()
    snps_list = list()

    for record in vcf_reader: #for loop each line in the VCF file excluding headers
        if re.fullmatch("[ATCG]", str(record.REF)) and re.fullmatch("\[[ATCG]\]", str(record.ALT)): #check if both ref and alt is one base
            alt_base = re.fullmatch("\[([ATCG])\]", str(record.ALT)).group(1)
            if chrom_pre == "":    #the first SNP record
                current_list.append(record.CHROM)
                current_list.append(record.POS)
                current_list.append(record.REF)
                current_list.append(alt_base)
                chrom_pre, pos_pre, ref_pre, alt_pre = record.CHROM, record.POS, record.REF, alt_base
            else: #the second SNP record and more
                if record.CHROM == chrom_pre and record.POS == pos_pre + 1: #check if the two snps are adjacent
                    current_list.append(record.CHROM)
                    current_list.append(record.POS)
                    current_list.append(record.REF)
                    current_list.append(alt_base)
                    chrom_pre, pos_pre, ref_pre, alt_pre = record.CHROM, record.POS, record.REF, alt_base
                else:
                    if len(current_list) >= 8: # at least two adjacent SNPs
                        snps_list.append(current_list)
                        print(current_list, file=sys.stderr)
                        current_list = []
                        current_list.append(record.CHROM)
                        current_list.append(record.POS)
                        current_list.append(record.REF)
                        current_list.append(alt_base)
                        chrom_pre, pos_pre, ref_pre, alt_pre = record.CHROM, record.POS, record.REF, alt_base
                    else:
                        current_list = []
                        current_list.append(record.CHROM)
                        current_list.append(record.POS)
                        current_list.append(record.REF)
                        current_list.append(alt_base)
                        chrom_pre, pos_pre, ref_pre, alt_pre = record.CHROM, record.POS, record.REF, alt_base   

    if len(current_list) >= 8:
        snps_list.append(current_list)
        print(current_list, file=sys.stderr) 

    return snps_list




def validate_multiple_snp(bam_file, adjacent_snps_list):
    snps_number = len(adjacent_snps_list)/4
    
    chrom = adjacent_snps_list[0]
    pos_list = []
    ref_bases = ""
    alt_bases = ""
    pattern = ""
    i = 0
    while i < snps_number:
        pos_list.append(adjacent_snps_list[1+i*4])
        i += 1
    
    start_pos = pos_list[0]
    end_pos = pos_list[len(pos_list) - 1]

    j = 0
    while j < snps_number:
        ref_bases = ref_bases + adjacent_snps_list[2+j*4]
        j += 1


    k = 0
    while k < snps_number:
        alt_bases = alt_bases + adjacent_snps_list[3+k*4]
        k += 1

    l = 0
    while l < snps_number:
        pattern = pattern + "[" + adjacent_snps_list[2+l*4] + adjacent_snps_list[3+l*4] + "]"
        l += 1    
    #print(pattern)
    ref_bases_number = alt_bases_number = OTHER = 0
    pattern_count_dict = {}

    samfile = pysam.AlignmentFile(bam_file, "rb")
    iter = samfile.fetch(chrom, start_pos-1, end_pos) #fechch all the reads in the bam file covering the chrom and start to end positions. Within pysam, coordinates are 0-based,half-open intervals. i.e., (10000, 20000),the position 10,000 is part of the interval, but 20,000 is not.
    for x in iter:
        if x.reference_end == None:
            pass
        else:
            if x.reference_end < end_pos or x.reference_start + 1 > start_pos: #exclude the reads only cover partially
                pass
            else:
                query_sequence = x.query_sequence
                aligned_pairs = x.get_aligned_pairs(matches_only=False, with_seq=False)
                read_index_list = []

                i = 0
                while i < len(pos_list):
                    for t in aligned_pairs:
                        if t[1] == int(pos_list[i]) - 1:
                            read_index_list.append(t[0])
                    i += 1

                read_index_list_len = len(read_index_list)

                if None not in read_index_list and read_index_list_len == read_index_list[read_index_list_len - 1] - read_index_list[0] + 1:  #remove reads with indel alignment
                    multiple_bases = ""
                    j = 0
                    while j < len(read_index_list):
                        multiple_bases = multiple_bases + query_sequence[read_index_list[j]]
                        j += 1
                    if re.fullmatch(pattern, multiple_bases):
                        if multiple_bases in pattern_count_dict:
                            pattern_count_dict[multiple_bases] = pattern_count_dict[multiple_bases] + 1
                        else:
                            pattern_count_dict[multiple_bases] = 1
                    else:
                        OTHER += 1
                else:
                    OTHER += 1     

    if ref_bases in pattern_count_dict:
        ref_bases_number = pattern_count_dict[ref_bases]
    if alt_bases in pattern_count_dict:
        alt_bases_number = pattern_count_dict[alt_bases]

    total_read_number_alt_ref = 0
    for value in pattern_count_dict.values():
         total_read_number_alt_ref = total_read_number_alt_ref + value
    
    total_read_number = total_read_number_alt_ref + OTHER

    read_support_MNP_number = alt_bases_number
    read_not_support_MNP_number = total_read_number_alt_ref - alt_bases_number - ref_bases_number

    not_support_MNP_dic = pattern_count_dict.copy() #used to print out infos
    if ref_bases in not_support_MNP_dic:
        del not_support_MNP_dic[ref_bases]
    if alt_bases in not_support_MNP_dic:
        del not_support_MNP_dic[alt_bases]
    
    pos_list_length = len(pos_list)
    variant_type = ""
    if pos_list_length == 2:
        variant_type = "DNP"
    elif pos_list_length == 3:
        variant_type = "TNP"
    elif pos_list_length > 3:
        variant_type = "ONP"

    if read_support_MNP_number > read_not_support_MNP_number:
        mnp = (chrom, pos_list)
        print("{} -> Reads: Total = {}, Ref/Alt= {}, Alt Supporting {} = {}, Mixed Ref/Alt {}, Uninformative Ref {} = {}. {}: PASS.".format(mnp, total_read_number, total_read_number_alt_ref, alt_bases, read_support_MNP_number, not_support_MNP_dic, ref_bases, ref_bases_number, variant_type), file=sys.stderr)
        return mnp
    else:
        mnp = (chrom, pos_list)
        print("{} -> Reads: total = {}, Ref/Alt= {}, Alt Supporting {} = {}, Mixed Ref/Alt {}, Uninformative Ref {} = {}. {}: NOT PASS.".format(mnp, total_read_number, total_read_number_alt_ref, alt_bases, read_support_MNP_number, not_support_MNP_dic, ref_bases, ref_bases_number, variant_type), file=sys.stderr)
        return

def is_first_snp(mnp_list, chrom, pos):
    if len(mnp_list) == 0:
        return False
    else:
        flag = ""
        for mnps in mnp_list:
            if str(chrom) == str(mnps[0]) and int(pos) == int(mnps[1][0]):
                #print(type(mnps[1][0]))
                #print(type(pos))
                flag = "first_snp"
                break
            else:
                flag = "not_first_snp"
        if flag == "first_snp":
            return True
        else:
            return False

def is_secondTOend_snp(mnp_list, chrom, pos):
    if len(mnp_list) == 0:
        return False
    else:
        flag = ""
        for mnps in mnp_list:
            if str(chrom) == str(mnps[0]) and int(pos) in mnps[1] and int(pos) != int(mnps[1][0]):  #check pos type and mnps[1] type
                flag = "secondTOend_snp"
                break
            else:
                flag = "not_secondTOend_snp"
        if flag == "secondTOend_snp":
            return True
        else:
            return False
      

def combine_multiple_snp(mnp_list, vcf_file, output_file):
    first_snp_chrom = first_snp_pos = first_snp_id = mnp_ref = mnp_alt = first_snp_qual = first_snp_filter = first_snp_info = first_snp_format = first_snp_normal = first_snp_tumor = set_value = ""
    vcf_file = open(vcf_file, 'r', encoding = 'utf-8') 
    vcf_content = vcf_file.readlines()
    vcf_content_dict = {}
    for lines in vcf_content:
        if re.match("#", lines):
            pass
        else:
            lines = lines.rstrip()
            line_array = re.split("\t", lines)
            #print(line_array[0])
            #print(line_array[1])
            key = line_array[0] + "-" + line_array[1]
            vcf_content_dict[key] = lines
    variant_type_list =[]
    for mnp in mnp_list:
        if len(mnp[1]) == 2:
            variant_type_list.append("DNP")
        elif len(mnp[1]) == 3:
            variant_type_list.append("TNP")
        elif len(mnp[1]) > 3:
            variant_type_list.append("ONP")

    with open(output_file, 'w', encoding = 'utf-8') as combined_vcf_file:
        for line in vcf_content:
            if re.match("#", line):
                if re.match("##INFO=<ID=DP,", line):
                    if "DNP" in variant_type_list:
                        DNP_INFO_header = "##INFO=<ID=DNP,Number=0,Type=Flag,Description=\"Double nucleotide polymorphism -- a substitution in two consecutive nucleotides\">"
                        combined_vcf_file.write(DNP_INFO_header + "\n")
                        combined_vcf_file.write(line)
                    else:
                        combined_vcf_file.write(line)

                elif re.match("##INFO=<ID=TQSI,", line):
                    if "TNP" in variant_type_list:
                        TNP_INFO_header = "##INFO=<ID=TNP,Number=0,Type=Flag,Description=\"Triple nucleotide polymorphism -- a substitution in three consecutive nucleotides\">"
                        combined_vcf_file.write(TNP_INFO_header + "\n")
                        combined_vcf_file.write(line)
                    else:
                        combined_vcf_file.write(line)

                elif re.match("##INFO=<ID=OVERLAP,", line):
                    if "ONP" in variant_type_list:
                        ONP_INFO_header = "##INFO=<ID=ONP,Number=0,Type=Flag,Description=\"Oligo-nucleotide polymorphism -- a substitution in more than three consecutive nucleotides\">"
                        combined_vcf_file.write(ONP_INFO_header + "\n")
                        combined_vcf_file.write(line)
                    else:
                        combined_vcf_file.write(line)

                elif re.match("##FILTER=<ID=PASS,", line):
                    MNP_FILTER_header = "##FILTER=<ID=MNP,Description=\"Combine adjacent SNPs to 1 DNP, TNP, or ONP if the number of reads supporting DNP, TNP, or ONP is greater than the number of reads not supporting\">"
                    combined_vcf_file.write(MNP_FILTER_header + "\n")
                    combined_vcf_file.write(line)

                else:
                    combined_vcf_file.write(line)
            else:
                line = line.rstrip()
                snp_info = re.split("\t", line)

                if is_first_snp(mnp_list, snp_info[0], snp_info[1]):
                    first_snp_chrom, first_snp_pos, first_snp_id, first_snp_qual, first_snp_filter, first_snp_info, first_snp_format, first_snp_normal, first_snp_tumor = snp_info[0], snp_info[1], snp_info[2], snp_info[5], snp_info[6], snp_info[7], snp_info[8], snp_info[9], snp_info[10]
                    for mnps in mnp_list:
                        if str(snp_info[0]) == str(mnps[0]) and int(snp_info[1]) == int(mnps[1][0]):
                            pos_list = mnps[1]
                            length_pos_list = len(pos_list)
                            i = 0 
                            while i < length_pos_list:  # store mnp_refs and mnp_alts
                                position = pos_list[i]
                                process_line = vcf_content_dict[snp_info[0] + "-" + str(position)]
                                process_line_array = re.split("\t", process_line)
                                mnp_ref = mnp_ref + process_line_array[3]
                                mnp_alt = mnp_alt + process_line_array[4]
                                i += 1
                            j = 1
                            while j < length_pos_list: # store set values from the second position
                                position = pos_list[j]
                                process_line = vcf_content_dict[snp_info[0] + "-" + str(position)]
                                process_line_array = re.split("\t", process_line)
                                snp_info_list = re.split(";", process_line_array[7])
                                snp_set = snp_info_list[-1]
                                snp_set_list = re.split("=", snp_set)
                                set_value = set_value + "," + snp_set_list[-1]
                                j += 1
                    mnp_ref_length = len(mnp_ref)
                    variant_type = ""
                    if mnp_ref_length == 2:
                        variant_type = "DNP"
                    elif mnp_ref_length == 3:
                        variant_type = "TNP"
                    elif mnp_ref_length > 3:
                        variant_type = "ONP"
                    mnp_line = first_snp_chrom + "\t" + first_snp_pos + "\t" + first_snp_id + "\t" + mnp_ref + "\t" + mnp_alt + "\t" + first_snp_qual + "\t" + first_snp_filter + "\t" + first_snp_info + set_value + ";" + variant_type + "\t" + first_snp_format + "\t" + first_snp_normal + "\t" + first_snp_tumor + "\n"
                    combined_vcf_file.write(mnp_line)
                    
                    first_snp_chrom = first_snp_pos = first_snp_id = mnp_ref = mnp_alt = first_snp_qual = first_snp_filter = first_snp_info = first_snp_format = first_snp_normal = first_snp_tumor = set_value = ""



                elif not is_first_snp(mnp_list, snp_info[0], snp_info[1]) and is_secondTOend_snp(mnp_list, snp_info[0], snp_info[1]):
                    pass
          
                else:
                    combined_vcf_file.write(line + "\n")                   
    vcf_file.close()                
                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect MNP from a vcf file")
    parser.add_argument("-i", "--input", type=str, dest="vcf_file", help="input vcf file name")
    
    parser.add_argument("-b", "--bam", type=str, dest="bam_file", help="input bam file name")
    #parser.add_argument("-t", "--threshold", type=float, dest="threshold_value", default=0.5, help="set threshold value for validating MNP")
    parser.add_argument("-o", "--output", type=str, dest="output_file", help="output file name")
   
    args = parser.parse_args()

    abs_path_vcf = os.path.abspath(args.vcf_file)
    abs_path_bam = os.path.abspath(args.bam_file)
    abs_path_output = os.path.abspath(args.output_file)
    print("Input VCF: {}".format(abs_path_vcf), file=sys.stderr)
    print("Input BAM: {}".format(abs_path_bam), file=sys.stderr)
    print("Output VCF: {}".format(abs_path_output), file=sys.stderr)
    #print("MNP threshold: {}".format(args.threshold_value), file=sys.stderr)
    print("Adjacent SNPs in the input VCF:", file=sys.stderr)

    snps_list = search_multiple_snp(args.vcf_file)

    #print(snps_list)

    if len(snps_list) == 0:
        combine_multiple_snp([], args.vcf_file, args.output_file)
    else:
        print("Analyzing reads supporting DNP, TNP, or ONP:", file=sys.stderr)
        mnps_list = list()
        for adjacent_snps in snps_list:
            #CHROM, snp1_POS, snp1_REF, snp1_ALT, snp2_POS, snp2_REF, snp2_ALT = element[0], int(element[1]), element[2], element[3], int(element[5]), element[6], element[7] 
            mnp = validate_multiple_snp(args.bam_file, adjacent_snps)
            if mnp != None:
                mnps_list.append(mnp)
            elif mnp == None: # if not MNP
                if len(adjacent_snps) >= 12: # 3 or more adjacent snps
                    window = int(len(adjacent_snps)/4 - 1)
                    while window >= 2:
                        i = 0
                        while i < len(adjacent_snps):
                            if i + window*4 - 1 <= len(adjacent_snps) - 1:
                                start = i
                                stop = i + window*4
                                #print(start,stop)
                                sub_list = adjacent_snps[start:stop]
                                start_stop_list=[]
                                start_stop_list.append(sub_list[1])
                                start_stop_list.append(sub_list[-3])
                                chrom=sub_list[0]
                                flag = "no_overlap"
                                for mnps in mnps_list:
                                    if chrom == mnps[0] and all(positions in mnps[1] for positions in start_stop_list):
                                        flag = "overlap"
                                        break
                                if flag == "no_overlap":
                                    sub_list_mnp = validate_multiple_snp(args.bam_file, sub_list)
                                    if sub_list_mnp != None:
                                        mnps_list.append(sub_list_mnp)
                            i = i + 4    
                        window = window - 1

        if len(mnps_list) == 0:      
            combine_multiple_snp([], args.vcf_file, args.output_file)
        else:
            combine_multiple_snp(mnps_list, args.vcf_file, args.output_file)


