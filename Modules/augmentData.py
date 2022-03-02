import pandas as pd

def addNoise(df_col):
    import numpy as np
    return df_col * np.random.choice([1.001,1.0015,0.999,0.9995],size=df_col.shape[0],p=[0.25,0.25,0.25,0.25])

def mirrorSides(df,direction="left_right"):
    """
    dircetion = "left_right", "up_down", "both"
    """
    mirror_df = df.copy()
    lr_sides_to = [1,3,4,6,7,9]
    lr_sides_from = [3,1,6,4,9,7]
    ud_sides_to = [1,2,3,7,8,9]
    ud_sides_from = [7,8,9,1,2,3]
    
    if direction == "left_right" or direction == "both":
        for to_idx,from_idx in zip(lr_sides_to,lr_sides_from):
            mirror_df[f'B{to_idx}DensityAvg'] = df[f'B{from_idx}DensityAvg']
            mirror_df[f'B{to_idx}MoistureAvg'] = df[f'B{from_idx}MoistureAvg']
            mirror_df[f'B{to_idx}TemperatureAvg'] = df[f'B{from_idx}TemperatureAvg']
            mirror_df[f'B{to_idx}AllOtherDefectWidthSum'] = df[f'B{from_idx}AllOtherDefectWidthSum']
            mirror_df[f'B{to_idx}AllOtherDefectCount'] = df[f'B{from_idx}AllOtherDefectCount']
            mirror_df[f'B{to_idx}DecayWidthSum'] = df[f'B{from_idx}DecayWidthSum']
            mirror_df[f'B{to_idx}DecayCount'] = df[f'B{from_idx}DecayCount']
            mirror_df[f'B{to_idx}KnotWidthSum'] = df[f'B{from_idx}KnotWidthSum']
            mirror_df[f'B{to_idx}KnotCount'] = df[f'B{from_idx}KnotCount']
    if direction == "up_down" or direction == "both":
        for to_idx,from_idx in zip(ud_sides_to,ud_sides_from):
            mirror_df[f'B{to_idx}DensityAvg'] = df[f'B{from_idx}DensityAvg']
            mirror_df[f'B{to_idx}MoistureAvg'] = df[f'B{from_idx}MoistureAvg']
            mirror_df[f'B{to_idx}TemperatureAvg'] = df[f'B{from_idx}TemperatureAvg']
            mirror_df[f'B{to_idx}AllOtherDefectWidthSum'] = df[f'B{from_idx}AllOtherDefectWidthSum']
            mirror_df[f'B{to_idx}AllOtherDefectCount'] = df[f'B{from_idx}AllOtherDefectCount']
            mirror_df[f'B{to_idx}DecayWidthSum'] = df[f'B{from_idx}DecayWidthSum']
            mirror_df[f'B{to_idx}DecayCount'] = df[f'B{from_idx}DecayCount']
            mirror_df[f'B{to_idx}KnotWidthSum'] = df[f'B{from_idx}KnotWidthSum']
            mirror_df[f'B{to_idx}KnotCount'] = df[f'B{from_idx}KnotCount']
    return mirror_df

def noiseMaker(df):
    noise_df = df.copy()
    for key in df.keys():
        if key != 'm_dThickness' and key != 'peelFile' and key != 'dryFile' and key != 'traindevtest':
            noise_df[key] = addNoise(noise_df[key])
    return noise_df

def augmentData(df, amountFactor=50,shuffle=True,printProgress=True,dontIncludeOriginal=True):
    """
    Data augmenter
    --------------
    Example use:
    augmented_df = augmentData
    
    Parameters
    ----------
    
    df = pandas dataframe to be augmented
    amountFactor = int, amount of noise-added copies to be maked of the original df
                        after that also mirrorin will be added which makes a lot of more rows
    shuffle = bool, if True dataframe will be shuffled
    printProgress = bool, if True prints progress
    
    Returns
    -------
    
    Augmented version of the original pandas dataframe.

    ---------------------------------------------------------------
    DATE: 2021-12-03
    - Added option not to include the original set to augmented set
    - Added row amount calculation to printing
    ---------------------------------------------------------------
    """
    from datetime import datetime
    started = datetime.now()
    noise_df_list = []
    mirror_df_list = []
    if dontIncludeOriginal == False:
        full_df = df.copy()
    else:
        full_df = pd.DataFrame()
    progress = 0
    progress_end = amountFactor + 3 + (amountFactor*4) + ((amountFactor*3)+3)
    if dontIncludeOriginal == False:
        amount_of_rows = (amountFactor * 4 + 4) * df.shape[0]
    else:
        amount_of_rows = (amountFactor * 4 + 3) * df.shape[0]
    for i in range(amountFactor):
        progress += 1
        if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
        noise_df_list.append(noiseMaker(df))
    progress += 1
    if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
    mirror_df_list.append(mirrorSides(df,"left_right"))
    progress += 1
    if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
    mirror_df_list.append(mirrorSides(df,"up_down"))
    progress += 1
    if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
    mirror_df_list.append(mirrorSides(df,"both"))
    for noise_df in noise_df_list:
        progress += 1
        if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
        mirror_df_list.append(mirrorSides(noise_df,"left_right"))
        progress += 1
        if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
        mirror_df_list.append(mirrorSides(noise_df,"up_down"))
        progress += 1
        if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
        mirror_df_list.append(mirrorSides(noise_df,"both"))
        progress += 1
        if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
        full_df = full_df.append(noise_df,ignore_index=True)
        if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
    for mirror_df in mirror_df_list:
        full_df = full_df.append(mirror_df,ignore_index=True)
        progress += 1
        if printProgress == True: print(f"Progress {int((progress/progress_end)*100)} %\t\t-\tRow {full_df.shape[0]}/{amount_of_rows}\t-\t{datetime.now()-started}",end="\r")
    
    if shuffle == True:
        return full_df.sample(frac=1).reset_index(drop=True)
    else:
        return full_df