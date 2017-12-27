import random

debug=False

"""jobCreator Constants"""
capacity = 20
loadMin = 0.80
loadMax= 1.4
NumberOfTimeInterval=10
timeInterval=10
maxRunTime=1.5 #
vmCores = [2,4,8,16]
deadLineMin =2 # to 2+1
maxVMsize =16
maxVMoptions=3
minScaleFactor=1.5
maxScaleFactor=2
switchCaseDic={ 2: random.randint(1,2), 4: random.randint(1,2), 8: 1, 16: 1, }


"""Scheduler Constants"""
#resources = "~input/resources.txt"
resources = [[4,8,0,0,1],[16,64,0,0,2]] #core,mem,0,0,id
duration=41 # duration of running the app
firstOptionOnly=False
MEO=True
sleepTime =0.1
bidDegree=10000



"""sampleJob #            [s,[[e1],[e2],[e3]],d,b,id],"""
#jobList = "~input/jobList.txt"
testJobListMEO=[   [0,[[1,2,21],[2,2,11],[4,2,7]],23,15,1],#26
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
testJobListFirst=[   [0,[[1,2,21],[2,2,11],[4,2,7]],23,5,1],#26
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
