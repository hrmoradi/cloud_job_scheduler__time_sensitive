import SchedulerEmulator.Settings as Set

import time
import copy

class ClassSchduler():

    def MainScheduler(jobList ):
        print("MainScheduler")
        #print(len(Set.jobList))

        """
        defining required constants and variables
        """
        arrivalQueue = []
        jobsFailed=[]
        jobsAddressed=[]

        timeStamp = 0
        nextJobArrival =0

        numVM=0
        VMcore=1
        rCore=0
        rMem=1

        head=0
        arrival=0
        execs=1
        runtime =2
        deadline=2
        bid=3
        id = 4

        collectedBid=0

        pools = {}
        for res in Set.resources:
            pools[res[id]]=[]

        """
        Simulation Starts
        """

        for du in range(Set.duration):                    # for specified time
            print("\nCurrent timeStamp: ",timeStamp," duration:",du)



            """ reducing processing time & removing "finished" jobs *OOP: given pools dic, """

            for key in pools.keys():                 # for each pool ( each resource) # key is ID of resource
                thisPool=pools.get(key)
                shouldBeRemoved = []                 # creating array of jobs which should be removed for each pool (each resource)
                for job in thisPool:
                    #reserved.append([waiting[execs][head][VMcore],waiting[execs][head][runtime],waiting[bid],waiting[id]])
                    #print("b processtime",job)
                    job[1]=job[1]-1                  # reducing processing time
                    #print("a processtime",job)
                    if job[1]==0:                    # if job finished
                        print("                         a VM will be removed from pool",key," job done with ID", job[3])
                        for res in Set.resources:    # returning used resource to pool
                            if res[id]==key:
                                res[rCore]=res[rCore]+job[0]
                        shouldBeRemoved.append(job)  # collect jobs that SHOULD BE  removed
                for job in shouldBeRemoved:
                    thisPool.remove(job)             # remove collected jobs




            """adding "new jobs" to arrivalQueue based on arrival time stamp of jobs *OOP: given current timeStamp, joblist"""

            while (nextJobArrival<=timeStamp and len(Set.jobList)!=0):      # asses any job in list which received
                print("     new jobs arrived with ID: ", Set.jobList[head][id]," arrival: ",Set.jobList[head][arrival])
                moveToQueu = Set.jobList[head] # [0,[[1,2,21],[2,2,11],[4,2,7]],26,5,1],   [s,[[e1],[e2],[e3]],d,b,id],
                arrivalQueue.append(moveToQueu)
                del Set.jobList[head]
                if len(Set.jobList)!=0:
                    nextJobArrival = Set.jobList[head][arrival]  # assumptions: job are sorted based on arrival time on array
                #print(Queu)



            """removing jobs which "deadline passed" from arrivalQueue  *OOP: given arrivalQueue"""

            shouldBeRemoved = []
            for job in arrivalQueue:                                 # remove dead jobs
                exec2remove=[]
                for execution in job[execs]:
                    if ( (timeStamp+execution[runtime]-job[arrival]) > job[deadline]):
                        print("     Execution will be Removed for job ID: ", job[id],"     ", (timeStamp+execution[runtime]) ,">", job[deadline],"     ",job)
                        exec2remove.append(execution)
                        if Set.firstOptionOnly:
                            jobsFailed.append(job)
                            shouldBeRemoved.append(job)
                            print("           First Option only mode: JOB will be Removed with ID: ", job[id], "     ", job)
                for exe in exec2remove:
                    job[execs].remove(execution)

                if (len(job[execs])==0):
                    jobsFailed.append(job)
                    print("           no Exec left: JOB will be Removed with ID: ", job[id],"     ",job)
                    shouldBeRemoved.append(job)
            for job in shouldBeRemoved:                     # may have problem with jobs with single option and First option exec !!!
                 arrivalQueue.remove(job)



            """Sorting Queue *OOP: given arrivalQueue"""

            #Sorted Queue
            arrivalQueue.sort(key=( lambda x: ( float(timeStamp+x[execs][head][runtime]-job[arrival])/float(x[deadline]) ) ),reverse=True )
            #print(arrivalQueue)



            """evaluate and apply addressability of job and put in resource pool if addressable *OOP: given  arrivalQueue"""

            evaluateScaleability=[]
            shadowQueue =copy.deepcopy(arrivalQueue)
            for waiting in shadowQueue:
                print("\n     arrival queue head: ",waiting)
                ### <<< evaluation
                evaluateCurrentResource = copy.deepcopy(Set.resources) # copy resources so changes do not apply for evaluation
                evaluateCurrentResource.sort(key=(lambda resource: (resource[rCore] - (waiting[execs][head][VMcore]))))#, reverse=True)
                VMs2address = waiting[execs][head][numVM]
                for i in range(VMs2address):
                    #print("VMs2address: ",VMs2address)
                    for res in evaluateCurrentResource:
                        #print("res: ",res)
                        if (res[rCore]>=(waiting[execs][head][VMcore])):
                            VMs2address = VMs2address-1
                            #print("if b res[rCore]",res[rCore])
                            res[rCore]= res[rCore] - (waiting[execs][head][VMcore])
                            #print("if a res[rCore]", res[rCore])
                            break
                    #print("for res end res[rCore]", res[rCore])
                    evaluateCurrentResource.sort(key=(lambda resource: (resource[rCore] - (waiting[execs][head][VMcore]))))#,reverse=True)
                ### <<< end of evaluation
                if VMs2address ==0:                   # all requested VMs can be addressed
                    print("     current resources: ",Set.resources)
                    print("     addressable job with ID: ", waiting[id]," numVMs requested: ",waiting[execs][head][numVM])
                    # return(True)
                    # this job is addressable so apply
                    # repeat the process and put in pool
                    # update the resources
                    ### >>> apply
                    evaluateCurrentResource = copy.deepcopy(Set.resources)
                    #print("evaluateCurrentResource Second:",evaluateCurrentResource)
                    evaluateCurrentResource.sort(key=(lambda resource: (resource[rCore] - (waiting[execs][head][VMcore]))))#, reverse=True)
                    VMs2address = waiting[execs][head][numVM]
                    for i in range(VMs2address):
                        for res in evaluateCurrentResource:
                            if (res[rCore] >= (waiting[execs][head][VMcore])):
                                VMs2address = VMs2address - 1
                                #print("if b res[rCore]", res[rCore])
                                res[rCore] = res[rCore] - (waiting[execs][head][VMcore])
                                #print("if a res[rCore]", res[rCore])
                                reserved = pools[res[id]]
                                reserved.append([waiting[execs][head][VMcore],waiting[execs][head][runtime],waiting[bid],waiting[id]])
                                #print("res[id], reserved",res[id],res,reserved)
                                pools[res[id]]=reserved
                                break
                        evaluateCurrentResource.sort(key=(lambda resource: (resource[rCore] - (waiting[execs][head][VMcore]))))#, reverse=True)
                    evaluateScaleability.append([waiting]) # this job is addressed and should be evaluated for Scalibility
                    jobsAddressed.append(waiting)
                    collectedBid=collectedBid+waiting[bid]
                    #print("     collected bid ",collectedBid)
                    arrivalQueue.remove(waiting)
                    #print("     !2 check Scalability:",evaluateScaleability)
                    Set.resources = copy.deepcopy(evaluateCurrentResource)
                    ### >>> end of apply
                    print("     resources reduced: ", Set.resources)
                else:
                    print("     Job not addressable with ID: ", waiting[id])
                    print("     current resources: ", Set.resources)


            if Set.MEO:
                """Evaluate and apply scalability"""
                #evaluateScaleability.append([waiting]) # numVMs, numCores ?
                



            #print(Set.jobList)
            timeStamp=timeStamp+1
            time.sleep(0.1)

        # loss =(sum(x[bid]) for x in jobsFailed)
        loss=0
        for x in jobsFailed:
            loss=loss+x[bid]

        print("jobs Addressed: ", len(jobsAddressed))
        print("jobs Failed: " ,len(jobsFailed))
        print("collected bid: ", collectedBid)
        print("lost bid: ", loss)
        print("number of times we scaled:")  #!!! fill

        return ()