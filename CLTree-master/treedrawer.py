from build import CLNode
import Queue
# import pydot
import trandt
import Constant

if Constant.DRAWIMAGE:
    import pydot

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
    ofile = open(Constant.CACHEDIR+"/tmpf","w")
    ofile.write("digraph G {\n")
    # try:
    # ofile.write(writestr)
    # except:
    print writestr[:51]

    print ofile
    ofile.write(writestr.decode("utf-8").encode("utf-8"))
    ofile.write("}")
    ofile.close()


    (graph,) = pydot.graph_from_dot_file(Constant.CACHEDIR + '/tmpf')
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


def drawABtestTree(root):
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
    avgdensity = root.getdensity()
    avgarea = root.getarea()

    leafinfo = {}
    leafnode = []

    while not nodequeue.empty():
        curnode = nodequeue.get()
        idx += 1

        rulllist = curnode.fetchfullrawsplitrull()
        # print rulllist
        # rawdatainfo = calABtestdata(schemafname,datafname,rulllist)
        # print "==========="
        # pp.pprint(rawdatainfo)
        # print "-------------"
        # pp.pprint(rulllist)
        # if "slow" in rawdatainfo:
        #     print "aaa"
        # print "bbb:",rawdatainfo.keys(),targetcls,
        # targetclsrate = rawdatainfo[targetcls] * 1.0 / (sum(rawdatainfo.values()) - rawdatainfo["total"])
        # includedata = (sum(rawdatainfo.values()) - rawdatainfo["total"]) * 1.0 / rawdatainfo["total"]

        print "node: ",curnode.getNrInstancesInNode(),curnode.attribute,curnode.value,curnode.direction,curnode.depth

        datalen = curnode.dataset.length()
        rd =  curnode.getRelativeDensity()
        # nodestr = "WT:" + str(int(datalen*1.0/root.dataset.length()*100)) + "%\\nRD:" + str(rd) + "\\n" + targetcls + "%:" \
        #           + str(round(targetclsrate * 100,1)) + "%\\nEP:" + str(round(includedata*100,1) )+"%\\n" \
        #             + "DT:" + str(curnode.getdensity())
        nodestr = "WT:" + str(int(datalen*1.0/root.dataset.length()*100)) +"%\\n" \
                    + "DT:" + str("{:.2e}".format(curnode.getdensity()))
        if curnode.attribute:
            nodestr = curnode.attribute + "\\n" + nodestr
        # addnode = pydot.Node(nodestr)
        # graph.add_node(addnode)

        if not curnode.isPrune():
            shape = "rectangle"
        else:
            shape = "box"

        writeline = "\"" + str(idx) + "\"" + "[ shape=" + shape + " label=\"" + nodestr + "\"]" + "\n"
        writestr += writeline
        if not curnode.attribute:
            # leaf
            densityrate = round(curnode.getdensity() / avgdensity,1)
            nodestr += "\\n" +  str( densityrate) + " X AVG"
            writeline = "\"" + str(idx+1000) + "\"" + "[ shape=" + shape + " label=\"" + nodestr + "\"]" + "\n"
            writestr += writeline
            leafinfo[idx+1000] = densityrate
            leafnode.append([densityrate,curnode])

        if curnode in parmap:
            parnode = curnode.parent
            if parnode.dataset.attr_type(parnode.attribute) == float:
                if curnode.direction == "l":
                    splitstr = "<= "+ str(parnode.value)
                else:
                    splitstr = "> "+ str(parnode.value)
            elif parnode.dataset.attr_type(parnode.attribute) == int:
                realvalue = trandict[parnode.attribute][parnode.value]
                if curnode.direction == "l":
                    splitstr = realvalue
                else:
                    splitstr = "NOT "+ realvalue
            else:
                # try:
                max,min = curnode.getperiodicalrange(parnode.attribute)
                splitstr = "[" + str(max) + "," + str(min) + "]"
                # except:
                #     print "--------------------"
                #     print parnode.dataset.attr_type(parnode.attribute)
                #     print parnode.attribute
                #     raise

                # splitstr.encode("utf-8")
            # addedge = pydot.Edge(parmap[curnode],addnode,label=splitstr)
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

    leafinfolist = leafinfo.items()
    leafinfolist.sort(key=lambda v:v[1])
    for i in xrange(len(leafinfolist) - 1):
        if leafinfolist[i + 1][1] >= 1.5 and leafinfolist[i][1] < 1.5:
            splitstr = "1.5x AVG = " + str("{:.2e}".format(1.5*avgdensity))
        else:
            splitstr = ""
        writeline = "\""+ str(leafinfolist[i + 1][0]) + "\" -> \"" + str(leafinfolist[i][0]) + "\" [ label=\"" + splitstr + "\" ]" + "\n"
        writestr += writeline

    ofile = open("tmpf","w")
    ofile.write("digraph G {\n")
    # try:
    # ofile.write(writestr)
    # except:
    ofile.write(writestr.decode("utf-8").encode("utf-8"))
    ofile.write("}")
    ofile.close()

    if Constant.DRAWIMAGE:
        (graph,) = pydot.graph_from_dot_file('tmpf')
        graph.write_png(Constant.OUTPUTPNG)

    leafnode.sort(key=lambda v:v[0],reverse=True)
    wline = ""
    wline += "------------------------------------------------------\n"*3
    wline += "-------------------------result-----------------------\n"
    wline += "------------------------------------------------------\n"*3
    wline += "\nAVG density is : "+str(avgdensity)+"\n"
    for dt, node in leafnode:
        wline += "-------------------------\n"
        wline += pp.pformat(node.fetchrawcombinedrull())+"\n"
        wline += "Weight : "+str(int(node.dataset.length()*1.0/root.dataset.length()*100))+"%\n"
        wline += "Density : "+str("{:.2e}".format(node.getdensity()))+"\n"
        wline += "Density is " + str( round(node.getdensity() / avgdensity,1)) + " times of AVG\n"
        wline += "Area : " + str("{:.2e}".format(node.getarea()))+"\n"
        wline += "Area is " + str( round(node.getarea() / avgarea,1)) + " times of AVG\n"
    print wline
    file = open(Constant.OUTPUTTXT,"w")
    file.write(wline)
    file.close()

def drawtest():
    (graph,) = pydot.graph_from_dot_file('tmpf')
    graph.write_png('somefile.png')

if __name__ == "__main__":
    drawtest()