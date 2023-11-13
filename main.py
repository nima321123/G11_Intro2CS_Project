import time
from scheduler import *
from task1 import *
from task2 import *
from task3 import *


scheduler = Scheduler()
scheduler.SCH_Init()

task1 = Task1()
task2 = Task2()
task3 = Task3()


scheduler.SCH_Add_Task(task1.update_result_text, 0,0)
scheduler.SCH_Add_Task(task2.analyze_weather("d:\Downloads\VGU\Intro to CS\RTOS\BerlinGermany.csv"), 20000 ,0)
scheduler.SCH_Add_Task(task3.Task1_Run, 40000)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)
