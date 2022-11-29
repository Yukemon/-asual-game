import time
import copy
import random
import tkinter
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.ttk import Radiobutton


# функция вводных аргументов и создание окна игры
def start():
    global board  # Canvas
    global par_scale  # переменная пропорции масштаба
    global background  # Canvas
    global poz1_x  # позиция мыши
    global poz1_y  # позиция мыши
    global par_motion  # параметр определения ходы
    global copy_pole  # копия поля, для учета ходов компьютера

    # обозначение переменных
    par_scale = scale / 10  # для пропорции векторов
    poz1_x = -1  # для отладки
    poz1_y = - 1  # для отладки
    par_motion = -1  # параметр определение хода
    background = tkinter.Canvas(root, width=scale + 0.7 * scale, height=scale + 0.1 * scale, bg='grey')  # фон
    background.place(x=scale / 20, y=scale / 20, anchor=tkinter.NW)
    board = tkinter.Canvas(root, width=scale, height=scale)  # игровая зона
    board.place(x=scale / 20, y=scale / 20, anchor=tkinter.NW)

    create_place()  # создаем поле...
    # Выводим игровое поле. Первые 4 переменные pozy, pozx, pozy2, pox2, последняя фикс для случая в анимации.
    conclusion(-1, -1, -1, -1, 1)
    board.bind("<Motion>", position_1)  # отслеживаем движение мышки по полю
    board.bind("<Button-1>", position_2)  # нажатие левой кнопки
    # vibor() # сразу переход к выбору хода. Опционально включаем, выключаем мануал().
    manual()  # инструкция


# функция отрисовки позиций игрового поля
def create_place():
    global field
    # 0 = пустая клетка,
    # 1 и 5 гориз.фишка # 2 и 7 верт.фишка # 9 и 10 горизонт.квадрат # 11 и 12 верт.квадрат # игрок,
    # 3 и 6 гориз.фишка # 4 и 8   верт.фишка # 13 и 14 горизонт.квадрат # 15 и 16 верт.квадрат # компьютер
    # 17 - углы поворота

    field = [[17, 1, 5, 3, 6, 1, 5, 3, 6, 17],
             [4, 0, 0, 0, 0, 0, 0, 0, 0, 2],
             [8, 0, 0, 0, 0, 0, 0, 0, 0, 7],
             [2, 0, 0, 0, 0, 0, 0, 0, 0, 4],
             [7, 0, 0, 0, 0, 0, 0, 0, 0, 8],
             [4, 0, 0, 0, 0, 0, 0, 0, 0, 2],
             [8, 0, 0, 0, 0, 0, 0, 0, 0, 7],
             [2, 0, 0, 0, 0, 0, 0, 0, 0, 4],
             [7, 0, 0, 0, 0, 0, 0, 0, 0, 8],
             [17, 3, 6, 1, 5, 3, 6, 1, 5, 17]]
    # копия, если изменил поле
    # field = [[17, 1, 5, 3, 6, 1, 5, 3, 6, 17],
    #         [4,  0, 0, 0, 0, 0, 0, 0, 0, 2],
    #         [8,  0, 0, 0, 0, 0, 0, 0, 0, 7],
    #         [2,  0, 0, 0, 0, 0, 0, 0, 0, 4],
    #         [7,  0, 0, 0, 0, 0, 0, 0, 0, 8],
    #         [4,  0, 0, 0, 0, 0, 0, 0, 0, 2],
    #         [8,  0, 0, 0, 0, 0, 0, 0, 0, 7],
    #         [2,  0, 0, 0, 0, 0, 0, 0, 0, 4],
    #         [7,  0, 0, 0, 0, 0, 0, 0, 0, 8],
    #         [17, 3, 6, 1, 5, 3, 6, 1, 5, 17]]


# вызов инструкции
def manual():
    message_one = messagebox.askyesno(title='Инструкция к игре', message='Хочешь узнать правила игры?', icon='info')
    if message_one:
        board.create_rectangle(par_scale - 10, par_scale - 10, 9 * par_scale + 10, 9 * par_scale + 10, fill='white',
                               outline="black")

        board.create_text(scale / 2, scale / 7, fill="darkblue", font=f"Times {int(par_scale / 3.5)} italic bold",
                          text="ИНСТРУКЦИЯ К ИГРЕ", anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 4.6), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="Цель игры выбить все фишки противника \n              за пределы игровой зоны",
                          anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 3.6), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="Твои фишки красные, фишки противника зеленые", anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 3.18), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="В игре существует две игровых зоны: База и Поле", anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 2.69), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="На базах расположено как у тебя, так и у противника \n        "
                               "4 горизонтальных и 4 вертикальных фишки ",
                          anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 2.25), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="В начале каждого хода бросается кубик,\n число означает кол-во доступных ходов",
                          anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 1.94), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="Чтобы выбить противника, необходимо \n            подвести его фишку на базу",
                          anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 1.7), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="Выбивание возможно, если обе фишки \n стоят длинной стороной друг к другу",
                          anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 1.52), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="Чтобы развернуть фишку,необходимо \n            попасть в желтую зону",
                          anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 1.34), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="Если две союзных фишки стоят длинной стороной \n            "
                               "друг к другу  на Поле в области квадратов, \n                "
                               "то они образуют квадратную фишку",
                          anchor=tkinter.CENTER)
        board.create_text(scale / 2, int(scale / 1.2), fill="darkblue",
                          font=f"Times {int(par_scale / 4.2)} italic bold",
                          text="      Квадратной фишкой можно выбивать\n фишки противника  в любых положениях",
                          anchor=tkinter.CENTER)
        message_two = tkinter.messagebox.showinfo('Инструкция', 'Нажми OK, когда дочитаешь')
        if message_two:
            conclusion(-1, -1, -1, -1, 1)
            choice()
        else:
            tkinter.messagebox.askyesno(message='УВЫ И АХ', icon='info')
    else:
        choice()


# диалоговое окно выбора хода
def choice():
    global par_motion
    title = 'Добро пожаловать =)'
    if mode == 2:
        message_three = messagebox.askyesno(title=title, message='Игрок 1 ходит первым?', icon='info')
    else:
        message_three = messagebox.askyesno(title=title, message='Ты хочешь ходить первым?', icon='info')
    if message_three:
        par_motion = 1
    else:
        if mode == 2:
            par_motion = 2
        elif mode == 1:
            par_motion = 0
    determinant(par_motion)


# конец игры
def the_end():
    global end_p  # определяет конец хода, если на поле не осталось фишек одного из игроков
    f_player = 0  # переменные подсчёта кол-ва фишек на поле
    f_player2 = 0
    end_p = 0
    for i in range(10):
        for ii in field[i]:
            if ii == 1 or ii == 2 or ii == 9 or ii == 11:
                f_player += 1
            if ii == 3 or ii == 4 or ii == 13 or ii == 15:
                f_player2 += 1
    if f_player == 0:
        end_p = 1
        message(2)
    if f_player2 == 0:
        end_p = 1
        message(1)


# окно о завершении игры
def message(option):
    message_i = 0
    title = 'Игра завершена'
    if option == 1:
        if mode == 2:
            message_i = messagebox.askyesno(title=title, message='Игрок 1 победил!\nНажми "Да" что бы начать заново.',
                                            icon='info')
        else:
            message_i = messagebox.askyesno(title=title, message='Вы победили!\nНажми "Да" что бы начать заново.',
                                            icon='info')
    if option == 2:
        if mode == 2:
            message_i = messagebox.askyesno(title=title, message='Игрок 2 победил!\nНажми "Да" что бы начать заново.',
                                            icon='info')
        else:
            message_i = messagebox.askyesno(title=title, message='Вы проиграли!\nНажми "Да" что бы начать заново.',
                                            icon='info')
    if option == 3:
        message_i = messagebox.askyesno(title=title,
                                        message='Вы победили! У компьютера не осталось ходов.\nНажми "Да" что бы начать заново.',
                                        icon='info')
    if message_i:
        create_place()
        conclusion(-1, -1, -1, -1, 1)
        choice()  # ход игрока доступен
    else:
        root.destroy()
        print('До свидания!')


