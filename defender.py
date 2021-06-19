# Import socket module
import socket

# Import pickle module
import pickle

# Import Scoring module
from tkinter import messagebox, Label, Radiobutton, Frame, Button, Tk, IntVar

# Import the Scoring module to use the class Score
import Scoring

# Import Tabulate library to create a table
from tabulate import tabulate

# Import generateHammingCode function from HammingCode module
from HammingCode import checkError, decodeHammingCode

# Import the tkinter module. It is the standard Python interface to the Tk GUI toolkit.
from tkinter import Text

# import datetime function from datetime module
from datetime import datetime

# The attacker has a value 1 and the defender has a value 2 so we define
# a players list to check if the user select one of these options
players = [1, 2]

# The selection variable is used to hold the sentence
# "You selected the {option}" when the user select an option
slection = ''


# The function run() will run when the player clicks the button play on the window prompt
def run():
    # username = str(text1_widget.get(1.0, 'end'))
    if int(var.get()) == 1:
        name = "Attacker"
    else:
        name = "Defender"
    LIMIT = int(text_widget.get(1.0, 'end'))
    root1.destroy()
    HEADER_SIZE = 10

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # create an instance score of the class Scores and initiate the values to 0
    score = Scoring.Scores(0, 0)

    # connect to the server on local computer
    s.connect((socket.gethostname(), 1500))

    new_msg = True
    msg_len = 0

    # an infinite loop until we interrupt it or an error occurs
    while True:

        full_msg = b''
        while True:

            str_data = ''
            msg = s.recv(7)
            now = datetime.now()
            r_time = datetime.timestamp(now)

            # If the message is a new_msg, then the first thing we do is parse the header,
            # which we already know is a fixed-length of 10 characters.
            if new_msg:
                msg_len = int(msg[:HEADER_SIZE])
                new_msg = False

            # Build the full_msg
            full_msg += msg

            # we continue to build the full_msg, until that var
            # is the size of msglen + our HEADER_SIZE.
            if len(full_msg) - HEADER_SIZE == msg_len:
                print("full message received:")
                d = pickle.loads(full_msg[HEADER_SIZE:])
                received_message = d['scrambled_msg']

                # calculate the round trip time and print the result
                rtt_time = r_time - d['rtt']
                print("RTT = ", rtt_time)
                if rtt_time > 0.002:
                    print("TIMEOUT")
                    score.addPointsForDefender_RTT()
                else:
                    # we should run the error correction algorithm here on received_message
                    # then decode it and convert it to string using hamming code functions
                    for c in received_message:
                        checkError(c)
                        str_data += chr(int(decodeHammingCode(c), 2))
                    print(str_data)

                    if str_data == "ATTACK":
                        score.addPointsForAttacker()
                    else:
                        score.addPointsForDefender()

                score.checkScores()
                new_msg = True

                # if the we reach the number of rounds entered by the user,
                # the connection will close by sending an end message to the user
                if score.Count == LIMIT:
                    more = 'end'
                    break
                print()
                # we send again in order to continue our game
                more = 'again'
                score.Count += 1
                print()
                s.send(more.encode())
                break

        if more == 'end':
            break

    # To know who's winning
    if score.getPointsForAttacker() > score.getPointsForDefender():
        winner = 'Attacker'
    elif score.getPointsForAttacker() == score.getPointsForDefender():
        winner = 'tie'
    else:
        winner = 'Defender'

    # A label widget will appear depending on the winner
    if winner == name:
        youwin = "YOU WIN!"
    elif winner == 'tie':
        youwin = "IT'S A TIE!"
    else:
        youwin = "YOU LOSE!"

    s.close()

    # the client code is over, so now we will configure the GUI to show the result of the game
    # Just explained in detail in the end of the script

    # create another window
    root = Tk()
    # set the title of the window to Network Game
    root.title("Network Game")
    # change the background color of the window to white
    root.config(bg="#fff")
    # change the size of the window to width=600px and height=400px
    root.geometry("600x400")
    # Create a label widget to hold the text Scores
    Label(root, text="Scores", font="Serif 18 bold", bg="#fff").pack()
    Label(root, text="", font="Serif 18 bold", bg="#fff").pack()
    # This label will show who won
    Label(root, text=youwin + '\n', font="Serif 14 bold", bg="#fff").pack()

    # Now we will create a table that shows the score our table has 3 rows and 2 columns
    # First row will be the header row [Users  Scores]
    # Second row will contains the attacker player and it's score [Attacker score]
    # Third row will contains the attacker player and it's score [Defender score]

    # The header row for our table
    header = ['Users', 'Scores']

    # The data of our table will be as tuple inside a list[(attacker,score),(defender,score)]
    data = [('Attacker', score.getPointsForAttacker()), ('Defender', score.getPointsForDefender())]

    # a function called tabulate used to print our table has 3 attributes:
    # The first argument is the data of the table as a list or another tabular data type
    # The second optional argument named headers defines a list of column headers to be used:
    # The third optional argument named 'tablefmt' defines how the table is formatted.
    Label(root, text=tabulate(data, headers=header, tablefmt='fancy_grid'), font="Serif 14 bold").pack()
    global selection
    Label(root, text="\n\n" + selection + '\n', font="Serif 14 bold", bg="#fff").pack()
    root.mainloop()


