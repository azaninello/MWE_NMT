import re
import xlrd
import string
import matplotlib.pyplot as plt

def plot():
    fig1 = plt.figure(1)

    # and the first axes using subplot populated with data
    ax1 = fig1.add_subplot(211)
    # line1 = ax1.plot([1, 3, 4, 5, 2], 'o-')
    # ylabel("Left Y-Axis Data")

    # now, the second axes that shares the x-axis with the ax1
    ax2 = fig1.add_subplot(211, sharex=ax1, frameon=False)
    # line2 = ax2.plot([10, 40, 20, 30, 50], 'xr-')
    # ax2.yaxis.tick_right()
    # ax2.yaxis.set_label_position("right")
    # plt.yticks([0.1, 0.0], ["h +", "h -"], side='right')
    # ylabel("Right Y-Axis Data")

    # for the legend, remember that we used two different axes so, we need
    # to build the legend manually
    # legend((line1, line2), ("1", "2"))

    plt.figure(1)
    plt.subplot(211)
    #plt.plot(time[:t + 1], W[:t + 1])
    #data = time[:t + 1], W[:t + 1]
    # plt.plot(data)
    # plt.hlines(a,0,t)
    plt.hlines(y=0.1, xmin=0, xmax=100)
    plt.hlines(y=0, xmin=0, xmax=100)
    plt.xlabel("Reaction time (in ms)")
    plt.yticks([0.1, 0.0, 0.05], ["a = 0.1", "0", "z = 0.05"])
    plt.xticks([])
    plt.show()


def make_stats(infile="stats/train.exp3tb.BPE.en", raw=False, bpe=False, mwe=False, incremental=False):
    with open(infile, "r", encoding="utf-8") as s:
        myfile = s.readlines()

        if raw or bpe:
            types = {"the"}
            tokens = []
            if mwe:
                print("Select only one option")
            else:
                    for line in myfile:
                        if raw:
                            newline = re.sub("@@ ", "", line)
                            linelist = re.split("[ _\n]", newline)
                            #print(linelist)
                        if bpe:
                            linelist = re.split("[ \n]", line)
                        for word in linelist:
                            tokens.append(word)
                            types.add(word)
                    return tokens, types
        elif mwe:
            mwe_tokens = []
            c = 0
            wc = 0
            increm_tokens = []
            increm_types = []
            increm_wc = []
            for line in myfile:
                c += 1
                newline = re.sub("@@ ", "", line)
                for word in newline.split():
                    wc += len(newline.split())
                    if "_" in word:
                        mwe_tokens.append(word)
                    if incremental:
                        if wc%10000==0:
                            increm_tokens.append(len(mwe_tokens))
                            increm_types.append(len(set(mwe_tokens)))
                            increm_wc.append(wc)
            if incremental:
                increm_tokens.append(len(mwe_tokens))
                increm_types.append(len(set(mwe_tokens)))
                increm_wc.append(wc)
                return increm_tokens, increm_types, increm_wc
            #elif mwe:
                #return mwe_tokens

def count_mwe_big(myfile="C:/Users/azaninello/Desktop/experiments/nuovo/big/data_exp1_big/old/train_annotated.mos",
                  mwe_tokens=True, factor=0, lemmas=False):
    mwes = []
    steps = [0.2, 0.4, 0.6, 0.8, 1]
    with open(myfile, "r", encoding="utf-8") as file:
        #file = f.readlines()
        to = []
        ty = []
        le = {"the"}
        ty_c = []
        wc_c = []
        c = 0
        wc = 0
        for line in file:
            #print(line)
            c += 1
            if c%10000==0:
                print(c)
            for word in line.split():
                wc += len(line.split())
                #print(word)
                factors = [f for f in word.split("|")]
                #print(factors)
                if lemmas:
                    le.add(factors[factor])
                    if wc % 10000 == 0:
                        wc_c.append(wc)
                        ty_c.append(len(le))
                if mwe_tokens:
                    if "_" in factors[factor]:
                        mwes.append(factors[factor])
                    if wc%10000==0:
                        to.append(len(mwes))
                        ty.append(len(set(mwes)))
                        wc_c.append(wc)
    to.append(len(mwes))
    ty.append(len(set(mwes)))
    wc_c.append(wc)

    file.close()
    if mwe_tokens:
        return to,ty,wc_c
    if lemmas:
        return ty_c

    #return {"tokens": len(tokens), "types": len(types)}

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

