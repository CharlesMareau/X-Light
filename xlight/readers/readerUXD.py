
from .reader import Reader
from ..core.utils import is_number_float
from ..core.profil import Profil




#le fichier est composé de blocks
#chaque block se termine par une ligne vide (ou la fin du fichier)
#le block i est compris entre la ligne block[i] et block[i+1]-2
#le premier block contient le header, les autres un profile


class ReaderUXD(Reader):

    FileExt="uxd"
    FileType="UXD BRUKER"

    def ReadBlock(lines):
        keys={}
        data=[]
        for line in lines:
            if line[0]=="_":
                split=line.strip().split("=")
                if (len(split)==2):
                    keys[split[0].strip()]=split[1].strip()
            elif is_number_float(line):
                data.append(float(line))
        return keys,data

    def Read(filename:str,parameters=None):
        try:
            profils=[]
            count=0
            with open(filename) as fp:
            #Check if file is binary
                try:
                    Lines = fp.readlines()
                except BaseException as e:
                    raise e

                blocks=[0]
                for line in Lines:
                    count += 1
                    if line[0]=="\n":
                        blocks.append(count)
                blocks.append(count+1)
            if (count<2):
                raise Exception("bad format")
            #keys,data=ReaderUXD.ReadBlock(Lines[blocks[0]:blocks[1]-2])   
            keys,data=ReaderUXD.ReadBlock(Lines[blocks[0]:blocks[1]-1]) #modified by ChM to avoid skipping last line from header
            anode=None
            if "_ANODE" in keys:
                anode=keys["_ANODE"]

            if "_FILEVERSION" in keys and (keys["_FILEVERSION"]=="2" or keys["_FILEVERSION"]=="3"):
                for i in range(1,len(blocks)-1):
                    profil=Profil()
                    keys,data=ReaderUXD.ReadBlock(Lines[blocks[i]:blocks[i+1]-2])
                    if anode:
                        profil.Anode.name=anode
                    if "_KHI" in keys:
                        profil.Khi=float(keys["_KHI"])
                    if "_PHI" in keys:
                        profil.Phi=float(keys["_PHI"])
                    theta=None
                    if "_THETA" in keys:
                        theta=float(keys["_THETA"])
                    stepsize=None
                    if "_STEPSIZE" in keys:
                        stepsize=float(keys["_STEPSIZE"])
                    if "_STEPTIME" in keys:
                        profil.Time=float(keys["_STEPTIME"])
                    start=None
                    if "_START" in keys:
                        start=float(keys["_START"])


                    if "_DRIVE" in keys:
                        if keys["_DRIVE"]=="COUPLED":
                            istep=0.0
                            for d in data:
                                omega=theta+stepsize*istep*0.5
                                twotheta=start+stepsize*istep
                                profil.AddData(d,twotheta,omega)
                                istep+=1.0
                        elif keys["_DRIVE"]=="2THETA":
                            istep=0.0
                            for d in data:
                                omega=theta
                                twotheta=start+stepsize*istep
                                profil.AddData(d,twotheta,omega)
                                istep+=1.0
                        else:
                            raise Exception("Bad Format")
                        profils.append(profil)
                    else:
                        raise Exception("Bad Format")
                return profils
        except BaseException as e:
            raise e



