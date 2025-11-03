import os

# Process class to hold the process information
class Process:
    def __init__(self, name, arrival_time, burst_time, priority=0):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None
        self.priority = priority
        self.start_time = None  # Add this to track when a process starts executing


def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    gantt_chart = []
    
    for process in processes:
        if time < process.arrival_time:
            gantt_chart.append(('ID', time, process.arrival_time))
            time = process.arrival_time
        
        # Set start time if it hasn't started yet
        if process.start_time is None:
            process.start_time = time
        
        process.completion_time = time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        gantt_chart.append((process.name, time, process.completion_time))
        time = process.completion_time

    return gantt_chart

def sjf_non_preemptive_scheduling(processes):
    # Sort processes by arrival time initially
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    gantt_chart = []
    ready_queue = []
    completed_processes = 0
    
    # List to track completed processes and their metrics
    n = len(processes)
    
    while completed_processes < n:
        # Add all processes that have arrived by the current time to the ready queue
        while processes and processes[0].arrival_time <= time:
            ready_queue.append(processes.pop(0))
        
        if ready_queue:
            # Sort the ready queue by burst time (shortest job first)
            ready_queue.sort(key=lambda p: p.burst_time)
            
            # Pick the process with the shortest burst time
            process = ready_queue.pop(0)
            
            # Set the start time if this is the first time the process runs
            if process.start_time is None:
                process.start_time = time

            # Execute the process until completion
            gantt_chart.append((process.name, time, time + process.burst_time))
            time += process.burst_time
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            completed_processes += 1
        else:
            # If no process is ready, increment time by 1
            gantt_chart.append(('ID', time, time + 1))
            time += 1
    
         # Now, let's merge consecutive tasks of the same process in the gantt_chart
    merged_gantt_chart = []
    for task in gantt_chart:
        if not merged_gantt_chart or merged_gantt_chart[-1][0] != task[0]:
            merged_gantt_chart.append([task[0], task[1], task[2]])  # Start new task
        else:
            merged_gantt_chart[-1][2] = task[2]  # Extend the last task

    return merged_gantt_chart

def sjf_preemptive_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)  # Sort processes by arrival time
    time = 0
    gantt_chart = []
    ready_queue = []
    remaining_processes = {p.name: p for p in processes}
    processes = sorted(processes, key=lambda x: x.arrival_time)

    while remaining_processes:
        # Add processes that have arrived by the current time to the ready queue
        while processes and processes[0].arrival_time <= time:
            ready_queue.append(processes.pop(0))

        if not ready_queue:
            gantt_chart.append(('ID', time, time + 1))
            time += 1
            continue

        # Sort the ready queue by the remaining burst time (shortest job first)
        ready_queue.sort(key=lambda p: p.remaining_time)

        # Pick the process with the shortest remaining time
        process = ready_queue.pop(0)

        # Set the start time if it's the first time the process runs
        if process.start_time is None:
            process.start_time = time

        # Execute the process for one unit of time (preemptive nature)
        gantt_chart.append((process.name, time, time + 1))
        time += 1
        process.remaining_time -= 1

        # If the process is completed, calculate its final metrics
        if process.remaining_time == 0:
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            del remaining_processes[process.name]
        
        # Re-sort the ready queue, including any newly arrived processes
        ready_queue = [p for p in remaining_processes.values() if p.arrival_time <= time]

        # Now, let's merge consecutive tasks of the same process in the gantt_chart
    merged_gantt_chart = []
    for task in gantt_chart:
        if not merged_gantt_chart or merged_gantt_chart[-1][0] != task[0]:
            merged_gantt_chart.append([task[0], task[1], task[2]])  # Start new task
        else:
            merged_gantt_chart[-1][2] = task[2]  # Extend the last task

    return merged_gantt_chart

