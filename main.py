from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
german_dict = {}
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/german_words.csv")
    german_dict = original_data.to_dict(orient="records")
else:
    german_dict = data.to_dict(orient="records")

# ---------------------------- Create Flashcards ------------------------------- #


def create_flashcards():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(german_dict)
    canvas.itemconfig(flashcard_title, text="German", fill="black")
    canvas.itemconfig(flashcard_word, text=current_card["German"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(flashcard_title, text="English", fill="white")
    canvas.itemconfig(flashcard_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back_img)


def is_known():
    german_dict.remove(current_card)
    create_flashcards()
    data_file = pandas.DataFrame(german_dict)
    data_file.to_csv("data/words_to_learn.csv", index=False)
    create_flashcards()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
flashcard_title = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
flashcard_word = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Images
right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")

# Buttons
wrong_button = Button(image=wrong_img, highlightthickness=0, command=create_flashcards)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

create_flashcards()


window.mainloop()
