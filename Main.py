import SchedulerEmulator.Settings as Set
import copy
from SchedulerEmulator.JobCreator import ClassJobCreator as CJ
from SchedulerEmulator.Scheduler import ClassSchduler as CS

#print("\n\n***Main:createJobList")
JobCreator= CJ()
jobList=JobCreator.MainJobCreator()

print("\n\nJob Writer or Reader")
###################################################

#print("\n\n***Main:Emulate TSRA-MEO")
EmulateMEO =CS()
copyJoblist=copy.deepcopy(jobList)
EmulateMEO.MainScheduler(copyJoblist)

#print("\n\n***Main:Emulate TSRA-First")
Set.firstOptionOnly=True
Set.MEO=False
EmulateFirst=CS()
copyJoblist=copy.deepcopy(jobList)
EmulateFirst.MainScheduler(copyJoblist)