# функция отрисовки фигур, анимации
def conclusion(x_poz_1, y_poz_1, x_poz_2, y_poz_2, w):
    # выброс фигур вниз и вправо
    # разбитие квадрата рамка
    # анимация вправо квадраты нет выталкивание
    global field  # на основе поля отрисовка
    global frame_blue, frame_yellow  # делаем глобальными параметры рамки
    global par_V, b  # Определяем скорость анимации. И делаем глобальным параметр анимации(FIX)
    # print(field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7], field[8], field[9], sep='\n')
    # print(' ')  # Пробел между выводом в RUN поля

    # переменные
    k = x = x_3 = par_scale  # параметры отрисовки поля равны маштаб/10
    x1 = x2 = x3 = 3 * par_scale  # для отрисовки поля
    x_2 = y_2 = y_3 = 0  # для отрисовки поля

    board.delete('all')  # удаление прошлых ходов, чтобы не перегружать систему созданием новых объектов

    frame_blue = board.create_rectangle(-5, -5, -5, -5, outline='yellow', width=7)  # рамка при выборе
    frame_yellow = board.create_rectangle(-5, -5, -5, -5, outline='blue', width=7)  # рамка при наведении

    while True:  # поле, создание внешнего вида
        if y_2 == 0:  # уголки сверху
            board.create_polygon([0, par_scale - 1], [par_scale - 1, par_scale - 1], [par_scale - 1, 0], fill="yellow",
                                 outline="black")
            board.create_polygon([par_scale * 9 + 1, 0], [par_scale * 9 + 1, par_scale - 1], [scale, par_scale - 1],
                                 fill="yellow",
                                 outline="black")
            y_2 += k
        elif y_2 >= scale / 10 * 9:  # уголки снизу
            board.create_polygon([0, par_scale * 9 + 1], [par_scale - 1, par_scale * 9 + 1], [par_scale - 1, scale],
                                 fill="yellow",
                                 outline="black")
            board.create_polygon([par_scale * 9 + 1, par_scale * 9 + 1], [par_scale * 9 + 1, scale],
                                 [scale, par_scale * 9 + 1], fill="yellow", outline="black")
            break
        else:  # базы для фишек
            board.create_rectangle(x_2 + 10, y_2 + 10, x_2 + k - 10, y_2 + k * 2 - 10, fill="white",
                                   outline="black")
            board.create_rectangle(x_3 + 10, y_3 + 10, x_3 + 2 * k - 10, y_3 + k - 10, fill="white", outline="black")
            board.create_rectangle(x_2 + 9 * k + 10, y_2 + 10, x_2 + 10 * k - 10, y_2 + k * 2 - 10, fill="white",
                                   outline="black")
            board.create_rectangle(x_3 + 10, y_3 + 9 * k + 10, x_3 + 2 * k - 10, y_3 + 10 * k - 10, fill="white",
                                   outline="black")
            y_2 += 2 * k
            x_3 += 2 * k
    while x < k * 9:  # игровое поле без баз
        y = 1 * k
        while y < k * 9:
            board.create_rectangle(x, y, x + k, y + k, outline="black", width=1)
            y += 1 * k
        x += 1 * k
    while x1 < k * 9:  # маленькие квадраты на поле
        y1 = 3 * k
        while y1 < k * 9:
            board.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, outline="purple")
            y1 += 2 * k
        x1 += 2 * k
    while x2 < k * 9:  # вертикальные жирные линии
        y2 = par_scale
        board.create_line(x2, y2, x2, 9 * y2, width=3, fill="grey")
        x2 += 2 * k
    while x3 < k * 9:  # горизонтальные жирные линии
        y3 = par_scale
        # 100 300
        board.create_line(y3, x3, 9 * y3, x3, width=3, fill="grey")
        x3 += 2 * k
    ots = scale / 200  # отступ, что бы фишки не соприкасались
    ots_f = scale / 125  # отступ для рамки, чтобы создать вид трехмерности
    even_list = [2, 4, 6, 8]  # параметр для квадратов
    odd_list = [1, 3, 5, 7]
    # поле готово

    for t in range(10):  # Создание фишек. Стоячие фигуры без анимации
        for u in range(10):
            point = field[t][u]  # перебор каждого значения на поле
            if point:  # если в точке есть значение больше 0
                fhi = [0, 2]
                # стоячие красные фишки горизонтальные
                if point == 1:
                    list_of_squares = [13, 15]
                    if field[y_poz_1][x_poz_1] in list_of_squares:  # если по фигуре ходит квадрат соперника
                        # смещаем значения, чтобы не писать код дважды для разных координат
                        if field[y_poz_2][x_poz_2] != 1 and field[y_poz_2][x_poz_2] != 5:
                            if y_poz_2 in even_list:
                                y_poz_2 = y_poz_2 - 1
                            elif y_poz_2 in odd_list:
                                y_poz_2 = y_poz_2 + 1
                    # проверка чтобы тык засчитался
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) and par_motion in fhi \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        # если противник нас подвинул, то отрисовки стоячей фигуры нет.
                        if field[y_poz_2][x_poz_2] == 5:
                            x_poz_2 = x_poz_2 - 1
                            # в итоге пешки которые двигаем не оставляют шлейф
                    else:  # если ходим мы этой фигурой
                        if (x_poz_1, y_poz_1) != (u, t):  # если ходим, пропадает стоячая фигура.
                            # рамки
                            board.create_line(u * par_scale + ots_f, t * par_scale + par_scale - ots,
                                              u * par_scale + 2 * par_scale - par_scale / 100,
                                              t * par_scale + par_scale - ots, width=par_scale / 12.5)
                            board.create_line(u * par_scale + 2 * par_scale - ots, t * par_scale + ots_f,
                                              u * par_scale + 2 * par_scale - ots,
                                              t * par_scale + par_scale - par_scale / 100, width=par_scale / 12.5)
                            # фигура
                            board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                   u * par_scale + 2 * par_scale - 1.5 * ots,
                                                   t * par_scale + par_scale - 1.5 * ots, fill='red', outline="black")
                # стоячие зеленые фишки горизонтальные
                if point == 3:
                    list_of_squares = [9, 11]
                    if field[y_poz_1][x_poz_1] in list_of_squares:  # если ходим квадратом
                        # проверка сверху или снизу фигура
                        if field[y_poz_2][x_poz_2] != 3 and field[y_poz_2][x_poz_2] != 6:
                            if y_poz_2 in even_list:
                                y_poz_2 = y_poz_2 - 1
                            elif y_poz_2 in odd_list:
                                y_poz_2 = y_poz_2 + 1
                    # проверка чтобы тык засчитался
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) and par_motion == 1 \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if field[y_poz_2][x_poz_2] == 6:
                            x_poz_2 = x_poz_2 - 1
                        # в итоге пешки которые двигаем не оставляют шлейф
                    else:
                        if (x_poz_1, y_poz_1) != (u, t):
                            board.create_line(u * par_scale + ots_f, t * par_scale + par_scale - ots,
                                              u * par_scale + 2 * par_scale - par_scale / 100,
                                              t * par_scale + par_scale - ots, width=par_scale / 12.5)
                            board.create_line(u * par_scale + 2 * par_scale - ots, t * par_scale + ots_f,
                                              u * par_scale + 2 * par_scale - ots,
                                              t * par_scale + par_scale - par_scale / 100, width=par_scale / 12.5)
                            board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                   u * par_scale + 2 * par_scale - 1.5 * ots,
                                                   t * par_scale + par_scale - 1.5 * ots, fill='green', outline="black")
                # стоячие красные фишки вертикальные
                elif point == 2:
                    list_of_squares = [13, 15]
                    if field[y_poz_1][x_poz_1] in list_of_squares:
                        if field[y_poz_2][x_poz_2] != 2 and field[y_poz_2][x_poz_2] != 7:
                            if x_poz_2 in even_list:
                                x_poz_2 = x_poz_2 - 1
                            elif x_poz_2 in odd_list:
                                x_poz_2 = x_poz_2 + 1
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) and par_motion in fhi \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if field[y_poz_2][x_poz_2] == 7:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if (x_poz_1, y_poz_1) != (u, t):
                            board.create_line(u * par_scale + par_scale - ots, t * par_scale + ots_f,
                                              u * par_scale + par_scale - ots,
                                              t * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5)
                            board.create_line(u * par_scale + ots_f, t * par_scale + 2 * par_scale - ots,
                                              u * par_scale + par_scale - par_scale / 100,
                                              t * par_scale + 2 * par_scale - ots, width=par_scale / 12.5)
                            board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                   u * par_scale + par_scale - 1.5 * ots,
                                                   t * par_scale + 2 * par_scale - 1.5 * ots, fill='red',
                                                   outline="black")
                # стоячие зеленые фишки вертикальные
                elif point == 4:
                    list1 = [9, 11]
                    if field[y_poz_1][x_poz_1] in list1:
                        if field[y_poz_2][x_poz_2] != 4 and field[y_poz_2][x_poz_2] != 8:
                            if x_poz_2 in even_list:
                                x_poz_2 = x_poz_2 - 1
                            elif x_poz_2 in odd_list:
                                x_poz_2 = x_poz_2 + 1
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) and par_motion == 1 \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if field[y_poz_2][x_poz_2] == 8:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if (x_poz_1, y_poz_1) != (u, t):
                            board.create_line(u * par_scale + par_scale - ots, t * par_scale + ots_f,
                                              u * par_scale + par_scale - ots,
                                              t * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5)
                            board.create_line(u * par_scale + ots_f, t * par_scale + 2 * par_scale - ots,
                                              u * par_scale + par_scale - par_scale / 100,
                                              t * par_scale + 2 * par_scale - ots, width=par_scale / 12.5)
                            board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                   u * par_scale + par_scale - 1.5 * ots,
                                                   t * par_scale + 2 * par_scale - 1.5 * ots, fill='green',
                                                   outline="black")
                # для горизонатльных квадратов красных
                elif point == 9:
                    list_of_squares = [13, 15]
                    # если ходит противник по фигуре и указывает на точку внизу, то смещаем координаты
                    # чтобы не дублировать код
                    if field[y_poz_1][x_poz_1] in list_of_squares and y_poz_2 in even_list:
                        y_poz_2 -= 1
                    # если квадрат противника двигает фигуру
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) or (
                            (x_poz_2, y_poz_2 + 1) == (u, t) or (x_poz_2, y_poz_2 + 1) == (u + 1, t))) \
                            and par_motion in fhi and field[y_poz_1][x_poz_1] in list_of_squares and abs(
                        x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        # то не рисуем стоячую фигуру
                        if field[y_poz_2][x_poz_2] == 10:
                            x_poz_2 = x_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) \
                            and par_motion in fhi and field[y_poz_1][x_poz_1] == 3 and abs(
                        x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        # то не рисуем стоячую фигуру
                        if field[y_poz_2][x_poz_2] == 10:
                            x_poz_2 = x_poz_2 - 1
                    else:  # отрисовка стоячей фигуры
                        if field[t][u] == 9 and t in odd_list:  # для верхней планки
                            if (x_poz_1, y_poz_1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + 2 * par_scale - 1.5 * ots,
                                                       t * par_scale + par_scale - ots, fill='red', outline="black")
                        elif field[t - 1][u] == 9:  # для нижней планки + рамка
                            if (x_poz_1, y_poz_1 + 1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + 2 * par_scale - 1.5 * ots,
                                                       t * par_scale + par_scale - 1.5 * ots, fill='red',
                                                       outline="black")
                                board.create_line(u * par_scale + ots_f, t * par_scale + par_scale - ots + 1,
                                                  u * par_scale + 2 * par_scale - ots,
                                                  t * par_scale + par_scale - ots + 1,
                                                  width=par_scale / 15.2)
                                board.create_line(u * par_scale + 2 * par_scale - ots + 1,
                                                  t * par_scale - par_scale + ots_f,
                                                  u * par_scale + 2 * par_scale - ots + 1,
                                                  t * par_scale + par_scale - par_scale / 200,
                                                  width=par_scale / 15.2)
                # для вертикальных квадратов красных
                elif point == 13:
                    list1 = [9, 11]
                    if field[y_poz_1][x_poz_1] in list1 and y_poz_2 in even_list:
                        y_poz_2 -= 1
                    # проверка чтобы тык засчитался
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) or (
                            (x_poz_2, y_poz_2 + 1) == (u, t) or (x_poz_2, y_poz_2 + 1) == (
                            u + 1, t))) and par_motion and field[y_poz_1][x_poz_1] in list1 \
                            and abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        if field[y_poz_2][x_poz_2] == 14:
                            x_poz_2 = x_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) and par_motion and \
                            field[y_poz_1][x_poz_1] == 1 \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if field[y_poz_2][x_poz_2] == 14:
                            x_poz_2 = x_poz_2 - 1
                    else:
                        if field[t][u] == 13 and t in odd_list:
                            if (x_poz_1, y_poz_1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + 2 * par_scale - 1.5 * ots,
                                                       t * par_scale + par_scale - ots, fill='green', outline="black")
                        elif field[t - 1][u] == 13:
                            if (x_poz_1, y_poz_1 + 1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + 2 * par_scale - 1.5 * ots,
                                                       t * par_scale + par_scale - 1.5 * ots, fill='green',
                                                       outline="black")
                                board.create_line(u * par_scale + ots_f, t * par_scale + par_scale - ots + 1,
                                                  u * par_scale + 2 * par_scale - ots,
                                                  t * par_scale + par_scale - ots + 1,
                                                  width=par_scale / 15.2)
                                board.create_line(u * par_scale + 2 * par_scale - ots + 1,
                                                  t * par_scale - par_scale + ots_f,
                                                  u * par_scale + 2 * par_scale - ots + 1,
                                                  t * par_scale + par_scale - par_scale / 200,
                                                  width=par_scale / 15.2)
                # для горизонатльных квадратов зеленых
                elif point == 11:
                    list_of_squares = [13, 15]
                    if field[y_poz_1][x_poz_1] in list_of_squares and x_poz_2 in even_list:
                        x_poz_2 -= 1
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) or (
                            (x_poz_2 + 1, y_poz_2) == (u, t) or (x_poz_2 + 1, y_poz_2) == (u, t + 1))) \
                            and par_motion in fhi and field[y_poz_1][x_poz_1] in list_of_squares and abs(
                        x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        if field[y_poz_2][x_poz_2] == 12:
                            y_poz_2 = y_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) \
                            and par_motion in fhi and field[y_poz_1][x_poz_1] == 4 and abs(
                        x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if field[y_poz_2][x_poz_2] == 12:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if field[t][u] == 11 and u in odd_list:
                            if (x_poz_1, y_poz_1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + par_scale - ots,
                                                       t * par_scale + 2 * par_scale - 1.5 * ots, fill='red',
                                                       outline="black")
                        elif field[t][u - 1] == 11:
                            if (x_poz_1 + 1, y_poz_1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + par_scale - 1.5 * ots,
                                                       t * par_scale + 2 * par_scale - 1.5 * ots, fill='red',
                                                       outline="black")
                                board.create_line(u * par_scale - par_scale + ots_f,
                                                  t * par_scale + 2 * par_scale - ots + 1,
                                                  u * par_scale + par_scale - ots,
                                                  t * par_scale + 2 * par_scale - ots + 1,
                                                  width=par_scale / 15.2)
                                board.create_line(u * par_scale + par_scale - ots + 1, t * par_scale + ots_f,
                                                  u * par_scale + par_scale - ots + 1,
                                                  t * par_scale + 2 * par_scale - par_scale / 200,
                                                  width=par_scale / 15.2)
                # для вертикальных квадратов зеленых
                elif point == 15:
                    list1 = [9, 11]
                    if field[y_poz_1][x_poz_1] in list1 and x_poz_2 in even_list:
                        x_poz_2 -= 1
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) or (
                            (x_poz_2 + 1, y_poz_2) == (u, t) or (x_poz_2 + 1, y_poz_2) == (
                            u, t + 1))) and par_motion and field[y_poz_1][x_poz_1] in list1 \
                            and abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        if field[y_poz_2][x_poz_2] == 16:
                            y_poz_2 = y_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) and par_motion and \
                            field[y_poz_1][x_poz_1] == 2 \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if field[y_poz_2][x_poz_2] == 16:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if field[t][u] == 15 and u in odd_list:
                            if (x_poz_1, y_poz_1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + par_scale - ots,
                                                       t * par_scale + 2 * par_scale - 1.5 * ots, fill='green',
                                                       outline="black")
                        elif field[t][u - 1] == 15:
                            if (x_poz_1 + 1, y_poz_1) != (u, t):
                                board.create_rectangle(u * par_scale + ots, t * par_scale + ots,
                                                       u * par_scale + par_scale - 1.5 * ots,
                                                       t * par_scale + 2 * par_scale - 1.5 * ots, fill='green',
                                                       outline="black")
                                board.create_line(u * par_scale - par_scale + ots_f,
                                                  t * par_scale + 2 * par_scale - ots + 1,
                                                  u * par_scale + par_scale - ots,
                                                  t * par_scale + 2 * par_scale - ots + 1,
                                                  width=par_scale / 15.2)
                                board.create_line(u * par_scale + par_scale - ots + 1, t * par_scale + ots_f,
                                                  u * par_scale + par_scale - ots + 1,
                                                  t * par_scale + 2 * par_scale - par_scale / 200,
                                                  width=par_scale / 15.2)
    for y_i in range(1, 9):  # если квадраты образуются от хода соперника
        for x_i in range(1, 9):
            if field[y_i][x_i] == 1 and field[y_i + 1][x_i] == 1 and (y_i == 1 or y_i == 3 or y_i == 5 or y_i == 7):
                field[y_i][x_i] = 9
                field[y_i + 1][x_i] = 9
                field[y_i][x_i + 1] = 10
                field[y_i + 1][x_i + 1] = 10
            elif field[y_i][x_i] == 3 and field[y_i + 1][x_i] == 3 and (y_i == 1 or y_i == 3 or y_i == 5 or y_i == 7):
                field[y_i][x_i] = 13
                field[y_i + 1][x_i] = 13
                field[y_i][x_i + 1] = 14
                field[y_i + 1][x_i + 1] = 14
            elif field[y_i][x_i] == 2 and field[y_i][x_i + 1] == 2 and (x_i == 1 or x_i == 3 or x_i == 5 or x_i == 7):
                field[y_i][x_i] = 11
                field[y_i][x_i + 1] = 11
                field[y_i + 1][x_i] = 12
                field[y_i + 1][x_i + 1] = 12
            elif field[y_i][x_i] == 4 and field[y_i][x_i + 1] == 4 and (x_i == 1 or x_i == 3 or x_i == 5 or x_i == 7):
                field[y_i][x_i] = 15
                field[y_i][x_i + 1] = 15
                field[y_i + 1][x_i] = 16
                field[y_i + 1][x_i + 1] = 16

    # ANIMATION. Когда происходит ход, отрисовка стоячих фигур убирается в месте указанный позиций.
    point = field[y_poz_1][x_poz_1]
    if point:
        # Создаем Тэг для каждой детали для отрисовки движения
        if point == 1:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + par_scale - 1.5 * ots, fill='red', outline="black",
                                   tags='fig1')
            board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + par_scale - ots,
                              x_poz_1 * par_scale + 2 * par_scale - par_scale / 100,
                              y_poz_1 * par_scale + par_scale - ots, width=par_scale / 12.5,
                              tags='frame1')
            board.create_line(x_poz_1 * par_scale + 2 * par_scale - ots, y_poz_1 * par_scale + ots_f,
                              x_poz_1 * par_scale + 2 * par_scale - ots,
                              y_poz_1 * par_scale + par_scale - par_scale / 100, width=par_scale / 12.5, tags='frame2')
        elif point == 2:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + 2 * par_scale - 1.5 * ots, fill='red', tags='fig2')
            board.create_line(x_poz_1 * par_scale + par_scale - ots, y_poz_1 * par_scale + ots_f,
                              x_poz_1 * par_scale + par_scale - ots,
                              y_poz_1 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5,
                              tags='frame3')
            board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + 2 * par_scale - ots,
                              x_poz_1 * par_scale + par_scale - par_scale / 100,
                              y_poz_1 * par_scale + 2 * par_scale - ots, width=par_scale / 12.5,
                              tags='frame4')
        elif point == 3:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + par_scale - 1.5 * ots, fill='green', tags='fig3')
            board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + par_scale - ots,
                              x_poz_1 * par_scale + 2 * par_scale - par_scale / 100,
                              y_poz_1 * par_scale + par_scale - ots, width=par_scale / 12.5,
                              tags='frame1')
            board.create_line(x_poz_1 * par_scale + 2 * par_scale - ots, y_poz_1 * par_scale + ots_f,
                              x_poz_1 * par_scale + 2 * par_scale - ots,
                              y_poz_1 * par_scale + par_scale - par_scale / 100, width=par_scale / 12.5, tags='frame2')
        elif point == 4:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + 2 * par_scale - 1.5 * ots, fill='green', tags='fig4')
            board.create_line(x_poz_1 * par_scale + par_scale - ots, y_poz_1 * par_scale + ots_f,
                              x_poz_1 * par_scale + par_scale - ots,
                              y_poz_1 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5,
                              tags='frame3')
            board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + 2 * par_scale - ots,
                              x_poz_1 * par_scale + par_scale - par_scale / 100,
                              y_poz_1 * par_scale + 2 * par_scale - ots, width=par_scale / 12.5,
                              tags='frame4')
        elif point == 9:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + par_scale - ots, fill='red', tags='fig9')
            board.create_rectangle(x_poz_1 * par_scale + ots, (y_poz_1 + 1) * par_scale + ots,
                                   x_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   (y_poz_1 + 1) * par_scale + par_scale - 1.5 * ots,
                                   fill='red', tags='fig10')
            if y_poz_1 in odd_list:
                board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  x_poz_1 * par_scale + 2 * par_scale - ots,
                                  y_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  width=par_scale / 15.2, tags='frameCube1')
                board.create_line(x_poz_1 * par_scale + 2 * par_scale - ots + 1, y_poz_1 * par_scale + ots_f,
                                  x_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  y_poz_1 * par_scale + 2 * par_scale - par_scale / 200,
                                  width=par_scale / 15.2, tags='frameCube2')
        elif point == 13:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + par_scale - ots, fill='green', tags='fig13')
            board.create_rectangle(x_poz_1 * par_scale + ots, (y_poz_1 + 1) * par_scale + ots,
                                   x_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   (y_poz_1 + 1) * par_scale + par_scale - 1.5 * ots,
                                   fill='green', tags='fig14')
            if y_poz_1 in odd_list:
                board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  x_poz_1 * par_scale + 2 * par_scale - ots,
                                  y_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  width=par_scale / 15.2, tags='frameCube1')
                board.create_line(x_poz_1 * par_scale + 2 * par_scale - ots + 1, y_poz_1 * par_scale + ots_f,
                                  x_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  y_poz_1 * par_scale + 2 * par_scale - par_scale / 200,
                                  width=par_scale / 15.2, tags='frameCube2')
        elif point == 11:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + par_scale - ots,
                                   y_poz_1 * par_scale + 2 * par_scale - 1.5 * ots, fill='red', tags='fig11')
            board.create_rectangle((x_poz_1 + 1) * par_scale + ots, y_poz_1 * par_scale + ots,
                                   (x_poz_1 + 1) * par_scale + par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   fill='red', tags='fig12')
            if x_poz_1 in odd_list:
                board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  x_poz_1 * par_scale + 2 * par_scale - ots,
                                  y_poz_1 * par_scale + 2 * par_scale - ots + 1, width=par_scale / 15.2,
                                  tags='frameCube1')
                board.create_line(x_poz_1 * par_scale + 2 * par_scale - ots + 1, y_poz_1 * par_scale + ots_f,
                                  x_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  y_poz_1 * par_scale + 2 * par_scale - par_scale / 200, width=par_scale / 15.2,
                                  tags='frameCube2')
        elif point == 15:
            board.create_rectangle(x_poz_1 * par_scale + ots, y_poz_1 * par_scale + ots,
                                   x_poz_1 * par_scale + par_scale - ots,
                                   y_poz_1 * par_scale + 2 * par_scale - 1.5 * ots, fill='green', tags='fig15')
            board.create_rectangle((x_poz_1 + 1) * par_scale + ots, y_poz_1 * par_scale + ots,
                                   (x_poz_1 + 1) * par_scale + par_scale - 1.5 * ots,
                                   y_poz_1 * par_scale + 2 * par_scale - 1.5 * ots,
                                   fill='green', tags='fig16')
            if x_poz_1 in odd_list:
                board.create_line(x_poz_1 * par_scale + ots_f, y_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  x_poz_1 * par_scale + 2 * par_scale - ots,
                                  y_poz_1 * par_scale + 2 * par_scale - ots + 1, width=par_scale / 15.2,
                                  tags='frameCube1')
                board.create_line(x_poz_1 * par_scale + 2 * par_scale - ots + 1, y_poz_1 * par_scale + ots_f,
                                  x_poz_1 * par_scale + 2 * par_scale - ots + 1,
                                  y_poz_1 * par_scale + 2 * par_scale - par_scale / 200, width=par_scale / 15.2,
                                  tags='frameCube2')
    # переменные
    kx = 10  # коэффициент направления
    ky = 10  # коэффициент направления
    b = 0
    par_kvadro = 13  # определяем значения переменных, чтобы убрать указания по pep8 из консоли
    par_fishki = par_kvadro_gor = 0
    par_fishki2 = par_kvadro_vert = 0
    fig = fig2 = fig3 = fig4 = 0
    colour = vkx = vky = vrange = 0
    corner = corner2 = poz3 = poz4 = poz5 = -1
    poz33 = -2
    poz44 = -2
    vector_kv = 0
    frame1 = 'frame1'  # tags
    frame2 = 'frame2'
    frame3 = 'frame3'
    frame4 = 'frame4'
    frameCube1 = 'frameCube1'
    frameCube2 = 'frameCube2'
    if par_motion == 1:  # для ходов игрока параметры
        # ход игрока
        par_fishki = 3
        par_fishki2 = 4
        par_kvadro_gor = 13
        par_kvadro_vert = 15
        fig = 'fig1'
        fig2 = 'fig2'
        colour = 'green'
        if point == 9:
            fig3 = 'fig9'
            fig4 = 'fig10'
        elif point == 11:
            fig3 = 'fig11'
            fig4 = 'fig12'
    elif par_motion == 0 or par_motion == 2:  # для ходов игрока и компьютера разные параметры
        # ход компьютера
        par_fishki = 1
        par_fishki2 = 2
        par_kvadro_gor = 9
        par_kvadro_vert = 11
        fig = 'fig3'
        fig2 = 'fig4'
        colour = 'red'
        if point == 13:
            fig3 = 'fig13'
            fig4 = 'fig14'
        elif point == 15:
            fig3 = 'fig15'
            fig4 = 'fig16'
    if par_V == 0:  # скорость анимации фигур
        vkx = 1
        vky = 1
        vrange = 1
    elif par_V == 1:
        vkx = 2
        vky = 2
        vrange = 2
    elif par_V == 2:
        vkx = 4
        vky = 4
        vrange = 4
    # для горизонтальных
    if point == 1 or point == 3:
        if x_poz_2 == 2 or x_poz_2 == 4 or x_poz_2 == 6 or x_poz_2 == 8:  # корректировка смещения точки выбора
            x_poz_2 = x_poz_2 - 1
        # определение векторов для хода горизонтальных фишек
        if x_poz_1 == x_poz_2 and abs(y_poz_1 - y_poz_2) <= 3:
            kx = 0
            if y_poz_1 < y_poz_2:
                ky = 1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    poz3 = field[y_poz_2 + 1][x_poz_2]
                    poz4 = field[y_poz_2 + 1][x_poz_2 + 1]
                else:
                    poz3 = 0
                    poz4 = 0
            elif y_poz_1 > y_poz_2:
                ky = -1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    poz3 = field[y_poz_2 - 1][x_poz_2]
                    poz4 = field[y_poz_2 - 1][x_poz_2 + 1]
                else:
                    poz3 = 0
                    poz4 = 0
        elif y_poz_1 == y_poz_2 and abs(x_poz_1 - x_poz_2) <= 3:
            ky = 0
            if x_poz_1 < x_poz_2:
                kx = 2
                if x_poz_2 < 7:
                    poz3 = field[y_poz_2][x_poz_2 + 2]
                    poz4 = field[y_poz_2][x_poz_2 + 3]
            elif x_poz_1 > x_poz_2:
                kx = -2
                if x_poz_2 != 0:
                    poz3 = field[y_poz_2][x_poz_2 - 1]
                    poz4 = field[y_poz_2][x_poz_2 - 2]
        # после того как нашли коэффициенты
        if field[y_poz_2][x_poz_2] == 0 and x_poz_2 != 9:  # анимация хода для горизонтальных фигур
            if field[y_poz_2][x_poz_2 + 1] == 0 and w == 1:  # что бы не было задвоенного хода
                if kx == 0 and abs(y_poz_1 - y_poz_2) < 2:  # ход вверх и вниз
                    for i in range(abs(y_poz_1 - y_poz_2)):  # анимация перемещения пешки
                        for ii in range(0, int(par_scale / vrange)):  # анимация движения по длине в скобках.
                            b = 1
                            board.move(fig, vkx * kx, vky * ky)  # за счет умножения на 4 увеличиваем скорость анимации
                            board.move(frame1, vkx * kx, vky * ky)
                            board.move(frame2, vkx * kx, vky * ky)
                            board.update()  # обновление
                            time.sleep(0.01)
                elif ky == 0 and abs(x_poz_1 - x_poz_2) < 3:  # ход влево и вправо
                    for i in range(abs(x_poz_1 - x_poz_2)):  # анимация перемещения пешки
                        for ii in range(int(par_scale / vrange)):  # анимация движения по длине в скобках
                            b = 1
                            board.move(fig, vkx / 2 * kx, vky / 2 * ky)
                            board.move(frame1, vkx / 2 * kx, vky / 2 * ky)
                            board.move(frame2, vkx / 2 * kx, vky / 2 * ky)
                            board.update()  # обновление
                            time.sleep(0.01)
        # анимация перемещения противника
        elif field[y_poz_2][x_poz_2] == par_fishki and poz3 == 0 and poz4 == 0:  # анимация перемещения противника
            board.create_line(x_poz_2 * par_scale + ots_f, y_poz_2 * par_scale + par_scale - ots,
                              (x_poz_2 + 2) * par_scale - par_scale / 100,
                              y_poz_2 * par_scale + par_scale - ots, width=par_scale / 12.5, tags='ramaDV')  # рамка
            board.create_line(x_poz_2 * par_scale + 2 * par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + 2 * par_scale - ots,
                              y_poz_2 * par_scale + par_scale - par_scale / 100, width=par_scale / 12.5,
                              tags='ramaDV2')  # рамка
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + par_scale - 1.5 * ots, fill=colour, tags='DV')
            for i in range(abs(y_poz_1 - y_poz_2)):
                if y_poz_2 == 0 or y_poz_2 == 9:
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig, kx, vky / 2 * ky)
                        board.move(frame1, kx, vky / 2 * ky)
                        board.move(frame2, kx, vky / 2 * ky)
                        board.move('DV', kx, vky / 2 * ky)
                        board.move('ramaDV', kx, vky / 2 * ky)
                        board.move('ramaDV2', kx, vky / 2 * ky)
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig, - kx, - vky / 2 * ky)
                        board.move(frame1, - kx, - vky / 2 * ky)
                        board.move(frame2, - kx, - vky / 2 * ky)
                        board.update()
                        time.sleep(0.01)
                else:
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig, kx, vky * ky)
                        board.move(frame1, kx, vky * ky)
                        board.move(frame2, kx, vky * ky)
                        board.move('DV', kx, vky * ky)
                        board.move('ramaDV', kx, vky * ky)
                        board.move('ramaDV2', kx, vky * ky)
                        board.update()
                        time.sleep(0.01)
        # анимация разбивания квадрата противника
        elif field[y_poz_2][x_poz_2] == par_kvadro_gor and poz3 == 0 and poz4 == 0:
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + par_scale - 1.5 * ots, fill=colour, tags='DV')
            board.create_line(x_poz_2 * par_scale + ots_f, y_poz_2 * par_scale + par_scale - ots + 1,
                              x_poz_2 * par_scale + 2 * par_scale - ots, y_poz_2 * par_scale + par_scale - ots + 1,
                              width=par_scale / 15.2, tags='ramaDV')
            board.create_line(x_poz_2 * par_scale + 2 * par_scale - ots + 1, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + 2 * par_scale - ots + 1,
                              y_poz_2 * par_scale + par_scale - par_scale / 200,
                              width=par_scale / 15.2, tags='ramaDV2')
            for i in range(abs(2)):
                for ii in range(int(par_scale / vrange)):
                    b = 1
                    board.move(fig, kx, vky * ky)
                    board.move(frame1, kx, vky * ky)
                    board.move(frame2, kx, vky * ky)
                    board.move('DV', kx, vky * ky)
                    board.move('ramaDV', kx, vky * ky)
                    board.move('ramaDV2', kx, vky * ky)
                    board.update()
                    time.sleep(0.01)
        # фикс если ход не возможен
        elif field[y_poz_2][x_poz_2] == par_fishki and (poz3 != 0 or poz4 != 0):
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + par_scale - 1.5 * ots, fill=colour)
            board.create_line(x_poz_2 * par_scale + ots_f, (y_poz_2 + 1) * par_scale - ots,
                              (x_poz_2 + 2) * par_scale - par_scale / 100,
                              y_poz_2 * par_scale + par_scale - ots, width=par_scale / 12.5)  # рамка
            board.create_line(x_poz_2 * par_scale + 2 * par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + 2 * par_scale - ots,
                              y_poz_2 * par_scale + par_scale - par_scale / 100, width=par_scale / 12.5)
        # фикс если ход не возможен
        elif field[y_poz_2][x_poz_2] == par_fishki2:
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + 2 * par_scale - 1.5 * ots, fill=colour)
            board.create_line(x_poz_2 * par_scale + par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + par_scale - ots,
                              y_poz_2 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5)
            board.create_line(x_poz_2 * par_scale + ots_f, (y_poz_2 + 2) * par_scale - ots,
                              (x_poz_2 + 1) * par_scale - par_scale / 100,
                              y_poz_2 * par_scale + 2 * par_scale - ots, width=par_scale / 12.5)
        # фикс если ход не возможен
        elif field[y_poz_2][x_poz_2] == par_kvadro_gor and (poz3 != 0 or poz4 != 0):
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + par_scale - 1.5 * ots, fill=colour)
            board.create_line(x_poz_2 * par_scale + ots_f, y_poz_2 * par_scale + par_scale - ots + 1,
                              x_poz_2 * par_scale + 2 * par_scale - ots, y_poz_2 * par_scale + par_scale - ots + 1,
                              width=par_scale / 15.2)
            board.create_line(x_poz_2 * par_scale + 2 * par_scale - ots + 1, y_poz_2 * par_scale - par_scale + ots_f,
                              x_poz_2 * par_scale + 2 * par_scale - ots + 1,
                              y_poz_2 * par_scale + par_scale - par_scale / 200,
                              width=par_scale / 15.2)
        # анимация угла для горизонтальных фигур
        elif field[y_poz_2][x_poz_2] == 17:
            if y_poz_1 == 0:
                if x_poz_2 == 9:
                    corner = field[y_poz_1 + 1][x_poz_1 + 2]
                    corner2 = field[y_poz_1 + 2][x_poz_1 + 2]
                elif x_poz_2 == 0:
                    corner = field[y_poz_1 + 1][x_poz_1 - 1]
                    corner2 = field[y_poz_1 + 2][x_poz_1 - 1]
            elif y_poz_1 == 9:
                if x_poz_2 == 9:
                    corner = field[y_poz_1 - 1][x_poz_1 + 2]
                    corner2 = field[y_poz_1 - 2][x_poz_1 + 2]
                elif x_poz_2 == 0:
                    corner = field[y_poz_1 - 1][x_poz_1 - 1]
                    corner2 = field[y_poz_1 - 2][x_poz_1 - 1]
            if corner == 0 and corner2 == 0:
                for i in range(1):
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig, vkx * kx / 2, ky)
                        board.move(frame1, vkx * kx / 2, ky)
                        board.move(frame2, vkx * kx / 2, ky)
                        board.update()
                        time.sleep(0.01)
                # для нижнего справа угла
                if y_poz_2 == 9 and x_poz_2 == 9:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots) + vkx * ii - par_scale,
                                     (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame1, (x_poz_2 * par_scale) + vkx * ii - par_scale + ots_f,
                                     (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots) - vkx * ii,
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame2, (x_poz_2 * par_scale) + par_scale - ots,
                                     (y_poz_2 * par_scale) - vkx * ii + + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - ots,
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig, 0, - vkx * kx / 2)
                            board.move(frame1, 0, - vkx * kx / 2)
                            board.move(frame2, 0, - vkx * kx / 2)
                            board.update()
                            time.sleep(0.01)
                # для верхнего справа угла
                elif y_poz_2 == 0 and x_poz_2 == 9:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots) + vkx * ii - par_scale,
                                     (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame1, (x_poz_2 * par_scale) + vkx * ii - par_scale + ots_f,
                                     (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots) + vkx * ii)
                        board.coords(frame1, (x_poz_2 * par_scale) + ots_f,
                                     (y_poz_2 * par_scale) + par_scale + vkx * ii - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale) + vkx * ii - ots)
                        board.coords(frame2, (x_poz_2 * par_scale) + par_scale - ots, (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - ots,
                                     (y_poz_2 * par_scale + par_scale) + vkx * ii - par_scale / 100)
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig, 0, vkx * kx / 2)
                            board.move(frame1, 0, vkx * kx / 2)
                            board.move(frame2, 0, vkx * kx / 2)
                            board.update()
                            time.sleep(0.01)
                # для нижнего слева угла
                if y_poz_2 == 9 and x_poz_2 == 0:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - vkx * ii,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame1, (x_poz_2 * par_scale) + ots_f, (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - vkx * ii - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.coords(frame2, (x_poz_2 * par_scale) + 2 * par_scale - vkx * ii - ots,
                                     (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - vkx * ii - ots,
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots) - vkx * ii,
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame2, (x_poz_2 * par_scale) + par_scale - ots,
                                     (y_poz_2 * par_scale) - vkx * ii + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - ots,
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig, 0, vkx * kx / 2)
                            board.move(frame1, 0, vkx * kx / 2)
                            board.move(frame2, 0, vkx * kx / 2)
                            board.update()
                            time.sleep(0.01)
                # для верхнего слева угла
                if y_poz_2 == 0 and x_poz_2 == 0:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - vkx * ii,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame1, (x_poz_2 * par_scale) + ots_f, (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - vkx * ii - par_scale / 100 - ots,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.coords(frame2, (x_poz_2 * par_scale) - vkx * ii + 2 * par_scale - ots,
                                     (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - vkx * ii - ots,
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots) + vkx * ii)
                        board.coords(frame1, (x_poz_2 * par_scale) + ots_f,
                                     (y_poz_2 * par_scale) + par_scale + vkx * ii - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale) + vkx * ii - ots)
                        board.coords(frame2, (x_poz_2 * par_scale) + par_scale - ots, (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - ots,
                                     (y_poz_2 * par_scale + par_scale) + vkx * ii - par_scale / 100)
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig, 0, -vkx * kx / 2)
                            board.move(frame1, 0, -vkx * kx / 2)
                            board.move(frame2, 0, -vkx * kx / 2)
                            board.update()
                            time.sleep(0.01)
    # для вертикальных
    elif point == 2 or point == 4:
        if y_poz_2 == 2 or y_poz_2 == 4 or y_poz_2 == 6 or y_poz_2 == 8:
            y_poz_2 = y_poz_2 - 1
        # определение векторов для хода вертикальных фишек
        if x_poz_1 == x_poz_2 and abs(y_poz_1 - y_poz_2) <= 3:
            kx = 0
            if y_poz_1 < y_poz_2:
                ky = 2
                if y_poz_2 < 7:
                    poz3 = field[y_poz_2 + 2][x_poz_2]
                    poz4 = field[y_poz_2 + 3][x_poz_2]
            elif y_poz_1 > y_poz_2:
                ky = -2
                if y_poz_2 != 0:
                    poz3 = field[y_poz_2 - 1][x_poz_2]
                    poz4 = field[y_poz_2 - 2][x_poz_2]
        elif y_poz_1 == y_poz_2 and abs(x_poz_1 - x_poz_2) <= 3:
            ky = 0
            if x_poz_1 < x_poz_2:
                kx = 1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = field[y_poz_2][x_poz_2 + 1]
                    poz4 = field[y_poz_2 + 1][x_poz_2 + 1]
                else:
                    poz3 = 0
                    poz4 = 0
            elif x_poz_1 > x_poz_2:
                kx = -1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = field[y_poz_2][x_poz_2 - 1]
                    poz4 = field[y_poz_2 + 1][x_poz_2 - 1]
                else:
                    poz3 = 0
                    poz4 = 0
        # после того как нашли коэффициенты
        if field[y_poz_2][x_poz_2] == 0 and y_poz_2 != 9:  # анимация хода для вертикальных фигур
            if field[y_poz_2 + 1][x_poz_2] == 0 and w == 1:  # что бы не было задвоенного хода
                if ky == 0 and abs(x_poz_1 - x_poz_2) < 2:  # ход влево и вправо
                    for i in range(abs(x_poz_1 - x_poz_2)):  # анимация перемещения пешки
                        for ii in range(int(par_scale / vrange)):  # анимация движения по длине в скобках
                            b = 1
                            board.move(fig2, vkx * kx, vky * ky)
                            board.move(frame3, vkx * kx, vky * ky)
                            board.move(frame4, vkx * kx, vky * ky)
                            board.update()  # обновление
                            time.sleep(0.01)
                elif kx == 0 and abs(y_poz_1 - y_poz_2) < 3:  # ход вверх и вниз
                    for i in range(abs(y_poz_1 - y_poz_2)):  # анимация перемещения пешки
                        for ii in range(int(par_scale / vrange)):  # анимация движения по длине в скобках
                            b = 1
                            board.move(fig2, vkx / 2 * kx, vky / 2 * ky)
                            board.move(frame3, vkx / 2 * kx, vky / 2 * ky)
                            board.move(frame4, vkx / 2 * kx, vky / 2 * ky)
                            board.update()  # обновление
                            time.sleep(0.01)
        # анимация перемещения противника
        # вертикальные фигуры
        elif field[y_poz_2][x_poz_2] == par_fishki2 and poz3 == 0 and poz4 == 0:
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + 2 * par_scale - 1.5 * ots, fill=colour, tags='DV')
            board.create_line(x_poz_2 * par_scale + par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + par_scale - ots,
                              y_poz_2 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5,
                              tags='ramaDV')
            board.create_line(x_poz_2 * par_scale + ots_f, (y_poz_2 + 2) * par_scale - ots,
                              (x_poz_2 + 1) * par_scale - par_scale / 100,
                              y_poz_2 * par_scale + 2 * par_scale - ots, width=par_scale / 12.5, tags='ramaDV2')
            for i in range(abs(x_poz_1 - x_poz_2)):
                if x_poz_2 == 0 or x_poz_2 == 9:
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig2, vkx / 2 * kx, ky)
                        board.move(frame3, vkx / 2 * kx, ky)
                        board.move(frame4, vkx / 2 * kx, ky)
                        board.move('DV', vkx / 2 * kx, ky)
                        board.move('ramaDV', vkx / 2 * kx, ky)
                        board.move('ramaDV2', vkx / 2 * kx, ky)
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig2, - vkx / 2 * kx, - ky)
                        board.move(frame3, - vkx / 2 * kx, - ky)
                        board.move(frame4, - vkx / 2 * kx, - ky)
                        board.update()
                        time.sleep(0.01)
                else:
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig2, vkx * kx, ky)
                        board.move(frame3, vkx * kx, ky)
                        board.move(frame4, vkx * kx, ky)
                        board.move('DV', vkx * kx, ky)
                        board.move('ramaDV', vkx * kx, ky)
                        board.move('ramaDV2', vkx * kx, ky)
                        board.update()
                        time.sleep(0.01)
        # анимация разбивания квадрата противника
        elif field[y_poz_2][x_poz_2] == par_kvadro_vert and poz3 == 0 and poz4 == 0:
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + 2 * par_scale - 1.5 * ots, fill=colour, tags='DV')
            board.create_line(x_poz_2 * par_scale + par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + par_scale - ots,
                              y_poz_2 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5,
                              tags='ramaDV')
            board.create_line(x_poz_2 * par_scale + ots_f, (y_poz_2 + 2) * par_scale - ots,
                              (x_poz_2 + 1) * par_scale - par_scale / 100,
                              y_poz_2 * par_scale + 2 * par_scale - ots, width=par_scale / 12.5,
                              tags='ramaDV2')
            for i in range(abs(2)):
                for ii in range(int(par_scale / vrange)):
                    b = 1
                    board.move(fig2, vkx * kx, ky)
                    board.move(frame3, vkx * kx, ky)
                    board.move(frame4, vkx * kx, ky)
                    board.move('DV', vkx * kx, ky)
                    board.move('ramaDV', vkx * kx, ky)
                    board.move('ramaDV2', vkx * kx, ky)
                    board.update()
                    time.sleep(0.01)
        # фикс если ход не возможен для вертикальных
        elif field[y_poz_2][x_poz_2] == par_fishki2 and (poz3 != 0 or poz4 != 0):
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + 2 * par_scale - 1.5 * ots, fill=colour)
            board.create_line(x_poz_2 * par_scale + par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + par_scale - ots,
                              y_poz_2 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5)
            board.create_line(x_poz_2 * par_scale + ots_f, (y_poz_2 + 2) * par_scale - ots,
                              x_poz_2 * par_scale + par_scale - par_scale / 100,
                              y_poz_2 * par_scale + 2 * par_scale - ots, width=par_scale / 12.5)
        # фикс если ход не возможен для квадратов
        elif field[y_poz_2][x_poz_2] == par_kvadro_vert and (poz3 != 0 or poz4 != 0):
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + 2 * par_scale - 1.5 * ots, fill=colour)
            board.create_line(x_poz_2 * par_scale + par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + par_scale - ots,
                              y_poz_2 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5)
            board.create_line(x_poz_2 * par_scale - par_scale + ots_f, (y_poz_2 + 2) * par_scale - ots,
                              (x_poz_2 + 1) * par_scale - par_scale / 100,
                              y_poz_2 * par_scale + 2 * par_scale - ots, width=par_scale / 12.5)
        # фикс если ход не возможен для горизонтальных
        elif field[y_poz_2][x_poz_2] == par_fishki:
            board.create_line(x_poz_2 * par_scale + ots_f, y_poz_2 * par_scale + par_scale - ots,
                              (x_poz_2 + 2) * par_scale - par_scale / 100,
                              y_poz_2 * par_scale + par_scale - ots, width=par_scale / 12.5)  # рамка
            board.create_line(x_poz_2 * par_scale + 2 * par_scale - ots, y_poz_2 * par_scale + ots_f,
                              x_poz_2 * par_scale + 2 * par_scale - ots,
                              y_poz_2 * par_scale + par_scale - par_scale / 100, width=par_scale / 12.5)  # рамка
            board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                   x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                   y_poz_2 * par_scale + par_scale - 1.5 * ots, fill=colour)
        # анимация угла для вертикальных фигур
        elif field[y_poz_2][x_poz_2] == 17:
            if x_poz_1 == 0:
                if y_poz_2 == 9:  # левый низ
                    corner = field[y_poz_1 + 2][x_poz_1 + 1]
                    corner2 = field[y_poz_1 + 2][x_poz_1 + 2]
                elif y_poz_2 == 0:  # левый верх
                    corner = field[y_poz_1 - 1][x_poz_1 + 1]
                    corner2 = field[y_poz_1 - 1][x_poz_1 + 2]
            elif x_poz_1 == 9:
                if y_poz_2 == 9:  # правый низ
                    corner = field[y_poz_1 + 2][x_poz_1 - 1]
                    corner2 = field[y_poz_1 + 2][x_poz_1 - 2]
                elif y_poz_2 == 0:  # правый верх
                    corner = field[y_poz_1 - 1][x_poz_1 - 1]
                    corner2 = field[y_poz_1 - 1][x_poz_1 - 2]
            if corner == 0 and corner2 == 0:
                for i in range(1):
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig2, kx, vky * ky / 2)
                        board.move(frame3, kx, vky * ky / 2)
                        board.move(frame4, kx, vky * ky / 2)
                        board.update()
                        time.sleep(0.01)
                # для нижнего справа угла
                if y_poz_2 == 9 and x_poz_2 == 9:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots),
                                     (y_poz_2 * par_scale + ots) + vky * ii - par_scale,
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame3, (x_poz_2 * par_scale) + par_scale - ots,
                                     (y_poz_2 * par_scale) + vky * ii - par_scale + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - ots,
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots) - vky * ii, (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame4, (x_poz_2 * par_scale) - vky * ii + ots_f,
                                     (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig2, -vky * ky / 2, 0)
                            board.move(frame3, -vky * ky / 2, 0)
                            board.move(frame4, -vky * ky / 2, 0)
                            board.update()
                            time.sleep(0.01)
                # для верхнего справа угла
                elif y_poz_2 == 0 and x_poz_2 == 9:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots) - vky * ii + par_scale)
                        board.coords(frame3, (x_poz_2 * par_scale) + par_scale - ots, (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - ots,
                                     (y_poz_2 * par_scale + par_scale) - vky * ii + par_scale - par_scale / 100)
                        board.coords(frame4, (x_poz_2 * par_scale) + ots_f,
                                     (y_poz_2 * par_scale) - vky * ii + 2 * par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale) - vky * ii + par_scale - ots)
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots) - vky * ii, (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame4, (x_poz_2 * par_scale) - vky * ii + ots_f,
                                     (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig2, vky * ky / 2, 0)
                            board.move(frame3, vky * ky / 2, 0)
                            board.move(frame4, vky * ky / 2, 0)
                            board.update()
                            time.sleep(0.01)
                # для нижнего слева угла
                if y_poz_2 == 9 and x_poz_2 == 0:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots),
                                     (y_poz_2 * par_scale + ots) - par_scale + vky * ii,
                                     (x_poz_2 * par_scale + par_scale - 1.5 * ots),
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame3, (x_poz_2 * par_scale) + par_scale - ots,
                                     (y_poz_2 * par_scale) - par_scale + vky * ii + ots_f,
                                     (x_poz_2 * par_scale + par_scale - ots),
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale + vky * ii,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame3, (x_poz_2 * par_scale) + vky * ii + par_scale - ots,
                                     (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale + vky * ii - ots,
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.coords(frame4, (x_poz_2 * par_scale) + ots_f, (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale + vky * ii - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig2, vky * ky / 2, 0)
                            board.move(frame3, vky * ky / 2, 0)
                            board.move(frame4, vky * ky / 2, 0)
                            board.update()
                            time.sleep(0.01)
                # для верхнего слева угла
                if y_poz_2 == 0 and x_poz_2 == 0:
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots) - vky * ii + par_scale)
                        board.coords(frame3, (x_poz_2 * par_scale) + par_scale - ots, (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - ots,
                                     (y_poz_2 * par_scale + par_scale) - vky * ii + par_scale - par_scale / 100)
                        board.coords(frame4, (x_poz_2 * par_scale) + ots_f,
                                     (y_poz_2 * par_scale) - vky * ii + 2 * par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale) - vky * ii + par_scale - ots)
                        board.update()
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange + 1)):
                        board.coords(fig2, (x_poz_2 * par_scale + ots), (y_poz_2 * par_scale + ots),
                                     (x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots) - par_scale + vky * ii,
                                     (y_poz_2 * par_scale + par_scale - 1.5 * ots))
                        board.coords(frame3, (x_poz_2 * par_scale) + par_scale + vky * ii - ots,
                                     (y_poz_2 * par_scale) + ots_f,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale + vky * ii - ots,
                                     (y_poz_2 * par_scale + par_scale - par_scale / 100))
                        board.coords(frame4, (x_poz_2 * par_scale) + ots_f, (y_poz_2 * par_scale) + par_scale - ots,
                                     (x_poz_2 * par_scale + 2 * par_scale) - par_scale + vky * ii - par_scale / 100,
                                     (y_poz_2 * par_scale + par_scale - ots))
                        board.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(par_scale / vrange)):
                            b = 1
                            board.move(fig2, -vky * ky / 2, 0)
                            board.move(frame3, -vky * ky / 2, 0)
                            board.move(frame4, -vky * ky / 2, 0)
                            board.update()
                            time.sleep(0.01)
    # для квадратов
    elif point == 9 or point == 13 or point == 11 or point == 15:
        dv = dv1 = dv2 = -1
        if x_poz_2 == 2 or x_poz_2 == 4 or x_poz_2 == 6 or x_poz_2 == 8:  # корректировка смещения точки выбора
            x_poz_2 = x_poz_2 - 1
        if y_poz_2 == 2 or y_poz_2 == 4 or y_poz_2 == 6 or y_poz_2 == 8:  # корректировка смещения точки выбора
            y_poz_2 = y_poz_2 - 1
        if par_motion == 1:
            if field[y_poz_2][x_poz_2] == 13:
                par_kvadro = 13
            elif field[y_poz_2][x_poz_2] == 15:
                par_kvadro = 15
        elif par_motion == 0 or par_motion == 2:
            if field[y_poz_2][x_poz_2] == 9:
                par_kvadro = 9
            elif field[y_poz_2][x_poz_2] == 11:
                par_kvadro = 11
        # определение векторов для хода
        if x_poz_1 == x_poz_2:
            kx = 0
            vector_kv = 1
            if y_poz_1 < y_poz_2:
                ky = 1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    # определение свободного места для каждого вектора
                    poz3 = field[y_poz_2 + 2][x_poz_2]  # верхняя левая
                    poz4 = field[y_poz_2 + 2][x_poz_2 + 1]  # верхняя правая
                    if y_poz_2 != 7 and y_poz_2 != 2:
                        poz5 = field[y_poz_2 + 3][x_poz_2]  # нижняя левая
                        poz33 = field[y_poz_2 + 3][x_poz_2]
                        poz44 = field[y_poz_2 + 3][x_poz_2 + 1]
            elif y_poz_1 > y_poz_2:
                ky = -1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    poz3 = field[y_poz_2 - 1][x_poz_2]
                    poz4 = field[y_poz_2 - 1][x_poz_2 + 1]
                    if y_poz_2 != 7 and y_poz_2 != 2:
                        poz5 = field[y_poz_2 - 2][x_poz_2]
                        poz33 = field[y_poz_2 - 2][x_poz_2]
                        poz44 = field[y_poz_2 - 2][x_poz_2 + 1]
        elif y_poz_1 == y_poz_2:
            ky = 0
            vector_kv = 1
            if x_poz_1 < x_poz_2:
                kx = 1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = field[y_poz_2][x_poz_2 + 2]
                    poz4 = field[y_poz_2 + 1][x_poz_2 + 2]
                    if x_poz_2 != 7 and x_poz_2 != 2:
                        poz5 = field[y_poz_2][x_poz_2 + 3]
                        poz33 = field[y_poz_2][x_poz_2 + 3]
                        poz44 = field[y_poz_2 + 1][x_poz_2 + 3]
            elif x_poz_1 > x_poz_2:
                kx = -1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = field[y_poz_2][x_poz_2 - 1]
                    poz4 = field[y_poz_2 + 1][x_poz_2 - 1]
                    if x_poz_2 != 7 and x_poz_2 != 2:
                        poz5 = field[y_poz_2][x_poz_2 - 2]
                        poz33 = field[y_poz_2][x_poz_2 - 2]
                        poz44 = field[y_poz_2 + 1][x_poz_2 - 2]
        # после того как нашли коэффиценты
        if abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3 and kx != 10 and ky != 10:  # ход не дальше 3
            if y_poz_2 != 9 and x_poz_2 != 9 and y_poz_2 != 0 and x_poz_2 != 0:
                # если гор фишка сверху куба
                if field[y_poz_2][x_poz_2] == par_fishki:
                    if field[y_poz_2 + 1][x_poz_2] == 0 and poz3 == 0 and poz4 == 0:
                        board.create_rectangle(x_poz_2 * par_scale + 3, y_poz_2 * par_scale + 3,
                                               x_poz_2 * par_scale + 2 * par_scale - 3,
                                               y_poz_2 * par_scale + par_scale - 3, fill=colour, tags='DV')
                        board.create_line(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + par_scale,
                                          x_poz_2 * par_scale + 2 * par_scale,
                                          y_poz_2 * par_scale + par_scale, width=4, tags='ramaDV')
                        board.create_line(x_poz_2 * par_scale + 2 * par_scale, y_poz_2 * par_scale + ots,
                                          x_poz_2 * par_scale + 2 * par_scale,
                                          y_poz_2 * par_scale + par_scale, width=4, tags='ramaDV2')
                        if ky == -1:  # исключения для красоты :3
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                        else:  # остальные случаи
                            for i in range(abs(2)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif field[y_poz_2 + 1][x_poz_2] == 0 and (poz3 != 0 or poz4 != 0):
                        board.create_rectangle(x_poz_2 * par_scale + 3, y_poz_2 * par_scale + 3,
                                               x_poz_2 * par_scale + 2 * par_scale - 3,
                                               y_poz_2 * par_scale + par_scale - 3, fill=colour)
                # если гор фишка снизу куба
                elif field[y_poz_2 + 1][x_poz_2] == par_fishki:
                    if field[y_poz_2][x_poz_2] == 0 and poz3 == 0 and poz4 == 0:
                        board.create_rectangle(x_poz_2 * par_scale + 3, y_poz_2 * par_scale + 3 + par_scale,
                                               x_poz_2 * par_scale + 2 * par_scale - 3,
                                               y_poz_2 * par_scale + par_scale - 3 + par_scale,
                                               fill=colour, tags='DV')
                        board.create_line(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + 2 * par_scale,
                                          x_poz_2 * par_scale + 2 * par_scale,
                                          y_poz_2 * par_scale + 2 * par_scale, width=4, tags='ramaDV')
                        board.create_line(x_poz_2 * par_scale + 2 * par_scale, y_poz_2 * par_scale + ots + par_scale,
                                          x_poz_2 * par_scale + 2 * par_scale,
                                          y_poz_2 * par_scale + par_scale + par_scale, width=4,
                                          tags='ramaDV2')
                        if ky == 1:
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                        else:
                            for i in range(abs(2)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif field[y_poz_2][x_poz_2] == 0 and (poz3 != 0 or poz4 != 0):
                        board.create_rectangle(x_poz_2 * par_scale + 3, y_poz_2 * par_scale + 3 + par_scale,
                                               x_poz_2 * par_scale + 2 * par_scale - 3,
                                               y_poz_2 * par_scale + par_scale - 3 + par_scale, fill=colour)
                # если верт фишка слева куба
                elif field[y_poz_2][x_poz_2] == par_fishki2:
                    if field[y_poz_2][x_poz_2 + 1] == 0 and poz3 == 0 and poz4 == 0:
                        board.create_rectangle(x_poz_2 * par_scale + 3, y_poz_2 * par_scale + 3,
                                               x_poz_2 * par_scale + par_scale - 3,
                                               y_poz_2 * par_scale + 2 * par_scale - 3, fill=colour, tags='DV')
                        board.create_line(x_poz_2 * par_scale + par_scale, y_poz_2 * par_scale + ots,
                                          x_poz_2 * par_scale + par_scale,
                                          y_poz_2 * par_scale + 2 * par_scale, width=4, tags='ramaDV')
                        board.create_line(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + 2 * par_scale,
                                          x_poz_2 * par_scale + par_scale,
                                          y_poz_2 * par_scale + 2 * par_scale, width=4, tags='ramaDV2')
                        if kx == -1:  # исключения для красоты :3
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                        else:  # остальные случаи
                            for i in range(abs(2)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif field[y_poz_2][x_poz_2 + 1] == 0 and (poz3 != 0 or poz5 != 0):
                        board.create_rectangle(x_poz_2 * par_scale + 3, y_poz_2 * par_scale + 3,
                                               x_poz_2 * par_scale + par_scale - 3,
                                               y_poz_2 * par_scale + 2 * par_scale - 3, fill=colour)
                # если верт фишка справа куба
                elif field[y_poz_2][x_poz_2 + 1] == par_fishki2:
                    if field[y_poz_2][x_poz_2] == 0 and poz3 == 0 and poz4 == 0:
                        board.create_rectangle(x_poz_2 * par_scale + 3 + par_scale, y_poz_2 * par_scale + 3,
                                               x_poz_2 * par_scale + par_scale - 3 + par_scale,
                                               y_poz_2 * par_scale + 2 * par_scale - 3,
                                               fill=colour, tags='DV')
                        board.create_line((x_poz_2 + 1) * par_scale + par_scale, y_poz_2 * par_scale + ots,
                                          (x_poz_2 + 1) * par_scale + par_scale,
                                          y_poz_2 * par_scale + 2 * par_scale, width=4, tags='ramaDV')
                        board.create_line((x_poz_2 + 1) * par_scale + ots, y_poz_2 * par_scale + 2 * par_scale,
                                          (x_poz_2 + 1) * par_scale + par_scale,
                                          y_poz_2 * par_scale + 2 * par_scale, width=4, tags='ramaDV2')
                        if kx == 1:  # исключения для красоты :3
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                        else:  # остальные случаи
                            for i in range(abs(2)):
                                for ii in range(int(par_scale / vrange)):
                                    b = 1
                                    board.move(fig3, vkx * kx, vky * ky)
                                    board.move(fig4, vkx * kx, vky * ky)
                                    board.move(frameCube1, vkx * kx, vky * ky)
                                    board.move(frameCube2, vkx * kx, vky * ky)
                                    board.move('DV', vkx * kx, vky * ky)
                                    board.move('ramaDV', vkx * kx, vky * ky)
                                    board.move('ramaDV2', vkx * kx, vky * ky)
                                    board.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif field[y_poz_2][x_poz_2] == 0 and (poz3 != 0 or poz5 != 0):
                        board.create_rectangle(x_poz_2 * par_scale + 3 + par_scale, y_poz_2 * par_scale + 3,
                                               x_poz_2 * par_scale + par_scale - 3 + par_scale,
                                               y_poz_2 * par_scale + 2 * par_scale - 3,
                                               fill=colour)
                # если пусто место для хода
                elif field[y_poz_2][x_poz_2] == 0 and vector_kv == 1:
                    if field[y_poz_2 + 1][x_poz_2] == 0 and field[y_poz_2][x_poz_2 + 1] == 0:
                        for i in range(abs(2)):
                            for ii in range(int(par_scale / vrange)):
                                b = 1
                                board.move(fig3, vkx * kx, vky * ky)
                                board.move(fig4, vkx * kx, vky * ky)
                                board.move(frameCube1, vkx * kx, vky * ky)
                                board.move(frameCube2, vkx * kx, vky * ky)
                                board.update()  # обновление
                                time.sleep(0.01)
                # если квадрат противника
                elif field[y_poz_2][x_poz_2] == par_kvadro:  # and poz3 ==  poz4 == poz33 == poz44
                    list_k = [1, 7]
                    kub_par = 0
                    board.create_line(x_poz_2 * par_scale + ots_f, y_poz_2 * par_scale + 2 * par_scale - ots + 1,
                                      x_poz_2 * par_scale + 2 * par_scale - ots,
                                      y_poz_2 * par_scale + 2 * par_scale - ots + 1,
                                      width=par_scale / 15.2, tags='ramaDV')
                    board.create_line(x_poz_2 * par_scale + 2 * par_scale - ots + 1, y_poz_2 * par_scale + ots_f,
                                      x_poz_2 * par_scale + 2 * par_scale - ots + 1,
                                      y_poz_2 * par_scale + 2 * par_scale - par_scale / 200,
                                      width=par_scale / 15.2, tags='ramaDV2')
                    if field[y_poz_2][x_poz_2] == 9 or field[y_poz_2][x_poz_2] == 13:
                        dv2 = field[y_poz_2][x_poz_2]
                        dv = board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                                    x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                                    y_poz_2 * par_scale + par_scale - 1.5 * ots,
                                                    fill=colour)
                        dv1 = board.create_rectangle(x_poz_2 * par_scale + ots, (y_poz_2 + 1) * par_scale + ots,
                                                     x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                                     (y_poz_2 + 1) * par_scale + par_scale - 1.5 * ots, fill=colour)
                    elif field[y_poz_2][x_poz_2] == 11 or field[y_poz_2][x_poz_2] == 15:
                        dv2 = field[y_poz_2][x_poz_2]
                        dv = board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                                    x_poz_2 * par_scale + par_scale - 1.5 * ots,
                                                    y_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                                    fill=colour)
                        dv1 = board.create_rectangle((x_poz_2 + 1) * par_scale + ots, y_poz_2 * par_scale + ots,
                                                     (x_poz_2 + 1) * par_scale + par_scale - 1.5 * ots,
                                                     y_poz_2 * par_scale + 2 * par_scale - 1.5 * ots, fill=colour)

                    if (dv2 == par_kvadro_gor or dv2 == par_kvadro_vert) and poz3 == poz4 == poz33 == poz44:
                        kub_par = 1
                    elif (dv2 == par_kvadro_gor or dv2 == par_kvadro_vert) and poz3 == poz4 == 0 \
                            and (y_poz_2 in list_k or x_poz_2 in list_k):
                        kub_par = 1
                    if kub_par:
                        for i in range(abs(2)):
                            for ii in range(int(par_scale / vrange)):
                                b = 1
                                board.move(fig3, vkx * kx, vky * ky)
                                board.move(fig4, vkx * kx, vky * ky)
                                board.move(frameCube1, vkx * kx, vky * ky)
                                board.move(frameCube2, vkx * kx, vky * ky)
                                board.move(dv, vkx * kx, vky * ky)
                                board.move(dv1, vkx * kx, vky * ky)
                                board.move('ramaDV', vkx * kx, vky * ky)
                                board.move('ramaDV2', vkx * kx, vky * ky)
                                board.update()  # обновление
                                time.sleep(0.01)
            # если гор фишка на базе
            elif field[y_poz_2][x_poz_2] == par_fishki and (y_poz_2 == 9 or y_poz_2 == 0):
                board.create_rectangle(x_poz_2 * par_scale + ots, y_poz_2 * par_scale + ots,
                                       x_poz_2 * par_scale + 2 * par_scale - 1.5 * ots,
                                       y_poz_2 * par_scale + par_scale - 1.5 * ots,
                                       fill=colour, tags='DV')
                board.create_line(x_poz_2 * par_scale + ots_f, y_poz_2 * par_scale + par_scale - ots,
                                  x_poz_2 * par_scale + 2 * par_scale - par_scale / 100,
                                  y_poz_2 * par_scale + par_scale - ots,
                                  width=par_scale / 12.5, tags='ramaDV')
                board.create_line(x_poz_2 * par_scale + 2 * par_scale - ots, y_poz_2 * par_scale + ots_f,
                                  x_poz_2 * par_scale + 2 * par_scale - ots,
                                  y_poz_2 * par_scale + par_scale - par_scale / 100,
                                  width=par_scale / 12.5, tags='ramaDV2')
                for i in range(abs(1)):
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig3, vkx * kx, vky * ky)
                        board.move(fig4, vkx * kx, vky * ky)
                        board.move(frameCube1, vkx * kx, vky * ky)
                        board.move(frameCube2, vkx * kx, vky * ky)
                        board.move('DV', vkx * kx, vky * ky)
                        board.move('ramaDV', vkx * kx, vky * ky)
                        board.move('ramaDV2', vkx * kx, vky * ky)
                        board.update()  # обновление
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig3, -vkx * kx, -vky * ky)
                        board.move(fig4, -vkx * kx, -vky * ky)
                        board.move(frameCube1, -vkx * kx, -vky * ky)
                        board.move(frameCube2, -vkx * kx, -vky * ky)
                        board.update()  # обновление
                        time.sleep(0.01)
            # если верт фишка на базе
            elif field[y_poz_2][x_poz_2] == par_fishki2 and (x_poz_2 == 9 or x_poz_2 == 0):
                board.create_rectangle(x_poz_2 * par_scale + 3, y_poz_2 * par_scale + 3,
                                       x_poz_2 * par_scale + par_scale - 3,
                                       y_poz_2 * par_scale + 2 * par_scale - 3, fill=colour, tags='DV')
                board.create_line(x_poz_2 * par_scale + par_scale - ots, y_poz_2 * par_scale + ots_f,
                                  x_poz_2 * par_scale + par_scale - ots,
                                  y_poz_2 * par_scale + 2 * par_scale - par_scale / 100, width=par_scale / 12.5,
                                  tags='ramaDV')
                board.create_line(x_poz_2 * par_scale + ots_f, y_poz_2 * par_scale + 2 * par_scale - ots,
                                  x_poz_2 * par_scale + par_scale - par_scale / 100,
                                  y_poz_2 * par_scale + 2 * par_scale - ots,
                                  width=par_scale / 12.5, tags='ramaDV2')
                for i in range(abs(1)):
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig3, vkx * kx, vky * ky)
                        board.move(fig4, vkx * kx, vky * ky)
                        board.move(frameCube1, vkx * kx, vky * ky)
                        board.move(frameCube2, vkx * kx, vky * ky)
                        board.move('DV', vkx * kx, vky * ky)
                        board.move('ramaDV', vkx * kx, vky * ky)
                        board.move('ramaDV2', vkx * kx, vky * ky)
                        board.update()  # обновление
                        time.sleep(0.01)
                    for ii in range(int(par_scale / vrange)):
                        b = 1
                        board.move(fig3, -vkx * kx, -vky * ky)
                        board.move(fig4, -vkx * kx, -vky * ky)
                        board.move(frameCube1, -vkx * kx, -vky * ky)
                        board.move(frameCube2, -vkx * kx, -vky * ky)
                        board.update()  # обновление
                        time.sleep(0.01)


