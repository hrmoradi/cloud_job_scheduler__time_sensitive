import SchedulerEmulator.Settings as Set

import time
import copy

class ClassSchduler:

    def MainScheduler(self,jobList ):
        self.jobList=jobList
        print("\nMainScheduler")
        #print(len(Set.jobList))



        """
        defining required constants and variables
        """
        self.unUsedArea=0
        self.arrivalQueue = []
        self.jobsFailed=[]
        self.jobsAddressed=[]
        self.jobsScaled=[]

        self.timeStamp = 0
        self.nextJobArrival =0

        self.numVM=0
        self.VMcore=1
        self.rCore=0
        self.rMem=1

        self.head=0
        self.arrival=0
        self.execs=1
        self.runtime =2
        self.deadline=2
        self.bid=3
        self.id = 4

        self.collectedBid=0

        self.pools = {}
        for res in Set.resources:
            self.pools[res[self.id]]=[]



        """
        Simulation Starts
        """

        for du in range(Set.duration):                    # for specified time
            if Set.debugTimer:
                print("Current timeStamp: ",self.timeStamp)#," duration:",du)
            if Set.debugLevel1:
                print(" resources: ", Set.resources)


            """ reducing processing time & removing "finished" jobs *OOP: given pools dic, """

            for key in self.pools.keys():                 # for each pool ( each resource) # key is ID of resource
                self.thisPool=self.pools.get(key)
                self.shouldBeRemoved = []                 # creating array of jobs which should be removed for each pool (each resource)
                for job in self.thisPool:
                    #reserved.append([waiting[execs][head][VMcore],waiting[execs][head][runtime],waiting[bid],waiting[id]])
                    if Set.debugDetail:
                        print("b processtime",job)
                    job[1]=job[1]-1                  # reducing processing time
                    #print("a processtime",job)
                    if job[1]<=0:                    # if job finished
                        if Set.debugLevel1:
                            print("                         a VM will be removed from pool",key," job done with ID", job[3])
                        for res in Set.resources:    # returning used resource to pool
                            if res[self.id]==key:
                                res[self.rCore]=res[self.rCore]+job[0]
                        self.shouldBeRemoved.append(job)  # collect jobs that SHOULD BE  removed
                for job in self.shouldBeRemoved:
                    self.thisPool.remove(job)             # remove collected jobs

            if Set.debug:
                print(" resources: ", Set.resources)




            """adding "new jobs" to arrivalQueue based on arrival time stamp of jobs *OOP: given current timeStamp, joblist"""

            while (self.nextJobArrival<=self.timeStamp and len(self.jobList)!=0):      # asses any job in list which received
                if Set.debug:
                    print("     new jobs arrived with ID: ", self.jobList[self.head][self.id]," arrival: ",self.jobList[self.head][self.arrival])
                self.moveToQueu = self.jobList[self.head] # [0,[[1,2,21],[2,2,11],[4,2,7]],26,5,1],   [s,[[e1],[e2],[e3]],d,b,id],
                if Set.lastOption:
                    while len(self.moveToQueu[self.execs])>1:
                        del self.moveToQueu[self.execs][0]
                    if Set.debugDetail:
                        print("last option: ", self.moveToQueu)
                self.arrivalQueue.append(self.moveToQueu)
                del self.jobList[self.head]
                if len(self.jobList)!=0:
                    self.nextJobArrival = self.jobList[self.head][self.arrival]  # assumptions: job are sorted based on arrival time on array
                #print(Queu)



            """removing jobs which "deadline passed" from arrivalQueue  *OOP: given arrivalQueue"""

            self.shouldBeRemoved = []
            for job in self.arrivalQueue:                                 # remove dead jobs
                self.exec2remove=[]
                for execution in job[self.execs]:
                    if ( (self.timeStamp+execution[self.runtime]-job[self.arrival]) > job[self.deadline]):
                        if Set.debug:
                            print("     Execution will be Removed for job ID: ", job[self.id],"     ", (self.timeStamp+execution[self.runtime]) ,">", job[self.deadline],"     ",job)

                        if Set.firstOptionOnly:
                            #self.jobsFailed.append(job)
                            #self.shouldBeRemoved.append(job)
                            job[self.execs]=[]
                            if Set.debug:
                                print("           First Option only mode: JOB will be Removed with ID: ", job[self.id], "     ", job)
                        else:
                            self.exec2remove.append(execution)
                for exe in self.exec2remove:
                    job[self.execs].remove(exe)

                if (len(job[self.execs])==0):
                    self.jobsFailed.append(job)
                    if Set.debug:
                        print("           no Exec left: JOB will be Removed with ID: ", job[self.id],"     ",job)
                    self.shouldBeRemoved.append(job)
            for job in self.shouldBeRemoved:                     # may have problem with jobs with single option and First option exec !!!
                if self.shouldBeRemoved.count(job)>=1:
                    self.arrivalQueue.remove(job) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



            """Sorting Queue *OOP: given arrivalQueue"""

            #Sorted Queue
            self.arrivalQueue.sort(key=( lambda x: (( float(self.timeStamp+x[self.execs][self.head][self.runtime]-job[self.arrival])/float(x[self.deadline]) ) )+(x[self.bid]/float(Set.bidDegree))),reverse=True )
            #print(arrivalQueue)


            if True:
                """evaluate and apply addressability of job and put in resource pool if addressable *OOP: given  arrivalQueue"""

                self.evaluateScaleability=[]
                self.shadowQueue =copy.deepcopy(self.arrivalQueue[0:5])
                for waiting in self.shadowQueue:
                    if Set.debug:
                        print("\n     arrival queue head: ",waiting)
                    ### <<< evaluation
                    self.evaluateCurrentResource = copy.deepcopy(Set.resources) # copy resources so changes do not apply for evaluation
                    self.evaluateCurrentResource.sort(key=(lambda resource: (resource[self.rCore] - (waiting[self.execs][self.head][self.VMcore]))))#, reverse=True)
                    self.VMs2address = waiting[self.execs][self.head][self.numVM]
                    for i in range(self.VMs2address):
                        #print("VMs2address: ",VMs2address)
                        for res in self.evaluateCurrentResource:
                            #print("res: ",res)
                            if (res[self.rCore]>=(waiting[self.execs][self.head][self.VMcore])):
                                self.VMs2address = self.VMs2address-1
                                #print("if b res[rCore]",res[rCore])
                                res[self.rCore]= res[self.rCore] - (waiting[self.execs][self.head][self.VMcore])
                                #print("if a res[rCore]", res[rCore])
                                break
                        #print("for res end res[rCore]", res[rCore])
                        self.evaluateCurrentResource.sort(key=(lambda resource: (resource[self.rCore] - (waiting[self.execs][self.head][self.VMcore]))))#,reverse=True)
                    ### <<< end of evaluation
                    if self.VMs2address ==0:                   # all requested VMs can be addressed
                        if Set.debugLevel2:
                            print("     current resources: ",Set.resources)
                        if Set.debug:
                            print("     addressable job with ID: ", waiting[self.id]," numVMs requested: ",waiting[self.execs][self.head][self.numVM])
                        # return(True)
                        # this job is addressable so apply
                        # repeat the process and put in pool
                        # update the resources
                        ### >>> apply
                        self.evaluateCurrentResource = copy.deepcopy(Set.resources)
                        #print("evaluateCurrentResource Second:",evaluateCurrentResource)
                        self.evaluateCurrentResource.sort(key=(lambda resource: (resource[self.rCore] - (waiting[self.execs][self.head][self.VMcore]))))#, reverse=True)
                        self.VMs2address = waiting[self.execs][self.head][self.numVM]
                        for i in range(self.VMs2address):
                            for res in self.evaluateCurrentResource:
                                if (res[self.rCore] >= (waiting[self.execs][self.head][self.VMcore])):
                                    self.VMs2address = self.VMs2address - 1
                                    #print("if b res[rCore]", res[rCore])
                                    res[self.rCore] = res[self.rCore] - (waiting[self.execs][self.head][self.VMcore])
                                    #print("if a res[rCore]", res[rCore])
                                    self.reserved = self.pools[res[self.id]]
                                    self.reserved.append([waiting[self.execs][self.head][self.VMcore],waiting[self.execs][self.head][self.runtime],waiting[self.bid],waiting[self.id]])
                                    #print("res[id], reserved",res[id],res,reserved)
                                    self.pools[res[self.id]]=self.reserved
                                    break
                            self.evaluateCurrentResource.sort(key=(lambda resource: (resource[self.rCore] - (waiting[self.execs][self.head][self.VMcore]))))#, reverse=True)
                        self.evaluateScaleability.append(waiting) # this job is addressed and should be evaluated for Scalibility
                        self.jobsAddressed.append(waiting)
                        self.collectedBid=self.collectedBid+waiting[self.bid]
                        #print("     collected bid ",collectedBid)
                        self.arrivalQueue.remove(waiting)
                        #print("     !2 check Scalability:",evaluateScaleability)
                        Set.resources = copy.deepcopy(self.evaluateCurrentResource)
                        ### >>> end of apply
                        if Set.debugLevel2:
                            print("     resources reduced: ", Set.resources)
                    else:
                        if Set.debug:
                            print("     Job not addressable with ID: ", waiting[self.id])
                        if Set.debugLevel2:
                            print("     current resources: ", Set.resources)



                """Evaluate and apply scalability"""

                if Set.MEO:

                    if Set.debug:
                        print("\n     Evaluate and apply scalability")
                    time.sleep(Set.sleepTime)
                    self.notScaleable = []                 # first remove jobs with one execution option
                    for job in self.evaluateScaleability:
                        if Set.debug:
                            print("         job in evaluate scalability: ",job)
                        self.execsList= job[self.execs]
                        if len(self.execsList) == 1:
                            self.notScaleable.append(job)
                    for job in self.notScaleable:
                        self.evaluateScaleability.remove(job)

                    while len(self.evaluateScaleability)!=0:
                        # evaluateScaleability.append([waiting]) # numVMs, numCores ?

                        self.evaluateScaleability.sort(key=(#(lambda  x: x[self.execs][self.head])=========================================================================================================================================================================================================
                        lambda x: ( x[self.execs][self.head][self.runtime]+float(x[self.execs][self.head][self.runtime]*x[self.execs][self.head][self.numVM]*x[self.execs][self.head][self.VMcore]) / float(x[self.execs][self.head+1][self.runtime]*x[self.execs][self.head+1][self.numVM]*x[self.execs][self.head+1][self.VMcore])))
                        ,reverse=True)
                        if Set.debug:
                            print("     id: ",self.evaluateScaleability[self.head][self.id]," Scalability Factor: ",(self.evaluateScaleability[self.head][self.execs][self.head][self.runtime]*self.evaluateScaleability[self.head][self.execs][self.head][self.numVM]*self.evaluateScaleability[self.head][self.execs][self.head][self.VMcore]) / float(self.evaluateScaleability[self.head][self.execs][self.head+1][self.runtime]*self.evaluateScaleability[self.head][self.execs][self.head+1][self.numVM]*self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore]))

                        ### <<< evaluation

                        self.shadowPools= copy.deepcopy(self.pools)
                        self.shadowResources = copy.deepcopy(Set.resources)

                        for key in self.shadowPools.keys():  # for each pool ( each resource) # key is ID of resource
                            self.thisPool = self.shadowPools.get(key)
                            self.shouldBeRemoved = []  # creating array of jobs which should be removed for each pool (each resource)
                            for job in self.thisPool:
                                # reserved.append([waiting[execs][head][VMcore],waiting[execs][head][runtime],waiting[bid],waiting[id]])
                                if job[3] == self.evaluateScaleability[self.head][self.id]:  # if job finished
                                    if Set.debugLevel2:
                                        print("                         remove from pool to evaluate resource: ", key, " job ID: " ,job[3]," head execs: ",self.evaluateScaleability[self.head][self.execs][self.head])

                                    for res in self.shadowResources:  # returning used resource to pool
                                        if res[self.id] == key:
                                            res[self.rCore] = res[self.rCore] + job[0]
                                    self.shouldBeRemoved.append(job)  # collect jobs that SHOULD BE  removed
                            for job in self.shouldBeRemoved:
                                self.thisPool.remove(job)  # remove collected jobs


                        self.VMs2address = self.evaluateScaleability[self.head][self.execs][self.head+1][self.numVM]
                        self.shadowResources.sort(key=(lambda resource: (resource[self.rCore] - (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore]))))  # , reverse=True)
                        for i in range(self.VMs2address):
                            # print("VMs2address: ",VMs2address)
                            for res in self.shadowResources:
                                # print("res: ",res)
                                if (res[self.rCore] >= (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore])):
                                    self.VMs2address = self.VMs2address - 1
                                    # print("if b res[rCore]",res[rCore])
                                    res[self.rCore] = res[self.rCore] - (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore])
                                    # print("if a res[rCore]", res[rCore])
                                    break
                            # print("for res end res[rCore]", res[rCore])
                            self.shadowResources.sort(key=(
                            lambda resource: (resource[self.rCore] - (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore]))))  # ,reverse=True)

                        ### <<< end of evaluation

                        if self.VMs2address == 0:
                            ### >>> apply
                            for key in self.pools.keys():  # for each pool ( each resource) # key is ID of resource
                                self.thisPool = self.pools.get(key)
                                self.shouldBeRemoved = []  # creating array of jobs which should be removed for each pool (each resource)
                                for job in self.thisPool:
                                    # reserved.append([waiting[execs][head][VMcore],waiting[execs][head][runtime],waiting[bid],waiting[id]])
                                    if job[3] == self.evaluateScaleability[self.head][self.id]:  # if job finished
                                        if Set.debug:
                                            print("                         remove from pool (applicalable): resource: ", key, " job ID:", job[3],
                                              " Execs: ", self.evaluateScaleability[self.head][self.execs][self.head+1])
                                        self.shouldBeRemoved.append(job)
                                        for res in Set.resources:  # returning used resource to pool
                                            if res[self.id] == key:
                                                res[self.rCore] = res[self.rCore] + job[0]
                                          # collect jobs that SHOULD BE  removed
                                for job in self.shouldBeRemoved:
                                    self.thisPool.remove(job)  # remove collected jobs

                            if Set.debugLevel2:
                                print("         Scalability current resources: ", Set.resources)
                                print("         Scalability addressable job with ID: ", self.evaluateScaleability[self.head][self.id], " numVMs requested: ",
                                  self.evaluateScaleability[self.head][self.execs][self.head+1][self.numVM])

                            self.evaluateCurrentResource = copy.deepcopy(Set.resources)
                            # print("evaluateCurrentResource Second:",evaluateCurrentResource)
                            self.evaluateCurrentResource.sort(key=(
                            lambda resource: (resource[self.rCore] - (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore]))))  # , reverse=True)
                            self.VMs2address = self.evaluateScaleability[self.head][self.execs][self.head+1][self.numVM]
                            for i in range(self.VMs2address):
                                for res in self.evaluateCurrentResource:
                                    if (res[self.rCore] >= (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore])):
                                        self.VMs2address = self.VMs2address - 1
                                        # print("if b res[rCore]", res[rCore])
                                        res[self.rCore] = res[self.rCore] - (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore])
                                        # print("if a res[rCore]", res[rCore])
                                        self.reserved = self.pools[res[self.id]]
                                        self.reserved.append(
                                            [self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore], self.evaluateScaleability[self.head][self.execs][self.head+1][self.runtime], self.evaluateScaleability[self.head][self.bid],
                                             self.evaluateScaleability[self.head][self.id]])
                                        # print("res[id], reserved",res[id],res,reserved)
                                        self.pools[res[self.id]] = self.reserved
                                        if Set.debug:
                                            print("***after Scale putting in pools: " ,self.pools[res[self.id]])
                                        break
                                self.evaluateCurrentResource.sort(key=(
                                lambda resource: (resource[self.rCore] - (self.evaluateScaleability[self.head][self.execs][self.head+1][self.VMcore]))))  # , reverse=True)
                            self.jobsScaled.append(self.evaluateScaleability[self.head])
                            Set.resources = copy.deepcopy(self.evaluateCurrentResource)
                            if Set.debugLevel2:
                                print("         Scalability reduced resources: ", Set.resources)
                            self.evaluateScaleability[self.head][self.execs].remove(self.evaluateScaleability[self.head][self.execs][self.head])
                        else:
                            self.evaluateScaleability[self.head][self.execs].remove(self.evaluateScaleability[self.head][self.execs][self.head+1])
                            ### >>> end of apply


                        self.notScaleable = []  # first remove jobs with one execution option
                        for job in self.evaluateScaleability:
                            self.execsList = job[self.execs]
                            if len(self.execsList) == 1:
                                self.notScaleable.append(job)
                        for job in self.notScaleable:
                            self.evaluateScaleability.remove(job)



            #print(Set.jobList)
            self.timeStamp=self.timeStamp+1
            for res in Set.resources:
                self.unUsedArea=self.unUsedArea+res[self.rCore]
            time.sleep(Set.sleepTime)

        # loss =(sum(x[bid]) for x in jobsFailed)
        print("\n")
        self.totalArea=0
        for res in Set.resourcesMain:
            self.totalArea = self.totalArea + res[self.rCore]
        self.totalArea= self.totalArea * self.timeStamp

        self.loss=0
        for x in self.jobsFailed:
            self.loss=self.loss+x[self.bid]

        self.scaled = 0
        for x in self.jobsScaled:
            self.scaled = self.scaled + 1

        if Set.MEO:
            print(">>>MEO Results")
        if Set.firstOptionOnly:
            print(">>>First Options Results")
        if Set.lastOption:
            print(">>>last Options Results")
        if Set.debugLevel1:
            print("jobs Addressed: ", len(self.jobsAddressed))
            print("jobs Failed: " ,len(self.jobsFailed))
            print("number time Scaled: ",self.scaled)
            print("collected bid: ", self.collectedBid)
            print("lost bid: ", self.loss)
            print("unused area: ",self.unUsedArea)
            print("total area: ", self.totalArea)
            #print("number of times we scaled:")  #!!! fill
        print(Set.resources.sort(key=lambda x:x[self.id]))
        print("% Job Failed: ",int((len(self.jobsFailed)/float(len(self.jobsFailed)+len(self.jobsAddressed)))*100))
        print("% Job Scaled: ", int(self.scaled / float(len(self.jobsFailed) + len(self.jobsAddressed))*100))
        print("% unused area: ", int((self.unUsedArea / float(self.totalArea))*100))
        print("% gained bid: ",int((self.collectedBid/float(self.loss+self.collectedBid))*100))

        return ()