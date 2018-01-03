
from pylab import *
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.cbook as cbook
from matplotlib.pyplot import figure, xlabel, ylabel, title, show
"""
y = list(range(32,0,-1))
print(y)
logY = np.log2(y)
logYr = np.sort(logY)
print(logY)
print(logYr)
p190 = np.float_power(1.80,logY)
print(p190)
p180 = np.float_power(1.90,logY)
print(p180)
plt.plot(logYr ,p190)
plt.plot(logYr ,p180)
plt.xlim(0, 32)
plt.ylim(0, 32)
plt.autoscale(False)
show()


plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.5)
#plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2)
#plt.xticks(range(40))
#plt.yticks(range(40))
plt.legend(['1.80', '1.90'])
"""
##########################################################################

xred=[10,7,5,3.5,3]
xblue=[10,6,3.5,2,1.25]
y=[2,4,8,16,24]
plt.plot(np.sort(xblue),np.sort(y)[::-1] )
plt.plot(np.sort(xred),np.sort(y)[::-1] )

xred2=[x/3 for x in xred]
xblue2=[x/3 for x in xblue]
y=[x for x in y]
plt.plot(np.sort(xblue2),np.sort(y)[::-1] )
plt.plot(np.sort(xred2),np.sort(y)[::-1] )

#plt.plot(np.sort(xblue)-5,np.sort(y)[::-1]*2 )
#plt.plot(np.sort(xred)-5,np.sort(y)[::-1]*2 )

#x=[5,3,1.75,1,0.75]
#y=[2,4,8,16,24]
#p190 = np.float_power(1.90,np.log2(y))
#plt.plot(np.sort(x),np.sort(p190)[::-1])
#p170 = np.float_power(1.70,np.log2(y))
#plt.plot(np.sort(x),np.sort(p170)[::-1])



plt.xlim(0,10)
plt.ylim(0,26)
plt.autoscale(False)
plt.grid(b=True, which='major', color='k', linestyle=':', alpha=0.5)

plt.xticks(np.sort(xred+xblue+xred2+xblue2), rotation=90)
plt.yticks(np.sort(y))
show()


plt.xlim(0, 9)
plt.ylim(0, 25)
plt.autoscale(False)
plt.grid(b=True, which='major', color='k', linestyle=':', alpha=0.5)

plt.xticks(range(14))
plt.yticks(range(25))

from pylab import *
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.cbook as cbook
from matplotlib.pyplot import figure, xlabel, ylabel, title, show
"""
y = list(range(32,0,-1))
print(y)
logY = np.log2(y)
logYr = np.sort(logY)
print(logY)
print(logYr)
p190 = np.float_power(1.80,logY)
print(p190)
p180 = np.float_power(1.90,logY)
print(p180)
plt.plot(logYr ,p190)
plt.plot(logYr ,p180)
plt.xlim(0, 32)
plt.ylim(0, 32)
plt.autoscale(False)
show()


plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.5)
#plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2)
#plt.xticks(range(40))
#plt.yticks(range(40))
plt.legend(['1.80', '1.90'])
"""
##########################################################################

xred=[10,7,5,3.5,3]
xblue=[10,6,3.5,2,1.25]
y=[2,4,8,16,24]
plt.plot(np.sort(xblue),np.sort(y)[::-1] )
plt.plot(np.sort(xred),np.sort(y)[::-1] )

xred2=[x/3 for x in xred]
xblue2=[x/3 for x in xblue]
y=[x for x in y]
plt.plot(np.sort(xblue2),np.sort(y)[::-1] )
plt.plot(np.sort(xred2),np.sort(y)[::-1] )

#plt.plot(np.sort(xblue)-5,np.sort(y)[::-1]*2 )
#plt.plot(np.sort(xred)-5,np.sort(y)[::-1]*2 )

#x=[5,3,1.75,1,0.75]
#y=[2,4,8,16,24]
#p190 = np.float_power(1.90,np.log2(y))
#plt.plot(np.sort(x),np.sort(p190)[::-1])
#p170 = np.float_power(1.70,np.log2(y))
#plt.plot(np.sort(x),np.sort(p170)[::-1])



plt.xlim(0,10)
plt.ylim(0,26)
plt.autoscale(False)
plt.grid(b=True, which='major', color='k', linestyle=':', alpha=0.5)

plt.xticks(np.sort(xred+xblue+xred2+xblue2), rotation=90)
plt.yticks(np.sort(y))
show()


plt.xlim(0, 9)
plt.ylim(0, 25)
plt.autoscale(False)
plt.grid(b=True, which='major', color='k', linestyle=':', alpha=0.5)

plt.xticks(range(14))
plt.yticks(range(25))
#show()

