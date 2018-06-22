import os
import glob
import json
import pandas
import pexpect


# Still working on this
class DatasetGroup:
    """DatasetGroup is a class for a group of datasets"""
    def __init__(self, datasetList):
        self.datasetList = datasetList

    def addDatasetToGroup(self, dataset):
        if not dataset.isPackaged:
            self.arePackaged = False
        if dataset not in self.datasetList:
            self.datasetList.append(dataset)


class Dataset(object):
    """Dataset class"""
    def __init__(self, name, webSource, folderPath):
        self.name = name
        self.webSource = webSource
        self.folderPath = folderPath
        self.isPackaged = 'datapackage.json' in os.listdir(folderPath)

    def __str__(self):
        dictForPrint = {
            "Name": self.name,
            "Source": self.webSource,
            "Local Folder Path": self.folderPath,
            "Is packaged": self.isPackaged
        }
        stringToPrint = '{\n' + ',\n'.join(map(lambda key: '\t' + key + ': ' + str(dictForPrint[key]), dictForPrint))
        stringToPrint += '\n}'
        return stringToPrint

    def createDatapackage(self):
        if self.isPackaged:
            print("dataset is already packaged")
        else:
            oldPath = os.getcwd()
            os.chdir(self.folderPath)
            os.system('data init ')
            os.chdir(oldPath)
            self.isPackaged = True
            print("dataset has been succesfully packaged")

    def validateDatapackage(self):
        child = pexpect.spawn('data validate ' + self.folderPath)
        byteOutput = child.read()
        outputString = byteOutput.decode("utf-8")
        print(outputString)
        if "Error!" in outputString:
            print(False)
        # os.system('data validate ' + self.folderPath)

    def loadCsvResources(self):
        csvFilePaths = glob.glob(self.folderPath + '/**/*.csv', recursive=True)
        csvDataDictionary = {}
        for filePath in csvFilePaths:
            csvDataDictionary[filePath] = pandas.read_csv(filePath)
        self.csvDataDictionary = csvDataDictionary

    def loadMetadataJSON(self):
        self.metadataJSON = json.loads(open(self.folderPath + "/datapackage.json", "r").read())
        print(self.metadataJSON["name"])

    def pushToDataHubByUser(self, user=''):
        if user:
            os.environ["DATAHUB_JSON"] = user.configJsonFilePath
        print('DATAHUB_JSON', os.environ["DATAHUB_JSON"])
        # os.system('data login --api https://api-testing.datahub.io')
        # print(('data push ' + self.folderPath + ' --name=' + self.name + ' --unlisted'))
        # os.system('data push ' + self.folderPath + ' --name=' + self.name + ' --unlisted')
        print('data push \"' + self.folderPath + '\" --published')
        os.system('data push \"' + self.folderPath + '\" --published')


class DataHubUser:
    """docstring for DataHubUser"""
    def __init__(self, name, configJsonFilePath):
        self.name = name
        self.configJsonFilePath = configJsonFilePath

    def __str__(self):
        return '{\n\tname: ' + self.name + '\n\tconfigJsonFilePath: ' + self.configJsonFilePath + '\n}'

    def printConfigJSON(self):
        print(open(os.environ["HOME"] + '/' + self.configJsonFilePath).read())
