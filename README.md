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
