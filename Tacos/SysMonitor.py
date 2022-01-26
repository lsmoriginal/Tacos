import torch
import os

import pynvml # for GPU checks
import psutil # for CPU checks

class SystemResourceObserver():
    """
    This is a resource reporter wrapper class that can report 
    the usage of CPU load, CPU RAM, GPU RAM
    """

    def __init__(self) -> None:
        hasGPU = torch.cuda.is_available()
        self.hasGPU = hasGPU
        if hasGPU:
            pynvml.nvmlInit()
            self.gpus = pynvml.nvmlDeviceGetCount()

        if not hasGPU:
            self.totalGPUMem = 0
        else:
            self.gpuDevices = list(pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.gpus))
            self.totalGPUMem = sum(pynvml.nvmlDeviceGetMemoryInfo(gpuHandler).total for\
                 gpuHandler in self.gpuDevices)
    
    def cpuLoad(self, percent = False):
        if percent:
            return psutil.getloadavg()[2]/os.cpu_count()
        else:
            return psutil.getloadavg()[2]
    
    def gpuRam(self, percent = False, format = 'GB'):
        if not self.hasGPU:
            return 0

        usedMem = sum(pynvml.nvmlDeviceGetMemoryInfo(gpuHandler).used for\
             gpuHandler in self.gpuDevices)
        if percent:
            return usedMem/self.totalGPUMem
        else:
            if format == 'GB':
                return usedMem/(1024**3)
            else:
                return usedMem
    
    def cpuRam(self, percent = False, format = 'GB'):
        if percent:
            return psutil.virtual_memory()[2]/100
        else:
            if format == 'GB':
                return psutil.virtual_memory()[3]/(1024**3)
            else:
                return psutil.virtual_memory()[3]

    def reportStatus(self):
        report = str(f'CPU:{self.cpuLoad():.2} {self.cpuLoad(percent=True):.2%} ' 
                    f'RAMcpu: {self.cpuRam():.1f}GB {self.cpuRam(percent=True):.2%} '
                    f'RAMgpu: {self.gpuRam():.1f}GB {self.gpuRam(percent=True):.2%}')
        return report

    def close(self):
        if self.hasGPU:
            pynvml.nvmlShutdown()