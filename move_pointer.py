#!/usr/bin/env python3
from ddtrace import tracer

@tracer.wrap(resource="move_pointer")
def move_pointer():
    import pyautogui
    x, y = pyautogui.position()
    pyautogui.moveTo(x + 1, y)

move_pointer()
