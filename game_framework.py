

running = None
stack = []


def get_prev_state():
    try:
        return stack[-2]
    except:
        return None


def change_state(state):
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()
    stack.append(state)
    state.enter()


def push_state(state):
    global stack
    # if (len(stack) > 0):
    #     stack[-1].pause()
    stack.append(state)
    state.enter()


def pop_state():
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


# pree fill statck with previous states
def fill_states(*states):
    for state in states:
        stack.append(state)

import time
frame_time = 0.0

def run(start_state):
    global running, stack
    running = True

    # prepare previous states if any
    for state in stack:
        state.enter()
        state.pause()

    stack.append(start_state)
    stack[-1].enter()

    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        global frame_time
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time
        
    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].exit()
        stack.pop()

