
# ========== please change these parameters according to your own environment and data=======
CACHEDIR = "cache/"
OUTPUTPNG = CACHEDIR + "/cltree.png"
OUTPUTTXT = CACHEDIR + "/cltree.txt"
# SCHEMAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/schema.csv"
# DATAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/example.csv.tab"
# SCHEMAFNAME = "/mnt/mfs/users/zoul15/didierrordata/focusdata/notagschema.csv"
# DATAFNAME = "/mnt/mfs/users/zoul15/didierrordata/focusdata/samplednotagdata.log"
# SCHEMAFNAME = "/mnt/mfs/users/zoul15/airdata/schema.csv"
# DATAFNAME = "/mnt/mfs/users/zoul15/airdata/airline.csv.tab"
SCHEMAFNAME = "/mnt/mfs/users/zoul15/didiorder/focusdata/schema.csv"
DATAFNAME = "/mnt/mfs/users/zoul15/didiorder/focusdata/didiorder.csv"
# SCHEMAFNAME = "example data/schema.csv"
# DATAFNAME = "example data/example.csv.tab"
DRAWIMAGE = True

# ========== cltree parameters ======================
NODERATIOTHRE = 0.05
MININFORMATIONGAIN = 0.01
#RAWDATAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/20140922.csv.tab"
#RAWDATAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/20140922.csv.tab"

# ========== intermediate result ======================
TRANFILE = CACHEDIR + "/tmptrandict"
DATAFILE = CACHEDIR + "/tmp.arff"

# ===========  other ===============================
MINY = 1
MINRD = 100
MIN_NR_INSTANCES = 2