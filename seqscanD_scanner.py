"""Implementation of the SEQSCAN algorithm on a single Object."""

# Standard modules
from datetime import datetime, timedelta
from dateutil.parser import parse
from collections import defaultdict, OrderedDict
from numpy import genfromtxt
# my modules
from region import Region
from point import Point

from config.config_parser import loadConfigFile
from feature import Feature
import sys
import os
import psycopg2

ACCEPTABLE_EXTENSIONS= ('.csv')

def get_keys(feature):
    """
    This function is referenced in many of the scripts and is used as sorting key
    during the scan of a layer.
        """
    return (feature.objectTime)


def update_progress(progress):
    sys.stdout.write('\rProgress: [{0}] {1}%'.format('#' * int(progress), round(progress, 2)))


class DScanner(object):
    """Implementation of the SEQSCAN-D algorithm."""

    def __init__(self):
        
        input_exist= False
        while (input_exist is False):
            self.filePath = input("Please enter the input file path: ")
            if os.path.isfile(self.filePath) and os.path.splitext(self.filePath)[-1].lower() in ACCEPTABLE_EXTENSIONS:
                input_exist=True
            else:
                print("The input file does not exist or it is not a csv file, please try again")

        output_valid=False
        while(output_valid is False):
            self.output_file_path=input("Enter the output path: ")
            if self.output_file_path.endswith(ACCEPTABLE_EXTENSIONS):
                output_valid=True
            else:
                print("The output should be a csv file, please try again")


        n_exist= False
        while (n_exist is False):
            try:
                self.number= int(input("Enter the minimum number of points parameter N: "))
                n_exist= True
            except:
                print("N should be integer, try again: ")

        delta_exist= False
        while (delta_exist is False):
            try:
                self.presence= float(input("Enter the presence parameter delta, in days: "))
                delta_exist= True
            except:
                print("Delta should be numeric, try again: ")

        self.params = (self.number, self.presence)
        self.hashComputation = {}
        self.configDict = self.loadAndParseConfigFile()

        self.seqscan_d()


        
    def loadAndParseConfigFile(self):
        config_dict = loadConfigFile("config")

        self.pzone_field = config_dict["input_file_structure"]["pzone_field"]
        self.time_field = config_dict["input_file_structure"]["time_field"]
        self.time_field_format = config_dict["input_file_structure"]["time_field_format"]

        self.output_pzone_field = config_dict["output_file_structure"]["pzone_field"]
        self.output_start_time_field = config_dict["output_file_structure"]["start_time"]
        self.output_end_time_field = config_dict["output_file_structure"]["end_time"]
        self.output_presence_field = config_dict["output_file_structure"]["presence"]
        self.output_duration_field = config_dict["output_file_structure"]["duration"]
        self.output_q_index_field = config_dict["output_file_structure"]["q_index"]
        self.output_time_field_format = config_dict["output_file_structure"]["output_time_field_format"]

        return config_dict
    
    def loadDataPointsFromFile(self, filePath):
        features_array_tmp = []
        for att in genfromtxt(filePath, delimiter=',', names=True, dtype=None, encoding='UTF-8'):
            feature = Feature(
                att[self.pzone_field],
                datetime.strptime(att[self.time_field], self.time_field_format)
            )
            features_array_tmp.append(feature)
        return features_array_tmp
        
    def prepareDataPointsFromFile(self, filePath):
        self.features = self.loadDataPointsFromFile(filePath)
        
        dataset = []
        self.zoneSet=set()
        
        sorted_features = sorted(
            self.features, 
            key = lambda feature : get_keys(feature)
        )

        self.featuresCount = len(self.features)

        for feature in sorted_features:
            point = Point(
                feature.pzone,
                feature.objectTime  # parse(feature.objectTime, ignoretz=True),
            )
            self.zoneSet.add(feature.pzone)
            dataset.append(point)

        for z in self.zoneSet:
            self.hashComputation[z] = (0, 0,None)

        del sorted_features[:]
        del sorted_features
        del self.features[:]
        del self.features
        return dataset


    def add_cluster(self, cluster):
        if cluster is not None:
            self.clusters.add(cluster)  # final form


    def seqscan_d(self):
        """Excecutes the SEQSCAN-D clustering algorithm on a single object.
        """
        dataset = None

        try:
            dataset = self.prepareDataPointsFromFile(self.filePath)
            self.clusters = set()
            active_cluster = None
            previous_zone=None
            previous_timestamp=None

            counter =0
            for point in dataset:
                counter=counter+1
                current_z = point.pzone
                try:
                    current_npt_value=self.hashComputation[current_z]
                except:
                    continue;

                if(previous_zone==current_z):
                    if(previous_timestamp is None):
                        additional_pr=0
                    else:
                        diff=(point.time-previous_timestamp)
                        days,seconds =diff.days,diff.seconds
                        additional_pr= float(days)+ float((seconds/3600)/24)

                    new_pr=current_npt_value[1]+additional_pr
                    new_nb=current_npt_value[0]+1
                    self.hashComputation[current_z]=(new_nb,new_pr,current_npt_value[2])

                else:
                    new_pr=current_npt_value[1]
                    new_nb=current_npt_value[0]+1
                    self.hashComputation[current_z]=(new_nb,new_pr, current_npt_value[2] if current_npt_value[2]is not None else point.time)

                if(new_pr>self.presence)and float(new_nb)>=self.number:

                    if(active_cluster is None): #new first cluster is created
                        active_cluster= Region( point.pzone,current_npt_value[2],point.time,new_pr, new_nb)

                    elif(point.pzone==active_cluster.label): #expansion
                        active_cluster.time_end=point.time
                        active_cluster.presence=new_pr
                        active_cluster.n=new_nb

                    else: #new cluster is created, other than the active one
                        self.clusters.add(active_cluster)
                        active_cluster= Region(point.pzone,current_npt_value[2],point.time,new_pr, new_nb)

                    for z in self.zoneSet:
                        if(z!=point.pzone):
                            self.hashComputation[z]=(0,0,None)

                previous_zone=current_z
                previous_timestamp=point.time
                if(counter==len(dataset)):
                    if active_cluster is not None:
                        if active_cluster not in self.clusters:
                            self.clusters.add(active_cluster)

            try:
                self.exportOutputFiles()
            except:
                pass

            self.clearObjectMemory(dataset)


        except MemoryError as error:
            print("Out of memory while processing: " +str(error)+ "\n\n")
            self.clearObjectMemory(dataset)


    def exportOutputFiles(self):
        objectOutputFile=open(self.output_file_path, 'w+')
        locationKeyName = self.output_pzone_field
        starttimeKeyName = self.output_start_time_field
        endtimeKeyName=self.output_end_time_field
        presenceKeyName = self.output_presence_field
        durationKeyName = self.output_duration_field
        qindexKeyName= self.output_q_index_field
        keysArr = [locationKeyName, starttimeKeyName,endtimeKeyName, presenceKeyName, durationKeyName, qindexKeyName ]
        rowToPrint = ""

        for key in keysArr:
            valStr = str(key)
            if rowToPrint != "" :
                rowToPrint += "," + valStr
            else:
                rowToPrint += valStr

        print (rowToPrint, file=objectOutputFile)

        list_clusters = sorted(
            list(self.clusters),
            key=lambda region: region.id
        )
        for c in list_clusters:
            diff=(c.time_end-c.time_start)
            days,seconds =diff.days,diff.seconds
            duration= float(days)+ float((seconds/3600)/24)
            index=float(c.presence/duration)
            
            valuesToPrint = dict.fromkeys(keysArr,"")
            valuesToPrint[locationKeyName] = c.label
            valuesToPrint[starttimeKeyName] = c.time_start
            valuesToPrint[endtimeKeyName] = c.time_end#.strftime(self.time_field_format)
            valuesToPrint[presenceKeyName] = c.presence
            valuesToPrint[durationKeyName] = duration
            valuesToPrint[qindexKeyName] = index

            rowToPrint = ''
            for key in keysArr:
                valStr = str(valuesToPrint[key])
                if rowToPrint != "" :
                    rowToPrint += "," + valStr
                else:
                    rowToPrint += valStr

            print (rowToPrint, file=objectOutputFile)

        del valuesToPrint
        del rowToPrint
        objectOutputFile.close()

    def clearObjectMemory(self, dataset):
        Region.counter=0
        try:
            del self
        except Exception as exception:
            print(exception)

DScanner()