def priority_preemptive_scheduling(processes, highprio):
    # Sort processes by arrival time first
    processes.sort(key=lambda p: p.arrival_time)

    time = 0
    gantt_chart = []
    ready_queue = []
    remaining_processes = {p.name: p for p in processes}
    processes = sorted(processes, key=lambda p: p.arrival_time)
    
    while remaining_processes:
        # Add processes that have arrived by the current time to the ready queue
        while processes and processes[0].arrival_time <= time:
            ready_queue.append(processes.pop(0))

        if not ready_queue:
            gantt_chart.append(('ID', time, time + 1))
            time += 1
            continue

        # Sort the ready queue by priority (higher priority = lower value)
        if highprio == 1:
            ready_queue.sort(key=lambda p: p.priority)  # Ascending order: Lower priority number is better
        else:
            ready_queue.sort(key=lambda p: p.priority, reverse=True)  # Descending order: Higher priority number is better

        # Pick the process with the highest priority (lowest priority number)
        process = ready_queue.pop(0)

        # Set the start time if it's the first time the process runs
        if process.start_time is None:
            process.start_time = time

        # Execute the process for one unit of time (preemptive nature)
        gantt_chart.append((process.name, time, time + 1))
        time += 1
        process.remaining_time -= 1

        # If the process is completed, calculate its final metrics
        if process.remaining_time == 0:
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            del remaining_processes[process.name]

        # Re-sort the ready queue, including any newly arrived processes
        ready_queue = [p for p in remaining_processes.values() if p.arrival_time <= time]

        # Now, let's merge consecutive tasks of the same process in the gantt_chart
    merged_gantt_chart = []
    for task in gantt_chart:
        if not merged_gantt_chart or merged_gantt_chart[-1][0] != task[0]:
            merged_gantt_chart.append([task[0], task[1], task[2]])  # Start new task
        else:
            merged_gantt_chart[-1][2] = task[2]  # Extend the last task

    return merged_gantt_chart

def priority_non_preemptive_scheduling(processes,highprio):
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    gantt_chart = []
    ready_queue = []
    remaining_processes = {p.name: p for p in processes}

    while remaining_processes:
        ready_queue = [p for p in remaining_processes.values() if p.arrival_time <= time]
        
        if ready_queue:
            if ready_queue:
                if highprio == 1:
                    ready_queue.sort(key=lambda x: x.priority)  # Sort by priority (lower value = higher priority)
                elif highprio == 2:
                    ready_queue.sort(key=lambda x: x.priority, reverse=True) # Sort by priority (higher value = higher priority)
            process = ready_queue.pop(0)  # Pop the first process
            
            # Set the start time if it's the first time the process runs
            if process.start_time is None:
                process.start_time = time
            
            gantt_chart.append((process.name, time, time + process.burst_time))
            time += process.burst_time
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            del remaining_processes[process.name]
        else:
            gantt_chart.append(('ID', time, time + 1))
            time += 1

            # Now, let's merge consecutive tasks of the same process in the gantt_chart
    merged_gantt_chart = []
    for task in gantt_chart:
        if not merged_gantt_chart or merged_gantt_chart[-1][0] != task[0]:
            merged_gantt_chart.append([task[0], task[1], task[2]])  # Start new task
        else:
            merged_gantt_chart[-1][2] = task[2]  # Extend the last task

    return merged_gantt_chart

def round_robin_scheduling(processes, quantum):
    time = 0
    gantt_chart = []
    ready_queue = []
    processes = sorted(processes, key=lambda x: x.arrival_time)
    
    while processes or ready_queue:
        while processes and processes[0].arrival_time <= time:
            ready_queue.append(processes.pop(0))

        if not ready_queue:
            gantt_chart.append(('ID', time, time + 1))
            time += 1
            continue

        process = ready_queue.pop(0)

        if process.start_time is None:
            process.start_time = time

        if process.remaining_time > quantum:
            gantt_chart.append((process.name, time, time + quantum))
            time += quantum
            process.remaining_time -= quantum
            while processes and processes[0].arrival_time <= time:
                ready_queue.append(processes.pop(0))
            ready_queue.append(process)
        else:
            gantt_chart.append((process.name, time, time + process.remaining_time))
            time += process.remaining_time
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.remaining_time = 0

        while processes and processes[0].arrival_time <= time:
            ready_queue.append(processes.pop(0))

        # Now, let's merge consecutive tasks of the same process in the gantt_chart
    merged_gantt_chart = []
    for task in gantt_chart:
        if not merged_gantt_chart or merged_gantt_chart[-1][0] != task[0]:
            merged_gantt_chart.append([task[0], task[1], task[2]])  # Start new task
        else:
            merged_gantt_chart[-1][2] = task[2]  # Extend the last task

    return merged_gantt_chart

