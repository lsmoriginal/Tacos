'''
There are better ways to log than this, this should not be used anymore
'''

import sys
import os
import logging
from pandas import DataFrame

def getLogger(loggerName:str, 
              fileDir:str = None,
              level = logging.DEBUG,
              consoleLevel = logging.WARNING,
              format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
              tofile = True):
    """return a logger for logging
    somehow the logDecorator function does 
    not write to the log folder
    Args:
        loggerName (str): name given to the logger
        fileDir (str): directory
        level ([type], optional): [description]. Defaults to logging.DEBUG.
        format (str, optional): [description]. Defaults to '%(asctime)s - %(name)s - %(levelname)s - %(message)s'.
    Returns:
        logger: [description]
    """

    myLogger = logging.getLogger(loggerName)
    myLogger.propagate = False
    myLogger.setLevel(level)

    myFormat = logging.Formatter(format)
    
    if tofile:
        myHandler = logging.FileHandler(fileDir, mode='a')
        myHandler.setFormatter(myFormat)
        myHandler.setLevel(level)
        myLogger.addHandler(myHandler)
        

    # console only prints WARNING & ABOVE
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(consoleLevel)
    console.setFormatter(myFormat)
    myLogger.addHandler(console)

    return myLogger

class _NoneLogger():
    def info(self, info):
        return None
    
    def debug(self, debug):
        return None

    def warning(self, warning):
        return warning

    def critical(self, critical):
        return critical

class SimplyLog():
    '''
    This class is a quick and simple wrapper for logging module 
    so that we dont need to spend too much time initialising loggers;
    and configuring it in other scripts
    
    
    logGetter = SimplyLog(outputLocation)
    logger = logGetter('infomation')
    logger.info(message)
    '''

    def __init__(self, outputDir):
        # a dictionary storing all loggers
        self.myLoggers = dict()
        self.outputDir = str(outputDir)

        noneLogger = _NoneLogger()
        self.myLoggers['None'] = noneLogger

    def __call__(self, loggerName:str, **kwagrs):
        try:
            return self.myLoggers[loggerName]
        except KeyError:
            logger = getLogger(loggerName, 
                               os.path.join(self.outputDir, 
                                            loggerName+'.log'),
                               **kwagrs)
            self.myLoggers[loggerName] = logger
            return logger

class _CSVlogger():
    def __init__(self, logger, 
                 columns:list,
                 keepacopy:bool=False) -> None:
        self.logger = logger
        self.columns = columns
        self.columnCount = len(columns)
        self.len = 0
        header = ",".join(str(i) for i in columns)
        self.logger.info(header)
        self.rows = [] if keepacopy else None
        self.keepacopy = keepacopy
    
    def writeRow(self, data:list):
        assert len(data) == self.columnCount, 'ColumnLenError'
        row = ",".join(str(i) for i in data)
        self.logger.info(row)
        self.len += 1
        if self.keepacopy:
            self.rows.append(data)
        
    def getDataFrame(self):
        if not self.keepacopy:
            return None
        return DataFrame(self.rows,
                  columns=self.columns)
        
    def __len__(self):
        return self.len
        
        
class CSVwriter(SimplyLog):
    '''
    myCSVWriter = CSVwriter(outputLocation)
    
    # initiate the csv
    thiscsv = myCSVWriter('csvName', # without .csv
                [columns of the csv]
    )
    
    thiscsv.writeRow([columns of data])
    len(thiscsv) # get the current number of rows of data
    '''
    def __call__(self, csvName:str, columns:list, keepacopy:bool=False):
        assert isinstance(columns, list), 'columns must be list'
        try:
            return self.myLoggers[csvName]
        except KeyError:
            logger = getLogger(csvName, 
                               os.path.join(self.outputDir, 
                                            csvName+'.csv'),
                               format = '%(message)s',)
            logger = _CSVlogger(logger, columns, keepacopy)
            self.myLoggers[csvName] = logger
            return logger
