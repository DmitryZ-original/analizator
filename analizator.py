import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import ttkbootstrap as ttk


class DataAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ csv файла")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        style = ttk.Style("darkly")

        self.stol = None
        self.orig_stol = None

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        load_frame = ttk.Frame(main_frame)
        load_frame.pack(fill=tk.X, pady=5)

        self.load_button = ttk.Button(
            load_frame,
            text="Загрузить файл",
            command=self.load,
            bootstyle="LIGHT, OUTLINE",
        )
        self.load_button.pack(pady=10)

        stol_frame = ttk.Frame(main_frame)
        stol_frame.pack(fill=tk.BOTH, expand=True)

        x_scrollbar = ttk.Scrollbar(stol_frame, orient="horizontal")
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        y_scrollbar = ttk.Scrollbar(stol_frame, orient="vertical")
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            stol_frame,
            show="headings",
            xscrollcommand=x_scrollbar.set,
            yscrollcommand=y_scrollbar.set,
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        x_scrollbar.config(command=self.tree.xview)
        y_scrollbar.config(command=self.tree.yview)

        filter_frame = ttk.Labelframe(
            main_frame, text="Фильтрация данных", padding=10, bootstyle="LIGHT"
        )
        filter_frame.pack(fill=tk.X, pady=10)

        self.filter_column_lb = ttk.Label(
            filter_frame, text="Выберите столбец для фильтрации:"
        )
        self.filter_column_lb.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.filter_column_combobox = ttk.Combobox(filter_frame, state="readonly")
        self.filter_column_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.filter_lb = ttk.Label(
            filter_frame, text="Введите значение для фильтрации:"
        )
        self.filter_lb.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.filter_entry = ttk.Entry(filter_frame)
        self.filter_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.filter_button = ttk.Button(
            filter_frame,
            text="Фильтрация",
            command=self.filter,
            bootstyle="LIGHT, OUTLINE",
        )
        self.filter_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.reset_button = ttk.Button(
            filter_frame,
            text="Сброс фильтра",
            command=self.reset,
            bootstyle="DANGER, OUTLINE",
        )
        self.reset_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        analysis_frame = ttk.Labelframe(
            main_frame, text="Анализ данных", padding=10, bootstyle="LIGHT"
        )
        analysis_frame.pack(fill=tk.X, pady=10)

        self.column_select_lb = ttk.Label(
            analysis_frame, text="Выберите столбец для анализа:"
        )
        self.column_select_lb.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.column_combobox = ttk.Combobox(analysis_frame, state="readonly")
        self.column_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.mean_button = ttk.Button(
            analysis_frame,
            text="Среднее",
            command=self.find_mean,
            bootstyle="LIGHT, OUTLINE",
        )
        self.mean_button.grid(row=1, column=0, padx=5, pady=5)

        self.min_button = ttk.Button(
            analysis_frame,
            text="Минимум",
            command=self.find_min,
            bootstyle="LIGHT, OUTLINE",
        )
        self.min_button.grid(row=1, column=1, padx=5, pady=5)

        self.max_button = ttk.Button(
            analysis_frame,
            text="Максимум",
            command=self.find_max,
            bootstyle="LIGHT, OUTLINE",
        )
        self.max_button.grid(row=1, column=2, padx=5, pady=5)

    def load(self):
        file_way = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_way:
            try:
                self.orig_stol = pd.read_csv(file_way)
                self.stol = self.orig_stol.copy()
                self.show()

                columns = list(self.stol.columns)
                self.column_combobox["values"] = columns
                self.filter_column_combobox["values"] = columns

                self.column_combobox.current(0)
                self.filter_column_combobox.current(0)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def show(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["column"] = list(self.stol.columns)
        self.tree["show"] = "headings"
        for col in self.tree["column"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")

        for _, row in self.stol.iterrows():
            self.tree.insert("", "end", values=list(row))

    def find_mean(self):
        column = self.column_combobox.get()
        if column:
            try:
                mean_znach = self.stol[column].mean()
                messagebox.showinfo(
                    "Среднее значение",
                    f"Среднее значение для столбца '{column}': {mean_znach:.2f}",
                )
            except Exception as e:
                messagebox.showerror(
                    "Ошибка", f"Нельзя найти среднее значение для столбца '{column}'"
                )

    def find_min(self):
        column = self.column_combobox.get()
        if column:
            min_znach = self.stol[column].min()
            messagebox.showinfo(
                "Минимальное значение",
                f"Минимальное значение для столбца '{column}': {min_znach}",
            )

    def find_max(self):
        column = self.column_combobox.get()
        if column:
            max_znach = self.stol[column].max()
            messagebox.showinfo(
                "Максимальное значение",
                f"Максимальное значение для столбца '{column}': {max_znach}",
            )

    def filter(self):
        filter_column = self.filter_column_combobox.get()
        filter_znach = self.filter_entry.get()

        if self.stol is not None and filter_column and filter_znach:
            filtered_stol = self.stol[
                self.stol[filter_column].astype(str).str.contains(filter_znach)
            ]
            self.stol = filtered_stol
            self.show()

    def reset(self):
        if self.orig_stol is not None:
            self.stol = self.orig_stol.copy()
            self.show()


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = DataAnalyzerApp(root)
    root.mainloop()