def print_gantt_chart(gantt_chart, max_width=100):

    print("\nProcess List(Full Summary):")
    for task in gantt_chart:
        print(f" {task[0]}: {task[1]} - {task[2]}") #task 0 = pid, task 1 = arrival time, task 2 = burst time

    # Calculate how many tasks can fit in one line based on max_width
    task_width = 9  # Width of each task ("| P1 |", which is 5 characters plus 1 space)
    tasks_per_line = max_width // task_width  # How many tasks can fit in one line
    
    # Print the Gantt chart header
    print("\nGantt Chart:")
    
    # Variable to track the current time unit (start from 0)
    current_time = 0

    # Print the tasks line by line
    for i in range(0, len(gantt_chart), tasks_per_line):
        # Print the tasks in the current chunk
        print(" |", end="")
        for task in gantt_chart[i:i + tasks_per_line]:
            print(f"{task[0]} |".center(5), end="")
        print()
        
        # Print the timeline (time units) under the tasks
        print(f" {current_time}", end="   ") #if single digit apat, pag dalawang digit, tatlong space
        for task in gantt_chart[i:i + tasks_per_line]:
            # Print the time unit for each task and update the current_time
            print(f"{task[2]}".ljust(5), end="")
            current_time = task[2]
        print("\n")

def calculate_averages(processes):
    total_tat = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)
    total_burst_time = sum(p.burst_time for p in processes)
    
    total_time_elapsed = max(p.completion_time for p in processes)
    
    # CPU utilization
    cpu_utilization = (total_burst_time / total_time_elapsed) * 100
    
    # Calculate average turnaround and waiting times
    n = len(processes)
    avg_tat = total_tat / n
    avg_wt = total_wt / n
    
    print(f"\n Average TT: {avg_tat:.2f}")
    print(f" Average WT: {avg_wt:.2f}")
    print(f" CPU Utilization: {cpu_utilization:.2f}%")

def get_user_input(choice):
    processes = []
    num_processes = 0

    # Loop to ensure a valid integer is entered for the number of processes
    while True:
        try:
            num_processes = int(input(" Enter the number of processes: "))
            os.system("clear")
            if num_processes <= 0:
                os.system("clear")
                print("+----+-----+-----+-----+-----+-----+-----+")
                print("|                                        |")
                print("| Reminder: Please enter a VALID number! |")
                print("|                                        |")
                print("+----+-----+-----+-----+-----+-----+-----+")
                continue
            break
        except ValueError:
            os.system("clear")
            print("+----+-----+-----+-----+-----+-----+-----+")
            print("|                                        |")
            print("| Reminder: Please enter a VALID number! |")
            print("|                                        |")
            print("+----+-----+-----+-----+-----+-----+-----+")
            continue

    if choice == 3:
        cpu_design()
        for i in range(num_processes):
            print(f"\n No.{i+1}")
            name = f"P{i+1}"
            print(f" PID : P{i+1}")
            
            # Loop to ensure a valid integer is entered for arrival time
            while True:
                try:
                    arrival_time = int(input(f" AT for {name}  : "))
                    if arrival_time < 0:
                        print(" Invalid Input!\n")
                        continue
                    break
                except ValueError:
                    print(" Invalid Input!\n")
                                
            # Loop to ensure a valid integer is entered for burst time
            while True:
                try:
                    burst_time = int(input(f" BT for {name}  : "))
                    if burst_time <= 0:
                        print(" Invalid Input!\n")
                        continue
                    break
                except ValueError:
                    print(" Invalid Input!\n")
            
            # Loop to ensure a valid integer is entered for priority
            while True:
                try:
                    priority = int(input(f" PRIO for {name}: "))
                    if priority <= 0:
                        print(" Invalid Input!\n")
                        continue
                    break
                except ValueError:
                    print(" Invalid Input!\n")
            
            process = Process(name, arrival_time, burst_time, priority)
            processes.append(process)
        os.system("clear")

    else:
        cpu_design()
        for i in range(num_processes):
            print(f"\n No.{i+1}")
            name = f"P{i+1}"
            print(f" PID : P{i+1}")
        
            

            # Loop to ensure a valid integer is entered for arrival time
            while True:
                try:
                    arrival_time = int(input(f" AT for {name}  : "))
                    if arrival_time < 0:
                        print(" Invalid Input!\n")
                        continue
                    break
                except ValueError:
                    print(" Invalid Input!\n")
            
            # Loop to ensure a valid integer is entered for burst time
            while True:
                try:
                    burst_time = int(input(f" BT for {name}  : "))
                    if burst_time <= 0:
                        print(" Invalid Input!\n")
                        continue
                    break
                except ValueError:
                    print(" Invalid Input!\n")
            
            process = Process(name, arrival_time, burst_time)
            processes.append(process)
        os.system("clear")
    
    return processes

