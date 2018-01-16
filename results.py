import matplotlib.pyplot as plt
import numpy as np
import SchedulerEmulator.Settings as Set
import SchedulerEmulator.Main as Mainfile



location = np.arange(7)
load=["80","90","100","110","120","130","140"]



""" Start of automated result generation """

pointer=-1
clusterString= ["largeCluster","mediumCluster","smallCluster"]

for cluster in  [Set.LargeCluster]:#,Set.MediumCluster, Set.SmallCluster]: ######################### cluster size set
    pointer+=1
    Set.resources = cluster
    Set.capacity = sum(int(cpu) for cpu, b, c, d, e in Set.resources)
    Set.capMem= sum(int(mem) for cpu, mem, c, d, e in Set.resources)
    print(" cap:",Set.capacity,"mem: ",Set.capMem," Set.resources",Set.resources)

    discardedMEO = []
    discardedFirst = []
    discardedLast = []
    discardedgreedyFirst=[]

    bidMEO = []
    bidFirst = []
    bidLast = []
    bidgreedyFirst=[]

    unusedMEO=[]
    unusedFirst=[]
    unusedLast=[]
    unusedgreedyFirst=[]

    mfcpArray=[]
    ffcpArray=[]
    lfcpArray=[]
    gfcpArray=[]

    mfmpArray=[]
    ffmpArray=[]
    lfmpArray=[]
    gfmpArray=[]

    avgLastUnusedMemArray=[]
    avgFirstUnusedMemArray=[]
    avgMeoUnusedMemArray=[]
    avggreedyFirstUnusedMemArray=[]


    for loadRatio in range(80,140+Set.loadInc,Set.loadInc): ############################################################# load
        Set.avgSysLoad=loadRatio/100.0
        #print("Set.avgSysLoad",Set.avgSysLoad)

        results= Mainfile.MainClass.mainMethod() ####################################################### running simulation
        [graph, title]=results
        [avgMeoFailed, avgMeoGained, avgFirstFailed, avgFirstGained, avgLastFailed, avgLastGained, avggreedyFirstFailed,avggreedyFirstGained,avgMeoUnused,avgFirstUnused,avgLastUnused,avggreedyFirstUnused,mfcp,mfmp,ffcp,ffmp,lfcp,lfmp,gfcp,gfmp,avgLastUnusedMem,avgFirstUnusedMem,avgMeoUnusedMem,avggreedyFirstUnusedMem]=graph
        print("results returned from main: mf mg f l: ",results)
        discardedMEO.append(avgMeoFailed)
        bidMEO.append(avgMeoGained)
        unusedMEO.append(avgMeoUnused)

        discardedFirst.append(avgFirstFailed)
        bidFirst.append(avgFirstGained)
        unusedFirst.append(avgFirstUnused)

        discardedLast.append(avgLastFailed)
        bidLast.append(avgLastGained)
        unusedLast.append(avgLastUnused)

        discardedgreedyFirst.append(avggreedyFirstFailed)
        bidgreedyFirst.append(avggreedyFirstGained)
        unusedgreedyFirst.append(avggreedyFirstUnused)

        mfcpArray.append(mfcp)
        ffcpArray.append(ffcp)
        lfcpArray.append(lfcp)
        gfcpArray.append(gfcp)

        mfmpArray.append(mfmp)
        ffmpArray.append(ffmp)
        lfmpArray.append(lfmp)
        gfmpArray.append(gfmp)

        avgLastUnusedMemArray.append(avgLastUnusedMem)
        avgFirstUnusedMemArray.append(avgFirstUnusedMem)
        avgMeoUnusedMemArray.append(avgMeoUnusedMem)
        avggreedyFirstUnusedMemArray.append(avggreedyFirstUnusedMemArray)

    """ cp: core area percentage """
    plt.bar(location - 0.2, lfcpArray, align="center", width=0.1, color="lightcoral")
    plt.bar(location - 0.1, ffcpArray, align="center", width=0.1, color="k")
    plt.bar(location, mfcpArray, align="center", width=0.1, color="springgreen")
    plt.bar(location + 0.1, gfcpArray, align="center", width=0.1, color="g")
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 110, 5))
    plt.ylabel("% Discarded Core*time Area")
    plt.xlabel("Load")
    plt.legend(["Thickest Option", "First Option", "Resource Scale Up (RSU)", "TSRA-Greedy"])
    title4Plot = 'Discarded Core*time'  # +title
    plt.title(title4Plot)
    # plt.show()
    plt.savefig(Set.add+ clusterString[
        pointer] + "-discarded-CoreTimePercentage.eps")
    plt.clf()

    """ mp: memory area percentage """
    plt.bar(location - 0.2, lfmpArray, align="center", width=0.1, color="lightcoral")
    plt.bar(location - 0.1, ffmpArray, align="center", width=0.1, color="k")
    plt.bar(location, mfmpArray, align="center", width=0.1, color="springgreen")
    plt.bar(location + 0.1, gfmpArray, align="center", width=0.1, color="g")
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 110, 5))
    plt.ylabel("% Discarded Mem*time Area")
    plt.xlabel("Load")
    plt.legend(["Thickest Option", "First Option", "Resource Scale Up (RSU)", "TSRA-Greedy"])
    title4Plot = 'Discarded Mem*time'  # +title
    plt.title(title4Plot)
    # plt.show()
    plt.savefig(Set.add+ clusterString[
        pointer] + "-discarded-MemTimePercentage.eps")
    plt.clf()

    """ Discarded barchart """
    plt.bar(location - 0.2, discardedLast, align="center", width=0.1, color="lightcoral")
    plt.bar(location - 0.1, discardedFirst, align="center", width=0.1, color="k")
    plt.bar(location, discardedMEO, align="center", width=0.1, color="springgreen")
    plt.bar(location +0.1, discardedgreedyFirst, align="center", width=0.1, color="g")
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 110, 5))
    plt.ylabel("% Discarded Jobs")
    plt.xlabel("Load")
    plt.legend(["Thickest Option", "First Option", "Resource Scale Up (RSU)", "TSRA-Greedy"])
    title4Plot= 'Discarded JOBS'#+title
    plt.title(title4Plot)
    #plt.show()
    plt.savefig(Set.add+ clusterString[pointer] + "-discarded-Job-Percentage.eps")
    plt.clf()

    """ Gained benefit line"""
    plt.plot(location, bidLast, '.-', color="lightcoral", linewidth=0.4)
    plt.plot(location, bidFirst, '+-', color="k", linewidth=0.4)
    plt.plot(location, bidMEO, 'x-', color="springgreen", linewidth=0.4)
    plt.plot(location , bidgreedyFirst,'-', color="green", linewidth=0.4)
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 110, 10))
    plt.ylabel("% Achived Benefit")
    plt.xlabel("Load")
    plt.legend(["Thickest Option", "First Option", "Resource Scale Up (RSU)", "TSRA-Greedy"])
    title4Plot = 'Gained Benefit'# + title
    plt.title(title4Plot)
    #plt.show()
    plt.savefig(Set.add+clusterString[pointer] +"-gained-Bid-Percentage.eps")
    plt.clf()

    """ Unused CPU Barchart """
    plt.bar(location - 0.2, unusedLast, align="center", width=0.1, color="lightcoral")
    plt.bar(location - 0.1, unusedFirst, align="center", width=0.1, color="k")
    plt.bar(location,unusedMEO, align="center", width=0.1, color="springgreen")
    plt.bar(location +0.1, unusedgreedyFirst, align="center", width=0.1, color="g")
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 110, 5))
    plt.ylabel("% Unused Area")
    plt.xlabel("Load")
    plt.legend(["Thickest Option", "First Option", "Resource Scale Up (RSU)", "TSRA-Greedy"])
    title4Plot = 'Unused Area'# + title
    plt.title(title4Plot)
    #plt.show()
    plt.savefig(Set.add+clusterString[pointer] + "-unusedArea-CPU-Percentage.eps")
    #plt.savefig("/home/hrmoradi/PycharmProjects/PythonProjects/SchedulerEmulator/output/" + clusterString[pointer] + "-unusedAreaPercentage.png")
    plt.clf()

    """ Unused MEM Barchart """
    plt.bar(location - 0.2, avgLastUnusedMemArray, align="center", width=0.1, color="lightcoral")
    plt.bar(location - 0.1, avgFirstUnusedMemArray, align="center", width=0.1, color="k")
    plt.bar(location, avgMeoUnusedMemArray, align="center", width=0.1, color="springgreen")
    plt.bar(location + 0.1, avggreedyFirstUnusedMem, align="center", width=0.1, color="g")
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 110, 5))
    plt.ylabel("% Unused Mem Area")
    plt.xlabel("Load")
    plt.legend(["Thickest Option", "First Option", "Resource Scale Up (RSU)", "TSRA-Greedy"])
    title4Plot = 'Unused Mem Area'  # + title
    plt.title(title4Plot)
    # plt.show()
    plt.savefig(Set.add + clusterString[pointer] + "-unusedArea-MEM-Percentage.eps")
    # plt.savefig("/home/hrmoradi/PycharmProjects/PythonProjects/SchedulerEmulator/output/" + clusterString[pointer] + "-unusedAreaPercentage.png")
    plt.clf()

    plt.title(title)
    # plt.show()
    plt.savefig(Set.add+ clusterString[pointer] + "-detail.eps")

