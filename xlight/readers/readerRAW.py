
from .reader import Reader

from ..core.utils import is_number_float

from ..core.profil import Profil



from PySide6.QtCore import QFile, QIODevice, QDateTime, QMetaType,QByteArray


from os import SEEK_SET
import struct



def hex2long(hexa):
    return struct.unpack("i",hexa)[0]

def hex2float(hexa):
    return struct.unpack("f",hexa)[0]

def hex2double(hexa):
    return struct.unpack("d",hexa)[0]






def readV4ExtraRecord10(f,pos,lenght, minimal=False):
    auxInfo={}
    sizeLong=4

    if lenght < 36:
        #qDebug() << QString("BrukerRawImport::readV4ExtraRecord10(): Illegal array size: %1").arg(a.size());
        return auxInfo

    if not minimal:
        f.seek(pos+8,SEEK_SET)
        iFlags=hex2long(f.read(sizeLong))
        #iFlags = hex2long(a.mid(8, sizeLong))
        #QString szType = a.mid(12, 24).trimmed();
        f.seek(pos+12,SEEK_SET)
        #szType=f.read(24).trimmed().data().decode().rstrip('\x00')
        szType=f.read(24).decode().rstrip('\x00')
        #print(szType)
        
        #read data only if it is in ASCII format, ignore binary format
        data=''
        if iFlags==0:
            f.seek(pos+36,SEEK_SET)
            data=f.read(lenght - 36).decode()
        #QString data = (iFlags == 0 ? a.mid(36, a.size() - 36).trimmed() : QString())
        auxInfo[szType]=data  ############################################TO MODIFY###########################################################
    return auxInfo




