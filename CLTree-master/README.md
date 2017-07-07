Clustering through Decision Tree Construction:

This code has been tested under ubuntu 14.

Software dependency:
Graphviz
installation command under ubuntu: #apt-get install graphviz

Module dependency:
pydot     // please install graphviz before pydot
numpy

usage and configuration:
Please change data in Constant.py to make configuration.
CACHEDIR = "test/"
    The directory that stores programme intermediate results and cltree picture.

OUTPUTPNG = CACHEDIR + "/cltree.png"
    The picture that stores cltree results.

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

How to run the programme?
cltree.py is the main programme, just run #python cltree.py