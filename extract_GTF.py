import sys

for line in open(GTF):
  if line.split('\t')[0] == input_chr:
    out.write(line)
    