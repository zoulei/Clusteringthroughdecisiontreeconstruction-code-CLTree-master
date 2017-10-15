from arff import Data

from math import sqrt as sqrt

import numpy as np
import copy
import trandt
import Constant

def _relative_density(dataset):
    return float(dataset.length())/dataset.nr_virtual_points

def calculatenumericallength(bounddict, minvalue, maxvalue):
    if "lower" not in bounddict:
        length = bounddict["upper"] - minvalue
    elif "upper" not in bounddict:
        length = maxvalue - bounddict["lower"]
    else:
        length = bounddict["upper"] - bounddict["lower"]
    if length < 0:
        length += maxvalue - minvalue
    return length

def calculatecategoricallength(bounddict, fullrange):
    if "is" in bounddict:
        length = len(bounddict["is"])
    else:
        length = len(fullrange) - len(bounddict["not"])

    return length

class BuildTree(object):
    def __init__(self, min_split, min_infogame = -100):
        self.cutCreator = InfoGainCutFactory(min_split, min_infogame)
        self.datasetSplitter = DatasetSplitter()                        
        self.root = None
            
    def build(self, dataset):
        self._build_tree(dataset, None, 0)        
        return self.root

    def _build_tree(self, dataset, parent, depth, direction = ""):
        bestCut = self._findBestCut(dataset)

        # if bestCut:
        #     print "bstcut: ",bestCut.attribute," : ",bestCut.value,self.cutCreator.min_split

        attribute = "" if bestCut is None else bestCut.attribute

        if bestCut is None:
            dt_node = CLNode(dataset, parent, attribute, depth, direction, 0)
        else:
            dt_node = CLNode(dataset, parent, attribute, depth, direction, bestCut.value)
        if parent: parent.addChildNode(dt_node)
        if self._isRootNode(depth): self.root = dt_node
        
        if bestCut is None:
            return
        print "bestCut:",bestCut.attribute,bestCut.value
        lhs_dataset, rhs_dataset = self._splitDatasetUsingBestCut(dataset, bestCut)
        
        #self._plotCut(bestCut, dataset, lhs_dataset, rhs_dataset)
        # if depth == 1:
        #     return
        if lhs_dataset.length() > 0:
            self._build_tree(lhs_dataset, dt_node, (depth+1),"l")
        if rhs_dataset.length() > 0:
            self._build_tree(rhs_dataset, dt_node, (depth+1),"r")
            
            
    def _isRootNode(self, depth):
        if depth==0 and self.root is None: return True
        
    def _splitDatasetUsingBestCut(self, dataset, bestCut):
        attrtype = dataset.attr_types_dict[bestCut.attribute]
        if attrtype == float:

            dataset.sort(bestCut.attribute)
            idx = dataset.getInstanceIndex(bestCut.inst_id)
            lhs_set, rhs_set = self.datasetSplitter.split(dataset, bestCut.attribute, bestCut.value, idx)

            # for attribute in dataset.attr_names:
            #     if attribute == bestCut.attribute:
            #         continue
            #     if dataset.attr_types_dict[attribute] == "float":
            #         minVal = dataset.get_min(attribute)
            #         maxVal = dataset.get_max(attribute)
            #         lhs_set.set_min(attribute, minVal)
            #         lhs_set.set_max(attribute, maxVal)
            #         rhs_set.set_min(attribute, minVal)
            #         rhs_set.set_max(attribute, maxVal)
            #     else:
            #         attrrange = copy.deepcopy(dataset.get_range(attribute))
            #         lhs_set.set_range(attribute,attrrange)
            #         rhs_set.set_range(attribute,attrrange)

            # return lhs_set, rhs_set
        elif attrtype == int:
            lhs_set, rhs_set = self.datasetSplitter.splitCat(dataset, bestCut.attribute, bestCut.value)
        else:
            attr = bestCut.attribute
            peri = dataset.getperiod(attr)
            if not dataset.isattrsplitted():
                newdataset = self._generatenumericaldataset(dataset, attr, bestCut.m_splitpoint)
            else:
                newdataset = self._generatenumericaldataset(dataset, attr)
                    # treat as numerical
            idx = newdataset.getInstanceIndex(bestCut.inst_id)
            lhs_set, rhs_set = self.datasetSplitter.split(newdataset, attr, bestCut.value, idx)

            lhs_set.setperiodicalinfo(dataset)
            rhs_set.setperiodicalinfo(dataset)
            if not dataset.isattrrevrsered(attr) and dataset.isattrsplitted(attr):
                # numerical
                # lhs_set.setperiodicalinfo(dataset)
                # rhs_set.setperiodicalinfo(dataset)
                pass
            elif dataset.isattrrevrsered(attr) and dataset.isattrsplitted(attr):
                # reversed numerical
                if lhs_set.get_max(attr) <= lhs_set.get_rootmax(attr):
                    lhs_set.m_reversed.remove(attr)
                    rhs_set.set_max(attr,dataset.get_max(attr))
                else:
                    lhs_set.set_max(attr,lhs_set.get_max(attr)-peri)
                    lhs_set.getrealvalue(attr)
                    rhs_set.m_reversed.remove(attr)
                    rhs_set.set_max(attr,dataset.get_max(attr))
                    rhs_set.set_min(attr,rhs_set.get_min(attr)-peri)
                rhs_set.getrealvalue(attr)
            else:
                lhs_set.m_splitted.add(attr)
                rhs_set.m_splitted.add(attr)
                if bestCut.m_splitpoint == dataset.get_max(attr):
                    # lhs_set.m_splitted.add(attr)
                    # rhs_set.m_splitted.add(attr)
                    pass
                else:
                    if lhs_set.get_max(attr) <= lhs_set.get_rootmax(attr):
                        rhs_set.getrealvalue(attr)
                        rhs_set.set_max(attr, rhs_set.get_max(attr) - peri)
                        rhs_set.m_reversed.add(attr)
                    else:
                        lhs_set.set_max(attr, lhs_set.get_max(attr) - peri)
                        lhs_set.getrealvalue(attr)
                        lhs_set.m_reversed.add(attr)
                        rhs_set.set_max(attr, rhs_set.get_max(attr) - peri)
                        rhs_set.set_min(attr, rhs_set.get_min(attr) - peri)
                        rhs_set.getrealvalue(attr)

        for attribute in dataset.attr_names:
            if attribute == bestCut.attribute:
                continue
            if dataset.attr_types_dict[attribute] == float:
                minVal = dataset.get_min(attribute)
                maxVal = dataset.get_max(attribute)
                lhs_set.set_min(attribute, minVal)
                lhs_set.set_max(attribute, maxVal)
                rhs_set.set_min(attribute, minVal)
                rhs_set.set_max(attribute, maxVal)
            else:
                attrrange = copy.deepcopy(dataset.get_range(attribute))
                lhs_set.set_range(attribute,attrrange)
                rhs_set.set_range(attribute,attrrange)

        return lhs_set, rhs_set
            
    def _findBestCut(self, dataset):               
        bestCut = None # bestCut is outside of for loop
        for idx, attribute in enumerate(dataset.attr_names):
            attrtype = dataset.attr_types[idx + 2][1]
            if attrtype == float:

                dataset.sort(attribute)
                di_cut1 = self._calcCut1(dataset, attribute)
                if di_cut1:
                    print "split1:",attribute,di_cut1.value
                if di_cut1 is None: # Ignore dimension
                    continue

                di_cut2 = self._calcCut2(di_cut1)
                if di_cut2:
                    print "split2:",attribute,di_cut2.value
                if di_cut2 is None:
                    # bestCut = self._selectLowerDensityCut(di_cut1, bestCut)
                    bestCut = self._selectHigherInfoCut(di_cut1, bestCut)
                    continue

                di_cut3 = self._calcCut3(di_cut1, di_cut2)
                if di_cut3:
                    print "split3:",attribute,di_cut3.value
                if di_cut3 is None:
                    # bestCut = self._selectLowerDensityCut(di_cut2, bestCut)
                    bestCut = self._selectHigherInfoCut(di_cut2, bestCut)
                else:
                    # bestCut = self._selectLowerDensityCut(di_cut3, bestCut)
                    bestCut = self._selectHigherInfoCut(di_cut3, bestCut)
            elif attrtype == int:
                # categorical
                pass
                di_cut1 = self._calcCut1(dataset, attribute)
                if di_cut1 is None: # Ignore dimension
                    continue
                # bestCut = self._selectLowerDensityCut(di_cut1, bestCut)
                bestCut = self._selectHigherInfoCut(di_cut1, bestCut)
            else:
                # periodical
                pass
                curbestcut = self._findperiodicalbestcut(dataset, attribute)
                # bestCut = self._selectLowerDensityCut(curbestcut,bestCut)
                bestCut = self._selectHigherInfoCut(curbestcut, bestCut)

        # if bestCut is None:
        #     return None
        # if len(bestCut.lhs_set.instance_values) < self.cutCreator.min_split or len(bestCut.rhs_set.instance_values) < self.cutCreator.min_split:
        #     return None
        return bestCut

    def _generatenumericaldataset(self, dataset, attribute, splitpoint = None):
        valuelist = dataset.instance_values.tolist()
        if splitpoint is not None:
            splitpoint = dataset.get_max(attribute)
        for idx in xrange(len(valuelist)):
            if valuelist[idx][dataset.attr_idx[attribute]] <= splitpoint:
                valuelist[idx][dataset.attr_idx[attribute]] += dataset.getperiod(attribute)
        dttype = list()
        for attr,value in dataset.attr_types:
            dttype.append((attr,float))
        output = np.array(valuelist, dtype=dttype)
        newdataset = Data(output, dataset.class_map, dataset.class_names, dataset.attr_types)
        newdataset.setperiodicalinfo(dataset)
        newdataset.sort(attribute)
        return newdataset

    def _findperiodicalbestcut(self, dataset, attribute):
        if not dataset.isattrrevrsered(attribute) and dataset.isattrsplitted(attribute):
            # treat as numerical feature
            return self._findperiodicalbestcutsimplecase(dataset, attribute)
                # bestCut = self._selectLowerDensityCut(di_cut3, bestCut)
        elif dataset.isattrrevrsered(attribute) and not dataset.isattrsplitted(attribute):
            # treat as numerical feature, but need to be reversed, that means
            # the left para need to add period.
            pass
            newdataset = self._generatenumericaldataset(dataset,attribute)
            return self._findperiodicalbestcutsimplecase(newdataset, attribute)
        else:
            bestcut = None
            instances = dataset.getInstances(attribute)
            for i, value in enumerate(instances):
                if len(instances) > i + 1 and instances[i + 1] == value:
                    continue
                oldmax = dataset.get_max(attribute)
                oldmin = dataset.get_min(attribute)
                dataset.max_values[dataset.attr_idx[attribute]] = value
                if len(instances) > i + 1:
                    dataset.min_values[dataset.attr_idx[attribute]] = instances[i + 1]
                else:
                    dataset.min_values[dataset.attr_idx[attribute]] = instances[0]
                dataset.m_reversed.add(attribute)
                dataset.m_splitted.add(attribute)
                newdataset = self._generatenumericaldataset(dataset,attribute)
                dataset.m_reversed.remove(attribute)
                dataset.m_splitted.remove(attribute)
                dataset.max_values[dataset.attr_idx[attribute]] = oldmax
                dataset.min_values[dataset.attr_idx[attribute]] = oldmin
                curcut = self._findperiodicalbestcutsimplecase(newdataset, attribute)
                curcut.m_splitpoint = value
                bestcut = self._selectLowerDensityCut(curcut, bestcut)
            return bestcut

    def _findperiodicalbestcutsimplecase(self, dataset, attribute):
        dataset.sort(attribute)
        di_cut1 = self._calcCut1(dataset, attribute)
        if di_cut1:
            print "split1:",attribute,di_cut1.value
        if di_cut1 is None: # Ignore dimension
            return

        di_cut2 = self._calcCut2(di_cut1)
        if di_cut2:
            print "split2:",attribute,di_cut2.value
        if di_cut2 is None:
            return di_cut1
            # bestCut = self._selectLowerDensityCut(di_cut1, bestCut)
            # continue

        di_cut3 = self._calcCut3(di_cut1, di_cut2)
        if di_cut3:
            print "split3:",attribute,di_cut3.value
        if di_cut3 is None:
            return di_cut2
            # bestCut = self._selectLowerDensityCut(di_cut2, bestCut)
        else:
            return di_cut3

    def _calcCut1(self, dataset, attribute):
        print "cut by attr:",attribute
        return self.cutCreator.cut(dataset, attribute) 

    def _calcCut2(self, di_cut1):   
        lower_density_set = di_cut1.getLowerDensityRegion() 
        return self.cutCreator.cut(lower_density_set, di_cut1.attribute)                                        
            
    def _calcCut3(self, di_cut1, di_cut2):   
        adjacentRegion = di_cut2.getAdjacentRegion(di_cut1.value, di_cut1.attribute)
        otherRegion = di_cut2.getNonAdjacentRegion(di_cut1.value, di_cut1.attribute)
                
        di_cut3 = None
        if _relative_density(adjacentRegion) <= _relative_density(otherRegion):
            lower_density_set = di_cut2.getLowerDensityRegion()                                    
            di_cut3 = self.cutCreator.cut(lower_density_set, di_cut2.attribute)                                        
        return di_cut3
    
    def _selectLowerDensityCut(self, cut1, cut2):
        if cut1 is None: return cut2
        if cut2 is None: return cut1
        rd1 = cut1.getRelativeDensityOfLowerDensityRegion() 
        rd2 = cut2.getRelativeDensityOfLowerDensityRegion()
        if rd1 < rd2: return cut1
        else: return cut2

    def _selectHigherInfoCut(self, cut1, cut2):
        if cut1 is None: return cut2
        if cut2 is None: return cut1
        if cut1.m_ig < cut2.m_ig: return cut2
        else: return cut1
        
    def _plotCut(self, bestCut, dataset, lhs_dataset, rhs_dataset):
        if lhs_dataset.length() > 0 or rhs_dataset.length() > 0:
            if myplt.attribute_1 == bestCut.attribute:
                minVal = dataset.get_min(myplt.attribute_2)
                maxVal = dataset.get_max(myplt.attribute_2)
            else:
                minVal = dataset.get_min(myplt.attribute_1)
                maxVal = dataset.get_max(myplt.attribute_1)
            myplt.line(bestCut.attribute, bestCut.value, minVal, maxVal)
            #myplt.draw()


