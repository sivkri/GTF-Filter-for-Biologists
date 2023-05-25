# extractgtf

**To filter and extract information based on your input**

The below procedure can be carrried on linux commands

**Example Usage**

`python extractGTF.py homo_sapiens_short.gtf 11 11_result.txt`

**Explanation of input**
`sys.argv[1] # a gtf file name i.e., homo_sapiens_short.gtf`

`sys.argv[2] # the requested chromosome name (seqname); for ENSEMBL use e.g. 11, for UCSC: chr11, etc.`

`sys.argv[3] # open the output file i.e., 11_result.txt`

**Alternative option**

If you want to shortlist based on **"feature"** then replace _line.split('\t')[0]_ with _line.split('\t')[2]_

Under sys.argv[2], provide input as **"start_codon"** or **"CDS"**


# Traditional usage

**Step0. Unzipping and extracting the contents of .gz file**

`gunzip 1.gtf.gz`

ls  # check if 1.gtf.gz has been unzipped to 1.gtf

**Step1. View the basic information of the file**

`cat 1.gtf | head` Display the first 10 lines of 1.gtf file

`cat 1.gtf | tail` Display the last 10 lines of the 1.gtf file

`cat 1.gtf | head -15` Display the first 15 lines of the 1.gtf file (the input value 15 can be replaced by other integers)

`ls -lh 1.gtf` Display the size of the 1.gtf file

`wc -l 1.gtf` Statistics 1.gtf file line number

**Use grep -v to exclude comment line (parts beginning with #) and blank lines with a length of 0**

`'^' matches the beginning of the line, '$' matches the end of the line`

`'^#' matches lines starting with '#'`

If '^$' can match a certain line, it means that the line is empty (the beginning of the line is followed by the end of the line, and there are no other characters in between)

`grep -v "^#" 1.gtf | grep -v '^$' | wc -l`

**Filter blank empty lines (in addition to line breaks, lines that may also include blank characters, such as spaces and tabs), display the first 10 lines of results
`'\s'` matches a blank character, `'*'` means that such a character will appear 0 or more times, `'^\s*$'` indicates that there are only 0 or more blank characters between the beginning and end of a line**

`cat 1.gtf | awk '$0!~/^\s*$/{print}' | head -10`

`grep -v '^\s*$' 1.gtf | head -10`

**step2. Data extraction**

**step2.1 Filter specific columns**

Select the data of 1-3 columns (the following two commands are available)

awk's default line separator is space `" "` and tab `"\t"`

After awk divides each row into columns by delimiter, the values of columns 1, 2, and 3 can be obtained through $1, $2, and $3 ($0 represents the content of the entire row)

`cat 1.gtf | awk ' { print $1, $2, $3 } ' | head`

The default delimiter for cut is "\t"

`cat 1.gtf | cut -f 1,2,3 | head`

Eg. For example, I only need columns 1, 3, 4, and 5 of the GTF file, which are chr, feature, start, and end.

`cut -f 1,3,4,5 1.gtf | head`

**step2.2 Filter specific rows**

Suppose we want to extract the row whose third column is gene, and only display the information in columns 1, 3, and 9.

awk separates each line into columns according to the default line separator, and prints out columns 1, 3, and 9 for the line whose third column is equal to "gene"

`cat 1.gtf | awk '$3 == "gene" { print $1, $3, $9 } ' | head`

**step3. Extract and calculate specific features**

**step3.1 Extract and count featrue types**

`grep -v '^#' 1.gtf |awk '{print $3}'| sort | uniq -c` #Extract and count how many types of features there are

**step3.2 Calculate the feature length of a specific feature**

The value in the 5th column minus the value in the 4th column + 1, that is, the length of the feature feature

The coordinates of the gff/gtf file start from 1, and the range is a closed interval (the coordinates of the bed file we will encounter later start from 0, and the range is left closed and right open)

`cat 1.gtf | awk ' { print $3, $5-$4 + 1 } ' | head`

**_Calculate the total length of all CDS_**

`cat 1.gtf | awk 'BEGIN{size=0;}$3 =="CDS"{ len=$5-$4 + 1; size += len; print "Size:", size } ' | tail -n 1`

Or use awk to only output the statistical results at the end:

`cat 1.gtf | awk 'BEGIN{L=0;}$3 =="CDS"{L+=$5-$4 + 1;}END{print L;}'`

Or use the feature of awk automatic initialization:

`cat 1.gtf | awk '$3 =="CDS"{L+=$5-$4 + 1;}END{print L;}'`

**_Calculate the average length of chromosome 1 cds_**

awk can read input from both pipe and file

`awk 'BEGIN {s = 0;line = 0;}$3 =="CDS" && $1 =="I"{ s += $5-$4+1;line += 1}END {print "mean="s/ line}' 1.gtf`

**Step3.3 Separate and extract the gene name**

Separate and extract the gene name from the gtf file and calculate its length

split is a built-in function of awk, because the string is split according to the specified delimiter. It takes three parameters as input string, output list and delimiter

Here x is the output list, no prior declaration is required in awk

The list subscript of awk starts from 1

gsub is also a built-in function of awk, used to replace

gsub(`"\""`, "", name) is to remove the quotation marks in the name. `"` itself is a special character in awk. `\` is the escape symbol, `\"` tells awk to treat the " here as a normal character

`cat 1.gtf | awk '$3 == "gene"{split($10,x,";");name = x[1];gsub("\"", "", name);print name,$5- $4+1}' | head`

**Step4. Extract the data and store it in a new file**

This stage is mainly to learn to extract data and save it into a new file, for example, find the 3 exons with the longest length, and report their length.

Two methods are introduced here.

The first is to directly extract and calculate the longest 3 exons, report their length, and save them in a `.txt` file;

The second method is to write an executable file `run.sh`, find the 3 longest exons, and report their lengths.

**step4.1 Demonstration of extracting data and storing it in a txt file**

We use the output redirection operator `>` to save what would be printed to the terminal screen by default into a disk file `1.txt`.

`grep exon 1.gtf | awk '{print $5-$4+1}' | sort -n | tail -3 > 1.txt`

If `1.txt` is an existing file, the content of the output redirection operator `>` will overwrite the original file.

If we want to append the output to the redirected file instead of overwriting the original file when the redirected file exists, we can use the `>>` operator.

Then enter the command `less 1.txt` or `vi 1.txt` to enter the vi general mode interface to display the output results.

At this time, press `:q` or `:wq` as input method state to return to the terminal shell window.

When typing less to view a file, you can also use q to exit the viewing mode.

Copy `1.txt` to `/home/`, and you can view the `1.txt` file in the shared directory of the host.

**step4.2 Executable file editing demonstration**

The first step is to enter the command to enter the vi editing interface.

`vi run.sh`

In the second step, after pressing the i key to switch to the insert mode, write down the contents of the rush.sh file as follows:

`#!/bin/bash`

`grep exon *.gtf | awk '{print $5-$4+1}' | sort -n | tail -3`

`#!/bin/bash` on the first line tells the operating system to use `/bin/bash` as the interpreter to run the script

The third step is to press Esc or `ctrl+[` to switch back to the normal mode, enter :wq to exit the vi editor, and type after the command line:

Give the script executable permissions

`chmod u+x run.sh`

# run the script

`./run.sh`

Since we added the `#!/bin/bash` line, the operating system will use `/bin/bash` to run the script. If `run.sh` is not given executable permission, running `./run.sh` will prompt permission denied, However if you manually specify the interpreter and use it `bash run.sh`, can also run normally

The output is consistent with the content of `1.txt.`

