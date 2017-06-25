import copy

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
            return

    def dotestfornode(self,node):
        rulldict = node.fetchcombinedrull()
        generaterulllist = self.generaterulls(rulldict)

        attrkeys = rulldict.keys()
        attrkeys.sort()

        for attr, generaterull in zip(attrkeys,generaterulllist):
            if attr == float:
                minvalue = node.dataset.get_min(attr)
                maxvalue = node.dataset.get_max(attr)
                rawlength = self.calculatenumericallength(rulldict[attr],minvalue,maxvalue)
