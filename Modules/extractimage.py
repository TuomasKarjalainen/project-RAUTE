import os
import shutil
import zipfile
import io
def extractImage(datx_fullfilepath, image_targetfolder=None, writeMode='memory'):
    """
    -------------------
    VERSION: 2021-11-15
    -------------------
    
    Either extract ColorImage from .datx-file or read it into memory.
    
    As a remainder, default paths to datx-files (add a filename to these):
    ----------------------------------------------------------------------
    
    peel datx-files = '/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Sorvi/koivu/testRun20210505/'
    dry datx-files = '/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Kuivaus/testRun20210505/'
    
    Parameters as a string:
    -----------------------
    
    - datx_fullfilepath
    - image_targetfolder (case extracting only, optional, default=None) - if not None image will be moved from current working directory to the target folder
    - writeMode ('memory' or 'disk') - if 'memory' image is returned as memory buffer, if 'disk' image will be extracted to disk and nothing is returned
    
    Case extracting image
    ---------------------
    Extracts ColorImage from .datx file, renames it to match the datx-file and moves it to desired folder. Creates the desired folder if it doesn't exist.
    
    Extracting example:
    -------------------
    
    datxFile = '/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Sorvi/koivu/testRun20210505/20210505123334_85.datx'
    image_targetfolder = '/home/jovyan/work/team-network-training/SheetImages/'
    extractImage(datx_fullfilepath, image_targetfolder, writeMode='disk')
    
    
    Case reading image into memory
    ------------------------------
    
    Istead of saving image to disk, just return the image as a memory buffer.
    
    Memory reading example
    ----------------------
    datxFile = '/home/jovyan/work/data/nfs_shared_data/Raute/ai-2021h2-data/rawdata/3-Sorvi/koivu/testRun20210505/20210505123334_85.datx'
    myimage = extractImage(datx_fullfilepath=datxFile)
    
    Then load image with image reading libraries:
    from PIL import Image
    import matplotlib.pyplot as plt
    img = Image.open(myimage)
    plt.imshow(img)
    img.close() # Remember to close image after reading!
    """
    
    datx_filename = os.path.basename(datx_fullfilepath) # get filename without path
    imagename = datx_filename.rstrip('datx') # use otherwise same name for image except for the filetype (filetype determined when looking inside the datx-file)
    if image_targetfolder != None: image_targetfolder = os.path.join(image_targetfolder,'')
    if writeMode == 'disk':
        with zipfile.ZipFile(datx_fullfilepath, "r") as zip_ref:
            filelist = zip_ref.namelist()
            for file in filelist:
                # Looking for the desired file 'ColorImage.bmp'
                if 'ColorImage' in file:
                    if file.endswith('jpeg'):
                        imagename += 'jpeg'
                    else:
                        imagename += 'bmp'
                    ColorImage = zip_ref.open(file) # When found open it from the datx
                    # Code below is for saving without folderstructure
                    # Partially adapted from: https://stackoverflow.com/questions/46954626/extract-zip-file-without-folder-python
                    with open(imagename,'wb') as imagefile: 
                        shutil.copyfileobj(ColorImage,imagefile)
                    break # After the desired image is found, stop looking and exit
        # Move created image to desired path; leave to working directory if image_targetfolder=None:
        # os.rename(os.getcwd()+'/'+imagename,image_targetfolder+imagename)
        if image_targetfolder != None:
            os.makedirs(image_targetfolder, exist_ok=True)
            shutil.move(os.getcwd()+'/'+imagename,image_targetfolder+imagename)
    elif writeMode == 'memory':
        with zipfile.ZipFile(datx_fullfilepath, "r") as zip_ref:
            filelist = zip_ref.namelist()
            for file in filelist:
                if 'ColorImage' in file: 
                    #Tutorial where part of this is copyed: https://stackoverflow.com/questions/31777169/python-how-to-read-images-from-zip-file-in-memory
                    ColorImageBmp = zip_ref.read(file) # When found open it from the datx
                    dataEnc = io.BytesIO(ColorImageBmp)
                    return dataEnc