def readV4ExtraRecord30(f,pos,lenght,  minimal=False):
    auxInfo={}
    sizeLong=4
    sizeFloat=4
    sizeDouble=8
    
    if lenght < 136:
        #qDebug() << QString("BrukerRawImport::readV4ExtraRecord30(): Illegal array size: %1").arg(a.size());
        return auxInfo
    
    sizeFlags = 8 * sizeLong
    
    if not minimal:
        #store the bits of iGoniomModel in an array of bools:
        #flagsGoniomModel[0] = "0x1"
        #flagsGoniomModel[1] = "0x2"
        #flagsGoniomModel[2] = "0x4"
        #flagsGoniomModel[3] = "0x8"
        #flagsGoniomModel[4] = "0x10"
        #flagsGoniomModel[5] = "0x20"
        #...
        f.seek(pos+8,SEEK_SET)
        iGoniomModel = hex2long(f.read(sizeLong))
        flagsGoniomModel = [None]*sizeFlags
        
        for j in range(sizeFlags):
            flagsGoniomModel[j]=iGoniomModel == 1<<j
            
        
        lGoniomModel=[]
        if flagsGoniomModel[0]: lGoniomModel.append("D5000_TYPE")
        if flagsGoniomModel[1]: lGoniomModel.append("D5005_TYPE")
        if flagsGoniomModel[2]: lGoniomModel.append("D8_TYPE")
        if flagsGoniomModel[3]: lGoniomModel.append("D500_TYPE")
        if flagsGoniomModel[4]: lGoniomModel.append("OTHER_TYPE")
        if flagsGoniomModel[5]: lGoniomModel.append("D4_TYPE")
        if flagsGoniomModel[8]: lGoniomModel.append("THETA_2THETA")
        if flagsGoniomModel[9]: lGoniomModel.append("THETA_THETA")
        if flagsGoniomModel[10]: lGoniomModel.append("ALPHA_THETA")
        if flagsGoniomModel[11]: lGoniomModel.append("MATIC")
        if flagsGoniomModel[16]: lGoniomModel.append("GADDS")
        if flagsGoniomModel[17]: lGoniomModel.append("SAXS")
        if flagsGoniomModel[18]: lGoniomModel.append("SMART")
        if flagsGoniomModel[19]: lGoniomModel.append("OTHER_SYSTEM")
        
        auxInfo["iGoniomModel"]=lGoniomModel

        f.seek(pos+12,SEEK_SET)
        iGoniomStage = hex2long(f.read(sizeLong))
        if (iGoniomStage == 0): auxInfo["iGoniomStage"]="STANDARD_STAGE"
        if (iGoniomStage == 1): auxInfo["iGoniomStage"]="SYNCHR_ROT"
        if (iGoniomStage == 2): auxInfo["iGoniomStage"]="ROT_REFLECTION"
        if (iGoniomStage == 3): auxInfo["iGoniomStage"]="ROT_TRANSMISSION"
        if (iGoniomStage == 4): auxInfo["iGoniomStage"]="OPEN_CRADLE"
        if (iGoniomStage == 5): auxInfo["iGoniomStage"]="CLOSED_CRADLE"
        if (iGoniomStage == 6): auxInfo["iGoniomStage"]="QUARTER_CRADLE"
        if (iGoniomStage == 7): auxInfo["iGoniomStage"]="PHI_STAGE"
        if (iGoniomStage == 8): auxInfo["iGoniomStage"]="CHI_STAGE"
        if (iGoniomStage == 9): auxInfo["iGoniomStage"]="XYZ_STAGE"
        if (iGoniomStage == 10): auxInfo["iGoniomStage"]="LOW_TEMP"
        if (iGoniomStage == 11): auxInfo["iGoniomStage"]="HIGH_TEMP"
        if (iGoniomStage == 12): auxInfo["iGoniomStage"]="EXTERNAL_TEMP"
        if (iGoniomStage == 13): auxInfo["iGoniomStage"]="PHI_AT_FIXED_CHI"
        if (iGoniomStage == 14): auxInfo["iGoniomStage"]="FOUR_CYCLE"
        if (iGoniomStage == 15): auxInfo["iGoniomStage"]="SMALL_XYZ_STAGE"
        if (iGoniomStage == 16): auxInfo["iGoniomStage"]="LARGE_XYZ_STAGE"
        if (iGoniomStage == 17): auxInfo["iGoniomStage"]="UNKNOWN"

        f.seek(pos+16,SEEK_SET)
        iSampleChanger = hex2long(f.read(sizeLong))
        if (iSampleChanger == 0): auxInfo["iSampleChanger"]="NONE"
        if (iSampleChanger == 1): auxInfo["iSampleChanger"]="FOURTY_POSITION"
        if (iSampleChanger == 2): auxInfo["iSampleChanger"]="Y_MATIC"
        if (iSampleChanger == 3): auxInfo["iSampleChanger"]="XY_MATIC"
        if (iSampleChanger == 4): auxInfo["iSampleChanger"]="MANUAL"
        if (iSampleChanger == 5): auxInfo["iSampleChanger"]="UNKNOWN"

        f.seek(pos+20,SEEK_SET)
        iGoniomCtrl = hex2long(f.read(sizeLong))
        flagsGoniomCtrl = [None]*sizeFlags
        for j in range(sizeFlags):
            flagsGoniomCtrl[j]=iGoniomCtrl == 1<<j

        lGoniomCtrl=[]
        if (flagsGoniomCtrl[0]): lGoniomCtrl.append("DIFF_CONT")
        if (flagsGoniomCtrl[1]): lGoniomCtrl.append("TC_SOC")
        if (flagsGoniomCtrl[2]): lGoniomCtrl.append("FDC_SOC")
        if (flagsGoniomCtrl[3]): lGoniomCtrl.append("TC_OTHER")
        if (flagsGoniomCtrl[4]): lGoniomCtrl.append("FDC_OTHER")
        if (flagsGoniomCtrl[5]): lGoniomCtrl.append("GGCS")
        if (flagsGoniomCtrl[6]): lGoniomCtrl.append("UNKNOWN")
        auxInfo["iGoniomCtrl"]=lGoniomCtrl

        f.seek(pos+24,SEEK_SET)
        auxInfo["fGoniomDiameter"]=hex2float(f.read(sizeFloat))

        f.seek(pos+28,SEEK_SET)
        iSyncAxis = hex2long(f.read(sizeLong))
        if (iSyncAxis == 0): auxInfo["iSyncAxis"]="NONE"
        if (iSyncAxis == 1): auxInfo["iSyncAxis"]="REFLECTION_PHI"
        if (iSyncAxis == 2): auxInfo["iSyncAxis"]="TRANSMISSION_PHI"
        if (iSyncAxis == 3): auxInfo["iSyncAxis"]="X_CLOSED_CRADLE"

        f.seek(pos+32,SEEK_SET)
        iBeamOpticsFlags = hex2long(f.read(sizeLong))

        flagsBeamOpticsFlags = [None]*sizeFlags
        for j in range(sizeFlags):
            flagsBeamOpticsFlags[j]=iBeamOpticsFlags == 1<<j
        lBeamOpticsFlags=[]
        if (flagsBeamOpticsFlags[0]): lBeamOpticsFlags.append("DIVSLIT_SET")
        if (flagsBeamOpticsFlags[1]): lBeamOpticsFlags.append("NEAR_SAMPLE_SLIT_SET")
        if (flagsBeamOpticsFlags[2]): lBeamOpticsFlags.append("PRIM_SOLLER_SLIT_SET")
        if (flagsBeamOpticsFlags[3]): lBeamOpticsFlags.append("ANTISC_SLIT_SET")
        if (flagsBeamOpticsFlags[4]): lBeamOpticsFlags.append("DET_SLIT_SET")
        if (flagsBeamOpticsFlags[5]): lBeamOpticsFlags.append("SEC_SOLLER_SLIT_SET")
        if (flagsBeamOpticsFlags[6]): lBeamOpticsFlags.append("THINFILM_ATT_SET")
        if (flagsBeamOpticsFlags[7]): lBeamOpticsFlags.append("BETA_FILTER_SET")
        if (flagsBeamOpticsFlags[8]): lBeamOpticsFlags.append("MOT_SLIT_CHANGER_SET")
        if (flagsBeamOpticsFlags[9]): lBeamOpticsFlags.append("MOT_ABS_CHANGER_SET")
        if (flagsBeamOpticsFlags[10]): lBeamOpticsFlags.append("MOT_ROTARY_ABSORBER_SET")
        auxInfo["iBeamOpticsFlags"]=lBeamOpticsFlags

        f.seek(pos+36,SEEK_SET)
        auxInfo["fDivSlit"]=hex2float(f.read(sizeFloat))
        f.seek(pos+40,SEEK_SET)
        auxInfo["fNearSampleSlit"]=hex2float(f.read(sizeFloat))
        f.seek(pos+44,SEEK_SET)
        auxInfo["fPrimSollerSlit"]=hex2float(f.read(sizeFloat))

        f.seek(pos+48,SEEK_SET)
        iMonochromator = hex2long(f.read(sizeLong))
        if (iMonochromator == 0): auxInfo["iMonochromator"]="NONE"
        if (iMonochromator == 1): auxInfo["iMonochromator"]="TRANSMISSION_MONO"
        if (iMonochromator == 2): auxInfo["iMonochromator"]="REFLECTION_MONO"
        if (iMonochromator == 3): auxInfo["iMonochromator"]="GE220_2_BOUNCE"
        if (iMonochromator == 4): auxInfo["iMonochromator"]="GE220_4_BOUNCE"
        if (iMonochromator == 5): auxInfo["iMonochromator"]="GE440_4_BOUNCE"
        if (iMonochromator == 6): auxInfo["iMonochromator"]="FLAT_GRAPHITE_MONO"
        if (iMonochromator == 7): auxInfo["iMonochromator"]="SINGLE_GOEBEL_MIRROR"
        if (iMonochromator == 8): auxInfo["iMonochromator"]="CROSSED_GOEBEL_MIRROR"
        if (iMonochromator == 9): auxInfo["iMonochromator"]="FLAT_GERMANIUM_111"
        if (iMonochromator == 10): auxInfo["iMonochromator"]="FLAT_SILICON_111"
        if (iMonochromator == 11): auxInfo["iMonochromator"]="GE_REFLECTION"
        if (iMonochromator == 12): auxInfo["iMonochromator"]="ASYM_GE_4_BOUNCE"
        if (iMonochromator == 13): auxInfo["iMonochromator"]="UNKNOWN"

        f.seek(pos+52,SEEK_SET)
        auxInfo["fAntiScSlit"]=hex2float(f.read(sizeFloat))
        f.seek(pos+56,SEEK_SET)
        auxInfo["fDetSlit"]=hex2float(f.read(sizeFloat))
        f.seek(pos+60,SEEK_SET)
        auxInfo["fSecondSollerSlit"]=hex2float(f.read(sizeFloat))
        f.seek(pos+64,SEEK_SET)
        auxInfo["fThinFilmAtt"]=hex2float(f.read(sizeFloat))

        f.seek(pos+68,SEEK_SET)
        iAnalyzer = hex2long(f.read(sizeLong))
        if (iAnalyzer == 0): auxInfo["iAnalyzer"]="NONE"
        if (iAnalyzer == 1): auxInfo["iAnalyzer"]="GRAPHITE_ANALYZER"
        if (iAnalyzer == 2): auxInfo["iAnalyzer"]="LIF_ANALYZER"
        if (iAnalyzer == 3): auxInfo["iAnalyzer"]="GE220_CHANNEL_CUT"
        if (iAnalyzer == 4): auxInfo["iAnalyzer"]="GOEBEL_MIRROR_ANALYZER"
        if (iAnalyzer == 5): auxInfo["iAnalyzer"]="UNKNOWN"
        
        #// wavelengths are read outside the "minimal" condition

        f.seek(pos+104,SEEK_SET)
        auxInfo["fAlphaRatio"]=hex2double(f.read(sizeDouble))
        f.seek(pos+112,SEEK_SET)
        auxInfo["fBetaRelInt"]=hex2float(f.read(sizeFloat))
        f.seek(pos+116,SEEK_SET)
        auxInfo["szAnode"]=f.read(4).decode().rstrip('\x00')
        f.seek(pos+120,SEEK_SET)
        auxInfo["szWaveUnit"]=f.read(4).decode().rstrip('\x00')
        f.seek(pos+124,SEEK_SET)
        auxInfo["fActivateAbsorber"]=hex2float(f.read(sizeFloat))
        f.seek(pos+128,SEEK_SET)
        auxInfo["fDeactivateAbsorber"]=hex2float(f.read(sizeFloat))
        f.seek(pos+123,SEEK_SET)
        auxInfo["fAbsFactor"]=hex2float(f.read(sizeFloat))
    #// wavelengths
    f.seek(pos+72,SEEK_SET)
    auxInfo["fAlphaAverage"]=hex2double(f.read(sizeDouble))
    f.seek(pos+80,SEEK_SET)
    auxInfo["fAlpha1"]=hex2double(f.read(sizeDouble))
    f.seek(pos+88,SEEK_SET)
    auxInfo["fAlpha2"]=hex2double(f.read(sizeDouble))
    f.seek(pos+96,SEEK_SET)
    auxInfo["fBeta"]=hex2double(f.read(sizeDouble))
    return auxInfo











