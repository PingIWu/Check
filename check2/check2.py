#! /usr/bin/env python
#-------------------------------------------------------------
# File: genText.py
# Created: 12 May 2017 Shu-Xiao Liu
#-------------------------------------------------------------
import glob
import errno
#import ROOT
#from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
#from ROOT import TGraph2D, TGaxis
from array import array
import os
import csv
class GetValue():
    def __init__(self):
        self.fileNum = []
        self.mzp = []
        self.ma0 = []
        self.lhaid = []
        self.gener = []
        self.tanbeta = []
        self.gz = []
        self.pdf = []
        self.ID = []

hAList = []
hApath = '/Volumes/FAT/lhe_files/job*.lhe'
#'/Volumes/FAT/lhe_files/job*.lhe'
#'/Users/Mac/job/LHE/Z*.lhe'
#path of LHE files
hA_files = glob.glob(hApath)
n=str(hA_files).count('lhe') #count the amount of the files ----------have error
print(str(hA_files).count('lhe'))
#----------------Settings-----------------
lhaid=315200.0
tanbeta=1.0
gz=0.8
min=315200 #min value of PDFID
max=315300 #max
#-----------------------------------------

def getFile(fileName):
    num = str(fileName).split('_')[5] #MZp
    num2 = str(fileName).split('_')[6] #MA0
    num3 = str(fileName).split('/')[4] #filename
    #3/4/5 for original testing files
    #5/6/4 for real files
    global s
    s = GetValue()
    s.lhename = num3
    s.fileNum = num.strip('MZp')
    s.fileNum2 = num2.strip('MA')
    return s

def getMZpValue(readLine):
    mzpValue = readLine.strip().split(' # ')[0].split('32')[1]
    return mzpValue

def getMA0Value(readLine):
    ma0Value = readLine.strip().split(' # ')[0].split('28')[1]
    return ma0Value

def getLHAID(readLine):
    LHAID = int(readLine.strip().split('=')[0])
    return LHAID

def getTanBeta(readLine):
    tbValue  = readLine.split(' # ')[0].split()[1]
    return tbValue

def getgz(readLine):
    gzValue  = readLine.split(' # ')[0].split()[1]
    return gzValue

def getG(readLine):
    pros = readLine.strip().split('generate')[1]
    return pros

def getPDF(readLine):
    weightID = readLine.strip().split('"')[7]
    return weightID

def gethAList(lhefile):
    hAList = []
    for name in lhefile:
        s = getFile(name)
        try:
            with open(name) as f:
                s.ID=[]
                for lheFile in f:
                    if lheFile.find('mzp') > 0 and lheFile.find('32') > 0:
                        s.mzp = float(getMZpValue(lheFile))
                    elif lheFile.find('ma0') > 0 and lheFile.find('28') > 0:
                        s.ma0 = float(getMA0Value(lheFile))
                    elif lheFile.find('lhaid') > 0:
                        s.lhaid = float(getLHAID(lheFile))
                    elif lheFile.find('tb') > 0 and lheFile.find('#') > 0:
                        s.tanbeta = float(getTanBeta(lheFile))
                    elif lheFile.find('gz') > 0 and lheFile.find('#') > 0:
                        s.gz = float(getgz(lheFile))
                    elif lheFile.find('generate') == 0:
                        s.gener = getG(lheFile)
                    elif lheFile.find('weight') > 0 and lheFile.find('PDF') > 0 and lheFile.find('Member') > 0 :
                        s.pdf = int(getPDF(lheFile))
                        if s.pdf > 315199 and s.pdf < 315301 :
                            s.ID.append(s.pdf)
                    if  lheFile.find('totfact') > 0: break
                #print(s.ID)
                hAList.append(s)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return hAList

def main():
    hAList = gethAList(hA_files)
    textLine = []
    compare = [0,0,0,0,0,0,0]
    title=["file","mzp","ma0","LHAID","tanBeta","gz","process"]
    with open("LHEcheck.txt", "w") as g:
        for a in hAList:
            MZp=int(a.fileNum)
            MA0=int(a.fileNum2)
            Name=a.lhename
            PDF=1
            
            for i in range(min,max):
                if (a.ID.count(i)<1):
                    PDF=2

            if (int(a.mzp) != 0):
                compare[1] = a.mzp
            if (int(a.ma0) != 0):
                compare[2] = a.ma0
            if (int(a.lhaid) != 0):
                compare[3] = a.lhaid
            if (int(a.tanbeta) != 0):
                compare[4] = a.tanbeta
            if (int(a.tanbeta) != 0):
                compare[5] = a.gz
            if (a.gener != 0):
                compare[6] = a.gener
            if (int(compare[1])==MZp and int(compare[2])!=0 and int(compare[3])==lhaid and int(compare[4])==tanbeta and compare[5]==gz and compare[6]!=0 and PDF==1):
            
                compare = [Name, a.mzp, a.ma0, a.lhaid, a.tanbeta, a.gz, a.gener]
                print(123)
                textLine.append(["true"])
                '''#-------Also write on txt if true-------
                ZpMass=str(a.mzp)
                A0Mass=str(a.ma0)
                I=str(a.lhaid)
                TB=str(a.tanbeta)
                GZ=str(a.gz)
                Gen=str(a.gener)
                g.writelines(['File:',Name,'\n'])
                g.writelines(['MZp:',ZpMass,'\n'])
                g.writelines(['MA0:',A0Mass,'\n'])
                g.writelines(['LHAID:',I,'\n'])
                g.writelines(['tb:',TB,'\n'])
                g.writelines(['gz:',GZ,'\n'])
                g.writelines(['process:',Gen,'\n'])
                '''
                g.writelines(['true','\n'])
                g.writelines(['\n'])
            
            else :
                print(456)
                textLine.append(["false"])
                compare = [Name, a.mzp, a.ma0, a.lhaid, a.tanbeta, a.gz, a.gener]
                ZpMass=str(a.mzp)
                A0Mass=str(a.ma0)
                I=str(a.lhaid)
                TB=str(a.tanbeta)
                GZ=str(a.gz)
                Gen=str(a.gener)
                g.writelines(['false','\n'])
                g.writelines(['File:',Name,'\n'])
                g.writelines(['MZp from file name: ',str(MZp),'; MZp in the file: ',ZpMass,'\n'])
                g.writelines(['MA0 from file name: ',str(MA0),'; MA0 in the file: ',A0Mass,'\n'])
                g.writelines(['LHAID: ',str(lhaid),'; LHAID in the file: ',I,'\n'])
                g.writelines(['tb: ',str(tanbeta),'; tb in the file: ',TB,'\n'])
                g.writelines(['gz: ',str(gz),'; gz in the file: ',GZ,'\n'])
                g.writelines(['process: ',Gen,'\n'])
                g.writelines(['Missing PDFIDs: '])
                for i in range(min,max):
                    if (a.ID.count(i)<1):
                        g.writelines([str(i),'; '])
                g.writelines(['\n','\n'])

if __name__ == "__main__":
    main()

