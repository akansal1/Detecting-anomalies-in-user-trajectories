'''
Created on Nov 23, 2016

@author: zahran
'''
from MyEnums import *
import sys

class HypTesting:    
    def __init__(self, alpha, testsetCountAdjust, testsetCount):
        self.sigLevel = alpha
        self.testsetCountAdjust = testsetCountAdjust
        self.testsetCount = testsetCount
        self.type = None
    def adjustSigLevel(self):
        pass
    def classify(self, keySortedPvalues, pValues):
        pass


class Bonferroni(HypTesting):
    def __init__(self, alpha, testsetCountAdjust, testsetCount):
        HypTesting.__init__(self, alpha, testsetCountAdjust, testsetCount)
        self.adjustedSigLevel = None
        self.type = HYP.BONFERRONI
        
    def adjustSigLevel(self, actionsCount):        
        self.adjustedSigLevel = float(self.sigLevel) / float(actionsCount)
        if(self.testsetCountAdjust):
            self.adjustedSigLevel = self.adjustedSigLevel / float(self.testsetCount)
    
    def classify(self, keySortedPvalues, pValues):
        if(self.adjustedSigLevel == None):
            self.adjustSigLevel(len(keySortedPvalues))
        
        outlierVector = [DECISION.UNDECIDED]*len(keySortedPvalues)
        
        for i in range(len(keySortedPvalues)):
            if(pValues[keySortedPvalues[i]] <= self.adjustedSigLevel):
                outlierVector[keySortedPvalues[i]] = DECISION.OUTLIER# rejecting H0 (i.e rejecting that the action is normal ==> outlier)
            else:
                outlierVector[keySortedPvalues[i]] = DECISION.NORMAL
        return outlierVector
    
    
class Holms(HypTesting):
    def __init__(self, alpha, testsetCountAdjust, testsetCount):
        HypTesting.__init__(self, alpha, testsetCountAdjust, testsetCount)
        self.adjustedSigLevel = None
        self.type = HYP.HOLMS
    
    def adjustSigLevel(self, actionsCount, currentAction): 
        if(self.testsetCountAdjust == True):
            self.adjustedSigLevel = float(self.sigLevel)/float(((actionsCount*self.testsetCount)-currentAction))
        else:            
            self.adjustedSigLevel = float(self.sigLevel)/float((actionsCount-currentAction))  
        
    def classify(self, keySortedPvalues, pValues):
        outlierVector = [DECISION.UNDECIDED]*len(keySortedPvalues)
        k = sys.maxint
        for i in range(len(keySortedPvalues)):
            self.adjustSigLevel(len(keySortedPvalues), i)            
            if(pValues[keySortedPvalues[i]] > self.adjustedSigLevel):
                k = i
                break
        
        for i in range(len(keySortedPvalues)):
            if(i<k):
                outlierVector[keySortedPvalues[i]] = DECISION.OUTLIER
            else:
                outlierVector[keySortedPvalues[i]] = DECISION.NORMAL
        return outlierVector
            
        
            
    
        
        