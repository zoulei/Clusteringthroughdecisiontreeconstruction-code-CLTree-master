from __future__ import print_function
import json
import Constant

SEP = "\t"

def gettrandict(headfname ,fname, ofile):
    file = open(headfname)
    header = file.readline()
    header = header.lower()
    datatype = file.readline()
    ignore = file.readline()

    header = header.strip().split(SEP)
    datatype = datatype.strip().split(SEP)
    ignore = ignore[:-1].rstrip().split(SEP)
    file.close()

    file = open(fname)
    trandict = {}

    for title, dtp in zip(header,datatype):
        if dtp == "d":
            trandict[title] = {}

    idx1 = 0
    for line in file:
        data = line.strip().split(SEP)
        idx1 += 1
        # print "idx1:",idx1
        # print len(datatype)
        # print len(data)
        # print line.split(SEP)
        for idx in xrange(len(data)):
            try :
                if datatype[idx] == "c":
                    continue
                value = data[idx]
                if value == "":
                    value = "None"
                title = header[idx]
                trandict[title][value] = 1

            except:
                print ("read data error, error occurs in line:",idx1)
                print ("the content of this line is:",line)
                print ("parse result is:",line.split(SEP))
                # raise
    file.close()




    for key in trandict:
        subtran = trandict[key]
        valuelist = subtran.keys()
        for idx,value in enumerate(valuelist):
            subtran[value] = idx + 1

    print ("trandict:")
    print (trandict)

    file = open(fname)
    line = file.readline()
    data = line.strip().split(SEP)
    print("=" * 100, ignore)
    clsidx = ignore.index("class")

    try:
        cls = data[clsidx]
    except:
        print (line)
        print (data)
        print (clsidx)
        print (len(data))
        raise

    file.close()
    ofile = open(ofile,"w")

    print ("ignore:",ignore)
    print ("header:",header)
    print ("datatype:",datatype)

    for idx in xrange(len(header)):
        title = header[idx]
        dtp = datatype[idx]
        ign = ignore[idx]
        if dtp == "d":
            writeline = "@attribute "+ title +" cat"
        else:
            writeline = "@attribute "+ title +" numeric"
        if ign == "class":
            writeline = "@attribute class {"+cls+"}"
        if ign == "i":
            continue
        ofile.write(writeline+"\n")
    ofile.write("@data\n")

    attrlen = ignore.index("class")

    file = open(fname)
    for line in file:
        data = line.strip().split(SEP)

        data = data[:attrlen + 1]
        label = data[-1]
        # if label == "fast":
        #     continue

        for idx in xrange(len(data) - 1):
            title = header[idx]
            if datatype[idx] == "c":
                continue
            elif datatype[idx] == "d":
                if data[idx] == "":
                    data[idx] = "None"
                data[idx] = trandict[title][data[idx]]

        data = [str(v) for v in data]
        writeline = ",".join(data) + "\n"
        ofile.write(writeline)

    file.close()

    return trandict

def savetrandict(fname,trandict):
    file = open(fname,"w")
    print(trandict,file=file)
    file.close()

def readtrandict(fname):
    file = open(fname)
    exec('tempdict='+file.readline())
    file.close()
    return tempdict

def reversedict(trandict):
    reversetran = {}
    for key in trandict:
        if key not in reversetran:
            reversetran[key] = {}
        for value,order in trandict[key].items():
            reversetran[key][order] = value
    return reversetran

def readreversedict(fname):
    return reversedict(readtrandict(fname))

def trandata(schema,rawfile,targetfile,dictfile):
    trandict = gettrandict(schema,rawfile,targetfile)

    import pprint
    pp = pprint.PrettyPrinter(indent= 4)
    pp.pprint(trandict)

    savetrandict(dictfile,trandict)

    trandict = readtrandict(dictfile)
    # import pprint
    # pp = pprint.PrettyPrinter(indent= 4)
    pp.pprint(trandict)

def tranSRT():
    trandata("/mnt/mfs/users/zoul15/SRTdata/sparknewdata/schema.csv",
                           "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/example.csv.tab",
                           "/home/zoul15/cltree/CLTree/test/srt.arff",
                "/home/zoul15/cltree/CLTree/test/srttrandict")

def trandidierror():
    trandata("/mnt/mfs/users/zoul15/didierrordata/focusdata/schema.csv",
                           "/mnt/mfs/users/zoul15/didierrordata/focusdata/sampleddata.log",
                           "/home/zoul15/cltree/CLTree/test/didierror.arff",
                "/home/zoul15/cltree/CLTree/test/didierrortrandict")

def tranfulldidierror():
    trandata("/mnt/mfs/users/zoul15/didierrordata/focusdata/schema.csv",
                           "/mnt/mfs/users/zoul15/didierrordata/focusdata/combo-web_20161213_0.log",
                           "/home/zoul15/cltree/CLTree/test/didifullerror.arff",
                "/home/zoul15/cltree/CLTree/test/didifullerrortrandict")

def tranfatadidierror():
    trandata("/mnt/mfs/users/zoul15/didierrordata/focusdata/schema.csv",
                           "/mnt/mfs/users/zoul15/didierrordata/focusdata/fata.log",
                           "/home/zoul15/cltree/CLTree/test/fata.arff",
                "/home/zoul15/cltree/CLTree/test/didifataerrortrandict")

def tranfatahostdidierror():
    trandata("/mnt/mfs/users/zoul15/didierrordata/focusdata/schema.csv",
                           "/mnt/mfs/users/zoul15/didierrordata/focusdata/fatafilterhost.log",
                           "/home/zoul15/cltree/CLTree/test/fatafilterhost.arff",
                "/home/zoul15/cltree/CLTree/test/fatahosttrandict")

def tranloan():
    trandata("/mnt/mfs/users/zoul15/paipaidai/focusdata/schema.csv",
                           "/mnt/mfs/users/zoul15/paipaidai/focusdata/LC.csv",
    # trandata("F:/myfile/file/undergraduate research/paipaidai/ppd/data/focusdata/schema.csv",
    #          "F:/myfile/file/undergraduate research/paipaidai/ppd/data/focusdata/LC.csv",
                           Constant.CLTREEHOME+"test/loan.arff",
                Constant.CLTREEHOME+"test/loandict")

def tranwebbrowsing():
    trandata("/mnt/mfs/users/zoul15/webbrowsingdata/focusdata/schema.csv",
                           "/mnt/mfs/users/zoul15/webbrowsingdata/focusdata/webbrowsingper.csv",
    # trandata("F:/myfile/file/undergraduate research/webbrowsing/focusdata/schema.csv",
    #          "F:/myfile/file/undergraduate research/webbrowsing/focusdata/webbrowsingper.csv",
                           Constant.CLTREEHOME+"test/webbrowsing.arff",
                Constant.CLTREEHOME+"test/webbrowsingdict")

def trancreditclient():
    # trandata("/mnt/mfs/users/zoul15/creditclient/focusdata/schema.csv",
    #                        "/mnt/mfs/users/zoul15/creditclient/focusdata/UCI_Credit_Card.csv",
    trandata("F:/myfile/file/undergraduate research/creditcardclient/default-of-credit-card-clients-dataset/focusdata/schema.csv",
             "F:/myfile/file/undergraduate research/creditcardclient/default-of-credit-card-clients-dataset/focusdata/UCI_Credit_Card.csv",
                           Constant.CLTREEHOME+"test/creditclient.arff",
                Constant.CLTREEHOME+"test/creditclientdict")

if __name__ == "__main__":
    # trancreditclient()
    # tranwebbrowsing()
    tranSRT()