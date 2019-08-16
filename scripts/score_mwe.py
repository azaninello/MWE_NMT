import numpy as np
from process_testset import *

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def score(trans_file="", test="test1", exp="exp1"):
    """reads in the test set (as returned by read_excel()) or from arg;
     calculates Scores_mwe; trans_file is the reference MWE translations file;
     change where the trans_file variable reads the input
     sentences to to adapt to different reference translations"""
    values = read_excel_t2()
    vals = []
    if test=="test2":
        with open(trans_file, "r", encoding="utf-8") as t:
            trans = t.readlines()
    elif test=="test1":
        trans = []
        for num in values:
            trans.append(values[num][exp])
        print(trans[:10])
    for p,line in enumerate(trans):
            trans[p] = line.lower()
    for sent_num in range(len(trans)):
        ref_trans = re.sub("[{}]".format(string.punctuation)," ", trans[sent_num]).split() # ignores punctuation,
                                                                        # including ... indicating discontinuous MWEs
        for mwe in values[sent_num]["mwes"]:
            new_match = []
            if mwe is not '':
                mwe_proc = re.sub("[{}]".format(string.punctuation)," ", mwe).split()
                for item in mwe_proc:
                    try:
                        distances = [levenshteinDistance(item,w) for w in ref_trans]

                        item_dist = min(distances)/len(item) if min(distances)/len(item) <= 1 else 1
                        new_match.append(item_dist)
                    except:
                        pass
                vals.append(1-(np.mean(new_match)))
    return np.mean(vals)