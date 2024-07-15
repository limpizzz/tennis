import tkinter
import time
import tkinter.messagebox


#задаем размеры холста
canvasWidth = 750
canvasHeight = 500

#распалагаем холст на окне
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight, bg="green")
canvas.pack()

#создаем ракетку и мяч
racquet = canvas.create_rectangle(0,0,40,10, fill="yellow")
ball = canvas.create_oval(0,0,10,10, fill="pink")

#создаем переменную для отслеживания за изменением окна
windowOpen = True
score = 0
reboundCount = 0

#создаем функцию, которая будет отслеживать изменения на игровом поле
def main_loop():
    while windowOpen == True:
        move_racquet()
        move_ball()
        window.update()
        time.sleep(0.02)
        if windowOpen == True:
            check_game_over()

#создаем переменые для работы с клавишами
leftPressed = 0
rightPressed = 0

#создаем функцию для нажатия клавиш
def on_key_press(event):
    global leftPressed, rightPressed
    if event.keysym == "Left":
        leftPressed = 1
    elif event.keysym == "Right":
        rightPressed = 1

#создаем функцию для отжатия клавиш
def on_key_release(event):
    global leftPressed, rightPressed
    if event.keysym == "Left":
        leftPressed = 0
    elif event.keysym == "Right":
        rightPressed = 0    

#создаем переменную для движения ракетки и напишем формулу для изменения этой переменной в заваисимсти от нажатой клавиши
racquetSpeed = 6 #это количество пикселей, на которое перемещается раектка при каждом обновлении экрана
def move_racquet():
    racquetMove = racquetSpeed*rightPressed - racquetSpeed*leftPressed
    (racquetLeft, racquetTop, racquetRight, racquetBottom) = canvas.coords(racquet)
    if (racquetLeft > 0 or racquetMove > 0) and (racquetRight < canvasWidth or racquetMove < 0):
        canvas.move(racquet, racquetMove, 0)

#создаем переменные для движения мячика
ballMoveX = 4
ballMoveY = -4

#оздаем переменные для обозначения касания мячика ракетки
setRacquetTop = canvasHeight-60
setRacquetBottom = canvasHeight-40

def move_ball():
    global ballMoveX, ballMoveY, score, reboundCount, racquetSpeed
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballMoveX > 0 and ballRight > canvasWidth:
        ballMoveX = -ballMoveX
    if ballMoveX < 0 and ballLeft < 0:
        ballMoveX = -ballMoveX
    if ballMoveY < 0 and ballTop < 0:
        ballMoveY = -ballMoveY
    if ballMoveY > 0 and ballBottom > setRacquetTop and ballBottom < setRacquetBottom:
        (racquetLeft, racquetTop, racquetRight, racquetBottom) = canvas.coords(racquet)
        if ballRight > racquetLeft and ballLeft < racquetRight:
            ballMoveY = -ballMoveY
            score = score + 1
            reboundCount = reboundCount + 1
            if reboundCount == 4:
                reboundCount = 0
                racquetSpeed = racquetSpeed +1
                if ballMoveX > 0:
                    ballMoveX = ballMoveX +1               
    canvas.move(ball, ballMoveX, ballMoveY)
    
#создаём функцию для проверки конца игры
def check_game_over():
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballTop > canvasHeight:
        print("Вы набрали " + str(score), "очко/очков")
        playAgain = tkinter.messagebox.askyesno(message="Погнали еще?")
        if playAgain == True:
            reset()
        else:
            close()

#создаём функцию для конца игры
def close():
    global windowOpen
    windowOpen = False
    window.destroy()

#создаём функцию для продолжения игры
def reset():
    global score, reboundCount, racquetSpeed
    reboundCount = 0
    racquetSpeed = 6
    global leftPressed, rightPressed
    global ballMoveX, ballMoveY
    leftPressed = 0
    rightPressed = 0
    ballMoveX = 4
    ballMoveY = -4
    canvas.coords(racquet, 10, setRacquetTop, 60, setRacquetBottom)
    canvas.coords(ball, 20, setRacquetTop-10, 30, setRacquetTop)
    score = 0

window.protocol("WM_DELETE_WINDOW", close)
window.bind("<KeyPress>", on_key_press)
window.bind("<KeyRelease>", on_key_release)

     

reset()
main_loop()

    
