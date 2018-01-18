import SchedulerEmulator.Settings as Set
import time
import random
import copy
import math
import numpy as np



class ClassJobCreator:

    def MainJobCreator(self):
        if Set.randJob:
            print("MainJobCreator - Random Job")
        if Set.tableJob:
            print("MainJobCreator - Table Job")

        time.sleep(Set.sleepTime)
        #sampleJob # [s,[[e1],[e2],[e3]],d,b,id],

        joblist=[]
        id=0
        capSum=0
        head=0
        numVM=0
        numCore=1
        execTime=2
        mem=3


        """ for each interval """
        for i in range(Set.NumberOfTimeInterval): # Creating Time intervals
            randomCapScale=0
            if i%6==0:
                randomCapScale= random.uniform(Set.avgSysLoad+(Set.fluctuation*0.75),Set.avgSysLoad+Set.fluctuation)
            elif i%6==1:
                randomCapScale = random.uniform(Set.avgSysLoad + (Set.fluctuation * 0.75),Set.avgSysLoad + Set.fluctuation)
            elif i%6==2:
                randomCapScale = random.uniform(Set.avgSysLoad + (Set.fluctuation * 0.75),Set.avgSysLoad + Set.fluctuation)
            elif i%6==3:
                randomCapScale = random.uniform(Set.avgSysLoad-Set.fluctuation,Set.avgSysLoad-(Set.fluctuation*0.75))
            elif i%6==4:
                randomCapScale = random.uniform(Set.avgSysLoad-Set.fluctuation,Set.avgSysLoad-(Set.fluctuation*0.75))
            elif i%6==5:
                randomCapScale = random.uniform(Set.avgSysLoad-Set.fluctuation,Set.avgSysLoad-(Set.fluctuation*0.75))
            #elif i%3==2:
            #    randomCapScale=random.uniform(
            #randomCapScale = random.uniform(Set.avgSysLoad - Set.fluctuation, Set.avgSysLoad + Set.fluctuation)
            cap = float(randomCapScale*Set.eachTimeInterval*Set.capacity)
            capMem= float(randomCapScale*Set.eachTimeInterval*Set.capMem) # testing setting cap for mem)
            capSum= capSum+cap



            if Set.debug:
                print("interval", i, " cap:", cap," capMEM:",capMem)
                # print("timeinterval: ", i," cap: ",cap," load: ",Set.load," coreCount: ",Set.capacity)
                time.sleep(Set.sleepTime)



            """ Create job based on table """

            if Set.tableJob:
                options=[]
                app = random.choice(["bt","cg","ep","is","lu","mg","sp","ua"])
                if app != "is":
                    generateExec = ClassJobCreator.table1(app) #1
                    options.append(generateExec)
                generateExec = ClassJobCreator.table2(app) #2
                options.append(generateExec)
                generateExec = ClassJobCreator.table3(app) #3
                options.append(generateExec)
                generateExec = ClassJobCreator.table4(app) #4
                options.append(generateExec)
                #options.sort(key=lambda x: x[2],reverse=True) # not sorting for now
                if Set.debugLevel2:
                    print("options",options)

                core = options[head][numCore]
                vmConut= options[head][numVM]
                runTime=options[head][execTime]
                vmMem=options[head][mem]
                if cap > 0 and capMem > 0:
                    if (cap < (core * vmConut * runTime)or capMem < (vmMem * vmConut * runTime)):
                        #print("exceed", cap, " ", capMem, "area:", core * vmConut * runTime, "run", runTime) ###############
                        if ((core * vmConut * runTime) / cap > (vmMem * vmConut * runTime) / capMem):
                            keepLoad = (cap / float(core * vmConut * runTime))
                            runTime = runTime * keepLoad
                            for item in options:
                                item[execTime]=item[execTime]* keepLoad
                            #print("****cap exceed", cap, "area:", core * vmConut * runTime, "run", runTime) #################
                        else:
                            keepLoad = (capMem / float(vmMem * vmConut * runTime))
                            runTime = runTime * keepLoad
                            for item in options:
                                options[head][execTime]=options[head][execTime]* keepLoad
                            #print("****mem exceed", capMem, "area:", core * vmConut * runTime, "run", runTime) #######
                cap = math.floor(cap - (core * vmConut * runTime))
                capMem = math.floor(capMem - (vmMem * vmConut * runTime))
                #print("interval", i, " cap:", cap, " capMEM:", capMem)
                while (cap >= -1 and capMem >=-1):  # Creating Each Time interval # for 80% how do you know which one ended ??? ###### tweek reduce load >=
                    id = id + 1
                    if Set.debugLevel2:
                        print("     id", id)  # ," cap: ",cap)
                    if Set.debugLevel2:
                        print("     core: ", core, " vmCount: ", vmConut, " cap: ", cap)
                    time.sleep(Set.sleepTime)

                    bid = ClassJobCreator.realBid(core, vmConut) * (runTime) * vmConut  # =====================# bid is base core*runtime
                    deadLine = random.uniform(Set.deadLineMin,Set.deadLineMax) * runTime  # deadline 2-4 times of runtime
                    joblist.append([i * Set.eachTimeInterval, options, deadLine, bid, id])
                    #print("interval", i, " cap:", cap, " capMEM:", capMem) ##########
                    #print(joblist[-1]) ##########

                    """ next job gen """
                    options = []
                    app = random.choice(["bt", "cg", "ep", "is", "lu", "mg", "sp", "ua"])
                    #print(app)
                    if app != "is":
                        generateExec = ClassJobCreator.table1(app)  # 1
                        options.append(generateExec)
                    generateExec = ClassJobCreator.table2(app)  # 2
                    options.append(generateExec)
                    generateExec = ClassJobCreator.table3(app)  # 3
                    options.append(generateExec)
                    generateExec = ClassJobCreator.table4(app)  # 4
                    options.append(generateExec)
                    #options.sort(key=lambda x: x[2], reverse=True) # no sorting for now
                    #print("options", options)

                    core = options[head][numCore]
                    vmConut = options[head][numVM]
                    runTime = options[head][execTime]
                    vmMem= options[head][mem]
                    if cap > 0 and capMem > 0:
                        if (cap < (core * vmConut * runTime) or capMem < (vmMem * vmConut * runTime)):
                            #print("exceed", cap, " ", capMem, "area:", core * vmConut * runTime, "run", runTime)
                            if ((core * vmConut * runTime) / cap > (vmMem * vmConut * runTime) / capMem):
                                keepLoad = (cap / float(core * vmConut * runTime))
                                runTime = runTime * keepLoad
                                for item in options:
                                    item[execTime] = item[execTime] * keepLoad
                                #print("***i*cap exceed", cap, "area:", core * vmConut * runTime, "run", runTime)
                            else:
                                keepLoad = (capMem / float(vmMem * vmConut * runTime))
                                runTime = runTime * keepLoad
                                for item in options:
                                    options[head][execTime] = options[head][execTime] * keepLoad
                                #print("****mem exceed", capMem, "area:", core * vmConut * runTime, "run", runTime)
                    cap = math.floor(cap - (core * vmConut * runTime))
                    capMem = math.floor(capMem - (vmMem * vmConut * runTime))
                    #print("interval", i, " cap:", cap, " capMEM:", capMem)

            """ creating random job """

            if Set.randJob:
                core = random.choice([4,8,16]) #=====================================================
                vmConut = ClassJobCreator.vmCountDic(core)  # base VM core
                runTime = random.uniform(Set.minRuntime,Set.maxRunTime)
                memRatio= random.choice([2,4])  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                vmMem= core*memRatio
                if cap > 0 and capMem>0:
                    if (cap < (core * vmConut * runTime) or capMem < (vmMem * vmConut * runTime)):
                        #print("exceed", cap, " ", capMem, "area:", core * vmConut * runTime, "run", runTime)
                        if ((core * vmConut * runTime) / cap > (vmMem * vmConut * runTime) / capMem):
                            keepLoad = (cap / float(core * vmConut * runTime))
                            runTime = runTime * keepLoad
                            #print("****cap exceed", cap, "area:", core * vmConut * runTime, "run", runTime)
                        else:
                            keepLoad = (capMem / float(vmMem * vmConut * runTime))
                            runTime = runTime * keepLoad
                            #print("****mem exceed", capMem, "area:", core * vmConut * runTime, "run", runTime)
                cap = math.floor(cap - (core * vmConut * runTime))
                capMem = math.floor(capMem - (vmMem * vmConut * runTime))
                #print("interval", i, " cap:", cap, " capMEM:", capMem)
                #print("     core: ",core," vmCount: ",vmConut," mem:",vmMem," cap: ",cap)
                while(cap>=-1 and capMem>=-1):  # Creating Each Time interval # for 80% how do you know which one ended ??? ###### tweek reduce load >=
                    id=id+1
                    #print("     core: ", core, " vmCount: ", vmConut, " mem:", vmMem, " cap: ", cap," id:",id)
                    if Set.debugLevel2:
                        print("     id",id)#," cap: ",cap)
                    if Set.debugLevel2:
                        print("     core: ", core, " vmCount: ", vmConut, " cap: ", cap)
                    time.sleep(Set.sleepTime)

                    bid=ClassJobCreator.realBid(core,vmConut)*(runTime)*vmConut#=====================# bid is base core*runtime
                    deadLine= random.uniform(Set.deadLineMin,Set.deadLineMax)*runTime # deadline 2-4 times of runtime
                    maxOptions=int(Set.maxVMoptions)
                    #print(maxOptions)
                    options=[]
                    minScale=Set.minScaleFactor
                    option=1
                    while(maxOptions>0):

                        maxScale = 1/float(vmConut*core)
                        options.append([vmConut,core,runTime,core*memRatio]) # core but what to do with VM*Core ???
                        if Set.debugDetail:
                            print("          option num",option)
                        option=option+1
                        time.sleep(Set.sleepTime)
                        if vmConut==1:
                            vmConut=2
                        else:
                            vmConut=(vmConut+2)
                        maxOptions=maxOptions-1

                        maxScale = maxScale*(vmConut*core)
                        scaleFactor =random.uniform(minScale,maxScale)
                        runTime=runTime/scaleFactor


                    joblist.append([i * Set.eachTimeInterval, options, deadLine, bid, id])
                    #print(joblist[-1])
                    core = random.choice([4,8,16])
                    vmConut = ClassJobCreator.vmCountDic(core)  # base VM core
                    runTime = random.uniform(Set.minRuntime, Set.maxRunTime)  # =================================#randint(1, Set.maxRunTime * Set.eachTimeInterval)         # run time 1 to 1.5*10 [max*each]
                    memRatio = random.choice([2,4])  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    vmMem = core * memRatio
                    if cap > 0 and capMem > 0:
                        if (cap < (core * vmConut * runTime) or capMem < (vmMem * vmConut * runTime)):
                            #print("exceed", cap, " ", capMem, "area:", core * vmConut * runTime, "run", runTime)
                            if ((core * vmConut * runTime) / cap > (vmMem * vmConut * runTime) / capMem):
                                keepLoad = (cap / float(core * vmConut * runTime))
                                runTime = runTime * keepLoad
                                #print("****cap exceed", cap, "area:", core * vmConut * runTime, "run", runTime)
                            else:
                                keepLoad = (capMem / float(vmMem * vmConut * runTime))
                                runTime = runTime * keepLoad
                                #print("****mem exceed", capMem, "area:", core * vmConut * runTime, "run", runTime)
                    cap = math.floor(cap - (core * vmConut * runTime))
                    capMem = math.floor(capMem - (vmMem * vmConut * runTime))
                    #print("interval", i, " cap:", cap, " capMEM:", capMem)

        for item in joblist[0:4]:
            if Set.fx:
                print(item[4]," :",item)
        print("number of jobs Created:",len(joblist))

        print("random Cap avg: ", 100 * (capSum / float(Set.capMem * Set.duration)))

        sumLoad = 0
        for item in joblist:
            sumLoad = sumLoad + (item[1][0][3] * item[1][0][0] * item[1][0][2])
        print("avg load 1st execs area MEM: ", 100 * (sumLoad / float(Set.capMem  * Set.duration)))

        sumLoad = 0
        sumTime = 0
        for item in joblist:
            sumLoad = sumLoad + (item[1][0][1] * item[1][0][0] * item[1][0][2])
            sumTime = sumTime + item[1][0][2]
        print("avg load 1st execs area cPU: ", 100*(sumLoad / float(Set.capacity*Set.duration)))
        print("avg Time 1st exec: ",( sumTime / float(len(joblist))))
        sumLoad = 0
        sumTime = 0
        for item in joblist:
            sumLoad = sumLoad + (item[1][1][1] * item[1][1][0] * item[1][1][2])
            sumTime = sumTime + item[1][1][2]
        print("avg load 2nd execs CPU: ",100*(sumLoad / float(Set.capacity*Set.duration)))
        print("avg Time 2nd exec: ",( sumTime / float(len(joblist))))
        sumLoad = 0
        sumTime = 0
        #for item in joblist:
        #    sumLoad = sumLoad + (item[1][2][1] * item[1][2][0] * item[1][2][2])
        #    sumTime = sumTime + item[1][2][2]
        #print("avg load 3rd execs: ", (sumLoad / float(Set.capacity * Set.duration)))
        #print("avg Time 3rd exec: ", (sumTime / float(len(joblist))))
        #print("avg Cap: ", capSum/Set.NumberOfTimeInterval)

        #print(np.average([48,21,87,83,43,60,30,89,106,56,60,30,85,102,51,61,85,96,51,85,29,8,47,75,79,27,45,66,29,69,25,44,56,82,34,50,67,98,15,88,111,67,97,58,15,98,99,78,15,73,29,49,63,57,34,44,51,74,28,43,60,75,33,53,65]))

        time.sleep(5*Set.sleepTime)
        return joblist


    """ bid function """#  TO DO : make it accurate by mem !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def realBid(core,vmCount):
        if Set.randJob:
            if core == 2:
                return 0.15
            if core ==  4:
                return 0.25
            if core ==  8:
                return 0.45
            if core== 16:
                return 0.85
        if Set.tableJob:
            if core == 2:
                return 0.15
            if core == 4:
                return (vmCount * random.choice([0.25, 0.32, 0.25]))
            if core == 8:
                return (vmCount * random.choice([0.45, 0.58, 0.45]))
            if core == 16:
                return (vmCount * 0.85)
        return()



    """ tableJob """  # [#vm,#core,time,mem]

    def table1(app): #########################################################  1vm 4 core diff mem
        table = {"bt": random.choice([[1, 4, 98.37, 16], [1, 4, 97.12, 30.5]]),
                  "cg": random.choice([[1, 4, 58.01, 30.5]]),
                  "ep": random.choice([[1, 4, 15.38, 16], [1, 4, 15.44, 30.5], [1, 4, 15.50, 7.5]]),
                  "is": random.choice([[]]),  # is is not running on single 4 core
                  "lu": random.choice([[1, 4, 88.79, 16], [1, 4, 98.65, 30.5]]),
                  "mg": random.choice([[1, 4, 8.08, 30.5]]),
                  "sp": random.choice([[1, 4, 111.37, 16], [1, 4, 99.34, 30.5]]),
                  "ua": random.choice([[1, 4, 67.38, 16], [1, 4, 78.83, 30.5]])
                  }
        return (table[app])

    def table2(app): #########################################################  1vm 8 core diff mem
        table = {"bt": random.choice([[1, 8, 60.5, 32], [1, 8, 60.55, 61]]),
                  "cg": random.choice([[1, 8, 30.94, 32], [1, 8, 30.39, 61]]),
                  "ep": random.choice([[1, 8, 8.31, 32], [1, 8, 8.27, 61], [1, 8, 8.28, 15]]),
                  "is": random.choice([[1, 8, 1.35, 61]]),
                  "lu": random.choice([[1, 8, 89.24, 32], [1, 8, 85.19, 61], [1, 8, 85.89, 15]]),
                  "mg": random.choice([[1, 8, 6.54, 32], [1, 8, 6.12, 61]]),
                  "sp": random.choice([[1, 8, 106.06, 32], [1, 8, 102.62, 61], [1, 8, 96.50, 15]]),
                  "ua": random.choice([[1, 8, 56.79, 32], [1, 8, 51.43, 61], [1, 8, 51.37, 15]])
                  }
        return (table[app])
    """
    def table3(app): #########################################################  mixed old table 3
        table = {"bt": random.choice(
            [[1, 16, 48.55, 64], [4, 4, 73.75, 16], [2, 8, 85.14, 61], [8, 2, 69.61, 3.75], [4, 4, 74.29, 7.5]]),
                  "cg": random.choice(
                      [[1, 16, 21.72, 64], [4, 4, 29.76, 16], [2, 8, 29.22, 61], [8, 2, 25.45, 3.75], [4, 4, 28.47, 7.5]]),
                  "ep": random.choice(
                      [[1, 16, 4.97, 64], [4, 4, 8.07, 16], [2, 8, 8.05, 61], [8, 2, 7.51, 3.75], [4, 4, 7.48, 7.5]]),
                  "is": random.choice([[1, 16, 0.83, 64]]),
                  "lu": random.choice(
                      [[1, 16, 87.09, 64], [4, 4, 49.67, 16], [2, 8, 47.75, 61], [8, 2, 44.14, 3.75], [4, 4, 43.11, 7.5]]),
                  "mg": random.choice(
                      [[1, 16, 5.74, 64], [4, 4, 5.29, 16], [2, 8, 5.55, 61], [8, 2, 5.06, 3.75], [4, 4, 4.79, 7.5]]),
                  "sp": random.choice(
                      [[1, 16, 83.98, 64], [4, 4, 63.86, 16], [2, 8, 75.13, 61], [8, 2, 56.48, 3.75], [4, 4, 60.39, 7.5]]),
                  "ua": random.choice([[1, 16, 43.32, 64]])
                  }
        return (table[app])
    """


    def table3(app): #########################################################  diff VM 16 core 32 mem
        table = {"bt": random.choice(
            [   [8, 2, 69.61, 3.75], [4, 4, 74.29, 7.5]]),
            "cg": random.choice(
                [  [8, 2, 25.45, 3.75], [4, 4, 28.47, 7.5]]),
            "ep": random.choice(
                [  [8, 2, 7.51, 3.75], [4, 4, 7.48, 7.5]]),
            "is": random.choice([[1, 16, 0.83, 64]]),
            "lu": random.choice(
                [  [8, 2, 44.14, 3.75], [4, 4, 43.11, 7.5]]),
            "mg": random.choice(
                [ [8, 2, 5.06, 3.75], [4, 4, 4.79, 7.5]]),
            "sp": random.choice(
                [   [8, 2, 56.48, 3.75], [4, 4, 60.39, 7.5]]),
            "ua": random.choice([[1, 16, 43.32, 64]])
        }
        return (table[app])

    def table4(app): #########################################################  diff VM  16 core 64,128 mem
        table = {"bt": random.choice(
            [[4, 4, 73.75, 16],[1, 16, 48.55, 64],  [2, 8, 85.14, 61]]),
                  "cg": random.choice(
                      [[4, 4, 29.76, 16],[1, 16, 21.72, 64], [2, 8, 29.22, 61]]),
                  "ep": random.choice(
                      [[4, 4, 8.07, 16],[1, 16, 4.97, 64], [2, 8, 8.05, 61]]),
                  "is": random.choice([[1, 16, 0.83, 64]]),
                  "lu": random.choice(
                      [[4, 4, 49.67, 16],[1, 16, 87.09, 64], [2, 8, 47.75, 61], ]),
                  "mg": random.choice(
                      [[4, 4, 5.29, 16],[1, 16, 5.74, 64], [2, 8, 5.55, 61]]),
                  "sp": random.choice(
                      [[4, 4, 63.86, 16],[1, 16, 83.98, 64], [2, 8, 75.13, 61], ]),
                  "ua": random.choice([[1, 16, 43.32, 64]])
                  }
        return (table[app])

    def vmCountDic(core):
        switchCaseDic = {2: random.randint(1, 2), 4: random.randint(1, 2), 8: 1, 16: 1, }
        return (switchCaseDic[core])