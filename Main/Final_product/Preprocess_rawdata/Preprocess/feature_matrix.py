import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from Preprocess.coordinates import coordinates
from Modules.createColumns import createColumns
from PIL import Image
from Preprocess.extractimage import extractImage
from timeit import default_timer as timer
import json
import os
from Preprocess.densitychecker import *


def featureMatrix(dataPath="/home/jovyan/work/raute_data/NewDry/20210505151241_35.json",
                  blockplot=False,
                  datxPath="/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Sorvi/koivu/testRun20210505",
                  prints=False):
    """
    ------------------------
    VERSION: 09/12/2021 
    ------------------------
    
    LAST UPDATE(S) :
            - Added checking for None values after calling coordinates-function
            - Updated densitychecker blocks that have too few sensors for averaging density value
            - Conditions done in loop
            - Plotting for "All" fixed when there are no density sensors at all
            - Density values for blocks with missing sensors by "densitychecker.py"
    
    
    DESCRIPTION :
        A function that creates feature matrix of the given JSON-file. If necessary, it's also possible to plot image or just a single block to make sure
        that function works properly. 
    
    ARGS :     
        dataPath :
            - Path to the JSON-file 
            - Example: '/home/jovyan/work/data/nfs_shared_data/Raute/JsonForSchoolProjectTest/Peel/20210505123334_85.json'
            
        blockplot :
            - Plots all blocks or only one selected block on the sheet's image.
            - Default : False
            - "All" : Plots all nine blocks on image.
            - (1-9) : Plots block of given number.
            
        datxPath : 
            - The path to the folder that contains the images that will be extracted for plot
            - Default : /home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Sorvi/koivu/testRun20210505
            
        prints : 
            - If True, function prints it's progress e.q. filename. Mainly for debugging.
            - Default : False
            
    EXAMPLES :
        features = featureMatrix('data/nfs_shared_data/Raute/JsonForSchoolProjectTest/Peel/20210505123334_85.json',"All")
        features = featureMatrix('data/nfs_shared_data/Raute/JsonForSchoolProjectTest/Peel/20210505123334_85.json', 9)
        
        features = featureMatrix('data/nfs_shared_data/Raute/JsonForSchoolProjectTest/Peel/20210505123334_85.json',prints=True
        features = featureMatrix('data/nfs_shared_data/Raute/JsonForSchoolProjectTest/Peel/20210505123334_85.json')
        
    FOR DISPLAYING ALL COLUMNS USE:
        pd.set_option('display.max_columns', None)
        
    RETURNS :
        feature matrix of the given JSON-file

    """
       
    start = timer()    
    
    with open(dataPath,'r') as f:
        data = json.load(f)
        
    fileName = data['FileName']
    if prints==True:
        print(f"Filename: {fileName}")
       
    # Creating columns using function
    df_Defects, df_DensityBlocks, df_MoistureBlocks, basic_features, df_ObjectData = createColumns(data)
    # Get coordinates of the given sheet
    min_x, min_y, max_x, max_y, firstH, secondH, firstV, secondV = coordinates(data)
    # Checking if there are None values in coordinates, if so dataframe with one NaN value is returned that full feature matrix creator can delete the row
    if min_x == None or min_y == None or max_x == None or max_y == None or firstH == None or secondH == None or firstV == None or secondV == None:
        return pd.DataFrame(data=[np.nan],columns=["empty"])
    ###  -----------------   BLOCKS    -----------------

    x_values = [min_x-1, firstV, secondV, max_x+1]
    y_values = [min_y-1, firstH, secondH, max_y+1]
    B_all_Mconditions = []
    B_all_Dconditions = []
    x_index = 0
    y_index = 0

    for blocknumber in range(1,10):
        BCurrentMCondition = (
            ((df_MoistureBlocks['m_pntTL.x'] <= x_values[x_index+1]) & (df_MoistureBlocks['m_pntTL.y'] <= y_values[y_index+1]) & (df_MoistureBlocks['m_pntTL.x'] > x_values[x_index]) & (df_MoistureBlocks['m_pntTL.y'] > y_values[y_index])) |

            ((df_MoistureBlocks['m_pntTR.x'] <= x_values[x_index+1]) & (df_MoistureBlocks['m_pntTR.y'] <= y_values[y_index+1]) & (df_MoistureBlocks['m_pntTR.x'] > x_values[x_index]) & (df_MoistureBlocks['m_pntTR.y'] > y_values[y_index])) |

            ((df_MoistureBlocks['m_pntBL.x'] <= x_values[x_index+1]) & (df_MoistureBlocks['m_pntBL.y'] <= y_values[y_index+1]) & (df_MoistureBlocks['m_pntBL.x'] > x_values[x_index]) & (df_MoistureBlocks['m_pntBL.y'] > y_values[y_index])) |

            ((df_MoistureBlocks['m_pntBR.x'] <= x_values[x_index+1]) & (df_MoistureBlocks['m_pntBR.y'] <= y_values[y_index+1]) & (df_MoistureBlocks['m_pntBR.x'] > x_values[x_index]) & (df_MoistureBlocks['m_pntBR.y'] > y_values[y_index]))
        )
        B_all_Mconditions.append(BCurrentMCondition)
        
        if len(data['DensityBlocks']) != 0:
            BCurrentDCondition = (
                ((df_DensityBlocks['m_pntTL.x'] <= x_values[x_index+1]) & (df_DensityBlocks['m_pntTL.y'] <= y_values[y_index+1]) & (df_DensityBlocks['m_pntTL.x'] > x_values[x_index]) & (df_DensityBlocks['m_pntTL.y'] > y_values[y_index])) |

                ((df_DensityBlocks['m_pntTR.x'] <= x_values[x_index+1]) & (df_DensityBlocks['m_pntTR.y'] <= y_values[y_index+1]) & (df_DensityBlocks['m_pntTR.x'] > x_values[x_index]) & (df_DensityBlocks['m_pntTR.y'] > y_values[y_index])) |

                ((df_DensityBlocks['m_pntBL.x'] <= x_values[x_index+1]) & (df_DensityBlocks['m_pntBL.y'] <= y_values[y_index+1]) & (df_DensityBlocks['m_pntBL.x'] > x_values[x_index]) & (df_DensityBlocks['m_pntBL.y'] > y_values[y_index])) |

                ((df_DensityBlocks['m_pntBR.x'] <= x_values[x_index+1]) & (df_DensityBlocks['m_pntBR.y'] <= y_values[y_index+1]) & (df_DensityBlocks['m_pntBR.x'] > x_values[x_index]) & (df_DensityBlocks['m_pntBR.y'] > y_values[y_index]))
            )
            B_all_Dconditions.append(BCurrentDCondition)

        x_index += 1
        if x_index == 3:
            y_index += 1
            x_index = 0
    

    # Block 1

    # -----------Moisture-----------                 
    B1_Mcondition = B_all_Mconditions[0]
    B1_moisture = df_MoistureBlocks.loc[B1_Mcondition]

    m1X = []
    for key in B1_moisture.keys():
        if '.x' in key:
            m1X += B1_moisture[key].to_list()

    m1Y = []
    for key in B1_moisture.keys():
        if '.y' in key:
            m1Y += B1_moisture[key].to_list()

    # -----------Density-----------
    if len(data['DensityBlocks']) != 0:
        B1_Dcondition = B_all_Dconditions[0]
        B1_density = df_DensityBlocks.loc[B1_Dcondition]

        d1X = []
        for key in B1_density.keys():
            if '.x' in key:
                d1X += B1_density[key].to_list()

        d1Y = []
        for key in B1_density.keys():
            if '.y' in key:
                d1Y += B1_density[key].to_list()
    else:
        df_DensityBlocks = pd.json_normalize(data['DensityBlocks'])
        zeros = np.random.randint(1, size=(1,9))
        columns = ['Density','m_pntTL.x','m_pntTL.y','m_pntTR.x','m_pntTR.y','m_pntBL.x','m_pntBL.y','m_pntBR.x','m_pntBR.y']
        df_density = pd.DataFrame(data=zeros, columns=columns)
        B1_density = df_density.replace(0,np.nan)
    
    # Block 2

    # -----------Moisture-----------
    B2_Mcondition = B_all_Mconditions[1]
    B2_moisture = df_MoistureBlocks.loc[B2_Mcondition]

    m2X = []
    for key in B2_moisture.keys():
        if '.x' in key:
            m2X += B2_moisture[key].to_list()

    m2Y = []
    for key in B2_moisture.keys():
        if '.y' in key:
            m2Y += B2_moisture[key].to_list()


    # Block 3

    # -----------Moisture-------------
    B3_Mcondition = B_all_Mconditions[2]
    B3_moisture = df_MoistureBlocks.loc[B3_Mcondition]

    m3X = []
    for key in B3_moisture.keys():
        if '.x' in key:
            m3X += B3_moisture[key].to_list()

    m3Y = []
    for key in B3_moisture.keys():
        if '.y' in key:
            m3Y += B3_moisture[key].to_list()            

    #  ----------Density-----------
    if len(data['DensityBlocks']) != 0:
        B3_Dcondition = B_all_Dconditions[2]
        B3_density = df_DensityBlocks.loc[B3_Dcondition] 
        

        d3X = []
        for key in B3_density.keys():
            if '.x' in key:
                d3X += B3_density[key].to_list()

        d3Y = []
        for key in B3_density.keys():
            if '.y' in key:
                d3Y += B3_density[key].to_list()  
    else:
        df_DensityBlocks = pd.json_normalize(data['DensityBlocks'])
        zeros = np.random.randint(1, size=(1,9))
        columns = ['Density','m_pntTL.x','m_pntTL.y','m_pntTR.x','m_pntTR.y','m_pntBL.x','m_pntBL.y','m_pntBR.x','m_pntBR.y']
        df_density = pd.DataFrame(data=zeros, columns=columns)
        B3_density = df_density.replace(0,np.nan)
        

    # Block 4

    # -----------Moisture-------------
    B4_Mcondition = B_all_Mconditions[3]
    B4_moisture = df_MoistureBlocks.loc[B4_Mcondition]

    m4X = []
    for key in B4_moisture.keys():
        if '.x' in key:
            m4X += B4_moisture[key].to_list()

    m4Y = []
    for key in B4_moisture.keys():
        if '.y' in key:
            m4Y += B4_moisture[key].to_list()

    #  ----------Density-----------
    if len(data['DensityBlocks']) != 0:
        B4_Dcondition = B_all_Dconditions[3]
        B4_density = df_DensityBlocks.loc[B4_Dcondition] 
        
        d4X = []
        for key in B4_density.keys():
            if '.x' in key:
                d4X += B4_density[key].to_list()

        d4Y = []
        for key in B4_density.keys():
            if '.y' in key:
                d4Y += B4_density[key].to_list() 
    else:
        df_DensityBlocks = pd.json_normalize(data['DensityBlocks'])
        zeros = np.random.randint(1, size=(1,9))
        columns = ['Density','m_pntTL.x','m_pntTL.y','m_pntTR.x','m_pntTR.y','m_pntBL.x','m_pntBL.y','m_pntBR.x','m_pntBR.y']
        df_density = pd.DataFrame(data=zeros, columns=columns)
        B4_density = df_density.replace(0,np.nan)
        

    # Block 5

    # -----------Moisture-------------
    B5_Mcondition = B_all_Mconditions[4]
    B5_moisture = df_MoistureBlocks.loc[B5_Mcondition] 

    m5X = []
    for key in B5_moisture.keys():
        if '.x' in key:
            m5X += B5_moisture[key].to_list()

    m5Y = []
    for key in B5_moisture.keys():
        if '.y' in key:
            m5Y += B5_moisture[key].to_list()

    # Block 6

    # -----------Moisture-------------
    B6_Mcondition = B_all_Mconditions[5]
    B6_moisture = df_MoistureBlocks.loc[B6_Mcondition]

    m6X = []
    for key in B6_moisture.keys():
        if '.x' in key:
            m6X += B6_moisture[key].to_list()

    m6Y = []
    for key in B6_moisture.keys():
        if '.y' in key:
            m6Y += B6_moisture[key].to_list()

    #  ----------Density-----------
    if len(data['DensityBlocks']) != 0:
        B6_Dcondition = B_all_Dconditions[5]
        B6_density = df_DensityBlocks.loc[B6_Dcondition] 
   
        d6X = []
        for key in B6_density.keys():
            if '.x' in key:
                d6X += B6_density[key].to_list()

        d6Y = []
        for key in B6_density.keys():
            if '.y' in key:
                d6Y += B6_density[key].to_list()
    else:
        df_DensityBlocks = pd.json_normalize(data['DensityBlocks'])
        zeros = np.random.randint(1, size=(1,9))
        columns = ['Density','m_pntTL.x','m_pntTL.y','m_pntTR.x','m_pntTR.y','m_pntBL.x','m_pntBL.y','m_pntBR.x','m_pntBR.y']
        df_density = pd.DataFrame(data=zeros, columns=columns)
        B6_density = df_density.replace(0,np.nan)


    # Block 7

    # -----------Moisture-------------
    B7_Mcondition = B_all_Mconditions[6] 
    B7_moisture = df_MoistureBlocks.loc[B7_Mcondition] 

    m7X = []
    for key in B7_moisture.keys():
        if '.x' in key:
            m7X += B7_moisture[key].to_list()

    m7Y = []
    for key in B7_moisture.keys():
        if '.y' in key:
            m7Y += B7_moisture[key].to_list()

    #  ----------Density-----------
    if len(data['DensityBlocks']) != 0:
        B7_Dcondition = B_all_Dconditions[6]
        B7_density = df_DensityBlocks.loc[B7_Dcondition] 
           
        d7X = []
        for key in B7_density.keys():
            if '.x' in key:
                d7X += B7_density[key].to_list()

        d7Y = []
        for key in B7_density.keys():
            if '.y' in key:
                d7Y += B7_density[key].to_list()
    else:
        df_DensityBlocks = pd.json_normalize(data['DensityBlocks'])
        zeros = np.random.randint(1, size=(1,9))
        columns = ['Density','m_pntTL.x','m_pntTL.y','m_pntTR.x','m_pntTR.y','m_pntBL.x','m_pntBL.y','m_pntBR.x','m_pntBR.y']
        df_density = pd.DataFrame(data=zeros, columns=columns)
        B7_density = df_density.replace(0,np.nan)


    # Block 8

    # -----------Moisture-------------
    B8_Mcondition = B_all_Mconditions[7]
    B8_moisture = df_MoistureBlocks.loc[B8_Mcondition] 

    m8X = []
    for key in B8_moisture.keys():
        if '.x' in key:
            m8X += B8_moisture[key].to_list()

    m8Y = []
    for key in B8_moisture.keys():
        if '.y' in key:
            m8Y += B8_moisture[key].to_list()

    # Block 9

    # -----------Moisture-------------
    B9_Mcondition =  B_all_Mconditions[8]
    B9_moisture = df_MoistureBlocks.loc[B9_Mcondition] 

    m9X = []
    for key in B9_moisture.keys():
        if '.x' in key:
            m9X += B9_moisture[key].to_list()

    m9Y = []
    for key in B9_moisture.keys():
        if '.y' in key:
            m9Y += B9_moisture[key].to_list()

    #  ----------Density-----------
    if len(data['DensityBlocks']) != 0:
        B9_Dcondition = B_all_Dconditions[8]
        B9_density = df_DensityBlocks.loc[B9_Dcondition] 

        d9X = []
        for key in B9_density.keys():
            if '.x' in key:
                d9X += B9_density[key].to_list()

        d9Y = []
        for key in B9_density.keys():
            if '.y' in key:
                d9Y += B9_density[key].to_list() 
    else:
        df_DensityBlocks = pd.json_normalize(data['DensityBlocks'])
        zeros = np.random.randint(1, size=(1,9))
        columns = ['Density','m_pntTL.x','m_pntTL.y','m_pntTR.x','m_pntTR.y','m_pntBL.x','m_pntBL.y','m_pntBR.x','m_pntBR.y']
        df_density = pd.DataFrame(data=zeros, columns=columns)
        B9_density = df_density.replace(0,np.nan)

    # --------------------- CALCULATING VALUES --------------------------- 

    # ----------  BLOCK 1 ----------------

    # defects - knots
    if df_Defects['m_ObjDefectName'][0] != 0:
        B1_DefectCondition = (df_Defects['GravityX'] <= firstV) & (df_Defects['GravityY'] <= firstH)
        B1_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B1_DefectKnots = df_Defects.loc[B1_DefectCondition & B1_DefectOnlyKnots]

        # defects - decay
        B1_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B1_DefectDecayBlock = df_Defects.loc[B1_DefectCondition & B1_DefectDecay]

        # Defects - all other
        B1_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B1_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B1_defectsRest = df_Defects.loc[B1_DefectCondition & B1_defectsRestBlock]
        # Counting defects
        B1KnotsTotalWidth = B1_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B1KnotCount = B1_DefectKnots.shape[0]
        B1_DefectDecayTotalWidth = B1_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B1_DefectDecayBlockCount = B1_DefectDecayBlock.shape[0]
        B1_defectsRestTotalWidth = B1_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B1_defectsRestCount = B1_defectsRest.shape[0]
        
    elif df_Defects['m_ObjDefectName'][0] == 0:
        B1KnotsTotalWidth = 0
        B1KnotCount = 0
        B1_DefectDecayTotalWidth = 0
        B1_DefectDecayBlockCount = 0
        B1_defectsRestTotalWidth = 0
        B1_defectsRestCount = 0

    # Calculating averages
    B1MoistureAvg = B1_moisture['Moisture'].mean()
    B1TemperatureAvg = B1_moisture['Temperature'].mean()
    B1DensityAvg = B1_density['Density'].mean()

    # ----------- BLOCK 2 -------------
    if df_Defects['m_ObjDefectName'][0] != 0:
        # defects - knots
        B2_DefectCondition = (df_Defects['GravityX'] > firstV) & (df_Defects['GravityX'] <= secondV)  & (df_Defects['GravityY'] <= firstH) 
        B2_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B2_DefectKnots = df_Defects.loc[B2_DefectCondition & B2_DefectOnlyKnots]

        # defects - decay
        B2_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B2_DefectDecayBlock = df_Defects.loc[B2_DefectCondition & B2_DefectDecay]

        # Defects - all other
        B2_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B2_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B2_defectsRest = df_Defects.loc[B2_DefectCondition & B2_defectsRestBlock]
        
        # Counting defects
        B2KnotsTotalWidth = B2_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B2KnotCount = B2_DefectKnots.shape[0]
        B2_DefectDecayTotalWidth = B2_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B2_DefectDecayBlockCount = B2_DefectDecayBlock.shape[0]
        B2_defectsRestTotalWidth = B2_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B2_defectsRestCount = B2_defectsRest.shape[0]
    else:
        B2KnotsTotalWidth = 0
        B2KnotCount = 0
        B2_DefectDecayTotalWidth = 0
        B2_DefectDecayBlockCount = 0
        B2_defectsRestTotalWidth = 0
        B2_defectsRestCount = 0

    # Calculating averages
    B2MoistureAvg = B2_moisture['Moisture'].mean()
    B2TemperatureAvg = B2_moisture['Temperature'].mean()


    # --------- BLOCK 3 -----------
    if df_Defects['m_ObjDefectName'][0] != 0:

        # defects - knots
        B3_DefectCondition = (df_Defects['GravityX'] > secondV) & (df_Defects['GravityY'] <= firstH) 
        B3_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B3_DefectKnots = df_Defects.loc[B3_DefectCondition & B3_DefectOnlyKnots]

        # defects - decay
        B3_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B3_DefectDecayBlock = df_Defects.loc[B3_DefectCondition & B3_DefectDecay]

        # Defects - all other
        B3_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B3_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B3_defectsRest = df_Defects.loc[B3_DefectCondition & B3_defectsRestBlock]
        
        # Counting defects
        B3KnotsTotalWidth = B3_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B3KnotCount = B3_DefectKnots.shape[0]
        B3_DefectDecayTotalWidth = B3_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B3_DefectDecayBlockCount = B3_DefectDecayBlock.shape[0]
        B3_defectsRestTotalWidth = B3_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B3_defectsRestCount = B3_defectsRest.shape[0]
    else:
        B3KnotsTotalWidth = 0
        B3KnotCount = 0
        B3_DefectDecayTotalWidth = 0
        B3_DefectDecayBlockCount = 0
        B3_defectsRestTotalWidth = 0
        B3_defectsRestCount = 0

    # Calculating averages
    B3MoistureAvg = B3_moisture['Moisture'].mean()
    B3TemperatureAvg = B3_moisture['Temperature'].mean()
    B3DensityAvg = B3_density['Density'].mean()


    # --------- BLOCK 4 -----------
    if df_Defects['m_ObjDefectName'][0] != 0:
        # defects - knots
        B4_DefectCondition = (df_Defects['GravityX'] <= firstV) & (df_Defects['GravityY'] > firstH) & (df_Defects['GravityY'] <= secondH)
        B4_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B4_DefectKnots = df_Defects.loc[B4_DefectCondition & B4_DefectOnlyKnots]

        # defects - decay
        B4_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B4_DefectDecayBlock = df_Defects.loc[B4_DefectCondition & B4_DefectDecay]

        # Defects - all other
        B4_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B4_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B4_defectsRest = df_Defects.loc[B4_DefectCondition & B4_defectsRestBlock]
        # Counting defects
        B4KnotsTotalWidth = B4_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B4KnotCount = B4_DefectKnots.shape[0]

        B4_DefectDecayTotalWidth = B4_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B4_DefectDecayBlockCount = B4_DefectDecayBlock.shape[0]

        B4_defectsRestTotalWidth = B4_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B4_defectsRestCount = B4_defectsRest.shape[0]
    else:
        B4KnotsTotalWidth = 0
        B4KnotCount = 0
        B4_DefectDecayTotalWidth = 0
        B4_DefectDecayBlockCount = 0
        B4_defectsRestTotalWidth = 0
        B4_defectsRestCount = 0

    # Calculating averages
    B4MoistureAvg = B4_moisture['Moisture'].mean()
    B4TemperatureAvg = B4_moisture['Temperature'].mean()
    B4DensityAvg = B4_density['Density'].mean()

    # --------- BLOCK 5 -----------
    if df_Defects['m_ObjDefectName'][0] != 0:
        # defects - knots
        B5_DefectCondition = (df_Defects['GravityX'] > firstV) & (df_Defects['GravityX'] <= secondV) & (df_Defects['GravityY'] > firstH) & (df_Defects['GravityY'] <= secondH)
        B5_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B5_DefectKnots = df_Defects.loc[B5_DefectCondition & B5_DefectOnlyKnots]

        # defects - decay
        B5_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B5_DefectDecayBlock = df_Defects.loc[B5_DefectCondition & B5_DefectDecay]

        # Defects - all other
        B5_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B5_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B5_defectsRest = df_Defects.loc[B5_DefectCondition & B5_defectsRestBlock]
        
        # Counting defects
        B5KnotsTotalWidth = B5_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B5KnotCount = B5_DefectKnots.shape[0]
        B5_DefectDecayTotalWidth = B5_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B5_DefectDecayBlockCount = B5_DefectDecayBlock.shape[0]
        B5_defectsRestTotalWidth = B5_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B5_defectsRestCount = B5_defectsRest.shape[0]
    else:
        B5KnotsTotalWidth = 0
        B5KnotCount = 0
        B5_DefectDecayTotalWidth = 0
        B5_DefectDecayBlockCount = 0
        B5_defectsRestTotalWidth = 0
        B5_defectsRestCount = 0

    # Calculating averages
    B5MoistureAvg = B5_moisture['Moisture'].mean()
    B5TemperatureAvg = B5_moisture['Temperature'].mean()

    # --------- BLOCK 6 -----------
    if df_Defects['m_ObjDefectName'][0] != 0:
        # defects - knots
        B6_DefectCondition = (df_Defects['GravityX'] > secondV) & (df_Defects['GravityY'] > firstH) & (df_Defects['GravityY'] <= secondH)
        B6_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B6_DefectKnots = df_Defects.loc[B6_DefectCondition & B6_DefectOnlyKnots]

        # defects - decay
        B6_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B6_DefectDecayBlock = df_Defects.loc[B6_DefectCondition & B6_DefectDecay]

        # Defects - all other
        B6_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B6_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B6_defectsRest = df_Defects.loc[B6_DefectCondition & B6_defectsRestBlock]
        
        # Counting defects
        B6KnotsTotalWidth = B6_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B6KnotCount = B6_DefectKnots.shape[0]
        B6_DefectDecayTotalWidth = B6_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B6_DefectDecayBlockCount = B6_DefectDecayBlock.shape[0]
        B6_defectsRestTotalWidth = B6_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B6_defectsRestCount = B6_defectsRest.shape[0]
    else:
        B6KnotsTotalWidth = 0
        B6KnotCount = 0
        B6_DefectDecayTotalWidth = 0
        B6_DefectDecayBlockCount = 0
        B6_defectsRestTotalWidth = 0
        B6_defectsRestCount = 0

    # Calculating averages
    B6MoistureAvg = B6_moisture['Moisture'].mean()
    B6TemperatureAvg = B6_moisture['Temperature'].mean()
    B6DensityAvg = B6_density['Density'].mean()

    # --------- BLOCK 7 -----------
    if df_Defects['m_ObjDefectName'][0] != 0:
        # defects - knots
        B7_DefectCondition = (df_Defects['GravityX'] <= firstV) & (df_Defects['GravityY'] > secondH) 
        B7_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B7_DefectKnots = df_Defects.loc[B7_DefectCondition & B7_DefectOnlyKnots]

        # defects - decay
        B7_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B7_DefectDecayBlock = df_Defects.loc[B7_DefectCondition & B7_DefectDecay]

        # Defects - all other
        B7_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B7_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B7_defectsRest = df_Defects.loc[B7_DefectCondition & B7_defectsRestBlock]
        # Counting defects
        B7KnotsTotalWidth = B7_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B7KnotCount = B7_DefectKnots.shape[0]
        B7_DefectDecayTotalWidth = B7_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B7_DefectDecayBlockCount = B7_DefectDecayBlock.shape[0]
        B7_defectsRestTotalWidth = B7_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B7_defectsRestCount = B7_defectsRest.shape[0]
    else:
        B7KnotsTotalWidth = 0
        B7KnotCount = 0
        B7_DefectDecayTotalWidth = 0
        B7_DefectDecayBlockCount = 0
        B7_defectsRestTotalWidth = 0
        B7_defectsRestCount = 0

    # Calculating averages
    B7MoistureAvg = B7_moisture['Moisture'].mean()
    B7TemperatureAvg = B7_moisture['Temperature'].mean()
    B7DensityAvg = B7_density['Density'].mean()


    # --------- BLOCK 8 -----------
    if df_Defects['m_ObjDefectName'][0] != 0:
        # defects - knots
        B8_DefectCondition = (df_Defects['GravityX'] > firstV) & (df_Defects['GravityX'] <= secondV) & (df_Defects['GravityY'] > secondH) 
        B8_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B8_DefectKnots = df_Defects.loc[B8_DefectCondition & B8_DefectOnlyKnots]

        # defects - decay
        B8_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B8_DefectDecayBlock = df_Defects.loc[B8_DefectCondition & B8_DefectDecay]

        # Defects - all other
        B8_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B8_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B8_defectsRest = df_Defects.loc[B8_DefectCondition & B8_defectsRestBlock]
        
        # Counting defects
        B8KnotsTotalWidth = B8_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B8KnotCount = B8_DefectKnots.shape[0]
        B8_DefectDecayTotalWidth = B8_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B8_DefectDecayBlockCount = B8_DefectDecayBlock.shape[0]
        B8_defectsRestTotalWidth = B8_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B8_defectsRestCount = B8_defectsRest.shape[0]
    else:
        B8KnotsTotalWidth = 0
        B8KnotCount = 0
        B8_DefectDecayTotalWidth = 0
        B8_DefectDecayBlockCount = 0
        B8_defectsRestTotalWidth = 0
        B8_defectsRestCount = 0
    # Calculating averages
    B8MoistureAvg = B8_moisture['Moisture'].mean()
    B8TemperatureAvg = B8_moisture['Temperature'].mean()

    # --------- BLOCK 9 -----------
    if df_Defects['m_ObjDefectName'][0] != 0:
        # defects - knots
        B9_DefectCondition = (df_Defects['GravityX'] > secondV) & (df_Defects['GravityY'] > secondH) 
        B9_DefectOnlyKnots = (df_Defects['m_ObjDefectName'].str.endswith('KNOT'))
        B9_DefectKnots = df_Defects.loc[B9_DefectCondition & B9_DefectOnlyKnots]


        # defects - decay
        B9_DefectDecay = (df_Defects['m_ObjDefectName'] == 'DEFECT_DECAY') 
        B9_DefectDecayBlock = df_Defects.loc[B9_DefectCondition & B9_DefectDecay]


        # Defects - all other
        B9_defectsRest = (df_Defects['m_ObjDefectName'].str.endswith('KNOT') == False) 
        B9_defectsRestBlock = (df_Defects['m_ObjDefectName'].str.contains('KNOT') == False) & (df_Defects['m_ObjDefectName'] != 'DEFECT_DECAY')
        B9_defectsRest = df_Defects.loc[B9_DefectCondition & B9_defectsRestBlock]
        
        # Counting defects
        B9KnotsTotalWidth = B9_DefectKnots['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B9KnotCount = B9_DefectKnots.shape[0]
        B9_DefectDecayTotalWidth = B9_DefectDecayBlock['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B9_DefectDecayBlockCount = B9_DefectDecayBlock.shape[0]
        B9_defectsRestTotalWidth = B9_defectsRest['DEFECT_FEATURE_BOX_WIDTH'].sum()
        B9_defectsRestCount = B9_defectsRest.shape[0]
    else:
        B9KnotsTotalWidth = 0
        B9KnotCount = 0
        B9_DefectDecayTotalWidth = 0
        B9_DefectDecayBlockCount = 0
        B9_defectsRestTotalWidth = 0
        B9_defectsRestCount = 0

    # Calculating averages
    B9MoistureAvg = B9_moisture['Moisture'].mean()
    B9TemperatureAvg = B9_moisture['Temperature'].mean()
    B9DensityAvg = B9_density['Density'].mean()

    
    # ----------- DENSITY CHECK -----------  
    
    # Checks missing density sensors
    if len(data['DensityBlocks']) >= 40:       
        if (len(B3_density) == 0) & (len(B6_density) == 0) & (len(B9_density) == 0):
            B3DensityAvg, B6DensityAvg, B9DensityAvg = densityCheck(data, B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
            
        elif (len(B3_density) == 0) & (len(B6_density) == 0) & (len(B9_density) != 0):
            B3DensityAvg, B6DensityAvg = densityCheck(data, B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)

        elif (len(B3_density) == 0) & (len(B6_density) != 0) & (len(B9_density) != 0):        
            B3DensityAvg = densityCheck(data, B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)

        elif (len(B6_density) == 0) & (len(B9_density) == 0):            
            B6DensityAvg, B9DensityAvg = densityCheck(data, B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)

        elif (len(B6_density) == 0) & (len(B9_density) != 0):
            B6DensityAvg, _ = densityCheck(data, B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
            
        elif len(B9_density) == 0:
            B9DensityAvg = densityCheck(data, B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)

            
    # Checks if block has too few sensors for averaging density value
    if ((len(B1_density) > 1) & (len(B1_density) <5)):                                       
        B1DensityAvg = recalculation(B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
        
    if ((len(B3_density) > 1) & (len(B3_density)<5)):                                               
        B3DensityAvg = recalculation(B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
        
    if ((len(B4_density) > 1) & (len(B4_density)<5)): 
        B4DensityAvg = recalculation( B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
        
    if ((len(B6_density) > 1) & (len(B6_density)<5)):
        B6DensityAvg = recalculation(B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
        
    if ((len(B7_density) > 1) & (len(B7_density)<5)):
        B7DensityAvg = recalculation(B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
        
    if ((len(B9_density) > 1) & (len(B9_density)<5)):
        B9DensityAvg = recalculation(B1_density,B3_density,B4_density,B6_density,B7_density,B9_density)
        

    # Densities for middle blocks
    B2DensityAvg = (B1DensityAvg + B3DensityAvg) / 2 
    B5DensityAvg = (B4DensityAvg + B6DensityAvg) / 2
    B8DensityAvg = (B7DensityAvg + B9DensityAvg) / 2
     
    # -------------------------------- FEATURES TO DATAFRAME ----------------------------------------

    # BLOCK 1 features to dataframe
    basic_features['B1MoistureAvg'] = B1MoistureAvg
    basic_features['B1TemperatureAvg'] = B1TemperatureAvg
    basic_features['B1DensityAvg'] = B1DensityAvg

    basic_features['B1KnotWidthSum'] = B1KnotsTotalWidth
    basic_features['B1KnotCount'] = B1KnotCount

    basic_features['B1DecayWidthSum'] = B1_DefectDecayTotalWidth
    basic_features['B1DecayCount'] = B1_DefectDecayBlockCount

    basic_features['B1AllOtherDefectWidthSum'] = B1_defectsRestTotalWidth
    basic_features['B1AllOtherDefectCount'] = B1_defectsRestCount

    # BLOCK 2 features to dataframe        
    basic_features['B2MoistureAvg'] = B2MoistureAvg
    basic_features['B2TemperatureAvg'] = B2TemperatureAvg
    basic_features['B2DensityAvg'] = B2DensityAvg

    basic_features['B2KnotWidthSum'] = B2KnotsTotalWidth
    basic_features['B2KnotCount'] = B2KnotCount

    basic_features['B2DecayWidthSum'] = B2_DefectDecayTotalWidth
    basic_features['B2DecayCount'] = B2_DefectDecayBlockCount

    basic_features['B2AllOtherDefectWidthSum'] = B2_defectsRestTotalWidth
    basic_features['B2AllOtherDefectCount'] = B2_defectsRestCount        

    # BLOCK 3 features to dataframe
    basic_features['B3MoistureAvg'] = B3MoistureAvg
    basic_features['B3TemperatureAvg'] = B3TemperatureAvg
    basic_features['B3DensityAvg'] = B3DensityAvg

    basic_features['B3KnotWidthSum'] = B3KnotsTotalWidth
    basic_features['B3KnotCount'] = B3KnotCount

    basic_features['B3DecayWidthSum'] = B3_DefectDecayTotalWidth
    basic_features['B3DecayCount'] = B3_DefectDecayBlockCount

    basic_features['B3AllOtherDefectWidthSum'] = B3_defectsRestTotalWidth
    basic_features['B3AllOtherDefectCount'] = B3_defectsRestCount                

    # BLOCK 4 features to dataframe
    basic_features['B4MoistureAvg'] = B4MoistureAvg
    basic_features['B4TemperatureAvg'] = B4TemperatureAvg
    basic_features['B4DensityAvg'] = B4DensityAvg

    basic_features['B4KnotWidthSum'] = B4KnotsTotalWidth
    basic_features['B4KnotCount'] = B4KnotCount

    basic_features['B4DecayWidthSum'] = B4_DefectDecayTotalWidth
    basic_features['B4DecayCount'] = B4_DefectDecayBlockCount

    basic_features['B4AllOtherDefectWidthSum'] = B4_defectsRestTotalWidth
    basic_features['B4AllOtherDefectCount'] = B4_defectsRestCount                   

    # BLOCK 5 features to dataframe
    basic_features['B5MoistureAvg'] = B5MoistureAvg
    basic_features['B5TemperatureAvg'] = B5TemperatureAvg
    basic_features['B5DensityAvg'] = B5DensityAvg

    basic_features['B5KnotWidthSum'] = B5KnotsTotalWidth
    basic_features['B5KnotCount'] = B5KnotCount

    basic_features['B5DecayWidthSum'] = B5_DefectDecayTotalWidth
    basic_features['B5DecayCount'] = B5_DefectDecayBlockCount

    basic_features['B5AllOtherDefectWidthSum'] = B5_defectsRestTotalWidth
    basic_features['B5AllOtherDefectCount'] = B5_defectsRestCount          

    # BLOCK 6 features to dataframe
    basic_features['B6MoistureAvg'] = B6MoistureAvg
    basic_features['B6TemperatureAvg'] = B6TemperatureAvg
    basic_features['B6DensityAvg'] = B6DensityAvg

    basic_features['B6KnotWidthSum'] = B6KnotsTotalWidth
    basic_features['B6KnotCount'] = B6KnotCount

    basic_features['B6DecayWidthSum'] = B6_DefectDecayTotalWidth
    basic_features['B6DecayCount'] = B6_DefectDecayBlockCount

    basic_features['B6AllOtherDefectWidthSum'] = B6_defectsRestTotalWidth
    basic_features['B6AllOtherDefectCount'] = B6_defectsRestCount    

    # BLOCK 7 features to dataframe
    basic_features['B7MoistureAvg'] = B7MoistureAvg
    basic_features['B7TemperatureAvg'] = B7TemperatureAvg
    basic_features['B7DensityAvg'] = B7DensityAvg

    basic_features['B7KnotWidthSum'] = B7KnotsTotalWidth
    basic_features['B7KnotCount'] = B7KnotCount

    basic_features['B7DecayWidthSum'] = B7_DefectDecayTotalWidth
    basic_features['B7DecayCount'] = B7_DefectDecayBlockCount

    basic_features['B7AllOtherDefectWidthSum'] = B7_defectsRestTotalWidth
    basic_features['B7AllOtherDefectCount'] = B7_defectsRestCount   

    # BLOCK 8 features to dataframe
    basic_features['B8MoistureAvg'] = B8MoistureAvg
    basic_features['B8TemperatureAvg'] = B8TemperatureAvg
    basic_features['B8DensityAvg'] = B8DensityAvg

    basic_features['B8KnotWidthSum'] = B8KnotsTotalWidth
    basic_features['B8KnotCount'] = B8KnotCount

    basic_features['B8DecayWidthSum'] = B8_DefectDecayTotalWidth
    basic_features['B8DecayCount'] = B8_DefectDecayBlockCount

    basic_features['B8AllOtherDefectWidthSum'] = B8_defectsRestTotalWidth
    basic_features['B8AllOtherDefectCount'] = B8_defectsRestCount 

    # BLOCK 9 features to dataframe
    basic_features['B9MoistureAvg'] = B9MoistureAvg
    basic_features['B9TemperatureAvg'] = B9TemperatureAvg
    basic_features['B9DensityAvg'] = B9DensityAvg

    basic_features['B9KnotWidthSum'] = B9KnotsTotalWidth
    basic_features['B9KnotCount'] = B9KnotCount

    basic_features['B9DecayWidthSum'] = B9_DefectDecayTotalWidth
    basic_features['B9DecayCount'] = B9_DefectDecayBlockCount

    basic_features['B9AllOtherDefectWidthSum'] = B9_defectsRestTotalWidth
    basic_features['B9AllOtherDefectCount'] = B9_defectsRestCount
    
    # FileName to feature matrix
    basic_features.insert(0, "peelFile", [fileName])
    
                         
  # ------------------------ Plotting ------------------------

    if blockplot==1:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m1X,m1Y,label='Moisture', color='b')
        plt.scatter(d1X,d1Y,label='Density',color='red')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B1_DefectKnots['GravityX'],B1_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B1_DefectDecayBlock['GravityX'],B1_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()
            
    elif blockplot==2:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m2X,m2Y,label='Moisture', color='b')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B2_DefectKnots['GravityX'],B2_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B2_DefectDecayBlock['GravityX'],B2_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()

    elif blockplot==3:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m3X,m3Y, label='Moisture',color='b')
        plt.scatter(d3X,d3Y,label='Density',color='red')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B3_DefectKnots['GravityX'],B3_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B3_DefectDecayBlock['GravityX'],B3_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()         

    elif blockplot==4:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m4X,m4Y,label='Moisture', color='b')
        plt.scatter(d4X,d4Y,label='Density',color='red')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B4_DefectKnots['GravityX'],B4_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B4_DefectDecayBlock['GravityX'],B4_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()

    elif blockplot==5:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m5X,m5Y,label='Moisture', color='b')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B5_DefectKnots['GravityX'],B5_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B5_DefectDecayBlock['GravityX'],B5_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()

    elif blockplot==6:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m6X,m6Y,label='Moisture', color='b')
        plt.scatter(d6X,d6Y,label='Density',color='red')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B6_DefectKnots['GravityX'],B6_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B6_DefectDecayBlock['GravityX'],B6_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()

    elif blockplot==7:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m7X,m7Y,label='Moisture', color='b')
        plt.scatter(d7X,d7Y,label='Density',color='red')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B7_DefectKnots['GravityX'],B7_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B7_DefectDecayBlock['GravityX'],B7_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()

    elif blockplot==8:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m8X,m8Y,label='Moisture', color='b')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B8_DefectKnots['GravityX'],B8_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B8_DefectDecayBlock['GravityX'],B8_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()

    elif blockplot==9:
        print(f"\nPlotting block {blockplot}...\n")
        plt.figure(figsize=(12,12))
        plt.plot([min_x,max_x],[firstH,firstH], color='green')
        plt.plot([min_x,max_x],[secondH,secondH], color='green')
        plt.plot([firstV,firstV],[min_y,max_y], color='green')
        plt.plot([secondV,secondV],[min_y,max_y], color='green') 
        plt.scatter(m9X,m9Y,label='Moisture', color='b')
        plt.scatter(d9X,d9Y,label='Density', color='red')
        if df_Defects['m_ObjDefectName'][0] != 0:
            plt.scatter(B9_DefectKnots['GravityX'],B9_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B9_DefectDecayBlock['GravityX'],B9_DefectDecayBlock['GravityY'], color='orange',label='Decay')
        fullPathtoImage = os.path.join(datxPath, fileName)
        img = extractImage(fullPathtoImage)
        image = Image.open(img)
        plt.imshow(image)
        image.close()
        plt.legend()

    elif blockplot=="All" :       
        if df_Defects['m_ObjDefectName'][0] != 0:
            print(f"\nPlotting {blockplot}...\n")
            plt.figure(figsize=(12,12))           
            plt.plot([min_x,max_x],[firstH,firstH], color='green') # Grid
            plt.plot([min_x,max_x],[secondH,secondH], color='green')# Grid
            plt.plot([firstV,firstV],[min_y,max_y], color='green')# Grid
            plt.plot([secondV,secondV],[min_y,max_y], color='green') # Grid         
            plt.scatter(m1X,m1Y,label='Moisture', color='b')
            if len(data['DensityBlocks']) != 0: plt.scatter(d1X,d1Y,label='Density',color='red')         
            plt.scatter(m2X,m2Y, color='slategrey')             
            plt.scatter(m3X,m3Y, color='cornflowerblue')
            if len(data['DensityBlocks']) != 0: plt.scatter(d3X,d3Y,color='indianred')           
            plt.scatter(m4X,m4Y, color='royalblue')
            if len(data['DensityBlocks']) != 0: plt.scatter(d4X,d4Y,color='tomato')         
            plt.scatter(m5X,m5Y, color='navy')           
            plt.scatter(m6X,m6Y, color='slateblue')
            if len(data['DensityBlocks']) != 0: plt.scatter(d6X,d6Y,color='salmon')           
            plt.scatter(m7X,m7Y, color='midnightblue')
            if len(data['DensityBlocks']) != 0: plt.scatter(d7X,d7Y,color='orangered')        
            plt.scatter(m8X,m8Y, color='steelblue')            
            plt.scatter(m9X,m9Y, color='darkblue')
            if len(data['DensityBlocks']) != 0: plt.scatter(d9X,d9Y,color='darkred')         
            plt.scatter(B1_DefectKnots['GravityX'],B1_DefectKnots['GravityY'], color='yellow',label='Knots')
            plt.scatter(B1_DefectDecayBlock['GravityX'],B1_DefectDecayBlock['GravityY'], color='orange',label='Decay') 
            plt.scatter(B2_DefectKnots['GravityX'],B2_DefectKnots['GravityY'], color='khaki')
            plt.scatter(B2_DefectDecayBlock['GravityX'],B2_DefectDecayBlock['GravityY'], color='darkorange')                       
            plt.scatter(B3_DefectKnots['GravityX'],B3_DefectKnots['GravityY'], color='yellow')
            plt.scatter(B3_DefectDecayBlock['GravityX'],B3_DefectDecayBlock['GravityY'], color='orange')            
            plt.scatter(B4_DefectKnots['GravityX'],B4_DefectKnots['GravityY'], color='khaki')
            plt.scatter(B4_DefectDecayBlock['GravityX'],B4_DefectDecayBlock['GravityY'], color='darkorange')                        
            plt.scatter(B5_DefectKnots['GravityX'],B5_DefectKnots['GravityY'], color='yellow')
            plt.scatter(B5_DefectDecayBlock['GravityX'],B5_DefectDecayBlock['GravityY'], color='orange')                                   
            plt.scatter(B6_DefectKnots['GravityX'],B6_DefectKnots['GravityY'], color='khaki')
            plt.scatter(B6_DefectDecayBlock['GravityX'],B6_DefectDecayBlock['GravityY'], color='darkorange')                        
            plt.scatter(B7_DefectKnots['GravityX'],B7_DefectKnots['GravityY'], color='yellow')
            plt.scatter(B7_DefectDecayBlock['GravityX'],B7_DefectDecayBlock['GravityY'], color='orange')           
            plt.scatter(B8_DefectKnots['GravityX'],B8_DefectKnots['GravityY'], color='khaki')
            plt.scatter(B8_DefectDecayBlock['GravityX'],B8_DefectDecayBlock['GravityY'], color='darkorange')        
            plt.scatter(B9_DefectKnots['GravityX'],B9_DefectKnots['GravityY'], color='yellow')
            plt.scatter(B9_DefectDecayBlock['GravityX'],B9_DefectDecayBlock['GravityY'], color='orange')    
            fullPathtoImage = os.path.join(datxPath, fileName)
            img = extractImage(fullPathtoImage)
            image = Image.open(img)
            plt.imshow(image)
            image.close()
            plt.legend()
        else:
            print(f"\nPlotting {blockplot}...\nNO DEFECTS!")
            plt.figure(figsize=(12,12))
            plt.plot([min_x,max_x],[firstH,firstH], color='green') # Grid
            plt.plot([min_x,max_x],[secondH,secondH], color='green')# Grid
            plt.plot([firstV,firstV],[min_y,max_y], color='green')# Grid
            plt.plot([secondV,secondV],[min_y,max_y], color='green') # Grid
            plt.scatter(m1X,m1Y,label='Moisture', color='b')
            plt.scatter(d1X,d1Y,label='Density',color='red')         
            plt.scatter(m2X,m2Y, color='slategrey')             
            plt.scatter(m3X,m3Y, color='cornflowerblue')
            plt.scatter(d3X,d3Y,color='indianred')           
            plt.scatter(m4X,m4Y, color='royalblue')
            plt.scatter(d4X,d4Y,color='tomato')         
            plt.scatter(m5X,m5Y, color='navy')           
            plt.scatter(m6X,m6Y, color='slateblue')
            plt.scatter(d6X,d6Y,color='salmon')           
            plt.scatter(m7X,m7Y, color='midnightblue')
            plt.scatter(d7X,d7Y,color='orangered')        
            plt.scatter(m8X,m8Y, color='steelblue')            
            plt.scatter(m9X,m9Y, color='darkblue')
            plt.scatter(d9X,d9Y,color='darkred')
            fullPathtoImage = os.path.join(datxPath, fileName)
            img = extractImage(fullPathtoImage)
            image = Image.open(img)
            plt.imshow(image)
            image.close()
            plt.legend()
    
        features = basic_features
        end = timer()
        print("Done in", round(end-start,2),"seconds")
        return features
            
    else:
        features = basic_features
        end = timer()
        if prints==True:
            print("Done in", round(end-start,2),"seconds\n")
        return features