# The sel() function  used to configure the attribute text of the
# label widget in the window with the specific option the user selected
def sel():
    global selection
    if int(var.get()) == 1:
        selection = "You selected the Attacker"
    else:
        selection = "You selected the Defender"
    label.config(text=selection)


# The check() function check is the user fill the input form
def check():
    # if the user didn't choose an option a showerror message will prompt
    if int(var.get()) not in players:
        messagebox.showerror("Warning", "Please select an option")
        return
    # if the user didn't enter anything a showerror message will prompt
    if len(text_widget.get(1.0, 'end').strip()) == 0:
        messagebox.showerror("Warning", "Enter how many round you need to play")
        return
    run()


# To create a main window, tkinter offers a method Tk().Creating Window to put Widgets.
root1 = Tk()

# Change the title of the window
root1.title("Network game")

# Setup the window size widthxheigh
root1.geometry('500x300')

# change the background of the window to white
root1.config(bg='#fff')

# holds an integer default 0
var = IntVar()

# The Label widget is used to provide a single-line caption for other widgets.
Label(root1, text='Choose your option:', font="Helvetica 12 bold ", bg="#fff").pack(anchor='w', padx=10, pady=10)

# The Button widget is used to display buttons in your application.
R1 = Radiobutton(root1, text="Attacker", variable=var, value="1", font="Serif 12 normal", bg="#fff", command=sel)
# The Pack geometry manager packs widgets in rows or columns. We can use options like fill, expand, and side to
# control this geometry manager.
R1.pack(anchor='w', padx=25)

R2 = Radiobutton(root1, text="Defender", variable=var, value="2", font="Serif 12 normal", bg="#fff", command=sel)
R2.pack(anchor='w', padx=25)

label = Label(root1, font="Serif 12 bold", bg="#fff", fg="#ee343f")
label.pack()

Label(root1, text="", bg="#fff").pack()

# The Frame widget is used as a container widget to organize other widgets.
frame = Frame(root1).pack(anchor='w')
Label(frame, text='Enter how many rounds you want to play:', font="Serif 12 bold", bg="#fff").pack(anchor='w', padx=10)
text_widget = Text(frame, width=15, height=1, font="Serif 12 ", bg="#fff", padx=10, pady=8, borderwidth=2)
text_widget.pack(anchor='w', padx=10)

Label(root1, text="", bg="#fff").pack()

button = Button(root1, text="Play", width=20, font="Serif 12 bold", command=check)
button.pack()

# mainloop() is used when your application is ready to run.
root1.mainloop()
