import pandas as pd

names = ["COL4A5_1", "COL4A5_2", "COL4A5_3", "COL4A5_4"]
forwards = ["GCTTCTTTCTCTTCACCCAAG", "GGATTGTTGATTTCAGTTGAGC", "TGAATCTCAACCATGCCTGT", "TAAATGCTTCTTCCTTGGGTG"]
reverses = ["CCTAGTCAACGCCAAAAGGA", "TGTGACAGAAACTGATGTGTCC", "GACTCCCCGTCATTCCATT", "CATAATTCTCAACCATAAGCTAC"]
primer_seqs = pd.DataFrame([])
n = 0

while n < 4:
    ser = pd.Series([names[n], forwards[n], reverses[n]])
    primer_seqs = primer_seqs.append(ser, ignore_index=True)
    n += 1

primer_seqs.to_csv('ruffus_input.csv', header=None, index=None, sep='\t')
