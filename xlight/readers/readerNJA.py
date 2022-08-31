
from .reader import Reader

from ..core.utils import is_number_float

from ..core.profil import Profil




#le fichier est composé de blocks
#chaque block se termine par une ligne vide (ou la fin du fichier)
#le block i est compris entre la ligne block[i] et block[i+1]-2
#le 1 premier block contient le header, le deuxième le nombre de profile
#2 blocks: paramètres et valeurs x le nb de profils  


class ReaderNJA(Reader):

    FileExt="nja"
    FileType="NJA FILE TYPE"


    def SplitLine(line):
        keys={}
        split=line.strip().split("\t")
        for s in split:
            if s[0]=="&":
                split2=s.split("=")
                if (len(split2)==2):
                    keys[split2[0]]=split2[1]
        return keys
    
    def ReadBlock(lines):
        keys={}
        data=[]
        keys["Axis"]={}
        
        for line in lines:
            k=ReaderNJA.SplitLine(line)
            if "&Axis" in k:
                name=k["&Axis"]
                del k["&Axis"]
                keys["Axis"][name]=k
                #print(k)
            else:
                for kk in k:
                    keys[kk]=k[kk]
        return keys,data

    def ReadData(lines):
        data=[]
        for line in lines:
            split=line.strip().split("\t")
            if len(split)==2:
                if is_number_float(split[0]) & is_number_float(split[1]):
                    data.append([float(split[0]),float(split[1])])
        return data 

        
    def Read(filename:str,parameters=None):
        try:
            profils=[]
            count=0
            with open(filename) as fp:
                #Check if file is binary
                Lines = fp.readlines()
                blocks=[0]
                for line in Lines:
                    count += 1
                    if line[0]=="\n":
                        blocks.append(count)
                blocks.append(count+1)
                if (count<2):
                    raise Exception("Bad Format")
                    #return None
                keys,data=ReaderNJA.ReadBlock(Lines[blocks[0]:blocks[1]-1])
                anode=None
                if "&Anode" in keys:
                    anode=keys["&Anode"]
                keys,data=ReaderNJA.ReadBlock(Lines[blocks[1]:blocks[2]-1])
                nprofiles=0
                if not "&NumScans" in keys:
                    raise Exception("Bad Format")
                    #return None
                nprofiles=int(keys["&NumScans"])
                if len(blocks)-1!=2*nprofiles+2:
                    raise Exception("Bad Format")
                    #return None
                ib=2
                for p in range(nprofiles):
                    profil=Profil()
                    profil.Anode.name=anode
                    keys,data=ReaderNJA.ReadBlock(Lines[blocks[ib]:blocks[ib+1]-1])
                    #print(keys["Axis"])
                    if not "&ScanAxis" in keys:
                        raise Exception("Error during nja file -> &ScanAxis Not found")
                        #print("Error during nja file -> &ScanAxis Not found")
                        #return None
                    Omega=None
                    if keys["&ScanAxis"]=="T":
                        if not "O" in keys["Axis"]:
                            raise Exception("Error during nja file -> &ScanAxis=T and Axis=O Not found")
                            #return None
                        if not "&Pos" in keys["Axis"]["O"]:
                            raise Exception("Error during nja file -> &ScanAxis=T, Axis=O but &Pos is not found")
                            #return None
                        Omega=float(keys["Axis"]["O"]["&Pos"])
                    Phi=None
                    if "P" in keys["Axis"]:
                        if "&Pos" in keys["Axis"]["P"]:
                            Phi=float(keys["Axis"]["P"]["&Pos"])
                            profil.Phi=Phi
                    Khi=None
                    if "C" in keys["Axis"]:
                        if "&Pos" in keys["Axis"]["C"]:
                            Khi=float(keys["Axis"]["C"]["&Pos"])
                            profil.Khi=Khi
                    if "&Time" in keys:
                        profil.Time=float(keys["&Time"])
                    ib+=1
                    data=ReaderNJA.ReadData(Lines[blocks[ib]:blocks[ib+1]-1])
                    for d in data:
                        if Omega:
                            profil.AddData(d[1],d[0],Omega)
                        else:
                            profil.AddData(d[1],d[0],0.5*d[0])
                    ib+=1
                    profils.append(profil)
                return profils
        except BaseException as e:
            raise e
            