def read_excel(file="aggregated.xlsx"):
    """reads in the excel file to parse test set;
    returns a dictionary of the form
    {num_sent: {'sentences': [en, it, smt], 'mwes': [en, it, smt, y/n]}}"""
    workbook = xlrd.open_workbook(file, "r")
    sheet = workbook.sheet_by_name('AGGREGATOR')
    values = {}
    row_idx = 0
    while row_idx < sheet.nrows:
        try:
            count = int(sheet.cell(row_idx, 0).value)
            en, it, smt = sheet.cell(row_idx, 1).value, sheet.cell(row_idx, 2).value, sheet.cell(row_idx, 3).value
            values[count] = {"sentences": [en, it, smt], "mwes": []}
            temp_row_idx = row_idx+1
            try:
                while sheet.cell(temp_row_idx, 0).value == '':

                    if sheet.cell(temp_row_idx, 4).value == 'FINAL' and sheet.cell(temp_row_idx, 5).value == 'Y' \
                            and sheet.cell(temp_row_idx, 8).value == 'Y':
                        #print(sheet.cell(temp_row_idx, 4).value)
                        for c in range(8):
                            mwe_en_1, mwe_it_1, mwe_smt_1, correct = sheet.cell(temp_row_idx, 6*c+6).value, sheet.cell(temp_row_idx, 6*c+7).value, \
                                                                     sheet.cell(temp_row_idx, 6*c+10).value, sheet.cell(temp_row_idx, 6*c+11).value
                            values[count]["mwes"].append([mwe_en_1, mwe_it_1, mwe_smt_1, correct])
                    temp_row_idx += 1
            except(IndexError):
                print("fin")
                pass
        except(ValueError):
            pass
        finally:
            row_idx += 1
    return values



def read_excel_t2(file="eval/test2_annotated.xlsx"):
    """reads in the excel file to parse test set;
    returns a dictionary of the form
    {num_sent: {'sentences': [en, it, smt], 'mwes': [en, it, smt, y/n]}}"""
    workbook = xlrd.open_workbook(file, "r")
    sheet = workbook.sheet_by_name('results')
    values = {}
    row_idx = 0
    while row_idx < sheet.nrows:
            #count = int(sheet.cell(row_idx, 0).value)
            en, ref, mwe1, mwe2, bl_s, exp1, exp2, exp3, exp4, bl_b, exp5 = \
                sheet.cell(row_idx, 0).value, sheet.cell(row_idx, 1).value, sheet.cell(row_idx, 2).value, sheet.cell(row_idx, 3).value, \
            sheet.cell(row_idx, 4).value, sheet.cell(row_idx, 5).value, sheet.cell(row_idx, 6).value, sheet.cell(row_idx, 7).value, \
            sheet.cell(row_idx, 8).value, sheet.cell(row_idx, 9).value, sheet.cell(row_idx, 10).value
            values[row_idx] = {"en": en, "ref": ref, "mwes": [mwe1], "bl_s": bl_s, "exp1": exp1, "exp2": exp2,
                               "exp3": exp3, "exp4": exp4, "bl_b": bl_b, "exp5": exp5}
            row_idx += 1
    print("fin")
    return values

import numpy as np

from nltk.corpus import stopwords

def eval_t1(trans_file, stop=False):
    """reads in the test set (as returned by read_excel())
     and calculates an array of scores, score = length of ref MWE / terms of ref MWE in translation;
     change where the 'trans' variable reads the input sentences to to adapt to different translations"""
    it_stop = stopwords.words("italian")
    values = read_excel()
    vals = []
    n = []
    y = []
    # with open(trans_file, "r", encoding="utf-8") as t:
    #     trans = t.readlines()
    #     for p,line in enumerate(trans):
    #         trans[p] = line.lower()
    trans = [values[num]['sentences'][2] for num in values] # change here for other reference translations
    #with open("{}.mwes".format(trans_file), "w+", encoding="utf-8") as o:
    for sent_num in range(1,len(trans)+1):
        ref_trans = (re.sub("[{}]".format(string.punctuation)," ", trans[sent_num-1])).lower().split() # ignores punctuation,
                                                                                # including ... indicating discontinuous MWEs
        #if stop:
            #ref_trans = [m for m in ref_trans if m not in it_stop]

        for mwe in values[sent_num]["mwes"]:
            new_match = []
            if mwe[0] is not '':
                mwe_proc = (re.sub("[{}]".format(string.punctuation)," ", mwe[1])).lower().split()
                #if not stop:
                #match = [m.lower() for m in mwe_proc if m.lower() in ref_trans]
                #else:
                #match = [m.lower() for m in mwe_proc if m.lower() in ref_trans]
                #NEW

                for item in mwe_proc:
                    distances = [levenshteinDistance(item,w) for w in ref_trans]
                    item_dist = min(distances)/len(item) if min(distances)/len(item) <= 1 else 1
                    new_match.append(item_dist)
            vals.append(np.mean(new_match))
                    #ENDNEW

                    #if len(match) == len(mwe_proc):
                        #vals.append(1)
                        #y.append(1)
                        #o.write("{} > {} > {} > {}\n".format(1, mwe_proc, match, ref_trans))




                    #else:
                        #n.append(1)

                        ## #NEW CODE ###

                        #vals.append(len(match)/len(mwe_proc))


                        ### END NEW CODE ###
                        #o.write("{} > {} > {} > {}\n".format(len(match)/len(mwe_proc), mwe_proc, match, ref_trans))
                    #print(sent_num, ref_trans, mwe_proc, match)
    #y_n = [m["mwes"][2] for m in values]
    return np.mean(vals)



