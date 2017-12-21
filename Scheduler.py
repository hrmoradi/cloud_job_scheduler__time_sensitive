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
        queue = []
        failed=[]

        timeStamp = 0
        timeChecker =0

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


            for key in pools.keys():
                thisPool=pools.get(key)
                shouldBeRemoved = []
                for job in thisPool:
                    #reserved.append([waiting[execs][head][VMcore],waiting[execs][head][runtime],waiting[bid],waiting[id]])
                    #print("b processtime",job)
                    job[1]=job[1]-1
                    #print("a processtime",job)
                    if job[1]==0:
                        print("                         job done with ID", job[3])
                        for res in Set.resources:
                            if res[id]==key:
                                res[rCore]=res[rCore]+job[0]
                        shouldBeRemoved.append(job)
                for job in shouldBeRemoved:
                    thisPool.remove(job)

            while (timeChecker<=timeStamp and len(Set.jobList)!=0):      # asses any job in list which received
                print("     new jobs arrived", Set.jobList[head][id])
                moveToQueu = Set.jobList[head] # [0,[[1,2,21],[2,2,11],[4,2,7]],26,5,1],   [s,[[e1],[e2],[e3]],d,b,id],
                queue.append(moveToQueu)
                del Set.jobList[head]
                if len(Set.jobList)!=0:
                    timeChecker = Set.jobList[head][arrival]
                #print(Queu)

            shouldBeRemoved = []
            for job in queue:                                 # remove dead jobs
                for execution in job[execs]:
                    if ( (timeStamp+execution[runtime]-job[arrival]) > job[deadline]):
                        print("     Execution Removed for job ID: ", job[id],"     ", (timeStamp+execution[runtime]) ,">", job[deadline],"     ",job)
                        job[execs].remove(execution)
                        if Set.firstOptionOnly:
                            shouldBeRemoved.append(job)
                            print("           JOB Removed with ID: ", job[id], "     ", job)
                if (len(job[execs])==0):
                    failed.append(job)
                    print("           JOB Removed with ID: ", job[id],"     ",job)
                    shouldBeRemoved.append(job)
            for job in shouldBeRemoved:
                 queue.remove(job)


            #Sorted Queue
            queue.sort(key=( lambda x: ( float(timeStamp+x[execs][head][runtime]-job[arrival])/float(x[deadline]) ) ),reverse=True )
            #print(queue)

            #address ability of job in waiting
            waitingInPool=[]
            shadowQueue =copy.deepcopy(queue)
            for waiting in shadowQueue:
                print("\n     waiting head: ",waiting)
                ### <<<
                evaluateCurrentResource = copy.deepcopy(Set.resources)
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
                ### <<<
                if VMs2address ==0:
                    print("     current resources: ",Set.resources)
                    print("     addressable job with ID: ", waiting[id])
                    # return(True)
                    # this job is addressable so apply
                    # repeat the process and put in pool
                    # update the resources
                    ### >>>
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
                    waitingInPool.append([waiting])
                    collectedBid=collectedBid+waiting[bid]
                    print("     collected bid ",collectedBid)
                    queue.remove(waiting)
                    print("     !2 check Scalability:",waitingInPool)
                    Set.resources = copy.deepcopy(evaluateCurrentResource)
                    ### >>>
                    print("     resources reduced: ", Set.resources)
                else:
                    print("     Job not addressable with ID: ", waiting[id])
                    print("     current resources: ", Set.resources)



            #print(Set.jobList)
            timeStamp=timeStamp+1
            time.sleep(1)



        return ()