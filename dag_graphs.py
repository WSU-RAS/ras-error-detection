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
        'P3': ['P3', 'W', 'G', 'S'],
        'G': ['P3', 'W', 'G', 'S'],
        'S': ['P3', 'W', 'G', 'S'],
        'W': ['W'],
        'Done': 'W',
        'label': subtaskName[5],
        'next': subtaskName[6]
    }
    task4 = {
        'P2': ['P2', 'W', 'P3'],
        'W': ['P2', 'W', 'P3'],
        'P3': task5,
        'label': subtaskName[4],
        'next': subtaskName[5]
    }
    task3 = {
        'P1': ['P1', 'W', 'P2'],
        'W': ['P1', 'W', 'P2'],
        'P2': task4,
        'label': subtaskName[3],
        'next': subtaskName[4]
    }
    task2 = {
        'S': ['S', 'W', 'G', 'P1'],
        'W': ['S', 'W', 'G', 'P1'],
        'G': ['S', 'W', 'G', 'P1'],
        'P1': task3,
        'label': subtaskName[2],
        'next': subtaskName[3]
    }
    task1 = {
        'W': ['W', 'S', 'G'],
        'G': ['W', 'S', 'G'],
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
        'U': ['U', 'L', 'K', 'D', 'DR'],
        'L': ['U', 'L', 'K', 'D', 'DR'],
        'K': ['U', 'L', 'K', 'D', 'DR'],
        'D': ['U', 'L', 'K', 'D', 'DR'],
        'DR': ['Done'],
        'Done': 'DR',
        'label': subtaskName[4],
        'next': subtaskName[5]
    }
    task3 = {
        'U': ['U', 'L', 'K', 'D'],
        'L': ['U', 'L', 'K', 'D'],
        'K': ['U', 'L', 'K', 'D'],
        'D': task4,
        'label': subtaskName[3],
        'next': subtaskName[4]
    }
    task2 = {
        'U': ['U', 'L', 'K'],
        'L': ['U', 'L', 'K'],
        'K': task3,
        'label': subtaskName[2],
        'next': subtaskName[3]
    }
    task1 = {
        'U': ['U', 'L'],
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
        'F': ['F', 'M', 'C', 'S', 'G'],
        'C': ['F', 'M', 'C', 'S', 'G'],
        'S': ['F', 'M', 'C', 'S', 'G'],
        'G': ['F', 'M', 'C', 'S', 'G'],
        'M': ['Done'],
        'Done': 'M',
        'label': subtaskName[9],
        'next': subtaskName[10]
    }
    task8 = {
        'F': ['F', 'M', 'C', 'CH', 'S', 'G'],
        'M': ['F', 'M', 'C', 'CH', 'S', 'G'],
        'C': ['F', 'M', 'C', 'CH', 'S', 'G'],
        'CH': ['F', 'M', 'C', 'CH', 'S', 'G'],
        'S': ['F', 'M', 'C', 'CH', 'S', 'G'],
        'G': task9,
        'label': subtaskName[8],
        'next': subtaskName[9]
    }
    task7 = {
        'M': ['M', 'C'],
        'C': task8,
        'label': subtaskName[7],
        'next': subtaskName[8]
    }
    task6 = {
        'F': ['F', 'M'],
        'M': task7,
        'label': subtaskName[6],
        'next': subtaskName[7]
    }
    task5 = {
        'M': ['M', 'CH', 'F'],
        'CH': ['M', 'CH', 'F'],
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
        'F': ['F', 'C', 'S', 'M'],
        'C': ['F', 'C', 'S', 'M'],
        'S': ['F', 'C', 'S', 'M'],
        'M': task4,
        'label': subtaskName[3],
        'next': subtaskName[4]
    }
    task2 = {
        'F': ['F', 'C', 'S'],
        'C': ['F', 'C', 'S'],
        'S': task3,
        'label': subtaskName[2],
        'next': subtaskName[3]
    }
    task1 = {
        'F': ['F', 'C'],
        'C': task2,
        'label': subtaskName[1],
        'next': subtaskName[2]
    }
    taskStart = {
        'F': task1,
        'label': subtaskName[0],
        'next': subtaskName[1]
    }
    # task1_2 = {
    #     'C': ['F', 'C'],
    #     'F': task2,
    #     'label': subtaskName[0],
    #     'next': subtaskName[2]
    # }
    # task1_1 = {
    #     'F': ['F', 'C'],
    #     'C': task2,
    #     'label': subtaskName[1],
    #     'next': subtaskName[2]
    # }
    # taskStart = {
    #     'F': task1_1,
    #     'C': task1_2,
    #     'label': {'F': subtaskName[0], 'C': subtaskName[1]},
    #     'next': {'F': subtaskName[1], 'C': subtaskName[0]},
    #     'default_label': subtaskName[0]
    #     'default_next': subtaskName[1]
    # }


if __name__ == '__main__':
    w = WaterPlants()
    print(w.task1['W'])
    print(w.task1['S']['P1']['P2']['P3']['S']['Done'])

    wd = WalkDog()
    print(wd.task1['U'])
    print(wd.task1['L']['K']['D']['DR'])
