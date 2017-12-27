import SchedulerEmulator.Settings as Set
import time
import random
import copy

class ClassJobCreator():

    def MainJobCreator():

        print("\n\nMainJobCreator")
        #sampleJob # [s,[[e1],[e2],[e3]],d,b,id],
        #jobList = "~input/jobList.txt"
        #jobList = [[0, [[1, 2, 21], [2, 2, 11], [4, 2, 7]], 23, 15, 1],


        joblist=[]
        id=0
        for i in range(Set.NumberOfTimeInterval): # Creating Time intervals
            cap=copy.deepcopy(Set.load*Set.capacity)
            #print("timeinterval: ", i," cap: ",cap," load: ",Set.load," coreCount: ",Set.capacity)
            while(cap>0):  # Creating Each Time interval # for 80% how do you know which one ended ???
                id=id+1
                core = random.choice(Set.vmCores)
                vmConut = Set.switchCaseDic[core]#base VM core
                cap = cap - core*vmConut
                if cap<=0:
                    print("timeinterval: ", i," Cap Passed:",cap)
                    pass
                runTime = random.randint(1,Set.maxRunTime*Set.timeInterval)         # run time 1 to 1.5*10 [max*each]
                bid=core*runTime                                                    # bid is base core*runtime
                deadLine= random.uniform(Set.deadLineMin,Set.deadLineMin+1)*runTime # deadline 2-3 times of runtime
                maxOptions=Set.maxVMoptions
                options=[]
                minScale=Set.minScaleFactor
                maxScale=Set.maxScaleFactor

                while(core*vmConut<=Set.maxVMsize or maxOptions!=0):

                    options.append([vmConut,core,runTime]) # core but what to do with VM*Core ???

                    vmConut=vmConut*2
                    maxOptions=maxOptions-1

                    scaleFactor =random.uniform(minScale,maxScale)
                    runTime=runTime/scaleFactor
                    maxScale=scaleFactor

                joblist.append([i*Set.timeInterval,options,deadLine,bid,id])

        for item in joblist:
            print(item[4]," :",item)

        time.sleep(10*Set.sleepTime)
        return joblist