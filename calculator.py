import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from functools import partial

#initial conditions
var = [0]
negative = [False]
line = ''
decimal = [False]
pointer = 0
saved_operations = ['']
has_started = [False]
decimals_place = [10]

#when operator is pressed, add new conditions for new number
def append_num():
    global var, negative, decimal, saved_operations, has_started, decimals_place
    var.append(0)
    negative.append(False)
    decimal.append(False)
    saved_operations.append('')
    has_started.append(False)
    decimals_place.append(10)

#if del is pressed, reset back to initial conditions
def reset():
    global var, negative, decimal, saved_operations, has_started, decimals_place, pointer, line
    var[:] = [0]
    negative[:] = [False]
    decimal[:] = [False]
    saved_operations[:] = ['']
    has_started[:] = [False]
    decimals_place[:] = [10]
    pointer = 0
    line = ''
    calculator.config(text=line)

#if user doesn't press del after calculation, let them use the result
def not_done_calculating(result):
    global var, negative, decimal, saved_operations, has_started, decimals_place, pointer, line
    var.clear()
    saved_operations.clear()
    negative.clear()
    decimal.clear()
    has_started.clear()
    decimals_place.clear()
    var.append(abs(result))
    saved_operations.append('')
    negative.append(result < 0)
    decimal.append('.' in str(result))
    decimal_tracker = str(result)
    decimal_tracker_counter = 0
    for char in decimal_tracker:
        if char != '.':
            decimal_tracker_counter += 1
        else:
            break
    decimals_place.append(10 * 10 ** len(decimal_tracker[(decimal_tracker_counter+1):]))
    has_started.append(True)
    pointer = 0
    line = str(result)

#simple calculator functions
def add(num_one, num_two):
    result = num_one + num_two
    return result

def subtract(num_one, num_two):
    result = num_one - num_two
    return result

def multiply(num_one, num_two):
    result = num_one * num_two
    return result

def divide(num_one, num_two):
    if num_two == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    result = num_one / num_two
    return result

#takes the operations if conditions are met, alters negative and decimal states, moves pointer and re-creates conditions for next number
def operation(sign):
    global line, pointer, saved_operations, has_started, negative
    if has_started[pointer] == False and sign == '-' and negative[pointer] == False:
        negative[pointer]=True
        line += sign
        calculator.config(text=line)
    elif var[pointer] == 0 and sign == '.' and decimal[pointer]==False:
        decimal[pointer]=True
        has_started[pointer] = True
        line += '.'
        calculator.config(text=line)
    elif var[pointer] != 0 and decimal[pointer] == False and sign == '.':
        decimal[pointer]=True
        line += '.'
        calculator.config(text=line)
    elif sign in ('+', '-', '*', '/'):
        if negative[pointer] == True:
            if has_started[pointer] == False:
                return
            else:
                var[pointer] *= (-1)
        saved_operations[pointer] = sign
        line += sign
        calculator.config(text=line)
        append_num()
        pointer += 1

#stores numbers, records decimal places
def numbers(number):
    global line, var, pointer, decimals_place
    line += number
    calculator.config(text=line)
    if decimal[pointer]==False:
        var[pointer] = var[pointer]*10 + int(number)
    elif decimal[pointer]==True:
        var[pointer] += (int(number)/decimals_place[pointer]) # type: ignore
        decimals_place[pointer] *= 10

#access the calculation functions, applies negatives, updates display, follows order of operations
def calculate():
    global var, saved_operations, negative, pointer, line
    if negative[pointer] == True:
        var[pointer] *= (-1)
    backup_operations = saved_operations.copy()
    backup_var = var.copy()
    for i, sign in enumerate(backup_operations):
        if sign in ('/', '*'):
            if sign == '/':
                try:
                    backup_var[i+1] = divide(backup_var[i], backup_var[i+1]) # type: ignore
                except ZeroDivisionError:
                    calculator.config(text="UNDEF")
                    return
                backup_var[i+1] = round(backup_var[i+1], 10)
                backup_var[i] = None # type: ignore
            elif sign == '*':
                backup_var[i+1] = multiply(backup_var[i], backup_var[i+1]) # type: ignore
                backup_var[i+1] = round(backup_var[i+1], 10)
                backup_var[i] = None # type: ignore
    for i in range(len(backup_var)-1, -1, -1):
        if backup_var[i] == None:
            del backup_var[i]
            del backup_operations[i]
    saved_operations = backup_operations.copy()
    var = backup_var.copy()
    if len(var) == len(saved_operations) and len(saved_operations) != 1:
        del saved_operations[len(saved_operations) - 1]
    result = var[0]
    for i, sign in enumerate(saved_operations):
        if sign == '+':
            result = add(result, var[i+1])
        elif sign == '-':
            result = subtract(result, var[i+1])
        result = round(result, 10)
    calculator.config(text=str(result))
    not_done_calculating(result)
      
#button inputs
def button_command(label):
    global line, var, negative, decimal, pointer, saved_operations, has_started, decimals_place

    if label != 'del':
        if (label in ('+', '*', '/') and has_started[pointer]==True) or (label in ('-', '.')):
            operation(label)
        elif label in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',):
            has_started[pointer] = True
            numbers(label)
        elif label == '=':
            calculate()
    else:
        reset()
        
#tkinter stuff
root=tk.Tk()
root.geometry("400x475")
large_font=tkfont.Font(size=20)
frm=ttk.Frame(root, padding=10)
frm.grid()
frm.grid(sticky="nsew")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
for i in range(5):
    frm.rowconfigure(i, weight=1)
for j in range(5):
    frm.columnconfigure(j, weight=1)
calculator=tk.Label(frm, text="0", height=3, width = 3)
calculator.grid(row=0, column=0, columnspan=5, sticky='nsew', padx=5, pady=2)
calculator.config(font=('TkDefaultFont', 24), anchor='e', bg='white', fg='black', relief='sunken')

#making buttons
buttons=[
    ['7', '8', '9', '/', 'del'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]
for r, row in enumerate(buttons):
    for c, text in enumerate(row):
        if text == 'del':
            btn=tk.Button(frm, text=text, font=('TkDefaultFont', 20), height=3, width=4, relief='raised', command=partial(button_command, text))
            btn.grid(row=r + 1, column=c, rowspan=4, sticky='nsew', padx=2, pady=2)
        else:
            btn=tk.Button(frm, text=text, font=('TkDefaultFont', 20), height=3, width=4, relief='raised', command=partial(button_command, text))
            btn.grid(row=r + 1, column=c, sticky='nsew', padx=2, pady=2)
root.mainloop()