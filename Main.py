import SchedulerEmulator.Settings as Set
import copy
from SchedulerEmulator.JobCreator import ClassJobCreator as CJ
from SchedulerEmulator.Scheduler import ClassSchduler as CS

#print("\n\n***Main:createJobList")
JobCreator= CJ()
jobList=JobCreator.MainJobCreator()

#print("\n\n***Main:Emulate TSRA-MEO")
Set.resources=copy.deepcopy(Set.resourcesMain)
EmulateMEO =CS()
copyJoblist=copy.deepcopy(jobList)
EmulateMEO.MainScheduler(copyJoblist)

#print("\n\n***Main:Emulate TSRA-First")
Set.firstOptionOnly=True
Set.MEO=False
Set.resources=copy.deepcopy(Set.resourcesMain)
EmulateFirst=CS()
copyJoblist=copy.deepcopy(jobList)
EmulateFirst.MainScheduler(copyJoblist)

#print("\n\n***Main:Emulate TSRA-last")
Set.firstOptionOnly=False
Set.MEO=False
Set.lastOption=True
Set.resources=copy.deepcopy(Set.resourcesMain)
EmulateLast=CS()
copyJoblist=copy.deepcopy(jobList)
EmulateLast.MainScheduler(copyJoblist)
