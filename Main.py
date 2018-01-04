import SchedulerEmulator.Settings as Set
import copy
from SchedulerEmulator.JobCreator import ClassJobCreator as CJ
from SchedulerEmulator.Scheduler import ClassSchduler as CS

#print("\n\n***Main:createJobList")
JobCreator= CJ()
jobList=JobCreator.MainJobCreator()

#print("\n\n***Main:Emulate TSRA-MEO")
EmulateMEO =CS()
EmulateMEO.MainScheduler(jobList,Set.resources)

#print("\n\n***Main:Emulate TSRA-First")
Set.firstOptionOnly=True
Set.MEO=False
EmulateFirst=CS()
EmulateFirst.MainScheduler(jobList,Set.resources)

#print("\n\n***Main:Emulate TSRA-last")
Set.firstOptionOnly=False
Set.MEO=False
Set.lastOption=True
EmulateLast=CS()
EmulateLast.MainScheduler(jobList,Set.resources)
