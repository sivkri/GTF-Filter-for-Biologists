import sys

# read program parameters from the command line
GTF = sys.argv[1] # a gtf file name
input_chr = sys.argv[2] # the requested chromosome name; for ENSEMBL use e.g. 1, for UCSC: chr1, etc.
out = open(sys.argv[3], 'w')  # open the output file

for line in open(GTF):
  if line.split('\t')[0] == input_chr:
    out.write(line)
    