# выбор клетки для хода 1
def position_1(event):
    global poz1_x, poz1_y
    global hor1, hor2, ver1, ver2, sq1, sq2, sq3, sq4
    x, y = event.x // int(par_scale), event.y // int(par_scale)  # вычисляем координаты клетки
    even_list = [2, 4, 6, 8]
    odd_list = [1, 3, 5, 7]
    # функция рамки квадратов
    if par_motion == 1:
        hor1 = 1
        hor2 = 5
        ver1 = 2
        ver2 = 7
        sq1 = 9
        sq2 = 10
        sq3 = 11
        sq4 = 12
    elif par_motion == 2 or par_motion == 0:
        hor1 = 3
        hor2 = 6
        ver1 = 4
        ver2 = 8
        sq1 = 13
        sq2 = 14
        sq3 = 15
        sq4 = 16


    def frame_cut(x, y, poz1_y, poz1_x):  # что бы не писать код дважды
        if 0 < x < 9 and 0 < y < 9:
            if (y == poz1_y and x == poz1_x - 2) or (y == poz1_y - 2 and x == poz1_x) or (
                    y == poz1_y and x == poz1_x + 2) \
                    or (y == poz1_y + 2 and x == poz1_x):
                if field[y][x] == 0 and field[y + 1][x] == 0 and field[y][x + 1] == 0 and field[y + 1][x + 1] == 0:
                    board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3, x * par_scale + 2 * par_scale - 3,
                                 y * par_scale + 2 * par_scale - 3)
            elif (y == poz1_y and x == poz1_x - 1) or (y == poz1_y - 2 and x == poz1_x + 1) or (
                    y == poz1_y and x == poz1_x + 3) \
                    or (y == poz1_y + 2 and x == poz1_x + 1):
                if field[y][x] == 0 and field[y + 1][x] == 0 and field[y][x - 1] == 0 and field[y + 1][x - 1] == 0:
                    board.coords(frame_yellow, x * par_scale + 3 - par_scale, y * par_scale + 3,
                                 x * par_scale + 2 * par_scale - 3 - par_scale,
                                 y * par_scale + 2 * par_scale - 3)
            elif (y == poz1_y + 1 and x == poz1_x - 2) or (y == poz1_y - 1 and x == poz1_x) or (
                    y == poz1_y + 1 and x == poz1_x + 2) \
                    or (y == poz1_y + 3 and x == poz1_x):
                if field[y][x] == 0 and field[y - 1][x] == 0 and field[y][x + 1] == 0 and field[y - 1][x + 1] == 0:
                    board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3 - par_scale,
                                 x * par_scale + 2 * par_scale - 3,
                                 y * par_scale + 2 * par_scale - 3 - par_scale)
            elif (y == poz1_y + 1 and x == poz1_x - 1) or (y == poz1_y - 1 and x == poz1_x + 1) or (
                    y == poz1_y + 1 and x == poz1_x + 3) \
                    or (y == poz1_y + 3 and x == poz1_x + 1):
                if field[y][x] == 0 and field[y - 1][x] == 0 and field[y][x - 1] == 0 and field[y - 1][x - 1] == 0:
                    board.coords(frame_yellow, x * par_scale + 3 - par_scale, y * par_scale + 3 - par_scale,
                                 x * par_scale + 2 * par_scale - 3 - par_scale,
                                 y * par_scale + 2 * par_scale - 3 - par_scale)

    # создание рамок для фигур
    if x < 10 and y < 10:  # ограничение области для исключений
        # рамка для горизонта фишек
        if field[y][x] == 1 or field[y][x] == 5 or field[y][x] == 3 or field[y][x] == 6:
            if field[y][x] == 5 or field[y][x] == 6:
                x = x - 1
            board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3, x * par_scale + 2 * par_scale - 3,
                         y * par_scale + par_scale - 3)
        # рамка для верт фишек
        elif field[y][x] == 2 or field[y][x] == 7 or field[y][x] == 4 or field[y][x] == 8:
            if field[y][x] == 7 or field[y][x] == 8:
                y = y - 1
            board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3, x * par_scale + par_scale - 3,
                         y * par_scale + 2 * par_scale - 3)
        # квадраты горизонт
        elif field[y][x] == 9 or field[y][x] == 10 or field[y][x] == 13 or field[y][x] == 14:
            if field[y][x] == 10 or field[y][x] == 14:
                x = x - 1
            if field[y][x] == field[y - 1][x] and y in even_list:
                y = y - 1
            board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3, x * par_scale + 2 * par_scale - 3,
                         y * par_scale + 2 * par_scale - 3)
        # квадраты вертикаль
        elif field[y][x] == 11 or field[y][x] == 12 or field[y][x] == 15 or field[y][x] == 16:
            if field[y][x] == 12 or field[y][x] == 16:
                y = y - 1
            if field[y][x] == field[y][x - 1] and x in even_list:
                x = x - 1
            board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3, x * par_scale + 2 * par_scale - 3,
                         y * par_scale + 2 * par_scale - 3)
        # рамка хода для горизонтальных одиночных фишек игрока
        elif field[poz1_y][poz1_x] == hor1 or field[poz1_y][poz1_x] == hor2:
            if field[poz1_y][poz1_x] == hor2 and field[poz1_y][poz1_x - 1] == hor1:
                poz1_x = poz1_x - 1
            if (y == poz1_y + 1 and x == poz1_x) or (y == poz1_y + 1 and x == poz1_x + 1) or (
                    y == poz1_y - 1 and x == poz1_x + 1) \
                    or (y == poz1_y - 1 and x == poz1_x) or (y == poz1_y and x == poz1_x - 2) or (
                    y == poz1_y and x == poz1_x - 1) \
                    or (y == poz1_y and x == poz1_x + 2) or (y == poz1_y and x == poz1_x + 3):
                if x in even_list:
                    if field[y][x - 1] == 0 and field[y][x] == 0:
                        board.coords(frame_yellow, x * par_scale + 3 - par_scale, y * par_scale + 3,
                                     x * par_scale + 2 * par_scale - 3 - par_scale,
                                     y * par_scale + par_scale - 3)
                elif x in odd_list:
                    if field[y][x] == 0 and field[y][x + 1] == 0:
                        board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3,
                                     x * par_scale + 2 * par_scale - 3,
                                     y * par_scale + par_scale - 3)
        # рамка хода для вертикальных одиночных фишек игрока
        elif field[poz1_y][poz1_x] == ver1 or field[poz1_y][poz1_x] == ver2:
            if field[poz1_y][poz1_x] == ver2 and field[poz1_y - 1][poz1_x] == ver1:
                poz1_y = poz1_y - 1
            if (y == poz1_y + 2 and x == poz1_x) or (y == poz1_y + 3 and x == poz1_x) or (
                    y == poz1_y - 1 and x == poz1_x) or \
                    (y == poz1_y - 2 and x == poz1_x) or (y == poz1_y and x == poz1_x - 1) or (
                    y == poz1_y + 1 and x == poz1_x - 1) or \
                    (y == poz1_y + 1 and x == poz1_x + 1) or (y == poz1_y and x == poz1_x + 1):
                if y in even_list:
                    if field[y - 1][x] == 0 and field[y][x] == 0:  # (field[y][x] == 0 and field[y + 1][x] == 0) or
                        board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3 - par_scale,
                                     x * par_scale + par_scale - 3,
                                     y * par_scale + 2 * par_scale - 3 - par_scale)
                elif y in odd_list:
                    if field[y][x] == 0 and field[y + 1][x] == 0:
                        board.coords(frame_yellow, x * par_scale + 3, y * par_scale + 3, x * par_scale + par_scale - 3,
                                     y * par_scale + 2 * par_scale - 3)
        # рамка хода для горизонтальных квадратов игрока
        elif field[poz1_y][poz1_x] == sq1 or field[poz1_y][poz1_x] == sq2:
            if field[poz1_y][poz1_x] == sq2:
                poz1_x = poz1_x - 1
            if field[poz1_y][poz1_x] == field[poz1_y - 1][poz1_x] == sq1 and poz1_y in even_list:
                poz1_y = poz1_y - 1
            frame_cut(x, y, poz1_y, poz1_x)
        # рамка хода для вертикальных квадратов игрока
        elif field[poz1_y][poz1_x] == sq3 or field[poz1_y][poz1_x] == sq4:
            if field[poz1_y][poz1_x] == sq4:
                poz1_y = poz1_y - 1
            if field[poz1_y][poz1_x] == field[poz1_y][poz1_x - 1] == sq3 and poz1_x in even_list:
                poz1_x = poz1_x - 1
            frame_cut(x, y, poz1_y, poz1_x)


