import tkinter as tk
from tkinter import ttk
import sys
from process import CPUBar
from widget_update import Configure_widgets

class Application(tk.Tk, Configure_widgets):

    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 1)                                                                    # прозрачность
        self.attributes('-topmost', True)                                                               # поверх остальных окон
        self.overrideredirect(True)                                                                     # убираем рамку окна
        self.resizable(False, False)                                                                    # запрещаем изменять размер окна
        self.title('CPU-RAM monitor')                                                                   # название окна
        self.cpu = CPUBar()
        self.run_set_ui()

    def run_set_ui(self):
        self.set_ui()                                                                                   # запускаем метод с виджетами
        self.make_bar_cpu_usage()
        self.configure_cpu_bar()

    def set_ui(self):
        exit_but = ttk.Button(self, text='Exit', command=self.app_exit)                                 # создаем кнопку 'Exit'
        exit_but.pack(fill=tk.X)                                                                        # .pack() это метод сборщика кнопки

        self.bar2 = ttk.LabelFrame(self, text='Manual')                                                 # размещаем рамку (фрэйм)
        self.bar2.pack(fill=tk.X)

        self.combo_win = ttk.Combobox(self.bar2,
                                      values=['hide', "don't hide", 'min'],
                                      width=9, state='readonly')                                       # создаем выпадающий список
        self.combo_win.current(1)                                                                       # указываем стандартное значие при первоначальном отображении
        self.combo_win.pack(side=tk.LEFT)

        ttk.Button(self.bar2, text='Move', command=self.configure_win).pack(side=tk.LEFT)               # создаем кнопку 'Move'

        self.bar = ttk.LabelFrame(self, text='Power')                                                   # размещаем рамку (фрэйм) 'Power'
        self.bar.pack(fill=tk.BOTH)

        self.bind_class('Tk', '<Enter>', self.enter_mouse)
        self.bind_class('Tk', '<Leave>', self.leave_mouse)
        self.combo_win.bind('<<ComboboxSelected>>', self.choice_combo)

    def make_bar_cpu_usage(self):
        ttk.Label(self.bar, text=f'physical cores: {self.cpu.cpu_count}, '
                                 f'logical cores: {self.cpu.cpu_count_logical}.',
                                 anchor=tk.CENTER).pack(fill=tk.X)

        self.list_label = []
        self.list_pbar = []
        for i in range(self.cpu.cpu_count_logical):
            self.list_label.append(ttk.Label(self.bar, anchor=tk.CENTER))
            self.list_pbar.append(ttk.Progressbar(self.bar, length=100))
        for i in range(self.cpu.cpu_count_logical):
            self.list_label[i].pack(fill=tk.X)
            self.list_pbar[i].pack(fill=tk.X)

        self.ram_lab = ttk.Label(self.bar, text='', anchor=tk.CENTER)
        self.ram_lab.pack(fill=tk.X)
        self.ram_bar = ttk.Progressbar(self.bar, length=100)
        self.ram_bar.pack(fill=tk.X)

    def  make_minimal_win(self):
        self.bar1 = ttk.Progressbar(self, length=100)
        self.bar1.pack(side=tk.LEFT)

        self.ram_bar = ttk.Progressbar(self, length=100)
        self.ram_bar.pack(side=tk.LEFT)

        ttk.Button(self, text='full',
                   command=self.make_full_win, width=5).pack(side=tk.RIGHT)

        ttk.Button(self, text='move',
                   command=self.configure_win, width=5).pack(side=tk.RIGHT)

        self.update()
        self.configure_min_win()

    def enter_mouse(self, event):
        if self.combo_win.current() == 0 or 1:
            self.geometry('')

    def leave_mouse(self, event):
        if self.combo_win.current() == 0:
            self.geometry(f'{self.winfo_width()}x1')                        # высота окна остается равной 1 пиксель

    def choice_combo(self, event):
        if self.combo_win.current() == 2:
            self.enter_mouse('')
            self.unbind_class('Tk', '<Enter>')
            self.unbind_class('Tk', '<Leave>')
            self.combo_win.unbind('<<ComboboxSelected>>')
            self.after_cancel(self.wheel)
            self.clear_win()                                                   # очищаем окно от виджетов
            self.update()
            self.make_minimal_win()

    def make_full_win(self):
        self.after_cancel(self.wheel)
        self.clear_win()
        self.update()
        self.run_set_ui()
        # self.enter_mouse('')
        # self.combo_win.current(1)

    def app_exit(self):
        self.destroy()                                                      # закрываем окно
        sys.exit()                                                          # завершаем процесс

if __name__ == '__main__':
    root = Application()
    root. mainloop()                                                        # создаем и вызываем стандартное окно