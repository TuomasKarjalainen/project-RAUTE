def create_full_feature_and_target_matrix(fullpathToPairsCsv="/raute_data/Raute/JsonForSchoolProjectTest/VerifiedPairs.csv",
                                          pathToPeelJson='/raute_data/Raute/JsonForSchoolProjectTest/NewPeel/',
                                          pathToDryJson='/raute_data/Raute/JsonForSchoolProjectTest/NewDry/',
                                          printProgress=False,
                                          pushToDatabase=True,
                                          host = '172.17.0.2',
                                          user = 'root',
                                          password = 'team1',
                                          database = 'Projekti',
                                          port = 3306,
                                          chunksize=10,
                                          featuresTableName=None,
                                          targetTableName=None,
                                          combinedTableName='PreprocessedData',
                                          unique = True):
    """
    
    from Preprocess.full_feature_matrix import create_full_feature_and_target_matrix
    -------------------------------------------------------------------------------------
    VERSION: 2021-12-09
    LATEST UPDATE:
    - Changed pushToDatabase default value to True
    - Unique tables creation
    - Parameters to sql connection
    - Fixed bug with combinechunking where the function pushed one chunk too many to database
    - Added option to use chunking when using combinedTableName
    - removed import: from typing import Iterator
    - Chunker added
    - Added dryMoisturePercentage as a new feature to df_features / current_row
    - Added traindevtest column to df_features / current_row 
    - Added NaN-checking and dryShrinkage > 1 checking
    -------------------------------------------------------------------------------------
    
    Reads verified pairs from csv. Then runs paired peeling and drying json-files in a loop.
    Forms rows for feature matrix and target matrix pair by pair.

    Depending on user choice either pushed data to database (pushToDatabase=True) or just returns feature and target matrix (pushToDatabase=False).
    When pushing to database, data is possible to push in chunks (chunksize=<desired amount as integer>) or all data at once (chunksize=None).
    
    If pushToDatabase=False, after all files are done, function returns two dataframes: df_features and df_target.

    If unique = True, function will make new tables which wont allow duplicate values. If you have called this once and want to add more data to that specific table, then pass unique = False so it doesnt try to make a new table

    If you want to add data to your own database and container then change sql parameters when you call the function.
    
    Parameters
    ----------
    
    fullpathToPairsCsv = string, DEFAULT = "/home/jovyan/work/data/nfs_shared_data/Raute/JsonForSchoolProjectTest/VerifiedPairs.csv"
    pathToPeelJson = string, DEFAULT = '/home/jovyan/work/raute_data/NewPeel/'
    pathToDryJson = string, DEFAULT = '/home/jovyan/work/raute_data/NewDry/'
    printProgress = bool, if True (DEFAULT) prints how manieth file is being processed of total
    pushToDatabase= bool, if True data is pushed to database and nothing is returned, if False full feature and target matrixes are returned
    chunksize = int or None, if None data is pushed as a whole to database, otherwise in desired chunksize
    featuresTableName=None or string
    targetTableName=None or string, if both featuresTableName and targetTableName has a name, seperate tables will be created for them to database
    combinedTableName=string or None (default='PreprocesseddData') if not None, combined table will be created which has both features and target at the same table
    host = container ip
    user = username to your container
    password = password to your mariadb
    database = Database name where you want to push the data
    port = Port number of your container
    unique = If you want to make new tables which dont allow duplicate values then give this True

    Example
    -------
    
    df_features, df_target = create_full_feature_and_target_matrix(printProgress=True)
    
    If default values are fine with you, but you want to see printing, that's all you need to do.
    
    If pushing to database:
   
    create_full_feature_and_target_matrix(pushToDatabase=True,chunksize=1000, featuresTableName = 'featuretable', targetTableName = 'targettable', combinedTableName='PreprocessedData, unique = True)
    
    Project dependencies
    --------------------
    from Preprocess.readjson import readJson
    from Preprocess.feature_matrix import featureMatrix
    
    
    """
    from Preprocess.readjson import readJson
    from Preprocess.feature_matrix import featureMatrix
    from Preprocess.chunker import write_to_db, connection
    import pandas as pd
    import numpy as np
    import os

    
    pairs = pd.read_csv(fullpathToPairsCsv)

    pairs['pFile']=pairs.pFile.str.replace('bmp','json')
    pairs['dFile']=pairs.dFile.str.replace('bmp','json')

    df_features = pd.DataFrame()
    df_target = pd.DataFrame()
    nan_rows = []
    shrinkage_above_one = []
    if pushToDatabase == True:
        connection, db = connection(host, user, password, database, port)
        mycursor = db.cursor()
        
    
    amount_of_files = len(pairs['pFile'])
    if printProgress == True: print(f"0/{amount_of_files}\tdropped nan-rows {len(nan_rows)}\tdropped too big shrinkage rows {len(shrinkage_above_one)}",end="\r")
    pairset = enumerate(zip(pairs['pFile'], pairs['dFile']))
    length = len(list(zip(pairs['pFile'], pairs['dFile'])))

    if featuresTableName != None and targetTableName != None and unique == True and pushToDatabase == True:
                    query = f'CREATE TABLE {featuresTableName} (peelFile VARCHAR(255) UNIQUE, m_uWidth FLOAT, m_uLength FLOAT, m_dThickness FLOAT, B1MoistureAvg FLOAT, B1TemperatureAvg FLOAT, B1DensityAvg FLOAT, B1KnotCount FLOAT, B1KnotWidthSum FLOAT, B1DecayCount FLOAT, B1DecayWidthSum FLOAT, B1AllOtherDefectCount FLOAT, B1AllOtherDefectWidthSum FLOAT, B2MoistureAvg FLOAT, B2TemperatureAvg FLOAT, B2DensityAvg FLOAT, B2KnotCount FLOAT, B2KnotWidthSum FLOAT, B2DecayCount FLOAT, B2DecayWidthSum FLOAT, B2AllOtherDefectCount FLOAT, B2AllOtherDefectWidthSum FLOAT, B3MoistureAvg FLOAT, B3TemperatureAvg FLOAT, B3DensityAvg FLOAT, B3KnotCount FLOAT, B3KnotWidthSum FLOAT, B3DecayCount FLOAT, B3DecayWidthSum FLOAT, B3AllOtherDefectCount FLOAT, B3AllOtherDefectWidthSum FLOAT, B4MoistureAvg FLOAT, B4TemperatureAvg FLOAT, B4DensityAvg FLOAT, B4KnotCount FLOAT, B4KnotWidthSum FLOAT, B4DecayCount FLOAT, B4DecayWidthSum FLOAT, B4AllOtherDefectCount FLOAT, B4AllOtherDefectWidthSum FLOAT, B5MoistureAvg FLOAT, B5TemperatureAvg FLOAT, B5DensityAvg FLOAT, B5KnotCount FLOAT, B5KnotWidthSum FLOAT, B5DecayCount FLOAT, B5DecayWidthSum FLOAT, B5AllOtherDefectCount FLOAT, B5AllOtherDefectWidthSum FLOAT, B6MoistureAvg FLOAT, B6TemperatureAvg FLOAT, B6DensityAvg FLOAT, B6KnotCount FLOAT, B6KnotWidthSum FLOAT, B6DecayCount FLOAT, B6DecayWidthSum FLOAT, B6AllOtherDefectCount FLOAT, B6AllOtherDefectWidthSum FLOAT, B7MoistureAvg FLOAT, B7TemperatureAvg FLOAT, B7DensityAvg FLOAT, B7KnotCount FLOAT, B7KnotWidthSum FLOAT, B7DecayCount FLOAT, B7DecayWidthSum FLOAT, B7AllOtherDefectCount FLOAT, B7AllOtherDefectWidthSum FLOAT, B8MoistureAvg FLOAT, B8TemperatureAvg FLOAT, B8DensityAvg FLOAT, B8KnotCount FLOAT, B8KnotWidthSum FLOAT, B8DecayCount FLOAT,  B8DecayWidthSum FLOAT, B8AllOtherDefectCount FLOAT, B8AllOtherDefectWidthSum FLOAT, B9MoistureAvg FLOAT, B9TemperatureAvg FLOAT, B9DensityAvg FLOAT, B9KnotCount FLOAT, B9KnotWidthSum FLOAT, B9DecayCount FLOAT, B9DecayWidthSum FLOAT, B9AllOtherDefectCount FLOAT, B9AllOtherDefectWidthSum FLOAT, dryMoisturePercentage FLOAT, traindevtest INT);'
                    mycursor.execute(query)
            
                    query2 = f'CREATE TABLE {targetTableName} (dryFile VARCHAR(255) UNIQUE, dryWidth FLOAT, dryShrinkage FLOAT);'
                    mycursor.execute(query2)
    elif pushToDatabase == True and combinedTableName != None and unique == True:
                    query3 = f'CREATE TABLE {combinedTableName} (peelFile VARCHAR(255) UNIQUE, m_uWidth FLOAT, m_uLength FLOAT, m_dThickness FLOAT, B1MoistureAvg FLOAT, B1TemperatureAvg FLOAT, B1DensityAvg FLOAT, B1KnotCount FLOAT, B1KnotWidthSum FLOAT, B1DecayCount FLOAT, B1DecayWidthSum FLOAT, B1AllOtherDefectCount FLOAT, B1AllOtherDefectWidthSum FLOAT, B2MoistureAvg FLOAT, B2TemperatureAvg FLOAT, B2DensityAvg FLOAT, B2KnotCount FLOAT, B2KnotWidthSum FLOAT, B2DecayCount FLOAT, B2DecayWidthSum FLOAT, B2AllOtherDefectCount FLOAT, B2AllOtherDefectWidthSum FLOAT, B3MoistureAvg FLOAT, B3TemperatureAvg FLOAT, B3DensityAvg FLOAT, B3KnotCount FLOAT, B3KnotWidthSum FLOAT, B3DecayCount FLOAT, B3DecayWidthSum FLOAT, B3AllOtherDefectCount FLOAT, B3AllOtherDefectWidthSum FLOAT, B4MoistureAvg FLOAT, B4TemperatureAvg FLOAT, B4DensityAvg FLOAT, B4KnotCount FLOAT, B4KnotWidthSum FLOAT, B4DecayCount FLOAT, B4DecayWidthSum FLOAT, B4AllOtherDefectCount FLOAT, B4AllOtherDefectWidthSum FLOAT, B5MoistureAvg FLOAT, B5TemperatureAvg FLOAT, B5DensityAvg FLOAT, B5KnotCount FLOAT, B5KnotWidthSum FLOAT, B5DecayCount FLOAT, B5DecayWidthSum FLOAT, B5AllOtherDefectCount FLOAT, B5AllOtherDefectWidthSum FLOAT, B6MoistureAvg FLOAT, B6TemperatureAvg FLOAT, B6DensityAvg FLOAT, B6KnotCount FLOAT, B6KnotWidthSum FLOAT, B6DecayCount FLOAT, B6DecayWidthSum FLOAT, B6AllOtherDefectCount FLOAT, B6AllOtherDefectWidthSum FLOAT, B7MoistureAvg FLOAT, B7TemperatureAvg FLOAT, B7DensityAvg FLOAT, B7KnotCount FLOAT, B7KnotWidthSum FLOAT, B7DecayCount FLOAT, B7DecayWidthSum FLOAT, B7AllOtherDefectCount FLOAT, B7AllOtherDefectWidthSum FLOAT, B8MoistureAvg FLOAT, B8TemperatureAvg FLOAT, B8DensityAvg FLOAT, B8KnotCount FLOAT, B8KnotWidthSum FLOAT, B8DecayCount FLOAT,  B8DecayWidthSum FLOAT, B8AllOtherDefectCount FLOAT, B8AllOtherDefectWidthSum FLOAT, B9MoistureAvg FLOAT, B9TemperatureAvg FLOAT, B9DensityAvg FLOAT, B9KnotCount FLOAT, B9KnotWidthSum FLOAT, B9DecayCount FLOAT, B9DecayWidthSum FLOAT, B9AllOtherDefectCount FLOAT, B9AllOtherDefectWidthSum FLOAT, dryMoisturePercentage FLOAT, traindevtest INT, dryFile VARCHAR(255) UNIQUE, dryWidth FLOAT, dryShrinkage FLOAT);'
                    mycursor.execute(query3)
    for i, files in pairset:
        peel_file, dry_file = files
        skip_last_row = 0 # If last row will be skipped, loop still must go to the point of return or pushing to database (without appending last row)    

        try:
            # Feature matrix
            current_peelfile_fullpath = os.path.join(pathToPeelJson,peel_file)
            current_row = featureMatrix(current_peelfile_fullpath)
            # Checking for NaNs in current_row of feature matrix, if True don't append but skip (except for last row there is different behaviour)
            if current_row.iloc[0].isna().any(axis=0) == True:
                nan_rows.append(peel_file)
                if printProgress == True: print(f"{i}/{amount_of_files}\tdropped nan-rows {len(nan_rows)}\tdropped too big shrinkage rows {len(shrinkage_above_one)}",end="\r")
                if i != length-1: # If not last row, continue loop with next iteration
                    continue
                elif i == length-1: # If last row, go untill pushing to database or return without appending last row
                    skip_last_row = 1
            
            
            # Target matrix
            current_dryfile_fullpath = os.path.join(pathToDryJson,dry_file)
            dry = readJson(onefile=current_dryfile_fullpath)

            # Creating dictionary for dry data to-be-converted to dataframe
            dry_data = {"dryFile":[dry['FileName']],
                        "dryWidth":[dry['ObjectData'][0]['m_uWidth']],
                        "dryShrinkage":[dry['ObjectData'][0]['m_uWidth']/current_row['m_uWidth'][0]]} # shrinkage = dryWidth/peelWidth
            
            # Adding dryMoisturePercentage, and traindevtest to current_row of feature matrix
            current_row['dryMoisturePercentage'] = dry['ObjectData'][0]['m_dMoisturePercentage']
            current_row['traindevtest']= np.random.choice([1,2,3],size=1,p=[0.8,0.1,0.1])

            # Converting dry_data to dataframe
            dry_data = pd.DataFrame(dry_data)

            # Sanity checking dryShrinkage, if doesn't pass don't append but skip (except for last row there is different behaviour)
            if dry_data.iloc[0]['dryShrinkage'] > 1:
                shrinkage_above_one.append(dry_file)
                if printProgress == True: print(f"{i}/{amount_of_files}\tdropped nan-rows {len(nan_rows)}\tdropped too big shrinkage rows {len(shrinkage_above_one)}",end="\r")
                if i != length-1: # If not last row, continue loop with next iteration
                    continue
                elif i == length-1: # If last row, go untill pushing to database or return without appending last row
                    skip_last_row = 1
            
            # Appending data
            if skip_last_row == 0:
                df_features=df_features.append(current_row, ignore_index = True)
                df_target=df_target.append(dry_data, ignore_index = True)
            if pushToDatabase == True and (df_features.shape[0] == chunksize or i == length-1) and chunksize != None:

                if featuresTableName != None and targetTableName != None:
                    if df_features.shape[0] == chunksize or i == length-1: # take chunksize as a parameter
                        write_to_db(df_features, connection, featuresTableName, chunksize)
                        df_features = df_features.iloc[0:0]
                    if df_target.shape[0] == chunksize or i == length-1:
                        write_to_db(df_target, connection, targetTableName, chunksize)
                        df_target = df_target.iloc[0:0]
                                 
                
                if combinedTableName != None:
                        df = df_features.join(df_target)
                        write_to_db(df, connection, combinedTableName, chunksize)
                        df_target = df_target.iloc[0:0]
                        df = df.iloc[0:0]
                        df_features = df_features.iloc[0:0]
            
        except KeyError:
            pass
        if printProgress == True: print(f"{i+1}/{amount_of_files}\tdropped nan-rows {len(nan_rows)}\tdropped too big shrinkage rows {len(shrinkage_above_one)}",end="\r")

    if pushToDatabase == True and chunksize != None:
        print("All done.")
    # Return dataframes only if chunking is off
    elif pushToDatabase == True and chunksize == None:
        df = df_features.join(df_target)
        df.to_sql(combinedTableName, connection, if_exists='append', index = False)
        print("All done.")
    elif pushToDatabase == False:
        return df_features, df_target