class DatasetSplitter:
    def __init__(self):
        pass

    # split < x and >= x
    def split(self, dataset, attribute, value, idx):

        try:
            l = dataset.instance_values[0:idx+1]
            r = dataset.instance_values[idx+1:]
        except:
            l = dataset.instance_values[0:idx[0]]
            r = dataset.instance_values[idx[0]:]
                
        lhs_set = Data(l, dataset.class_map, dataset.class_names, dataset.attr_types)
        rhs_set = Data(r, dataset.class_map, dataset.class_names, dataset.attr_types)        
                
        rhs_set.set_min(attribute, value)
        
        self._splitNrVirtualPoints(dataset, attribute, value, lhs_set, rhs_set)
        self._updateVirtualPoints(lhs_set)
        self._updateVirtualPoints(rhs_set)
        
        return lhs_set, rhs_set

    # def splitPeriodical(self, dataset, attribute, value, idx):
    #     pass
    #     try:
    #         l = dataset.instance_values[0:idx+1]
    #         r = dataset.instance_values[idx+1:]
    #     except:
    #         l = dataset.instance_values[0:idx[0]]
    #         r = dataset.instance_values[idx[0]:]
    #
    #     lhs_set = Data(l, dataset.class_map, dataset.class_names, dataset.attr_types)
    #     rhs_set = Data(r, dataset.class_map, dataset.class_names, dataset.attr_types)
    #
    #     rhs_set.set_min(attribute, value)
    #
    #     self._splitNrVirtualPoints(dataset, attribute, value, lhs_set, rhs_set)
    #     self._updateVirtualPoints(lhs_set)
    #     self._updateVirtualPoints(rhs_set)
    #
    #     return lhs_set, rhs_set

    def splitCat(self, dataset, attribute, value):
        pass
        attr_pos = dataset.attr_idx[attribute]
        l = [v for v in dataset.instance_values if v[attr_pos] == value]
        l = np.array(l)


        r = [v for v in dataset.instance_values if v[attr_pos] != value]
        r = np.array(r)

        lhs_set = Data(l, dataset.class_map, dataset.class_names, dataset.attr_types)
        # lhs_set.set_range(attribute,[value,])

        rhs_set = Data(r, dataset.class_map, dataset.class_names, dataset.attr_types)

        # print "wow"*100
        # print attribute, value
        # print lhs_set.instance_values
        # print lhs_set._attr_range
        # print "ssss"*40
        # print rhs_set.instance_values
        # print rhs_set._attr_range

        # rhs_set.remove_range(attribute,value)


        self._splitNrVitualPointssCat(dataset, attribute, lhs_set, rhs_set)
        self._updateVirtualPoints(lhs_set)
        self._updateVirtualPoints(rhs_set)

        return lhs_set, rhs_set

    # update virtual points for split node
    def _splitNrVitualPointssCat(self, dataset, attribute, in_set, out_set):
        inlen = len(in_set.get_range(attribute))
        outlen = len(out_set.get_range(attribute))
        parlen = len(dataset.get_range(attribute))

        in_set.nr_virtual_points = int(inlen * dataset.nr_virtual_points / parlen )
        out_set.nr_virtual_points = int(outlen * dataset.nr_virtual_points / parlen )

    def _splitNrVirtualPoints(self, dataset, attribute, value, in_set, out_set):
        minV = dataset.get_min(attribute)
        maxV = dataset.get_max(attribute)
        in_set.nr_virtual_points = int(abs(dataset.nr_virtual_points*((value-minV)/(maxV-minV))))
        out_set.nr_virtual_points = dataset.nr_virtual_points - in_set.nr_virtual_points
        if out_set.nr_virtual_points < 0:
            self.raiseUndefinedNumberOfPoints()
    
    def _updateVirtualPoints(self, data_set):            
        nr_points_in_set = data_set.length()
        data_set.nr_virtual_points = self._calcNumberOfPointsToAdd(nr_points_in_set, data_set.nr_virtual_points)
        # data_set.nr_virtual_points = nr_points_in_set
        data_set.nr_total_instances = nr_points_in_set + data_set.nr_virtual_points

    def _calcNumberOfPointsToAdd(self, nr_points_in_node, nr_points_inherited):
        if nr_points_inherited < nr_points_in_node:
            nr_points = nr_points_in_node
        else:
            nr_points = nr_points_inherited
        return nr_points
    
    def raiseUndefinedNumberOfPoints(self):
        raise DatasetSplitter.UndefinedNumberOfPoints()
    class UndefinedNumberOfPoints(Exception):
        pass    
    
       
