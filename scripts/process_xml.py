import xml.etree.ElementTree as et
import xmltodict
import re
#import collections
import glob

def xml_to_dict(filename="./Rag2019_xml_en_it/ins.xml"):
    with open(filename, encoding="utf-8") as f:
        doc = xmltodict.parse(f.read())
    return doc

def unpack_form(item, target="lemma"):
    lemlist = []
    for num_lem, form in enumerate(item.iter("formSct")):
        if form.findall("hom"):
            hom_num = "_" + form.find("hom").text
        else:
            hom_num = ""
        lemmas = form.findall(target) + form.findall("var")  # + form.findall("sublem")
        for lem in lemmas:
            lemlist.append(lem.text)
    return lemlist, hom_num

def unpack_sem_for_gr(item):
    grlist = []
    #trlist = ""
    for semSct in item.iter("semSct"):
        for gc in semSct.findall("gc"):
            for g in gc.iter("gr"):
                tail = g.tail
                if tail == " + ":
                    grlist.append(g.text + tail)
                else:
                    grlist.append(g.text)
            try:
                for pos, element in enumerate(grlist):
                    if element[-3:] == " + ":
                        grlist[pos] = grlist[pos] + grlist[pos + 1]
                        grlist.pop(pos + 1)
            except:
                pass
    return grlist

def unpack_sem_for_tr(item):
    trstring = ""
    for semSct in item.iter("semSct"):
        for gc in semSct.findall("gc"):
            for sns in gc.findall("sns"):
                for t in sns.iter("t"):
                    trstring += "".join(t.itertext()) + "; "
                #trstring = re.sub(" \(.*\)", "", trstring) # fix later for processing
                trlist = trstring.split("; ")
    return trlist


                # examples = []
                # for e in sns.findall(".//exg"):
                #     ex = e.find("ex").text
                #     ext = e.find("ext").text
                #     print(ex, ext)
                #     examples.append((ex.text, ext.text))
                # dic[lemlist[0] + hom_num]["examples"] = examples
                #

def unpack_xml(filename="./Rag2019_xml_{}/{}.xml", dir = "en_it", letter = "ins"):
    tree = et.parse(filename.format(dir, letter))
    root = tree.getroot()
    dic = {}
    for num_item,item in enumerate(root.iter("item")):
        lemlist, hom_num = unpack_form(item)[0],unpack_form(item)[1]
        dic[lemlist[0] + hom_num] = {"lemma": lemlist, "id": dir + "_" + letter + "_" + str(num_item)}
        dic[lemlist[0] + hom_num]["gramm"] = unpack_sem_for_gr(item)
        dic[lemlist[0] + hom_num]["trad"] = unpack_sem_for_tr(item)
    return dic



def make_list(object):
    myobject = []
    if isinstance(object, list):
        return object
    else:
        return myobject.append(object)

