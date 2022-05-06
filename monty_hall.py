from tkinter import *
from tkinter import ttk
import pickle
import tkhtmlview
from PIL import Image, ImageTk
from Modules import bubble, Door, Player, Animation
import random
import pygame
import webbrowser

# <----------- Global Variables ------------->
tips_html = '''
<h1 style="text-align: center"> How to Play </h1>
<ol style="font-family: consolas; font-size: 20px">
<li>You will play 2 times – one without switching and one with switching  </li>
<li>But first you have to choose how many times you want to play in one round </li>
<li>And at last, you will get to see result of this match </li>
<li>
We will provide you even an excel sheet of result 
You can save it locally on your desktop
</li>
<li> Minimum rounds = 10 </li>
</ol>
'''  # Html string for Tips Label

my_profiles = ["https://github.com/PankajVishw50",
               "https://www.linkedin.com/in/pankaj-vishw-4802a9232/"]

pygame.init()  # Initializing Pygame for media player


# <---------- Other Functions -------------->

# To redirect to my Social media profiles
def redirect_profile(x):
    root.update()
    webbrowser.open(my_profiles[x])


# Page Scrolling Feature
def mouse_scroll(event):  # Mouse Scrolling Page Fucntion
    my_canvas.yview_scroll(int(-1 * event.delta / 120), "units")


# Making Button Dynamic
def change_img(object, img):
    object.configure(image=img)


# Deleting Frames and Window
def forget(object):
    for item in object:
        item.forget()


# Redirecting To Home/Tutorial Page
def redirect():
    # Deleting all useless Data
    user.norm_round.clear()
    user.switch_round.clear()
    forget([result_frame])

    # Configuring new Button Image
    header_button.config(image=play_inactive_image, command=round_counter, state=NORMAL)
    header_button.bind("<Enter>", lambda e: change_img(header_button, play_active_image))
    header_button.bind("<Leave>", lambda e: change_img(header_button, play_inactive_image))

    set_tutorial()
    root.update()


# To Add User's Round Choice into Input Box
def value_add(value, object):
    global round_value

    # Fetching data from Text field
    var = int(object.get("1.0", "end-1c"))
    object.config(state=NORMAL)

    # Inserting Logic
    if value > 0 and var > 10:
        object.delete("1.0", "end")
        object.insert("end", " " + str(var - 1))

    if value < 0:
        object.delete("1.0", "end")
        object.insert("end", " " + str(var + 1))

    # Fetching data
    round_value = int(object.get("1.0", "end-1c"))
    object.config(state=DISABLED)


# Switching Door Logic
def switch(item, host_opened):
    global switch_loop, user_choice

    # Deleting animation
    door_canvas.delete(animation.pointer)
    root.update()

    for x in [first_door, second_door, third_door]:
        if x != item and x != host_opened:
            x.selected = True
            user_choice = x
            animation.door_locater(user_choice.door_no)
        else:
            x.selected = False

    switch_loop = False


# Setting Door
def door():
    global close_door_img, close_door_image
    global open_door_car_img, open_door_goat_img
    global open_door_car_image, open_door_goat_image
    global first_door, second_door, third_door
    global switch_img, switch_image, switch_label

    close_door_img = Image.open("Resources/Closed_Door.png")
    close_door_image = ImageTk.PhotoImage(close_door_img)

    open_door_car_img = Image.open("Resources/opened_door_car.png")
    open_door_car_image = ImageTk.PhotoImage(open_door_car_img)
    open_door_goat_img = Image.open("Resources/opened_door_goat.png")
    open_door_goat_image = ImageTk.PhotoImage(open_door_goat_img)

    first_door = Door(door_canvas, 1,
                      close_door_image, open_door_goat_image, open_door_car_image)
    door_canvas.create_window((250, 200), window=first_door.close_door_label)
    first_door.close_door_label.config(command=first_door.select_door)

    second_door = Door(root, 2,
                       close_door_image, open_door_goat_image, open_door_car_image)
    door_canvas.create_window((650, 200), window=second_door.close_door_label)
    second_door.close_door_label.config(command=second_door.select_door)

    third_door = Door(root, 3,
                      close_door_image, open_door_goat_image, open_door_car_image)
    door_canvas.create_window((1050, 200), window=third_door.close_door_label)
    third_door.close_door_label.config(command=third_door.select_door)

    switch_img = Image.open("Resources/Switch_inactive_button.png")
    switch_image = ImageTk.PhotoImage(switch_img)
    switch_label = Button(door_canvas, image=switch_image, bd=0)
    door_canvas.create_window((600, 450), window=switch_label)