def featureMatrix_furrycap(fullpathToPairsCsv="/home/jovyan/work/data/nfs_shared_data/Raute/JsonForSchoolProjectTest/VerifiedPairs.csv",
    pathToPeelJson='/home/jovyan/work/raute_data/NewPeel/',
    pathToDryJson='/home/jovyan/work/raute_data/NewDry/',
    printProgress=True):
    from Modules.readjson import readJson
    import pandas as pd
    import os
   
    columns = ['peelFile','peelWidth','peelMoisture','peelTemperature','peelDensity','knotCount','knotWidthSum']
    df_karvalakki = pd.DataFrame()
    df_target_karvalakki = pd.DataFrame()
    pairs = pd.read_csv(fullpathToPairsCsv)

    pairs['pFile']=pairs.pFile.str.replace('bmp','json')
    pairs['dFile']=pairs.dFile.str.replace('bmp','json')

    df_features = pd.DataFrame()
    df_target = pd.DataFrame()

    amount_of_files = len(pairs['pFile'])
    if printProgress == True: print(f"0/{amount_of_files}",end="\r")
    for i, files in enumerate(zip(pairs['pFile'], pairs['dFile'])):
        peel_file, dry_file = files      
        try:
            # Feature matrix
            current_peelfile_fullpath = os.path.join(pathToPeelJson,peel_file)
            sheet = readJson(onefile=current_peelfile_fullpath)

            defects = pd.json_normalize(sheet['Defects'])
            try:
                knots = pd.DataFrame(defects.loc[defects['m_ObjDefectName'].str.endswith('KNOT')]['m_dOriginalFeatures'].to_list())[1]
                knotcount = knots.count()
                knotwidth = knots.sum()
            except:
                knotcount = 0
                knotwidth = 0
            data = [[sheet['FileName']],[sheet['ObjectData'][0]['m_uWidth']],[sheet['ObjectData'][0]['m_dMoisturePercentage']],[sheet['ObjectData'][0]['m_dTemperature']],[sheet['ObjectData'][1]['m_dDensityValue']],[knotcount],[knotwidth]]
            asdict = {key:value for key,value in zip(columns,data)}
            current_row = pd.DataFrame(data=asdict)
            df_karvalakki = df_karvalakki.append(current_row,ignore_index=True)

            # Target matrix
            current_dryfile_fullpath = os.path.join(pathToDryJson,dry_file)
            dry = readJson(onefile=current_dryfile_fullpath)
            dry_data = {"dryFile":[dry['FileName']],
                        "dryWidth":[dry['ObjectData'][0]['m_uWidth']]}
            df_target_karvalakki=df_target_karvalakki.append(pd.DataFrame(dry_data), ignore_index = True)

        except KeyError:
            pass
        if printProgress == True: print(f"{i+1}/{amount_of_files}",end="\r")
    return df_karvalakki, df_target_karvalakki
