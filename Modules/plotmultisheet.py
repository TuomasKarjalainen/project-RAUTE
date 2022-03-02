def plotMultisheet(sheet_list, datx_path='/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Sorvi/koivu/testRun20210505/',
              main_title=None, figsize=(24,24), plotImage='./myplot.png', columns=3):
    """
    -------------------
    VERSION: 2021-11-15
    -------------------
    
    Plots multiple sheets and sensor reading positions, when a list of sheets are given as a parameter.
    It is assumed that sheets in the given list are already read into a memory from json-files for example using readJson()-function.
    
    Also path to datx-files is needed as a parameter, unless default path for peeling files is suitable.
    
    By default saves the plot to current directory using name myplot.png.
    
    Parameters
    ----------
    
    sheet_list = a list containing json-data already read into Python form
    datx_path = path to datx-files for reading images, DEFAULT= '/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Sorvi/koivu/testRun20210505/'
    main_title = string, title for the plot, DEFAULT = None
    figsize = tuple, size of the plot, DEFAULT = (24,24)
    plotImage = string or None, path for saving the plot into image-file, if None image won't be saved, DEFAULT = './myplot.png'
    columns = int, how many images will be plotted on one row (= how many columns there will be), DEFAULT = 3
    
    NOTE: USE WITH CAUTION IF YOU WAN'T TO PLOT A LOT OF SHEETS.
    It's better to give shorter lists and call this function in a for-loop instead of passing the full sheet_list list directly.
    
    Example for plotting all drying sheets in sets of nine sheets
    -------------------------------------------------------------
    
    from Modules.readjson import readJson # Required for reading jsons
    _, dry = readJson(pathToPeelJson=None)
    drypath = '/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Kuivaus/testRun20210505/'
    plotImagePath = '/home/jovyan/work/team-network-training/Visualizations/Dry/'
    sheet_lists = []
    ii = 0
    setnumber = 0
    for sheet in dry:
        sheet_lists.append(sheet)
        ii += 1
        if ii % 9 == 0 or sheet['FileName'] == dry[-1]['FileName']:
            setnumber += 1
            plotMultisheet(sheet_lists,datx_path=drypath,main_title="Set number: "+str(setnumber),plotImage=f'{plotImagePath}drysheet_set_{setnumber}')
            sheet_lists = []
    
    Note: Currently seems to work weirdly with drying files, but plots look good on peeling files.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    from Modules.extractimage import extractImage
    
    # Coordinates
    from Modules.coordinatelister import coordinateLister
    xD_ALL, yD_ALL, xM_ALL, yM_ALL, xDEF_ALL, yDEF_ALL = coordinateLister(sheet_list)
    
    
    # PLOT SETUP
    # -------------------------------------------------------
    fig = plt.figure(figsize=figsize) # Plotin total size including all subplots
    fig.suptitle(main_title, fontsize='xx-large')
    
    # Lista plotattavista arkeista
                     
    # PLOTTING FRAME
    # -------------------------------------------------------
    # Subplot logic = (amount of rows, amount of columns, index number of this plot with this setting)
    # For example (3,3,1) Logic is 3X3 plot which equals nine images, current image has index number 1, which means it is top left image
    # (3,2,6) Logic 3X2, 3 rows, 2 columns, index 6, image's index is the last one = (third row, second column)
    # Part of the indexes can be left unplotted or even use different size on different subplot, but images may collide, if you are not careful
    # check more help(plt.Figure.add_subplot) and example at stackoverflow: https://stackoverflow.com/questions/48744165/uneven-subplot-in-python    
                     
    
    # Plot size = amount of rows * amount of columns, where last row can be left short                 
    cols_in_subplot=columns 
    rows_in_subplot=int(np.ceil(len(sheet_list)/cols_in_subplot))

                    
    # List for subplot-objects                 
    axes = [] # will be referenced later using index-numbers when doing the actual plot
                     
    # Loop in which the plot-frame is formed
    for ax in range(len(sheet_list)): # Loop length = number of sheets
        axes.append(fig.add_subplot(rows_in_subplot,cols_in_subplot,ax+1))   # ax+1, because loop starts from 0 and subplot-index from 1
                                                                             
        # SUBPLOT TITLE is filename
        axes[ax].set_title(sheet_list[ax]['FileName'])
                     
    # Actual plot
    # -------------------------------------------------------
    for ax in range(len(axes)): # Loop length = amount of subplots, which is amount of sheets
    #                            # ax is order number of subplot

        axes[ax].scatter(xD_ALL[ax],yD_ALL[ax],label='Density')
        axes[ax].scatter(xM_ALL[ax],yM_ALL[ax],label='Moisture')
        axes[ax].scatter(xDEF_ALL[ax],yDEF_ALL[ax],label='Defects')
        axes[ax].legend()
        filename = sheet_list[ax]['FileName']
        img = extractImage(datx_path+filename)
        image = Image.open(img)
        # Images in subplot: https://stackoverflow.com/questions/41793931/plotting-images-side-by-side-using-matplotlib
        axes[ax].imshow(image)
        image.close()

    if plotImage != None: plt.savefig(plotImage) # If plotImage-variable is defined image will be saved into a file 
    plt.show() # Näytetään plottaus