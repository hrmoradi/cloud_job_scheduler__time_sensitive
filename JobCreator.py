import SchedulerEmulator.Settings as Set
import time
import random
import copy

class ClassJobCreator:

    def MainJobCreator(self):

        print("MainJobCreator")
        time.sleep(Set.sleepTime)
        #sampleJob # [s,[[e1],[e2],[e3]],d,b,id],
        #jobList = "~input/jobList.txt"
        #jobList = [[0, [[1, 2, 21], [2, 2, 11], [4, 2, 7]], 23, 15, 1],


        joblist=[]
        id=0
        for i in range(Set.NumberOfTimeInterval): # Creating Time intervals
            if (i%2==0):
                cap = float(Set.loadMin) * float(Set.capacity)
            else:
                cap=cap = float(Set.loadMax) * float(Set.capacity)
            if Set.debugTimer:
                print("interval", i, " cap:", cap)
            time.sleep(Set.sleepTime)

            #print("timeinterval: ", i," cap: ",cap," load: ",Set.load," coreCount: ",Set.capacity)

            core = random.choice(Set.vmCores)
            vmConut = Set.switchCaseDic[core]  # base VM core
            cap = cap - core * vmConut
            #print("     core: ",core," vmCount: ",vmConut," cap: ",cap)
            while(cap>=0):  # Creating Each Time interval # for 80% how do you know which one ended ???
                id=id+1
                if Set.debug:
                    print("     id",id)#," cap: ",cap)
                if Set.debug:
                    print("     core: ", core, " vmCount: ", vmConut, " cap: ", cap)
                time.sleep(Set.sleepTime)



                #print(i,cap)
                #print("timeinterval: ", i, " Cap:", cap)
                #if cap<=0:
                 #   print("timeinterval: ", i," Cap Passed:",cap)
                  #  pass
                runTime = random.randint(1, Set.maxRunTime * Set.eachTimeInterval)         # run time 1 to 1.5*10 [max*each]
                bid=core*runTime                                                    # bid is base core*runtime
                deadLine= random.uniform(Set.deadLineMin,Set.deadLineMin+1)*runTime # deadline 2-3 times of runtime
                maxOptions=int(Set.maxVMoptions)
                options=[]
                minScale=Set.minScaleFactor
                maxScale=Set.maxScaleFactor
                option=1
                while(maxOptions>0):

                    options.append([vmConut,core,runTime]) # core but what to do with VM*Core ???
                    if Set.debug:
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

        time.sleep(10*Set.sleepTime)
        return joblist