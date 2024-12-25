import random
import time

def fcfs_scheduling(processes):
    # n is the number of processes in the CPU
    n = len(processes)
    if n == 0:
        return 0, 0, 0, []
    # Sort processes by arrival time to make sure the process that arrives first is executed first
    processes.sort(key=lambda x: x[1])

    completion_times = [0] * n  # Time when each process finishes execution
    waiting_times = [0] * n     # Time in which process waits in the system before execution
    turnaround_times = [0] * n  # Total time spent in process from arrival time until execution
    response_times = [0] * n    # Time between arrival and the start of execution
    current_time = 0            # The start time in the CPU
    process_info = []           # List to store detailed information for each process

    for i in range(n):
        process_id, arrival_time, burst_time = processes[i]

        # Makes the current time the arrival time (CPU waits until the process arrives)
        if current_time < arrival_time:  # CPU is idle
            current_time = arrival_time

        start_time = current_time
        completion_times[i] = current_time + burst_time
        current_time = completion_times[i]

        waiting_times[i] = start_time - arrival_time
        turnaround_times[i] = completion_times[i] - arrival_time
        response_times[i] = start_time - arrival_time
        process_info.append({
            "process_id": process_id,
            "arrival_time": arrival_time,
            "burst_time": burst_time,
            "completion_time": completion_times[i],
            "waiting_time": waiting_times[i],
            "turnaround_time": turnaround_times[i],
            "response_time": response_times[i]
        })

    avg_waiting_time = sum(waiting_times) / n
    avg_turnaround_time = sum(turnaround_times) / n
    avg_response_time = sum(response_times) / n

    return avg_waiting_time, avg_turnaround_time, avg_response_time, process_info
def simulate_processes(steps=100):
    processes = []  
    total_spawned = 0
    total_killed = 0

    for step in range(1, steps + 1):
        #spawn a process
        if random.random() < 0.7: 
            pid = random.randint(1000000000000, 9999999999999)
            arrival_time = step
            burst_time = random.randint(5, 50)
            processes.append((pid, arrival_time, burst_time))
            total_spawned += 1
            print(f"Process spawned: Process ID: {pid} | Arrival Time: {arrival_time} | Burst Time: {burst_time}")

        # kill a process
        if processes and random.random() < 0.3:  
            process_to_kill = random.choice(processes)
            processes.remove(process_to_kill)
            total_killed += 1
            print(f"Process killed: Process ID: {process_to_kill[0]}")

        if step % 5 == 0 and processes:
            avg_wait, avg_turnaround, avg_response, process_info = fcfs_scheduling(processes)
            print("\n--- FCFS Scheduling Summary ---")
            print(f"Average Waiting Time: {avg_wait:.2f}")
            print(f"Average Turnaround Time: {avg_turnaround:.2f}")
            print(f"Average Response Time: {avg_response:.2f}")
            print("Process Details:")
            for p in process_info:
                print(p)
            print("--------------------------------\n")

        time.sleep(0.5)
simulate_processes(10)