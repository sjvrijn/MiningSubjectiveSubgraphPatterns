###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################
import os
import sys
path = os.getcwd().split('MiningSubjectiveSubgraphPatterns')[0]+'MiningSubjectiveSubgraphPatterns/'
if path not in sys.path:
	sys.path.append(path)
import numpy as np
import math
import networkx as nx

from src.Utils.Measures import getCodeLength, getCodeLengthParallel, getDirectedSubgraph
from src.Utils.Measures import computeDescriptionLength, computeInterestingness
from src.Patterns.Pattern import Pattern
from src.HillClimbers.HC_v4 import findBestPattern, runNKseeds, runGivenSeeds, getSeeds

class EvaluateAdd:
    """
    This data structure shall contain all the possible addition candidates
    along with pattern number as key and other information as value
    """
    def __init__(self, gtype='U', isSimple=True, l=6, ic_mode=1, imode=2, minsize=2, seedType='interest', seedRuns=10, q=0.01, incEdges=False):
        """
        initialization function

        Parameters
        ----------
        gtype : str, optional
            Input Graph type, 'U': Undirected, 'D': Directed, by default 'U'
        isSimple : bool, optional
            if input graph is a simple graph then True else False if it is a multigraph, by default True
        l : int, optional
            Total number of unique action types that can be performed, by default 6
        icmode : int, optional
            Mode for information content--- 1: IC_ssg, 2: AD (aggregate deviation), 3: IC_dsimp, by default 1
        imode : int, optional
            Interestingness mode--- 1: fraction, 2: Difference, by default 2
        minsize : int, optional
            Minimum size of pattern, by default 2
        seedType : str, optional
            Type of seed run for the hill climber, it can be "all", "uniform", "degree" or "interest", by default "interest"
        seedRuns : int, optional
            Minimum size of pattern, by default 2
        q : float, optional
            Expected size of pattern, given as a factor of original size of the input graph, ranges 0.0-1.0, by default 0.01
        incEdges : bool, optional
            True in edges to be encoded for description length else false, by default false
        """
        self.Data = dict()
        self.seeds = list()
        self.gtype = gtype
        self.isSimple = isSimple
        self.l = l # possible types (give number) of action, default is 6
        self.imode = imode
        self.minsize = minsize
        self.q = q
        self.seedMode = seedType
        self.seedRuns = seedRuns
        self.incEdges = incEdges
        print('Initialized EvaluateAdd')

    def evaluateNew(self, G, PD):
        self.seeds = getSeeds(G, PD, self.q, self.seedMode, self.seedRuns, self.icmode, self.gtype, self.isSimple, self.incEdges)
        self.Data = runGivenSeeds(G, PD, self.q, self.nodes, self.icmode, self.gtype, self.isSimple, self.incEdges)
        return

    def checkAndUpdateAllPossibilities(self, G, PD, PrevPat):
        #First if the last action is add then we are required to find a new pattern again, that is, running a hill climber for top-k seeds fresh.
        if len(self.Data) < 1:
            self.evaluateNew(G, PD)
        else:
            #second if there is an overlap of nodes affected (to specific a node-pair) then we find a new pattern and run the hill climber for top-k seeds fresh.
            bestPattern = max(self.Data, key=lambda x: x.I)
            if self.gtype == 'U':
                if len(set(bestPattern.NL).intersection(set(PrevPat.NL))) > 1:
                    self.evaluateNew(G, PD)
            else:
                inInt = len(set(bestPattern.inNL).intersection(set(PrevPat.inNL)))
                outInt = len(set(bestPattern.outNL).intersection(set(PrevPat.outNL)))
                if inInt > 1 and outInt > 1:
                    self.evaluateNew(G, PD)
        return

    def getBestOption(self, G, PD):
        if len(self.Data) > 0:
            bestPattern = max(self.Data, key=lambda x: x.I)
            codeLengthC = None
            codeLengthCprime = None
            DL = None
            dlmode = 3
            if self.gtype == 'U':
                nlambda = PD.updateDistribution(bestPattern.G, None, 'return', 2, None)
                codeLengthC = getCodeLengthParallel(G, PD, NL=bestPattern.NL, case=2, gtype=self.gtype, isSimple=self.isSimple)
                codeLengthCprime = getCodeLengthParallel(G, PD, NL=bestPattern.NL, case=2, gtype=self.gtype, isSimple=self.isSimple, nlambda=nlambda)
                DL = computeDescriptionLength(dlmode=dlmode, V=G.number_of_nodes(), W=bestPattern.NCount, kw=bestPattern.ECount, q=self.q, isSimple=self.isSimple, kws=bestPattern.kws, excActionType=False, l=self.l)
            else:
                nlambda = PD.updateDistribution(bestPattern.G, None, 'return', 2, None)
                codeLengthC = getCodeLengthParallel(G, PD, NL=bestPattern.NL, case=2, gtype=self.gtype, isSimple=self.isSimple)
                codeLengthCprime = getCodeLengthParallel(G, PD, inNL=bestPattern.inNL, outNL=bestPattern.outNL, case=2, gtype=self.gtype, isSimple=self.isSimple, nlambda=nlambda)
                DL = computeDescriptionLength(dlmode=dlmode, V=G.number_of_nodes(), WI=bestPattern.inNL, WO=bestPattern.outNL, kw=bestPattern.ECount, q=self.q, isSimple=self.isSimple, kws=bestPattern.kws, excActionType=False, l=self.l)
            IC_dssg = codeLengthC - codeLengthCprime
            bestPattern.setIC_dssg(IC_dssg)
            bestPattern.setDL(DL)
            bestPattern.setI( computeInterestingness(bestPattern.IC_dssg, bestPattern.DL, mode=self.imode) )
            bestPattern.setPatType('add')
            Params = dict()
            Params['Pat'] = bestPattern
            Params['codeLengthC'] = codeLengthC
            Params['codeLengthCprime'] = codeLengthCprime
            return Params
        else:
            return None

    def updateDistribution(self, PD, bestA):
        """
        function to update background distribution.
        * Now here we add a new lambda for the added pattern.

        Parameters
        ----------
        PD : PDClass
            Background distribution
        bestA : Pattern
            last added pattern
        """
        self.Data = []
        self.seeds = []
        PD.updateDistribution( bestA['Pat'].G, idx=bestA.cur_order, val_retrun='save', case=2 )
        return