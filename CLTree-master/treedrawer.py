from build import CLNode
import Queue
import pydot
import trandt
import Constant
# class drawer():
def draw( root):
    graph = pydot.Dot(graph_type='digraph')

    parmap = {}

    trandict = trandt.readreversedict(Constant.TRANFILE)

    nodequeue = Queue.Queue()
    nodequeue.put(root)
    while not nodequeue.empty():
        curnode = nodequeue.get()

        print "node: ",curnode.getNrInstancesInNode(),curnode.attribute,curnode.value,curnode.direction,curnode.depth

        datalen = curnode.dataset.length()
        rd =  curnode.getRelativeDensity()
        nodestr = str(datalen) + "\n" + str(rd)
        if curnode.attribute:
            nodestr = curnode.attribute + "\n" + nodestr
        addnode = pydot.Node(nodestr)
        graph.add_node(addnode)

        if curnode in parmap:
            parnode = curnode.parent
            if parnode.dataset.attr_type(parnode.attribute) == float:
                if curnode.direction == "l":
                    splitstr = "<= "+ str(parnode.value)
                else:
                    splitstr = "> "+ str(parnode.value)
            else:
                realvalue = trandict[parnode.attribute][parnode.value]
                if parnode.direction == "l":
                    splitstr = realvalue
                else:
                    splitstr = "NOT "+ realvalue
            addedge = pydot.Edge(parmap[curnode],addnode,label=splitstr)

            graph.add_edge(addedge)

        if curnode.isPrune():
            continue
        else:
            for chnode in curnode.getChildNodes():
                parmap[chnode] = addnode
                nodequeue.put(chnode)

    graph.write_png("example.png")

def draw1( root):

    parmap = {}

    trandict = trandt.readreversedict(Constant.TRANFILE)

    idx = 0

    writestr = ""

    nodequeue = Queue.Queue()
    nodequeue.put(root)
    while not nodequeue.empty():
        curnode = nodequeue.get()
        idx += 1

        print "node: ",curnode.getNrInstancesInNode(),curnode.attribute,curnode.value,curnode.direction,curnode.depth

        datalen = curnode.dataset.length()
        rd =  curnode.getRelativeDensity()
        nodestr = "WT:" + str(int(datalen*1.0/root.dataset.length()*100)) + "%\\nRD:" + str(rd)
        if curnode.attribute:
            nodestr = curnode.attribute + "\\n" + nodestr
        addnode = pydot.Node(nodestr)
        # graph.add_node(addnode)

        if not curnode.isPrune():
            shape = "rectangle"
        else:
            shape = "box"

        writeline = "\"" + str(idx) + "\"" + "[ shape=" + shape + " label=\"" + nodestr + "\"]" + "\n"
        writestr += writeline

        if curnode in parmap:
            parnode = curnode.parent
            if parnode.dataset.attr_type(parnode.attribute) == float:
                if curnode.direction == "l":
                    splitstr = "<= "+ str(parnode.value)
                else:
                    splitstr = "> "+ str(parnode.value)
            else:
                realvalue = trandict[parnode.attribute][parnode.value]
                if curnode.direction == "l":
                    splitstr = realvalue
                else:
                    splitstr = "NOT "+ realvalue
                # splitstr.encode("utf-8")
            addedge = pydot.Edge(parmap[curnode],addnode,label=splitstr)
            # str(parmap[curnode]).encode("utf-8")
            # parmap[curnode].encode("utf-8")
            writeline ="\""+ str(parmap[curnode]) + "\" -> \"" + str(idx) + "\" [ label=\"" + splitstr + "\" ]" + "\n"
            writestr += writeline
            # graph.add_edge(addedge)

        if curnode.isPrune():
            continue
        else:
            for chnode in curnode.getChildNodes():
                parmap[chnode] = idx
                nodequeue.put(chnode)
    ofile = open("tmpf","w")
    ofile.write("digraph G {\n")
    # try:
    # ofile.write(writestr)
    # except:
    print writestr[:51]

    print ofile
    ofile.write(writestr.decode("utf-8").encode("utf-8"))
    ofile.write("}")
    ofile.close()

    (graph,) = pydot.graph_from_dot_file('tmpf')
    graph.write_png(Constant.OUTPUTPNG)

    # graph.write_png("example.png")

