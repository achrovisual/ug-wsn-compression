from os import system
import psutil, threading

def ratio(before, after):
    return 100 * (1 - (after / before))

def performance_metrics():
    global running
    global cpu_usage
    global memory_usage
    cpu_usage = []
    memory_usage = []

    running = True

    current_process = psutil.Process()

    # start loop
    while running:
        cpu_usage.append(current_process.cpu_percent(interval = 1))
        memory_usage.append(current_process.memory_percent())

def performance_metrics_system_wide():
    global running
    global cpu_usage
    global memory_usage
    cpu_usage = []
    memory_usage = []

    running = True
    before_cpu_usage = psutil.cpu_percent()
    before_memory_usage = psutil.virtual_memory().percent
    # start loop
    while running:
        cpu_usage.append(abs(psutil.cpu_percent(interval = 1)-before_cpu_usage))
        memory_usage.append(abs(psutil.virtual_memory().percent - before_memory_usage))

def start():
    global t

    # create thread and start it
    t = threading.Thread(target = performance_metrics)
    t.start()

def start_system_wide():
    global t

    # create thread and start it
    t = threading.Thread(target = performance_metrics_system_wide)
    t.start()

def stop():
    global running
    global cpu_usage
    global memory_usage
    global t
    result = []
    result.append(cpu_usage)
    result.append(memory_usage)

    # use `running` to stop loop in thread so thread will end
    running = False

    # wait for thread's end
    t.join()

    return result
