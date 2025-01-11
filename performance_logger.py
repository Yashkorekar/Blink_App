import psutil
import time
import threading
import os

class PerformanceLogger:
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []
        self.memory_percent = []
        self.running = False
        self.log_file = "performance_log.txt"
        self.process = psutil.Process(os.getpid())
        self.metrics = {
            'cpu_usage': [],
            'memory_usage': [],
            'memory_percent': [],
            'fps': [],
            'latency': []
        }

    def log_performance(self):
        self.running = True
        with open(self.log_file, "w") as file:
            file.write("Time,CPU_Usage,Memory_Usage_MB,Memory_Usage_Percent,Latency\n")

        while self.running:
            try:
                cpu = self.process.cpu_percent(interval=1)
                
                memory_mb = self.process.memory_info().rss / 1024 / 1024
                
                memory_percent = self.process.memory_percent()
                
                self.metrics['cpu_usage'].append(cpu)
                self.metrics['memory_usage'].append(memory_mb)
                self.metrics['memory_percent'].append(memory_percent)

                with open(self.log_file, "a") as file:
                    file.write(f"{time.time()},{cpu},{memory_mb:.2f},{memory_percent:.2f}\n")

                print(f"Process CPU Usage: {cpu}%, "
                      f"Process Memory Usage: {memory_mb:.2f} MB ({memory_percent:.2f}%)")
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                print("Failed to get process information")
                break

            time.sleep(1)

    def start_logging(self):
        threading.Thread(target=self.log_performance, daemon=True).start()

    def stop_logging(self):
        self.running = False

    def get_performance_summary(self):
        if not self.metrics['cpu_usage'] or not self.metrics['memory_usage']:
            return "No data collected."

        avg_cpu = sum(self.metrics['cpu_usage']) / len(self.metrics['cpu_usage'])
        peak_cpu = max(self.metrics['cpu_usage'])
        avg_memory_mb = sum(self.metrics['memory_usage']) / len(self.metrics['memory_usage'])
        peak_memory_mb = max(self.metrics['memory_usage'])
        avg_memory_percent = sum(self.metrics['memory_percent']) / len(self.metrics['memory_percent'])
        peak_memory_percent = max(self.metrics['memory_percent'])

        if self.metrics['latency']:
            avg_latency = sum(self.metrics['latency']) / len(self.metrics['latency'])
            peak_latency = max(self.metrics['latency'])
            latency_info = (f"\nAverage Latency: {avg_latency:.2f} ms\n"
                          f"Peak Latency: {peak_latency:.2f} ms")
        else:
            latency_info = ""

        summary = (f"Average Process CPU Usage: {avg_cpu:.2f}%\n"
                  f"Peak Process CPU Usage: {peak_cpu:.2f}%\n"
                  f"Average Process Memory Usage: {avg_memory_mb:.2f} MB ({avg_memory_percent:.2f}%)\n"
                  f"Peak Process Memory Usage: {peak_memory_mb:.2f} MB ({peak_memory_percent:.2f}%)"
                  f"{latency_info}")
        return summary