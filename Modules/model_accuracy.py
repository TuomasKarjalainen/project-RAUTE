import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
import numpy as np
import sys

#     --------------------------------------
#       from Modules.model_accuracy import * 
#     --------------------------------------


def modelAccuracy(model, data, visualize=True):
    """
    ----------------------------------------------------
    VERSION : 09/12/2021
    
    LAST UPDATE : 
        - Removed hard-coding from plot coordinates, added plot_lenght instead 
        - Fixed the example for how to use this function
        - Fixed percentage plotting 
    -----------------------------------------------------
    
    
    Function for visualizing model's predictions and errors.
    
    ARGS : 
        - model: Pretrained neural network model
        - data: Data for prediction e.q. test_data
        - visualize: Plotting
        
    EXAMPLE : 
        - If the model is defined before:
            modelAccuracy(model, data=(transformed_test_data,test_targets), visualize=True)
        
    RETURNS :
    
        Nothing
    
    """
    preds = model.predict(data[0])
    
    list_of_preds = []
    for sublist in preds:
        for item in sublist:
            list_of_preds.append(item)
    
    list_of_targets=[]
    for target in data[1]:
        list_of_targets.append(target) 
        
    difference = np.array(np.array(list_of_targets) - np.array(list_of_preds))
    print("\n\t\tPredicitons and targets")
    print("--------------------------------------------------------")
    print(f" Average difference:\t{difference.mean()}\n Max difference:\t{difference.max()}\n Min difference:\t{difference.min()}")
    print("--------------------------------------------------------")
    
    plot_length = len(list_of_targets)
    
    if visualize==True:        
        plt.figure(figsize=(12,6))
        sns.set(style="darkgrid")
        plt.title("Model accuracy",fontsize=(12), fontweight='bold')
        plt.plot(list_of_targets[:100],label="Targets")
        plt.plot(list_of_preds[:100], label="Predictions")
        plt.legend()                
        plt.figure(figsize=(12,6))
        percentage = np.array(np.array(list_of_preds / np.array(list_of_targets))) * 100
        plt.title("Percentage",fontsize=(12), fontweight='bold')
        plt.plot((0,plot_length),(100,100), color='green')
        plt.plot(percentage[:100]);
        plt.show()        
        plt.figure(figsize=(12,6))
        plt.title("Error",fontsize=(18), fontweight='bold')
        plt.plot(np.array(np.array(list_of_targets[:100]) - np.array(list_of_preds[:100])),color='red');
        
    
    

    
    
def savedModelAccuracy(model, path=None, data=None, visualize=False):
    """
    --------------------
    VERSION : 30/11/2021
    --------------------
    
    Function for visualizing SAVED model's predictions and errors.
    
    
    ARGS : 
        - path: Path to saved model
        - model: Saved model filename 
        - data: Data for prediction e.q. test_data
        - visualize: Plotting
        
    EXAMPLE : 
    
        If using SavedModel format:
            - savedModelAccuracy('regmodel',data=transformed_big_test_data, visualize=True)
            
        If using HDF5 format:
            - savedModelAccuracy('regmodel.h5',path='/home/jovyan/work/team-network-training/Sprint 4/', data=transformed_big_test_data, visualize=True)
        
    RETURNS :
    
        Nothing
    
    """
    
    loaded_model = tf.keras.models.load_model(path+model)       
    loaded_model.summary()

    import os
    import pycuda.autoinit
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    
    
    print("\nEvaluating pretrained model:")
    test_mse_score, test_mae_score = loaded_model.evaluate(data[0], data[1])
    print("\n\n\t\t Model Error")
    print("----------------------------------------------")
    print(f" Mean absolute error:\t{test_mae_score}\n Mean square error:\t{test_mse_score}")
    print("----------------------------------------------")
        
            
    if (visualize==True) & (type(data[0])==np.ndarray):
        print("\nPlotting:")
        preds = loaded_model.predict(data[0])
        list_of_preds = []
        for sublist in preds:
            for item in sublist:
                list_of_preds.append(item)

        list_of_targets=[]
        for target in data[1]:
            list_of_targets.append(target) 
    
        plot_length = len(list_of_targets)
        
        plt.figure(figsize=(12,6))
        sns.set(style="darkgrid")
        plt.title("Model accuracy",fontsize=(12), fontweight='bold')
        plt.plot(list_of_targets[:100],label="Targets")
        plt.plot(list_of_preds[:100], label="Predictions")
        plt.legend()                
        plt.figure(figsize=(12,6))
        percentage = np.array(np.array(list_of_preds / np.array(list_of_targets))) * 100
        plt.title("Percentage",fontsize=(12), fontweight='bold')
        plt.plot((0,plot_length),(100,100), color='green')
        plt.plot(percentage[:100]);
        plt.show()        
        plt.figure(figsize=(12,6))
        plt.title("Error",fontsize=(18), fontweight='bold')
        plt.plot(np.array(np.array(list_of_targets[:100]) - np.array(list_of_preds[:100])),color='red');
        
    elif (visualize==True) & (type(data[0])!=np.ndarray):
        print("Define data for predictions!", file=sys.stderr)