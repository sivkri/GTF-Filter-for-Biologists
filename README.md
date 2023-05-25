# extractgtf

**To filter and extract information based on your input**

The below procedure can be carrried on linux commands


**Example Usage**

python extractGTF.py homo_sapiens_short.gtf 11 11_result.txt


**Explanation of input**
sys.argv[1] # a gtf file name i.e., homo_sapiens_short.gtf

sys.argv[2] # the requested chromosome name (seqname); for ENSEMBL use e.g. 11, for UCSC: chr11, etc.

sys.argv[3] # open the output file i.e., 11_result.txt



**Alternative option**

If you want to shortlist based on **"feature"** then replace _line.split('\t')[0]_ with _line.split('\t')[2]_

Under sys.argv[2], provide input as **"start_codon"** or **"CDS"**


# Traditional usage

**Step1. View the basic information of the file**

cat 1.gtf | head #Display the first 10 lines of 1.gtf file

cat 1.gtf | tail #Display the last 10 lines of the 1.gtf file

cat 1.gtf | head -15 #Display the first 15 lines of the 1.gtf file (the input value 15 can be replaced by other integers)

ls -lh 1.gtf #Display the size of the 1.gtf file

wc -l 1.gtf #Statistics 1.gtf file line number

**Use grep -v to exclude comment line (parts beginning with #) and blank lines with a length of 0**

'^' matches the beginning of the line, '$' matches the end of the line

'^#' matches lines starting with '#'

If '^$' can match a certain line, it means that the line is empty (the beginning of the line is followed by the end of the line, and there are no other characters in between)

grep -v "^#" 1.gtf | grep -v '^$' | wc -l

**Filter blank empty lines (in addition to line breaks, lines that may also include blank characters, such as spaces and tabs), display the first 10 lines of results
('\s' matches a blank character, '*' means that such a character will appear 0 or more times, '^\s*$' indicates that there are only 0 or more blank characters between the beginning and end of a line)**

cat 1.gtf | awk '$0!~/^\s*$/{print}' | head -10

grep -v '^\s*$' 1.gtf | head -10


