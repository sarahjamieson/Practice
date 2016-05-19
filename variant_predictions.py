from urllib2 import Request, urlopen, URLError
import ast
import json
import argparse
from argparse import RawTextHelpFormatter
import os
from biomart import BiomartServer

# http://genetics.bwh.harvard.edu/pph2/dokuwiki/_media/hg0720.pdf - polyphen-2 api info
'''
parser = argparse.ArgumentParser(description="Outputs SNP predictions from PolyPhen-2, SIFT, MA & MT.",
                                 epilog="This script requires HGVS nomenclature.",
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument('-chr', action="store", dest='chr', help="chromosome", required=True, type=str)
parser.add_argument('-pos', action="store", dest='pos', help="genomic coordinate", required=True, type=int)
parser.add_argument('-wt', action="store", dest='wt', help="wild-type nucleotide", required=True, type=str)
parser.add_argument('-var', action="store", dest='var', help="variant nucleotide", required=True, type=str)
args = parser.parse_args()
'''
# get chr, location, wt, mut


def get_result(chr, coord, wt, var):
    result = urlopen("http://www.broadinstitute.org/oncotator/mutation/%s_%s_%s_%s_%s/"
                     % (chr, coord, coord, wt, var))
    response = result.read()
    onco_dict = ast.literal_eval(response)

    mut_ass_pred = onco_dict.get("dbNSFP_MutationAssessor_pred")
    mut_ass_rank = onco_dict.get("dbNSFP_MutationAssessor_rankscore")
    mut_ass_score = onco_dict.get("dbNSFP_MutationAssessor_score")

    mut_tas_pred = onco_dict.get("dbNSFP_MutationTaster_pred")
    mut_tas_rank = onco_dict.get("dbNSFP_MutationTaster_converted_rankscore")
    mut_tas_score = onco_dict.get("dbNSFP_MutationTaster_score")

    pp_humdiv_pred = onco_dict.get("dbNSFP_Polyphen2_HDIV_pred")
    pp_humdiv_rank = onco_dict.get("dbNSFP_Polyphen2_HDIV_rankscore")
    pp_humdiv_score = onco_dict.get("dbNSFP_Polyphen2_HDIV_score")

    pp_humvar_pred = onco_dict.get("dbNSFP_Polyphen2_HVAR_pred")
    pp_humvar_rank = onco_dict.get("dbNSFP_Polyphen2_HVAR_rankscore")
    pp_humvar_score = onco_dict.get("dbNSFP_Polyphen2_HVAR_score")

    sift_pred = onco_dict.get("dbNSFP_SIFT_pred")
    sift_rank = onco_dict.get("dbNSFP_SIFT_converted_rankscore")
    sift_score = onco_dict.get("dbNSFP_SIFT_score")

    output_file = open("variant_predictions.txt", "w")
    line1 = "Predictor\tPrediction\tRank\tScore"
    line2 = "%s\t%s\t%s\t%s" % ("Mutation Assessor", mut_ass_pred, mut_ass_rank, mut_ass_score)
    line3 = "%s\t%s\t%s\t%s" % ("Mutation Taster", mut_tas_pred, mut_tas_rank, mut_tas_score)
    line4 = "%s\t%s\t%s\t%s" % ("PolyPhen-2 HumDiv", pp_humdiv_pred, pp_humdiv_rank, pp_humdiv_score)
    line5 = "%s\t%s\t%s\t%s" % ("PolyPhen-2 HumVar", pp_humvar_pred, pp_humvar_rank, pp_humvar_score)
    line6 = "%s\t%s\t%s\t%s" % ("SIFT", sift_pred, sift_rank, sift_score)
    output_file.write("%s\n%s\n%s\n%s\n%s\n%s" % (line1, line2, line3, line4, line5, line6))
    output_file.close()

    print "done"

    return mut_ass_pred, mut_ass_rank, mut_ass_score, mut_tas_pred, mut_tas_rank, mut_tas_score, pp_humdiv_pred, \
        pp_humdiv_rank, pp_humdiv_score, pp_humvar_pred, pp_humvar_rank, pp_humvar_score, sift_pred, sift_rank, \
        sift_score


# get_result(args.chr, args.pos, args.wt, args.var)


def get_gene_info(gene):
    """Takes a gene and uses Ensembl API (GET xrefs/symbol/:species/:symbol) to extract ENSG and LRG codes.

    :param gene: gene to be searched for.
    :return: ENSG and LRG codes.
    """
    webpage = urlopen("http://rest.ensembl.org/xrefs/symbol/homo_sapiens/%s?content-type=application/json" % gene)
    result = webpage.read()
    jdata = json.loads(result)
    gene_list = []
    for item in jdata:
        for key, value in item.iteritems():
            if key == "id":
                gene_list.append(value)
    ensg = gene_list[0]
    lrg = gene_list[1]
    return ensg, lrg


def get_transcript(ensg, refseq):
    server = BiomartServer("http://www.ensembl.org/biomart")
    server.verbose = True
    new_list = []
    hs_genes = server.datasets['hsapiens_gene_ensembl']
    results = hs_genes.search({
        'filters': {'ensembl_gene_id': '%s' % ensg,
                    'refseq_mrna': '%s' % refseq},
        'attributes': ['ensembl_transcript_id', 'ensembl_peptide_id']
    }, header=1)
    for line in results.iter_lines():
        line = line.decode('utf-8')
        new_list.append(line.split())
    uni_transcript = new_list[1]
    transcript = uni_transcript[0]
    protein = uni_transcript[1]
    return transcript, protein


refseq = "NM_000059"
ensg, lrg = get_gene_info("BRCA2")  # example, use parser
get_transcript(ensg, refseq)

