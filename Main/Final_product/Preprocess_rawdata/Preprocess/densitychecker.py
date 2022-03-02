from Preprocess.coordinates import coordinates
from Preprocess.createColumns import createColumns
import pandas as pd
import numpy as np

def densityCheck(data, B1_density,B3_density,B4_density,B6_density,B7_density,B9_density):
    
    """
    ------------------
    VERSION 29/11/2021
    ------------------
    Function is for determining values for blocks without any sensors. This avoids NaN -values and we can save the sheet.
    This saves all sheets which have about half of sensor left.
    
    
    ARGS : 
        - data : JSON-file
        - B{1-9}_density : Dataframe of block's density sensors 
         
    
    RETURNS : 
        - Densities for blocks without any sensors :
        - B3DensityAvg, B6DensityAvg, B9DensityAvg
    
    """
    
    df_DensityBlocks = pd.json_normalize(data["DensityBlocks"])
    X_coordinates = []
    
    for key in df_DensityBlocks.keys():
        if '.x' in key:
            X_coordinates += df_DensityBlocks[key].to_list()
    X_coordinate_unique = list(set(X_coordinates))
    
    # There are sensors on the other side only (generally left only)
    if len(X_coordinate_unique) == 2: 
               
        # Determine the values for the blocks on the right from the averages of the left-side blocks
        B3DensityAvg = (B1_density['Density'].mean() + B4_density['Density'].mean() + B7_density['Density'].mean()) / 3
        B6DensityAvg = B3DensityAvg
        B9DensityAvg = B6DensityAvg
        return B3DensityAvg, B6DensityAvg, B9DensityAvg

    if len(X_coordinate_unique) == 4:            

        if len(B3_density) == 0:

            if len(B6_density) != 0:
                B3DensityAvg = (B1_density['Density'].mean() + B4_density['Density'].mean() + B7_density['Density'].mean() + B6_density['Density'].mean() + B9_density['Density'].mean()) / 5
                return B3DensityAvg
            else: 
                B3DensityAvg = (B1_density['Density'].mean() + B4_density['Density'].mean() + B7_density['Density'].mean() + B9_density['Density'].mean()) / 4
                B6DensityAvg = B3DensityAvg
                return B3DensityAvg, B6DensityAvg

        if len(B6_density) == 0 :
            B6DensityAvg = (B1_density['Density'].mean() + B4_density['Density'].mean() + B7_density['Density'].mean() + B3_density['Density'].mean()) / 4            
            B9DensityAvg = (B1_density['Density'].mean() + B4_density['Density'].mean() + B7_density['Density'].mean() + B3_density['Density'].mean() + B6DensityAvg) / 5
            return B6DensityAvg, B9DensityAvg

        elif len(B9_density) == 0:
            B9DensityAvg = (B1_density['Density'].mean() + B4_density['Density'].mean() + B7_density['Density'].mean() + B3_density['Density'].mean() + B6_density['Density'].mean()) / 5
            return B9DensityAvg
        
    
def recalculation(B1_density,B3_density,B4_density,B6_density,B7_density,B9_density):
    """
    ------------------
    VERSION 29/11/2021
    ------------------
    
    Checks if block has too few sensors for averaging density value
    
    ARGS : 
        - data : JSON-file
        - B{1-9}_density : Dataframe of block's density sensors 
         
    RETURNS : 
        - B1DensityAvg, B4DensityAvg, B6DensityAvg, B9DensityAvg

    """
    
    # Block 1 
    if (len(B1_density)<5):      
        if (len(B4_density) >= (len(B7_density))): 
            B1DensityAvg = B4_density['Density'].mean()
            return B1DensityAvg            
        else:
            B1DensityAvg = B7_density['Density'].mean()
            return B1DensityAvg
                       
    # Block 4 
    if (len(B4_density) < 5):
        if (len(B7_density) >= (len(B1_density))): 
            B4DensityAvg = B7_density['Density'].mean()
            return B4DensityAvg            
        else:
            B4DensityAvg = B1_density['Density'].mean()
            return B4DensityAvg
                      
    # Block 7
    if (len(B7_density)<5):
        if (len(B4_density) >= (len(B1_density))): 
            B7DensityAvg = B4_density['Density'].mean()
            return B7DensityAvg
        else:
            B7DensityAvg = B1_density['Density'].mean()
            return B7DensityAvg
            
    # ---------- Right side ----------        
                        
    # Block 3 
    if (len(B3_density)<5):
        if (len(B6_density) >= (len(B9_density))): 
            B3DensityAvg = B6_density['Density'].mean()
            return B3DensityAvg            
        else:
            B3DensityAvg = B9_density['Density'].mean()
            return B3DensityAvg
                       
    # Block 6 
    if (len(B6_density) < 5):
        if (len(B3_density) >= (len(B9_density))): 
            B6DensityAvg = B3_density['Density'].mean()
            return B6DensityAvg            
        else:
            B6DensityAvg = B9_density['Density'].mean()
            return B6DensityAvg
                      
    # Block 9
    if (len(B9_density)<5):
        if (len(B6_density) >= (len(B3_density))): 
            B9DensityAvg = B6_density['Density'].mean()
            return B9DensityAvg
        else:
            B9DensityAvg = B3_density['Density'].mean()
            return B9DensityAvg
                        