'''
def unpack_items(file="./Rag2019_xml_{}/{}.xml", dir="en_it", lett="ins"):
    print("Processing {}".format(file.format(dir,lett)))
    doc = xml_to_dict(file.format(dir,lett))
    return [item for item in doc["items"]["item"]]

def unpack_formSct(item): # one item of a list of items
    formScts = []
    for formSct in make_list(item["formSct"]):
        try:
            hom_num = "_" + formSct["hom"]
        except(KeyError):\
            hom_num = ""
        try:
            lemma = lemma = formSct["lemma"] + hom_num
        except(KeyError):
            lemma = None
        try:
            var = formSct["var"]
        except(KeyError):
            var = None
        try:
            sublem = formSct["sublem"]
        except(KeyError):
            sublem = None
        formScts.append([lemma, var, sublem])
    return formScts

def unpack_semSct(item): # one item of a list of items
    semSct = make_list(item["semSct"])
    semSct = semSct[0] # only takes first
    gramm = []
    #trad = []
    for gc in make_list(semSct["gc"]):
        try:
            gr = gc["grDiv"]["gr"]
        except:
            gr = None
        gramm.append(gr)
    return gramm

    #     for sns in make_list(gc["sns"]):
    #         for tdiv in make_list(sns["tDiv"]):
    #             try:
    #                 for t in make_list(tdiv["t"]):
    #                     trad.append(t)
    #             except:
    #                 trad.append(None)
    # return [gramm, trad]


def hash_xml(file="./Rag2019_xml_{}/{}.xml", dir="en_it", lett="ins"):
    dictionary = {}
    print("Processing {}".format(file.format(dir,lett)))
    doc = xml_to_dict(file.format(dir,lett))
    exceptions_lemma = []
    exceptions_gramm = []
    for pp,dd in enumerate(doc["items"]["item"]):
        id = "#{}&{}&{}".format(dir,lett,pp)
        #dictionary["id"] = {}
        for d in make_list(dd["formSct"]):
            try:
                h = "_" + d["hom"]
            except:
                h = ""
                pass
            try:
                lemma = d["lemma"] + h
                dictionary[lemma] = {"lemma": lemma, "id": id}
            except:
                exceptions_lemma.append((pp, dd))
                print("Lemma VAR? except ---->", pp,dd)

            try:
            for g in make_list(dd["semSct"]["gc"]):
                try:
                    conn = g["grDiv"]["#text"]
                except:
                    conn = ""
                    pass
                try: # FIX HERE
                    gramm = g["grDiv"]["gr"]
                    dictionary[id]["gramm"] = gramm
                    dictionary[id]["gramm_conn"] = conn
                except:
                    exceptions_gramm.append((pp, dd))
                    print("Lemma GRAMM except ---->", pp,dd)
                pass
        except:
            print("HELP", pp, lemma)
            pass
    '''
    # dictionary["EXC_lemma"] = exceptions_lemma
    # dictionary["EXC_gramm"] = exceptions_gramm
    # return dictionary

    #
    #     gramm = d["semSct"]["gc"]["grDiv"]["gr"]
    #             dictionary[lemma] = {"gramm": gramm}
    #
    #     try:
    #                 lemma = d["formSct"][0]["lemma"]
    #                 gramm = d["semSct"][0]["gc"]["grDiv"]["gr"]
    #                 dictionary[lemma] = {"gramm": gramm}
    #             except:
    #                 exceptions2.append((p,d))
    #                 print("Other EXCEPTION <<<<<<<<<<<<<<<<<<<<<<<<", p)
    #                 pass
    # dictionary["EXC"] = (exceptions1, exceptions2)

def new_parse_dict_for_mwes(dir="en_it", mwe_only=False):
    filelist = glob.glob("./Rag2019_xml_{}/*.xml".format(dir))
    dictionary = {}
    for file in filelist:
        print("Processing {}".format(file))
        doc = xml_to_dict(file)
        exceptions1 = []
        exceptions2 = []
        for p,d in enumerate(doc["items"]["item"]):
            try:
                #print("ALTRIGHT", d["formSct"]["lemma"], p)
                lemma = d["formSct"]["lemma"]
                gramm = d["semSct"]["gc"]["grDiv"]["gr"]
                dictionary[lemma] = {"gramm": gramm}
            except:
                exceptions1.append((p,d))
                print("Lemma EXCEPTION ----------------------------->", p)
                try:
                    lemma = d["formSct"][0]["lemma"]
                    gramm = d["semSct"][0]["gc"]["grDiv"]["gr"]
                    dictionary[lemma] = {"gramm": gramm}
                except:
                    exceptions2.append((p,d))
                    print("Other EXCEPTION <<<<<<<<<<<<<<<<<<<<<<<<", p)
                    pass
    dictionary["EXC"] = (exceptions1, exceptions2)
    if dir == "it_en": # nneded for diacritics transform
        new_mydict_it = {}
        for k, v in dictionary.items():
            n_k = k.replace("`", "").replace("̣", "").replace("̱", "").replace("´", "")
            new_mydict_it[n_k] = v
        return new_mydict_it
    else:
        return dictionary