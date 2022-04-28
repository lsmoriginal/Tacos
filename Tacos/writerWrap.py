import yaml
import json

import pickle
import os

def writePickle(pickle_obj, 
                directory, 
                pickle_name = None): 
    if not pickle_name:
        pickle_name = os.path.basename(directory)
        directory = os.path.dirname(directory)

    file_loc = os.path.join(directory, pickle_name)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Its important to use binary mode 
    dbfile = open(file_loc, 'wb') 
    # source, destination 
    pickle.dump(pickle_obj, dbfile)                      
    dbfile.close() 

def writeJSON(object, path, sort_keys=False):
    """[summary]

    Parameters
    ----------
    object : [type]
        [description]
    path : [type]
        [description]
    sort_keys : bool, optional
        by default False
        leave it to false if its not important to sort it, 
        otherwise it might take too much time to sort the values
    """
    with open(path, 'w') as json_file:
        json.dump(object, json_file, indent=4, sort_keys=sort_keys)
        
def writeYAML(object, path, sort_keys=False):
    with open(path, 'w') as f:
        yaml.safe_dump(object, f, sort_keys=sort_keys)
        
def writeYASON(object, path, sort_keys=False):
    if str(path).lower().endswith('.json'):
        writeJSON(object, path, sort_keys)
    else:
        writeYAML(object, path, sort_keys)
    
