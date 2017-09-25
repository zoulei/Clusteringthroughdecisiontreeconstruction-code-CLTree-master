import trandt
import Constant

def printvaluerange():
    trandict = trandt.readtrandict(Constant.TRANFILE)
    for key, subtrandict in trandict.items():
        print "="*10,key,"="*10
        print subtrandict.keys()

    for key, subtrandict in trandict.items():
        print key,":\t",len(subtrandict.keys())

if __name__ == "__main__":
    printvaluerange()