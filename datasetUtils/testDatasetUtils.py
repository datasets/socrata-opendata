from datasetUtils.datasetUtils import Dataset, DatasetGroup, DataHubUser


testDatasetOpenMV = Dataset(
    name='TestOpenMV',
    webSource='https://www.example.com',
    folderPath='500ds-Saad/datapackage-factory-openMV/aeration-rate'
)
testDatasetWorldBank = Dataset(
    name='TestWB',
    webSource='https://www.example.com',
    folderPath='test_push/gc.dod.totl.gd.zs'
)
testDatasetVehiclesUK = Dataset(
    name='TestVehicles',
    webSource='https://www.example.com',
    folderPath='500ds-Vladimir/500ds/vehicles-in-uk'
)
test5kb = Dataset(
    name='5kb-test',
    webSource='https://www.example.com',
    folderPath='/home/branko/BRANKO/Programming/Datopian/Datasets/500datasets-project/test_push'
)
# Test 1 - testing print of a class
# print(testDatasetOpenMV)
print(testDatasetWorldBank)
# print(testDatasetVehiclesUK)
# print(test5kb)

# Test 2 - Check to see if the local dataset has a datapackage
# print(testDatasetOpenMV.isPackaged)
print(testDatasetWorldBank.isPackaged)
# print(testDatasetVehiclesUK.isPackaged)
# print(test5kb.isPackaged)

# Test 3 - Create a datapackage.json for dataset that doesn't have one
# testDatasetOpenMV.createDatapackage()
testDatasetWorldBank.createDatapackage()
# testDatasetVehiclesUK.createDatapackage()

# Test 4 - Check to see if the datapackage is valid
# testDatasetOpenMV.validateDatapackage()
testDatasetWorldBank.validateDatapackage()
# testDatasetVehiclesUK.validateDatapackage()

# Test 5 - Load csv data
# testDatasetOpenMV.loadCsvResources()
# testDatasetWorldBank.loadCsvResources()
# testDatasetVehiclesUK.loadCsvResources()

# Test 6 - Load JSON metadata
# testDatasetOpenMV.loadMetadataJSON()
# testDatasetWorldBank.loadMetadataJSON()
# testDatasetVehiclesUK.loadMetadataJSON()

# Test 7 - Create new user
testUser = DataHubUser(name='test', configJsonFilePath='.config/datahub/config-test.json')
# worldBankUser = DataHubUser(name='world-bank', configJsonFilePath='.config/datahub/config-world-bank.json')

# Test 8 - Print new user
# print(testUser)
print(testUser)

# Test 9 - Push to datahub by different usersf

testDatasetWorldBank.pushToDataHubByUser(testUser)

# Test 10 - Scan folder for world-bank datasets