def print_process_table(processes, choice):
    if choice == 3:
    # Print the table header
        print("\nTABLE:")
        print("+----+-----+-----+-----+-----+-----+-----+-----+")
        print("{:<4} {:<5} {:<5} {:<4} {:<5} {:<5} {:<5} {:<5}".format("|PID","| AT","| BT","|PRIO","| CT","| RT","| TT","| WT  |"))
        print("+----+-----+-----+-----+-----+-----+-----+-----+")

        # Print process details in a tabular format
        for process in processes:
            print("| {:<3}|  {:<3}|  {:<3}|  {:<3}|  {:<3}|  {:<3}|  {:<3}|  {:<3}|".format(
                process.name, process.arrival_time, process.burst_time, process.priority,process.completion_time, 
                process.start_time - process.arrival_time if process.start_time else '0', 
                process.turnaround_time, process.waiting_time))
            print("+----+-----+-----+-----+-----+-----+-----+-----+")
    else:
    # Print the table header
        print("\nTABLE:")
        print("+----+-----+-----+-----+-----+-----+-----+")
        print("{:<4} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format("|PID","| AT","| BT","| CT","| RT","| TT","| WT  |"))
        print("+----+-----+-----+-----+-----+-----+-----+")
        
        # Print process details in a tabular format
        for process in processes:
            print("| {:<3}|  {:<3}|  {:<3}|  {:<3}|  {:<3}|  {:<3}|  {:<3}|".format(
                process.name, process.arrival_time, process.burst_time, process.completion_time, 
                process.start_time - process.arrival_time if process.start_time else '0', 
                process.turnaround_time, process.waiting_time))
            print("+----+-----+-----+-----+-----+-----+-----+")

def header():
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|  +-----+-----+ GROUP 2 +------+-----+  |")
    print("|  WELCOME TO CPU SCHEDULING SIMULATOR   |")
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|Options:                                |")
    print("| [1] FCFS                               |")
    print("| [2] SJF                                |")
    print("| [3] PRIORITY                           |")
    print("| [4] ROUND ROBIN                        |")
    print("| [0] EXIT                               |")
    print("|                                        |")
    print("| Reminder:Please select a valid choice! |")
    print("+----+-----+-----+-----+-----+-----+-----+")

def fcfs_design():
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|         FIRST COME FIRST SERVE         |")
    print("|             CPU SCHEDULING             |")
    print("+----+-----+-----+-----+-----+-----+-----+")
    
def sjf_design():
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|           SHORTEST JOB FIRST           |")
    print("|             CPU SCHEDULING             |")
    print("+----+-----+-----+-----+-----+-----+-----+")
    
def sjf_np_design():
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|   NON-PREEMPTIVE  SHORTEST JOB FIRST   |")
    print("|             CPU SCHEDULING             |")
    print("+----+-----+-----+-----+-----+-----+-----+")
    
def sjf_p_design():
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|     PREEMPTIVE  SHORTEST JOB FIRST     |")
    print("|             CPU SCHEDULING             |")
    print("+----+-----+-----+-----+-----+-----+-----+")
    
def priority_design():
    print("+----+-----+-----+-----+-----+-----+-----+-----+")
    print("|                  PRIORITY                    |")
    print("|               CPU SCHEDULING                 |")
    print("+----+-----+-----+-----+-----+-----+-----+-----+")

def priority_np_design():
    print("+----+-----+-----+-----+-----+-----+-----+-----+")
    print("|          NON-PREEMPTIVE PRIORITY             |")
    print("|               CPU SCHEDULING                 |")
    print("+----+-----+-----+-----+-----+-----+-----+-----+")
    
def priority_p_design():
    print("+----+-----+-----+-----+-----+-----+-----+-----+")
    print("|            PREEMPTIVE PRIORITY               |")
    print("|               CPU SCHEDULING                 |")
    print("+----+-----+-----+-----+-----+-----+-----+-----+")

def rr_design():
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|              ROUND ROBIN               |")
    print("|             CPU SCHEDULING             |")
    print("+----+-----+-----+-----+-----+-----+-----+")
    
def cpu_design():
    print("+----+-----+-----+-----+-----+-----+-----+")
    print("|  +-----+-----+ GROUP 2 +------+-----+  |")
    print("|       CPU SCHEDULING SIMULATOR         |")
    print("+----+-----+-----+-----+-----+-----+-----+")
    
# Main function to simulate the scheduling
while True:
    os.system("clear")
    header()

    try:
        choice = int(input(" Enter choice: "))  # Convert input to integer
    except ValueError:
        continue
    os.system("clear")

    if choice == 1:
        fcfs_design()
        processes = get_user_input(choice)

        fcfs_design()
        fcfs_gantt = fcfs_scheduling(processes.copy())
        # Call the print_process_table function after FCFS scheduling
        print_process_table(processes, choice)
        print_gantt_chart(fcfs_gantt)
        calculate_averages(processes)

    elif choice == 2:
        while True:
            try:
                sjf_design()
                np_or_p = int(input("Options:\n [1] Non-Preemptive\n [2] Preemptive\n\n Enter your choice: "))
                if np_or_p <= 0 or np_or_p >= 3:
                    os.system("clear")
                    print("\n Reminder: Please enter VALID number!\n")
                    continue
                break
            except ValueError:
                os.system("clear")
                print("\n Reminder: Please enter VALID number!\n")
        os.system("clear")
        
        if np_or_p == 1:
            sjf_np_design()
            processes = get_user_input(choice)
        
            sjf_np_design()
            sjf_gantt = sjf_non_preemptive_scheduling(processes.copy())
            # Call the print_process_table function after FCFS scheduling
            print_process_table(processes,choice)
            print_gantt_chart(sjf_gantt)
            calculate_averages(processes)
            
        else:
            sjf_p_design()
            processes = get_user_input(choice)

            sjf_p_design()
            sjfpreem_gantt = sjf_preemptive_scheduling(processes.copy())
            # Call the print_process_table function after FCFS scheduling
            print_process_table(processes, choice)
            print_gantt_chart(sjfpreem_gantt)
            calculate_averages(processes)

    elif choice == 3:
        while True:
            try:
                priority_design()
                np_or_p = int(input("Options:\n [1] Non-Preemptive\n [2] Preemptive\n\n Enter your choice: "))
                if np_or_p <= 0 or np_or_p >= 3:
                    os.system("clear")
                    print("\n Reminder: Please enter VALID number!\n")
                    continue
                break
            except ValueError:
                os.system("clear")
                print("\n Reminder: Please enter VALID number!\n")
        os.system("clear")

        while True:
            try:
                priority_design()
                highprio = int(input("\nSelect Higher Priorities:\n [1] Lowest Value = Highest Priority\n [2] Highest Value = Highest Priority\n\n Enter your choice: "))
                if highprio <= 0 or highprio >= 3:
                    os.system("clear")
                    print("\n Reminder: Please enter VALID number!\n")
                    continue
                break
            except ValueError:
                os.system("clear")
                print("\n Reminder: Please enter VALID number!\n")
        os.system("clear")
        
        if np_or_p == 1:
            priority_np_design()
            processes = get_user_input(choice)
        
            priority_np_design()
            if highprio == 1:
                print("NOTE: Lowest Value = Highest Priority")
            else:
                print("NOTE: Highest Value = Highest Priority")
            priority_non_preemptive_gantt = priority_non_preemptive_scheduling(processes.copy(), highprio)
            # Call the print_process_table function after FCFS scheduling
            print_process_table(processes, choice)
            print_gantt_chart(priority_non_preemptive_gantt)
            calculate_averages(processes)
        
        else:
            priority_p_design()
            processes = get_user_input(choice)

            priority_p_design()
            if highprio == 1:
                print("NOTE: Lowest Value = Highest Priority")
            else:
                print("NOTE: Highest Value = Highest Priority")
            priority_preemptive_gantt = priority_preemptive_scheduling(processes.copy(),highprio)
            # Call the print_process_table function after FCFS scheduling
            print_process_table(processes, choice)
            print_gantt_chart(priority_preemptive_gantt)
            calculate_averages(processes)

    elif choice == 4:
        
        while True:
            try:
                rr_design()
                quantum = int(input(" Enter Quantum Number: "))
                if quantum <= 0:
                    print("\n Please enter a positive integer for the number of processes.\n")
                    continue
                break
            except ValueError:
                os.system("clear")

        processes = get_user_input(choice)
        rr_design()
        print(f"           |   Quantum = {quantum}   |")
        print("           +-----+-----+-----+")
        rr_gantt = round_robin_scheduling(processes.copy(), quantum)
        # Call the print_process_table function after FCFS scheduling
        print_process_table(processes, choice)
        print_gantt_chart(rr_gantt)
        calculate_averages(processes)

    elif choice == 0:
        print(" Exiting program..")
        break

    else:
        print(" Wrong input for the choices! ")

    while True:
        try_again = input("\n Do you want to continue Y/N: ")

        if try_again == 'y' or try_again == 'Y':
            os.system("clear")
            break  # Exit the inner loop and continue to the next iteration of the main loop
        elif try_again == 'n' or try_again == 'N':
            os.system("clear")
            print(" Exiting program...")
            exit() # Exit the the entire loop
        else:
            os.system("clear")
            print(" Invalid input, please enter 'Y' or 'N'.")
