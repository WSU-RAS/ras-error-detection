#!/usr/bin/env python3

from ras_error_detector import check_sequence
from ras_error_detector.lib import WaterPlants, WalkDog, TakeMedication


def test_water_plants():
    result = check_sequence(
        WaterPlants.taskStart,
        seq=['W', 'S', 'P1', 'P2', 'P3', 'S'],
        task_num=WaterPlants.numTasks
    )
    print(result)
    assert result == (
        5, True, WaterPlants.subtaskName[5],
        False, WaterPlants.subtaskName[6]
    )

    result = check_sequence(
        WaterPlants.taskStart,
        seq=['W', 'S', 'P1', 'P2', 'P3', 'S', 'W'],
        task_num=WaterPlants.numTasks
    )
    print(result)
    assert result == (
        6, True, WaterPlants.subtaskName[6],
        True, WaterPlants.subtaskName[7]
    )

def test_walk_dog():
    result = check_sequence(
        WalkDog.taskStart,
        seq=['U', 'U', 'U'],
        task_num=WalkDog.numTasks
    )
    print(result)
    assert result == (
        0, True, WalkDog.subtaskName[0],
        False, WalkDog.subtaskName[1]
    )

def test_take_medication():
    result = check_sequence(
        TakeMedication.taskStart,
        seq=['F', 'F', 'C', 'C', 'F', 'F', 'C', 'F',
             'S', 'S', 'F', 'C', 'C', 'C', 'F', 'F',
             'C', 'C', 'M', 'CH', 'CH', 'C', 'F', 'F',
             'F', 'M', 'M', 'C', 'C', 'C', 'CH', 'C',
             'CH', 'M', 'F', 'C', 'C', 'M', 'F', 'M',
             'F', 'M', 'C', 'F', 'F', 'S', 'C', 'C',
             'F', 'M', 'M', 'F', 'C', 'M', 'C', 'C',
             'G', 'M', 'G', 'M'],
        task_num=TakeMedication.numTasks)
    print(result)
    assert result == (
        11, False, TakeMedication.subtaskName[11],
        False, TakeMedication.subtaskName[11]
    )
