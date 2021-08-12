import pickle
import os

def toPickle(pickle_obj, directory, pickle_name = None): 
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
  
def fromPickle(directory, pickle_name = None):
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