def readV4ExtraRecord50(f,pos,lenght, minimal=False):
    auxInfo={}
    sizeLong=4
    sizeFloat=4
    sizeDouble=8

    if lenght < 64:
        #qDebug() << QString("BrukerRawImport::readV4ExtraRecord10(): Illegal array size: %1").arg(a.size());
        return auxInfo

    f.seek(pos+12,SEEK_SET)
    szType=f.read(36).decode().rstrip('\x00')
    szType.rstrip(" ")
    f.seek(pos+56,SEEK_SET)
    auxInfo[szType]=hex2double(f.read(sizeDouble))

    return auxInfo


def readV4ExtraRecord110(f,pos,lenght, minimal=False):
    auxInfo={}
    sizeLong=4
    sizeFloat=4
    sizeDouble=8

    return auxInfo











def readV4RangeHeader(f,pos,lenght, minimal=False):
    sizeLong=4
    sizeFloat=4
    sizeDouble=8
    auxInfo={}

    if (lenght < 160):
        #qDebug() << QString("BrukerRawImport::readV4RangeHeader(): Illegal array size: %1").arg(a.size());
        return auxInfo


    sizeFlags = 8 * sizeLong

    if (not minimal):
        #// optional data
        f.seek(pos+0,SEEK_SET)
        auxInfo["iDataLength"]=hex2long(f.read(sizeLong))
        f.seek(pos+4,SEEK_SET)
        auxInfo["iNoOfMeasuredData"]=hex2long(f.read(sizeLong))
        f.seek(pos+8,SEEK_SET)
        auxInfo["iNoOfCompletedData"]=hex2long(f.read(sizeLong))
        f.seek(pos+12,SEEK_SET)
        auxInfo["iNoOfConfDrives"]=hex2long(f.read(sizeLong))

        f.seek(pos+16,SEEK_SET)
        iMotSlitChangerIn = hex2long(f.read(sizeLong))
        if (iMotSlitChangerIn == 0): auxInfo["iMotSlitChangerIn"]="MOT_CHANGER_OUT"
        if (iMotSlitChangerIn == 1): auxInfo["iMotSlitChangerIn"]="MOT_CHANGER_IN"
        if (iMotSlitChangerIn == 2): auxInfo["iMotSlitChangerIn"]="MOT_CHANGER_AUTO"

        f.seek(pos+20,SEEK_SET)
        auxInfo["iNoOfDetectors"]=hex2long(f.read(sizeLong))

        f.seek(pos+24,SEEK_SET)
        iAdditionalDetectorFlags = hex2long(f.read(sizeLong))
        flagsAdditionalDetectorFlags = [None]*sizeFlags
        for j in range(sizeFlags):
            flagsAdditionalDetectorFlags[j]=iAdditionalDetectorFlags == 1<<j
        
        lAdditionalDetectorFlags=[]
        if (flagsAdditionalDetectorFlags[0]): lAdditionalDetectorFlags.append("PSD_SET")
        if (flagsAdditionalDetectorFlags[1]): lAdditionalDetectorFlags.append("AD_SET")
        if (flagsAdditionalDetectorFlags[2]): lAdditionalDetectorFlags.append("PSD_MEASURED")
        if (flagsAdditionalDetectorFlags[3]): lAdditionalDetectorFlags.append("AD_MEASURED")
        if (flagsAdditionalDetectorFlags[4]): lAdditionalDetectorFlags.append("PSD_SAVED")
        if (flagsAdditionalDetectorFlags[5]): lAdditionalDetectorFlags.append("AD_SAVED")
        if (flagsAdditionalDetectorFlags[6]): lAdditionalDetectorFlags.append("NONE")
        auxInfo["iAdditionalDetectorFlags"]=lAdditionalDetectorFlags

        f.seek(pos+28,SEEK_SET)
        iScanMode = hex2long(f.read(sizeLong))
        if (iScanMode == 0): auxInfo["iScanMode"]="STEPSCAN"
        if (iScanMode == 1): auxInfo["iScanMode"]="CONTINUOUSSCAN"
        if (iScanMode == 2): auxInfo["iScanMode"]="CONTINUOUSSTEPSCAN"


        f.seek(pos+32,SEEK_SET)
        auxInfo["szScanType"]=f.read(24).decode().rstrip('\x00')
        f.seek(pos+56,SEEK_SET)
        auxInfo["iSynchRotation"]=hex2long(f.read(sizeLong))
        f.seek(pos+60,SEEK_SET)
        auxInfo["fMeasDelayTime"]=hex2float(f.read(sizeFloat))
        f.seek(pos+64,SEEK_SET)
        auxInfo["iEstScanTime"]=hex2long(f.read(sizeLong))
        f.seek(pos+68,SEEK_SET)
        auxInfo["fRangeSampleStarted"]=hex2float(f.read(sizeFloat))
        #// fStart, fIncrement, iSteps, iExtraRecordSize, fStepTime are required
        f.seek(pos+96,SEEK_SET)
        auxInfo["fRotationSpeed"]=hex2float(f.read(sizeFloat))
        f.seek(pos+100,SEEK_SET)
        auxInfo["fGeneratorVoltage"]=hex2float(f.read(sizeFloat))
        f.seek(pos+104,SEEK_SET)
        auxInfo["fGeneratorCurrent"]=hex2float(f.read(sizeFloat))
        f.seek(pos+108,SEEK_SET)
        auxInfo["iDisplayPlaneNumber"]=hex2long(f.read(sizeLong))
        f.seek(pos+112,SEEK_SET)
        auxInfo["fActUsedLambda"]=hex2double(f.read(sizeDouble))
        f.seek(pos+120,SEEK_SET)
        auxInfo["iNoOfVaryingParams"]=hex2long(f.read(sizeLong))
        f.seek(pos+124,SEEK_SET)
        auxInfo["iNoCounts"]=hex2long(f.read(sizeLong))
        f.seek(pos+128,SEEK_SET)
        auxInfo["iNoEncoderDrives"]=hex2long(f.read(sizeLong))

        f.seek(pos+132,SEEK_SET)
        iExtraParamFlags = hex2long(f.read(sizeLong))
        flagsExtraParamFlags = [None]*sizeFlags #8 * 4, 4 is the size of long on a 32bit system
        for j in range(sizeFlags):
            flagsExtraParamFlags[j]=iExtraParamFlags == 1<<j


        lExtraParamFlags=[]

        if (flagsExtraParamFlags[0]): lExtraParamFlags.append("VARIABLE_TIME_PER_STEP")
        auxInfo["iExtraParamFlags"]=lExtraParamFlags

        f.seek(pos+136,SEEK_SET)
        auxInfo["iDataRecordLength"]=hex2long(f.read(sizeLong))
        #iExtraRecordSize is required
        f.seek(pos+144,SEEK_SET)
        auxInfo["fSmoothingWidth"]=hex2float(f.read(sizeFloat))
        f.seek(pos+148,SEEK_SET)
        auxInfo["iSimMeasCond"]=hex2long(f.read(sizeLong))
        f.seek(pos+152,SEEK_SET)
        auxInfo["fIncrement_3"]=hex2double(f.read(sizeDouble))
            
        
    #required data
    f.seek(pos+72,SEEK_SET)
    auxInfo["fStart"]=hex2double(f.read(sizeDouble))
    f.seek(pos+80,SEEK_SET)
    auxInfo["fIncrement"]=hex2double(f.read(sizeDouble))
    f.seek(pos+88,SEEK_SET)
    auxInfo["iSteps"]=hex2long(f.read(sizeLong))
    f.seek(pos+92,SEEK_SET)
    auxInfo["fStepTime"]=hex2float(f.read(sizeFloat))
    f.seek(pos+140,SEEK_SET)
    auxInfo["iExtraRecordSize"]=hex2long(f.read(sizeLong))
    
    return auxInfo




