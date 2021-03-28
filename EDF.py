import random as r
from math import gcd
import sys
from os import system, name

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
clear()
#Reading Task Set
def Task_Set():
    Temp=[]
    Task_Set=[]
    Tasks=[]
    #Reading file to a list
    data = open('Tasks.txt','r')
    data.seek(20)#Doesn't consider first line of file
    tasks= data.readlines()
    for line in tasks:
        stripped_task=line.strip('\n')
        Temp.append(stripped_task)
    #split item
    for i in Temp:
        li = list(i.split(","))
        Tasks.append( li)
    #Convert every item in task set to integer
    for task in Tasks:
        Task_Set.append(list(map(int, task)))
    # Add Task ID for Each Task
    i=0
    while (i < len(Task_Set)):
           Task_Set[i].insert(0,i+1)
           Task_Set[i].append(int(0))
           i+=1
    return Task_Set
tasks= Task_Set()
n=len(tasks)
#print(Len_Task_Set)
print("TID\tC\tD\tP\tRT")
for i in tasks:
    print("")
    for j in i:
        print(j, end = '\t')

print("\n")


#Calculating Hyper Perios as LCM
def LCM(Task_Set):

    P=[]
    for i in range(n):
        P.append(tasks[i][3])
    lcm = P[0]
    for i in P[1:]:
        lcm =int( lcm*i/gcd(lcm, i))
    return lcm
lcm=LCM(Task_Set)
print("Hyper Period is: ",lcm,)

def utilization(Task_Set,Len_Task_Set):
    u=0
    for i in range (n):
        u+=float(Task_Set[i][1]/Task_Set[i][3])
    return u
util=utilization(tasks,n)
print('utilization of task set is %s\n'%round(util,2))

def TimeLeft(Task_Set,Len_Task_Set):
    time_left=[]
    for i in range (Len_Task_Set):
        if Task_Set[i][4]==0:
            time_left.append(Task_Set[i][1])
        else:
             time_left.append(int(0))
    return time_left
timeLeft=TimeLeft(tasks,n)

def array_sort(instances,index=1):
    for i in range(len(instances)):
        tmp = instances[i].copy()
        k = i
        while k > 0 and tmp[index] < instances[k-1][index]:
            instances[k] = instances[k - 1].copy()
            k -= 1
        instances[k] = tmp.copy()
    return instances

def EDF(tasks,n,lcm,util):
    #Jobs=Jobs_Set(Task_Set,Len_Task_Set)

    i=0
    instances=[]
    for i in range(n):
        j=1
        while 1:
            if j*tasks[i][2]<=lcm:
                instances.append([tasks[i],j*tasks[i][2]])
                j+=1
            else:
                break

        #for i in range(len(instances)):
        #    print(instances[i])


    for i in range(len(instances)):
        tmp = instances[i].copy()
        k = i
        while k > 0 and tmp[1] < instances[k-1][1]:
            instances[k] = instances[k - 1].copy()
            k -= 1
        instances[k] = tmp.copy()


    timeLine=[]
    time=0

    #current_job=[]
    while(time <lcm):
        #print(time)
        if util <=1:

            while time<lcm:
                for i in range(n):
                    if time>1 and ((time%tasks[i][2]==0 and time>tasks[i][4]) or
                    time==tasks[i][4]):
                        #print("true ", end='')
                        timeLeft[i]=tasks[i][1]
                anyrun=0
                for j in range(len(instances)):
                    #print("YESSS %s"%timeLeft[instances[j][1][0]])
                    if j==0 and timeLeft[instances[j][0][0]-1]>0:
                        timeLine.append(instances[j][0][0])
                        timeLeft[instances[j][0][0]-1]-=1
                        anyrun=1
                        if timeLeft[instances[j][0][0]-1]==0:
                            instances.pop(j)
                        #print("[",time,"]",instances[j][0][0],timeLeft[instances[j][0][0]-1], time )
                        break

                    elif j>0 and instances[j][1]==instances[0][1]:
                        if timeLeft[instances[j][0][0]-1]>0:
                            tmp=instances[j].copy()
                            instances[j]=instances[0].copy()
                            instances[0]=tmp.copy()
                            time-=1
                            anyrun=1
                            break
                    elif j>0 and timeLeft[instances[j][0][0]-1]>0:
                        timeLine.append(instances[j][0][0])
                        timeLeft[instances[j][0][0]-1]-=1
                        anyrun=1
                        if timeLeft[instances[j][0][0]-1]==0:
                            instances.pop(j)
                        #print("[",time,"]",instances[j][0][0],timeLeft[instances[j][0][0]-1], time )
                        break


                if anyrun==0:
                    timeLine.append(0)

                time+=1

            mn=0
            mx=0
            print('******************************************')
            print("* Start Time\t","End Time\t", "Task ID *")
            for i in range(lcm):
                if i>0 and timeLine[i]!=timeLine[i-1]:
                    mx=i
                    print("*",mn,"\t\t",mx,"\t\t", "["+str(timeLine[i-1])+"]\t","*")

                    mn=i
                if i==lcm-1:
                    mx=lcm
                    print("*",mn,"\t\t",mx,"\t\t", "["+str(timeLine[i])+"]\t","*")
            print('******************************************')
        else:
            print('Task set is not feasible.(Utilization Must be <=1.)')
            break
EDF(tasks,n,lcm,util)
