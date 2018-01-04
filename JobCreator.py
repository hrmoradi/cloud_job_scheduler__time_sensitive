import SchedulerEmulator.Settings as Set
import time
import random
import copy
import math
import numpy as np

class ClassJobCreator:

    def MainJobCreator(self):

        print("MainJobCreator")
        time.sleep(Set.sleepTime)
        #sampleJob # [s,[[e1],[e2],[e3]],d,b,id],

        joblist=[]
        id=0
        for i in range(Set.NumberOfTimeInterval): # Creating Time intervals

            if (i%2==0):# or i%10==7  ): # ====================================================================
                cap = float(Set.loadMin) * float(Set.capacity)
            elif (i%2==1 ):
                cap= float(Set.loadMax) * float(Set.capacity)
            elif True:
                cap=0
            """
            cap = Set.avgSysLoad* float(Set.capacity)*(Set.loadMin) + int(math.floor(math.cos(i*90) *(Set.loadMax)* float(Set.capacity))) #Rihanna
            """


            if Set.debugTimer:
                print("interval", i, " cap:", cap)
                # print("timeinterval: ", i," cap: ",cap," load: ",Set.load," coreCount: ",Set.capacity)
            time.sleep(Set.sleepTime)

            core = random.choice(Set.vmCores) #=====================================================
            vmConut = Set.switchCaseDic[core]  # base VM core
            cap = cap - core * vmConut
            #print("     core: ",core," vmCount: ",vmConut," cap: ",cap)
            while(cap>=0):  # Creating Each Time interval # for 80% how do you know which one ended ??? ###### tweek reduce load >=
                id=id+1
                if Set.debugLevel2:
                    print("     id",id)#," cap: ",cap)
                if Set.debugLevel2:
                    print("     core: ", core, " vmCount: ", vmConut, " cap: ", cap)
                time.sleep(Set.sleepTime)

                runTime = ClassJobCreator.realRuntime(core,vmConut)#=================================#randint(1, Set.maxRunTime * Set.eachTimeInterval)         # run time 1 to 1.5*10 [max*each]
                bid=ClassJobCreator.realBid(core,vmConut)*(runTime)*vmConut#=====================# bid is base core*runtime
                deadLine= random.uniform(Set.deadLineMin,Set.deadLineMax)*runTime # deadline 2-4 times of runtime
                maxOptions=int(Set.maxVMoptions)
                #print(maxOptions)
                options=[]
                minScale=Set.minScaleFactor
                maxScale=Set.maxScaleFactor
                option=1
                while(maxOptions>0):

                    options.append([vmConut,core,runTime]) # core but what to do with VM*Core ???
                    if Set.debugDetail:
                        print("          option num",option)
                    option=option+1
                    time.sleep(Set.sleepTime)
                    if vmConut==1:
                        vmConut=2
                    else:
                        vmConut=(vmConut+2)
                    maxOptions=maxOptions-1

                    scaleFactor =random.uniform(minScale,maxScale)
                    runTime=runTime/scaleFactor
                    maxScale=scaleFactor

                joblist.append([i * Set.eachTimeInterval, options, deadLine, bid, id])

                core = random.choice(Set.vmCores)
                vmConut = Set.switchCaseDic[core]  # base VM core
                cap = cap - core * vmConut

        for item in joblist:
            if Set.debug:
                print(item[4]," :",item)
        print("number of jobs Created:",len(joblist))

        sumLoad = 0
        sumTime = 0
        for item in joblist:
            sumLoad = sumLoad + (item[1][0][1] * item[1][0][0] * item[1][0][2])
            sumTime = sumTime + item[1][0][2]
        print("avg load 1st execs: ", (sumLoad / float(Set.capacity*Set.duration)))
        print("avg Time 1st exec: ",( sumTime / float(len(joblist))))
        sumLoad = 0
        sumTime = 0
        for item in joblist:
            sumLoad = sumLoad + (item[1][1][1] * item[1][1][0] * item[1][1][2])
            sumTime = sumTime + item[1][1][2]
        print("avg load 2nd execs: ",( sumLoad / float(Set.capacity * Set.duration)))
        print("avg Time 2nd exec: ",( sumTime / float(len(joblist))))

        #print(np.average([48,21,87,83,43,60,30,89,106,56,60,30,85,102,51,61,85,96,51,85,29,8,47,75,79,27,45,66,29,69,25,44,56,82,34,50,67,98,15,88,111,67,97,58,15,98,99,78,15,73,29,49,63,57,34,44,51,74,28,43,60,75,33,53,65]))

        time.sleep(10*Set.sleepTime)
        return joblist

    def realRuntime(core,vmCount):
        if core == 2:
            return (random.choice([29,69,25,44,56,82,34,50,67,7,5,8,6]))#/vmCount)
        if core ==  4:
            return (random.choice([15,67,58,15,78,15,73,29,49,63,57,34,44,51,28,43,33,53,65,8,5,6,4,4,7,7,74,75,60,98,98,11,97]))#/vmCount)#xlarge
        if core ==  8:
            return (random.choice([60,30,89,56,60,30,85,51,61,96,51,29,8,47,75,79,27,45,66,8,8,8,5,6,6,7,5,102,106,96,85]))#/vmCount)#2xlarge
        if core== 16:
            return (random.choice([48,21,87,83,434,1,5]))#/vmCount) #4xlarge
        return()

    def realBid(core,vmCount):
        if core == 2:
            return 0.15
        if core ==  4:
            return (vmCount*random.choice([0.25,0.32,0.25]))
        if core ==  8:
            return (vmCount*random.choice([0.45,0.58,0.45]))
        if core== 16:
            return (vmCount*0.85)
        return()