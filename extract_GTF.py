import sys

# read program parameters from the command line
GTF = sys.argv[1]  # a gtf file name i.e., homo_sapiens_short.gtf
input_chr = sys.argv[2]  # the requested chromosome name (seqname); for ENSEMBL use e.g. 11, for UCSC: chr11, etc.
out_file = sys.argv[3]  # open the output file i.e., 11_result.txt

# open the output file for writing
with open(out_file, 'w') as out:
    # iterate through each line in the GTF file
    for line in open(GTF):
        # check if the chromosome name in the line matches the requested chromosome
        if line.split('\t')[0] == input_chr:
            out.write(line)
