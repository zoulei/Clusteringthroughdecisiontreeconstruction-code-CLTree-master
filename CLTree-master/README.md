Clustering through Decision Tree Construction:

This code has been tested under ubuntu 14.

Software dependency:
Graphviz
// Installation command under ubuntu: #apt-get install graphviz.
// If you do not need to store cltree results as image, graphviz is not needed.

Module dependency:
pydot
// Please install graphviz before pydot.
// If you do not need to store cltree results as image, pydot is not needed.
numpy

usage and configuration:
Please change data in Constant.py to make configuration.
CACHEDIR = "cache/"
    The directory that stores programme intermediate results and cltree picture.

OUTPUTPNG = CACHEDIR + "/cltree.png"
    The picture that stores cltree results.

OUTPUTTXT = CACHEDIR + "/cltree.txt"
    The file that stores cltree text results.

SCHEMAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/schema.csv"
    Specify the format of data.
    This file contains three lines. The first line specifies the name of attributes and KPI,
    the second line specifies the data type of each attribute and KPI, the third line
    specifies the attributes that is to be ignored and which attribute is kPI.
    Under "example data" directory, there is a example.

DATAFNAME = "/mnt/mfs/users/zoul15/SRTdata/sparknewdata/example.csv.tab"
    Input data file.
    Each line contains a data, and each attribute is seperated by tab.
    Under "example data" directory, there is a example.

DRAWIMAGE = False
    Weather to draw cltree.
    If graphviz and pydot are not installed, this parameter must be set to be False.

How to run the programme?
cltree.py is the main programme, just run #python cltree.py