# <----------- Main Functions -------------->

# To start the Programme
def init():
    global user

    # Loading User Object
    try:
        with open("User.obj", "rb") as file:
            user = pickle.load(file)
    except:
        user = Player()

    # Redirecting further
    set_tutorial()


# Setting the Home/Tutorial page
def set_tutorial():
    global my_canvas, main_frame, my_scroll

    # <----- Main Frame ----->
    main_frame = Frame(root, bg="#bababa")
    main_frame.pack(fill=BOTH, pady=(0, 0), expand=True)

    # <------ Canvas ------->
    my_canvas = Canvas(main_frame, bg="#F4FCD9")
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # <------- ScrollBar ------->
    my_scroll = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scroll.pack(side=RIGHT, fill=Y)

    # <------ Binding Canvas to Scrollbar ------->
    my_canvas.configure(yscrollcommand=my_scroll.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    my_canvas.bind_all("<MouseWheel>", mouse_scroll)

    # <-------- Second Frame --------->
    second_frame = Frame(my_canvas, bg="#F4FCD9")

    # Packing second screen to canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor="ne")

    # Redirecting further
    html_page(second_frame)


# Setting the Tutorial Text and Images
def html_page(second_frame):
    global img_1, image_1, img_2, image_2, img_3, image_3, img_4, image_4, img_5, image_5, img_6, image_6
    global img_7, image_7, img_8, image_8, img_9, image_9, img_10, image_10, img_11, image_11, img_12, image_12

    # <----------- Text and stylised Images ------------->
    img_1 = Image.open("Resources/Html resources/1.Intro.png")  # First Image
    image_1 = ImageTk.PhotoImage(img_1)
    tut_story_1 = bubble(second_frame, image_1, (300, 10), (25, 0))

    img_2 = Image.open("Resources/Html resources/2.what.png")  # Second Image
    image_2 = ImageTk.PhotoImage(img_2)
    tut_story_2 = bubble(second_frame, image_2, (5, 500))

    img_3 = Image.open("Resources/Html resources/3.suppose.png")  # Third Image
    image_3 = ImageTk.PhotoImage(img_3)
    tut_story_3 = bubble(second_frame, image_3, (25, 10))

    img_4 = Image.open("Resources/Html resources/4.host_suppose.png")  # Fourth Image
    image_4 = ImageTk.PhotoImage(img_4)
    tut_story_4 = bubble(second_frame, image_4, (350, 10))

    img_5 = Image.open("Resources/Html resources/5.most_people.png")  # Fifth Image
    image_5 = ImageTk.PhotoImage(img_5)
    tut_story_5 = bubble(second_frame, image_5, (200, 10))

    img_6 = Image.open("Resources/Html resources/6.your_first.png")  # Sixth Image
    image_6 = ImageTk.PhotoImage(img_6)
    tut_story_6 = bubble(second_frame, image_6, (3, 600))

    img_7 = Image.open("Resources/Html resources/7.all_probability.png")  # Seventh Image
    image_7 = ImageTk.PhotoImage(img_7)
    tut_story_7 = bubble(second_frame, image_7, (500, 10), 20)

    img_8 = Image.open("Resources/Html resources/8.Asset.png")  # Eight Image
    image_8 = ImageTk.PhotoImage(img_8)
    tut_story_8 = bubble(second_frame, image_8, (200, 10))

    img_9 = Image.open("Resources/Html resources/9.Asset.png")  # Ninth Image
    image_9 = ImageTk.PhotoImage(img_9)
    tut_story_9 = bubble(second_frame, image_9, (25, 400))

    img_10 = Image.open("Resources/Html resources/10.Asset.png")  # Tenth Image
    image_10 = ImageTk.PhotoImage(img_10)
    tut_story102 = bubble(second_frame, image_10, (600, 10))

    img_11 = Image.open("Resources/Html resources/11.Asset.png")  # Eleventh Image
    image_11 = ImageTk.PhotoImage(img_11)
    tut_story_11 = bubble(second_frame, image_11, (25, 250))

    img_12 = Image.open("Resources/Html resources/12.Asset.png")  # Twelfth Image
    image_12 = ImageTk.PhotoImage(img_12)
    tut_story_12 = bubble(second_frame, image_12, (25, 10), (10, 50))


# Asking For User's Input
def round_counter():
    global plus_count_img, plus_count_image
    global minus_count_image, minius_count_image
    global start_inactive_img, start_inactive_image, start_active_img, start_active_image
    global tips_label, round_value

    # <------- To destroy previous Frames ------->
    forget([main_frame])

    # <--------- Setting Images and Configuring Button ----------->

    start_inactive_img = Image.open("Resources/Start_inactive_button.png")
    start_inactive_image = ImageTk.PhotoImage(start_inactive_img)
    start_active_img = Image.open("Resources/Start_active_button.png")
    start_active_image = ImageTk.PhotoImage(start_active_img)

    # Configure Header button to redirect to main()
    header_button.config(image=start_inactive_image, command=main)
    header_button.bind("<Enter>", lambda e: change_img(header_button, start_active_image))
    header_button.bind("<Leave>", lambda e: change_img(header_button, start_inactive_image))

    # <------------ New Frame for Tips ------------->
    tips_label = Frame(root)
    tips_label.pack(side=TOP, fill=BOTH, padx=25, expand=True)

    # Html Label
    playing_rules = tkhtmlview.HTMLLabel(tips_label, html=tips_html)
    playing_rules.pack(fill=BOTH, expand=True)

    # <---------- Widget for counting round ----------->
    # For Subtraction
    minus_count_img = Image.open("Resources/Minus_inactive_button.png")
    minus_count_image = ImageTk.PhotoImage(minus_count_img)
    minus_counter_button = Button(tips_label, image=minus_count_image, bd=0, activebackground=None,
                                  command=lambda: value_add(1, input_field))
    minus_counter_button.place(relx=0.35, y=400)

    # Input Field
    input_field = Text(tips_label, height=1, width=3, font="Forte 40")
    input_field.place(relx=0.45, y=410)
    input_field.insert("end", " 10")
    round_value = int(input_field.get("1.0", "end-1c"))
    input_field.config(state=DISABLED)

    # For Addiction
    plus_count_img = Image.open("Resources/Plus_inactive_button.png")
    plus_count_image = ImageTk.PhotoImage(plus_count_img)
    plus_count_button = Button(tips_label, image=plus_count_image, bd=0, activebackground=None,
                               command=lambda: value_add(-1, input_field))
    plus_count_button.place(relx=0.55, y=400)

    # Placeholder
    rounds_label = Label(tips_label, text="   rounds", fg="Grey")
    rounds_label.place(relx=0.46, y=480)


# Main Function
def main():
    global door_canvas, round_value
    global animation, user

    # <----------- Destroying Previous frames -------------->
    forget([tips_label])

    # Configure Header Button
    header_button.config(state=DISABLED, image=None, bd=0)

    # <--------- New Canvas -----------
    door_canvas = Canvas(root, height=600)
    door_canvas.pack(side=TOP, fill=X)

    # Calling out door function to set up
    door()

    # Creating an Animation object
    animation = Animation(root, door_canvas)

    round_counter_label = Label(door_canvas, text=f"Normal Round 1/{round_value}", fg="#c9c9c7")
    door_canvas.create_window((625, 500), window=round_counter_label)

    # <-------- Main Loop --------->
    for method in range(1, 3):
        # Round User Chooses to Play for each Mode
        for round_no in range(1, round_value + 1):
            user_input = True
            switch_label.config(state=DISABLED)


            # To Display which mode is running right now
            if method == 1:
                round_counter_label.configure(text=f"Normal Round {len(user.norm_round)}/{round_value}")
            else:
                round_counter_label.configure(text=f"Switching Round {len(user.switch_round)}/{round_value}")

            # While Loop to check user input
            while user_input:
                for item in [first_door, second_door, third_door]:
                    if item.selected:
                        global user_choice
                        user_choice = item
                        switch_label.config(state=DISABLED)
                        car_door = random.choice([first_door, second_door, third_door])
                        animation.door_locater(item.door_no)

                        # Disabling other Door button
                        if item == first_door:
                            second_door.close_door_label.configure(state=DISABLED)
                            third_door.close_door_label.configure(state=DISABLED)
                        elif item == second_door:
                            first_door.close_door_label.config(state=DISABLED)
                            third_door.close_door_label.config(state=DISABLED)
                        elif item == third_door:
                            first_door.close_door_label.config(state=DISABLED)
                            second_door.close_door_label.config(state=DISABLED)

                        root.update()

                        # switching logic
                        if method == 2:
                            for hostx in [first_door, second_door, third_door]:
                                if hostx != user_choice and hostx != car_door:
                                    global host_opened
                                    host_opened = hostx
                                    hostx.close_door_label.config(image=open_door_goat_image)
                                    break

                            global switch_loop
                            switch_loop = True
                            switch_label.config(state=NORMAL,
                                                command=lambda: switch(item, host_opened))

                            # While Loop for user to Choose Switch Option
                            while switch_loop:
                                root.update()

                        # Win or Loose Logic
                        if car_door == user_choice:

                            # Playing Win Sound
                            pygame.mixer.music.load("Resources/media/win_sound.wav")
                            pygame.mixer.music.play()

                            # Storing data into Database
                            if method == 1:
                                user.norm_round.append("Win")
                            else:
                                user.switch_round.append("Win")

                        else:
                            # Fail sound
                            pygame.mixer.music.load("Resources/media/lose_sound.wav")
                            pygame.mixer.music.play()

                            # Storing data into database
                            if method == 1:
                                user.norm_round.append("Lose")
                            else:
                                user.switch_round.append("Lose")

                        # Opening Door
                        for x in {first_door, second_door, third_door, car_door}:
                            if x == car_door:
                                x.close_door_label.config(image=open_door_car_image)
                            else:
                                x.close_door_label.config(image=open_door_goat_image)

                        animation.switch_animation()

                        # Configuring For next Round
                        first_door.selected = False
                        second_door.selected = False
                        third_door.selected = False
                        user_input = False
                        door_canvas.delete(animation.pointer)

                        for x in [first_door, second_door, third_door]:
                            x.close_door_label.config(image=close_door_image)

                first_door.close_door_label.config(state=NORMAL)
                second_door.close_door_label.config(state=NORMAL)
                third_door.close_door_label.config(state=NORMAL)

                root.update()

    # Redirecting further
    result()


# To Prepare Result
def result():
    global result_frame
    global home_inactive_img, home_inactive_image, home_active_img, home_active_image
    global save_inactive_img, save_inactive_image, save_active_img, save_active_image

    # <------ Destroying Previous Frames --------->
    forget([door_canvas])

    # <------ Configure Header Button ------>
    home_inactive_img = Image.open("Resources/home_inactive_button.png")
    home_inactive_image = ImageTk.PhotoImage(home_inactive_img)

    home_active_img = Image.open("Resources/home_active_button.png")
    home_active_image = ImageTk.PhotoImage(home_active_img)

    header_button.config(image=home_inactive_image, command=redirect, state=NORMAL)
    header_button.bind("<Enter>", lambda e: change_img(header_button, home_active_image))
    header_button.bind("<Leave>", lambda e: change_img(header_button, home_inactive_image))

    # <--------- New Frame For result ----------->
    result_frame = Frame(root)
    result_frame.pack(fill=BOTH, expand=True, pady=(0, 200))

    # To Display normal round data
    norm_frame = LabelFrame(result_frame, width=640)
    norm_frame.pack(fill=Y, expand=True, side=LEFT, anchor="w")
    norm_frame.pack_propagate(0)
    normal_label = Label(norm_frame, text="Normal Round",
                         font="Courier")
    normal_label.pack(side=TOP)

    # To Display Switch round data
    switch_frame = LabelFrame(result_frame, width=640)
    switch_frame.pack(fill=Y, expand=True, side=RIGHT, anchor="e")
    switch_frame.pack_propagate(0)
    switch_text_label = Label(switch_frame, text="Switch Round",
                              font="Courier")
    switch_text_label.pack(side=TOP)

    # <---------- Preparing Result ----------->
    norm_round_win = user.norm_round.count("Win")
    norm_round_lose = user.norm_round.count("Lose")

    switch_round_win = user.switch_round.count("Win")
    switch_round_lose = user.switch_round.count("Lose")

    norm_win_percentage = (user.norm_round.count("Win") * 100) // round_value
    switch_win_percentage = (user.switch_round.count("Win") * 100) // round_value

    # <-------- Widget To display result ---------->
    # For Normal Mode
    norm_match_label = Label(norm_frame, text="Total Match:", font="Corbel")
    norm_match_value = Label(norm_frame, text=round_value, font="Corbel")
    norm_match_label.place(x=50, y=50)
    norm_match_value.place(x=570, y=50)

    norm_win_label = Label(norm_frame, text="Win", font="Corbel")
    norm_win_value = Label(norm_frame, text=norm_round_win, font="Corbel")
    norm_win_label.place(x=50, y=100)
    norm_win_value.place(x=570, y=100)

    norm_lose_label = Label(norm_frame, text="Lose", font="Corbel")
    norm_lose_value = Label(norm_frame, text=norm_round_lose, font="Corbel")
    norm_lose_label.place(x=50, y=150)
    norm_lose_value.place(x=570, y=150)

    norm_per_label = Label(norm_frame, text="Win Percentage", font="Corbel")
    norm_per_value = Label(norm_frame, text=f"{norm_win_percentage} %", font="Roboto")
    norm_per_label.place(x=50, y=200)
    norm_per_value.place(x=570, y=200)

    # For Switch Mode
    switch_match_label = Label(switch_frame, text="Total Match:", font="Corbel")
    switch_match_value = Label(switch_frame, text=round_value, font="Corbel")
    switch_match_label.place(x=50, y=50)
    switch_match_value.place(x=570, y=50)

    switch_win_label = Label(switch_frame, text="Win", font="Corbel")
    switch_win_value = Label(switch_frame, text=switch_round_win, font="Corbel")
    switch_win_label.place(x=50, y=100)
    switch_win_value.place(x=570, y=100)

    switch_lose_label = Label(switch_frame, text="Lost", font="Corbel")
    switch_lose_value = Label(switch_frame, text=switch_round_lose, font="Corbel")
    switch_lose_label.place(x=50, y=150)
    switch_lose_value.place(x=570, y=150)

    switch_per_label = Label(switch_frame, text="Win Percentage", font="Corbel")
    switch_per_value = Label(switch_frame, text=f"{switch_win_percentage} %", font="Roboto")
    switch_per_label.place(x=50, y=200)
    switch_per_value.place(x=570, y=200)

    # <--------- Save File Button >
    save_inactive_img = Image.open("Resources/save_inactive_button.png")
    save_inactive_image = ImageTk.PhotoImage(save_inactive_img)

    save_active_img = Image.open("Resources/save_active_button.png")
    save_active_image = ImageTk.PhotoImage(save_active_img)

    save_file_button = Button(root, image=save_inactive_image, bd=0,
                              command=save)
    save_file_button.bind("<Enter>", lambda e: change_img(save_file_button, save_active_image))
    save_file_button.bind("<Leave>", lambda e: change_img(save_file_button, save_inactive_image))
    save_file_button.place(x=500, y=550)


# Completing and saving important files
def save():
    user.play_time += 1
    user.save_worksheet()

    # <---------- Saving user object --------->
    user.norm_round.clear()
    user.switch_round.clear()

    with open("User.obj", "wb") as file:
        pickle.dump(user, file)


# <----------- Root Window ------------->
root = Tk()
root.geometry("1280x720")
root.resizable(False, False)
root.title("Monty Hall")
root.iconbitmap("Resources/logo.ico")

# <------ Absolute Header ------->
header = Frame(root, bg="Yellow", height=50, bd=3)
header.pack(side=TOP, fill=X, anchor="n")

# <------- Monty Hall header text ---------->
monty_label = Label(header, text="Monty Hall", bg="Yellow", font=("Cascadia Code", 25))
monty_label.pack(side=TOP, pady=10)

# <------ Play Button ----->
play_inactive_img = Image.open("Resources/Play_inactive_button.png")
play_inactive_image = ImageTk.PhotoImage(play_inactive_img)
play_active_img = Image.open("Resources/Play_active_button.png")
play_active_image = ImageTk.PhotoImage(play_active_img)
header_button = Button(header, image=play_inactive_image, bd=0,
                       bg="Yellow", activebackground="Yellow",
                       command=round_counter)
header_button.place(x=1100, y=5)

header_button.bind("<Enter>", lambda e: change_img(header_button, play_active_image))
header_button.bind("<Leave>", lambda e: change_img(header_button, play_inactive_image))

# <-------- My Profiles ---------->
# Github
github_label = Button(header, text="Github", font="Argentina 13",
                      fg="black", bg="#FAF5E4",
                      activebackground="Beige", activeforeground="Brown",
                      command=lambda: redirect_profile(0))

# Linkedin
linkedin_label = Button(header, text="Linkedin", font="Argentina 13",
                        fg="Black", bg="#FAF5E4",
                        activebackground="Beige", activeforeground="Brown",
                        command=lambda: redirect_profile(1))

github_label.pack(side=LEFT, anchor="w")
linkedin_label.pack(side=LEFT, anchor="w")

# <------------ Footer ---------------->

init()  # starting the program
root.mainloop()
