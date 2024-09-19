
from .reader import Reader
from ..core.utils import is_number_float
from ..core.profil import Profil




#le fichier est composé de blocks
#chaque block se termine par une ligne vide (ou la fin du fichier)
#le block i est compris entre la ligne block[i] et block[i+1]-2
#le premier block contient le header, les autres un profile


class ReaderXY(Reader):

    FileExt="xy"
    FileType="XY FILE TYPE"

    def ReadBlock(lines):
        keys={}
        data=[]
        for line in lines:
            if line[0]=="_":
                split=line.strip().split("=")
                if (len(split)==2):
                    keys[split[0].strip()]=split[1].strip()
            else:
                split=line.strip().split()
                if len(split)==2:
                    if is_number_float(split[0]) & is_number_float(split[1]):
                        data.append([float(split[0]),float(split[1])])
        return keys,data

    def Read(filename:str,parameters=None):
        try:
            profils=[]
            count=0
            with open(filename) as fp:
                try:
                    Lines = fp.readlines()
                except BaseException as e:
                    raise e
                start=0
                finish=0
                for line in Lines:
                    finish += 1
            if (finish<start):
                raise Exception("bad format")
            # print("Count",count)
            keys,data=ReaderXY.ReadBlock(Lines[start:finish])
            anode=None
            if data==[]:
                print("No data in file ",filename)
            else:
                profil=Profil()
                if "_ANODE" in keys:
                    profil.Anode.name=keys["_ANODE"]
                if "_KHI" in keys:
                    profil.Khi=float(keys["_KHI"])
                if "_PHI" in keys:
                    profil.Phi=float(keys["_PHI"])
                if "_GAMMA" in keys:
                    profil.Gamma=float(keys["_GAMMA"])
                if "_OMEGA" in keys:
                    omega=float(keys["_OMEGA"])
                    for d in data:
                        twotheta=d[0]
                        intensity=d[1]
                        profil.AddData(intensity,twotheta,omega)
                else:
                    for d in data:
                        twotheta=d[0]
                        intensity=d[1]
                        omega=0.5*twotheta
                        profil.AddData(intensity,twotheta,omega)
                profils.append(profil)
            return profils
        except BaseException as e:
            raise e



