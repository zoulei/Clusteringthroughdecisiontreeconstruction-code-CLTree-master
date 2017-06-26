import copy
import numpy as np
import Queue
import pprint

class ABTest:
    def __init__(self,root):
        self.m_root = root

    def generaterulls(self,rulldict):

        attrkeys = rulldict.keys()
        attrkeys.sort()

        generaterulllist = []
        for attr in attrkeys:
            generaterulldict = copy.deepcopy(rulldict)
            if self.m_root.dataset.getAttrType(attr) == float:
                if "upper" not in generaterulldict[attr]:
                    generaterulldict[attr]["upper"] = generaterulldict[attr]["lower"]
                    del generaterulldict[attr]["lower"]
                elif "lower" not in generaterulldict[attr]:
                    generaterulldict[attr]["lower"] = generaterulldict[attr]["upper"]
                    del generaterulldict[attr]["upper"]
                else:
                    tmp = generaterulldict[attr]["upper"]
                    generaterulldict[attr]["upper"] = generaterulldict[attr]["lower"]
                    generaterulldict[attr]["lower"] = tmp
            else:
                if "not" not in generaterulldict[attr]:
                    generaterulldict[attr]["not"] = generaterulldict[attr]["is"]
                    del generaterulldict[attr]["is"]
                else:
                    generaterulldict[attr]["is"] = generaterulldict[attr]["not"]
                    del generaterulldict[attr]["not"]
            generaterulllist.append(generaterulldict)

        return generaterulllist

    def calculatenumericallength(self, bounddict, minvalue, maxvalue):
        if "lower" not in bounddict:
            length = bounddict["upper"] - minvalue
        elif "upper" not in bounddict:
            length = maxvalue - bounddict["lower"]
        else:
            length = bounddict["upper"] - bounddict["lower"]
        if length < 0:
            length += maxvalue - minvalue
        return length

    def calculatecategoricallength(self, bounddict, fullrange):
        if "is" in bounddict:
            length = len(bounddict["is"])
        else:
            length = len(fullrange) - len(bounddict["not"])

        return length

    def filterbynumericalfeature(self, data, idx, bounddict):
        if "lower" not in bounddict:
            return data[data[:,idx]<=bounddict["upper"]]
        elif "upper" not in bounddict:
            return data[data[:,idx]>bounddict["lower"]]
        else:
            return data[(data[:,idx]<=bounddict["upper"]) | (data[:,idx]>bounddict["lower"])]

    def filterbycategoricalfeature(self, data, idx , bounddict):
        filterarray = None
        if "is" in bounddict:
            for value in bounddict["is"]:
                if filterarray == None:
                    filterarray = data[:,idx] == value
                else:
                    filterarray = filterarray | (data[:,idx] == value)
        else:
            for value in bounddict["not"]:
                if filterarray == None:
                    filterarray = data[:,idx] != value
                else:
                    filterarray = filterarray & (data[:,idx] != value)
        return data[filterarray]

    def dotestfornode(self,node):
        rulldict = node.fetchcombinedrull()
        generaterulllist = self.generaterulls(rulldict)

        attrkeys = rulldict.keys()
        attrkeys.sort()

        ABtestresult = {}

        for attr, generaterull in zip(attrkeys,generaterulllist):
            if self.m_root.dataset.getAttrType(attr) == float:
                minvalue = self.m_root.dataset.get_min(attr)
                maxvalue = self.m_root.dataset.get_max(attr)
                rawlength = self.calculatenumericallength(rulldict[attr],minvalue,maxvalue)
                generatelength = self.calculatenumericallength(generaterull[attr],minvalue,maxvalue)
            else:
                rawrange = self.m_root.dataset.get_range(attr)
                rawlength = self.calculatecategoricallength(rulldict[attr],rawrange)
                generatelength = self.calculatecategoricallength(generaterull[attr],rawrange)

            # generatearray = np.copy(self.m_root.dataset.instance_values)
            generatearray = self.m_root.dataset.instance_values.view(dtype=float).reshape(self.m_root.dataset.length(),-1)
            for curattr, bounddict in generaterull.items():
                idx = self.m_root.dataset.attr_idx[curattr]
                # print "generatearray:"
                # print generatearray
                # print "curattr: ",curattr,len(generatearray),idx
                if self.m_root.dataset.getAttrType(curattr) == float:
                    generatearray = self.filterbynumericalfeature(generatearray,idx,bounddict)
                else:
                    generatearray = self.filterbycategoricalfeature(generatearray,idx,bounddict)

                print "substep:",curattr,len(generatearray)

            # print "test attr:",attr,rawlength,generatelength
            rawdensity = node.dataset.length() * 1.0 / rawlength
            generatedensity = len(generatearray) * 1.0 / generatelength

            print "length:",rawlength,generatelength
            print rawdensity,generatedensity,len(generatearray),node.dataset.length()

            generatedensity /= rawdensity

            ABtestresult[attr] = generatedensity

        return ABtestresult

    def dotest(self):
        nodequeue = Queue.Queue()
        nodequeue.put(self.m_root)

        pp = pprint.PrettyPrinter(indent=4)

        while not nodequeue.empty():
            curnode = nodequeue.get()

            if curnode.isPrune():
                print "==============================================="
                print "rawrule: "
                pp.pprint(curnode.fetchrawcombinedrull() )
                print "abtestresult: "
                pp.pprint(self.dotestfornode(curnode) )

            else:
                for chnode in curnode.getChildNodes():
                    nodequeue.put(chnode)
        print "#==============================================="