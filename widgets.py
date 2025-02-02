import tkinter as tk


class Choice:
    def __init__(self, root, text, options, selected_option=0, values=None, command=None, horizontal_options=False):
        if not values:
            values = options[:]

        self.values = values
        self.options = options

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.var = tk.StringVar(value=options[selected_option])

        self.label = tk.Label(self.frame, text=text)

        self.rb = []
        for option, value in zip(options, values):
            self.rb.append(tk.Radiobutton(self.frame, text=option, variable=self.var, value=value, command=command))

        if horizontal_options:
            self.label.grid(row=0, column=0)
            for i, rb in enumerate(self.rb):
                rb.grid(row=0, column=i + 1)
        else:
            self.label.pack()
            for rb in self.rb:
                rb.pack()

    def get(self):
        return self.var

    def set_option(self, option):
        if option in self.options:
            self.var = option
        raise ValueError(f"Невозможно выбрать опцию {option}. Допустимые: {self.options}")


class ChoiceYesNo(Choice):
    def __init__(self, root, text, selected_option=0, command=None):
        super().__init__(root, text, options=("Yes", "No"), selected_option=int(selected_option),
                         command=command, horizontal_options=True)

    def get(self):
        return self.var == 'Yes'


class TextEntry:
    def __init__(self, root, text, defaultEntryValue=''):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text=text)
        self.label.grid(row=0, column=0)

        self.entry = tk.Entry(self.frame)
        self.entry.grid(row=0, column=1)
        self.set(defaultEntryValue)

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.clear()
        self.entry.insert(0, value)

    def clear(self):
        self.entry.delete(0, tk.END)
