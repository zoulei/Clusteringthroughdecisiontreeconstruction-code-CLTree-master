import numpy as np
import copy

class Data:
    '''ARFF Data'''
    def __init__(self, instance_values, class_map, class_names, types):
        # self.real_types = types
        # floattype = list()
        # for attr, value in types.items():
        #     floattype.append((attr,float))

        self.instance_values = instance_values
        self.class_map = class_map
        self.class_names = class_names
        self.attr_types = types
        self.attr_idx = dict()
        self.attr_names = list()

        self.attr_types_dict = dict()

        self._init_attr_names()
        self._init_max_min()

        self._attr_range = dict()
        # self._init_range()

        self.calculate_range()

        # this is fill point
        self.nr_virtual_points = len(self.instance_values)
        # this is total point
        self.nr_total_instances = 2*self.nr_virtual_points

        self.m_rootmax = self.max_values
        self.m_rootmin = self.min_values

        self.m_reversed = set()
        self.m_splitted = set()

        self.m_period = dict()
        self.initperiod()

    @ staticmethod
    def generatedata(data):
        newdata = list()
        for v in data:
            newdata.append(tuple(v))
        return newdata

    def fetchinstanceaslist(self):
        v = self.instance_values.tolist()
        for idx in xrange(len(v)):
            v[idx] = list(v[idx])
        return v

    def initperiod(self):
        for attr, value in self.attr_types:
            if isinstance(value, float):
                self.m_period[attr] = value

    def getrealvalue(self, attr):
        attridx = self.attr_idx[attr]
        listdata = self.instance_values.tolist()
        for idx in xrange(len(listdata)):
            if listdata[idx][attridx] > self.get_rootmax(attr):
                listdata[idx][attridx] -= self.getperiod(attr)
        self.instance_values = np.array(listdata, self.attr_types)

    def setperiodicalinfo(self, otherset):
        self.m_reversed = otherset.m_reversed
        self.m_splitted = otherset.m_splitted
        self.m_period = otherset.m_period
        self.m_rootmax = otherset.m_rootmax
        self.m_rootmin = otherset.m_rootmin

    # def increperiod(self, attr):
    #     self.instance_values

    def isattrsplitted(self, attr):
        return attr in self.m_splitted

    def isattrrevrsered(self, attr):
        return attr in self.m_reversed

    def getperiod(self, attr):
        return self.m_period[attr]

    def get_range(self,attribute):
        return self._attr_range[attribute]

    def set_range(self,attribute,rangelist):
        self._attr_range[attribute] = copy.deepcopy(rangelist)

    def remove_range(self,attribute,value):
        self._attr_range[attribute].remove(value)

    # def _init_range(self):
    #     for key,value in self.attr_types[2:]:
    #         if value == int:
    #             self._attr_range[key] = range(int(self.get_min(key)),int(self.get_max(key))+1)

    def _init_max_min(self):
        if len(self.instance_values) > 1:
            self.instance_view = self.instance_values.view(dtype=float).reshape(len(self.instance_values),-1)
            self.max_values = np.amax(self.instance_view, 0) 
            self.min_values = np.amin(self.instance_view, 0)
            #self.instance_view = self.instance_values.view(dtype = self.attr_types).reshape(len(self.instance_values),-1)

        else:
            self.instance_view = self.instance_values.view(dtype = float)
            self.max_values = copy.copy(self.instance_view)
            self.min_values = copy.copy(self.instance_view)
            #self.instance_view = self.instance_values.view(dtype = self.attr_types)

    def _init_attr_names(self):
        for i, attr in enumerate(self.attr_types):
            #if i == 0: #Dimitri
            if i < 2:
                continue
            attr_name, attr_type = attr
            self.attr_idx[attr_name] = i
            self.attr_names.append(attr_name)
            self.attr_types_dict[attr_name] = attr_type
        
    def __str__(self):
        s = 'Data: ' + str(len(self.instance_values)) + "\n"
        s += str(self.attr_names) + "\n"  
        s += " Max :" + str(self.max_values)+ "\n"  
        s += " Min :" + str(self.min_values)+ "\n"
        s += str(self.instance_values)
        s += '\n--------\n'
        return s
    
    def calculate_limits(self):
        self._init_max_min()
        self.calculate_range()

    def attr_type(self,attr):
        return self.attr_types_dict[attr]

    def calculate_range(self):
        for attr, value in self.attr_types_dict.items():
            if value == int:
                allvalue = self.getInstances(attr)
                valueset = set(allvalue)
                rangelist = list(valueset)
                self.set_range(attr,rangelist)

    def sort(self, attribute):
        self.instance_values.sort(order=attribute)
        
    def length(self):
        return len(self.instance_values)

    def getClasses(self):
        idx = 1
        if self.length() > 1:
            return self.instance_view[:,idx]
        elif self.length() == 1:
            return [self.instance_view[idx]]
        else:
            return []
    
    def getInstances(self, attribute):
        idx = self.attr_idx[attribute]
        if self.length() > 1:
            return self.instance_view[:,idx]
        elif self.length() == 1:
            return [self.instance_view[idx]]
        else:
            return []
        
    def getInstanceIndex(self, id):
        if self.length() > 1:                
            idx = np.argwhere(self.instance_view[:,0] == id)
            return idx[0]
        elif self.length() == 1 and id == self.instance_view[0]:            
            return 0
        else:
            return None

    # get the order of the data
    def getId(self, idx):
        if self.length() > 1:        
            return self.instance_view[idx][0]
        elif self.length() == 1:
            return self.instance_view[0]
        else:
            return -1

    def getAttrType(self,attr):
        return self.attr_types_dict[attr]

    def get_rootmax(self, attribute):
        idx = self.attr_idx[attribute]
        return self.m_rootmax[idx]
    def get_rootmin(self, attribute):
        idx = self.attr_idx[attribute]
        return self.m_rootmin[idx]

    def get_max(self, attribute):
        idx = self.attr_idx[attribute]
        return self.max_values[idx]
    def get_min(self, attribute):
        idx = self.attr_idx[attribute]
        return self.min_values[idx]
    def set_max(self, attribute, value):
        if len(self.max_values) > 0:
            idx = self.attr_idx[attribute]
            self.max_values[idx] = value
    def set_min(self, attribute, value):
        if len(self.min_values) > 0:
            idx = self.attr_idx[attribute]
            self.min_values[idx] = value


    