class InfoGainCutFactory:
    def __init__(self, min_split, min_infogain):
        self.min_split = min_split
        self.min_infogain = min_infogain
        self.datasetSplitter = DatasetSplitter()
        self.revdict = trandt.readreversedict(Constant.TRANFILE)

    def cut(self, dataset, attribute):
        di_cut = None
        max_info_gain = -1
        if dataset.attr_types_dict[attribute] == float:
            instances = dataset.getInstances(attribute)
            for i, value in enumerate(instances):
                if len(instances) > i + 1 and instances[i + 1] == value:
                    continue
                # if len(instances) == i + 1:
                #     continue
                if self._hasRectangle(dataset, attribute, value):
                    lhs_set, rhs_set = self.datasetSplitter.split(dataset, attribute, value, i)

                    # why update virtual points number before calculate info gain
                    ig, lset, rset = self._info_gain(dataset, lhs_set, rhs_set)
                    #print "cut detail:",attribute,value,ig,lhs_set.nr_total_instances,rhs_set.nr_total_instances
                    # if dataset.length() == 709 and attribute == "#images":
                    #     print "-----testcut:", ig, value
                    if ig > max_info_gain:
                        max_info_gain = ig
                        di_cut = Cut(attribute, value, dataset.getId(i), lset, rset)
                        di_cut.m_ig = ig
                        # print "######curig:",max_info_gain, lset.length(),rset.length()

        else:
            # categorical
            pass
            if len(dataset.get_range(attribute)) > 1:
                for value in dataset.get_range(attribute):
                    try:
                        if self.revdict[attribute][value] == "None":
                            continue
                    except:
                        print "attribute:",attribute
                        print "value:",value
                        import pprint
                        pp = pprint.PrettyPrinter(indent=4)
                        pp.pprint(self.revdict)
                        raise
                    lhs_set, rhs_set = self.datasetSplitter.splitCat(dataset,attribute, value)

                    ig, lset, rset = self._info_gain(dataset, lhs_set, rhs_set)
                    if ig > max_info_gain:
                        max_info_gain = ig
                        #di_cut = Cut(attribute, value, dataset.getId(i), lset, rset)
                        di_cut = Cut(attribute, value, 0, lset, rset)
                        di_cut.m_ig = ig
                        # print "######curig:",max_info_gain, lset.length(),rset.length()
        print "mxinfogain: ",max_info_gain
        # if di_cut is None:
        #     return None
        # if len(di_cut.lhs_set.instance_values) < self.min_split or len(di_cut.rhs_set.instance_values) < self.min_split:
        #     return None
        return di_cut
    
    def _hasRectangle(self, dataset, attribute, value):
        if dataset.get_max(attribute) == dataset.get_min(attribute): 
            return False
        else:
            if dataset.get_max(attribute) == value:
                return False
            else:
                return True

    def _info_gain(self, dataset, lhs_set, rhs_set):                   
        #if (lhs_set.nr_total_instances < self.min_split) or (rhs_set.nr_total_instances < self.min_split):
        if (len(lhs_set.instance_values) < self.min_split) or (len(rhs_set.instance_values) < self.min_split):
            return -1, lhs_set, rhs_set
    
        ratio_instances_lhs = (float(lhs_set.nr_total_instances)/dataset.nr_total_instances)
        ratio_instances_rhs = (float(rhs_set.nr_total_instances)/dataset.nr_total_instances)
        entropy2 = ratio_instances_lhs*self._calc_entropy(lhs_set) + ratio_instances_rhs*self._calc_entropy(rhs_set)
    
        entropy1 = self._calc_entropy(dataset)
        if entropy1 - entropy2 < self.min_infogain:
            return -1, lhs_set, rhs_set

        return (entropy1 - entropy2), lhs_set, rhs_set

    def _calc_entropy(self, dataset):
        nr_existing_instances = dataset.length()
        total = nr_existing_instances + dataset.nr_virtual_points
        terms = list()
        terms.append((float(nr_existing_instances)/float(total))*sqrt(float(nr_existing_instances)/float(total)))    
        terms.append((float(dataset.nr_virtual_points)/float(total))*sqrt(float(dataset.nr_virtual_points)/float(total)))                
        return sum(terms)*-1
        
