# A typing speed test in TKinter

from tkinter import *
import tkinter.font as tkFont
import random

# Globals to start app
timer_count = 0
end_time = 0
errors = 0

sentence_list = ["When I've built up my savings, I'll be able to travel to Mexico.",
                 "Wouldn't it be lovely to enjoy a week soaking up the culture?",
                 "The plots failed because of some trusted friends of the king.",
                 "After the death of the king, everyone wanted to be a king.",
                 "War does not bring anything good to the common people.",
                 "If opportunity doesn't knock, build a door."]


def user_input(*args):
    # Gets input from entry box and starts timer
    global typed_chars
    typed_chars = textbox.get()
    if timer_count == 0:
        typing_timer()


def typing_timer():
    # Updates timer
    global timer_count, timer
    timer_count += .1
    timer_canvas.itemconfig(timer_text, text=f'Timer: {round(timer_count,1)}')
    timer = window.after(100, typing_timer)  # Assign a variable to the timer
    if end_time != 0:
        window.after_cancel(timer)  # Stops timer by given variable


def print_result(*args):
    # Print results after user presses enter
    global end_time, errors
    end_time = round(timer_count, 1)
    # Stop timer and print ending time
    timer_canvas.itemconfig(timer_text, text=f'Timer: {end_time}')
    typing_wpm = (len(typed_chars)/5) / (end_time / 60)
    wpm_label.config(text=f'WPM = {int(typing_wpm)}')
    # Determine error rate - pass if typed text is longer than sentence
    for char_count, char in enumerate(typed_chars):
        try:
            if char != working_sentence[char_count]:
                errors += 1
        except IndexError:
            pass
    accuracy = int((char_count-errors) / char_count * 100)
    accuracy_label.config(text=f'Accuracy = {accuracy}%')


def reset_app():
    # Clears entry box, result print-outs, and timer reset
    global timer_count, end_time, errors, working_sentence
    # Stop timer - pass if timer isn't running
    try:
        window.after_cancel(timer)
    except NameError:
        pass
    # Clear text in entrybox
    textbox.delete(0, END)
    # Reset timer, WPM, errors
    timer_count = 0
    end_time = 0
    errors = 0
    timer_canvas.itemconfig(timer_text, text='Timer: 0')
    wpm_label.config(text=f'WPM =   ')
    accuracy_label.config(text=f'Accuracy =    ')
    # Print a new sentence
    working_sentence = random.choice(sentence_list)
    sentence_label.config(text=working_sentence)


# Set up window and define fonts
window = Tk()
user_text = StringVar()
window.title("Typing Speed Tester")
window.geometry('525x375')
window.resizable(width=False, height=False)
info_font = tkFont.Font(family='Helvetica', size=14, weight='bold')
sentence_font = tkFont.Font(family='Helvetica', size=12)
results_font = tkFont.Font(family='Helvetica', size=10, weight='bold')

# Game instructions
info_label = Label(text="Test your typing skills.\n\n"
                   + "Type the sentence below.\nPress return when finished "
                   + "and see your typing speed.", justify='center',
                   font=info_font)
info_label.grid(column=0, row=0, pady=10, padx=5)

# Text for "testing" sentence
working_sentence = random.choice(sentence_list)
sentence_label = Label(text=working_sentence, justify='center',
                       font=sentence_font)
sentence_label.grid(column=0, row=1, pady=20)

# Add a widget for user input text
textbox = Entry(width=50, textvariable=user_text, justify='center',
                font=sentence_font)
textbox.grid(column=0, row=2)
textbox.focus_set()

# Timer text
timer_canvas = Canvas(width=200, height=40, highlightthickness=0)
timer_text = timer_canvas.create_text(100, 20, text='Timer: 0',
                                      font=results_font)
timer_canvas.grid(column=0, row=3)
user_text.trace("w", user_input)

# WPM text
wpm_label = Label(text='WPM =   ', justify='center', font=results_font)
wpm_label.grid(column=0, row=4, pady=5)

# Typing Accuracy
accuracy_label = Label(text='Accuracy =    ', justify='center',
                       font=results_font)
accuracy_label.grid(column=0, row=5, pady=5)

# Reset Button
reset_button = Button(text="RESET", command=reset_app, font=results_font)
reset_button.grid(column=0, row=6, pady=10)

# Detect enter key
window.bind('<Return>', print_result)


window.mainloop()
