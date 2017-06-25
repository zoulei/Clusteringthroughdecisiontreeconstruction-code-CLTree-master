import copy
import numpy as np

class ABTest:
    def __init__(self,root):
        self.m_root = root

    def generaterulls(self,rulldict):

        attrkeys = rulldict.keys()
        attrkeys.sort()

        generaterulllist = []
        for attr in attrkeys:
            generaterulldict = copy.deepcopy(rulldict)
            if self.root.dataset.getAttrType(attr) == float:
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
        # elif bounddict["upper"] >= bounddict["lower"]:
        #     data = data[data[:,idx]>bounddict["lower"]]
        #     return data[data[:,idx]<=bounddict["upper"]]
        else:
            data = data[data[:,idx]>bounddict["lower"]]
            return data[data[:,idx]<=bounddict["upper"]]

    def filterbycategoricalfeature(self, data, idx , bounddict):
        if "is" in bounddict:
            return data[data[:,idx] in bounddict["is"]]
        else:
            return data[data[:,idx] not in bounddict["not"]]

    def dotestfornode(self,node):
        rulldict = node.fetchcombinedrull()
        generaterulllist = self.generaterulls(rulldict)

        attrkeys = rulldict.keys()
        attrkeys.sort()

        for attr, generaterull in zip(attrkeys,generaterulllist):
            if self.m_root.dataset.getAttrType(attr) == float:
                minvalue = node.dataset.get_min(attr)
                maxvalue = node.dataset.get_max(attr)
                rawlength = self.calculatenumericallength(rulldict[attr],minvalue,maxvalue)
                generatelength = self.calculatenumericallength(generaterull[attr],minvalue,maxvalue)
            else:
                rawrange = self.m_root.get_range(attr)
                rawlength = self.calculatecategoricallength(rulldict[attr],rawrange)
                generatelength = self.calculatecategoricallength(generaterull[attr],rawrange)

            generatearray = np.copy(self.m_root.dataset)
            for curattr, bounddict in generaterull:
                idx = self.m_root.dataset.attr_idx[curattr]
                if self.m_root.dataset.getAttrType(curattr) == float:
                    generatearray = self.filterbynumericalfeature(generatearray,idx,bounddict)
                else:
                    generatearray = self.filterbycategoricalfeature(generatearray,idx,bounddict)