import matplotlib.pyplot as plt
import numpy as np
import SchedulerEmulator.Settings as Set
import SchedulerEmulator.Main as Mainfile



location = np.arange(7)
load=["80","90","100","110","120","130","140"]
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



""" Start of automated result generation """

pointer=-1
clusterString= ["s","m","l"]

for cluster in [Set.SmallCluster, Set.MediumCluster, Set.LargeCluster]:
    pointer+=1
    Set.resources = cluster
    Set.capacity = sum(int(s) for s, b, c, d, e in Set.resources)
    print(" cap:",Set.capacity," Set.resources",Set.resources)

    discardedMEO = []
    discardedFirst = []
    discardedLast = []

    bidMEO = []
    bidFirst = []
    bidLast = []

    for loadRatio in range(80,140+10,10):
        Set.avgSysLoad=loadRatio/100.0
        print("Set.avgSysLoad",Set.avgSysLoad)

        results= Mainfile.MainClass.mainMethod()
        [graph, title]=results
        [avgMeoFailed, avgMeoGained, avgFirstFailed, avgFirstGained, avgLastFailed, avgLastGained]=graph
        print(results)
        discardedMEO.append(avgMeoFailed)
        bidMEO.append(avgMeoGained)

        discardedFirst.append(avgFirstFailed)
        bidFirst.append(avgFirstGained)

        discardedLast.append(avgLastFailed)
        bidLast.append(avgLastGained)

    plt.bar(location - 0.2, discardedLast, align="center", width=0.1, color="lightcoral")
    plt.bar(location - 0.1, discardedFirst, align="center", width=0.1, color="k")
    plt.bar(location, discardedMEO, align="center", width=0.1, color="springgreen")
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 50, 5))
    plt.ylabel("Discarded Jobs")
    plt.xlabel("Load")
    plt.legend(["TSRA-Thickest Option", "TSRA-First Option", "TSRA-Addaptive"])
    #plt.show()
    plt.savefig("/home/hrmoradi/PycharmProjects/PythonProjects/SchedulerEmulator/output/" + clusterString[pointer] + "-discard.png")
    plt.clf()

    plt.plot(location, bidLast, '.-', color="lightcoral", linewidth=0.4)
    plt.plot(location, bidFirst, '+-', color="k", linewidth=0.4)
    plt.plot(location, bidMEO, 'x-', color="springgreen", linewidth=0.4)
    plt.xticks(location, load)
    plt.yticks(np.arange(0, 110, 10))
    plt.ylabel("Achived benefit")
    plt.xlabel("Load")
    plt.legend(["TSRA-Thickest Option", "TSRA-First Option", "TSRA-Addaptive"])
    plt.title(title)
    #plt.show()
    plt.savefig("/home/hrmoradi/PycharmProjects/PythonProjects/SchedulerEmulator/output/"+clusterString[pointer] +"-bid.png")
    plt.clf()
