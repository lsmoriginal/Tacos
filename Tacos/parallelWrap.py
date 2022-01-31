from multiprocessing import Manager
from tqdm import tqdm
from multiprocessing import Pool
from itertools import repeat
from datetime import datetime
now = datetime.now
from os import cpu_count

def intoChunks(lst, n):
    """Yield successive n chunks from lst."""
    steps = len(lst)//n
    for i in range(0, len(lst), steps):
        yield lst[i:i + steps]
        
def Process(TaskLogic,progressBar,
            minInterval,
            taskList, *args):
    # initialise the worker
    # provide all your settings here
    # including the config needed for 
    # aggregate task
    task = TaskLogic(*args) 
    
    timeStart = now()
    timeTaken = 0
    taskFinished = 0
    for each in taskList:
        try:
            results = task.workSingleTask(each)
        except Exception:
            results = None
        task.results.append(results)
        timeTaken = (now() - timeStart).seconds
        taskFinished += 1
        if timeTaken >= minInterval:
            # do a report
            progressBar.put(taskFinished)
            taskFinished = 0
            timeStart = now()
    if taskFinished:
        progressBar.put(taskFinished)
            
    return task.aggregateAllTasks()

        
class ParallelWorker():
    '''
    Wrap the job you want to multi-process into
    a function taking in a list of tasks: ideally, 
    do not create too many processes, creating and destruction
    is a waste of resources
    '''
    
    def __init__(self,
                 taskLogic,
                 taskList,
                 taskArgs=[],
                 processes:int = 2,
                 chunks:int = 8,
                 minInterval = 2) -> None:
        """[summary]

        Parameters
        ----------
        taskLogic : [type]
            class implementing TaskLogic interface
        taskList : [type]
            The whole list of tasks needed processing
        taskArgs : list, optional
            position arguments to initialise 
            the TaskLogic class
            , by default []
        processes : int, optional
            [description], by default 2
        chunks : int, optional
            Split the tasks into N chunks
            , by default 8
        minInterval : int, optional
            Minimum seconds to refresh the progress bar,
            too frequent refresh may consume too much resources
            , by default 2
        """
        
        assert processes <= chunks, 'Having more processes than chunks'
        assert processes <= cpu_count(), 'You dont have that many CPU'
        
        self.taskLogic = taskLogic
        self.taskArgs = taskArgs
        self.taskCount = len(taskList)
        self.taskLists = intoChunks(taskList,
                                    chunks)
        self.minInterval = minInterval
        
        thisManager = Manager()
        self.progressBar = thisManager.Queue()
        self.pool = Pool(processes)
        
    def run(self):
        
        taskArgs = (repeat(arg) for arg in self.taskArgs)
        intputArgs = zip(
            repeat(self.taskLogic),
            repeat(self.progressBar),
            repeat(self.minInterval),
            self.taskLists,
            *taskArgs
        )
        result = self.pool.starmap_async(Process,
                                         intputArgs)
        self.pool.close()
        
        taskProgress = tqdm(range(self.taskCount),
                            mininterval=self.minInterval)
        allDone = 0
        while allDone < self.taskCount:
            # getting the updates from 
            # each sub-process to update the progress bar
            taskDone = self.progressBar.get()
            taskProgress.update(taskDone)
            allDone += taskDone
        
        result = result.get()
        # print('--------Status--------')
        # print(f'Process ready   : {result.ready()}')
        # print(f'Process success : {result.successful()}')
        self.results = result
        return result
    
    def getResults(self):
        results = []
        while self.results:
            results.extend(self.results.pop(0))
        self.results = results
        return self.results
  
  
class TaskLogic():
    def __init__(self) -> None:
        self.results = []
    
    def workSingleTask(self, oneTask):
        pass
    
    def aggregateAllTasks(self):
        pass    

'''

        
# example use of the wrapper
class GenerateTextEmbeddings(TaskLogic):
    def __init__(self, modelName, modelConfig, writeLocation) -> None:
    
        # initializing the embdedding Model
        self.model = NLP_framework.loadModel(modelName)
        self.model.initialise(modelConfig)
        self.writeLocation = writeLocation
        self.results = []
        
    def workSingleTask(self, oneTask:PosixPath):
        text = read(oneTask)
        embedding = self.model.encode(text)
        # mean pooling of embedding
        embedding = embedding.mean(axis=0)
        writeEmbedding(embedding, self.writeLocation/oneTask.name)
        
        return embedding
        
    def aggregateAllTasks(self):
        return np.array(self.results, dtype=float)
        
listOf10000Documents = [...]
process = ParallelWorker(GenerateTextEmbeddings,
               listOf10000Documents,
                ['BERT', {config}, '../results/bert'],
                processes = 8,
                chunks = 7,
                minInterval = 2)
process.run()
process.getResults()

================================


'''
from time import sleep
class StringEachNumber(TaskLogic):
    def __init__(self, exception = 5) -> None:
        super().__init__()
        self.exception = exception
    
    def workSingleTask(self, task):
        if task == self.exception:
            raise Exception
        else:
            result = str(task)
        return result
    
    def aggregateAllTasks(self):
        return self.results
        
if __name__ == '__main__':
    # another simple example
    
    task = list(range(100))
    process = ParallelWorker(StringEachNumber,
                             task,
                             [5,],
                             processes = 2,
                             chunks = 2,
                             minInterval = 2)
    process.run()
    print(process.getResults())