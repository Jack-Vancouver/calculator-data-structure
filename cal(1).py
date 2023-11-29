import tkinter as tk
import math
from fractions import Fraction

# 在代码的开始部分添加“是否上一次有展示结果”这个全局变量
is_result_displayed = False
def calculate(expression):
    def apply_operator(operators, values):
        operator = operators.pop()
        if operator in ['sin', 'cos', 'tan', 'ln ', 'exp']:
            operand = values.pop()
            if operator == 'sin':
                values.append(math.sin(math.radians(operand)) if angle_mode.get() == "DEG" else math.sin(operand))
            elif operator == 'cos':
                values.append(math.cos(math.radians(operand)) if angle_mode.get() == "DEG" else math.cos(operand))
            elif operator == 'tan':
                values.append(math.tan(math.radians(operand)) if angle_mode.get() == "DEG" else math.tan(operand))
            elif operator == 'ln ':
                values.append(math.log(operand))
            elif operator == 'exp':
                values.append(math.exp(operand))
        else:
            right = values.pop()
            left = values.pop()
            if operator == '+':
                values.append(left + right)
            elif operator == '-':
                values.append(left - right)
            elif operator == '*':
                values.append(left * right)
            elif operator == '/':
                values.append(left / right)

    def precedence(operator):
        if operator in ['sin', 'cos', 'tan', 'ln ', 'exp']:
            return 3
        elif operator in ['*', '/']:
            return 2
        elif operator in ['+', '-']:
            return 1
        else:
            return 0

    operators = []
    values = []
    i = 0


    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue

        if expression[i] in '.0123456789':
            j = i
            while j < len(expression) and expression[j] in '.0123456789':
                j += 1
            values.append(float(expression[i:j]))
            i = j
            continue

        if expression[i] in '+-*/':
            while operators and precedence(operators[-1]) >= precedence(expression[i]):
                apply_operator(operators, values)
            operators.append(expression[i])

        if expression[i:i+3] in ['sin', 'cos', 'tan', 'ln ', 'exp']:
            operators.append(expression[i:i+3])
            i += 2

        if expression[i] == '(':
            operators.append(expression[i])

        if expression[i] == ')':
            while operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()

        i += 1

    while operators:
        apply_operator(operators, values)

    return values[0]

# 用于呈现表达式的函数
def evaluate_expression(expression):
    global is_result_displayed
    try:
        # 计算数学表达式的值
        result_fraction = calculate(expression)

        # 将分数转换为小数，保留六位小数
        result_decimal = float(result_fraction)
        result_str = format(result_decimal, ".6f")
        is_result_displayed = True  # 设置标识为True，表示当前显示的是计算结果

        # 用结果更新输入字段
        input_text.set(result_str)
    except:
        # 如果表达式有误，输入字段显示“Error”
        input_text.set("Error")
        is_result_displayed = True

# 更新输入字段中的表达式的函数
def update_expression(symbol):
    global is_result_displayed
    current_text = input_text.get()

    # 如果当前显示的是计算结果，则先清除
    if is_result_displayed:
        current_text = ""
        is_result_displayed = False

    if symbol == 'π':
        current_text += str(math.pi)  # Append the value of Pi
    else:
        current_text += str(symbol)
    input_text.set(current_text)

# 清除输入的函数
def clear_input():
    input_text.set("")

# 创建基本窗口
window = tk.Tk()
window.title("Scientific Calculator")

# 创建一个StringVar()来保存表达式
input_text = tk.StringVar()

# 默认设置为角度模式
angle_mode = tk.StringVar()
angle_mode.set("DEG")  # 默认设置为角度模式

# 创建一个输入控件来显示当前的表达式
input_field = tk.Entry(window, textvar=input_text, font=('Helvetica', 30), bd=5, insertwidth=4, width=25, justify='right')
input_field.grid(row=0, column=0, columnspan=5)

# 按钮布局
buttons = [
    '7', '8', '9', '/', 'ln ',
    '4', '5', '6', '*', 'exp',
    '1', '2', '3', '-', 'sin',
    'C', '0', '.', '+', 'cos',
    '(', ')', 'π', '=', 'tan'
]

row = 1
col = 0

# 生成按钮并将它们放在网格中
for button in buttons:
    tk.Button(window, text=button, padx=38, pady=20, font=('Courier New', 30), 
              command=lambda b=button: update_expression(b) if b not in ['=', 'C'] else (evaluate_expression(input_text.get()) if b == '=' else clear_input())).grid(row=row, column=col)
    col += 1
    if col > 4:
        col = 0
        row += 1

# 切换角度和弧度，添加 toggle_button
def toggle_angle_mode():
    if angle_mode.get() == "DEG":
        angle_mode.set("RAD")
        angle_mode_label.config(text="Mode: RAD")  # 更新标签的文本
    else:
        angle_mode.set("DEG")
        angle_mode_label.config(text="Mode: DEG")  # 更新标签的文本

# 你需要计算正确的行和列来放置这个新按钮
toggle_button = tk.Button(window, text="DEG/RAD switch", command=toggle_angle_mode, font=('Helvetica, 20'))
toggle_button.grid(row=6, column=0, columnspan=2)  # 根据需要调整 row 和 column

# 在这里添加一个标签来显示当前的角度模式
angle_mode_label = tk.Label(window, text="Mode: DEG", font=('Helvetica', 20))
angle_mode_label.grid(row=6, column=2, columnspan=3)  # 根据需要调整 row 和 column

# 处理特殊按钮
input_text.set("")

# 运行应用程序
window.mainloop()



