
from pathlib import Path, PosixPath
import json
import yaml
import pickle
from typing import Union
import os

def readYASON(directory:Union[str, PosixPath])->dict:
    """YASON stands for YAML or JSON

    Parameters
    ----------
    directory : str
        Path to the YAML or JSON file

    Returns
    -------
    dict
        dictionary representation of the configuration file
    """
    directory = str(directory)
    
    if directory.endswith('.json'):
        result = json.load(open(directory))
        return result
    else:
        with open(directory, 'r') as stream:
            result = yaml.safe_load(stream)
        return result

def readPickle(directory:Union[str, PosixPath], 
               pickle_name:str = None):
    # return False if file not found
    if not pickle_name:
        file_loc = directory
    else:
        file_loc = os.path.join(directory, pickle_name)

    if not os.path.exists(file_loc):
        return False
    # for reading also binary mode is important 
    dbfile = open(file_loc, 'rb')      
    db = pickle.load(dbfile) 
    dbfile.close() 
    return db