class ReaderRAW(Reader):

    FileExt="raw"
    FileType="RAW BRUKER"


    def Read(filename:str,parameters=None):
        try:
            sizeLong=4
            sizeFloat=4
            sizeDouble=8

            profils=[]

            #QFile f(fileName);
            f=QFile(filename)

            if not f.open(QIODevice.ReadOnly):
                raise Exception("Bad Format")
                #return None
        

            a = f.readAll()
            f.close()


            f=open(filename, "rb")
            #f.seek(40,SEEK_SET)
            #val=f.read(4)
            #print(struct.unpack("i",val))
            #f.close()


            #print(a.mid(40, sizeLong))
            #print(struct.unpack("i",b'\x08\x00\x00\x00'))
            #print(struct.unpack("i",a.mid(40, sizeLong).trimmed()))
            #struct.unpack("i",hexa)

            
            #szDate = QDateTime.fromString(a.mid(12, 12).trimmed().data().decode(), "MM/dd/yyyy")
            #szTime = QDateTime.fromString(a.mid(24, 12).trimmed().data().decode(), "hh:mm:ss")

            

            f.seek(40,SEEK_SET)
            iNoOfRanges = hex2long(f.read(sizeLong))

            f.seek(44,SEEK_SET)
            iNoOfMeasuredRanges = hex2long(f.read(sizeLong))
            f.seek(56,SEEK_SET)
            iExtraRecordSize = hex2long(f.read(sizeLong))
            
            f.seek(60,SEEK_SET)
            szFurther_dql_reading = struct.unpack("?",f.read(1))[0]



            pos = 61

            if szFurther_dql_reading:
                f.seek(pos+sizeLong,SEEK_SET)
                pos += struct.unpack("i",f.read(sizeLong))[0]  #STRANGE, TO VERIFY!

            r = 1

            anode=None

            f.seek(0,2) #end on file
            fsize=f.tell() #file size
            #print(fsize)
            #print(a.size())

            while pos < 61 + iExtraRecordSize:
                #range check, give headroom to read two long variables
                if pos >= fsize - 8:
                    break
                f.seek(pos,SEEK_SET)
                iRecordType = hex2long(f.read(sizeLong))
                f.seek(pos+sizeLong,SEEK_SET)
                iRecordLength = hex2long(f.read(sizeLong))

                #print(iRecordType)
                #qDebug() << QString("BrukerRawImport::readV4(): Extra record %1 parsed").arg(r);

                #parse V4_VARIABLE_INFO records
                if iRecordType == 10:
                    #qDebug() << QString("BrukerRawImport::readV4(): Variable record at %1").arg(pos);
                    #varInfoMap.unite(readV4ExtraRecord10(a.mid(pos, iRecordLength), minimal));
                    Info=readV4ExtraRecord10(f,pos,iRecordLength)
            
                #parse V4_RAW_HARDWARE_CONF
                if iRecordType == 30:
                    #qDebug() << QString("BrukerRawImport::readV4(): Hardware record at %1").arg(pos);
                    #hwConfMap.unite(readV4ExtraRecord30(a.mid(pos, iRecordLength), minimal));
                    Info=readV4ExtraRecord30(f,pos,iRecordLength)
                    if "szAnode" in Info:
                        anode=Info["szAnode"]
            
                #move to beginning of next block
                pos += iRecordLength
                r+=1


            cRanges = 0

            #print(iNoOfMeasuredRanges, iNoOfRanges)

            for n in range(min(iNoOfMeasuredRanges, iNoOfRanges)):
                profil=Profil()
                if anode:
                    profil.Anode.name=anode
                #/* V4_RAW_RANGE_HEADER */
                #print(n)
                if pos + 160 >= fsize:
                    #break
                    raise Exception("Bad Format")
                #print(n)
                rangeHeaderMap = readV4RangeHeader(f,pos, 160)
                coupled=False
                if rangeHeaderMap['szScanType']=="Unlocked Coupled":
                    coupled=True
                #print(coupled)

                fStart=-1.0
                if "fStart" in rangeHeaderMap:
                    fStart=rangeHeaderMap["fStart"]
                fIncrement=-1.0
                if "fIncrement" in rangeHeaderMap:
                    fIncrement=rangeHeaderMap["fIncrement"]
                iSteps=-1
                if "iSteps" in rangeHeaderMap:
                    iSteps=rangeHeaderMap["iSteps"]
                iExtraRecordSize=-1
                if "iExtraRecordSize" in rangeHeaderMap:
                    iExtraRecordSize=rangeHeaderMap["iExtraRecordSize"]
                fStepTime=-1.0
                if "fStepTime" in rangeHeaderMap:
                    fStepTime=rangeHeaderMap["fStepTime"]
            
                if (fIncrement < 0.0):
                    raise Exception("Bad Format")
                    #return None

                if iExtraRecordSize>2*sizeLong:
                    f.seek(pos+160,SEEK_SET)
                    iRecordType = hex2long(f.read(sizeLong))
                    f.seek(pos+160+sizeLong,SEEK_SET)
                    iRecordLength = hex2long(f.read(sizeLong))
                    if iRecordType == 10:
                        Info=readV4ExtraRecord10(f,pos,iRecordLength)



                r = 1
                pos+=160
                pos2=pos

                omega=0.0
                while pos2 < pos+iExtraRecordSize:
                    #range check, give headroom to read two long variables
                    if pos2 >= fsize - 8:
                        break
                    f.seek(pos2,SEEK_SET)
                    iRecordType = hex2long(f.read(sizeLong))
                    f.seek(pos2+sizeLong,SEEK_SET)
                    iRecordLength = hex2long(f.read(sizeLong))
                    #print(iRecordType)  ###############################################################ECRIRE LE 110 #################################################################
                    if iRecordType == 50:
                        Info=readV4ExtraRecord50(f,pos2,iRecordLength)
                        #print(Info)
                        if "Theta" in Info:
                            omega=Info["Theta"]
                        if "Chi" in Info:
                            profil.Khi=Info["Chi"]
                        if "Phi" in Info:
                            profil.Phi=Info["Phi"]
                    if iRecordType == 110:
                        Info=readV4ExtraRecord110(f,pos2, iRecordLength)
                    #parse V4_VARIABLE_INFO records
                    if iRecordType == 10:
                        Info=readV4ExtraRecord10(f,pos2, iRecordLength)
                        #print(Info)
                    #parse V4_RAW_HARDWARE_CONF
                    if iRecordType == 30:
                        Info=readV4ExtraRecord30(f,pos2, iRecordLength)
                    #move to beginning of next block
                    pos2 += iRecordLength
                    r+=1



            
            
                pos +=  iExtraRecordSize
            
                #/* V4 Intensities */
                #Scan scan(name, QColor(), 1);
                #scan.setSourceFileName(fname);
                #scan.setAuxInfo("FormatVersion", QVariant("RAW4"));
            
                #scan.setName(name);
                #scan.setComment(comment);
                #scan.setAuxInfo("MeasureDate", QVariant(szDate));
                #scan.setAuxInfo("MeasureTime", QVariant(szTime));
                #scan.setWaveLength(lambda1);
                #scan.setWaveLength2(lambda2);
                #scan.setTimePerStep(fStepTime);
            
                #// initialize the vectors
                #QVector<double> vec_a;       // angle
                #QVector<double> vec_i;       // intensity
            
                #vec_a.reserve(iSteps);
                #vec_i.reserve(iSteps);
            
                #scan.setStepSize(fIncrement);
            
                ang = fStart;
            
                #// read data
                for j in range(iSteps):
                    if pos >= fsize:
                        #qDebug() << QString("BrukerRawImport::readV4(): Reached the end of the input array.");
                        raise Exception("Bad Format")
                        #return None
            
                    f.seek(pos,SEEK_SET)
                    intens = hex2float(f.read(sizeFloat))
                    profil.AddData(intens,ang,omega)
            
                    #vec_a.push_back(ang);
                    #vec_i.push_back(intens);
                    #print(n,ang,intens)

                    ang += fIncrement
                    if coupled:
                        omega+=fIncrement/2.0
                    pos += sizeFloat
                profils.append(profil)
        
            #scan.setDataAng(vec_a);
            #scan.setDataInt(vec_i);
        
            #// store aux info in scan
            #scan.addAuxInfo(varInfoMap);
            #scan.addAuxInfo(hwConfMap);
            #scan.addAuxInfo(rangeHeaderMap);

            #// store scan in scanHeap
            #scan.setTypes(Scan::XY | Scan::MEASURED);
            #scanHeap.push_back(scan);
        
            #cRanges = n;




            f.close()
            return profils
        except BaseException as e:
            raise e












