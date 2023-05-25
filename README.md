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

**Step0. Unzipping and extracting the contents of .gz file**

gunzip 1.gtf.gz

ls  # check if 1.gtf.gz has been unzipped to 1.gtf

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

**step2. Data extraction**

**step2.1 Filter specific columns**

Select the data of 1-3 columns (the following two commands are available)

awk's default line separator is space " " and tab "\t"

After awk divides each row into columns by delimiter, the values of columns 1, 2, and 3 can be obtained through $1, $2, and $3 ($0 represents the content of the entire row)

cat 1.gtf | awk ' { print $1, $2, $3 } ' | head

The default delimiter for cut is "\t"

cat 1.gtf | cut -f 1,2,3 | head

Eg. For example, I only need columns 1, 34, and 5 of the GTF file, which are chr, feature, start, and end.

cut -f 1,3,4,5 1.gtf | head

**step2.2 Filter specific rows**

Suppose we want to extract the row whose third column is gene, and only display the information in columns 1, 3, and 9.

awk separates each line into columns according to the default line separator, and prints out columns 1, 3, and 9 for the line whose third column is equal to "gene"

cat 1.gtf | awk '$3 == "gene" { print $1, $3, $9 } ' | head

**step3. Extract and calculate specific features**

This stage is a further study on the basis of learning step2. For the first attempt, first copy the following commands, observe the output results, and then suggest trying to modify the parameters in the following commands for more practice.

**step3.1 Extract and count featrue types**

grep -v '^#' 1.gtf |awk '{print $3}'| sort | uniq -c #Extract and count how many types of features there are

**step3.2 Calculate the feature length of a specific feature**

The value in the 5th column minus the value in the 4th column + 1, that is, the length of the feature feature

The coordinates of the gff/gtf file start from 1, and the range is a closed interval (the coordinates of the bed file we will encounter later start from 0, and the range is left closed and right open)

cat 1.gtf | awk ' { print $3, $5-$4 + 1 } ' | head

**_Calculate the total length of all CDS_**

cat 1.gtf | awk 'BEGIN{size=0;}$3 =="CDS"{ len=$5-$4 + 1; size += len; print "Size:", size } ' | tail -n 1

Or use awk to only output the statistical results at the end:

cat 1.gtf | awk 'BEGIN{L=0;}$3 =="CDS"{L+=$5-$4 + 1;}END{print L;}'

Or use the feature of awk automatic initialization:

cat 1.gtf | awk '$3 =="CDS"{L+=$5-$4 + 1;}END{print L;}'

**_Calculate the average length of chromosome 1 cds_**

awk can read input from both pipe and file

awk 'BEGIN {s = 0;line = 0;}$3 =="CDS" && $1 =="I"{ s += $5-$4+1;line += 1}END {print "mean="s/ line}' 1.gtf

