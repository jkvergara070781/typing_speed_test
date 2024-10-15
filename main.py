import tkinter as tk
from word_bank import two_letter_words, three_letter_words, four_letter_words, five_letter_words
import random

root = tk.Tk()
root.title('Typing Speed Tester')
root.config(background='#1526ea')

window_width = 1200
window_height = 800

speed_value = 0
accuracy = 0
adjusted_value = 0
level = ''
index = 0
time_left = 60
after_id = None
wrong_word = 0
correct_word = 0


def timer():
    global time_left, after_id
    if time_left >= 1:
        time_left -= 1
        label.config(text=f'Time left: {time_left}')
        after_id = label.after(1000, timer)


def reset_timer():
    global after_id, time_left
    if after_id is not None:
        label.after_cancel(f'{after_id}')
        after_id = None
        time_left = 60
        label.config(text=f'Time left: {time_left}')


def entry_display():
    entry.insert(0, 'type the words here')
    center_position = len(entry.get()) // 2
    entry.icursor(center_position)
    entry.focus()


def clear_entry(event):
    if entry.get() == 'type the words here':
        entry.delete(0, tk.END)

    if time_left == 60:
        timer()


def clear_entered_word(event):
    entry.delete(0, tk.END)


def generate_words():

    list_two_letter_word = [random.choice(two_letter_words) for _ in range(30)]
    list_three_letter_word = [random.choice(three_letter_words) for _ in range(30)]
    list_four_letter_word = [random.choice(four_letter_words) for _ in range(30)]
    list_five_letter_word = [random.choice(five_letter_words) for _ in range(30)]

    word_list = list_two_letter_word + list_three_letter_word + list_four_letter_word + list_five_letter_word
    random.shuffle(word_list)

    words = ' '.join(word_list)
    if text_1.get('1.0', tk.END).strip() == '':
        text_1.insert(tk.END, words)

    entry_display()


def delete_words():
    global index, time_left, speed_value, accuracy, adjusted_value, level
    text_1.delete('1.0', tk.END)
    entry.delete(0, tk.END)
    index = 0
    speed_value = 0
    accuracy = 0
    adjusted_value = 0
    level = ''

    text_2.delete('1.0', tk.END)
    text_2.insert(1.0, f'Speed (WPM): {speed_value}')
    text_3.delete('1.0', tk.END)
    text_3.insert(1.0, f'Accuracy (%): {accuracy}')
    text_4.delete('1.0', tk.END)
    text_4.insert(1.0, f'Adj. Speed (WPM): {adjusted_value}')
    text_5.delete('1.0', tk.END)
    text_5.insert(1.0, f'Level: {level}')

    entry.config(state=tk.NORMAL)

    reset_timer()


def compare_word(event):
    global index, correct_word, wrong_word, speed_value, adjusted_value, accuracy, level

    text_content = text_1.get('1.0', tk.END).split()
    entry_content = entry.get().strip()

    current_word = text_content[index]

    start_index = f'1.0 + {sum(len(w) + 1 for w in text_content[:index])}c'
    end_index = f'{start_index} + {len(current_word)}c'

    if entry_content == current_word:
        text_1.tag_add('correct', start_index, end_index)
        text_1.tag_config('correct', foreground='green')
        correct_word += 1
    else:
        text_1.tag_add('incorrect', start_index, end_index)
        text_1.tag_config('incorrect', foreground='red')
        wrong_word += 1

    clear_entered_word(event)

    index += 1

    if index >= len(text_content):
        entry.config(state=tk.DISABLED)
    if time_left == 60:
        speed_value = 0
        accuracy = 0
        adjusted_value = 0
        level = ''
    elif time_left == 0:
        entry.config(state=tk.DISABLED)
        speed_value = wrong_word + correct_word
        text_2.delete('1.0', tk.END)
        text_2.insert(1.0, f'Speed (WPM): {speed_value}')
        accuracy = round((speed_value - wrong_word) / speed_value * 100, 1)
        text_3.delete('1.0', tk.END)
        text_3.insert(1.0, f'Accuracy (%): {accuracy}')
        adjusted_value = speed_value - wrong_word
        text_4.delete('1.0', tk.END)
        text_4.insert(1.0, f'Adj. Speed (WPM): {adjusted_value}')
        if adjusted_value < 20:
            level = 'Beginner'
            text_5.delete('1.0', tk.END)
            text_5.insert(1.0, f'Level: {level}')
        elif adjusted_value < 40:
            level = 'Intermediate'
            text_5.delete('1.0', tk.END)
            text_5.insert(1.0, f'Level: {level}')
        elif adjusted_value < 60:
            level = 'Average'
            text_5.delete('1.0', tk.END)
            text_5.insert(1.0, f'Level: {level}')
        elif adjusted_value < 80:
            level = 'Advanced'
            text_5.delete('1.0', tk.END)
            text_5.insert(1.0, f'Level: {level}')
        elif adjusted_value < 100:
            level = 'Professional'
            text_5.delete('1.0', tk.END)
            text_5.insert(1.0, f'Level: {level}')
        else:
            level = 'Expert'
            text_5.delete('1.0', tk.END)
            text_5.insert(1.0, f'Level: {level}')


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.wm_geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

text_1 = tk.Text(root, background='#e6e4fd', font=('Courier', 30), foreground='#091064', height=12, width=50, wrap='word')
entry = tk.Entry(root, background='#aaa4f7', font=('Courier', 30), justify='center', foreground='#091064')
entry.bind('<KeyPress>', clear_entry)
entry.bind('<space>', compare_word)
button_1 = tk.Button(root, text='Generate Words', font=('Courier', 20), width=13, command=generate_words)
button_2 = tk.Button(root, text='Clear Display', font=('Courier', 20), width=13, command=delete_words)
text_2 = tk.Text(root, font=('Courier', 20,), height=1, width=16, background='#d5f40b', foreground='#090a03')
text_2.insert(1.0, f'Speed (WPM): {speed_value}')
text_3 = tk.Text(root, width=18, height=1, font=('Courier', 20,), background='#d5f40b', foreground='#090a03')
text_3.insert(1.0, f'Accuracy (%): {accuracy}')
text_4 = tk.Text(root, width=20, height=1, font=('Courier', 20,), background='#d5f40b', foreground='#090a03')
text_4.insert(1.0, f'Adj. Speed (WPM): {adjusted_value}')
text_5 = tk.Text(root, width=20, height=1, font=('Courier', 20,), background='#d5f40b', foreground='#090a03')
text_5.insert(1.0, f'Level: {level}')
# text_6 = tk.Text(root, width=14, height=1, font=('Courier', 20,), background='#d5f40b', foreground='#090a03')
# text_6.insert(1.0, f'Time left: {time_left}')
label = tk.Label(root, text=f'Time left: {time_left}', font=('Courier', 20,), background='#d5f40b', foreground='#090a03')

text_1.grid(row=0, column=0, columnspan=4)
entry.grid(row=1, column=0, columnspan=4)
# text_6.grid(row=2, column=0, columnspan=4)
label.grid(row=2, column=0, columnspan=4)
text_2.grid(row=3, column=0)
text_3.grid(row=3, column=1)
text_4.grid(row=3, column=2)
text_5.grid(row=3, column=3)
button_1.grid(row=4, column=0, columnspan=2)
button_2.grid(row=4, column=2, columnspan=2)

root.mainloop()
