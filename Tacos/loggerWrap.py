import sys
import os
import logging

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

class NoneLogger():
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
    '''

    def __init__(self, outputDir):
        # a dictionary storing all loggers
        self.myLoggers = dict()
        self.outputDir = outputDir

        noneLogger = NoneLogger()
        self.myLoggers['None'] = noneLogger

    def __call__(self, loggerName:str):
        try:
            return self.myLoggers[loggerName]
        except KeyError:
            logger = getLogger(loggerName, 
                               os.path.join(self.outputDir, 
                                            loggerName+'.log'))
            self.myLoggers[loggerName] = logger
            return logger
        
    def DEBUG(self, loggerName:str):
        self.__call__(loggerName).DEBUG
        
    def INFO(self, loggerName:str):
        self.__call__(loggerName).INFO
        
    def WARNING(self, loggerName:str):
        self.__call__(loggerName).WARNING
        
    def CRITICAL(self, loggerName:str):
        self.__call__(loggerName).CRITICAL
        
        