import pandas as pd
import numpy as np
import csv
import argparse
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras import layers
from keras.layers import Dropout
from keras.activations import *

from Modules.ssh_connector import *
from Modules.chunker import connection


def get_pickle_data(pickle="augmented4.pkl",columns_to_drop=['dryFile','peelFile','m_dThickness']):
    """
    Function recienves a pickle file from the desired folder. If the pickle file is in the same directory as the used .ipynb, then you can only put the pickle file name to the pickle parameter.
    
    Example on how to use
    ---------------------
    df_features = get_pickle_data(columns_to_drop=['dryFile','peelFile','m_dThickness','traindevtest'])
    
    """
    df_features = pd.read_pickle(pickle)
    df_features = df_features.drop(columns=columns_to_drop)
    return df_features

def get_database_data(env_path, table_name, ssh=True, limit=100000, columns_to_drop=['peelFile','m_dThickness','traindevtest','dryFile']):
    
    """
    Function gets data from the database with SSH connection or without it.
    
    Example on how to use
    ---------------------
    df_features = get_database_data(env_path="/home/jovyan/work/customer_project/neural_network/salasana.env", table_name="Preprocessed3", ssh=True, columns_to_drop=['peelFile','m_dThickness','traindevtest','dryFile'])
    
    Parameters
    ----------
    env_path = String, Define the directory path to the .env file.
    table_name = String, Name of table containing the data in the database.
    ssh = Bool, If `True`, ssh_connector program will be used to get the data from the database through ssh network protocol. If `False`, chuncker program will take direct contact to the database. Use this only if you are working inside the same network and the database.
    columns_to_drop = Array, Removes the columns from the table you do not need.
    
    """
    
    if ssh == True:
        connector = Connector(path=env_path)
        
        data = connector.connector(query=f"SELECT * FROM {table_name} LIMIT {limit}")
        data = data.drop(columns=columns_to_drop)
       
        
    elif ssh == False:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        
        host=os.getenv("MARIADB_IP")
        user=os.getenv("MARIADB_USER")
        password=os.getenv("MARIADB_PASSWORD")
        database=os.getenv("MARIADB_DATABASE")
        port=int(os.getenv("MARIADB_PORT"))
        conn, _ = connection(host, user, password, database, port)
        query=f"SELECT * FROM {table_name} LIMIT {limit}"
        data = pd.read_sql(query, conn)
        data = data.drop(columns=columns_to_drop)
       

    return data

# Custom metrics funtions:
def distance_from_true(y_train, y_pred):
    return y_pred - y_train

def precentage_from_true(y_train, y_pred):
    return y_pred/y_train

def mean_absolute_percentage(y_train, y_pred):
    return abs((y_train - y_pred)/y_train)

    
