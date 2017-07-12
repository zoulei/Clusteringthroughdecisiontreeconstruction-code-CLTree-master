
# ========== please change these parameters according to your own environment and data=======
CACHEDIR = "cache/"
OUTPUTPNG = CACHEDIR + "/cltree.png"
OUTPUTTXT = CACHEDIR + "/cltree.txt"
# SCHEMAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/schema.csv"
# DATAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/example.csv.tab"
SCHEMAFNAME = "example data/schema.csv"
DATAFNAME = "example data/example.csv.tab"
DRAWIMAGE = False

# ========== cltree parameters ======================
NODERATIOTHRE = 0.05
MINY = 1
MINRD = 70
MIN_NR_INSTANCES = 2


# ABTESTPNG = CACHEDIR + "/ABTEST_" + "SRT.png"


#RAWDATAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/20140922.csv.tab"
#RAWDATAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/20140922.csv.tab"

# ========== intermediate result ======================
TRANFILE = CACHEDIR + "/tmptrandict"
DATAFILE = CACHEDIR + "/tmp.arff"