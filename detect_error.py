#!/usr/bin/env python3

from dag_graphs import WaterPlants, WalkDog, TakeMedication
from items import Items


def check_sequence(graph, seq=[], task_count=0, task_num=-1):
    if seq == []:
        return 0, False, graph['label'], False, graph['label']

    if seq[0] not in graph:
        return 0, False, graph['label'], False, graph['label']

    if len(seq) == 1:
        return 0, True, graph['label'], False, graph['next']

    return _check_sequence(graph[seq[0]], seq[1:], task_count+1, task_num-1, label=graph['label'])

def _check_sequence(graph, seq=[], task_count=0, task_num=-1, label=None):

    if seq[0] not in graph:
        return task_count+1, False, graph['label'], False, graph['label']

    if task_count == task_num and seq[0] == graph['Done']:
        return task_count, True, graph['label'], True, graph['next']

    if len(seq) == 1:
        if type(graph[seq[0]]) is dict:
            return task_count, True, graph['label'], False, graph['next']
        return task_count-1, True, label, False, graph['label']

    if type(graph[seq[0]]) is dict:
        return _check_sequence(graph[seq[0]], seq, task_count+1, task_num, graph['label'])

    return _check_sequence(graph, seq[1:], task_count, task_num, label)



if __name__ == '__main__':

    print(check_sequence(
        WaterPlants.taskStart,
        seq=['W', 'S', 'P1', 'P2', 'P3', 'S'],
        task_num=WaterPlants.numTasks))
    print(check_sequence(
        WaterPlants.taskStart,
        seq=['W', 'S', 'P1', 'P2', 'P3', 'S', 'W'],
        task_num=WaterPlants.numTasks))

    print(check_sequence(
        WalkDog.taskStart,
        seq=['U', 'U', 'U'],
        task_num=WalkDog.numTasks))
