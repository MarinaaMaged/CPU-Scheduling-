from manim import *
import random

class FCFSSimulation(Scene):
    def construct(self):
        title = Text("First-Come-First-Serve (FCFS) Scheduling", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Initialize Process Data
        processes = []
        process_rects = VGroup()

        timeline_start = 0
        timeline_end = 10  
        timeline = Line(start=LEFT * 6, end=RIGHT * 6, color=GRAY)
        self.play(Create(timeline))

        ticks = VGroup()
        tick_spacing = timeline.get_length() / (timeline_end - timeline_start)
        for i in range(timeline_start, timeline_end + 1):
            tick = Line(start=DOWN * 0.2, end=UP * 0.2, color=WHITE)
            tick.move_to(timeline.get_start() + i * tick_spacing * RIGHT)
            ticks.add(tick)

            tick_label = Text(str(i), font_size=18).next_to(tick, DOWN)
            self.add(tick_label)
        self.play(Create(ticks))

        # Create a text box for displaying metrics
        metrics_box = Rectangle(width=4, height=2, color=WHITE, fill_opacity=0.5).to_edge(DOWN)
        metrics_text = Text("Metrics:", font_size=18).move_to(metrics_box.get_center() + UP * 0.5)
        avg_waiting_time_text = Text("Avg Waiting Time: --", font_size=16).next_to(metrics_text, DOWN)
        avg_turnaround_time_text = Text("Avg Turnaround Time: --", font_size=16).next_to(avg_waiting_time_text, DOWN)
        avg_response_time_text = Text("Avg Response Time: --", font_size=16).next_to(avg_turnaround_time_text, DOWN)
        self.play(Create(metrics_box), Write(metrics_text), Write(avg_waiting_time_text), Write(avg_turnaround_time_text), Write(avg_response_time_text))

        # Simulate process arrival and execution
        for step in range(1, timeline_end + 1):
            # Randomly spawn a process
            if random.random() < 0.7:
                pid = random.randint(1000, 9999)
                burst_time = random.randint(1, 3)
                processes.append((pid, step, burst_time))

                process_rect = Rectangle(width=burst_time * tick_spacing, height=0.5, color=BLUE, fill_opacity=0.7)
                process_rect.next_to(timeline.get_start() + (step - timeline_start) * tick_spacing * RIGHT, UP, buff=0.1)

                process_label = Text(f"P{pid}", font_size=16).move_to(process_rect.get_center())
                self.play(Create(process_rect), Write(process_label))
                process_rects.add(process_rect)
            # Randomly kill a process
            if processes and random.random() < 0.3:  
                process_to_kill = random.choice(processes)
                processes.remove(process_to_kill)
                # Remove the last process rectangle from the screen
                self.play(FadeOut(process_rects[-1]))  
            self.wait(0.5)

            # Calculate FCFS metrics and update them
            avg_wait, avg_turnaround, avg_response, _ = fcfs_scheduling(processes)
            self.play(
                Transform(avg_waiting_time_text, Text(f"Avg Waiting Time: {avg_wait:.2f}", font_size=16).next_to(metrics_text, DOWN)),
                Transform(avg_turnaround_time_text, Text(f"Avg Turnaround Time: {avg_turnaround:.2f}", font_size=16).next_to(avg_waiting_time_text, DOWN)),
                Transform(avg_response_time_text, Text(f"Avg Response Time: {avg_response:.2f}", font_size=16).next_to(avg_turnaround_time_text, DOWN))
            )

        # Final observation time
        self.wait(2)

# This function calculates the FCFS scheduling metrics and returns them
def fcfs_scheduling(processes):
    n = len(processes)
    if n == 0:
        return 0, 0, 0, []

    processes.sort(key=lambda x: x[1])  # Sort processes by arrival time

    completion_times = [0] * n
    waiting_times = [0] * n
    turnaround_times = [0] * n
    response_times = [0] * n
    current_time = 0
    process_info = []

    for i in range(n):
        process_id, arrival_time, burst_time = processes[i]
        if current_time < arrival_time:
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
