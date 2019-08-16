import re
import string
from sacremoses import MosesTokenizer as MT
import nltk
from textblob import TextBlob as tb
from nltk.parse import CoreNLPParser
parser = CoreNLPParser(url='http://localhost:9000')
pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')

def clean(l1= "C:/Users/azaninello/Desktop/experiments/nuovo/exp1/zing_phrases_examples", l2= "C:/Users/azaninello/Desktop/experiments/nuovo/exp1/zing_phrases_examples"):
    en_tok = MT(lang='en')
    it_tok = MT(lang='it')
    with open(l1, "r", encoding="utf-8") as en, open(l2, "r", encoding="utf-8") as it:
        en_text = en.readlines()
        it_text = it.readlines()
    with open("STOCAZZO.en", "w+", encoding="utf-8") as cl_en, open("DAJE.it", "w+", encoding="utf-8") as cl_it:
        c = 0
        for line_en, line_it in zip(en_text,it_text):
            line_en = " ".join(en_tok.tokenize(line_en)).lower().replace("&apos;", "'").replace("&quot;", '"')
            line_it = " ".join(it_tok.tokenize(line_it)).lower().replace("&apos;", "'").replace("&quot;", '"')
            cl_en.write(line_en + "\n")
            cl_it.write(line_it + "\n")
            c+=1
            if c % 500 == 0:
                print("Processed {} sentences".format(c))
    #return en_text, it_text

def exp3_pipeline(mos_infile, BPE_infile, outfile):
    new_txt = moses(mos_infile)
    new_BPE_text = manage_BPE(new_txt, BPE_infile)
    text(new_BPE_text, outfile)

def annotate_lemmas(infile="file.txt", outfile="file.mos"):
    wd = nltk.WordNetLemmatizer()
    with open(infile, "r", encoding="utf-8") as f:
        text = f.readlines()
        new_text = []
        for line in text:
            if len(new_text) % 500 == 0:
                print("Processing sentence", len(new_text))
            if line[0] == "#":
                pass
            else:
                line = line.split()
                newline = []
                for word in line:
                    factors = "{}|{}|{}|{}".format(word, wd.lemmatize(word), "O", "Null")
                    newline.append(factors)
            new_text.append(newline)
    with open(outfile, "w", encoding="utf-8") as ff:
        for nl in new_text:
            for nw in nl:
                ff.write(nw+" ")
            ff.write("\n")

def annotator_splitter(infile="file.txt"):
    wd = nltk.WordNetLemmatizer()
    with open(infile, "r", encoding="utf-8") as f:
        text = f.readlines()
        new_text = []
        for line in text:
            if len(new_text)%500 == 0:
                print("Processing sentence", len(new_text))
            if line[0] == "#":
                pass
            else:
                line = line.split()
                newline = []
                for word in line:
                    factors = word.split("|")  # [surface, lemma, pos, other]
                    #print(word, factors)
                    if "_" not in factors[0]:
                        factors.pop(2) #nltk.pos_tag([factors[0]])[0][1]
                        #try:
                            #factors[1] = wd.lemmatize(factors[0], factors[2].lower()[0])
                        #except(KeyError):
                            #factors[1] = wd.lemmatize(factors[0])
                        factors[2] = 'O'
                        newline.append(factors)
                    else:
                        new_words = factors[0].split("_")
                        for pos, w in enumerate(new_words):
                            try:
                                if pos == 0:
                                    w_factors = [w, factors[1], "B"]
                                else:
                                    w_factors = [w, factors[1], "I"]
                                newline.append(w_factors)
                            except:
                                print(line)
                                break
                #new_w = [w[0] for w in newline]
                #print(new_w)
                #line_withpos_t = list(list(nltk.pos_tag(new_w)))
                #print(line_withpos_t)
                #for p,word in enumerate(newline):
                    #word.pop(2)
                    #print(newline[p][2])
                #print(newline)
                new_text.append(newline)
                #print(len(new_text))
    return new_text


def moses(infile="moses.3"):
    wd = nltk.WordNetLemmatizer()

    with open(infile, "r", encoding="utf-8") as f:
        text = f.readlines()
        new_text = []
        for line in text:
            if len(new_text)%500 == 0:
                print("Processing sentence", len(new_text))
            if line[0] == "#":
                pass
            else:
                line = line.split()
                newline = []
                for word in line:
                    factors = word.split("|")  # [surface, lemma, pos, other]
                    #print(word, factors)
                    if "_" not in factors[0]:
                        factors[2] = "POS" #nltk.pos_tag([factors[0]])[0][1]
                        try:
                            factors[1] = wd.lemmatize(factors[0], factors[2].lower()[0])
                        except(KeyError):
                            factors[1] = wd.lemmatize(factors[0])
                        factors[3] = 'O'

                        if factors[0] == "i":
                            factors[2] = "PRP"
                        elif factors[0] == "want":
                            factors[2] == "VB"
                        elif factors[0] == "'s":
                            factors[2] == "VBZ"
                        newline.append(factors)
                    else:
                        new_words = factors[0].split("_")
                        for pos, w in enumerate(new_words):
                            try:
                                if pos == 0:
                                    w_factors = [w, factors[1], "POS", "B"]
                                else:
                                    w_factors = [w, factors[1], "POS", "I"]
                                if w == "i":
                                    w_factors[2] = "PRP"
                                elif w == "want":
                                    w_factors[2] == "VB"
                                elif w == "'s":
                                    w_factors[2] == "VBZ"
                                newline.append(w_factors)
                            except:
                                print(line)
                                break
                new_w = [w[0] for w in newline]
                print(new_w)
                line_withpos_t = list(list(nltk.pos_tag(new_w)))
                print(line_withpos_t)
                for p,word in enumerate(newline):
                    newline[p][2] = line_withpos_t[p][1]
                    print(newline[p][2])
                print(newline)
                new_text.append(newline)
    return new_text # list!

def only_text(new_text, outfile, factor=0): # new test is a list
    text = [[w[factor] for w in line] for line in new_text]
    with open(outfile, "w+", encoding="utf-8") as out:
        for ln, line in enumerate(text):
            out.write(" ".join(line)+"\n")


def text_out(new_text, outfile):
    with open(outfile, "w+", encoding="utf-8") as out:
        for ln,line in enumerate(new_text):
            print(ln)
            for pos,f in enumerate(line):
                #out.write(f[0]+"|"+f[1]+"|"+f[2]+"|"+f[3]+" ")
                out.write(f[0]+"|"+f[1]+"|"+f[2]+" ")
            out.write("\n")

def manage_BPE(new_text, BPE_infile, outfile):
    text = [[w[0] for w in line] for line in new_text]
    with open(BPE_infile, "r", encoding="utf-8") as f:
        bpe = f.readlines()
        new_file = []
        for n, line in enumerate(bpe):
            line_no_bpe = re.sub("@@ ", "", line)
            list_no_bpe = line_no_bpe.split()
            list_with_bpe = line.split()
            if list_no_bpe != text[n]:
                print("LINES DON'T MATCH!", line_no_bpe, text[n]) # sanity check
                break
            bpe_line = []
            counter = 0
            for word in list_with_bpe:
                bpe_line.append((word, new_text[n][counter][1], new_text[n][counter][2]))
                if word[-2:] != "@@":
                    counter += 1
            new_file.append(bpe_line)
    text_out(new_file, outfile)
    #return new_file