def create_and_fit(df_features, df_target, test_size, norm, inputs, hidden_sizes, outputs ,activ, EPOCHS, loss, optimizer, lr, metrics=['mae', distance_from_true, 'mape'], dropout=None, with_predictions=False, save_model=False, path='./model.h5'):
    """
    from Neural_Network import *
    -------------------
    VERSION: 2021-12-9
    -------------------
    Function for neural network training and saving. For this function to work you need to define df_features and all the desired parameters in advance.
    
    Example on how to use
    ---------------------
    model, history, train, test, model_name = create_compile_and_fit(*parameters)
    
    Parameters
    ----------
    df_features = Dataframe, A previously made dataframe that has both the trainable values and the target value/values
    df_target = String, The name of the column that we want to use as the target value. Needs to be in df_features dataframe
    test_size = Float, The size of the test size as a percentage.
    norm = String, Two option for now, 'standard' and 'minmax'. The name of the normalization funtion.
    inputs = Int, The amount of columns in our train set.
    hidden_sizes = Array, The hidden layer sizes that we want to use when training the network
    outputs = Int, Default = 1
    activ = String, The name of the activation funtion that we want to use for the network
    dropout = Float, Thie size of the dropout function how much we want to drop when training the network. Value is prefered to keep in between 0.2 - 0.5. Default = None.
    EPOCHS = Int, The amount of epochs that we want the network to go through
    loss = String, The name of the loss function that we want the network to use
    optimizer = Code example: tf.keras.optimizers.RMSprop, The tensorflow optimizer funtion that we want to use when training the network
    lr = Float, The learning rate value that the optimizer will use to optimize the network
    metrics = Array, Give all the metrics functions that you want to see while the network is training for example: ['mae', distance_from_true, 'mape']
    with_predictions = Bool, if True, the neural network will print out the the true values and the predictions in a column after each epoch. Default = False
    save_model = Bool, if True, after the neural network has gone though the last epoch, this funtion will save the model to the desired form.
    path= String, for example './model.h5'. This path parameter is used when saving the model. It will requre the chosen path, the desired model name and the type of the saved model. Example types, SavedModel (Folder which consists the models metadata, checkpoint and variables folder) or .h5 filetype.
    
    Example parameters
    ------------------
    Split an Scale parameters:
    df_target = 'dryShrinkage'
    test_size = 0.2
    norm = 'standard' or 'minmax'

    Model creation parameters:
    inputs = 84
    hidden_sizes = [64,32,16]
    outputs = 1
    activ = 'relu'
    dropout = 0.2

    Model fit parameters:
    EPOCHS = 5
    loss = 'mse'
    optimizer = tf.keras.optimizers.RMSprop
    lr = 0.001
    metrics = ['mae', 'mse', distance_from_true, 'mape', precentage_from_true]
    with_predictions = False

    Model Saving parameters:
    save_model = False
    path='./models/SavedModel'

    Model stats saving parameters:
    csv_path='./logs/'
    save_to_csv=True
    
    Returns
    -------
    model = The trained model and its structure
    history = All the values that the model got while training the network. Loss values and the metrics values
    train = The train set. This is afterwards used when saving the values to a csv file
    test = The test set. This is afterwards used when saving the values to a csv file
    model_name = The name of the model which the logs info takes into account. This is used afterwards when saving the csv files
    
    """
    # Makes the logs folder
    os.makedirs(csv_path, exist_ok = True)
    
    # Split and scale: 
    train, test, y_train, y_test = train_test_split(df_features.drop(["dryShrinkage","dryWidth"],axis=1)
                                                    ,df_features[df_target],test_size=test_size,random_state=42)

    print("Train set size:", train.shape, "/ Train sets target size:", y_train.shape)
    print("Test set size:", test.shape, "/ Test sets target size:", y_test.shape, "\n")
    
    # Normalizasion with sckikit-learn StandardScaler function
    if norm == 'standard':
        sc = StandardScaler()
        
        train_norm = sc.fit_transform(train)
        test_norm = sc.transform(test)
    
    # Normalizasion with sckikit-learn MinMaxScaler
    elif norm == 'minmax':
        scaler = MinMaxScaler()

        train_norm = scaler.fit_transform(train)
        test_norm = scaler.fit_transform(test)
        
    print("Scaling done. Next is model creation\n")

    # Model creation:
    
    # For looping the hidden_sizes so that we can have as many hidden layers as we want.
    # TODO: Add dropout functions to the model: Make it better!
    hiddens = len(hidden_sizes)
    model = Sequential()
    
    for i in range(hiddens):
        if i == 0:
            model.add(Dense(hidden_sizes[i], input_dim=inputs, activation=activ))
            if dropout != None:
                model.add(Dropout(dropout))
        elif i <= hiddens-1:
            model.add(Dense(hidden_sizes[i], activation=activ))
            if dropout != None:
                model.add(Dropout(dropout))
            if i == hiddens-1:
                model.add(Dense(outputs))
                
    # Showing the models structure        
    model.summary()

    optim = optimizer(learning_rate=lr)

    # Compiling the model for training
    model.compile(loss=loss, optimizer=optim, metrics=metrics)
    
    # Defining the model name as datetime
    model_name=datetime.now()
    
    # Creating the logs csv. This logs all the models history values that the model finds while training
    csv_logger = tf.keras.callbacks.CSVLogger(f'./logs/{model_name}-log.csv', separator=",", append=True)
    
    # Training the network with predictions and true values or without
    if with_predictions == True:
        for i in range(EPOCHS):
            history = model.fit(train_norm, y_train,
                                epochs=1,
                                validation_split=0.2)
            predictions = model.predict(train_norm)
            values = np.column_stack((y_train,predictions))
            print(values)
    else:
        history = model.fit(train_norm, y_train,
                            epochs=EPOCHS,
                            validation_split=0.2,
                           callbacks=[csv_logger])
      
    
    if save_model == True:
        model.save(path)
    else:
        return model, history, train, test, model_name
    
    return model, history, train, test, model_name

def model_stat(model, history, df_features, df_target, test_size, norm, inputs, hidden_sizes, outputs ,activ, EPOCHS, loss, optimizer, lr, metrics, dropout, train, test, csv_path, save_to_csv, model_name):
    """
    This function makes a dataframe out of the parameters used for training the neural network and then saves the dataframe into a csv file.
    
    Example on how to use
    ---------------------
    stats = model_stat(model, history, df_features, df_target, test_size, norm, inputs, hidden_sizes, outputs ,activ, EPOCHS, loss, optimizer, lr, metrics, train, test, csv_path, save_to_csv, model_name)
    
    """
    model_structure = str(model)
    
    model_stats = {'Model structure': model_structure,
                   'Inputs': inputs,
                   'Hidden layers': hidden_sizes,
                   'Output': outputs,
                   'Activation': activ,
                   'Optimizer': optimizer,
                   'Learning rate': lr,
                   'Normalization': norm,
                   'Loss fuction': loss,
                   'Epochs': EPOCHS,
                   'Train-set size': train.shape,
                   'Test-set size': test.shape,
                   'Target': df_target
                  }
    
    df = pd.DataFrame.from_dict(model_stats, orient='index')
    #df = df.transpose()

    if save_to_csv == True:
        df.to_csv(csv_path+f'{model_name}-model_stats.csv')
    
    return df


