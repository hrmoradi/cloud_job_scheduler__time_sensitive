import SchedulerEmulator.Settings as Set

import time
import copy

class ClassSchduler():

    def MainScheduler(jobList ):
        print("MainScheduler")
        print(len(Set.jobList))
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

        for du in range(Set.duration):                    # for specified time
            print("\nCurrent timeStamp: ",timeStamp," duration:",du)



            while (timeChecker<=timeStamp and len(Set.jobList)!=0):      # asses any job in list which received
                moveToQueu = Set.jobList[head] # [0,[[1,2,21],[2,2,11],[4,2,7]],26,5,1],   [s,[[e1],[e2],[e3]],d,b,id],
                queue.append(moveToQueu)
                del Set.jobList[head]
                if len(Set.jobList)!=0:
                    timeChecker = Set.jobList[head][arrival]
                #print(Queu)



            for job in queue:                                 # remove dead jobs
                for execution in job[execs]:
                    if ( (timeStamp+execution[runtime]) > job[deadline]):
                        print("          Execution Removed for job ID: ", job[id],"     ", (timeStamp+execution[runtime]) ,">", job[deadline],"     ",job)
                        job[execs].remove(execution)
                if (len(job[execs])==0):
                    failed.append(job)
                    print("     JOB Removed with ID: ", job[id],"     ",job)
                    queue.remove(job)


            #Sorted Queue
            queue.sort(key=( lambda x: ( (timeStamp+x[execs][head][runtime])/(x[deadline]) ) ),reverse=True )
            #print(queue)

            #address ability of job in waiting
            for waiting in queue:
                evaluateCurrentResource = copy.copy(Set.resources)
                evaluateCurrentResource.sort(key=(lambda resource: (resource[rCore] - (waiting[execs][head][VMcore]))), reverse=True)
                VMs2address = waiting[execs][head][numVM]
                for i in range(VMs2address):
                    for res in Set.resources:
                        if (res[rCore]>(waiting[execs][head][VMcore])):
                            VMs2address = VMs2address-1
                            print("if b res[rCore]",res[rCore])
                            res[rCore]= res[rCore] - (waiting[execs][head][VMcore])
                            print("if a res[rCore]", res[rCore])
                            break
                    print("for res end res[rCore]", res[rCore])
                    evaluateCurrentResource.sort(key=(lambda resource: (resource[rCore] - (waiting[execs][head][VMcore]))),reverse=True)
                if VMs2address ==0:
                    print("addressable job with ID: ", waiting[id])
                    # return(True)
                    # this job is addressable so apply
                    # repeat the process and put in pool
                    # update the resources
                    
                else:
                    print("not currently addressable job with ID: ", waiting[id])



            #print(Set.jobList)
            timeStamp=timeStamp+1
            time.sleep(4)



        return ()