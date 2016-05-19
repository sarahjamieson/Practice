from ruffus import *
import os
import sys

starting_file = "ruffus_input.csv"


@posttask(lambda: sys.stdout.write("PCR complete\n"))
@transform(starting_file, suffix(".csv"), ".tmp.psl")
def run_pcr(input_file, output_file):
    chromosomes = ['chr1.2bit', 'chr11.2bit', 'chr12.2bit', 'chrX.2bit', 'chr13.2bit', 'chr14.2bit', 'chr15.2bit',
                   'chr16.2bit', 'chr17.2bit', 'chr18.2bit', 'chr19.2bit', 'chr20.2bit', 'chr21.2bit', 'chr22.2bit',
                   'chr2.2bit', 'chr3.2bit', 'chr4.2bit', 'chr5.2bit', 'chr6.2bit', 'chr7.2bit', 'chr8.2bit',
                   'chr9.2bit', 'chr10.2bit', 'chrY.2bit']

    for chr in chromosomes:
        os.system(
            "/opt/kentools/isPcr -out=psl /media/genomicdata/ucsc_hg19_by_chr/2bit_chr/%s \
            %s %s" % (chr, input_file, output_file))


@posttask(lambda: sys.stdout.write("PSL converted to BED\n"))
@follows("run_pcr")
@transform(run_pcr, suffix(".tmp.psl"), ".bed")
def psl_to_bed(input_file, output_file):
    os.system("/opt/kentools/pslToBed %s %s" % (input_file, output_file))

pipeline_run(verbose=3)
