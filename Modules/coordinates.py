import pandas as pd 
import numpy as np
import json
import matplotlib.pyplot as plt
from Modules.createColumns import createColumns

def coordinates(data):
    """
    ------------------
    VERSION 09/12/2021
    
    LATEST UPDATES:
    - Removed hard-coding from a scenario where some value(s) are missing, Nones are returned instead
    ------------------
    
    Function for creating minimum and maximum coordinates (angular coordinates) of the sheet. Coordinates are used to define the blocks in feature_matrix.py
    If possible, the function retrieves the coordinates directly from the JSON-file and if not, minimun- and maximum X are hard coded.
     
    ARGS : 
        - data : JSON-file
        
    RETURNS :
    
        min_x, min_y, max_x, max_y, firstH, secondH, firstV, secondV, firstV
        
    """
    
    fileName = data['FileName']
    
    # Create columns with function
    df_Defects, df_DensityBlocks, df_MoistureBlocks, basic_features, df_ObjectData = createColumns(data)
    
    # Coordinates to dataframe
    if len(data["ObjectData"]) > 2:
        df_coordinates = pd.json_normalize(data["ObjectData"][2])
        df_coordinates = df_coordinates.drop(columns=df_coordinates.columns.difference(['m_iDiffInReportAndDisplay','m_mmpntTopLeft.x','m_mmpntTopLeft.y','m_mmpntTopRight.x','m_mmpntTopRight.y', 'm_mmpntBottomLeft.x','m_mmpntBottomLeft.y','m_mmpntBottomRight.x','m_mmpntBottomRight.y']))

        #  minimum X-coordinate of the sheet
        if df_coordinates['m_mmpntTopLeft.x'][0] <= df_coordinates['m_mmpntBottomLeft.x'][0]:
            min_x = df_coordinates['m_mmpntTopLeft.x'][0] / df_ObjectData['ObjectResX'][0]      
        else: 
            min_x = df_coordinates['m_mmpntBottomLeft.x'][0] / df_ObjectData['ObjectResX'][0]

        # minimum Y-coordinate    
        if df_coordinates['m_mmpntTopLeft.y'][0] <= df_coordinates['m_mmpntTopRight.y'][0]:
            min_y = df_coordinates['m_mmpntTopLeft.y'][0] / df_ObjectData['ObjectResY'][0]
            min_y = min_y + df_coordinates['m_iDiffInReportAndDisplay'][0]
        else: 
            min_y = df_coordinates['m_mmpntTopRight.y'][0] / df_ObjectData['ObjectResY'][0]
            min_y = min_y + df_coordinates['m_iDiffInReportAndDisplay'][0]


        # maximum X
        if df_coordinates['m_mmpntTopRight.x'][0] >= df_coordinates['m_mmpntBottomRight.x'][0]:
            max_x = df_coordinates['m_mmpntTopRight.x'][0] / df_ObjectData['ObjectResX'][0]        
        else:
            max_x = df_coordinates['m_mmpntBottomRight.x'][0] / df_ObjectData['ObjectResX'][0]

        # maximum Y
        if df_coordinates['m_mmpntBottomLeft.y'][0] >= df_coordinates['m_mmpntBottomRight.y'][0]:
            max_y = df_coordinates['m_mmpntBottomLeft.y'][0] / df_ObjectData['ObjectResY'][0]
            max_y = max_y + df_coordinates['m_iDiffInReportAndDisplay'][0]
        else:
            max_y = df_coordinates['m_mmpntBottomRight.y'][0] / df_ObjectData['ObjectResY'][0]
            max_y = max_y + df_coordinates['m_iDiffInReportAndDisplay'][0]
    
    else:
        # If some value is missing, return all as Nones so that full feature matrix creator knows to delete row later
        return None, None, None, None, None, None, None, None
        

    # Minimum values mustn't be less than zero 
    min_x = 0 if float(min_x) < 0 else float(min_x)
    min_y = 0 if float(min_y) < 0 else float(min_y)
    
    # Horizontal
#     firstH = max_y / 3
    firstH = (max_y - min_y)/3 + min_y
#     secondH = firstH * 2
    secondH = firstH + (max_y - min_y) / 3
    
    # Vertical
    firstV = (max_x-min_x) / 3
    secondV = firstV * 2 + min_x
    firstV = firstV + min_x
        
    return  min_x, min_y, max_x, max_y, firstH, secondH, firstV, secondV
