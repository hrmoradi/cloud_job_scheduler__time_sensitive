import random

winAdd="C:\\Users\\Admin\\PycharmProjects\\PythonProjects\\SchedulerEmulator\\output\\"
linuxAdd="/home/hrmoradi/PycharmProjects/PythonProjects/SchedulerEmulator/output/"
add=linuxAdd

tx=True
fx=False

debugLevel1=fx
debugLevel2=fx
debug=fx
debugDetail=fx
debugTimer=fx
sleepTime =0.0


""" Main Constants"""
numberOfIteration = 1



"""jobCreator Constants"""
randJob=tx
tableJob= fx

capacity = 80 ########################################################
capMem= 256
fluctuation= 0.40 ####################################################
avgSysLoad= 0.8
loadInc=10

NumberOfTimeInterval=1000 ##############################################
eachTimeInterval=10
maxRunTime=140 ###########################################################
minRuntime=70
#vmCores = [2,4,8,16] ###################################################
deadLineMin =2 #########################################################
deadLineMax=4 # was 6 for results of friday
maxVMoptions=4 #########################################################
minScaleFactor=1.4 #####################################################
maxScaleFactor=2
#switchCaseDic={ 2: random.randint(1,2), 4: random.randint(1,2), 8: 1, 16: 1, }



""" Scheduler Constants """
bidDegree=100000
#resources = "~input/resources.txt"
SmallCluster = [[4,8,0,0,1],[4,8,0,0,2],[2,4,0,0,3],[2,4,0,0,4]]
MediumCluster = [[8,32,0,0,1],[8,32,0,0,2],[4,8,0,0,3],[4,8,0,0,4],[2,4,0,0,5],[2,4,0,0,6],[2,4,0,0,7],[2,4,0,0,8]]
LargeCluster = [[16,64,0,0,1],[16,64,0,0,2],[8,32,0,0,3],[8,32,0,0,4],[4,8,0,0,5],[4,8,0,0,6],[4,8,0,0,7],[4,8,0,0,8],[2,4,0,0,9],[2,4,0,0,10],[2,4,0,0,11],[2,4,0,0,12],[2,4,0,0,13],[2,4,0,0,14],[2,4,0,0,15],[2,4,0,0,16]]
#LargeCluster = [[32,128,0,0,1],[32,128,0,0,2],[32,128,0,0,3],[32,128,0,0,4],[32,128,0,0,5],[32,128,0,0,6],[32,128,0,0,7],[32,128,0,0,8]]
resources=LargeCluster
duration=NumberOfTimeInterval*eachTimeInterval+eachTimeInterval ##################################################### additional for last time jobs dead
MEO=True
firstOptionOnly=False
lastOption=False
greedy=False



""" sample test Job """  #[s,[[e1],[#vm,#core,time,mem],[e3]],d,b,id],
#jobList = "~input/jobList.txt"
testMEO=[   [0,[[1,2,21],[2,2,11],[4,2,7]],23,15,1],#26
            [0,[[2,2,27],[4,2,15]],29,10,2],#29
            [0,[[1,4,20],[2,4,11],[4,4,6]],24, 28,3],
            [10, [[1,4,7], [2,4,4], [4,4,3]], 10, 4,4],
            [10, [[1,8,9], [2,8,5]], 14, 1,5],
            [10, [[1,2,17], [2,2,10]], 27, 14,6],
            [20, [[1,4,15], [2,4,11]], 16, 6,7],
            [20, [[2, 2, 19], [2, 8, 7]], 22, 8,8],
            [20, [[1, 4, 20], [2, 4, 12]], 24, 9,9],
            [20, [[4, 2, 8], [4, 4, 5]], 21, 5,10],
            [20, [[2, 4, 10], [1, 4, 6]], 16, 4,11],   #do no takeplace in 20 let id 9 scale
        ]
testFirst=[   [0,[[1,2,21],[2,2,11],[4,2,7]],23,5,1],#26
            [0,[[2,2,27],[4,2,15]],29,10,2],#29
            [0,[[1,4,20],[2,4,11],[4,4,6]],24, 8,3],
            [10, [[1,4,7], [2,4,4], [4,4,3]], 10, 4,4],
            [10, [[1,8,9], [2,8,5]], 14, 8,5],
            [10, [[1,2,17], [2,2,10]], 27, 4,6],
            [20, [[1,4,15], [2,4,11]], 16, 6,7],
            [20, [[2, 2, 19], [2, 8, 7]], 22, 8,8],
            [20, [[1, 4, 20], [2, 4, 12]], 24, 9,9],
            [20, [[4, 2, 8], [4, 4, 5]], 21, 5,10],
            [20, [[1, 4, 10], [2, 4, 6]], 16, 4,11],
        ]
