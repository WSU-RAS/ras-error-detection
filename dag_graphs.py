#!/usr/bin/env python3
'''
W   watercan                F   food/snack
S   sink                    C   cup
P1  windowsill plant        M   medication
P2  coffee table plant      CH  chair
P3  side table plant        G   garbage
U   umbrella
L   leash
K   keys
D   dog
DR  door
'''

class WaterPlants(object):
    subtaskName = {
        0: 'Retrieve Water can',
        1: 'Fill Water can',
        2: 'Water Windowsill plant',
        3: 'Water Coffee table plant',
        4: 'Water Side table plant',
        5: 'Return Water can',
        6: 'Completed'
    }
    numTasks = 6
    task5 = {
        'P3': None,
        'G': None,
        'S': None,
        'W': None,
        'Done': 'W',
        'label': subtaskName[5],
        'next': subtaskName[6]
    }
    task4 = {
        'P2': None,
        'W': None,
        'P3': task5,
        'label': subtaskName[4],
        'next': subtaskName[5]
    }
    task3 = {
        'P1': None,
        'W': None,
        'P2': task4,
        'label': subtaskName[3],
        'next': subtaskName[4]
    }
    task2 = {
        'S': None,
        'W': None,
        'G': None,
        'P1': task3,
        'label': subtaskName[2],
        'next': subtaskName[3]
    }
    task1 = {
        'W': None,
        'G': None,
        'S': task2,
        'label': subtaskName[1],
        'next': subtaskName[2]
    }
    taskStart = {
        'W': task1,
        'label': subtaskName[0],
        'next': subtaskName[1]
    }

class WalkDog(object):
    subtaskName = {
        0: 'Retrieve Umbrella',
        1: 'Retrieve Leash',
        2: 'Retrieve Keys',
        3: 'Leash Dog',
        4: 'Exit',
        5: 'Completed'
    }
    numTasks = 5
    task4 = {
        'U': None,
        'L': None,
        'K': None,
        'D': None,
        'DR': None,
        'Done': 'DR',
        'label': subtaskName[4],
        'next': subtaskName[5]
    }
    task3 = {
        'U': None,
        'L': None,
        'K': None,
        'D': task4,
        'label': subtaskName[3],
        'next': subtaskName[4]
    }
    task2 = {
        'U': None,
        'L': None,
        'K': task3,
        'label': subtaskName[2],
        'next': subtaskName[3]
    }
    task1 = {
        'U': None,
        'L': task2,
        'label': subtaskName[1],
        'next': subtaskName[2]
    }
    taskStart = {
        'U': task1,
        'label': subtaskName[0],
        'next': subtaskName[1]
    }

class TakeMedication(object):
    subtaskName = {
        0: 'Retrieve Food',
        1: 'Retrieve Cup',
        2: 'Fill Cup',
        3: 'Retrieve Medication',
        4: 'Sit Chair',
        5: 'Eat Food',
        6: 'Take Medication',
        7: 'Drink Water',
        8: 'Throw Garbage',
        9: 'Return Medication',
        10: 'Completed'
    }
    numTasks = 10
    task9 = {
        'F': None,
        'C': None,
        'S': None,
        'G': None,
        'M': None,
        'Done': 'M',
        'label': subtaskName[9],
        'next': subtaskName[10]
    }
    task8 = {
        'F': None,
        'M': None,
        'C': None,
        'CH': None,
        'S': None,
        'G': task9,
        'label': subtaskName[8],
        'next': subtaskName[9]
    }
    task7 = {
        'M': None,
        'C': task8,
        'label': subtaskName[7],
        'next': subtaskName[8]
    }
    task6 = {
        'F': None,
        'M': task7,
        'label': subtaskName[6],
        'next': subtaskName[7]
    }
    task5 = {
        'M': None,
        'CH': None,
        'F': task6,
        'label': subtaskName[5],
        'next': subtaskName[6]
    }
    task4 = {
        'M': ['M', 'CH'],
        'CH': task5,
        'label': subtaskName[4],
        'next': subtaskName[5]
    }
    task3 = {
        'F': None,
        'C': None,
        'S': None,
        'M': task4,
        'label': subtaskName[3],
        'next': subtaskName[4]
    }
    task2 = {
        'F': None,
        'C': None,
        'S': task3,
        'label': subtaskName[2],
        'next': subtaskName[3]
    }
    ''' cup->sink->food '''
    task2_1 = {
        'C': None,
        'S': None,
        'F': task3,
        'label': subtaskName[0],
        'next': subtaskName[3]
    }
    ''' cup->sink '''
    task1_2_2 = {
        'C': None,
        'S': task2_1,
        'label': subtaskName[2],
        'next': subtaskName[0]
    }
    ''' cup->food '''
    task1_2_1 = {
        'C': None,
        'F': task2,
        'label': subtaskName[0],
        'next': subtaskName[2]
    }
    ''' cup->Y '''
    task1_2 = {
        'Y': [task1_2_1, task1_2_2]
        # 'C': None,
        # 'F': task2,
        # 'label': subtaskName[0],
        # 'next': subtaskName[2]
    }
    ''' food->cup '''
    task1_1 = {
        'F': None,
        'C': task2,
        'label': subtaskName[1],
        'next': subtaskName[2]
    }
    ''' starts with retrieving cup '''
    taskStart_2 = {
        'C': task1_2,
        'label': subtaskName[1],
        'next': subtaskName[0]
    }
    ''' starts with retrieving food '''
    taskStart_1 = {
        'F': task1_1,
        'label': subtaskName[0],
        'next': subtaskName[1]
    }
    ''' start->Y '''
    taskStart = {
        'Y': [taskStart_1, taskStart_2], # Y intersection
    }


if __name__ == '__main__':
    w = WaterPlants()
    print(w.task1['W'])
    print(w.task1['S']['P1']['P2']['P3']['S']['Done'])

    wd = WalkDog()
    print(wd.task1['U'])
    print(wd.task1['L']['K']['D']['DR'])
