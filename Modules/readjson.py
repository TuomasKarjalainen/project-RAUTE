def readJson(pathToPairsCsv="/home/jovyan/work/data/nfs_shared_data/Raute/JsonForSchoolProjectTest/VerifiedPairs.csv",
             pathToPeelJson='/home/jovyan/work/raute_data/NewPeel/',
             pathToDryJson='/home/jovyan/work/raute_data/NewDry/',
             onefile=None):
    """
    -------------------
    VERSION: 2021-11-18
    -------------------
    
    As a default returns all jsons using VerifiedPairs.csv. Jsons are return in json form in where one instance in list contains data of one json-file.
    By default uses these default paths:
        pathToPairsCsv="/home/jovyan/work/data/nfs_shared_data/Raute/JsonForSchoolProjectTest/VerifiedPairs.csv",
        pathToPeelJson='/home/jovyan/work/raute_data/NewPeel/'
        pathToDryJson='/home/jovyan/work/raute_data/NewDry/'
    
    If pathToPeelJson or pathToDryJson is set None, creating json data for them is skipped. Then use underscore (_) (see example) when storing returned values.
    
    Returns two lists:
    - list of peel-json files in Python form
    - list of dry-json files in Python form
    
    Example
    -------
    peel, dry = readJson() # No parameters needed, if default values are ok
    peel, _ = readJson(pathToDryJson=None) # Peeling files only (Use underscore to discard unneeded variables)
    _, dry = readJson(pathToPeelJson=None) # Drying files only
    
    ALTERNATE WAY TO USE:
    - You can also provide a full path to one json-file using onefile-parameter. If this parameter is provided, other parameters doesn't matter.
        Then only json-data of that one file is provided (as a dictionary, not as a list).
        
    Example
    -------
    myjson = readJson(onefile='/home/jovyan/work/raute_data/NewPeel/20210505121149_13.json')
    """

    import json
    import pandas as pd
    import os

    if onefile == None:
        pairs = pd.read_csv(pathToPairsCsv)
        pairs.drop(columns=["Unnamed: 0"],inplace=True)
        pairs['pFile']=pairs.pFile.str.replace('bmp','json')
        pairs['dFile']=pairs.dFile.str.replace('bmp','json')
        peel = []
        dry = []

        if pathToPeelJson != None:
            for file in pairs['pFile']:
                with open(os.path.join(pathToPeelJson)+file,'r') as f:
                    peel.append(json.load(f))

        if pathToDryJson != None:
            for file in pairs['dFile']:
                with open(os.path.join(pathToDryJson+file),'r') as f:
                    dry.append(json.load(f))

        return peel, dry
    else:
        with open(onefile,'r') as f:
            return json.load(f)