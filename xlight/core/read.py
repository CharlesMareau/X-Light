#from readers import *

#import readers as readers
#from core.model import *
import os.path
from ..readers import Reader



def GetExt():
    exts=[]
    for s in Reader.__subclasses__():
        exts.append(s.FileExt)
    return exts

def GetListReader():
    re=[]
    for s in Reader.__subclasses__():
        re.append(s)
    return re


def ReadFile(filename:str,parameters=None):
    #for s in readers.Reader.__subclasses__():
    ext=os.path.splitext(filename)[1]

    for R in GetListReader():
        Rext="."+R.FileExt
        #print(Rext,ext)
        if Rext==ext:
            return R.Read(filename,parameters)
    raise Exception("No Reader Found for file "+filename)
    
    
    #for s in Reader.__subclasses__():
    #    #print(s.__name__+" "+s.FileExt)
    #    try:
    #        p=s.Read(filename)
    #        #print(p)
    #        return p
    #    except BaseException as e:
    #        pass
    #        #print(str(e))
    #raise Exception("No Reader Found")
    #    #if p:
    #    #    return p
    ##return None
