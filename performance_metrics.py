from os import system
import psutil, threading, hashlib

def ratio(before, after):
    return 100 * (1 - (after / before))

# def integrity(before, after):
#     md5_before = None
#     md5_after = None
#     # Open,close, read file and calculate MD5 on its contents
#     with open(before) as file_to_check:
#         # read contents of the file
#         data = file_to_check.read()
#         # pipe contents of the file through
#         md5_before = hashlib.md5(data.encode("utf8")).hexdigest()

#     with open(after) as file_to_check:
#         # read contents of the file
#         data = file_to_check.read()
#         # pipe contents of the file through
#         md5_after = hashlib.md5(data.encode("utf8")).hexdigest()

#     # Finally compare original MD5 with freshly calculated
#     if md5_before == md5_after:
#         print("MD5 verified.")
#     else:
#         print("MD5 verification failed!.")

def integrity(filename):
    md5 = hashlib.md5()
    # Open,close, read file and calculate MD5 on its contents
    with open(filename, "rb") as file_to_check:
        # read contents of the file
        for block in iter(lambda: file_to_check.read(4096), b''):
            md5.update(block)

    return md5.hexdigest()

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