# выбор клетки для хода 2
def position_2(event):
    global poz1_x, poz1_y, poz2_x, poz2_y
    global par_motion
    global cube
    # ход игрока и параметр b запрещает дублировать анимацию хода, если тот сделан
    if (par_motion == 1 or par_motion == 2) and b == 0:
        x, y = event.x // int(par_scale), event.y // int(par_scale)  # вычисляем координаты клетки
        if cube:
            # рамка выбора горизонт фигуры игрока
            if x < 10 and y < 10:  # fix щелчка за игровое поле
                if field[y][x] == hor1 or field[y][x] == hor2:
                    if field[y][x] == hor2:
                        x = x - 1
                    board.coords(frame_blue, x * par_scale + 3, y * par_scale + 3, x * par_scale + 2 * par_scale - 3,
                                 y * par_scale + par_scale - 3)  # рамка в выбранной клетке
                    poz1_x, poz1_y = x, y
                # рамка выбора вертикальных фигур игрока
                elif field[y][x] == ver1 or field[y][x] == ver2:
                    if field[y][x] == ver2:
                        y = y - 1
                    board.coords(frame_blue, x * par_scale + 3, y * par_scale + 3, x * par_scale + par_scale - 3,
                                 y * par_scale + 2 * par_scale - 3)  # рамка в выбранной клетке
                    poz1_x, poz1_y = x, y
                # квадраты игрока
                elif field[y][x] == sq1 or field[y][x] == sq2:
                    if field[y][x] == sq2:
                        x = x - 1
                    if field[y][x] == field[y - 1][x] and (y == 2 or y == 4 or y == 6 or y == 8):
                        y = y - 1
                    board.coords(frame_blue, x * par_scale + 3, y * par_scale + 3, x * par_scale + 2 * par_scale - 3,
                                 y * par_scale + 2 * par_scale - 3)
                    poz1_x, poz1_y = x, y
                elif field[y][x] == sq3 or field[y][x] == sq4:
                    if field[y][x] == sq4:
                        y = y - 1
                    if field[y][x] == field[y][x - 1] and (x == 2 or x == 4 or x == 6 or x == 8):
                        x = x - 1
                    board.coords(frame_blue, x * par_scale + 3, y * par_scale + 3, x * par_scale + 2 * par_scale - 3,
                                 y * par_scale + 2 * par_scale - 3)
                    poz1_x, poz1_y = x, y
                # когда выбрана фигура делаем ход
                else:
                    if poz1_x != -1:  # клетка выбрана
                        poz2_x, poz2_y = x, y
                        if cube > 0:
                            copy_pole = copy.deepcopy(field)
                            motion(poz1_x, poz1_y, poz2_x, poz2_y)
                            board.update()
                            if copy_pole != field:
                                cube -= 1
                                the_end()
                        poz1_x = -1  # клетка не выбрана
                        board.coords(frame_blue, -5, -5, -5, -5)  # рамка вне поля
        if cube == 0:  # закончился ход
            if par_motion == 1 and mode == 2:  # игра с игроком
                par_motion = 2
            elif par_motion == 1 and mode == 1:  # игра с компьютером
                par_motion = 0
            elif par_motion == 2:  # игра с игроком
                par_motion = 1
            determinant(par_motion)


