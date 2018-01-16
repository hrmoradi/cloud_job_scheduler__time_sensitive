import SchedulerEmulator.Settings as Set
import copy
from SchedulerEmulator.JobCreator import ClassJobCreator as CJ
from SchedulerEmulator.Scheduler import ClassSchduler as CS



class MainClass:
    def mainMethod():
        meo=[]
        first=[]
        last=[]
        greedyFirst=[]

        failed=0
        scaled=1
        unused=2
        gain=3

        print("\nnumber of iteration: ",Set.numberOfIteration,
              "| number of time interval: ", Set.NumberOfTimeInterval,
              "| each interval: ",Set.eachTimeInterval,
              "| avg Load: ", Set.avgSysLoad,
              "| random Job: ",Set.randJob,
              "| capacity: ",Set.capacity,
              "| mem: ", Set.capMem)


        """ Running Simulation iterations """

        for i in range(Set.numberOfIteration):

            print("\n Main Iteration:", i,"\n")
            #print("\n\n***Main:createJobList")
            JobCreator= CJ()
            jobList=JobCreator.MainJobCreator()

            #print("\n\n***Main:Emulate TSRA-MEO")
            Set.firstOptionOnly = False
            Set.MEO = True
            Set.lastOption = False
            Set.greedy=False
            EmulateMEO =CS()
            results=EmulateMEO.MainScheduler(jobList,Set.resources)
            meo.append(results)

            #print("\n\n***Main:Emulate TSRA-First")
            Set.firstOptionOnly=True
            Set.MEO=False
            Set.lastOption=False
            Set.greedy=False
            EmulateFirst=CS()
            results =EmulateFirst.MainScheduler(jobList,Set.resources)
            first.append(results)

            #print("\n\n***Main:Emulate TSRA-last")
            Set.firstOptionOnly=False
            Set.MEO=False
            Set.lastOption=True
            Set.greedy=False
            EmulateLast=CS()
            results =EmulateLast.MainScheduler(jobList,Set.resources)
            last.append(results)

            # print("\n\n***Main:Emulate Greedy")
            Set.firstOptionOnly = False
            Set.MEO = False
            Set.lastOption = False
            Set.greedy = True
            EmulateLast = CS()
            results = EmulateLast.MainScheduler(jobList, Set.resources)
            greedyFirst.append(results)



        """ Average of simulations """

        avgMeoFailed = sum(int(f) for f,s,u,g,a,uM in meo)/float(Set.numberOfIteration)
        print("\navg Meo Failed: %",avgMeoFailed)
        avgMeoScaled = sum(int(s) for f,s,u,g,a,uM in meo)/float(Set.numberOfIteration)
        print("avg Meo Scaled: %",avgMeoScaled)
        avgMeoUnused = sum(int(u) for f,s,u,g,a,uM in meo)/float(Set.numberOfIteration)
        print("avg Meo Unused: %",avgMeoUnused)
        avgMeoUnusedMem = sum(int(uM) for f, s, u, g, a, uM in meo) / float(Set.numberOfIteration)
        print("avg Meo Unused MEM: %", avgMeoUnusedMem)
        avgMeoGained = sum(int(g) for f,s,u,g,a,uM in meo)/float(Set.numberOfIteration)
        print("avg Meo Gained Bid: %",avgMeoGained)

        fc = (sum(int(fc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in meo)   /float(Set.numberOfIteration))
        print("fc: ", fc)
        gc = (sum(int(gc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in meo)   /float(Set.numberOfIteration))
        print("gc: ", gc)
        tc = (sum(int(tc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in meo)   /float(Set.numberOfIteration))
        print("fc: ", tc)

        print("fc: %", (fc/gc)*100)
        print("gc: %", (gc/tc)*100)
        print("tc: %", ((fc+gc)/tc)*100)

        fm = (sum(int(fm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in meo) /float(Set.numberOfIteration))
        #print("fm: ", fm)
        tm = (sum(int(tm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in meo)/float(Set.numberOfIteration))
        #print("tm: ", tm)
        mfmp=((fm) / tm) * 100
        print("mfmp: %", mfmp)

        fc = (sum(int(fc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in meo) / float(Set.numberOfIteration))
        #print("fc: ", fc)
        tc = (sum(int(tc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in meo) / float(Set.numberOfIteration))
        #print("tc: ", tc)
        mfcp = ((fc) / tc) * 100
        print("mfcp: %", mfcp)

        avgFirstFailed = sum(int(f) for f,s,u,g,a,uM in first)/float(Set.numberOfIteration)
        print("\navg First Failed: %",avgFirstFailed)
        avgFirstScaled = sum(int(s) for f,s,u,g,a,uM in first)/float(Set.numberOfIteration)
        print("avg First Scaled: %",avgFirstScaled)
        avgFirstUnused = sum(int(u) for f,s,u,g,a,uM in first)/float(Set.numberOfIteration)
        print("avg First Unused: %",avgFirstUnused)
        avgFirstUnusedMem = sum(int(uM) for f, s, u, g, a, uM in first) / float(Set.numberOfIteration)
        print("avg First Unused MEM: %", avgFirstUnusedMem)
        avgFirstGained = sum(int(g) for f,s,u,g,a,uM in first)/float(Set.numberOfIteration)

        print("avg First Gained Bid: %",avgFirstGained)

        fm = (sum(int(fm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in first) / float(Set.numberOfIteration))
        # print("fm: ", fm)
        tm = (sum(int(tm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in first) / float(Set.numberOfIteration))
        # print("tm: ", tm)
        ffmp = ((fm) / tm) * 100
        print("ffmp: %", ffmp)

        fc = (sum(int(fc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in first) / float(Set.numberOfIteration))
        # print("fc: ", fc)
        tc = (sum(int(tc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in first) / float(Set.numberOfIteration))
        # print("tc: ", tc)
        ffcp = ((fc) / tc) * 100
        print("ffcp: %", ffcp)

        avgLastFailed = sum(int(f) for f,s,u,g,a,uM in last)/float(Set.numberOfIteration)
        print("\navg Last Failed: %",avgLastFailed)
        avgLastScaled = sum(int(s) for f,s,u,g,a,uM in last)/float(Set.numberOfIteration)
        print("avg Last Scaled: %",avgLastScaled)
        avgLastUnused = sum(int(u) for f,s,u,g,a,uM in last)/float(Set.numberOfIteration)
        print("avg Last Unused: %",avgLastUnused)
        avgLastUnusedMem = sum(int(uM) for f, s, u, g, a, uM in last) / float(Set.numberOfIteration)
        print("avg Last Unused MEM: %", avgLastUnusedMem)
        avgLastGained = sum(int(g) for f,s,u,g,a,uM in last)/float(Set.numberOfIteration)
        print("avg Last Gained Bid: %",avgLastGained)

        fm = (sum(int(fm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in last) / float(Set.numberOfIteration))
        # print("fm: ", fm)
        tm = (sum(int(tm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in last) / float(Set.numberOfIteration))
        # print("tm: ", tm)
        lfmp = ((fm) / tm) * 100
        print("lfmp: %", lfmp)

        fc = (sum(int(fc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in last) / float(Set.numberOfIteration))
        # print("fc: ", fc)
        tc = (sum(int(tc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in last) / float(Set.numberOfIteration))
        # print("tc: ", tc)
        lfcp = ((fc) / tc) * 100
        print("lfcp: %", lfcp)

        avggreedyFirstFailed = sum(int(f) for f, s, u, g,a,uM in greedyFirst) / float(Set.numberOfIteration)
        print("\navg greedyFirst Failed: %", avggreedyFirstFailed)
        avggreedyFirstScaled = sum(int(s) for f, s, u, g,a,uM in greedyFirst) / float(Set.numberOfIteration)
        print("avg greedyFirst Scaled: %", avggreedyFirstScaled)
        avggreedyFirstUnused = sum(int(u) for f, s, u, g,a,uM in greedyFirst) / float(Set.numberOfIteration)
        print("avg greedyFirst Unused: %", avggreedyFirstUnused)
        avggreedyFirstUnusedMem = sum(int(uM) for f, s, u, g, a, uM in greedyFirst) / float(Set.numberOfIteration)
        print("avg greedyFirst Unused MEM: %", avggreedyFirstUnusedMem)
        avggreedyFirstGained = sum(int(g) for f, s, u, g,a,uM in greedyFirst) / float(Set.numberOfIteration)
        print("avg greedyFirst Gained Bid: %", avggreedyFirstGained)
        fc = (sum(int(fc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in greedyFirst) / float(Set.numberOfIteration))
        # print("fc: ", fc)
        tc = (sum(int(tc) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in greedyFirst) / float(Set.numberOfIteration))
        # print("tc: ", tc)
        gfcp = ((fc) / tc) * 100
        print("gfcp: %", gfcp)
        fm = (sum(int(fm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in greedyFirst) / float(Set.numberOfIteration))
        # print("fm: ", fm)
        tm = (sum(int(tm) for f, s, u, g, [fc, fm, gc, gm, tc, tm],uM in greedyFirst) / float(Set.numberOfIteration))
        # print("tm: ", tm)
        gfmp = ((fm) / tm) * 100
        print("gfmp: %", gfmp)

        print("\nnumber of iteration: ",Set.numberOfIteration,
              "| number of time interval: ", Set.NumberOfTimeInterval,
              "| each interval: ",Set.eachTimeInterval,
              "| avg Load: ", Set.avgSysLoad,
              "| random Job: ",Set.randJob,
              "| capacity: ",Set.capacity)

        return ([avgMeoFailed,avgMeoGained,avgFirstFailed,avgFirstGained,avgLastFailed,avgLastGained,avggreedyFirstFailed,avggreedyFirstGained,avgMeoUnused,avgFirstUnused,avgLastUnused,avggreedyFirstUnused,mfcp,mfmp,ffcp,ffmp,lfcp,lfmp,gfcp,gfmp,avgLastUnusedMem,avgFirstUnusedMem,avgMeoUnusedMem,avggreedyFirstUnusedMem],
                ["it:",Set.numberOfIteration,
              "|interval:", Set.NumberOfTimeInterval,
              "|of:",Set.eachTimeInterval,
              "|rand:",Set.randJob])

if __name__== '__main__':
    MainClass.mainMethod()