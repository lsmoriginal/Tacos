
from pathlib import Path


def nextName(name:str)->str:
    """
    Given a directory, 
    return the available name to this name, 
    if the name already exist, then increase the suffix by 1
    """
    
    originalPath = Path(name)
    if not originalPath.exists():
        return name
    
    index = 1
    while Path(f"{originalPath.parent/originalPath.stem}_{index}{originalPath.suffix}").exists():
        index += 1
    return f"{originalPath.parent/originalPath.stem}_{index}{originalPath.suffix}"
