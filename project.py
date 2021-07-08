import tkinter as tk
from tkinter import Entry, IntVar, Tk
import random

def quit_frame():
    main.destroy()

#used to generate the GUI for the sudoku board
#https://python-forum.io/Thread-Tkinter-Sudoku-solver-with-tkinter
def SquareCreate():
    sq = []
    for j in range(0, 9):
        for i in range(0,9):
            data = IntVar()
            t = tk.Entry(main, textvariable=data, justify="center",font=("Arial",16))
            ixtra=0
            jxtra=0
            if i > 2:
                ixtra=4
            if i > 5:
                ixtra=8
            if j > 2:
                jxtra=4
            if j > 5:
                jxtra=8
            t.place(x=i*40+70+ixtra, y=j*40+80+jxtra, width=40, height=40)
            t.delete(0)
            sq.append(data)
    return sq



#returns a 2d array of the sudoku board
def get_board():
    board = []
    #loop through each row
    for x in range(0,9):
        row = []
        #loop through each column
        for y in range(0,9):
            try:
                #if board has value add to the row
                row.append(Square[(x*9)+y].get())
            except:
                #if square is empty add to row as zero
                row.append(0)
        #add row to board
        board.append(row)
    #return board for other functions
    return board

#check if the board is completed correctly
#no return but will update puzzle status
def check():
    #get board state
    board = get_board()
    #checks if board has any empty spaces and returns false if there are
    if find_empty(board):
        return False
    #loop through each cell
    for i in range(0,81):
        row=i//9
        col=i%9
        #store value of cell number
        num = board[row][col]
        #returns false if number is not 1-9
        if (num < 1 or num > 9):
            return False
        #zero out that number to check
        board[row][col] = 0
        #check if number in the cell is valid
        if not cell_check(board,row,col,num):
            board[row][col] = num
            return False
        #add number back to cell regardless of correctness
        board[row][col] = num
    #Update puzzle status
    status.config(text="Puzzle Status: Complete")

#helper function used to create a board
#calls create() to fill out board completely then
#calls remove_numbers() to ready the board for play
def crate():
    board = get_board()
    create(board)
    remove_numbers()

#fills in a correct solution for the board
def solve():
    board = get_board()
    create(board)

#takes current board, the row column and value of number
#being placed
#returns true if valid placement or false if not
def cell_check(board,row,col,num):
    #checks if number already exists in the row
    if num in board[row]:
        return False
    #creates a list of values in the column
    column = []
    for x in range(0,9):
        column.append(board[x][col])
    #checks if number already exists in the column
    if num in column:
        return False

    #creates the square list which will be one of the 9 squares on the board
    square = []

    #determines which 3x3 the cell is in
    #and sets i and j values to be used to generate the list
    i = 0
    j = 0
    if row<3:
        i = 0
        if col<3:
            j = 0
        elif col<6:
            j = 3
        else:
            j = 6
    elif row<6:
        i = 3
        if col<3:
            j=0
        elif col<6:
            j=3
        else:
            j=6
    else:
        i=6
        if col<3:
            j=0
        elif col<6:
            j=3
        else:
            j=6
    #gets the values of the 3x3 that the cell is in
    for x in range(i, i+3):
        for y in range(j, j+3):
            square.append(board[x][y])
    #checks if number is in the 3x3
    if num in square:
        return False
    return True

#checks if there are any empty values on the board
#retruns true if there is an empty value or false if full
def find_empty(board):
    for x in range(0,9):
        for y in range(0,9):
            if board[x][y] == 0:
                return True
    return False


#creates the board and used in solving puzzle
#Solving function was adapted from 
#https://lvngd.com/blog/generating-and-solving-sudoku-puzzles-python/
def create(board):
    #setup number values
    numbers = [1,2,3,4,5,6,7,8,9]
    #loop through each cell
    for x in range(0,81):
        #get row and column
        row=x//9
        col=x%9
        #checks if value is empty 
        if board[row][col]==0:
            #randomizes integers
            random.shuffle(numbers)
            #loops through each possible number
            for num in numbers:
                #checks if the selected number is a valid entry
                if cell_check(board,row,col,num):
                    #updates board and cell value
                    Square[x].set(num)
                    board[row][col]=num
                    #if board is full then return true
                    if not find_empty(board):
                        return True
                    #if board is not full then pass back loop to create function
                    else:
                        if create(board):
                            return True
            #if not possible break loop
            break
    #empty cell from invalid entry
    board[row][col]=0
    #returns false on the "if create(board)" check
    return False

#removes numbers from the completed board
def remove_numbers():
    number_list = []
    for x in range(0,81):
        number_list.append(x)

    count = 81

    #gets number of starting hints minimum 17
    user = int(e.get())   
    diff = max(user, 17)
    diff = min(diff, 81)
    
    #randomly removes cells until number of hints selected are left
    while count > diff:

        #get random cell
        num = random.randint(0,count)
        #clear cell contents
        Square[number_list[num]].set('')
        #swap selected cell number with ending cell value
        number_list[num] = number_list[count-1]
        #decrement remaining cells remaining
        count -= 1
    #update puzzel status to incomplete when starting new puzzle
    status.config(text="Puzzle Status: Incomplete")

#clears all values from the board
#and updates board status
def clear_board():
    for i in range(0,81):
        Square[i].set('')
    status.config(text="Puzzle Status: Incomplete")



 
#Sets up the board and buttons
main = tk.Tk()
main.geometry("500x540")
main.resizable(width=0, height=0)
main.title("Sudoku")
status = tk.Label(main, text="Puzzle Status: Incomplete")
status.place(x=0, y=0)
button1=tk.Button(main, text="quit", command = quit_frame)
button1.place(x=50,y=450)
button2=tk.Button(main, text="generate", command = crate)
button2.place(x=100, y=450)
button4=tk.Button(main, text='clear', command = clear_board)
button4.place(x=200, y=450)
button5=tk.Button(main, text='check', command = check)
button5.place(x=250, y=450)
button6=tk.Button(main, text='solve', command = solve)
button6.place(x=300, y=450)
label1=tk.Label(text="Starting Hints:")
label1.place(x=0,y=30)
data = IntVar()
e=tk.Entry(main,textvariable=data)
data.set(24)
e.place(x=80,y=30)
Square=SquareCreate()
main.mainloop()