"""
discardedMEO = [4,7,10.2,13.4,16.8,20.5,23.8]
discardedFirst=[1,4.2,11.1,16.1,20.3,24.0,27.4]
discardedLast= [21,25.7,29.3,31.6,34.9,38.4,40]

bidMEO=[99,99,98.2,96.3,90.4,83.0,76.1]
bidFirst=[99,99,98.9,94.6,85.5,77.7,70.9]
bidLast=[84,76.2,69.9,64.3,58.5,53.7,49.6]

plt.bar(location-0.2,discardedLast, align="center",width=0.1, color="lightcoral")
plt.bar(location-0.1,discardedFirst, align="center",width=0.1, color="k")
plt.bar(location,discardedMEO, align="center",width=0.1, color="springgreen")
plt.xticks(location,load)
plt.yticks(np.arange(0,50,5))
plt.ylabel("Discarded Jobs")
plt.xlabel("Load")
plt.legend(["TSRA-Thickest Option","TSRA-First Option","TSRA-Addaptive"])
plt.show()

plt.plot(location,bidLast,'.-',color="lightcoral", linewidth=0.4)
plt.plot(location,bidFirst,'+-',color="k", linewidth=0.4)
plt.plot(location,bidMEO,'x-',color="springgreen", linewidth=0.4)
plt.xticks(location,load)
plt.yticks(np.arange(0,110,10))
plt.ylabel("Achived benefit")
plt.xlabel("Load")
plt.legend(["TSRA-Thickest Option","TSRA-First Option","TSRA-Addaptive"])
plt.show()
"""