def calABtestdata(schemafname, datafname, rulllist):
    file = open(schemafname)
    headerline = file.readline()
    headerline=headerline.lower()
    typeline = file.readline()
    classline = file.readline()
    header = headerline.strip().split("\t")
    headerdict = dict(zip(header,range(len(header))))
    classdata = classline[:-1].split("\t")
    classidx = classdata.index("class")
    file.close()

    file = open(datafname)
    clscounter = {}
    total = 0
    for line in file:
        data = line.strip().split("\t")
        total += 1
        # if len(rulllist) == 5:
        #     print line
        for splittype,splitattr,splitvalue,direction in rulllist:
            realvalue = data[headerdict[splitattr]]
            if direction == "l":
                if splittype == float:
                    realvalue = float(realvalue)
                    if realvalue <= splitvalue:
                        # if len(rulllist) == 5:
                        #     print "continue"
                        continue
                    else:
                        # if len(rulllist) == 5:
                        #     print "break"
                        break
                else:
                    if realvalue == splitvalue:
                        continue
                    else:
                        # if len(rulllist) == 5:
                        #     print "break1"
                        break
            else:
                if splittype == float:
                    realvalue = float(realvalue)
                    if realvalue <= splitvalue:
                        # if len(rulllist) == 5:
                        #     print "break2"
                        break
                    else:
                        continue
                else:
                    if realvalue == splitvalue:
                        # if len(rulllist) == 5:
                        #     print "break3"
                        break
                    else:
                        continue
        else:
            cls = data[classidx]
            if cls not in clscounter:
                clscounter[cls] = 0
            clscounter[cls] += 1
    clscounter["total"] = total

    return clscounter


def drawABtestTree(root, schemafname, datafname):
    parmap = {}

    trandict = trandt.readreversedict(Constant.TRANFILE)

    idx = 0

    writestr = ""

    # file = open(schemafname)
    # headerline = file.readline()
    # headerline = headerline.lower()
    # typeline = file.readline()
    # classline = file.readline()
    # header = headerline.strip().split("\t")
    # # headerdict = dict(zip(header,range(len(header))))
    # classdata = classline[:-1].split("\t")
    # classidx = classdata.index("class")
    # file.close()
    #
    # classheader = header[classidx]
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(trandict)
    # print classheader
    # print root.dataset.class_names[0]
    targetcls = root.dataset.class_names[0]

    nodequeue = Queue.Queue()
    nodequeue.put(root)
    while not nodequeue.empty():
        curnode = nodequeue.get()
        idx += 1

        rulllist = curnode.fetchfullrawsplitrull()
        # print rulllist
        rawdatainfo = calABtestdata(schemafname,datafname,rulllist)
        print "==========="
        pp.pprint(rawdatainfo)
        print "-------------"
        pp.pprint(rulllist)
        # if "slow" in rawdatainfo:
        #     print "aaa"
        # print "bbb:",rawdatainfo.keys(),targetcls,
        targetclsrate = rawdatainfo[targetcls] * 1.0 / (sum(rawdatainfo.values()) - rawdatainfo["total"])
        includedata = (sum(rawdatainfo.values()) - rawdatainfo["total"]) * 1.0 / rawdatainfo["total"]

        print "node: ",curnode.getNrInstancesInNode(),curnode.attribute,curnode.value,curnode.direction,curnode.depth

        datalen = curnode.dataset.length()
        rd =  curnode.getRelativeDensity()
        nodestr = "WT:" + str(int(datalen*1.0/root.dataset.length()*100)) + "%\\nRD:" + str(rd) + "\\n" + targetcls + "%:" \
                  + str(round(targetclsrate * 100,1)) + "%\\nEP:" + str(round(includedata*100,1) )+"%\\n" \
                    + "DT:" + str(curnode.getdensity())
        if curnode.attribute:
            nodestr = curnode.attribute + "\\n" + nodestr
        addnode = pydot.Node(nodestr)
        # graph.add_node(addnode)

        if not curnode.isPrune():
            shape = "rectangle"
        else:
            shape = "box"

        writeline = "\"" + str(idx) + "\"" + "[ shape=" + shape + " label=\"" + nodestr + "\"]" + "\n"
        writestr += writeline

        if curnode in parmap:
            parnode = curnode.parent
            if parnode.dataset.attr_type(parnode.attribute) == float:
                if curnode.direction == "l":
                    splitstr = "<= "+ str(parnode.value)
                else:
                    splitstr = "> "+ str(parnode.value)
            else:
                realvalue = trandict[parnode.attribute][parnode.value]
                if curnode.direction == "l":
                    splitstr = realvalue
                else:
                    splitstr = "NOT "+ realvalue
                # splitstr.encode("utf-8")
            addedge = pydot.Edge(parmap[curnode],addnode,label=splitstr)
            # str(parmap[curnode]).encode("utf-8")
            # parmap[curnode].encode("utf-8")
            writeline ="\""+ str(parmap[curnode]) + "\" -> \"" + str(idx) + "\" [ label=\"" + splitstr + "\" ]" + "\n"
            writestr += writeline
            # graph.add_edge(addedge)

        if curnode.isPrune():
            continue
        else:
            for chnode in curnode.getChildNodes():
                parmap[chnode] = idx
                nodequeue.put(chnode)
    ofile = open("tmpf","w")
    ofile.write("digraph G {\n")
    # try:
    # ofile.write(writestr)
    # except:
    print writestr[:51]

    print ofile
    ofile.write(writestr.decode("utf-8").encode("utf-8"))
    ofile.write("}")
    ofile.close()

    (graph,) = pydot.graph_from_dot_file('tmpf')
    graph.write_png(Constant.ABTESTPNG)


def drawtest():

    (graph,) = pydot.graph_from_dot_file('tmpf')
    graph.write_png('somefile.png')

if __name__ == "__main__":
    drawtest()