class ArffReader:
    def __init__(self,limit = 0):
        self.limit = limit
    
    def read(self, filename):
        f = open(filename, 'r')
        types, classes_names = self._read_header(f)

        # this is the class line, which is not used in real time
        class_map = dict()
        for i, name in enumerate(classes_names):
            class_map[name] = float(i)
        
        output = self._read_instances(f, class_map)
        readtype = list()
        for attr,value in types:
            readtype.append((attr,float))
        output = np.array(output, dtype=readtype)

        data = Data(output, class_map, classes_names, types)
                
        print "read " + str(data.length()) + ' instances from ' + filename
        print "attribute names:", data.attr_types
        print "class names:", data.class_names

        print "attribute range:\n"
        for attribute in data.attr_names:
            if data.attr_types_dict[attribute] != int:
                print attribute,":",data.get_min(attribute),",",data.get_max(attribute)
            else:
                print attribute,":",str(data.get_range(attribute))

        print "output data:"
        print data.attr_types_dict
        # print data.attr_idx
        # print data.instance_view
        # print "--------------------------"

        return data
        
    def _read_header(self, contents):
        dtype = list() 
        classes = None
        dtype.append(("id", float))        
        dtype.append(("class", float))  
        for line in contents:
            line = line.strip().lower()
            if line.startswith("%") or line.startswith("@RELATION"):
                continue
            if line == "@data":
                break            
            if line.find("@attribute") != -1:
                attr_name, attr_type = self._getAttribute(line)
                if attr_type in ["real", "numeric"]:
                    dtype.append((attr_name, float))

                elif attr_type == "cat":
                    dtype.append((attr_name, int))

                elif attr_name == "class":
                    classes = attr_type.split(",")
                else:
                    dtype.append((attr_name, float(attr_type)))
                    # raise NotImplemented()
        return dtype, classes

    def _getAttribute(self, line):
        print "123:",line
        print line.split()
        attr_, attr_name, attr_type = line.split()
        attr_name = attr_name.lower()
        attr_type = attr_type.strip("'").strip("{").strip("}").lower()
        return attr_name, attr_type
        
    def _read_instances(self, contents, class_map): 
        output = list()
        class_values = list()
        count = 0.0
        for line in contents:

            if line.startswith("%"):
                continue
            line = line.split(',')
            row = list()
            row.append(count)
            cls = class_map[line[-1].strip('\n')]
            row.extend([cls]) #class
            row.extend([float(s.strip()) for s in line[0:-1]])
            output.append(tuple(row))
            count += 1.0
            if self.limit != 0 and self.limit < count:
                break
        return output