class Cut:
    def __init__(self, attribute, value, inst_id, lhsset, rhsset):
        self.attribute = attribute
        self.value = value
        self.inst_id = inst_id
        self.lhs_set = lhsset
        self.rhs_set = rhsset

    def __str__(self):
        s = 'Cut: ' + self.attribute + "\n"
        s += str(self.lhs_set.attr_names) + "\n"  
        s += " Max lhs:" + str(self.lhs_set.max_values)+ "\n"  
        s += " Min lhs:" + str(self.lhs_set.min_values)+ "\n"
        s += " Max rhs:" + str(self.rhs_set.max_values)+ "\n" 
        s += " Min rhs:" + str(self.rhs_set.min_values)        
        s += '\n--------\n'
        return s
                
    def getNonAdjacentRegion(self, value, attribute):    
        dataset = self.getAdjacentRegion(value, attribute)
        if dataset is self.lhs_set:
            return self.rhs_set
        if dataset is self.rhs_set:
            return self.lhs_set
        return None
        
    def getAdjacentRegion(self, value, attribute):
        def getMinimumDistanceFromValue(dataset, attribute, value):
            distance1 = abs(dataset.get_max(attribute) - value)
            distance2 = abs(dataset.get_min(attribute) - value)
            return min(distance1, distance2)
        rhs_distance = getMinimumDistanceFromValue(self.rhs_set, attribute, value)
        lhs_distance = getMinimumDistanceFromValue(self.lhs_set, attribute, value)

        if lhs_distance < rhs_distance: return self.rhs_set
        else: return self.lhs_set
    
    def getRelativeDensityOfLowerDensityRegion(self):    
        lower_density_set = self.getLowerDensityRegion()                                                    
        r_density = _relative_density(lower_density_set)                
        return r_density

    def getLowerDensityRegion(self):
        if self.lhs_set is None or self.rhs_set is None:
            self.raiseNoRegionsDefined()
            
        if _relative_density(self.lhs_set) > _relative_density(self.rhs_set):
            return self.rhs_set
        else:
            return self.lhs_set  
    
    def raiseNoRegionsDefined(self):
        raise Cut.NoRegionsDefined("hi")
    class NoRegionsDefined(Exception):
        pass    
       
         
