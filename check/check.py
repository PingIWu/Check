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
        self.mzp2 = []
        self.ma02 = []
        self.tanbeta2 = []
        self.lhaid2 = []
        self.gz2 = []

hAList = []
hAList2 = []
hApath = '/Users/Mac/MG5_aMC_v2_6_2/forDCS/MZpWrong/j*.lhe'
hApath2 = '/Users/Mac/MG5_aMC_v2_6_2/forDCS/MZpWrong/Zprime_A0h_A0chichi_MZp1400_MA0400/Z*.dat'
hA_files = glob.glob(hApath)
hA_files2 = glob.glob(hApath2)

def getFile(fileName):
    num = str(fileName).split('_')[8] #[]is the nth object between 2_
    global s
    s = GetValue()
    s.fileNum = num
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
                    if  lheFile.find('initrwgt') > 0: break
                hAList.append(s)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return hAList

def getMZpValue2(readLine):
    print readLine
    mzpValue2 = readLine.split(' ')[4]
    return mzpValue2

def getMA0Value2(readLine):
    ma0Value2 = readLine.split(' ')[4]
    return ma0Value2

def getTanBeta2(readLine):
    tbValue2  = readLine.strip().split(' ')[4]
    return tbValue2

def getgz2(readLine):
    gzValue2  = readLine.strip().split(' ')[4]
    return gzValue2

def getLHAID2(readLine):
    LHAID2 = int(readLine.strip().split('=')[0])
    return LHAID2

def getG2(readLine):
    pros2 = readLine.strip().split('generate')[1]
    return pros2

def gethAList2(card):
    hAList2 = []
    s = getFile(card)
    for name in card:
        #s = getFile(name)
        try:
            with open(name) as f:
                for cards in f:
                    if cards.find('param_card') > 0 and cards.find('mass')>0 and cards.find('32') > 0:
                        s.mzp2 = float(getMZpValue2(cards))
                    elif cards.find('param_card') > 0 and cards.find('mass')>0 and cards.find('28') > 0:
                        s.ma02 = float(getMA0Value2(cards))
                    elif cards.find('lhaid') > 0:
                        s.lhaid2 = float(getLHAID2(cards))
                        break
                    elif cards.find('param_card') > 0 and cards.find('1') > 0 and cards.find('ZpINPUTS') > 0:
                        s.tanbeta2 = float(getTanBeta2(cards))
                    elif cards.find('param_card') > 0 and cards.find('2') > 0 and cards.find('ZpINPUTS') > 0:
                        s.gz2 = float(getgz2(cards))
                    elif cards.find('generate') == 0:
                        s.gener2 = getG2(cards)
                    #hAList2.append(s)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    hAList2.append(s)
    return hAList2


def main():
    hAList = gethAList(hA_files)
    hAList2 = gethAList2(hA_files2)
    textLine = []
    compare = [0,0,0,0,0,0,0]
    compare2 = [0,0,0,0,0,0,0]
    title=["file","mzp","ma0","LHAID","tanBeta","gz","process"]
    for a in hAList:
        compare[0] = "lhefile"
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
        if (int(compare[1])!=0 and int(compare[2])!=0 and int(compare[3])!=0 and int(compare[4])!=0 and compare[5]!=0 and compare[6]!=0):
            for b in hAList2:
                print(compare)
                print(b.mzp2, b.ma02, b.lhaid2, b.tanbeta2, b.gz2)
                print(b.gener2)
                
                if (int(b.mzp2)==int(compare[1]) and int(b.ma02)==int(compare[2]) and int(b.lhaid2)==int(compare[3]) and int(b.tanbeta2)==int(compare[4]) and b.gz2==compare[5] and b.gener2==compare[6]):
                    compare2 = ["cards", b.mzp2, b.ma02, b.lhaid2, b.tanbeta2, b.gz2, b.gener2]
                    print(123)
                    textLine.append(["true"])
                else :
                    print(456)
                    compare2 = ["cards", b.mzp2, b.ma02, b.lhaid2, b.tanbeta2, b.gz2, b.gener2]
                    textLine.append(["false"])

    with open("LHEcheckWr.txt", "w") as f:
        wr = csv.writer(f,delimiter="\t")
        wr.writerow(title)
        wr.writerow(compare)
        wr.writerow(compare2)
        wr.writerows(textLine)

if __name__ == "__main__":
    main()
