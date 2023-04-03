import psutil as pt


class CPUBar:

    def __init__(self):
        self.cpu_count = pt.cpu_count(logical=False)            # узнаем кол-во ядер процессора
        self.cpu_count_logical = pt.cpu_count()

    def cpu_percent_return(self):
        return pt.cpu_percent(percpu=True)

    def ram_usage(self):
        return pt.virtual_memory()

