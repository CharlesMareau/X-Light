import os

IconFile=os.path.join(os.path.dirname(__file__),'icon','icon.ico')

def GetConfigPath():
    paths=[]
    paths.append(os.path.join(os.path.dirname(__file__),"database"))
    return paths

def GetMaterialDict():
    materials=dict()
    CPATHS=GetConfigPath()
    for P in CPATHS:
        DIR=os.path.join(P,"materials")
        for F in os.listdir(DIR):
            if F.endswith(".txt"):
                materials[os.path.splitext(F)[0]]=os.path.join(DIR,F)
    return materials

def GetAnodeDict():
    anodes=dict()
    CPATHS=GetConfigPath()
    for P in CPATHS:
        DIR=os.path.join(P,"anodes")
        for F in os.listdir(DIR):
            if F.endswith(".txt"):
                anodes[os.path.splitext(F)[0]]=os.path.join(DIR,F)
    return anodes

def GetDetectorDict():
    detectors=dict()
    CPATHS=GetConfigPath()
    for P in CPATHS:
        DIR=os.path.join(P,"detectors")
        for F in os.listdir(DIR):
            if F.endswith(".txt"):
                detectors[os.path.splitext(F)[0]]=os.path.join(DIR,F)
    return detectors



TOL_PIC=0.1
