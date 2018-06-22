import os

from datasetUtils.datasetUtils import Dataset, DataHubUser

dir_path = os.path.dirname(os.path.realpath(__file__))
testUser = DataHubUser(name='test', configJsonFilePath=dir_path + '\\datasetUtils\\config-test.json')


for dir in os.listdir('datasets'):
    for inner_dir in os.listdir('datasets/' + dir):
        pushableDataset = Dataset(
            name=inner_dir,
            webSource='https://opendata.socrata.com/',
            folderPath=dir_path + '\\datasets\\' + dir + '\\' + inner_dir
        )

        pushableDataset.pushToDataHubByUser(testUser)
