# import the libraries
import tkinter as tk

# colors and fonts
WHITE = "#efefef"
OFF_WHITE = "#d8dada"
LIGHT_GRAY = "#c5c8c8"
LABEL_COLOR = "#252626"

FONT_LG = ("Poppins", 40, "bold")
FONT_MD = ("Poppins", 24, "bold")
FONT_SM = ("Poppins", 20, "bold")


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x670")
        self.window.title("Calculator")
        self.window.resizable(0, 0)

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_button_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digits()
        self.create_operator()
        self.clear_button()
        self.equal_button()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event,
                             digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event,
                             operator=key: self.append_operator(operator))

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression,
                               anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=FONT_SM)
        total_label.pack(fill="both", expand=True)

        label = tk.Label(self.display_frame, text=self.current_expression,
                         anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=FONT_LG)
        label.pack(fill="both", expand=True)

        return total_label, label

    def create_display_frame(self):
        display_frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        display_frame.pack(fill="both", expand=True)
        return display_frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digits(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(
                digit), bg=WHITE, fg=LABEL_COLOR, font=FONT_MD, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0],
                        column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=FONT_SM,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=FONT_SM,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()
            self.update_total_label()

        self.update_label()

    def equal_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_GRAY, fg=LABEL_COLOR, font=FONT_SM,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_button_frame(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill="both", expand=True)

        return button_frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')

        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