def eval_new(trans_file="", test="test1", exp="exp1"):
    """reads in the test set (as returned by read_excel())
     and calculates an array of scores, score = length of ref MWE / terms of ref MWE in translation;
     change where the 'trans' variable reads the input sentences to to adapt to different translations"""
    it_stop = stopwords.words("italian")

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
            #print("CAZZO", trans[p])
    #trans = [values[num]['sentences'][2] for num in values] # change here for other reference translations
    #with open("{}.mwes".format(trans_file), "w+", encoding="utf-8") as o:
    for sent_num in range(len(trans)):
        ref_trans = re.sub("[{}]".format(string.punctuation)," ", trans[sent_num]).split() # ignores punctuation,
                                                                        # including ... indicating discontinuous MWEs
        #print(ref_trans)
        for mwe in values[sent_num]["mwes"]:
            #print(mwe)
            new_match = []
            if mwe is not '':
                #print(mwe)
                mwe_proc = re.sub("[{}]".format(string.punctuation)," ", mwe).split()
                #print(mwe_proc)
                    #NEW
                for item in mwe_proc:
                    try:
                        distances = [levenshteinDistance(item,w) for w in ref_trans]

                        #print(distances)
                        item_dist = min(distances)/len(item) #if min(distances)/len(item) <= 1 else 1
                        new_match.append(item_dist)
                        #print(new_match)
                    except:
                        pass
                vals.append(1-(np.mean(new_match)))
                #print(1-(np.mean(new_match)))

    return np.mean(vals)


def count_disc(values): # returns a count of discontinuos MWEs (En, It, It for disc_En)
    punt = re.compile(r"\w+\s?\.\.\s?(\.)*\s?\w+") # detects discontinuous MWEs
    disc_en = [m[0] for i in range(1,len(values)+1) for m in values[i]["mwes"] if punt.search(m[0])]
    disc_it = [m[1] for i in range(1,len(values)+1) for m in values[i]["mwes"] if punt.search(m[1])]
    disc_it_foren = [m[1] for i in range(1,len(values)+1) for m in values[i]["mwes"] if punt.search(m[0])
                      and punt.search(m[1])] # num of Engl discont'ed MWEs which translated into Italian discont'ed MWEs
    return len(disc_en), len(disc_it), len(disc_it_foren)

def print_data(values, en_file="test_en", it_file="test_it", smt_file="smt_it", mwes="mwes_all"):
    """creates 4 different output files:
    parallel EN, It, SMT traslations;
    a MWE list > this maybe to be fixed"""
    with open(en_file, "w", encoding="utf-8") as en, open(it_file, "w", encoding="utf-8") as it, \
            open(smt_file, "w", encoding="utf-8") as smt, open(mwes, "a+", encoding="utf-8") as m:
        for i in range(1,len(values)+1):
            en.write(values[i]["sentences"][0] + "\n")
            it.write(values[i]["sentences"][1] + "\n")
            smt.write(values[i]["sentences"][2] + "\n")
            m.write("{}".format(i) + "\n")
            for mwe in values[i]["mwes"]:
                if mwe[0] != '':
                    m.write(mwe[0] + "\t" + mwe[1] + "\t" + mwe[2] + "\t" + mwe[3] + "\n")