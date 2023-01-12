from email import policy
import random,argparse,sys,subprocess,os
parser = argparse.ArgumentParser()
import numpy as np
seeds = 100
random_seeds =np.zeros(seeds)
for i in range(seeds):
     random_seeds[i] = i
random_seeds = (random_seeds).astype(int)
task = "T2"
counter = 0
task2_avg = np.zeros(seeds) + 240
FAILS = 0 
failing_seeds = []
def verifyOutput(cmd_output, task, counter):

        output = cmd_output.split("\n")        
        est = [i.split() for i in output if i != '']
        mistakeFlag = False
        roadFlag = True
        # Check 1: Checking the number of lines printed
        # if not len(est) == 10:
        #     mistakeFlag = True
        #     print("\n", "*"*10, "Mistake: Exact number of lines in the standard output should be", 10, "but has", len(est), "*"*10)
            
        # Check 2: Each line should have only two values
        # for i in range(len(est)):
        #     if not len(est[i])==2:
        #         mistakeFlag = True
        #         print("\n", "*"*10, "Mistake: On each line you should print only road status, time taken for an episode", "*"*10)
        #         break
        
        # if not mistakeFlag:
        #     print("ALL CHECKS PASSED!")
        # else:
        #     print("You haven't printed output in the correct format.")
            
        avg_time = 0
        
        for i in range(2,len(est)):

            road_status = est[i][0]
            time_taken = int(est[i][1])
            avg_time += time_taken

            if road_status == 'False':
                flag_ok = 1
                roadFlag = False
                print('Car does not reach the road')

            if time_taken >= 1000:
                flag_ok = 1
                roadFlag = False
                print('Car exceeds time limit')

        avg_time = avg_time/len(est)

        if True:

            task2_time = task2_avg[counter]

            if avg_time < 1.1*task2_time:
                time_success = True

            else:
                # print('Your car is not efficient enough')
                time_success = False

        return roadFlag, time_success
        
for seed in random_seeds:
    
        
    cmd_planner = "python", "run_simulator.py", "--task", str(task), "--random_seed", str(seed), "--frames_per_sec", str(20000)
    
    print('Test case', str(counter))
    cmd_output = subprocess.check_output(cmd_planner, universal_newlines=True)
    roadFlag, time_success = verifyOutput(cmd_output, task, counter-1)

    if time_success and roadFlag:
        print("PASSED")
    else:
        print("FAIL")
        failing_seeds.append(seed)
        FAILS +=1

    
    counter += 1
if(FAILS > 0):
    print("Failed testcases:" + ' ' + str(FAILS))
    print("List of failing testcases:")
    print(failing_seeds)
else:
    print("Perfection has been achieved")

