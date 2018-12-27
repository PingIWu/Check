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

hAList = []
hApath = '/Users/Mac/job/LHE/Z*.lhe'
#path of lhefiles
hA_files = glob.glob(hApath)

#----------------Settings-----------------
lhaid=315200.0
tanbeta=1.0
gz=0.8
#-----------------------------------------

ID=[]

def getFile(fileName):
    num = str(fileName).split('_')[3] #[]is the nth object between 2_
    num2 = str(fileName).split('_')[4]
    num3 = str(fileName).split('_')[3]
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
                            ID.append(s.pdf)
                    if  lheFile.find('totfact') > 0: break
                hAList.append(s)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return hAList

def main():
    hAList = gethAList(hA_files)
    #hAList2 = gethAList2(hA_files2)
    textLine = []
    compare = [0,0,0,0,0,0,0]
    title=["file","mzp","ma0","LHAID","tanBeta","gz","process"]
    for a in hAList:
        #compare[0] = "lhefile"
        MZp=int(a.fileNum)
        MA0=int(a.fileNum2)
        Name=a.lhename
        print(a.pdf)   #PDF
        if (int(a.mzp) != 0):
            compare[1] = a.mzp
            #print(a.mzp)
        if (int(a.ma0) != 0):
            compare[2] = a.ma0
            #print(a.ma0)
        if (int(a.lhaid) != 0):
            compare[3] = a.lhaid
            #print(a.lhaid)
        if (int(a.tanbeta) != 0):
            compare[4] = a.tanbeta
        if (int(a.tanbeta) != 0):
            compare[5] = a.gz
        if (a.gener != 0):
            compare[6] = a.gener
        if (int(compare[1])==MZp and int(compare[2])!=0 and int(compare[3])==lhaid and int(compare[4])==tanbeta and compare[5]==gz and compare[6]!=0):
            
            #print(MA0,int(compare[2]))
            #print(a.mzp, a.ma0, a.lhaid, a.tanbeta, a.gz)
            #print(a.gener)
            compare = [Name, a.mzp, a.ma0, a.lhaid, a.tanbeta, a.gz, a.gener]
            print(123)
            textLine.append(["true"])
        
        else :
            print(456)
            print(a.mzp2, a.ma02, a.lhaid2, a.tanbeta2, a.gz2)
            compare = [Name, a.mzp, a.ma0, a.lhaid, a.tanbeta, a.gz, a.gener]
            textLine.append(["false"])

    with open("LHEcheck.txt", "w") as f:
        wr = csv.writer(f,delimiter="\t")
        wr.writerow(title)
        wr.writerow(compare)
        wr.writerows(textLine)

if __name__ == "__main__":
    main()

