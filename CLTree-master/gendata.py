# import Constant
import random
import sys

def gendata(size):
    ifile = open(Constant.SEEDFNAME)
    ofile = open(Constant.DATAFNAME,"w")
    seeddata = []
    for line in ifile:
        seeddata.append(line.strip().split("\t"))
    ifile.close()
    for _ in xrange(size):
        idx = random.randint(0,len(seeddata) -1)
        seed = seeddata[idx]
        newdata = []
        for value in seed[:-1]:
            newdata.append(str(float(value) + random.uniform(-4,4)))
        newdata.append(seed[-1])
        # print newdata
        ofile.write("\t".join(newdata)+"\n")
    ofile.close()

def gendataforrawcltree(size):
    ifile = open("rawtest/D05.arff")
    ofile = open("rawtest/newD05.arff","w")
    for _ in xrange(8):
        ofile.write(ifile.readline())
    seeddata = []
    for line in ifile:
        seeddata.append(line.strip().split(","))
    ifile.close()
    for _ in xrange(size):
        idx = random.randint(0,len(seeddata) -1)
        seed = seeddata[idx]
        newdata = []
        for value in seed[:-1]:
            newdata.append(str(float(value) + random.uniform(-4,4)))
        newdata.append(seed[-1])
        # print newdata
        ofile.write(",".join(newdata)+"\n")
    ofile.close()

def genperiodicaldata(size):
    ofile = open("rawtest/newD05.csv","w")
    for _ in xrange(size / 2):
        x = random.uniform(0,3)
        y = random.uniform(0,10)
        ofile.write("\t".join([str(x),str(y)])+"\n")
    for _ in xrange(size / 2):
        x = random.uniform(7,10)
        y = random.uniform(0,10)
        ofile.write("\t".join([str(x),str(y)])+"\n")
    ofile.close()

if __name__ == "__main__":
    genperiodicaldata(int(sys.argv[1]))