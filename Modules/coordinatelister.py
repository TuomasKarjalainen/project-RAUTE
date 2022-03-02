def coordinateLister(jsonlist):
    """
    -------------------
    VERSION: 2021-11-15
    -------------------
    
    Give a list of jsons as a parameter. For example a list created with readJson()-function.
    This function gives all x- and y-coordinates of density blocks, moisture blocks and all defects.
    
    Six lists will be returned, which all contains lists of all sheets as a parameter.
    
    Example
    -------
    
    xDensity, yDensity, xMoisture, yMoisture, xDefects, yDefects = coordinateLister(jsonlist)
    
    So if your jsonlist contains all 146 peeling sheets, then for example
    list xDensity contains 146 lists. First list inside xDensity contains all density x-coordinates of the first sheet and so on.    
    
    """
    xD_ALL = []; yD_ALL = []; xM_ALL = []; yM_ALL = []; xDEF_ALL = []; yDEF_ALL = []

    # Looping all sheets and appending sheets coordinates lists to lists containing lists of all sheets coordinate-lists
    for sheet in jsonlist:
        # Density-blocks
        xD = []; yD = []
        for dblock in sheet['DensityBlocks']:
            for key in dblock:
                if key == 'm_pntTL' or key == 'm_pntTR' or key == 'm_pntBL' or key == 'm_pntBR':
                    xD.append(dblock[key]['x'])
                    yD.append(dblock[key]['y'])
        xD_ALL.append(xD)
        yD_ALL.append(yD)

        # Moisture blocks
        xM = []; yM = []
        for dblock in sheet['MoistureBlocks']:
            for key in dblock:
                if key == 'm_pntTL' or key == 'm_pntTR' or key == 'm_pntBL' or key == 'm_pntBR':
                    xM.append(dblock[key]['x'])
                    yM.append(dblock[key]['y'])
        xM_ALL.append(xM)
        yM_ALL.append(yM)

        # Defects
        xDEF = []; yDEF = []
        for dblock in sheet['Defects']:
            for key in dblock:
                if key == 'm_mmpntGravity':
                    xDEF.append(dblock[key]['x']/sheet['ObjectData'][0]['ObjectResX'])
                    yDEF.append(dblock[key]['y']/sheet['ObjectData'][0]['ObjectResY'])
        xDEF_ALL.append(xDEF)
        yDEF_ALL.append(yDEF)
    return xD_ALL, yD_ALL, xM_ALL, yM_ALL, xDEF_ALL, yDEF_ALL