# Переход хода
def determinant(par_motion):
    global a
    global cube
    a = 1
    colour = 0
    cube = random.randint(1, 6)
    u = scale / 10
    board.update()
    background.update()
    background.delete('all')
    background.create_rectangle(int(1.14 * scale), int(0.34 * scale), int(1.56 * scale), int(0.76 * scale),
                                fill='black',
                                outline="black")  # белый фон
    background.create_rectangle(int(1.15 * scale), int(0.35 * scale), int(1.55 * scale), int(0.75 * scale),
                                fill='white', outline="black")  # фон куба
    # кубик
    if cube:
        if par_motion == 1:
            colour = 'red'
        elif par_motion == 0 or par_motion == 2:
            colour = 'green'

        if cube == 1:
            background.create_oval(int(1.30 * scale), int(0.50 * scale), int(1.40 * scale), int(0.60 * scale),
                                   fill=colour,
                                   outline="black")  # выпало 1
        elif cube == 2:
            background.create_oval(int(1.21 * scale), int(0.50 * scale), int(1.31 * scale), int(0.60 * scale),
                                   fill=colour,
                                   outline="black")  # выпало 2
            background.create_oval(int(1.39 * scale), int(0.50 * scale), int(1.49 * scale), int(0.60 * scale),
                                   fill=colour,
                                   outline="black")
        elif cube == 3:
            background.create_oval(int(1.17 * scale), int(0.63 * scale), int(1.27 * scale), int(0.73 * scale),
                                   fill=colour,
                                   outline="black")  # выпало 3
            background.create_oval(int(1.30 * scale), int(0.50 * scale), int(1.40 * scale), int(0.60 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.43 * scale), int(0.37 * scale), int(1.53 * scale), int(0.47 * scale),
                                   fill=colour,
                                   outline="black")
        elif cube == 4:
            background.create_oval(int(1.21 * scale), int(0.60 * scale), int(1.31 * scale), int(0.70 * scale),
                                   fill=colour,
                                   outline="black")  # выпало 4
            background.create_oval(int(1.39 * scale), int(0.60 * scale), int(1.49 * scale), int(0.70 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.21 * scale), int(0.40 * scale), int(1.31 * scale), int(0.50 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.39 * scale), int(0.40 * scale), int(1.49 * scale), int(0.50 * scale),
                                   fill=colour,
                                   outline="black")
        elif cube == 5:
            background.create_oval(int(1.30 * scale), int(0.50 * scale), int(1.40 * scale), int(0.60 * scale),
                                   fill=colour,
                                   outline="black")  # выпало 5
            background.create_oval(int(1.21 * scale), int(0.60 * scale), int(1.31 * scale), int(0.70 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.39 * scale), int(0.60 * scale), int(1.49 * scale), int(0.70 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.21 * scale), int(0.40 * scale), int(1.31 * scale), int(0.50 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.39 * scale), int(0.40 * scale), int(1.49 * scale), int(0.50 * scale),
                                   fill=colour,
                                   outline="black")
        elif cube == 6:
            background.create_oval(int(1.17 * scale), int(0.60 * scale), int(1.27 * scale), int(0.70 * scale),
                                   fill=colour,
                                   outline="black")  # выпало 6
            background.create_oval(int(1.30 * scale), int(0.60 * scale), int(1.40 * scale), int(0.70 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.43 * scale), int(0.60 * scale), int(1.53 * scale), int(0.70 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.17 * scale), int(0.40 * scale), int(1.27 * scale), int(0.50 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.30 * scale), int(0.40 * scale), int(1.40 * scale), int(0.50 * scale),
                                   fill=colour,
                                   outline="black")
            background.create_oval(int(1.43 * scale), int(0.40 * scale), int(1.53 * scale), int(0.50 * scale),
                                   fill=colour,
                                   outline="black")

    if par_motion == 0:
        background.create_text(int(1.35 * scale), int(0.2 * scale), text='ХОД КОМПЬЮТЕРА', justify=tkinter.CENTER,
                               font=f'Helvetica 30 bold', fill='black')
        background.create_text(int(1.35 * scale), int(0.26 * scale), text=cube, justify=tkinter.CENTER,
                               font=f'Verdana {int(u / 2.5)}', fill='black')
        if cube:
            motion_comp(cube)

    elif par_motion == 1:  # ход игрока
        background.create_text(int(1.35 * scale), int(0.2 * scale), text='ХОД ИГРОКА', justify=tkinter.CENTER,
                               font=f'Helvetica 30 bold', fill='black')
        background.create_text(int(1.35 * scale), int(0.26 * scale), text=cube, justify=tkinter.CENTER,
                               font=f'Aesthetic {int(u / 2.5)}', fill='black')
        if cube:
            board.bind("<Button-1>", position_2)
    elif par_motion == 2:  # ход второго игрока
        background.create_text(int(1.35 * scale), int(0.2 * scale), text='ХОД ВТОРОГО ИГРОКА', justify=tkinter.CENTER,
                               font=f'Helvetica 30 bold', fill='black')
        background.create_text(int(1.35 * scale), int(0.26 * scale), text=cube, justify=tkinter.CENTER,
                               font=f'Aesthetic {int(u / 2.5)}', fill='black')
        if cube:
            board.bind("<Button-1>", position_2)


# Распределение ходов
def motion(poz1_x, poz1_y, poz2_x, poz2_y):
    global field
    global par_motion
    global cube
    global field

    conclusion(poz1_x, poz1_y, poz2_x, poz2_y, 1)  # рисуем игровое поле
    if par_motion == 1 or par_motion == 2:
        if field[poz1_y][poz1_x] == hor1 or field[poz1_y][poz1_x] == sq1:
            hor_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y)
        elif field[poz1_y][poz1_x] == hor2 and field[poz1_y][poz1_x - 1] == hor1 \
                or field[poz1_y][poz1_x] == sq2 and field[poz1_y][poz1_x - 1] == sq1:
            poz1_x = poz1_x - 1
            hor_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y)
        elif field[poz1_y][poz1_x] == ver1 or field[poz1_y][poz1_x] == sq3:
            vert_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y)
        elif field[poz1_y][poz1_x] == ver2 and field[poz1_y - 1][poz1_x] == ver1 \
                or field[poz1_y][poz1_x] == sq4 and field[poz1_y - 1][poz1_x] == sq3:
            poz1_y = poz1_y - 1
            vert_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y)
    elif par_motion == 0:
        if field[poz1_y][poz1_x] == 3 or field[poz1_y][poz1_x] == 13:
            hor_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y)
        elif field[poz1_y][poz1_x] == 4 or field[poz1_y][poz1_x] == 15:
            vert_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y)
    board.update()
    conclusion(poz1_x, poz1_y, poz2_x, poz2_y, 0)  # рисуем игровое поле после хода


# ход компьютера
def motion_comp(kub1):
    global par_motion, end_game
    global field, end_p
    end_game = 0
    time.sleep(0.5)
    case = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, -2], [-2, 0], [0, 2], [2, 0]]
    end_game = 0
    while kub1 > 0:  # ход компьютера отсюда все ходы кубика
        iy = random.randint(0, 9)  #
        ix = random.randint(0, 9)  # 36 48 1314 1516
        # print(end_game, kub1)
        end_game += 1
        list_of_squares = [13, 15]
        if end_game == 1500:
            message(3)
            break
        the_end()
        if end_p:
            break

        # если рандом горизонтальная фишка
        if field[iy][ix] == 3:  # для горизонтальных фишек
            h1 = random.choice((case[1], case[3], case[4], case[6]))  # рандом хода ↓ 1 ↑ 1  ← 2 → 2
            h2 = random.choice((case[4], case[6]))  # ← 2 → 2
            trans = 0
            even_list = [2, 4, 6, 8]
            if cube > 0:
                # ↑ 24 ↓ 25 → 26 ← 27
                # if (mode == 1 or mode == 2 or mode == 3): #проверяем сложность компьютера
                # ходы внизу
                if iy == 9 or iy == 8 or iy == 7:  # ↓
                    # выбивание на базе снизу, поворот на углу и трансформация в куб
                    if iy == 9 or iy == 8:
                        # выбивание если противник слева на базе ↑ ← ↓
                        if field[iy][ix - 2] == 1 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy - 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy - 1][ix] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy - 1, ix - 2, iy - 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy - 1][ix - 2] == 3:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix - 2, iy - 1, ix - 2, iy)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # выбивание если противник справа на базе ↑ → ↓
                        elif field[iy][ix + 2] == 1 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy - 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy - 1][ix] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy - 1, ix + 2, iy - 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy - 1][ix + 2] == 3:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix - 2, iy - 1, ix - 2, iy)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif iy == 8:
                            # толкаем противника с базы ↓
                            if field[iy + 1][ix] == 1:
                                copy_pole1 = field
                                motion(ix, iy, ix, iy + 1)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                            # если загородили путь своей фишкой, делаем квадрат 1↑ 2↑
                            elif field[iy + 1][ix] == 3 and (mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix, iy - 1)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix, iy + 1, ix, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                        # поворот на углу снизу
                        elif iy == 9:
                            if (field[iy - 1][ix] == 1 or field[iy - 1][ix] == 9 or field[iy - 1][ix] == 11) and (
                                    mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix + h2[1], iy + h2[0])
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                    # выводим противника к базе снизу
                    if (iy == 7 or iy == 8) and kub1 > 0:
                        # справа снизу → ↓
                        if field[iy + 1][ix + 2] == 1:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix + 2, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix + 2] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix + 2, iy, ix + 2, iy + 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                        # слева снизу ← ↓
                        elif field[iy + 1][ix - 2] == 1:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix - 2, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix - 2] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix - 2, iy, ix - 2, iy + 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                # ходы сверху
                elif iy == 2 or iy == 1 or iy == 0:  # ↑
                    # выбивание на базе сверху, поворот на углу и трансформация в куб
                    if iy == 1 or iy == 0:
                        # выбивание если противник справа на базе ↓ → ↑
                        if field[iy][ix + 2] == 1 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy + 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy + 1][ix] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy + 1, ix + 2, iy + 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy - 1][ix + 2] == 3:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix + 2, iy + 1, ix + 2, iy)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # выбивание если противник слева на базе ↓ ← ↑
                        elif field[iy][ix - 2] == 1 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy + 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy + 1][ix] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy + 1, ix + 2, iy - 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy + 1][ix + 2] == 3:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix + 2, iy + 1, ix + 2, iy)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif iy == 1:
                            # толкаем противника с базы ↑
                            if field[iy - 1][ix] == 1:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix, iy - 1)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                            # если загородили путь своей, делаем квадрат 1↓ 2↓
                            elif field[iy - 1][ix] == 3 and (mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix, iy + 1)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix, iy - 1, ix, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                        # уход от противника и на угол
                        elif iy == 0:
                            if (field[iy + 1][ix] == 1 or field[iy + 1][ix] == 9 or field[iy + 1][ix] == 11) and (
                                    mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix + h2[1], iy + h2[0])
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                    # выводим противника к базе сверху
                    if (iy == 1 or iy == 2) and kub1 > 0:
                        # сверху слева ← ↑
                        if field[iy - 1][ix - 2] == 1:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix - 2, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix - 2] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix - 2, iy, ix - 2, iy - 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                        # сверху справа → ↑
                        elif field[iy - 1][ix + 2] == 1:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix + 2, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix + 2] == 3:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix + 2, iy, ix + 2, iy - 1)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # уходим если наш квадрат может выбить противника
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and (mode == 2 or mode == 3):
                    if ix == 1 and field[iy][ix - 1] == 2 and field[iy][ix + 2] in list_of_squares:
                        if iy in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy + 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                        elif iy not in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy - 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                    elif ix == 7 and field[iy][ix + 2] == 2 and field[iy][ix - 2] in list_of_squares:
                        if iy in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy + 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                        elif iy not in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy - 1)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # ходы влево и вправо для разбития или трансформации
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and mode == 3:
                    # вправо →
                    if field[iy][ix + 2] == 9:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                    # влево ←
                    elif field[iy][ix - 2] == 9:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix - 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                    # трансформация в куб ← верхняя
                    elif field[iy + 1][ix - 2] == 3 and iy not in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix - 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ← нижняя
                    elif field[iy - 1][ix - 2] == 3 and iy in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix - 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб → верхняя
                    elif field[iy + 1][ix + 2] == 3 and iy not in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб → нижняя
                    elif field[iy - 1][ix + 2] == 3 and iy in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб ↑
                if (iy == 3 or iy == 5 or iy == 7 or iy == 9) and kub1 > 0 and trans == 0 and (mode == 2 or mode == 3):
                    if field[iy - 2][ix] == 3:  # подъем для квадрата, нельзя равняться 1
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy - 1)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб ↓
                if (iy == 0 or iy == 2 or iy == 4 or iy == 6) and kub1 > 0 and trans == 0 and (mode == 2 or mode == 3):
                    if field[iy + 2][ix] == 3:  # спуск для квадрата, нельзя равняться 8
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy + 1)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # когда нет вышеупомянутых ходов, есть ходы и фишка на том же месте
                if 0 < ix + h1[1] < 9 and 0 <= iy + h1[0] <= 9 and kub1 > 0 and field[iy][ix] == 3:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + h1[1], iy + h1[0])
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
        # если рандом вертикальная фишка
        elif field[iy][ix] == 4:

            h1 = random.choice((case[0], case[2], case[5], case[-1]))  # рандом первого хода
            h2 = random.choice((case[5], case[-1]))
            trans = 0
            even_list = [2, 4, 6, 8]
            # ↑ 24 ↓ 25 → 26 ← 27
            if cube > 0:
                # ходы справа
                if ix == 9 or ix == 8 or ix == 7:
                    # выбивание на базе справа, поворот на углу и трансформация в куб
                    if ix == 9 or ix == 8:
                        # выбивание если противник сверху на базе ← ↑ →
                        if field[iy - 2][ix] == 2 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix - 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix - 1] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix - 1, iy, ix - 1, iy - 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy - 2][ix - 1] == 4:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix - 1, iy - 2, ix, iy - 2)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # выбивание если противник снизу на базе ← ↓ →
                        elif field[iy + 2][ix] == 2 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix - 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix - 1] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix - 1, iy, ix - 1, iy + 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy + 2][ix - 1] == 4:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix - 1, iy + 2, ix, iy + 2)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif ix == 8:
                            # толкаем противника с базы →
                            if field[iy][ix + 1] == 2:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix + 1, iy)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                            # если загородили путь своей, делаем квадрат
                            elif field[iy][ix + 1] == 4 and (mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix - 1, iy)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix + 1, iy, ix, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                        elif ix == 9:
                            if (field[iy][ix - 1] == 2 or field[iy][ix - 1] == 9 or field[iy][ix - 1] == 11) and (
                                    mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix + h2[1], iy + h2[0])
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                    # выводим противника к базе справа
                    if (ix == 7 or ix == 8) and kub1 > 0:
                        # справа снизу
                        if field[iy + 2][ix + 1] == 2:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy + 2)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy + 2][ix] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy + 2, ix + 1, iy + 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                        # справа сверху
                        elif field[iy - 2][ix + 1] == 2:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy - 2)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy - 2][ix] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy - 2, ix + 1, iy - 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                # ходы слева
                elif ix == 2 or ix == 1 or ix == 0:
                    # выбивание на базе слева, поворот на углу и трансформация в куб
                    if ix == 1 or ix == 0:
                        # выбивание если противник справа на базе ↓ → ↑
                        if field[iy - 2][ix] == 2 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix + 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix + 1] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix + 1, iy, ix + 1, iy - 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy - 2][ix + 1] == 4:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix + 1, iy - 2, ix, iy - 2)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # выбивание если противник слева на базе ↓ ← ↑
                        elif field[iy + 2][ix] == 2 and (mode == 2 or mode == 3):
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix + 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy][ix + 1] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix + 1, iy, ix + 1, iy + 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and field[iy + 2][ix + 1] == 4:
                                            copy_pole1 = copy.deepcopy(field)
                                            motion(ix + 1, iy + 2, ix, iy + 2)
                                            if copy_pole1 != field:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif ix == 1:
                            # толкаем противника с базы
                            if field[iy][ix - 1] == 2:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix - 1, iy)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                            # если загородили путь своей, делаем квадрат
                            elif field[iy][ix - 1] == 4 and (mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix + 1, iy)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix - 1, iy, ix, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                        # уход от противника и на угол
                        elif ix == 9:
                            if (field[iy][ix + 1] == 2 or field[iy][ix + 1] == 9 or field[iy][ix + 1] == 11) and (
                                    mode == 2 or mode == 3):
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy, ix + h2[1], iy + h2[0])
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                    if (ix == 1 or ix == 2) and kub1 > 0:  # выводим противника к базе слева
                        # слева сверху
                        if field[iy - 2][ix - 1] == 2:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy - 2)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy - 2][ix] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy - 2, ix - 1, iy - 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                        # слева снизу
                        elif field[iy + 2][ix - 1] == 2:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix, iy + 2)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                                if kub1 > 0 and field[iy + 2][ix] == 4:
                                    copy_pole1 = copy.deepcopy(field)
                                    motion(ix, iy + 2, ix - 1, iy + 2)
                                    if copy_pole1 != field:
                                        kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # уходим если наш квадрат может выбить противника
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and (mode == 2 or mode == 3):
                    if iy == 1 and field[iy - 1][ix] == 1 and field[iy + 2][ix] in list_of_squares:
                        if ix in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix + 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                        elif ix not in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix - 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                    elif iy == 7 and field[iy + 2][ix] == 2 and field[iy - 2][ix] in list_of_squares:
                        if ix in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix + 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                        elif ix not in even_list:
                            copy_pole1 = copy.deepcopy(field)
                            motion(ix, iy, ix - 1, iy)
                            if copy_pole1 != field:
                                kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # ходы вниз и вверх для разбития или трансформации
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and mode == 3:
                    # вниз ↓
                    if field[iy + 1][ix] == 11:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                    # вверх ↑
                    elif field[iy][ix - 2] == 11:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix - 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                    # трансформация в куб ↓ правая
                    elif field[iy + 2][ix + 1] == 4 and ix not in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy + 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ↓ левая
                    elif field[iy + 2][ix - 1] == 4 and ix in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy + 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ↑ правая
                    elif field[iy - 2][ix + 1] == 4 and ix not in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy - 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ↑ левая
                    elif field[iy - 2][ix - 1] == 4 and ix in even_list and trans == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy - 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб
                if (ix == 3 or ix == 5 or ix == 7 or ix == 9) and kub1 > 0 and trans == 0 and (
                        mode == 2 or mode == 3):  # трансформация в куб left
                    if field[iy][ix - 2] == 4:  # берем влево для квадрата, нельзя равняться 1
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix - 1, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб
                if (ix == 0 or ix == 2 or ix == 4 or ix == 6) and kub1 > 0 and trans == 0 and (
                        mode == 2 or mode == 3):  # трансформация в куб right
                    if field[iy][ix + 2] == 4:  # берем вправо для квадрата, нельзя равняться 8
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 1, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # когда нет вышеупомянутых ходов, есть ходы и фишка на том же месте
                if 0 <= ix + h1[1] <= 9 and 0 < iy + h1[0] < 9 and kub1 > 0 and field[iy][ix] == 4:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + h1[1], iy + h1[0])
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
        # если рандом квадрат и выбираем только голову куба
        elif field[iy][ix] == 13 and field[iy + 1][ix] == 13 and (iy == 1 or iy == 3 or iy == 5 or iy == 7) \
                or field[iy][ix] == 15 and field[iy][ix + 1] == 15 and (ix == 1 or ix == 3 or ix == 5 or ix == 7):
            h1 = random.choice((case[4], case[5], case[-2], case[-1]))
            spisok_kvdr = [1, 2, 9, 11]
            # квадрат выталкивает влево фигуры к базе
            if ix == 3 and field[iy][ix - 3] == 0:
                if field[iy][ix - 2] in spisok_kvdr or field[iy + 1][ix - 2] == 1 or field[iy][ix - 1] == 2:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if ix == 3 and field[iy][ix - 3] == 2 and kub1 > 0 and (mode == 2 or mode == 3):
                if field[iy][ix - 2] == field[iy + 1][ix - 2] == field[iy][ix - 1] == 0:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # квадрат выталкивает вверх фигуры к базе
            if iy == 3 and field[iy - 3][ix] == 0 and kub1 > 0:
                if field[iy - 2][ix] in spisok_kvdr or field[iy - 1][ix] == 1 or field[iy - 2][ix + 1] == 2:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if iy == 3 and field[iy - 3][ix] == 1 and kub1 > 0 and (mode == 2 or mode == 3):
                if field[iy - 2][ix] == field[iy - 1][ix] == field[iy - 2][ix + 1] == 0:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # квадрат выталкивает вправо фигуры к базе
            if ix == 5 and field[iy][ix + 4] == 0 and kub1 > 0:
                if field[iy][ix + 2] in spisok_kvdr or field[iy + 1][ix + 2] == 1 or field[iy][ix + 3] == 2:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if ix == 5 and field[iy][ix + 4] == 2 and kub1 > 0 and (mode == 2 or mode == 3):
                if field[iy][ix + 2] == field[iy + 1][ix + 2] == field[iy][ix + 3] == 0:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # квадрат выталкивает вниз фигуры к базе
            if iy == 5 and field[iy + 4][ix] == 0 and kub1 > 0:
                if field[iy + 2][ix] in spisok_kvdr or field[iy + 3][ix] == 1 or field[iy + 2][ix + 1] == 2:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy + 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if iy == 5 and field[iy + 4][ix] == 1 and kub1 > 0 and (mode == 2 or mode == 3):
                if field[iy + 2][ix] == field[iy + 3][ix] == field[iy + 2][ix + 1] == 0:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy + 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # слева
            if ix == 1 and kub1 > 0:
                # квадрат слева у базы. на базе враг
                if field[iy][ix - 1] == 2:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 1, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy - 1][ix] == 1 and iy == 1:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 1)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy + 2][ix] == 1 and iy == 7:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy + 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # ограждение противника сверху
                elif field[iy - 2][ix - 1] == 2 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # ограждение противника снизу
                elif field[iy + 2][ix - 1] == 2 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy + 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (field[iy][ix + 2] == 9 or field[iy][ix + 2] == 11) and mode == 3:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                    else:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy + 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                # обходим противника вправо вниз влево
                if field[iy + 2][ix] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy + 2][ix - 1] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy][ix + 2] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix + 2, iy, ix + 2, iy + 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy + 2][ix + 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix + 2, iy + 2, ix, iy + 2)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                # обходим противника вправо вверх влево
                if field[iy - 2][ix] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy - 2][ix - 1] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy][ix + 2] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix + 2, iy, ix + 2, iy - 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy - 2][ix + 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix + 2, iy - 2, ix, iy - 2)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # сверху
            if iy == 1 and kub1 > 0:
                # квадрат сверху у базы. на базе враг
                if field[iy - 1][ix] == 1:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 1)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy][ix - 1] == 2 and ix == 1:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 1, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy][ix + 2] == 2 and ix == 7:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # ограждение противника сверху
                elif field[iy - 1][ix - 2] == 1 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # ограждение противника сверху
                elif field[iy - 1][ix + 2] == 1 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (field[iy + 2][ix] == 9 or field[iy + 2][ix] == 11) and mode == 3:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                    else:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                # обходим противника вниз право вверх
                if field[iy][ix + 2] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy - 1][ix + 2] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy + 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy + 2][ix] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy + 2, ix + 2, iy + 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy + 2][ix + 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix + 2, iy + 2, ix + 2, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                # обходим противника вниз влево вверх
                if field[iy][ix - 2] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy - 1][ix - 2] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy + 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy + 2][ix] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy + 2, ix - 2, iy + 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy + 2][ix - 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix - 2, iy + 2, ix - 2, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # справа
            if ix == 7 and kub1 > 0:
                # квадрат справа у базы. на базе враг
                if field[iy][ix + 2] == 2:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy + 2][ix] == 1 and iy == 7:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy + 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy - 1][ix] == 1 and iy == 1:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 1)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # ограждение противника справа
                elif field[iy + 2][ix + 2] == 2 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy + 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy - 2][ix + 2] == 2 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (field[iy][ix - 2] == 9 or field[iy][ix - 2] == 11) and mode == 3:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy - 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                    else:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy + 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                # обходим противника влево вниз вправо
                if field[iy + 2][ix] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy + 2][ix + 2] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix - 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy][ix - 2] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix - 2, iy, ix - 2, iy + 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy + 2][ix - 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix - 2, iy + 2, ix, iy + 2)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                # обходим противника влево вверх вправо
                if field[iy - 2][ix] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy - 2][ix + 2] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix - 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy][ix - 2] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix - 2, iy, ix - 2, iy - 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy - 2][ix - 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix - 2, iy - 2, ix, iy - 2)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # снизу
            if iy == 7 and kub1 > 0:  # квадрат снизу у базы. на базе враг
                if field[iy + 2][ix] == 1:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix, iy + 2)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy][ix + 2] == 2 and ix == 7:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy][ix - 1] == 2 and ix == 1:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 1, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # ограждение противника снизу
                elif field[iy + 2][ix + 2] == 1 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix + 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                elif field[iy + 2][ix - 2] == 1 and (mode == 2 or mode == 3):
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (field[iy - 2][ix] == 9 or field[iy - 2][ix] == 11) and mode == 3:
                    copy_pole1 = copy.deepcopy(field)
                    motion(ix, iy, ix - 2, iy)
                    if copy_pole1 != field:
                        kub1 = kub1 - 1
                    else:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix + 2, iy)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                # обходим противника вверх вправо вниз
                if field[iy][ix + 2] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy + 2][ix + 2] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy - 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy - 2][ix] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy - 2, ix + 2, iy - 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy - 2][ix + 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix + 2, iy - 2, ix + 2, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
                # обходим противника вверх влево вниз
                if field[iy][ix - 2] == spisok_kvdr and mode == 3 and kub1 > 0:
                    if field[iy + 2][ix - 2] == 0:
                        copy_pole1 = copy.deepcopy(field)
                        motion(ix, iy, ix, iy - 2)
                        if copy_pole1 != field:
                            kub1 = kub1 - 1
                            if kub1 > 0 and field[iy - 2][ix] in list_of_squares:
                                copy_pole1 = copy.deepcopy(field)
                                motion(ix, iy - 2, ix - 2, iy - 2)
                                if copy_pole1 != field:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and field[iy - 2][ix - 2] in list_of_squares:
                                        copy_pole1 = copy.deepcopy(field)
                                        motion(ix - 2, iy - 2, ix - 2, iy)
                                        if copy_pole1 != field:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # когда нет вышеупомянутых ходов, есть ходы и фишка на том же месте
            if 0 < ix + h1[1] < 9 and 0 < iy + h1[0] < 9 and kub1 > 0:
                copy_pole1 = copy.deepcopy(field)
                motion(ix, iy, ix + h1[1], iy + h1[0])
                if copy_pole1 != field:
                    kub1 = kub1 - 1

    time.sleep(0.01)
    board.update()
    par_motion = 1
    determinant(par_motion)


# определение какая фишка среди горизонтальных
def hor_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y):
    if 0 < poz1_y < 9 and field[poz1_y][poz1_x] == field[poz1_y + 1][poz1_x] and (
            poz1_y == 1 or poz1_y == 3 or poz1_y == 5 or poz1_y == 7):
        # проверка, что фишка не на базе, рядом есть ещё одна фишка и позиция нечетная
        chips_together(poz1_x, poz1_y, poz2_x, poz2_y)
    else:
        hor_rules(poz1_x, poz1_y, poz2_x, poz2_y)