class CLNode(object):
    def __init__(self, dataset, parent, attribute, depth, direction , value):
        self.dataset = dataset
        self.parent = parent
        self.attribute = attribute
        self.children = list()
        self.can_prune = False

        self.direction = direction
        self.value = value

        self.depth = depth

        self.root  = self.getroot()

    def fetchfullsplitrull(self):
        rull = []
        p = self
        while p.parent:

            par = p.parent
            splittype = par.dataset.getAttrType(par.attribute)
            splitattr = par.attribute
            splitvalue = par.value
            rull.append([splittype,splitattr,splitvalue,p.direction])
            p = p.parent
        return rull

    def fetchfullrawsplitrull(self):
        rull = self.fetchfullsplitrull()
        print "rule:", rull
        newrull = []
        revdict = trandt.readreversedict(Constant.TRANFILE)
        for splittype,splitattr,splitvalue,direction in rull:
            print "splittype:",splittype,splitattr
            if splittype == int:
                rawvalue = revdict[splitattr][splitvalue]
            else:
                rawvalue = splitvalue
            newrull.append([splittype,splitattr,rawvalue,direction])

        return newrull

    def fetchcombinedrull(self):
        rulllist = self.fetchfullsplitrull()

        # for numeric data attrtype : {"lower":,"upper"}
        # for catogorical data : {"is":,"not":[]}
        combinedrulldict = {}

        for splittype,splitattr,splitvalue,direction in rulllist:
            if splitattr not in combinedrulldict:
                combinedrulldict[splitattr] = {}
            if splittype == float:
                if direction == "l":
                    oldvalue = combinedrulldict[splitattr].get("upper")
                    if oldvalue == None or splitvalue < oldvalue:
                        combinedrulldict[splitattr]["upper"] = splitvalue
                else:
                    oldvalue = combinedrulldict[splitattr].get("lower")
                    if oldvalue == None or splitvalue > oldvalue:
                        combinedrulldict[splitattr]["lower"] = splitvalue
            else:
                if direction == "l":
                    combinedrulldict[splitattr]["is"] = [splitvalue,]
                else:
                    if  "not" not in combinedrulldict[splitattr]:
                        combinedrulldict[splitattr]["not"] = []
                    combinedrulldict[splitattr]["not"].append(splitvalue)

        return combinedrulldict

    def fetchrawcombinedrull(self):
        combinedrulldict = self.fetchcombinedrull()
        revdict = trandt.readreversedict(Constant.TRANFILE)
        for attr, bounddict in combinedrulldict.items():
            if self.getroot().dataset.getAttrType(attr) == float:
                continue
            for key, valuelist in bounddict.items():
                combinedrulldict[attr][key] = [revdict[attr][v] for v in valuelist]
        return combinedrulldict

    def setPruneState(self, prune):
        self.can_prune = prune

    def isPrune(self):
        return self.can_prune

    def getRelativeDensity(self):
        return _relative_density(self.dataset)*100.0

    def getNrInstancesInNode(self):
        return self.dataset.length()
    
    def addChildNode(self, node):
        self.children.append(node)

    def getChildNodes(self):
        return self.children
    
    def isLeaf(self):
        if len(self.children) == 0: 
            return True
        else: 
            return False

    def raiseAddNode(self):
        raise CLNode.AddNodeIlogical("hi")
    class AddNodeIlogical(Exception):
        pass   
    
    def _getMajorityClassName(self):
        counts = [0] * len(self.dataset.class_names)
        class_idx = dict()
        for i, cls in enumerate(self.dataset.class_names):
            class_idx[cls] = i
        new_dict = dict (zip(self.dataset.class_map.values(),self.dataset.class_map.keys()))            
        for cls in list(self.dataset.getClasses()):
            v = new_dict[cls]
            counts[class_idx[v]] += 1
            
        max_count = -2
        self.max_class = -1 
        for i, c in enumerate(counts):
            if c > max_count:
                max_count = c
                self.max_class = self.dataset.class_names[i]        

        self.percent = int((max_count / float(self.dataset.length()) )* 100)               
        self.misclassified = self.dataset.length() - max_count

    def getroot(self):
        p = self
        while p.parent:
            p = p.parent
        self.root = p
        return p

    def getarea(self):
        rulldict = self.fetchcombinedrull()
        root = self.getroot()
        area = 1
        for attr in root.dataset.attr_names:
            targetlen = 1
            if attr in rulldict:
                if root.dataset.getAttrType(attr) == float:
                    min = root.dataset.get_min(attr)
                    max = root.dataset.get_max(attr)
                    targetlen = calculatenumericallength(rulldict[attr],min,max)
                else:
                    datarange = root.dataset.get_range(attr)
                    targetlen = calculatecategoricallength(rulldict[attr], datarange)
            else:
                if root.dataset.getAttrType(attr) == float:
                    min = root.dataset.get_min(attr)
                    max = root.dataset.get_max(attr)
                    targetlen = max - min
                else:
                    datarange = root.dataset.get_range(attr)
                    targetlen = len(datarange)
            if targetlen == 0:
                continue
            else:
                area *= targetlen
        return area

    def getdensity(self):
        # print "ahaha : ",density
        density = self.dataset.length() * 1.0 / self.getarea()
        return density

    def expressCat(self,attribute,reversetran):
        rootrange = self.root.dataset.get_range(attribute)
        ownrange = self.dataset.get_range(attribute)
        if len(rootrange) == len(ownrange):
            return ""

        if len(ownrange) == 1:
            return reversetran[attribute][ownrange[0]]

        exp = ""
        if len(rootrange) / len(ownrange) < 2:
            # not
            for idx in rootrange:
                if idx not in ownrange:
                    exp += "not " + reversetran[attribute][idx] + " && "
            return exp[:-4]
        else:
            for idx in ownrange:
                exp += reversetran[attribute][idx] + " || "
            return exp[:-4]

    def expressNum(self,attribute):
        rootmax = self.root.dataset.get_max(attribute)
        rootmin = self.root.dataset.get_min(attribute)
        ownmax = self.dataset.get_max(attribute)
        ownmin = self.dataset.get_min(attribute)

        if rootmax == ownmax and rootmin == ownmin:
            return ""
        if rootmax == ownmax:
            return "> " + str(ownmin)
        if rootmin == ownmin:
            return "< " + str(ownmin)
        return "> " + str(ownmin) +" and < " + str(ownmax)

    def __str__(self):
        attr = list()
        p = self
        while p:
            attr.append(p.attribute)
            p = p.parent
        
        self._getMajorityClassName()
        s = 'Node: ' + '\n'
        s += str(self.dataset.length()) + ' instances, ' + str(self.misclassified) + ' misclassified, ' + str(self.percent)+ '% '+ self.max_class
        s += ", " + str(int(self.getRelativeDensity())) + " relative density " + '\n'
        s += "Cuts " + str(set(attr))+ '\n'
        
        revdict = trandt.readreversedict(Constant.TRANFILE)

        self.dataset.calculate_limits()
        for name in self.dataset.attr_names:
            if self.dataset.attr_types_dict[name] == float:
                exp = self.expressNum(name)
                if exp:
                    s += name + ' max: ' + str(self.dataset.get_max(name))+\
                    ' min: ' + str(self.dataset.get_min(name))+'\n'
            else:
                exp = self.expressCat(name,revdict)
                if exp:
                    s += name + " : " + self.expressCat(name,revdict) + "\n"

        return s


