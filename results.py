import matplotlib.pyplot as plt
import numpy as np

location = np.arange(8)
load=["70","80","90","100","110","120","130","140"]

discardedMEO = [0,0,4,9,15,22,27,27]
discardedFirst=[0,1,5,9,16,23,28,30]
discardedLast= [27,32,38,41,44,46,47,52]

bidMEO=[99,99,97,93,86,80,75,73]
bidFirst=[99,99,96,92,87,80,75,73]
bidLast=[77,70,63,58,55,51,48,46]

plt.bar(location-0.2,discardedLast, align="center",width=0.1, color="lightcoral")
plt.bar(location-0.1,discardedFirst, align="center",width=0.1, color="k")
plt.bar(location,discardedMEO, align="center",width=0.1, color="springgreen")
plt.xticks(location,load)
plt.yticks(np.arange(0,110,10))
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