# правила хода горизонтальных одиночных фишек
def hor_rules(poz1_x, poz1_y, poz2_x, poz2_y):
    g_par_gor = 0
    g_par_gor2 = 0
    g_par_vert = 0
    g_par_vert2 = 0
    g_par_kv1 = 0
    g_par_kv12 = 0
    g_ugol1 = 0
    g_ugol2 = 0
    g_svoi = 0
    g_svoi2 = 0
    g_kvad = 0
    even_list = [2, 4, 6, 8]
    if par_motion:
        g_par_gor = 3
        g_par_gor2 = 6
        g_par_vert = 4
        g_par_vert2 = 8
        g_par_kv1 = 9
        g_par_kv12 = 10
        g_ugol1 = 2
        g_ugol2 = 7
        g_svoi = 1
        g_svoi2 = 5
        g_kvad = 13
    if par_motion == 0 or par_motion == 2:
        g_par_gor = 1
        g_par_gor2 = 5
        g_par_vert = 2
        g_par_vert2 = 7
        g_par_kv1 = 13
        g_par_kv12 = 14
        g_ugol1 = 4
        g_ugol2 = 8
        g_svoi = 3
        g_svoi2 = 6
        g_kvad = 9
    # ПРОВЕРКА ХОДА ВНИЗ
    if (poz2_y == poz1_y + 1 and poz2_x == poz1_x) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x + 1):
        if poz1_y + 1 == 9:  # выброс врага с базы
            if field[poz1_y + 1][poz1_x] == g_par_gor and field[poz1_y + 1][poz1_x + 1] == g_par_gor2:
                field[poz1_y + 1][poz1_x] = 0
                field[poz1_y + 1][poz1_x + 1] = 0
            elif field[poz1_y + 1][poz1_x] == 0 and field[poz1_y + 1][poz1_x + 1] == 0:
                field[poz1_y + 1][poz1_x] = field[poz1_y][poz1_x]
                field[poz1_y + 1][poz1_x + 1] = field[poz1_y][poz1_x + 1]
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
        else:  # остальные случаи
            if poz1_y + 1 != 9:
                # проверка пустых клеток снизу
                if field[poz1_y + 2][poz1_x] == field[poz1_y + 2][poz1_x + 1] == 0 or field[poz1_y + 1][poz1_x] == \
                        field[poz1_y + 1][poz1_x + 1] == 0:
                    # фикс для компа если снизу своя фишка
                    if field[poz1_y + 1][poz1_x] == g_svoi and field[poz1_y + 1][poz1_x + 1] == g_svoi2:
                        pass
                    # проверка, что нет вертикальных чужих
                    elif field[poz1_y + 1][poz1_x] != g_par_vert and field[poz1_y + 1][poz1_x + 1] != g_par_vert:
                        # проверка что нет вертикальных своих
                        if field[poz1_y + 1][poz1_x] != g_ugol1 and field[poz1_y + 1][poz1_x + 1] != g_ugol1:
                            # смещение фигур врага рядом
                            if field[poz2_y][poz2_x] == g_par_gor or field[poz2_y][poz2_x] == g_par_gor2:
                                if field[poz2_y][poz2_x] == g_par_gor2:  # смещение значения
                                    poz2_x -= 1
                                field[poz2_y + 1][poz2_x] = field[poz2_y][poz2_x]
                                field[poz2_y + 1][poz2_x + 1] = field[poz2_y][poz2_x + 1]
                            field[poz1_y + 1][poz1_x] = field[poz1_y][poz1_x]
                            field[poz1_y + 1][poz1_x + 1] = field[poz1_y][poz1_x + 1]
                            field[poz1_y][poz1_x] = 0
                            field[poz1_y][poz1_x + 1] = 0
                            # если рядом фигура на четном месте, то соединение фигур
                            if field[poz1_y + 1][poz1_x] == field[poz1_y + 2][poz1_x] and (
                                    poz1_y + 1 == 1 or poz1_y + 1 == 3 or poz1_y + 1 == 5 or poz1_y + 1 == 7):
                                field[poz1_y + 1][poz1_x] = g_par_kv1
                                field[poz1_y + 1][poz1_x + 1] = g_par_kv12
                                field[poz1_y + 2][poz1_x] = g_par_kv1
                                field[poz1_y + 2][poz1_x + 1] = g_par_kv12
    # ПРОВЕРКА ХОДА ВВЕРХ
    elif (poz2_y == poz1_y - 1 and poz2_x == poz1_x) or (poz2_y == poz1_y - 1 and poz2_x == poz1_x + 1):
        if poz1_y - 1 == 0:  # выброс врага с базы
            if field[poz1_y - 1][poz1_x] == g_par_gor and field[poz1_y - 1][poz1_x + 1] == g_par_gor2:
                field[poz1_y - 1][poz1_x] = 0
                field[poz1_y - 1][poz1_x + 1] = 0
            elif field[poz1_y - 1][poz1_x] == 0 and field[poz1_y - 1][poz1_x + 1] == 0:
                field[poz1_y - 1][poz1_x] = field[poz1_y][poz1_x]
                field[poz1_y - 1][poz1_x + 1] = field[poz1_y][poz1_x + 1]
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
        else:  # остальные случаи
            if field[poz1_y - 2][poz1_x] == field[poz1_y - 2][poz1_x + 1] == 0 or \
                    field[poz1_y - 1][poz1_x] == field[poz1_y - 1][poz1_x + 1] == 0:  # проверка пустых клеток сверху
                # фикс для компа если сверху своя фишка
                if field[poz1_y - 1][poz1_x] == g_svoi and field[poz1_y - 1][poz1_x + 1] == g_svoi2:
                    pass
                # проверка, что нет вертикальных чужих
                elif field[poz1_y - 1][poz1_x] != g_par_vert2 and field[poz1_y - 1][poz1_x + 1] != g_par_vert2:
                    # проверка что нет вертикальных своих
                    if field[poz1_y - 1][poz1_x] != g_ugol2 and field[poz1_y - 1][poz1_x + 1] != g_ugol2:
                        # смещение фигур врага рядом
                        if field[poz2_y][poz2_x] == g_par_gor or field[poz2_y][poz2_x] == g_par_gor2:
                            if field[poz2_y][poz2_x] == g_par_gor2:
                                poz2_x -= 1
                            field[poz2_y - 1][poz2_x] = field[poz2_y][poz2_x]
                            field[poz2_y - 1][poz2_x + 1] = field[poz2_y][poz2_x + 1]
                        field[poz1_y - 1][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y - 1][poz1_x + 1] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
                        # если рядом фигура на нечетном месте, то соединение фигур
                        if field[poz1_y - 1][poz1_x] == field[poz1_y - 2][poz1_x] and (
                                poz1_y - 1 == 2 or poz1_y - 1 == 4 or poz1_y - 1 == 6 or poz1_y - 1 == 8):
                            field[poz1_y - 1][poz1_x] = g_par_kv1
                            field[poz1_y - 1][poz1_x + 1] = g_par_kv12
                            field[poz1_y - 2][poz1_x] = g_par_kv1
                            field[poz1_y - 2][poz1_x + 1] = g_par_kv12
    # ПРОВЕРКА ХОДА ВЛЕВО
    elif (poz2_y == poz1_y and poz2_x == poz1_x - 1) or (poz2_y == poz1_y and poz2_x == poz1_x - 2):
        if poz1_x - 2 != 0 and poz1_x - 1 != 0:  # фикс выхода на базу вертикальную
            # проверка пустых клеток слева
            if field[poz1_y][poz1_x - 2] == 0 and field[poz1_y][poz1_x - 1] == 0:
                field[poz1_y][poz1_x - 2] = field[poz1_y][poz1_x]
                field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x + 1]
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if field[poz1_y][poz1_x - 2] == field[poz1_y + 1][poz1_x - 2] and (
                            poz1_y == 1 or poz1_y == 3 or poz1_y == 5 or poz1_y == 7):
                        field[poz1_y][poz1_x - 2] = g_par_kv1
                        field[poz1_y][poz1_x - 1] = g_par_kv12
                        field[poz1_y + 1][poz1_x - 2] = g_par_kv1
                        field[poz1_y + 1][poz1_x - 1] = g_par_kv12
                    elif field[poz1_y][poz1_x - 2] == field[poz1_y - 1][poz1_x - 2] and (
                            poz1_y == 2 or poz1_y == 4 or poz1_y == 6 or poz1_y == 8):
                        field[poz1_y][poz1_x - 2] = g_par_kv1
                        field[poz1_y][poz1_x - 1] = g_par_kv12
                        field[poz1_y - 1][poz1_x - 2] = g_par_kv1
                        field[poz1_y - 1][poz1_x - 1] = g_par_kv12
            # если слева квадрат противника и стоим не впритык
            elif field[poz1_y][poz1_x - 2] == g_kvad and poz1_x != 3:
                # если слева есть место для выталкивания
                if field[poz1_y][poz1_x - 3] == 0 and field[poz1_y][poz1_x - 4] == 0:
                    if field[poz1_y + 1][poz1_x - 2] == g_kvad and poz1_y not in even_list: # если остальная часть снизу
                        field[poz1_y][poz1_x - 4] = g_par_gor
                        field[poz1_y][poz1_x - 3] = g_par_gor2
                        field[poz1_y + 1][poz1_x - 2] = g_par_gor
                        field[poz1_y + 1][poz1_x - 1] = g_par_gor2
                        field[poz1_y][poz1_x - 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
                    elif field[poz1_y - 1][poz1_x - 2] == g_kvad and poz1_y in even_list: # если остальная часть сверху
                        field[poz1_y][poz1_x - 4] = g_par_gor
                        field[poz1_y][poz1_x - 3] = g_par_gor2
                        field[poz1_y - 1][poz1_x - 2] = g_par_gor
                        field[poz1_y - 1][poz1_x - 1] = g_par_gor2
                        field[poz1_y][poz1_x - 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
            # если слева квадрат противника и стоим впритык к базе
            elif field[poz1_y][poz1_x - 2] == g_kvad and poz1_x == 3:
                if field[poz1_y][poz1_x - 3] == 0:
                    if field[poz1_y + 1][poz1_x - 2] == g_kvad and poz1_y not in even_list:
                        field[poz1_y + 1][poz1_x - 2] = g_par_gor
                        field[poz1_y + 1][poz1_x - 1] = g_par_gor2
                        field[poz1_y][poz1_x - 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
                    elif field[poz1_y - 1][poz1_x - 2] == g_kvad and poz1_y in even_list:
                        field[poz1_y - 1][poz1_x - 2] = g_par_gor
                        field[poz1_y - 1][poz1_x - 1] = g_par_gor2
                        field[poz1_y][poz1_x - 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 9 and field[8][0] == 0 and field[7][0] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            field[7][0] = g_ugol1
            field[8][0] = g_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 0 and field[1][0] == 0 and field[2][0] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            field[1][0] = g_ugol1
            field[2][0] = g_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y][poz1_x + 1] = 0
    # ПРОВЕРКА ХОДА ВПРАВО
    elif (poz2_y == poz1_y and poz2_x == poz1_x + 2) or (poz2_y == poz1_y and poz2_x == poz1_x + 3):
        if poz1_x + 2 != 9 and poz1_x + 1 != 9:
            if field[poz1_y][poz1_x + 2] == 0 and field[poz1_y][poz1_x + 3] == 0:
                field[poz1_y][poz1_x + 2] = field[poz1_y][poz1_x]
                field[poz1_y][poz1_x + 3] = field[poz1_y][poz1_x + 1]
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if field[poz1_y][poz1_x + 2] == field[poz1_y + 1][poz1_x + 2] and (
                            poz1_y == 1 or poz1_y == 3 or poz1_y == 5 or poz1_y == 7):
                        field[poz1_y][poz1_x + 2] = g_par_kv1
                        field[poz1_y][poz1_x + 3] = g_par_kv12
                        field[poz1_y + 1][poz1_x + 2] = g_par_kv1
                        field[poz1_y + 1][poz1_x + 3] = g_par_kv12
                    elif field[poz1_y][poz1_x + 2] == field[poz1_y - 1][poz1_x + 2] and (
                            poz1_y == 2 or poz1_y == 4 or poz1_y == 6 or poz1_y == 8):
                        field[poz1_y][poz1_x + 2] = g_par_kv1
                        field[poz1_y][poz1_x + 3] = g_par_kv12
                        field[poz1_y - 1][poz1_x + 2] = g_par_kv1
                        field[poz1_y - 1][poz1_x + 3] = g_par_kv12
            # если справа квадрат противника и стоим не впритык
            elif field[poz1_y][poz1_x + 2] == g_kvad and poz1_x != 5:
                # если слева есть место для выталкивания
                if field[poz1_y][poz1_x + 4] == 0 and field[poz1_y][poz1_x + 5] == 0:
                    if field[poz1_y + 1][poz1_x + 2] == g_kvad and poz1_y not in even_list: # если остальная часть снизу
                        field[poz1_y][poz1_x + 4] = g_par_gor
                        field[poz1_y][poz1_x + 5] = g_par_gor2
                        field[poz1_y + 1][poz1_x + 2] = g_par_gor
                        field[poz1_y + 1][poz1_x + 3] = g_par_gor2
                        field[poz1_y][poz1_x + 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x + 3] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
                    elif field[poz1_y - 1][poz1_x + 2] == g_kvad and poz1_y in even_list:  # если остальная часть сверху
                        field[poz1_y][poz1_x + 4] = g_par_gor
                        field[poz1_y][poz1_x + 5] = g_par_gor2
                        field[poz1_y - 1][poz1_x + 2] = g_par_gor
                        field[poz1_y - 1][poz1_x + 3] = g_par_gor2
                        field[poz1_y][poz1_x + 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x + 3] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
            elif field[poz1_y][poz1_x + 2] == g_kvad and poz1_x == 5:  # если справа квадрат противника и стоим впритык
                if field[poz1_y][poz1_x + 4] == 0:
                    if field[poz1_y + 1][poz1_x + 2] == g_kvad and poz1_y not in even_list:
                        field[poz1_y + 1][poz1_x + 2] = g_par_gor
                        field[poz1_y + 1][poz1_x + 3] = g_par_gor2
                        field[poz1_y][poz1_x + 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x + 3] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
                    elif field[poz1_y - 1][poz1_x + 2] == g_kvad and poz1_y in even_list:
                        field[poz1_y - 1][poz1_x + 2] = g_par_gor
                        field[poz1_y - 1][poz1_x + 3] = g_par_gor2
                        field[poz1_y][poz1_x + 2] = field[poz1_y][poz1_x]
                        field[poz1_y][poz1_x + 3] = field[poz1_y][poz1_x + 1]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 9 and field[8][9] == 0 and field[7][9] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            field[7][9] = g_ugol1
            field[8][9] = g_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 0 and field[1][9] == 0 and field[2][9] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            field[1][9] = g_ugol1
            field[2][9] = g_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y][poz1_x + 1] = 0


# определение какая фишка среди вертикальных
def vert_rules_distribution(poz1_x, poz1_y, poz2_x, poz2_y):
    if 0 < poz1_x < 9 and field[poz1_y][poz1_x] == field[poz1_y][poz1_x + 1] and (
            poz1_x == 1 or poz1_x == 3 or poz1_x == 5 or poz1_x == 7):
        chips_together(poz1_x, poz1_y, poz2_x, poz2_y)
    else:
        vert_rules(poz1_x, poz1_y, poz2_x, poz2_y)


# правила хода вертикальных одиночных фишек
def vert_rules(poz1_x, poz1_y, poz2_x, poz2_y):
    v_par_gor = 0
    v_par_gor2 = 0
    v_par_vert = 0
    v_par_vert2 = 0
    v_par_kv2 = 0
    v_par_kv22 = 0
    v_ugol1 = 0
    v_ugol2 = 0
    v_svoi = 0
    v_svoi2 = 0
    v_kvad = 0
    even_list = [2, 4, 6, 8]
    if par_motion:
        v_par_gor = 3
        v_par_gor2 = 6
        v_par_vert = 4
        v_par_vert2 = 8
        v_par_kv2 = 11
        v_par_kv22 = 12
        v_ugol1 = 1
        v_ugol2 = 5
        v_svoi = 2
        v_svoi2 = 7
        v_kvad = 15
    if par_motion == 0 or par_motion == 2:
        v_par_gor = 1
        v_par_gor2 = 5
        v_par_vert = 2
        v_par_vert2 = 7
        v_par_kv2 = 15
        v_par_kv22 = 16
        v_ugol1 = 3
        v_ugol2 = 6
        v_svoi = 4
        v_svoi2 = 8
        v_kvad = 11
    # ПРОВЕРКА ХОДА ВПРАВО
    if (poz2_y == poz1_y and poz2_x == poz1_x + 1) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x + 1):
        if poz1_x + 1 == 9:  # выброс врага с базы
            if field[poz1_y][poz1_x + 1] == v_par_vert and field[poz1_y + 1][poz1_x + 1] == v_par_vert2:
                field[poz1_y][poz1_x + 1] = 0
                field[poz1_y + 1][poz1_x + 1] = 0
            elif field[poz1_y][poz1_x + 1] == 0 and field[poz1_y + 1][poz1_x + 1] == 0:
                field[poz1_y][poz1_x + 1] = field[poz1_y][poz1_x]
                field[poz1_y + 1][poz1_x + 1] = field[poz1_y + 1][poz1_x]
                field[poz1_y][poz1_x] = 0
                field[poz1_y + 1][poz1_x] = 0
        else:  # остальные случаи
            if poz1_x + 1 != 9:
                # проверка пустых клеток справа
                if field[poz1_y][poz1_x + 2] == field[poz1_y + 1][poz1_x + 2] == 0 or \
                        field[poz1_y][poz1_x + 1] == field[poz1_y + 1][poz1_x + 1] == 0:
                    # фикс для компа если справа своя фишка
                    if field[poz1_y][poz1_x + 1] == v_svoi and field[poz1_y + 1][poz1_x + 1] == v_svoi2:
                        pass
                    # если справа горизонтальная фишка, то ничего не происходит
                    elif field[poz1_y][poz1_x + 1] != v_par_gor and field[poz1_y + 1][poz1_x + 1] != v_par_gor:
                        if field[poz1_y][poz1_x + 1] != v_ugol1 and field[poz1_y + 1][poz1_x + 1] != v_ugol1:
                            # смещение фигур врага рядом
                            if field[poz2_y][poz2_x] == v_par_vert or field[poz2_y][poz2_x] == v_par_vert2:
                                if field[poz2_y][poz2_x] == v_par_vert2:
                                    poz2_y -= 1
                                field[poz2_y][poz2_x + 1] = field[poz2_y][poz2_x]
                                field[poz2_y + 1][poz2_x + 1] = field[poz2_y + 1][poz2_x]
                            field[poz1_y][poz1_x + 1] = field[poz1_y][poz1_x]
                            field[poz1_y + 1][poz1_x + 1] = field[poz1_y + 1][poz1_x]
                            field[poz1_y][poz1_x] = 0
                            field[poz1_y + 1][poz1_x] = 0
                            # если рядом фигура на нечетном месте, то соединение фигур
                            if field[poz1_y][poz1_x + 1] == field[poz1_y][poz1_x + 2] and (
                                    poz1_x + 1 == 1 or poz1_x + 1 == 3 or poz1_x + 1 == 5 or poz1_x + 1 == 7):
                                field[poz1_y][poz1_x + 1] = v_par_kv2
                                field[poz1_y + 1][poz1_x + 1] = v_par_kv22
                                field[poz1_y][poz1_x + 2] = v_par_kv2
                                field[poz1_y + 1][poz1_x + 2] = v_par_kv22

    # ПРОВЕРКА ВЛЕВО
    elif (poz2_y == poz1_y and poz2_x == poz1_x - 1) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x - 1):
        if poz1_x - 1 == 0:  # выброс врага с базы
            if field[poz1_y][poz1_x - 1] == v_par_vert and field[poz1_y + 1][poz1_x - 1] == v_par_vert2:
                field[poz1_y][poz1_x - 1] = 0
                field[poz1_y + 1][poz1_x - 1] = 0
            elif field[poz1_y][poz1_x - 1] == 0 and field[poz1_y + 1][poz1_x - 1] == 0:
                field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x]
                field[poz1_y + 1][poz1_x - 1] = field[poz1_y + 1][poz1_x]
                field[poz1_y][poz1_x] = 0
                field[poz1_y + 1][poz1_x] = 0
        else:  # остальные случаи
            if field[poz1_y][poz1_x - 2] == field[poz1_y + 1][poz1_x - 2] == 0 or \
                    field[poz1_y][poz1_x - 1] == field[poz1_y + 1][poz1_x - 1] == 0:  # проверка пустых клеток слева
                # фикс для компа если слева своя фишка
                if field[poz1_y][poz1_x - 1] == v_svoi and field[poz1_y + 1][poz1_x - 1] == v_svoi2:
                    pass
                # если слева горизонтальная фишка, то ничего не происходит
                elif field[poz1_y][poz1_x - 1] != v_par_gor2 and field[poz1_y + 1][poz1_x - 1] != v_par_gor2:
                    if field[poz1_y][poz1_x - 1] != v_ugol2 and field[poz1_y + 1][poz1_x - 1] != v_ugol2:
                        if field[poz2_y][poz2_x] == v_par_vert or field[poz2_y][poz2_x] == v_par_vert2:
                            if field[poz2_y][poz2_x] == v_par_vert2:
                                poz2_y -= 1
                            field[poz2_y][poz2_x - 1] = field[poz2_y][poz2_x]
                            field[poz2_y + 1][poz2_x - 1] = field[poz2_y + 1][poz2_x]
                        field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x]
                        field[poz1_y + 1][poz1_x - 1] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
                        # если рядом фигура на четном месте, то соединение фигур
                        if field[poz1_y][poz1_x - 1] == field[poz1_y][poz1_x - 2] and (
                                poz1_x - 1 == 2 or poz1_x - 1 == 4 or poz1_x - 1 == 6 or poz1_x - 1 == 8):
                            field[poz1_y][poz1_x - 1] = v_par_kv2
                            field[poz1_y + 1][poz1_x - 1] = v_par_kv22
                            field[poz1_y][poz1_x - 2] = v_par_kv2
                            field[poz1_y + 1][poz1_x - 2] = v_par_kv22

    # ПРОВЕРКА ХОДА ВВЕРХ
    elif (poz2_y == poz1_y - 1 and poz2_x == poz1_x) or (poz2_y == poz1_y - 2 and poz2_x == poz1_x):
        if poz1_y - 2 != 0 and poz1_y - 1 != 0:  #
            if field[poz1_y - 1][poz1_x] == 0 and field[poz1_y - 2][poz1_x] == 0:  # проверка пустых клеток сверху
                field[poz1_y - 2][poz1_x] = field[poz1_y][poz1_x]
                field[poz1_y - 1][poz1_x] = field[poz1_y + 1][poz1_x]
                field[poz1_y][poz1_x] = 0
                field[poz1_y + 1][poz1_x] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if field[poz1_y - 2][poz1_x] == field[poz1_y - 2][poz1_x - 1] and (
                            poz1_x == 2 or poz1_x == 4 or poz1_x == 6 or poz1_x == 8):
                        field[poz1_y - 2][poz1_x] = v_par_kv2
                        field[poz1_y - 1][poz1_x] = v_par_kv22
                        field[poz1_y - 2][poz1_x - 1] = v_par_kv2
                        field[poz1_y - 1][poz1_x - 1] = v_par_kv22
                    elif field[poz1_y - 2][poz1_x] == field[poz1_y - 2][poz1_x + 1] and (
                            poz1_x == 1 or poz1_x == 3 or poz1_x == 5 or poz1_x == 7):
                        field[poz1_y - 2][poz1_x] = v_par_kv2
                        field[poz1_y - 1][poz1_x] = v_par_kv22
                        field[poz1_y - 2][poz1_x + 1] = v_par_kv2
                        field[poz1_y - 1][poz1_x + 1] = v_par_kv22
            # если сверху квадрат противника и стоим не впритык
            elif field[poz1_y - 2][poz1_x] == v_kvad and poz1_y != 3:
                # если сверху есть место для выталкивания
                if field[poz1_y - 3][poz1_x] == 0 and field[poz1_y - 4][poz1_x] == 0:
                    if field[poz1_y - 2][poz1_x - 1] == v_kvad and poz1_x in even_list:  # если остальная часть слева
                        field[poz1_y - 4][poz1_x] = v_par_vert
                        field[poz1_y - 3][poz1_x] = v_par_vert2
                        field[poz1_y - 2][poz1_x - 1] = v_par_vert
                        field[poz1_y - 1][poz1_x - 1] = v_par_vert2
                        field[poz1_y - 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y - 1][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
                    # если остальная часть справа
                    elif field[poz1_y - 2][poz1_x + 1] == v_kvad and poz1_x not in even_list:
                        field[poz1_y - 4][poz1_x] = v_par_vert
                        field[poz1_y - 3][poz1_x] = v_par_vert2
                        field[poz1_y - 2][poz1_x + 1] = v_par_vert
                        field[poz1_y - 1][poz1_x + 1] = v_par_vert2
                        field[poz1_y - 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y - 1][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
            elif field[poz1_y - 2][poz1_x] == v_kvad and poz1_y == 3:  # если сверху квадрат противника и стоим впритык
                if field[poz1_y - 3][poz1_x] == 0:
                    if field[poz1_y - 2][poz1_x - 1] == v_kvad and poz1_x in even_list:
                        field[poz1_y - 2][poz1_x - 1] = v_par_vert
                        field[poz1_y - 1][poz1_x - 1] = v_par_vert2
                        field[poz1_y - 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y - 1][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
                    elif field[poz1_y - 2][poz1_x + 1] == v_kvad and poz1_x not in even_list:
                        field[poz1_y - 2][poz1_x + 1] = v_par_vert
                        field[poz1_y - 1][poz1_x + 1] = v_par_vert2
                        field[poz1_y - 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y - 1][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 9 and field[0][8] == 0 and field[0][7] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            field[0][7] = v_ugol1
            field[0][8] = v_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 0 and field[0][1] == 0 and field[0][2] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            field[0][1] = v_ugol1
            field[0][2] = v_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y + 1][poz1_x] = 0
    # ПРОВЕРКА ХОДА ВНИЗ
    elif (poz2_y == poz1_y + 2 and poz2_x == poz1_x) or (poz2_y == poz1_y + 3 and poz2_x == poz1_x):
        if poz1_y + 2 != 9 and poz1_y + 1 != 9:  #
            if field[poz1_y + 2][poz1_x] == 0 and field[poz1_y + 3][poz1_x] == 0:  # проверка пустых клеток снизу
                field[poz1_y + 2][poz1_x] = field[poz1_y][poz1_x]
                field[poz1_y + 3][poz1_x] = field[poz1_y + 1][poz1_x]
                field[poz1_y][poz1_x] = 0
                field[poz1_y + 1][poz1_x] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if field[poz1_y + 2][poz1_x] == field[poz1_y + 2][poz1_x - 1] and (
                            poz1_x == 2 or poz1_x == 4 or poz1_x == 6 or poz1_x == 8):
                        field[poz1_y + 2][poz1_x] = v_par_kv2
                        field[poz1_y + 3][poz1_x] = v_par_kv22
                        field[poz1_y + 2][poz1_x - 1] = v_par_kv2
                        field[poz1_y + 3][poz1_x - 1] = v_par_kv22
                    elif field[poz1_y + 2][poz1_x] == field[poz1_y + 2][poz1_x + 1] and (
                            poz1_x == 1 or poz1_x == 3 or poz1_x == 5 or poz1_x == 7):
                        field[poz1_y + 2][poz1_x] = v_par_kv2
                        field[poz1_y + 3][poz1_x] = v_par_kv22
                        field[poz1_y + 2][poz1_x + 1] = v_par_kv2
                        field[poz1_y + 3][poz1_x + 1] = v_par_kv22
            # если снизу квадрат противника и стоим не впритык
            elif field[poz1_y + 2][poz1_x] == v_kvad and poz1_y != 5:
                # если снизу есть место для выталкивания
                if field[poz1_y + 5][poz1_x] == field[poz1_y + 4][poz1_x] == 0:
                    if field[poz1_y + 2][poz1_x - 1] == v_kvad and poz1_x in even_list:  # если остальная часть слева
                        field[poz1_y + 4][poz1_x] = v_par_vert
                        field[poz1_y + 5][poz1_x] = v_par_vert2
                        field[poz1_y + 2][poz1_x - 1] = v_par_vert
                        field[poz1_y + 3][poz1_x - 1] = v_par_vert2
                        field[poz1_y + 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y + 3][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
                    # если остальная часть справа
                    elif field[poz1_y + 2][poz1_x + 1] == v_kvad and poz1_x not in even_list:
                        field[poz1_y + 4][poz1_x] = v_par_vert
                        field[poz1_y + 5][poz1_x] = v_par_vert2
                        field[poz1_y + 2][poz1_x + 1] = v_par_vert
                        field[poz1_y + 3][poz1_x + 1] = v_par_vert2
                        field[poz1_y + 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y + 3][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
            elif field[poz1_y + 2][poz1_x] == v_kvad and poz1_y == 5:  # если снизу квадрат противника и стоим впритык
                if field[poz1_y + 4][poz1_x] == 0:
                    if field[poz1_y + 2][poz1_x - 1] == v_kvad and poz1_x in even_list:
                        field[poz1_y + 2][poz1_x - 1] = v_par_vert
                        field[poz1_y + 3][poz1_x - 1] = v_par_vert2
                        field[poz1_y + 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y + 3][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
                    elif field[poz1_y + 2][poz1_x + 1] == v_kvad and poz1_x not in even_list:
                        field[poz1_y + 2][poz1_x + 1] = v_par_vert
                        field[poz1_y + 3][poz1_x + 1] = v_par_vert2
                        field[poz1_y + 2][poz1_x] = field[poz1_y][poz1_x]
                        field[poz1_y + 3][poz1_x] = field[poz1_y + 1][poz1_x]
                        field[poz1_y][poz1_x] = 0
                        field[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 9 and field[9][8] == 0 and field[9][7] == 0:
            field[9][7] = v_ugol1
            field[9][8] = v_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 0 and field[9][1] == 0 and field[9][2] == 0:
            field[9][1] = v_ugol1
            field[9][2] = v_ugol2
            field[poz1_y][poz1_x] = 0
            field[poz1_y + 1][poz1_x] = 0


# Функция для всех квадратов. Правила хода
def chips_together(poz1_x, poz1_y, poz2_x, poz2_y):
    a1 = 0  # параметр для событий
    par_gor = 0
    par_vert = 0
    par_kv1 = 0
    par_kv2 = 0
    if par_motion:  # если ход игрока
        par_gor = 3
        par_vert = 4
        par_kv1 = 13
        par_kv2 = 15
    if par_motion == 0 or par_motion == 2:  # если ход компьютера
        par_gor = 1
        par_vert = 2
        par_kv1 = 9
        par_kv2 = 11
    # ДВИЖЕНИЕ ВНИЗ down
    if ((poz2_y == poz1_y + 2 and poz2_x == poz1_x) or (poz2_y == poz1_y + 3 and poz2_x == poz1_x) or (
            poz2_y == poz1_y + 2 and poz2_x == poz1_x + 1) or (poz2_y == poz1_y + 3 and poz2_x == poz1_x + 1)):
        if poz1_y != 7:  # проверка выхода квадрата на базу +
            # если снизу горизонтальная фишка внизу квадрата
            if field[poz1_y + 3][poz1_x] == par_gor and field[poz1_y + 2][poz1_x] == 0:
                if field[poz1_y + 4][poz1_x] == field[poz1_y + 4][poz1_x + 1] == 0:  # проверка места для сдвига
                    field[poz1_y + 4][poz1_x] = field[poz1_y + 3][poz1_x]
                    field[poz1_y + 4][poz1_x + 1] = field[poz1_y + 3][poz1_x + 1]
                    a1 = 1
            # если снизу горизонтальная фишка сверху квадрата
            elif field[poz1_y + 2][poz1_x] == par_gor and field[poz1_y + 3][poz1_x] == 0:
                if field[poz1_y + 4][poz1_x] == field[poz1_y + 4][poz1_x + 1] == 0:  # проверка места для сдвига
                    field[poz1_y + 4][poz1_x] = field[poz1_y + 2][poz1_x]
                    field[poz1_y + 4][poz1_x + 1] = field[poz1_y + 2][poz1_x + 1]
                    a1 = 1
            # если снизу вертикальная фишка слева в квадрате
            elif field[poz1_y + 2][poz1_x] == par_vert and field[poz1_y + 2][poz1_x + 1] == 0:
                if poz1_y + 4 != 9:
                    if field[poz1_y + 4][poz1_x] == 0 and field[poz1_y + 5][poz1_x] == 0:
                        field[poz1_y + 4][poz1_x] = field[poz1_y + 2][poz1_x]
                        field[poz1_y + 5][poz1_x] = field[poz1_y + 3][poz1_x]
                        a1 = 1
                else:
                    if field[poz1_y + 4][poz1_x] == field[poz1_y + 4][poz1_x + 1]:
                        a1 = 1
            # если снизу вертикальная фишка справа в квадрате
            elif field[poz1_y + 2][poz1_x + 1] == par_vert and field[poz1_y + 2][poz1_x] == 0:
                if poz1_y + 4 != 9:
                    if field[poz1_y + 4][poz1_x + 1] == 0 and field[poz1_y + 5][poz1_x + 1] == 0:
                        field[poz1_y + 4][poz1_x + 1] = field[poz1_y + 2][poz1_x + 1]
                        field[poz1_y + 5][poz1_x + 1] = field[poz1_y + 3][poz1_x + 1]
                        a1 = 1
                else:
                    if field[poz1_y + 4][poz1_x] == field[poz1_y + 4][poz1_x + 1]:
                        a1 = 1
            # если снизу квадрат противника 13 14 15 16
            elif field[poz1_y + 2][poz1_x] == par_kv1 or field[poz1_y + 2][poz1_x] == par_kv2:
                if poz1_y + 4 != 9:
                    if field[poz1_y + 4][poz1_x] == field[poz1_y + 4][poz1_x + 1] == field[poz1_y + 5][poz1_x]:
                        field[poz1_y + 4][poz1_x] = field[poz1_y + 2][poz1_x]
                        field[poz1_y + 4][poz1_x + 1] = field[poz1_y + 2][poz1_x + 1]
                        field[poz1_y + 5][poz1_x] = field[poz1_y + 3][poz1_x]
                        field[poz1_y + 5][poz1_x + 1] = field[poz1_y + 3][poz1_x + 1]
                        a1 = 1
                else:
                    if field[poz1_y + 4][poz1_x] == field[poz1_y + 4][poz1_x + 1]:
                        a1 = 1
            # проверка пустых клеток снизу
            elif field[poz1_y + 3][poz1_x] == field[poz1_y + 2][poz1_x] == 0:
                if field[poz1_y + 3][poz1_x + 1] == field[poz1_y + 2][poz1_x + 1] == 0:
                    a1 = 1
            if a1 == 1:  # если хотя бы одно произошло событие сверху, то происходит ход.
                field[poz1_y + 2][poz1_x] = field[poz1_y][poz1_x]
                field[poz1_y + 2][poz1_x + 1] = field[poz1_y][poz1_x + 1]
                field[poz1_y + 3][poz1_x] = field[poz1_y + 1][poz1_x]
                field[poz1_y + 3][poz1_x + 1] = field[poz1_y + 1][poz1_x + 1]
                field[poz1_y + 1][poz1_x + 1] = 0
                field[poz1_y + 1][poz1_x] = 0
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if field[poz1_y + 2][poz1_x] == par_gor:  # field[poz1_y + 2][poz1_x+1] == 6
                field[poz1_y + 2][poz1_x] = 0
                field[poz1_y + 2][poz1_x + 1] = 0
    # ДВИЖЕНИЕ ВВЕРХ up
    elif ((poz2_y == poz1_y - 1 and poz2_x == poz1_x) or (poz2_y == poz1_y - 2 and poz2_x == poz1_x) or (
            poz2_y == poz1_y - 1 and poz2_x == poz1_x + 1) or (poz2_y == poz1_y - 2 and poz2_x == poz1_x + 1)):
        if poz1_y - 1 != 0:  # проверка выхода квадрата на базу
            # если сверху горизонтальная фишка внизу квадрата
            if field[poz1_y - 1][poz1_x] == par_gor and field[poz1_y - 2][poz1_x] == 0:
                if field[poz1_y - 3][poz1_x] == 0 and field[poz1_y - 3][poz1_x + 1] == 0:
                    field[poz1_y - 3][poz1_x] = field[poz1_y - 1][poz1_x]
                    field[poz1_y - 3][poz1_x + 1] = field[poz1_y - 1][poz1_x + 1]
                    a1 = 1
            # если сверху горизонтальная фишка сверху квадрата
            elif field[poz1_y - 2][poz1_x] == par_gor and field[poz1_y - 1][poz1_x] == 0:
                if field[poz1_y - 3][poz1_x] == 0 and field[poz1_y - 3][poz1_x + 1] == 0:
                    field[poz1_y - 3][poz1_x] = field[poz1_y - 2][poz1_x]
                    field[poz1_y - 3][poz1_x + 1] = field[poz1_y - 2][poz1_x + 1]
                    a1 = 1
            # если сверху вертикальная фишка слева в квадрате
            elif field[poz1_y - 2][poz1_x] == par_vert and field[poz1_y - 2][poz1_x + 1] == 0:
                if poz1_y - 3 > 0:
                    if field[poz1_y - 3][poz1_x] == 0 and field[poz1_y - 4][poz1_x] == 0:
                        field[poz1_y - 3][poz1_x] = field[poz1_y - 1][poz1_x]
                        field[poz1_y - 4][poz1_x] = field[poz1_y - 2][poz1_x]
                        a1 = 1
                else:
                    if field[poz1_y - 3][poz1_x] == field[poz1_y - 3][poz1_x + 1]:
                        a1 = 1
            # если сверху вертикальная фишка справа в квадрате
            elif field[poz1_y - 2][poz1_x + 1] == par_vert and field[poz1_y - 2][poz1_x] == 0:
                if poz1_y - 3 > 0:
                    if field[poz1_y - 3][poz1_x + 1] == 0 and field[poz1_y - 4][poz1_x + 1] == 0:
                        field[poz1_y - 3][poz1_x + 1] = field[poz1_y - 1][poz1_x + 1]
                        field[poz1_y - 4][poz1_x + 1] = field[poz1_y - 2][poz1_x + 1]
                        a1 = 1
                else:
                    if field[poz1_y - 3][poz1_x] == field[poz1_y - 3][poz1_x + 1]:
                        a1 = 1
            # если сверху квадрат противника 13 14 15 16
            elif field[poz1_y - 2][poz1_x] == par_kv1 or field[poz1_y - 2][poz1_x] == par_kv2:
                if poz1_y - 3 > 0:
                    if field[poz1_y - 3][poz1_x] == field[poz1_y - 4][poz1_x] == field[poz1_y - 4][poz1_x + 1] == 0:
                        field[poz1_y - 4][poz1_x] = field[poz1_y - 2][poz1_x]
                        field[poz1_y - 4][poz1_x + 1] = field[poz1_y - 2][poz1_x + 1]
                        field[poz1_y - 3][poz1_x] = field[poz1_y - 1][poz1_x]
                        field[poz1_y - 3][poz1_x + 1] = field[poz1_y - 1][poz1_x + 1]
                        a1 = 1
                else:
                    if field[poz1_y - 3][poz1_x] == field[poz1_y - 3][poz1_x + 1]:
                        a1 = 1
            # проверка пустых клеток сверху
            elif field[poz1_y - 2][poz1_x] == field[poz1_y - 1][poz1_x] == 0:
                if field[poz1_y - 2][poz1_x + 1] == field[poz1_y - 1][poz1_x + 1] == 0:
                    a1 = 1
            if a1 == 1:  # если хоть одно произошло событие сверху, то происходит ход.
                field[poz1_y - 2][poz1_x] = field[poz1_y][poz1_x]
                field[poz1_y - 2][poz1_x + 1] = field[poz1_y][poz1_x + 1]
                field[poz1_y - 1][poz1_x] = field[poz1_y + 1][poz1_x]
                field[poz1_y - 1][poz1_x + 1] = field[poz1_y + 1][poz1_x + 1]
                field[poz1_y + 1][poz1_x + 1] = 0
                field[poz1_y + 1][poz1_x] = 0
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if field[poz1_y - 1][poz1_x] == par_gor:
                field[poz1_y - 1][poz1_x] = 0
                field[poz1_y - 1][poz1_x + 1] = 0
    # ДВИЖЕИЕ ВЛЕВО left
    elif ((poz2_y == poz1_y and poz2_x == poz1_x - 1) or (poz2_y == poz1_y and poz2_x == poz1_x - 2) or (
            poz2_y == poz1_y + 1 and poz2_x == poz1_x - 1) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x - 2)):
        if poz1_x != 1:  # заход на базу
            # если слева вертикальная фишка слева квадрата
            if field[poz1_y][poz1_x - 2] == par_vert and field[poz1_y][poz1_x - 1] == 0:
                if field[poz1_y][poz1_x - 3] == 0 and field[poz1_y + 1][poz1_x - 3] == 0:
                    field[poz1_y][poz1_x - 3] = field[poz1_y][poz1_x - 2]
                    field[poz1_y + 1][poz1_x - 3] = field[poz1_y + 1][poz1_x - 2]
                    a1 = 1
            # если слева вертикальная фишка справа квадрата
            elif field[poz1_y][poz1_x - 1] == par_vert and field[poz1_y][poz1_x - 2] == 0:
                if field[poz1_y][poz1_x - 3] == 0 and field[poz1_y + 1][poz1_x - 3] == 0:
                    field[poz1_y][poz1_x - 3] = field[poz1_y][poz1_x - 1]
                    field[poz1_y + 1][poz1_x - 3] = field[poz1_y + 1][poz1_x - 1]
                    a1 = 1
            # если слева горизонтальная фишка сверху в квадрате
            elif field[poz1_y][poz1_x - 2] == par_gor and field[poz1_y + 1][poz1_x - 2] == 0:
                if poz1_x - 3 > 0:  # fix
                    if field[poz1_y][poz1_x - 3] == 0 and field[poz1_y][poz1_x - 4] == 0:
                        field[poz1_y][poz1_x - 3] = field[poz1_y][poz1_x - 1]
                        field[poz1_y][poz1_x - 4] = field[poz1_y][poz1_x - 2]
                        a1 = 1
                else:
                    if field[poz1_y][poz1_x - 3] == field[poz1_y + 1][poz1_x - 3]:
                        a1 = 1
            # если слева горизонтальная фишка снизу в квадрате
            elif field[poz1_y + 1][poz1_x - 2] == par_gor and field[poz1_y][poz1_x - 2] == 0:
                if poz1_x - 3 > 0:
                    if field[poz1_y + 1][poz1_x - 3] == 0 and field[poz1_y + 1][poz1_x - 4] == 0:
                        field[poz1_y + 1][poz1_x - 3] = field[poz1_y + 1][poz1_x - 1]
                        field[poz1_y + 1][poz1_x - 4] = field[poz1_y + 1][poz1_x - 2]
                        a1 = 1
                else:
                    if field[poz1_y][poz1_x - 3] == field[poz1_y + 1][poz1_x - 3]:
                        a1 = 1
            # если слева квадрат противника 13 14 15 16
            elif field[poz1_y][poz1_x - 2] == par_kv1 or field[poz1_y][poz1_x - 2] == par_kv2:
                if poz1_x - 3 > 0:
                    if field[poz1_y][poz1_x - 3] == field[poz1_y][poz1_x - 4] == field[poz1_y + 1][poz1_x - 4] == 0:
                        field[poz1_y][poz1_x - 4] = field[poz1_y][poz1_x - 2]
                        field[poz1_y + 1][poz1_x - 4] = field[poz1_y + 1][poz1_x - 2]
                        field[poz1_y][poz1_x - 3] = field[poz1_y][poz1_x - 1]
                        field[poz1_y + 1][poz1_x - 3] = field[poz1_y + 1][poz1_x - 1]
                        a1 = 1
                else:
                    if field[poz1_y][poz1_x - 3] == field[poz1_y + 1][poz1_x - 3]:
                        a1 = 1
            # проверка пустых клеток слева
            elif field[poz1_y][poz1_x - 2] == field[poz1_y][poz1_x - 1] == 0:
                if field[poz1_y + 1][poz1_x - 2] == field[poz1_y + 1][poz1_x - 1] == 0:
                    a1 = 1
            if a1 == 1:  # если хоть одно произошло событие сверху, то происходит ход.
                field[poz1_y][poz1_x - 2] = field[poz1_y][poz1_x]
                field[poz1_y][poz1_x - 1] = field[poz1_y][poz1_x + 1]
                field[poz1_y + 1][poz1_x - 2] = field[poz1_y + 1][poz1_x]
                field[poz1_y + 1][poz1_x - 1] = field[poz1_y + 1][poz1_x + 1]
                field[poz1_y + 1][poz1_x + 1] = 0
                field[poz1_y + 1][poz1_x] = 0
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if field[poz1_y][poz1_x - 1] == par_vert:
                field[poz1_y][poz1_x - 1] = 0
                field[poz1_y + 1][poz1_x - 1] = 0
    # ДВИЖЕИЕ ВПРАВО right
    elif ((poz2_y == poz1_y and poz2_x == poz1_x + 2) or (poz2_y == poz1_y and poz2_x == poz1_x + 3) or (
            poz2_y == poz1_y + 1 and poz2_x == poz1_x + 2) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x + 3)):
        if poz1_x != 7:
            # если справа вертикальная фишка справа квадрата
            if field[poz1_y][poz1_x + 3] == par_vert and field[poz1_y][poz1_x + 2] == 0:
                if field[poz1_y][poz1_x + 4] == 0 and field[poz1_y + 1][poz1_x + 4] == 0:
                    field[poz1_y][poz1_x + 4] = field[poz1_y][poz1_x + 3]
                    field[poz1_y + 1][poz1_x + 4] = field[poz1_y + 1][poz1_x + 3]
                    a1 = 1
            # если справа вертикальная фишка слева квадрата
            elif field[poz1_y][poz1_x + 2] == par_vert and field[poz1_y][poz1_x + 3] == 0:
                if field[poz1_y][poz1_x + 4] == 0 and field[poz1_y + 1][poz1_x + 4] == 0:
                    field[poz1_y][poz1_x + 4] = field[poz1_y][poz1_x + 2]
                    field[poz1_y + 1][poz1_x + 4] = field[poz1_y + 1][poz1_x + 2]
                    a1 = 1
            # если справа горизонтальная фишка сверху в квадрате
            elif field[poz1_y][poz1_x + 2] == par_gor and field[poz1_y + 1][poz1_x + 2] == 0:
                if poz1_x + 4 != 9:  # чтобы исключения не выдавало
                    if field[poz1_y][poz1_x + 5] == 0 and field[poz1_y][poz1_x + 4] == 0:
                        field[poz1_y][poz1_x + 5] = field[poz1_y][poz1_x + 3]
                        field[poz1_y][poz1_x + 4] = field[poz1_y][poz1_x + 2]
                        a1 = 1
                else:
                    if field[poz1_y][poz1_x + 4] == field[poz1_y + 1][poz1_x + 4]:
                        a1 = 1
            # если справа горизонтальная фишка снизу в квадрате
            elif field[poz1_y + 1][poz1_x + 2] == par_gor and field[poz1_y][poz1_x + 2] == 0:
                if poz1_x + 4 != 9:  # чтобы исключения не выдавало
                    if field[poz1_y + 1][poz1_x + 5] == 0 and field[poz1_y + 1][poz1_x + 4] == 0:
                        field[poz1_y + 1][poz1_x + 5] = field[poz1_y + 1][poz1_x + 3]
                        field[poz1_y + 1][poz1_x + 4] = field[poz1_y + 1][poz1_x + 2]
                        a1 = 1
                else:
                    if field[poz1_y][poz1_x + 4] == field[poz1_y + 1][poz1_x + 4]:
                        a1 = 1
            # если справа квадрат противника 13 14 15 16
            elif field[poz1_y][poz1_x + 2] == par_kv1 or field[poz1_y][poz1_x + 2] == par_kv2:
                if poz1_x + 4 != 9:
                    if field[poz1_y][poz1_x + 5] == field[poz1_y + 1][poz1_x + 4] == 0 == field[poz1_y][poz1_x + 4]:
                        field[poz1_y][poz1_x + 4] = field[poz1_y][poz1_x + 2]
                        field[poz1_y + 1][poz1_x + 4] = field[poz1_y + 1][poz1_x + 2]
                        field[poz1_y][poz1_x + 5] = field[poz1_y][poz1_x + 3]
                        field[poz1_y + 1][poz1_x + 5] = field[poz1_y + 1][poz1_x + 3]
                        a1 = 1
                else:
                    if field[poz1_y][poz1_x + 4] == field[poz1_y + 1][poz1_x + 4]:
                        a1 = 1
            # проверка пустых клеток справа
            elif field[poz1_y][poz1_x + 2] == field[poz1_y][poz1_x + 3] == 0:
                if field[poz1_y + 1][poz1_x + 2] == field[poz1_y + 1][poz1_x + 3] == 0:
                    a1 = 1
            if a1 == 1:  # если хоть одно произошло событие сверху, то происходит ход.
                field[poz1_y][poz1_x + 2] = field[poz1_y][poz1_x]
                field[poz1_y][poz1_x + 3] = field[poz1_y][poz1_x + 1]
                field[poz1_y + 1][poz1_x + 2] = field[poz1_y + 1][poz1_x]
                field[poz1_y + 1][poz1_x + 3] = field[poz1_y + 1][poz1_x + 1]
                field[poz1_y + 1][poz1_x] = 0
                field[poz1_y + 1][poz1_x + 1] = 0
                field[poz1_y][poz1_x] = 0
                field[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if field[poz1_y][poz1_x + 2] == par_vert:
                field[poz1_y][poz1_x + 2] = 0
                field[poz1_y + 1][poz1_x + 2] = 0


# определяет параметры запуска
def clicked_start():
    global scale, res1
    global par_V
    global res
    if mode == 2:  # игра с игроком. par_motion 1 par_motion 2
        res = txt.get()
        res = int(res)
        res1 = '{}'.format(combo.get())
    elif mode == 1:  # игра с компьютером. par_motion 1 par_motion 0
        res = txt1
        res = int(res)
        res1 = combo1
    if 600 <= res <= 1000:
        scale = res
        if res1 == '0 - Медленный вариант':
            par_V = 0
        elif res1 == '1 - Стандартный вариант':
            par_V = 1
        elif res1 == '2 - Быстрый вариант':
            par_V = 2
        root.geometry(f'{int(1.8 * res)}x{int(res * 1.1)}')
        start()
    else:
        messagebox.showinfo('Оповещение', 'Введите значение от 600 до 1000')


# вывод второго окна при игре с компом
def pl_vs_comp():
    global btn1, txt1, combo1
    global selected
    if mode == 1:
        txt1 = txt.get()
        combo1 = '{}'.format(combo.get())
        # очищаем каждый объект отдельно
        lbl.destroy()
        lbl1.destroy()
        lbl2.destroy()
        lbl3.destroy()
        lbl4.destroy()
        lbl5.destroy()
        txt.destroy()
        btn.destroy()
        combo.destroy()
        rad_1.destroy()
        rad_2.destroy()

        selected = tkinter.IntVar()  # параметры для функции complexity
        rad1 = Radiobutton(root, text='Первый', value=1, variable=selected, command=complexity)  # light
        rad2 = Radiobutton(root, text='Второй', value=2, variable=selected, command=complexity)  # Medium
        rad3 = Radiobutton(root, text='Третий', value=3, variable=selected, command=complexity)  # Hard

        lbl_0 = tkinter.Label(root, text="                   \n\n", font=("Arial Bold", 20))
        lbl_01 = tkinter.Label(root, text="                   ", font=("Arial Bold", 5))
        lbl_02 = tkinter.Label(root, text="                   ", font=("Arial Bold", 10))
        lbl_1 = tkinter.Label(root, anchor=tkinter.CENTER, text="Укажи уровень сложности компьютера",
                              font=("Arial Bold", 20))
        btn1 = tkinter.Button(root, text="Готово", command=clicked_start, state=tkinter.DISABLED)  #
        lbl_0.grid(column=0, row=1)
        lbl_1.grid(column=1, row=1)
        lbl_01.grid(column=1, row=2)
        rad1.grid(column=1, row=3)
        rad2.grid(column=1, row=4)
        rad3.grid(column=1, row=5)
        lbl_02.grid(column=1, row=6)
        btn1.grid(column=1, row=7)
    else:
        clicked_start()


# определяет режим игры
def clicked_mode():
    global mode
    btn.configure(state=tkinter.NORMAL)
    mode = selected_1.get()


# определяет сложность компьютера
def complexity():
    global rad1
    btn1.configure(state=tkinter.NORMAL)
    rad1 = selected.get()


# создание окна
root = tkinter.Tk()
root.title("Добро пожаловать в приложение 'Yurki v(1.0)'")  # тайтл окна
root.geometry('800x500')  # размер окна

combo = Combobox(root, width=50, height=50, font=20, justify=tkinter.CENTER)  # панель выбора скорости игры
combo['values'] = ('0 - Медленный вариант', '1 - Стандартный вариант', '2 - Быстрый вариант')
combo.current(1)

txt = tkinter.Entry(root, width=20, justify=tkinter.CENTER, font=20)  # state='disabled' # панель выбора размера окна
txt.focus()
txt.insert(0, '700')

selected_1 = tkinter.IntVar()  # параметры выбора режима
rad_1 = tkinter.Radiobutton(root, text='Игрок vs Компьютер', value=1, variable=selected_1, command=clicked_mode)
rad_2 = tkinter.Radiobutton(root, text='Игрок vs Игрок', value=2, variable=selected_1, command=clicked_mode)
# распределение по сетке окна через функцию grid
lbl = tkinter.Label(root, text="      \n", font=("Arial Bold", 20))
lbl.grid(column=0, row=0)
lbl1 = tkinter.Label(root, text="Укажи удобный для тебя масштаб окна от 600 до 1000", font=("Arial Bold", 20))
lbl1.grid(column=1, row=1)
# вставляем панель выбора размера окна
txt.grid(column=1, row=2)
lbl2 = tkinter.Label(root, text="      \n", font=("Arial Bold", 5))
lbl2.grid(column=1, row=3)
lbl3 = tkinter.Label(root, text="Выбери скорость анимации фигур", font=("Arial Bold", 20))
lbl3.grid(column=1, row=4)
# вставляем панель выбора скорости игры
combo.grid(column=1, row=5)
lbl4 = tkinter.Label(root, text="      \n", font=("Arial Bold", 5))
lbl4.grid(column=1, row=7)
lbl5 = tkinter.Label(root, text="Выбери режим:", font=("Arial Bold", 20))
lbl5.grid(column=1, row=8)
# вставляем параметры выбора режима игры
rad_1.grid(column=1, row=9)
rad_2.grid(column=1, row=10)

lbl = tkinter.Label(root, text="      \n", font=("Arial Bold", 5))
lbl.grid(column=1, row=12)
btn = tkinter.Button(root, text="Готово", command=pl_vs_comp, state=tkinter.DISABLED)  #
btn.grid(column=1, row=13)

root.mainloop()  # Цикл отображения окна.
