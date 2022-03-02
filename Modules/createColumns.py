import sys
import json
import pandas as pd 
import numpy as np

def createColumns(data):
    """
    ------------------------
     VERSION: 19/11/2021
    ------------------------
    
    A function that creates columns from given a data file. Columns are necessary for other preprocessing functions.
    
    
    EXAMPLE HOW TO DEFINE COORDINATES OF THE SHEET:
    -----------------------------------------------
    
    df_Defects, df_DensityBlocks, df_MoistureBlocks, df_OriginalFeatures, basic_features, df_ObjectData = columns('/home/jovyan/work/data/nfs_shared_data/Raute/JsonForSchoolProjectTest/Peel/20210505123334_85.json')
    
    in other function (e.q. coordinatesV2.py):
    df_Defects, df_DensityBlocks, df_MoistureBlocks, df_OriginalFeatures, basic_features, df_ObjectData = columns(dataPath)
    
    
    Parameter(s)
    ----------
    
    data :
        - JSON-file
        
    Returns
    -------
    
    df_Defects, df_DensityBlocks, df_MoistureBlocks, basic_features, df_ObjectData
    
    """
    
    fileName = data['FileName']
    
    
    # Creating columns from object data
    FIELDS = ["m_uWidth", "m_uLength","m_dThickness","ObjectResX", "ObjectResY"]
    df_ObjectData = pd.json_normalize(data["ObjectData"][0])
    df_ObjectData.drop(columns=df_ObjectData.columns.difference(FIELDS),inplace=True)
    
    # Moisture block coordinates
    df_MoistureBlocks = pd.json_normalize(data["MoistureBlocks"])
    df_coordinates = df_MoistureBlocks.drop(columns=["m_dCalculatedFeatures","FeaturesExplained"])
    
    # Temperature- and moisture values from moisture sensors
    df_calculatedFeatures = pd.DataFrame(df_MoistureBlocks["m_dCalculatedFeatures"].to_list(), columns=['Moisture', 'Temperature'])

    
    # Join calculated values and coordinates together
    df_MoistureBlocks = df_calculatedFeatures.join(df_coordinates)
    
    df_DensityBlocks = pd.json_normalize(data["DensityBlocks"])

    # Defects 
    # Jos arkissa ei ole yhtään vikaa, luodaan kuitenkin sarakkeet, mutta täytetään ne nollilla
    if len(data['Defects']) == 0:
        df_Defects = pd.json_normalize(data["Defects"])
        zeros = np.random.randint(1, size=(1,5))
        columns = ['DEFECT_FEATURE_BOX_LENGTH','DEFECT_FEATURE_BOX_WIDTH','m_ObjDefectName', 'm_mmpntGravity.x', 'm_mmpntGravity.y']
        df_Defects = pd.DataFrame(data=zeros, columns=columns)
        df_Defects['GravityX'] = df_Defects['m_mmpntGravity.x'] / df_ObjectData['ObjectResX'][0]
        df_Defects['GravityY'] = df_Defects['m_mmpntGravity.y'] / df_ObjectData['ObjectResY'][0]
        df_Defects = df_Defects.drop(columns=["m_mmpntGravity.x","m_mmpntGravity.y"]) # Drop gravity millimeter coordinates
        defectX = df_Defects['GravityX'].to_list()
        defectY = df_Defects['GravityY'].to_list()
        basic_features = df_ObjectData.drop(columns=['ObjectResX','ObjectResY'])
        return df_Defects, df_DensityBlocks, df_MoistureBlocks, basic_features, df_ObjectData
        
        
    else: 
        df_Defects = pd.json_normalize(data["Defects"])
        df_Defects = df_Defects.drop(columns=["m_dFeatures","m_pPresentation.m_ePresentation","m_pPresentation.m_iReportingFrontEdge",
                                              "m_pPresentation.m_iPoints", "m_pPresentation.m_pntPoint", "m_mmpntRectangle.x", "m_mmpntRectangle.y"])
    
        # Values from m_dOriginalFeatures
        df_OriginalFeatures = pd.DataFrame(df_Defects["m_dOriginalFeatures"].to_list())
        df_OriginalFeatures.drop(columns=df_OriginalFeatures.columns.difference([0,1]),inplace=True)
        df_OriginalFeatures.rename(columns={0: "DEFECT_FEATURE_BOX_LENGTH",
                                            1: "DEFECT_FEATURE_BOX_WIDTH"}, inplace=True, errors='raise')

        df_Defects = df_Defects.drop(columns=["m_dOriginalFeatures","name","m_iDefectType"])

        # Join columns together
        df_Defects = df_OriginalFeatures.join(df_Defects)

        # Converting gravity coordinates to pixels
        df_Defects['GravityX'] = df_Defects['m_mmpntGravity.x'] / df_ObjectData['ObjectResX'][0]
        df_Defects['GravityY'] = df_Defects['m_mmpntGravity.y'] / df_ObjectData['ObjectResY'][0]
        df_Defects = df_Defects.drop(columns=["m_mmpntGravity.x","m_mmpntGravity.y"]) # Drop gravity millimeter coordinates


        defectX = df_Defects['GravityX'].to_list()
        defectY = df_Defects['GravityY'].to_list()

        basic_features = df_ObjectData.drop(columns=['ObjectResX','ObjectResY'])


        return df_Defects, df_DensityBlocks, df_MoistureBlocks, basic_features, df_ObjectData
    