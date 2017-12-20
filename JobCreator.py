import SchedulerEmulator.Settings as Set

import random


joblist=[]
for i in range(Set.NumberOfTimeInterval): # Creating Time intervals
    cap=Set.load*Set.capacity
    print("cap: ",cap)
    while(cap>=0):                    # Creating Each Time interval # for 80% how do you know which one ended ???
        core = random.choice(Set.vmCores)
        cap = cap - core
        runTime = random.randint(1,Set.maxRunTime*Set.timeInterval)
        bid=core*runTime
        deadLine= random.uniform(Set.deadLineMin,Set.deadLineMin+1)*runTime
        maxOptions=Set.maxVMoptions
        options=[]
        minScale=Set.minScaleFactor
        maxScale=Set.maxScaleFactor
        while(core<=Set.maxVMsize or maxOptions!=0):
            options.append([core,runTime]) # core but what to do with VM*Core ???

            core=core*2
            maxOptions=maxOptions-1

            scaleFactor =random.uniform(minScale,maxScale)
            runTime=runTime/scaleFactor
            maxScale=scaleFactor
        joblist.append([i*Set.timeInterval,options,deadLine,bid])


