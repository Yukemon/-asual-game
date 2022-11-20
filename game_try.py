import copy
import random
import time
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.ttk import Radiobutton


# функция вводных аргументов и создание окна игры
def nachalo():
    global doska  # Canvas
    global m_pr  # operator mashtaba
    global fon  # Canvas
    global kubiki  # параметр числа кубиков
    global poz1_x  # позиция мыши
    global poz1_y  # позиция мыши
    global f_hi  # параметр определения ходы
    global k_pole  # копия поля, для учета ходов компьютера

    # обозначение переменных
    m_pr = mashtab / 10  # для пропорции векторов
    poz1_x = -1  # для отладки
    poz1_y = - 1  # для отладки
    f_hi = 0  # параметр определение хода
    fon = Canvas(root, width=mashtab + 0.7 * mashtab, height=mashtab + 0.1 * mashtab, bg='grey')  # фон
    fon.place(x=mashtab / 20, y=mashtab / 20, anchor=NW)
    doska = Canvas(root, width=mashtab, height=mashtab)  # игровая зона
    doska.place(x=mashtab / 20, y=mashtab / 20, anchor=NW)

    novaya_igra()  # создаем поле...
    # Выводим игровое поле. Первые 4 переменные pozy, pozx, pozy2, pox2, последняя фикс для случая в анимации.
    vivod(-1, -1, -1, -1, 1)
    doska.bind("<Motion>", pozici_1)  # отслеживаем движение мышки по полю
    doska.bind("<Button-1>", pozici_2)  # нажатие левой кнопки
    # vibor() # сразу переход к выбору хода. Опционально включаем, выключаем мануал().
    manual()  # инструкция


# функция отрисовки позиций игрового поля
def novaya_igra():
    global pole
    # 0 = пустая клетка,
    # 1 и 5 гориз.фишка # 2 и 7 верт.фишка # 9 и 10 горизонт.квадрат # 11 и 12 верт.квадрат # игрок,
    # 3 и 6 гориз.фишка # 4 и 8   верт.фишка # 13 и 14 горизонт.квадрат # 15 и 16 верт.квадрат # компьютер
    # 17 - углы поворота

    pole = [[17, 1, 5, 3, 6, 1, 5, 3, 6, 17],
            [4,  0, 0, 0, 0, 0, 0, 0, 0, 2],
            [8,  0, 0, 0, 0, 0, 0, 0, 0, 7],
            [2,  0, 0, 0, 0, 0, 0, 0, 0, 4],
            [7,  0, 0, 0, 0, 0, 0, 0, 0, 8],
            [4,  0, 0, 0, 0, 0, 0, 0, 0, 2],
            [8,  0, 0, 0, 0, 0, 0, 0, 0, 7],
            [2,  0, 0, 0, 0, 0, 0, 0, 0, 4],
            [7,  0, 0, 0, 0, 0, 0, 0, 0, 8],
            [17, 3, 6, 1, 5, 3, 6, 1, 5, 17]]
    # копия, если изменил поле
    # pole = [[17, 1, 5, 3, 6, 1, 5, 3, 6, 17],
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
    z = 'Инструкция к игре'
    i4 = messagebox.askyesno(title=z, message='Хочешь узнать правила игры?', icon='info')
    if i4:
        doska.create_rectangle(m_pr - 10, m_pr - 10, 9 * m_pr + 10, 9 * m_pr + 10, fill='white', outline="black")

        doska.create_text(mashtab / 2, mashtab / 7, fill="darkblue", font=f"Times {int(m_pr / 3.5)} italic bold",
                          text="ИНСТРУКЦИЯ К ИГРЕ", anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 4.6), fill="darkblue", font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="Цель игры выбить все фишки противника \n              за пределы игровой зоны",
                          anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 3.6), fill="darkblue", font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="Твои фишки красные, фишки противника зеленые", anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 3.18), fill="darkblue",
                          font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="В игре существует две игровых зоны: База и Поле", anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 2.69), fill="darkblue",
                          font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="На базах расположено как у тебя, так и у противника \n        "
                               "4 горизонтальных и 4 вертикальных фишки ",
                          anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 2.25), fill="darkblue",
                          font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="В начале каждого хода бросается кубик,\n число означает кол-во доступных ходов",
                          anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 1.94), fill="darkblue",
                          font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="Чтобы выбить противника, необходимо \n            подвести его фишку на базу",
                          anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 1.7), fill="darkblue", font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="Выбивание возможно, если обе фишки \n стоят длинной стороной друг к другу",
                          anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 1.52), fill="darkblue",
                          font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="Чтобы развернуть фишку,необходимо \n            попасть в желтую зону",
                          anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 1.34), fill="darkblue",
                          font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="Если две союзных фишки стоят длинной стороной \n            "
                               "друг к другу  на Поле в области квадратов, \n                "
                               "то они образуют квадратную фишку",
                          anchor=CENTER)
        doska.create_text(mashtab / 2, int(mashtab / 1.2), fill="darkblue", font=f"Times {int(m_pr / 4.2)} italic bold",
                          text="      Квадратной фишкой можно выбивать\n фишки противника  в любых положениях",
                          anchor=CENTER)
        i = messagebox.showinfo('Инструкция', 'Нажми OK, когда дочитаешь')
        if i:
            vivod(-1, -1, -1, -1, 1)
            vibor()
        else:
            messagebox.askyesno(message='УВЫ И АХ', icon='info')
    else:
        vibor()


# диалоговое окно выбора хода
def vibor():
    global f_hi
    z = 'Добро пожаловать =)'
    if rad == 2:
        i = messagebox.askyesno(title=z, message='Игрок 1 ходит первым?', icon='info')
    else:
        i = messagebox.askyesno(title=z, message='Ты хочешь ходить первым?', icon='info')
    if i:
        f_hi = 1
    else:
        if rad == 2:
            f_hi = 2
        elif rad == 1:
            f_hi = 0
    opredel_hoda(f_hi)


# конец игры
def the_end():
    global end_p
    s_i = 0
    s_k = 0
    end_p = 0
    for i in range(10):
        for ii in pole[i]:
            if ii == 1 or ii == 2 or ii == 9 or ii == 11:
                s_i += 1
            if ii == 3 or ii == 4 or ii == 13 or ii == 15:
                s_k += 1
    if s_i == 0:
        end_p = 1
        soobsenie(2)
    if s_k == 0:
        end_p = 1
        soobsenie(1)



# окно о завершении игры
def soobsenie(s):
    z = 'Игра завершена'
    i = 0
    if s == 1:
        if rad == 2:
            i = messagebox.askyesno(title=z, message='Игрок 1 победил!\nНажми "Да" что бы начать заново.', icon='info')
        else:
            i = messagebox.askyesno(title=z, message='Вы победили!\nНажми "Да" что бы начать заново.', icon='info')
    if s == 2:
        if rad == 2:
            i = messagebox.askyesno(title=z, message='Игрок 2 победил!\nНажми "Да" что бы начать заново.', icon='info')
        else:
            i = messagebox.askyesno(title=z, message='Вы проиграли!\nНажми "Да" что бы начать заново.', icon='info')
    if s == 3:
        i = messagebox.askyesno(title=z, message='Вы победили! У компьютера не осталось ходов.\nНажми "Да" что бы начать заново.', icon='info')
    if i:
        novaya_igra()
        vivod(-1, -1, -1, -1, 1)
        vibor()  # ход игрока доступен
    else:
        try:
            root.destroy()
        except:
            print('До свидания!')


# функция отрисовки фигур, анимации
def vivod(x_poz_1, y_poz_1, x_poz_2, y_poz_2, w):
    # выброс фигур вниз и ваправо
    # разбитие квадрата рамка
    # анимация вправо квадраты нет выталкивание
    global pole  # на основе поля отрисовка
    global kr_ramka, zel_ramka  # делаем глобальными параметры рамки
    global par_V, b  # Определяем скорость анимации. И делаем глобальным параметр анимации(FIX)
    print(pole[0], pole[1], pole[2], pole[3], pole[4], pole[5], pole[6], pole[7], pole[8], pole[9], sep='\n')
    print(' ') # Пробел между выводом в RUN поля

    # переменные
    k = x = x_3 = m_pr  # параметры отрисовки поля равны маштаб/10
    x1 = x2 = x3 = 3 * m_pr  # для отрисовки поля
    x_2 = y_2 = y_3 = 0  # для отрисовки поля

    doska.delete('all')  # удаление прошлых ходов, чтобы не перегружать систему созданием новых объектов

    kr_ramka = doska.create_rectangle(-5, -5, -5, -5, outline='yellow', width=7)  # рамка при выборе
    zel_ramka = doska.create_rectangle(-5, -5, -5, -5, outline='blue', width=7)  # рамка при наведении

    while True:  # поле, создание внешнего вида
        if y_2 == 0:  # уголки сверху
            doska.create_polygon([0, m_pr - 1], [m_pr - 1, m_pr - 1], [m_pr - 1, 0], fill="yellow", outline="black")
            doska.create_polygon([m_pr * 9 + 1, 0], [m_pr * 9 + 1, m_pr - 1], [mashtab, m_pr - 1], fill="yellow",
                                 outline="black")
            y_2 += k
        elif y_2 >= mashtab / 10 * 9:  # уголки снизу
            doska.create_polygon([0, m_pr * 9 + 1], [m_pr - 1, m_pr * 9 + 1], [m_pr - 1, mashtab], fill="yellow",
                                 outline="black")
            doska.create_polygon([m_pr * 9 + 1, m_pr * 9 + 1], [m_pr * 9 + 1, mashtab], [mashtab, m_pr * 9 + 1],
                                 fill="yellow", outline="black")
            break
        else:  # базы для фишек
            doska.create_rectangle(x_2 + 10, y_2 + 10, x_2 + k - 10, y_2 + k * 2 - 10, fill="white",
                                   outline="black")
            doska.create_rectangle(x_3 + 10, y_3 + 10, x_3 + 2 * k - 10, y_3 + k - 10, fill="white", outline="black")
            doska.create_rectangle(x_2 + 9 * k + 10, y_2 + 10, x_2 + 10 * k - 10, y_2 + k * 2 - 10, fill="white",
                                   outline="black")
            doska.create_rectangle(x_3 + 10, y_3 + 9 * k + 10, x_3 + 2 * k - 10, y_3 + 10 * k - 10, fill="white",
                                   outline="black")
            y_2 += 2 * k
            x_3 += 2 * k
    while x < k * 9:  # игровое поле без баз
        y = 1 * k
        while y < k * 9:
            doska.create_rectangle(x, y, x + k, y + k, outline="black", width=1)
            y += 1 * k
        x += 1 * k
    while x1 < k * 9:  # маленькие квадраты на поле
        y1 = 3 * k
        while y1 < k * 9:
            doska.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, outline="purple")
            y1 += 2 * k
        x1 += 2 * k
    while x2 < k * 9:  # вертикальные жирные линии
        y2 = m_pr
        doska.create_line(x2, y2, x2, 9 * y2, width=3, fill="grey")
        x2 += 2 * k
    while x3 < k * 9:  # горизонтальные жирные линии
        y3 = m_pr
        # 100 300
        doska.create_line(y3, x3, 9 * y3, x3, width=3, fill="grey")
        x3 += 2 * k
    ots = mashtab / 200  # отступ, что бы фишки не соприкасались
    ots_r = mashtab / 125  # отступ для рамки, чтобы создать вид трехмерности
    spisok1 = [2, 4, 6, 8]  # параметр для квадратов
    spisok2 = [1, 3, 5, 7]
    # поле готово

    for t in range(10):  # Создание фишек. Стоячие фигуры без анимации
        for u in range(10):
            z = pole[t][u]  # перебор каждого значения на поле
            if z:  # если в точке есть значение больше 0
                fhi = [0, 2]
                # стоячие красные фишки горизонтальные
                if z == 1:
                    list = [13, 15]
                    if pole[y_poz_1][x_poz_1] in list: # если по фигуре ходит квадрат соперника
                        # смещаем значения, чтобы не писать код дважды для разных координат
                        if pole[y_poz_2][x_poz_2] != 1 and pole[y_poz_2][x_poz_2] != 5:
                            if y_poz_2 in spisok1:
                                y_poz_2 = y_poz_2 - 1
                            elif y_poz_2 in spisok2:
                                y_poz_2 = y_poz_2 + 1
                    # проверка чтобы тык засчитался
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) and f_hi in fhi and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        # если противник нас подвинул, то отрисовки стоячей фигуры нет.
                        if pole[y_poz_2][x_poz_2] == 5:
                            x_poz_2 = x_poz_2 - 1
                            # в итоге пешки которые двигаем не оставляют шлейф
                    else: # если ходим мы этой фигурой
                        if (x_poz_1, y_poz_1) != (u, t): # если ходим, пропадает стоячая фигура.
                            doska.create_line(u * m_pr + ots_r, t * m_pr + m_pr - ots, u * m_pr + 2 * m_pr - m_pr / 100,
                                              t * m_pr + m_pr - ots, width=m_pr / 12.5)  # рамка
                            doska.create_line(u * m_pr + 2 * m_pr - ots, t * m_pr + ots_r, u * m_pr + 2 * m_pr - ots,
                                              t * m_pr + m_pr - m_pr / 100, width=m_pr / 12.5)  # рамка
                            doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + 2 * m_pr - 1.5 * ots,
                                                   t * m_pr + m_pr - 1.5 * ots, fill='red', outline="black")  # фигура
                # стоячие зеленые фишки горизонтальные
                if z == 3:
                    list = [9, 11]
                    if pole[y_poz_1][x_poz_1] in list:  # если ходим квадратом
                        # проверка сверху или снизу фигура
                        if pole[y_poz_2][x_poz_2] != 3 and pole[y_poz_2][x_poz_2] != 6:
                            if y_poz_2 in spisok1:
                                y_poz_2 = y_poz_2 - 1
                            elif y_poz_2 in spisok2:
                                y_poz_2 = y_poz_2 + 1
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) and f_hi == 1\
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:  # проверка чтобы тык засчитался
                            if pole[y_poz_2][x_poz_2] == 6:
                                x_poz_2 = x_poz_2 - 1
                            # в итоге пешки которые двигаем не оставляют шлейф
                    else:
                        if (x_poz_1, y_poz_1) != (u, t):
                            doska.create_line(u * m_pr + ots_r, t * m_pr + m_pr - ots, u * m_pr + 2 * m_pr - m_pr / 100,
                                              t * m_pr + m_pr - ots, width=m_pr / 12.5)
                            doska.create_line(u * m_pr + 2 * m_pr - ots, t * m_pr + ots_r, u * m_pr + 2 * m_pr - ots,
                                              t * m_pr + m_pr - m_pr / 100, width=m_pr / 12.5)
                            doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + 2 * m_pr - 1.5 * ots,
                                                   t * m_pr + m_pr - 1.5 * ots, fill='green', outline="black")
                # стоячие красные фишки вертикальные
                elif z == 2:
                    list = [13, 15]
                    if pole[y_poz_1][x_poz_1] in list:
                        if pole[y_poz_2][x_poz_2] != 2 and pole[y_poz_2][x_poz_2] != 7:
                            if x_poz_2 in spisok1:
                                x_poz_2 = x_poz_2 - 1
                            elif x_poz_2 in spisok2:
                                x_poz_2 = x_poz_2 + 1
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) and f_hi in fhi and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if pole[y_poz_2][x_poz_2] == 7:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if (x_poz_1, y_poz_1) != (u, t):
                            doska.create_line(u * m_pr + m_pr - ots, t * m_pr + ots_r, u * m_pr + m_pr - ots,
                                              t * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5)
                            doska.create_line(u * m_pr + ots_r, t * m_pr + 2 * m_pr - ots, u * m_pr + m_pr - m_pr / 100,
                                              t * m_pr + 2 * m_pr - ots, width=m_pr / 12.5)
                            doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + m_pr - 1.5 * ots,
                                                   t * m_pr + 2 * m_pr - 1.5 * ots, fill='red', outline="black")
                # стоячие зеленые фишки вертикальные
                elif z == 4:
                    list1 = [9, 11]
                    if pole[y_poz_1][x_poz_1] in list1:
                        if pole[y_poz_2][x_poz_2] != 4 and pole[y_poz_2][x_poz_2] != 8:
                            if x_poz_2 in spisok1:
                                x_poz_2 = x_poz_2 - 1
                            elif x_poz_2 in spisok2:
                                x_poz_2 = x_poz_2 + 1
                    if ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) and f_hi == 1\
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if pole[y_poz_2][x_poz_2] == 8:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if (x_poz_1, y_poz_1) != (u, t):
                            doska.create_line(u * m_pr + m_pr - ots, t * m_pr + ots_r, u * m_pr + m_pr - ots,
                                              t * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5)
                            doska.create_line(u * m_pr + ots_r, t * m_pr + 2 * m_pr - ots,
                                              u * m_pr + m_pr - m_pr / 100,
                                              t * m_pr + 2 * m_pr - ots, width=m_pr / 12.5)
                            doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + m_pr - 1.5 * ots,
                                                   t * m_pr + 2 * m_pr - 1.5 * ots, fill='green', outline="black")
                # для горизонатльных квадратов красных
                elif z == 9:
                    list = [13, 15]
                    # если ходит противник по фигуре и указывает на точку внизу, то смещаем координаты
                    # чтобы не дублировать код
                    if pole[y_poz_1][x_poz_1] in list and y_poz_2 in spisok1:
                        y_poz_2 -= 1
                    # если квадрат противника двигает фигуру
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) or (
                            (x_poz_2, y_poz_2 + 1) == (u, t) or (x_poz_2, y_poz_2 + 1) == (u + 1, t)))\
                            and f_hi in fhi and pole[y_poz_1][x_poz_1] in list and abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        # то не рисуем стоячую фигуру
                        if pole[y_poz_2][x_poz_2] == 10:
                            x_poz_2 = x_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t))\
                            and f_hi in fhi and pole[y_poz_1][x_poz_1] == 3 and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        # то не рисуем стоячую фигуру
                        if pole[y_poz_2][x_poz_2] == 10:
                            x_poz_2 = x_poz_2 - 1
                    else: # отрисовка стоячей фигуры
                        if pole[t][u] == 9 and t in spisok2:  # для верхней планки
                            if (x_poz_1, y_poz_1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + 2 * m_pr - 1.5 * ots,
                                                       t * m_pr + m_pr - ots, fill='red', outline="black")
                        elif pole[t - 1][u] == 9: # для нижней планки + рамка
                            if (x_poz_1, y_poz_1 + 1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + 2 * m_pr - 1.5 * ots,
                                                       t * m_pr + m_pr - 1.5 * ots, fill='red', outline="black")
                                doska.create_line(u * m_pr + ots_r, t * m_pr + m_pr - ots + 1,
                                                  u * m_pr + 2 * m_pr - ots, t * m_pr + m_pr - ots + 1,
                                                  width=m_pr / 15.2)
                                doska.create_line(u * m_pr + 2 * m_pr - ots + 1, t * m_pr - m_pr + ots_r,
                                                  u * m_pr + 2 * m_pr - ots + 1, t * m_pr + m_pr - m_pr / 200,
                                                  width=m_pr / 15.2)
                # для вертикальных квадратов красных
                elif z == 13:
                    list1 = [9, 11]
                    if pole[y_poz_1][x_poz_1] in list1 and y_poz_2 in spisok1:
                        y_poz_2 -= 1
                    # проверка чтобы тык засчитался
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u + 1, t)) or (
                            (x_poz_2, y_poz_2 + 1) == (u, t) or (x_poz_2, y_poz_2 + 1) == (
                            u + 1, t))) and f_hi and pole[y_poz_1][x_poz_1] in list1\
                            and abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        if pole[y_poz_2][x_poz_2] == 14:
                            x_poz_2 = x_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u+1, t)) and f_hi and pole[y_poz_1][x_poz_1] == 1 \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if pole[y_poz_2][x_poz_2] == 14:
                            x_poz_2 = x_poz_2 - 1
                    else:
                        if pole[t][u] == 13 and t in spisok2:
                            if (x_poz_1, y_poz_1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + 2 * m_pr - 1.5 * ots,
                                                       t * m_pr + m_pr - ots, fill='green', outline="black")
                        elif pole[t - 1][u] == 13:
                            if (x_poz_1, y_poz_1 + 1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + 2 * m_pr - 1.5 * ots,
                                                       t * m_pr + m_pr - 1.5 * ots, fill='green', outline="black")
                                doska.create_line(u * m_pr + ots_r, t * m_pr + m_pr - ots + 1,
                                                  u * m_pr + 2 * m_pr - ots, t * m_pr + m_pr - ots + 1,
                                                  width=m_pr / 15.2)
                                doska.create_line(u * m_pr + 2 * m_pr - ots + 1, t * m_pr - m_pr + ots_r,
                                                  u * m_pr + 2 * m_pr - ots + 1, t * m_pr + m_pr - m_pr / 200,
                                                  width=m_pr / 15.2)
                # для горизонатльных квадратов зеленых
                elif z == 11:
                    list = [13, 15]
                    if pole[y_poz_1][x_poz_1] in list and x_poz_2 in spisok1:
                        x_poz_2 -= 1
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) or (
                            (x_poz_2 + 1, y_poz_2) == (u, t) or (x_poz_2 + 1, y_poz_2) == (u, t + 1)))\
                            and f_hi in fhi and pole[y_poz_1][x_poz_1] in list and abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        if pole[y_poz_2][x_poz_2] == 12:
                            y_poz_2 = y_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1))\
                        and f_hi in fhi and pole[y_poz_1][x_poz_1] == 4 and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if pole[y_poz_2][x_poz_2] == 12:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if pole[t][u] == 11 and u in spisok2:
                            if (x_poz_1, y_poz_1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + m_pr - ots,
                                                       t * m_pr + 2 * m_pr - 1.5 * ots, fill='red', outline="black")
                        elif pole[t][u - 1] == 11:
                            if (x_poz_1 + 1, y_poz_1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + m_pr - 1.5 * ots,
                                                       t * m_pr + 2 * m_pr - 1.5 * ots, fill='red', outline="black")
                                doska.create_line(u * m_pr - m_pr + ots_r, t * m_pr + 2 * m_pr - ots + 1,
                                                  u * m_pr + m_pr - ots, t * m_pr + 2 * m_pr - ots + 1,
                                                  width=m_pr / 15.2)
                                doska.create_line(u * m_pr + m_pr - ots + 1, t * m_pr + ots_r,
                                                  u * m_pr + m_pr - ots + 1, t * m_pr + 2 * m_pr - m_pr / 200,
                                                  width=m_pr / 15.2)
                # для вертикальных квадратов зеленых
                elif z == 15:
                    list1 = [9, 11]
                    if pole[y_poz_1][x_poz_1] in list1 and x_poz_2 in spisok1:
                        x_poz_2 -= 1
                    if (((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t + 1)) or (
                            (x_poz_2 + 1, y_poz_2) == (u, t) or (x_poz_2 + 1, y_poz_2) == (
                            u, t + 1))) and f_hi and pole[y_poz_1][x_poz_1] in list1\
                            and abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3:
                        if pole[y_poz_2][x_poz_2] == 16:
                            y_poz_2 = y_poz_2 - 1
                    elif ((x_poz_2, y_poz_2) == (u, t) or (x_poz_2, y_poz_2) == (u, t+1)) and f_hi and pole[y_poz_1][x_poz_1] == 2 \
                            and abs(x_poz_1 - x_poz_2) < 4 and abs(y_poz_1 - y_poz_2) < 4:
                        if pole[y_poz_2][x_poz_2] == 16:
                            y_poz_2 = y_poz_2 - 1
                    else:
                        if pole[t][u] == 15 and u in spisok2:
                            if (x_poz_1, y_poz_1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + m_pr - ots,
                                                       t * m_pr + 2 * m_pr - 1.5 * ots, fill='green', outline="black")
                        elif pole[t][u - 1] == 15:
                            if (x_poz_1 + 1, y_poz_1) != (u, t):
                                doska.create_rectangle(u * m_pr + ots, t * m_pr + ots, u * m_pr + m_pr - 1.5 * ots,
                                                       t * m_pr + 2 * m_pr - 1.5 * ots, fill='green', outline="black")
                                doska.create_line(u * m_pr - m_pr + ots_r, t * m_pr + 2 * m_pr - ots + 1,
                                                  u * m_pr + m_pr - ots, t * m_pr + 2 * m_pr - ots + 1,
                                                  width=m_pr / 15.2)
                                doska.create_line(u * m_pr + m_pr - ots + 1, t * m_pr + ots_r,
                                                  u * m_pr + m_pr - ots + 1, t * m_pr + 2 * m_pr - m_pr / 200,
                                                  width=m_pr / 15.2)
    for y_i in range(1, 9):  # если квадраты образуются от хода соперника
        for x_i in range(1, 9):
            if pole[y_i][x_i] == 1 and pole[y_i + 1][x_i] == 1 and (y_i == 1 or y_i == 3 or y_i == 5 or y_i == 7):
                pole[y_i][x_i] = 9
                pole[y_i + 1][x_i] = 9
                pole[y_i][x_i + 1] = 10
                pole[y_i + 1][x_i + 1] = 10
            elif pole[y_i][x_i] == 3 and pole[y_i + 1][x_i] == 3 and (y_i == 1 or y_i == 3 or y_i == 5 or y_i == 7):
                pole[y_i][x_i] = 13
                pole[y_i + 1][x_i] = 13
                pole[y_i][x_i + 1] = 14
                pole[y_i + 1][x_i + 1] = 14
            elif pole[y_i][x_i] == 2 and pole[y_i][x_i + 1] == 2 and (x_i == 1 or x_i == 3 or x_i == 5 or x_i == 7):
                pole[y_i][x_i] = 11
                pole[y_i][x_i + 1] = 11
                pole[y_i + 1][x_i] = 12
                pole[y_i + 1][x_i + 1] = 12
            elif pole[y_i][x_i] == 4 and pole[y_i][x_i + 1] == 4 and (x_i == 1 or x_i == 3 or x_i == 5 or x_i == 7):
                pole[y_i][x_i] = 15
                pole[y_i][x_i + 1] = 15
                pole[y_i + 1][x_i] = 16
                pole[y_i + 1][x_i + 1] = 16

    # ANIMATION. Когда происходит ход, отрисовка стоячих фигур убирается в месте указанный позиций.
    z = pole[y_poz_1][x_poz_1]
    if z:
        # Создаем Тэг для каждой детали для отрисовки движения
        if z == 1:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_1 * m_pr + m_pr - 1.5 * ots, fill='red', outline="black", tags='ani1')
            doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + m_pr - ots,
                              x_poz_1 * m_pr + 2 * m_pr - m_pr / 100, y_poz_1 * m_pr + m_pr - ots, width=m_pr / 12.5,
                              tags='rama1')
            doska.create_line(x_poz_1 * m_pr + 2 * m_pr - ots, y_poz_1 * m_pr + ots_r, x_poz_1 * m_pr + 2 * m_pr - ots,
                              y_poz_1 * m_pr + m_pr - m_pr / 100, width=m_pr / 12.5, tags='rama2')
        elif z == 2:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + m_pr - 1.5 * ots,
                                   y_poz_1 * m_pr + 2 * m_pr - 1.5 * ots, fill='red', tags='ani2')
            doska.create_line(x_poz_1 * m_pr + m_pr - ots, y_poz_1 * m_pr + ots_r, x_poz_1 * m_pr + m_pr - ots,
                              y_poz_1 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5, tags='rama3')
            doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + 2 * m_pr - ots,
                              x_poz_1 * m_pr + m_pr - m_pr / 100, y_poz_1 * m_pr + 2 * m_pr - ots, width=m_pr / 12.5,
                              tags='rama4')
        elif z == 3:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_1 * m_pr + m_pr - 1.5 * ots, fill='green', tags='ani3')
            doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + m_pr - ots,
                              x_poz_1 * m_pr + 2 * m_pr - m_pr / 100, y_poz_1 * m_pr + m_pr - ots, width=m_pr / 12.5,
                              tags='rama1')
            doska.create_line(x_poz_1 * m_pr + 2 * m_pr - ots, y_poz_1 * m_pr + ots_r, x_poz_1 * m_pr + 2 * m_pr - ots,
                              y_poz_1 * m_pr + m_pr - m_pr / 100, width=m_pr / 12.5, tags='rama2')
        elif z == 4:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + m_pr - 1.5 * ots,
                                   y_poz_1 * m_pr + 2 * m_pr - 1.5 * ots, fill='green', tags='ani4')
            doska.create_line(x_poz_1 * m_pr + m_pr - ots, y_poz_1 * m_pr + ots_r, x_poz_1 * m_pr + m_pr - ots,
                              y_poz_1 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5, tags='rama3')
            doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + 2 * m_pr - ots,
                              x_poz_1 * m_pr + m_pr - m_pr / 100, y_poz_1 * m_pr + 2 * m_pr - ots, width=m_pr / 12.5,
                              tags='rama4')
        elif z == 9:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_1 * m_pr + m_pr - ots, fill='red', tags='ani9')
            doska.create_rectangle(x_poz_1 * m_pr + ots, (y_poz_1 + 1) * m_pr + ots,
                                   x_poz_1 * m_pr + 2 * m_pr - 1.5 * ots, (y_poz_1 + 1) * m_pr + m_pr - 1.5 * ots,
                                   fill='red', tags='ani10')
            if y_poz_1 in spisok2:
                doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  x_poz_1 * m_pr + 2 * m_pr - ots, y_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  width=m_pr / 15.2, tags='ramakub1')
                doska.create_line(x_poz_1 * m_pr + 2 * m_pr - ots + 1, y_poz_1 * m_pr + ots_r,
                                  x_poz_1 * m_pr + 2 * m_pr - ots + 1, y_poz_1 * m_pr + 2 * m_pr - m_pr / 200,
                                  width=m_pr / 15.2, tags='ramakub2')
        elif z == 13:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_1 * m_pr + m_pr - ots, fill='green', tags='ani13')
            doska.create_rectangle(x_poz_1 * m_pr + ots, (y_poz_1 + 1) * m_pr + ots,
                                   x_poz_1 * m_pr + 2 * m_pr - 1.5 * ots, (y_poz_1 + 1) * m_pr + m_pr - 1.5 * ots,
                                   fill='green', tags='ani14')
            if y_poz_1 in spisok2:
                doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  x_poz_1 * m_pr + 2 * m_pr - ots, y_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  width=m_pr / 15.2, tags='ramakub1')
                doska.create_line(x_poz_1 * m_pr + 2 * m_pr - ots + 1, y_poz_1 * m_pr + ots_r,
                                  x_poz_1 * m_pr + 2 * m_pr - ots + 1, y_poz_1 * m_pr + 2 * m_pr - m_pr / 200,
                                  width=m_pr / 15.2, tags='ramakub2')
        elif z == 11:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + m_pr - ots,
                                   y_poz_1 * m_pr + 2 * m_pr - 1.5 * ots, fill='red', tags='ani11')
            doska.create_rectangle((x_poz_1 + 1) * m_pr + ots, y_poz_1 * m_pr + ots,
                                   (x_poz_1 + 1) * m_pr + m_pr - 1.5 * ots, y_poz_1 * m_pr + 2 * m_pr - 1.5 * ots,
                                   fill='red', tags='ani12')
            if x_poz_1 in spisok2:
                doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  x_poz_1 * m_pr + 2 * m_pr - ots,
                                  y_poz_1 * m_pr + 2 * m_pr - ots + 1, width=m_pr / 15.2, tags='ramakub1')
                doska.create_line(x_poz_1 * m_pr + 2 * m_pr - ots + 1, y_poz_1 * m_pr + ots_r,
                                  x_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  y_poz_1 * m_pr + 2 * m_pr - m_pr / 200, width=m_pr / 15.2, tags='ramakub2')
        elif z == 15:
            doska.create_rectangle(x_poz_1 * m_pr + ots, y_poz_1 * m_pr + ots, x_poz_1 * m_pr + m_pr - ots,
                                   y_poz_1 * m_pr + 2 * m_pr - 1.5 * ots, fill='green', tags='ani15')
            doska.create_rectangle((x_poz_1 + 1) * m_pr + ots, y_poz_1 * m_pr + ots,
                                   (x_poz_1 + 1) * m_pr + m_pr - 1.5 * ots, y_poz_1 * m_pr + 2 * m_pr - 1.5 * ots,
                                   fill='green', tags='ani16')
            if x_poz_1 in spisok2:
                doska.create_line(x_poz_1 * m_pr + ots_r, y_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  x_poz_1 * m_pr + 2 * m_pr - ots,
                                  y_poz_1 * m_pr + 2 * m_pr - ots + 1, width=m_pr / 15.2, tags='ramakub1')
                doska.create_line(x_poz_1 * m_pr + 2 * m_pr - ots + 1, y_poz_1 * m_pr + ots_r,
                                  x_poz_1 * m_pr + 2 * m_pr - ots + 1,
                                  y_poz_1 * m_pr + 2 * m_pr - m_pr / 200, width=m_pr / 15.2, tags='ramakub2')
    # переменные
    kx = 10  # коэффициент направления
    ky = 10  # коэффициент направления
    b = 0
    par_kvadro = 13  # определяем значения переменных, чтобы убрать указания по pep8 из консоли
    par_fishki = par_kvadro_gor = 0
    par_fishki2 = par_kvadro_vert = 0
    ani = ani2 = ani3 = ani4 = 0
    svet = vkx = vky = vrange = 0
    poz_ugla = poz_ugla2 = poz3 = poz4 = poz5 = -1
    poz33 = -2
    poz44 = -2
    vector_kv = 0
    rama1 = 'rama1'  # tags
    rama2 = 'rama2'
    rama3 = 'rama3'
    rama4 = 'rama4'
    ramakub1 = 'ramakub1'
    ramakub2 = 'ramakub2'
    if f_hi == 1:  # для ходов игрока параметры
        # ход игрока
        par_fishki = 3
        par_fishki2 = 4
        par_kvadro_gor = 13
        par_kvadro_vert = 15
        ani = 'ani1'
        ani2 = 'ani2'
        svet = 'green'
        if z == 9:
            ani3 = 'ani9'
            ani4 = 'ani10'
        elif z == 11:
            ani3 = 'ani11'
            ani4 = 'ani12'
    elif f_hi == 0 or f_hi == 2:  # для ходов игрока и компьютера разные параметры
        # ход компьютера
        par_fishki = 1
        par_fishki2 = 2
        par_kvadro_gor = 9
        par_kvadro_vert = 11
        ani = 'ani3'
        ani2 = 'ani4'
        svet = 'red'
        if z == 13:
            ani3 = 'ani13'
            ani4 = 'ani14'
        elif z == 15:
            ani3 = 'ani15'
            ani4 = 'ani16'
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
    if z == 1 or z == 3:
        if x_poz_2 == 2 or x_poz_2 == 4 or x_poz_2 == 6 or x_poz_2 == 8:  # корректировка смещения точки выбора
            x_poz_2 = x_poz_2 - 1
        # определение векторов для хода горизонтальных фишек
        if x_poz_1 == x_poz_2 and abs(y_poz_1 - y_poz_2) <= 3:
            kx = 0
            if y_poz_1 < y_poz_2:
                ky = 1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    poz3 = pole[y_poz_2 + 1][x_poz_2]
                    poz4 = pole[y_poz_2 + 1][x_poz_2 + 1]
                else:
                    poz3 = 0
                    poz4 = 0
            elif y_poz_1 > y_poz_2:
                ky = -1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    poz3 = pole[y_poz_2 - 1][x_poz_2]
                    poz4 = pole[y_poz_2 - 1][x_poz_2 + 1]
                else:
                    poz3 = 0
                    poz4 = 0
        elif y_poz_1 == y_poz_2 and abs(x_poz_1 - x_poz_2) <= 3:
            ky = 0
            if x_poz_1 < x_poz_2:
                kx = 2
                if x_poz_2 < 7:
                    poz3 = pole[y_poz_2][x_poz_2 + 2]
                    poz4 = pole[y_poz_2][x_poz_2 + 3]
            elif x_poz_1 > x_poz_2:
                kx = -2
                if x_poz_2 != 0:
                    poz3 = pole[y_poz_2][x_poz_2 - 1]
                    poz4 = pole[y_poz_2][x_poz_2 - 2]
        # после того как нашли коэффициенты
        if pole[y_poz_2][x_poz_2] == 0 and x_poz_2 != 9:  # анимация хода для горизонтальных фигур
            if pole[y_poz_2][x_poz_2 + 1] == 0 and w == 1:  # что бы не было задвоенного хода
                if kx == 0 and abs(y_poz_1 - y_poz_2) < 2:  # ход вверх и вниз
                    for i in range(abs(y_poz_1 - y_poz_2)):  # анимация перемещения пешки
                        for ii in range(0, int(m_pr / vrange)):  # анимация движения по длине в скобках.
                            b = 1
                            doska.move(ani, vkx * kx, vky * ky)  # за счет умножения на 4 увеличиваем скорость анимации
                            doska.move(rama1, vkx * kx, vky * ky)
                            doska.move(rama2, vkx * kx, vky * ky)
                            doska.update()  # обновление
                            time.sleep(0.01)
                elif ky == 0 and abs(x_poz_1 - x_poz_2) < 3:  # ход влево и вправо
                    for i in range(abs(x_poz_1 - x_poz_2)):  # анимация перемещения пешки
                        for ii in range(int(m_pr / vrange)):  # анимация движения по длине в скобках
                            b = 1
                            doska.move(ani, vkx / 2 * kx, vky / 2 * ky)
                            doska.move(rama1, vkx / 2 * kx, vky / 2 * ky)
                            doska.move(rama2, vkx / 2 * kx, vky / 2 * ky)
                            doska.update()  # обновление
                            time.sleep(0.01)
        # анимация перемещения противника
        elif pole[y_poz_2][x_poz_2] == par_fishki and poz3 == 0 and poz4 == 0:  # анимация перемещения противника
            doska.create_line(x_poz_2 * m_pr + ots_r, y_poz_2 * m_pr + m_pr - ots, (x_poz_2 + 2) * m_pr - m_pr / 100,
                              y_poz_2 * m_pr + m_pr - ots, width=m_pr / 12.5, tags='ramaDV')  # рамка
            doska.create_line(x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + 2 * m_pr - ots,
                              y_poz_2 * m_pr + m_pr - m_pr / 100, width=m_pr / 12.5, tags='ramaDV2')  # рамка
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + m_pr - 1.5 * ots, fill=svet, tags='DV')
            for i in range(abs(y_poz_1 - y_poz_2)):
                if y_poz_2 == 0 or y_poz_2 == 9:
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani, kx, vky / 2 * ky)
                        doska.move(rama1, kx, vky / 2 * ky)
                        doska.move(rama2, kx, vky / 2 * ky)
                        doska.move('DV', kx, vky / 2 * ky)
                        doska.move('ramaDV', kx, vky / 2 * ky)
                        doska.move('ramaDV2', kx, vky / 2 * ky)
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani, - kx, - vky / 2 * ky)
                        doska.move(rama1, - kx, - vky / 2 * ky)
                        doska.move(rama2, - kx, - vky / 2 * ky)
                        doska.update()
                        time.sleep(0.01)
                else:
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani, kx, vky * ky)
                        doska.move(rama1, kx, vky * ky)
                        doska.move(rama2, kx, vky * ky)
                        doska.move('DV', kx, vky * ky)
                        doska.move('ramaDV', kx, vky * ky)
                        doska.move('ramaDV2', kx, vky * ky)
                        doska.update()
                        time.sleep(0.01)
        # анимация разбивания квадрата противника
        elif pole[y_poz_2][x_poz_2] == par_kvadro_gor and poz3 == 0 and poz4 == 0:
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + m_pr - 1.5 * ots, fill=svet, tags='DV')
            doska.create_line(x_poz_2 * m_pr + ots_r, y_poz_2 * m_pr + m_pr - ots + 1,
                              x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + m_pr - ots + 1,
                              width=m_pr / 15.2, tags='ramaDV')
            doska.create_line(x_poz_2 * m_pr + 2 * m_pr - ots + 1, y_poz_2 * m_pr + ots_r,
                              x_poz_2 * m_pr + 2 * m_pr - ots + 1, y_poz_2 * m_pr + m_pr - m_pr / 200,
                              width=m_pr / 15.2, tags='ramaDV2')
            for i in range(abs(2)):
                for ii in range(int(m_pr / vrange)):
                    b = 1
                    doska.move(ani, kx, vky * ky)
                    doska.move(rama1, kx, vky * ky)
                    doska.move(rama2, kx, vky * ky)
                    doska.move('DV', kx, vky * ky)
                    doska.move('ramaDV', kx, vky * ky)
                    doska.move('ramaDV2', kx, vky * ky)
                    doska.update()
                    time.sleep(0.01)
        # фикс если ход не возможен
        elif pole[y_poz_2][x_poz_2] == par_fishki and (poz3 != 0 or poz4 != 0):
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + m_pr - 1.5 * ots, fill=svet)
            doska.create_line(x_poz_2 * m_pr + ots_r, (y_poz_2 + 1) * m_pr - ots, (x_poz_2 + 2) * m_pr - m_pr / 100,
                              y_poz_2 * m_pr + m_pr - ots, width=m_pr / 12.5)  # рамка
            doska.create_line(x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + 2 * m_pr - ots,
                              y_poz_2 * m_pr + m_pr - m_pr / 100, width=m_pr / 12.5)
        # фикс если ход не возможен
        elif pole[y_poz_2][x_poz_2] == par_fishki2:
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + 2 * m_pr - 1.5 * ots, fill=svet)
            doska.create_line(x_poz_2 * m_pr + m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + m_pr - ots,
                              y_poz_2 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5)
            doska.create_line(x_poz_2 * m_pr + ots_r, (y_poz_2 + 2) * m_pr - ots, (x_poz_2 + 1) * m_pr - m_pr / 100,
                              y_poz_2 * m_pr + 2 * m_pr - ots, width=m_pr / 12.5)
        # фикс если ход не возможен
        elif pole[y_poz_2][x_poz_2] == par_kvadro_gor and (poz3 != 0 or poz4 != 0):
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + m_pr - 1.5 * ots, fill=svet)
            doska.create_line(x_poz_2 * m_pr + ots_r, y_poz_2 * m_pr + m_pr - ots + 1,
                              x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + m_pr - ots + 1,
                              width=m_pr / 15.2)
            doska.create_line(x_poz_2 * m_pr + 2 * m_pr - ots + 1, y_poz_2 * m_pr - m_pr + ots_r,
                              x_poz_2 * m_pr + 2 * m_pr - ots + 1, y_poz_2 * m_pr + m_pr - m_pr / 200,
                              width=m_pr / 15.2)
        # анимация угла для горизонтальных фигур
        elif pole[y_poz_2][x_poz_2] == 17:
            if y_poz_1 == 0:
                if x_poz_2 == 9:
                    poz_ugla = pole[y_poz_1 + 1][x_poz_1 + 2]
                    poz_ugla2 = pole[y_poz_1 + 2][x_poz_1 + 2]
                elif x_poz_2 == 0:
                    poz_ugla = pole[y_poz_1 + 1][x_poz_1 - 1]
                    poz_ugla2 = pole[y_poz_1 + 2][x_poz_1 - 1]
            elif y_poz_1 == 9:
                if x_poz_2 == 9:
                    poz_ugla = pole[y_poz_1 - 1][x_poz_1 + 2]
                    poz_ugla2 = pole[y_poz_1 - 2][x_poz_1 + 2]
                elif x_poz_2 == 0:
                    poz_ugla = pole[y_poz_1 - 1][x_poz_1 - 1]
                    poz_ugla2 = pole[y_poz_1 - 2][x_poz_1 - 1]
            if poz_ugla == 0 and poz_ugla2 == 0:
                for i in range(1):
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani, vkx * kx / 2, ky)
                        doska.move(rama1, vkx * kx / 2, ky)
                        doska.move(rama2, vkx * kx / 2, ky)
                        doska.update()
                        time.sleep(0.01)
                # для нижнего справа угла
                if y_poz_2 == 9 and x_poz_2 == 9:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots) + vkx * ii - m_pr, (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama1, (x_poz_2 * m_pr) + vkx * ii - m_pr + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100, (y_poz_2 * m_pr + m_pr - ots))
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots) - vkx * ii,
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama2, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) - vkx * ii + + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - ots, (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani, 0, - vkx * kx / 2)
                            doska.move(rama1, 0, - vkx * kx / 2)
                            doska.move(rama2, 0, - vkx * kx / 2)
                            doska.update()
                            time.sleep(0.01)
                # для верхнего справа угла
                elif y_poz_2 == 0 and x_poz_2 == 9:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots) + vkx * ii - m_pr, (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama1, (x_poz_2 * m_pr) + vkx * ii - m_pr + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100, (y_poz_2 * m_pr + m_pr - ots))
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots) + vkx * ii)
                        doska.coords(rama1, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) + m_pr + vkx * ii - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100,
                                     (y_poz_2 * m_pr + m_pr) + vkx * ii - ots)
                        doska.coords(rama2, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - ots,
                                     (y_poz_2 * m_pr + m_pr) + vkx * ii - m_pr / 100)
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani, 0, vkx * kx / 2)
                            doska.move(rama1, 0, vkx * kx / 2)
                            doska.move(rama2, 0, vkx * kx / 2)
                            doska.update()
                            time.sleep(0.01)
                # для нижнего слева угла
                if y_poz_2 == 9 and x_poz_2 == 0:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - vkx * ii,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama1, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - vkx * ii - m_pr / 100, (y_poz_2 * m_pr + m_pr - ots))
                        doska.coords(rama2, (x_poz_2 * m_pr) + 2 * m_pr - vkx * ii - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - vkx * ii - ots, (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots) - vkx * ii,
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama2, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) - vkx * ii + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - ots, (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani, 0, vkx * kx / 2)
                            doska.move(rama1, 0, vkx * kx / 2)
                            doska.move(rama2, 0, vkx * kx / 2)
                            doska.update()
                            time.sleep(0.01)
                # для верхнего слева угла
                if y_poz_2 == 0 and x_poz_2 == 0:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - vkx * ii,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama1, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - vkx * ii - m_pr / 100 - ots,
                                     (y_poz_2 * m_pr + m_pr - ots))
                        doska.coords(rama2, (x_poz_2 * m_pr) - vkx * ii + 2 * m_pr - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - vkx * ii - ots, (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots) + vkx * ii)
                        doska.coords(rama1, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) + m_pr + vkx * ii - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100,
                                     (y_poz_2 * m_pr + m_pr) + vkx * ii - ots)
                        doska.coords(rama2, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - ots,
                                     (y_poz_2 * m_pr + m_pr) + vkx * ii - m_pr / 100)
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani, 0, -vkx * kx / 2)
                            doska.move(rama1, 0, -vkx * kx / 2)
                            doska.move(rama2, 0, -vkx * kx / 2)
                            doska.update()
                            time.sleep(0.01)
    # для вертикальных
    elif z == 2 or z == 4:
        if y_poz_2 == 2 or y_poz_2 == 4 or y_poz_2 == 6 or y_poz_2 == 8:
            y_poz_2 = y_poz_2 - 1
        # определение векторов для хода вертикальных фишек
        if x_poz_1 == x_poz_2 and abs(y_poz_1 - y_poz_2) <= 3:
            kx = 0
            if y_poz_1 < y_poz_2:
                ky = 2
                if y_poz_2 < 7:
                    poz3 = pole[y_poz_2 + 2][x_poz_2]
                    poz4 = pole[y_poz_2 + 3][x_poz_2]
            elif y_poz_1 > y_poz_2:
                ky = -2
                if y_poz_2 != 0:
                    poz3 = pole[y_poz_2 - 1][x_poz_2]
                    poz4 = pole[y_poz_2 - 2][x_poz_2]
        elif y_poz_1 == y_poz_2 and abs(x_poz_1 - x_poz_2) <= 3:
            ky = 0
            if x_poz_1 < x_poz_2:
                kx = 1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = pole[y_poz_2][x_poz_2 + 1]
                    poz4 = pole[y_poz_2 + 1][x_poz_2 + 1]
                else:
                    poz3 = 0
                    poz4 = 0
            elif x_poz_1 > x_poz_2:
                kx = -1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = pole[y_poz_2][x_poz_2 - 1]
                    poz4 = pole[y_poz_2 + 1][x_poz_2 - 1]
                else:
                    poz3 = 0
                    poz4 = 0
        # после того как нашли коэффициенты
        if pole[y_poz_2][x_poz_2] == 0 and y_poz_2 != 9:  # анимация хода для вертикальных фигур
            if pole[y_poz_2 + 1][x_poz_2] == 0 and w == 1:  # что бы не было задвоенного хода
                if ky == 0 and abs(x_poz_1 - x_poz_2) < 2:  # ход влево и вправо
                    for i in range(abs(x_poz_1 - x_poz_2)):  # анимация перемещения пешки
                        for ii in range(int(m_pr / vrange)):  # анимация движения по длине в скобках
                            b = 1
                            doska.move(ani2, vkx * kx, vky * ky)
                            doska.move(rama3, vkx * kx, vky * ky)
                            doska.move(rama4, vkx * kx, vky * ky)
                            doska.update()  # обновление
                            time.sleep(0.01)
                elif kx == 0 and abs(y_poz_1 - y_poz_2) < 3:  # ход вверх и вниз
                    for i in range(abs(y_poz_1 - y_poz_2)):  # анимация перемещения пешки
                        for ii in range(int(m_pr / vrange)):  # анимация движения по длине в скобках
                            b = 1
                            doska.move(ani2, vkx / 2 * kx, vky / 2 * ky)
                            doska.move(rama3, vkx / 2 * kx, vky / 2 * ky)
                            doska.move(rama4, vkx / 2 * kx, vky / 2 * ky)
                            doska.update()  # обновление
                            time.sleep(0.01)
        # анимация перемещения противника
        # вертикальные фигуры
        elif pole[y_poz_2][x_poz_2] == par_fishki2 and poz3 == 0 and poz4 == 0:
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + 2 * m_pr - 1.5 * ots, fill=svet, tags='DV')
            doska.create_line(x_poz_2 * m_pr + m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + m_pr - ots,
                              y_poz_2 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5, tags='ramaDV')
            doska.create_line(x_poz_2 * m_pr + ots_r, (y_poz_2 + 2) * m_pr - ots, (x_poz_2 + 1) * m_pr - m_pr / 100,
                              y_poz_2 * m_pr + 2 * m_pr - ots, width=m_pr / 12.5, tags='ramaDV2')
            for i in range(abs(x_poz_1 - x_poz_2)):
                if x_poz_2 == 0 or x_poz_2 == 9:
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani2, vkx / 2 * kx, ky)
                        doska.move(rama3, vkx / 2 * kx, ky)
                        doska.move(rama4, vkx / 2 * kx, ky)
                        doska.move('DV', vkx / 2 * kx, ky)
                        doska.move('ramaDV', vkx / 2 * kx, ky)
                        doska.move('ramaDV2', vkx / 2 * kx, ky)
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani2, - vkx / 2 * kx, - ky)
                        doska.move(rama3, - vkx / 2 * kx, - ky)
                        doska.move(rama4, - vkx / 2 * kx, - ky)
                        doska.update()
                        time.sleep(0.01)
                else:
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani2, vkx * kx, ky)
                        doska.move(rama3, vkx * kx, ky)
                        doska.move(rama4, vkx * kx, ky)
                        doska.move('DV', vkx * kx, ky)
                        doska.move('ramaDV', vkx * kx, ky)
                        doska.move('ramaDV2', vkx * kx, ky)
                        doska.update()
                        time.sleep(0.01)
        # анимация разбивания квадрата противника
        elif pole[y_poz_2][x_poz_2] == par_kvadro_vert and poz3 == 0 and poz4 == 0:
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + 2 * m_pr - 1.5 * ots, fill=svet, tags='DV')
            doska.create_line(x_poz_2 * m_pr + m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + m_pr - ots,
                                          y_poz_2 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5, tags='ramaDV')
            doska.create_line(x_poz_2 * m_pr + ots_r, (y_poz_2 + 2) * m_pr - ots, (x_poz_2 + 1) * m_pr - m_pr / 100,
                                          y_poz_2 * m_pr + 2 * m_pr - ots, width=m_pr / 12.5,
                              tags='ramaDV2')
            for i in range(abs(2)):
                for ii in range(int(m_pr / vrange)):
                    b = 1
                    doska.move(ani2, vkx * kx, ky)
                    doska.move(rama3, vkx * kx, ky)
                    doska.move(rama4, vkx * kx, ky)
                    doska.move('DV', vkx * kx, ky)
                    doska.move('ramaDV', vkx * kx, ky)
                    doska.move('ramaDV2', vkx * kx, ky)
                    doska.update()
                    time.sleep(0.01)
        # фикс если ход не возможен для вертикальных
        elif pole[y_poz_2][x_poz_2] == par_fishki2 and (poz3 != 0 or poz4 != 0):
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + 2 * m_pr - 1.5 * ots, fill=svet)
            doska.create_line(x_poz_2 * m_pr + m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + m_pr - ots,
                              y_poz_2 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5)
            doska.create_line(x_poz_2 * m_pr + ots_r, (y_poz_2 + 2) * m_pr - ots, x_poz_2 * m_pr + m_pr - m_pr / 100,
                              y_poz_2 * m_pr + 2 * m_pr - ots, width=m_pr / 12.5)
        # фикс если ход не возможен для квадратов
        elif pole[y_poz_2][x_poz_2] == par_kvadro_vert and (poz3 != 0 or poz4 != 0):
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + 2 * m_pr - 1.5 * ots, fill=svet)
            doska.create_line(x_poz_2 * m_pr + m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + m_pr - ots,
                              y_poz_2 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5)
            doska.create_line(x_poz_2 * m_pr - m_pr + ots_r, (y_poz_2 + 2) * m_pr - ots, (x_poz_2 + 1) * m_pr - m_pr / 100,
                              y_poz_2 * m_pr + 2 * m_pr - ots, width=m_pr / 12.5)
        # фикс если ход не возможен для горизонтальных
        elif pole[y_poz_2][x_poz_2] == par_fishki:
            doska.create_line(x_poz_2 * m_pr + ots_r, y_poz_2 * m_pr + m_pr - ots, (x_poz_2 + 2) * m_pr - m_pr / 100,
                              y_poz_2 * m_pr + m_pr - ots, width=m_pr / 12.5)  # рамка
            doska.create_line(x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + 2 * m_pr - ots,
                              y_poz_2 * m_pr + m_pr - m_pr / 100, width=m_pr / 12.5)  # рамка
            doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                   y_poz_2 * m_pr + m_pr - 1.5 * ots, fill=svet)
        # анимация угла для вертикальных фигур
        elif pole[y_poz_2][x_poz_2] == 17:
            if x_poz_1 == 0:
                if y_poz_2 == 9:  # левый низ
                    poz_ugla = pole[y_poz_1 + 2][x_poz_1 + 1]
                    poz_ugla2 = pole[y_poz_1 + 2][x_poz_1 + 2]
                elif y_poz_2 == 0:  # левый верх
                    poz_ugla = pole[y_poz_1 - 1][x_poz_1 + 1]
                    poz_ugla2 = pole[y_poz_1 - 1][x_poz_1 + 2]
            elif x_poz_1 == 9:
                if y_poz_2 == 9:  # правый низ
                    poz_ugla = pole[y_poz_1 + 2][x_poz_1 - 1]
                    poz_ugla2 = pole[y_poz_1 + 2][x_poz_1 - 2]
                elif y_poz_2 == 0:  # правый верх
                    poz_ugla = pole[y_poz_1 - 1][x_poz_1 - 1]
                    poz_ugla2 = pole[y_poz_1 - 1][x_poz_1 - 2]
            if poz_ugla == 0 and poz_ugla2 == 0:
                for i in range(1):
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani2, kx, vky * ky / 2)
                        doska.move(rama3, kx, vky * ky / 2)
                        doska.move(rama4, kx, vky * ky / 2)
                        doska.update()
                        time.sleep(0.01)
                # для нижнего справа угла
                if y_poz_2 == 9 and x_poz_2 == 9:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots) + vky * ii - m_pr,
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama3, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) + vky * ii - m_pr + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - ots, (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots) - vky * ii, (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama4, (x_poz_2 * m_pr) - vky * ii + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100, (y_poz_2 * m_pr + m_pr - ots))
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani2, -vky * ky / 2, 0)
                            doska.move(rama3, -vky * ky / 2, 0)
                            doska.move(rama4, -vky * ky / 2, 0)
                            doska.update()
                            time.sleep(0.01)
                # для верхнего справа угла
                elif y_poz_2 == 0 and x_poz_2 == 9:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots) - vky * ii + m_pr)
                        doska.coords(rama3, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - ots,
                                     (y_poz_2 * m_pr + m_pr) - vky * ii + m_pr - m_pr / 100)
                        doska.coords(rama4, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) - vky * ii + 2 * m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100,
                                     (y_poz_2 * m_pr + m_pr) - vky * ii + m_pr - ots)
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots) - vky * ii, (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama4, (x_poz_2 * m_pr) - vky * ii + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100, (y_poz_2 * m_pr + m_pr - ots))
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani2, vky * ky / 2, 0)
                            doska.move(rama3, vky * ky / 2, 0)
                            doska.move(rama4, vky * ky / 2, 0)
                            doska.update()
                            time.sleep(0.01)
                # для нижнего слева угла
                if y_poz_2 == 9 and x_poz_2 == 0:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots) - m_pr + vky * ii,
                                     (x_poz_2 * m_pr + m_pr - 1.5 * ots), (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama3, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) - m_pr + vky * ii + ots_r,
                                     (x_poz_2 * m_pr + m_pr - ots), (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr + vky * ii,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama3, (x_poz_2 * m_pr) + vky * ii + m_pr - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr + vky * ii - ots,
                                     (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.coords(rama4, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr + vky * ii - m_pr / 100,
                                     (y_poz_2 * m_pr + m_pr - ots))
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani2, vky * ky / 2, 0)
                            doska.move(rama3, vky * ky / 2, 0)
                            doska.move(rama4, vky * ky / 2, 0)
                            doska.update()
                            time.sleep(0.01)
                # для верхнего слева угла
                if y_poz_2 == 0 and x_poz_2 == 0:
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots) - vky * ii + m_pr)
                        doska.coords(rama3, (x_poz_2 * m_pr) + m_pr - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - ots,
                                     (y_poz_2 * m_pr + m_pr) - vky * ii + m_pr - m_pr / 100)
                        doska.coords(rama4, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) - vky * ii + 2 * m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr - m_pr / 100,
                                     (y_poz_2 * m_pr + m_pr) - vky * ii + m_pr - ots)
                        doska.update()
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange + 1)):
                        doska.coords(ani2, (x_poz_2 * m_pr + ots), (y_poz_2 * m_pr + ots),
                                     (x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots) - m_pr + vky * ii,
                                     (y_poz_2 * m_pr + m_pr - 1.5 * ots))
                        doska.coords(rama3, (x_poz_2 * m_pr) + m_pr + vky * ii - ots, (y_poz_2 * m_pr) + ots_r,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr + vky * ii - ots,
                                     (y_poz_2 * m_pr + m_pr - m_pr / 100))
                        doska.coords(rama4, (x_poz_2 * m_pr) + ots_r, (y_poz_2 * m_pr) + m_pr - ots,
                                     (x_poz_2 * m_pr + 2 * m_pr) - m_pr + vky * ii - m_pr / 100,
                                     (y_poz_2 * m_pr + m_pr - ots))
                        doska.update()
                        time.sleep(0.01)
                    for i in range(1):
                        for ii in range(int(m_pr / vrange)):
                            b = 1
                            doska.move(ani2, -vky * ky / 2, 0)
                            doska.move(rama3, -vky * ky / 2, 0)
                            doska.move(rama4, -vky * ky / 2, 0)
                            doska.update()
                            time.sleep(0.01)
    # для квадратов
    elif z == 9 or z == 13 or z == 11 or z == 15:
        dv = dv1 = dv2 = -1
        if x_poz_2 == 2 or x_poz_2 == 4 or x_poz_2 == 6 or x_poz_2 == 8:  # корректировка смещения точки выбора
            x_poz_2 = x_poz_2 - 1
        if y_poz_2 == 2 or y_poz_2 == 4 or y_poz_2 == 6 or y_poz_2 == 8:  # корректировка смещения точки выбора
            y_poz_2 = y_poz_2 - 1
        if f_hi == 1:
            if pole[y_poz_2][x_poz_2] == 13:
                par_kvadro = 13
            elif pole[y_poz_2][x_poz_2] == 15:
                par_kvadro = 15
        elif f_hi == 0 or f_hi == 2:
            if pole[y_poz_2][x_poz_2] == 9:
                par_kvadro = 9
            elif pole[y_poz_2][x_poz_2] == 11:
                par_kvadro = 11
        # определение векторов для хода
        if x_poz_1 == x_poz_2:
            kx = 0
            vector_kv = 1
            if y_poz_1 < y_poz_2:
                ky = 1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    # определение свободного места для каждого вектора
                    poz3 = pole[y_poz_2 + 2][x_poz_2]  # верхняя левая
                    poz4 = pole[y_poz_2 + 2][x_poz_2 + 1] # верхняя правая
                    if y_poz_2 != 7 and y_poz_2 != 2:
                        poz5 = pole[y_poz_2 + 3][x_poz_2]# нижняя левая
                        poz33 = pole[y_poz_2 + 3][x_poz_2]
                        poz44 = pole[y_poz_2 + 3][x_poz_2 + 1]
            elif y_poz_1 > y_poz_2:
                ky = -1
                if y_poz_2 != 9 and y_poz_2 != 0:
                    poz3 = pole[y_poz_2 - 1][x_poz_2]
                    poz4 = pole[y_poz_2 - 1][x_poz_2 + 1]
                    if y_poz_2 != 7 and y_poz_2 != 2:
                        poz5 = pole[y_poz_2 - 2][x_poz_2]
                        poz33 = pole[y_poz_2 - 2][x_poz_2]
                        poz44 = pole[y_poz_2 - 2][x_poz_2 + 1]
        elif y_poz_1 == y_poz_2:
            ky = 0
            vector_kv = 1
            if x_poz_1 < x_poz_2:
                kx = 1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = pole[y_poz_2][x_poz_2 + 2]
                    poz4 = pole[y_poz_2 + 1][x_poz_2 + 2]
                    if x_poz_2 != 7 and x_poz_2 != 2:
                        poz5 = pole[y_poz_2][x_poz_2 + 3]
                        poz33 = pole[y_poz_2][x_poz_2 + 3]
                        poz44 = pole[y_poz_2 + 1][x_poz_2 + 3]
            elif x_poz_1 > x_poz_2:
                kx = -1
                if x_poz_2 != 9 and x_poz_2 != 0:
                    poz3 = pole[y_poz_2][x_poz_2 - 1]
                    poz4 = pole[y_poz_2 + 1][x_poz_2 - 1]
                    if x_poz_2 != 7 and x_poz_2 != 2:
                        poz5 = pole[y_poz_2][x_poz_2 - 2]
                        poz33 = pole[y_poz_2][x_poz_2 - 2]
                        poz44 = pole[y_poz_2 + 1][x_poz_2 - 2]
        # после того как нашли коэффиценты
        if abs(x_poz_1 - x_poz_2) < 3 and abs(y_poz_1 - y_poz_2) < 3 and kx != 10 and ky != 10:  # ход не дальше 3
            if y_poz_2 != 9 and x_poz_2 != 9 and y_poz_2 != 0 and x_poz_2 != 0:
                # если гор фишка сверху куба
                if pole[y_poz_2][x_poz_2] == par_fishki:
                    if pole[y_poz_2 + 1][x_poz_2] == 0 and poz3 == 0 and poz4 == 0:
                        doska.create_rectangle(x_poz_2 * m_pr + 3, y_poz_2 * m_pr + 3, x_poz_2 * m_pr + 2 * m_pr - 3,
                                               y_poz_2 * m_pr + m_pr - 3, fill=svet, tags='DV')
                        doska.create_line(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + m_pr, x_poz_2 * m_pr + 2 * m_pr,
                                          y_poz_2 * m_pr + m_pr, width=4, tags='ramaDV')
                        doska.create_line(x_poz_2 * m_pr + 2 * m_pr, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + 2 * m_pr,
                                          y_poz_2 * m_pr + m_pr, width=4, tags='ramaDV2')
                        if ky == -1:  # исключения для красоты :3
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                        else:  # остальные случаи
                            for i in range(abs(2)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif pole[y_poz_2 + 1][x_poz_2] == 0 and (poz3 != 0 or poz4 != 0):
                        doska.create_rectangle(x_poz_2 * m_pr + 3, y_poz_2 * m_pr + 3, x_poz_2 * m_pr + 2 * m_pr - 3,
                                               y_poz_2 * m_pr + m_pr - 3, fill=svet)
                # если гор фишка снизу куба
                elif pole[y_poz_2 + 1][x_poz_2] == par_fishki:
                    if pole[y_poz_2][x_poz_2] == 0 and poz3 == 0 and poz4 == 0:
                        doska.create_rectangle(x_poz_2 * m_pr + 3, y_poz_2 * m_pr + 3 + m_pr,
                                               x_poz_2 * m_pr + 2 * m_pr - 3, y_poz_2 * m_pr + m_pr - 3 + m_pr,
                                               fill=svet, tags='DV')
                        doska.create_line(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + 2 * m_pr, x_poz_2 * m_pr + 2 * m_pr,
                                          y_poz_2 * m_pr + 2 * m_pr, width=4, tags='ramaDV')
                        doska.create_line(x_poz_2 * m_pr + 2 * m_pr, y_poz_2 * m_pr + ots + m_pr,
                                          x_poz_2 * m_pr + 2 * m_pr, y_poz_2 * m_pr + m_pr + m_pr, width=4,
                                          tags='ramaDV2')
                        if ky == 1:
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                        else:
                            for i in range(abs(2)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif pole[y_poz_2][x_poz_2] == 0 and (poz3 != 0 or poz4 != 0):
                        doska.create_rectangle(x_poz_2 * m_pr + 3, y_poz_2 * m_pr + 3 + m_pr,
                                               x_poz_2 * m_pr + 2 * m_pr - 3,
                                               y_poz_2 * m_pr + m_pr - 3 + m_pr, fill=svet)
                # если верт фишка слева куба
                elif pole[y_poz_2][x_poz_2] == par_fishki2:
                    if pole[y_poz_2][x_poz_2 + 1] == 0 and poz3 == 0 and poz4 == 0:
                        doska.create_rectangle(x_poz_2 * m_pr + 3, y_poz_2 * m_pr + 3, x_poz_2 * m_pr + m_pr - 3,
                                               y_poz_2 * m_pr + 2 * m_pr - 3, fill=svet, tags='DV')
                        doska.create_line(x_poz_2 * m_pr + m_pr, y_poz_2 * m_pr + ots, x_poz_2 * m_pr + m_pr,
                                          y_poz_2 * m_pr + 2 * m_pr, width=4, tags='ramaDV')
                        doska.create_line(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + 2 * m_pr, x_poz_2 * m_pr + m_pr,
                                          y_poz_2 * m_pr + 2 * m_pr, width=4, tags='ramaDV2')
                        if kx == -1:  # исключения для красоты :3
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                        else:  # остальные случаи
                            for i in range(abs(2)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif pole[y_poz_2][x_poz_2 + 1] == 0 and (poz3 != 0 or poz5 != 0):
                        doska.create_rectangle(x_poz_2 * m_pr + 3, y_poz_2 * m_pr + 3, x_poz_2 * m_pr + m_pr - 3,
                                               y_poz_2 * m_pr + 2 * m_pr - 3, fill=svet)
                # если верт фишка справа куба
                elif pole[y_poz_2][x_poz_2 + 1] == par_fishki2:
                    if pole[y_poz_2][x_poz_2] == 0 and poz3 == 0 and poz4 == 0:
                        doska.create_rectangle(x_poz_2 * m_pr + 3 + m_pr, y_poz_2 * m_pr + 3,
                                               x_poz_2 * m_pr + m_pr - 3 + m_pr, y_poz_2 * m_pr + 2 * m_pr - 3,
                                               fill=svet, tags='DV')
                        doska.create_line((x_poz_2+1) * m_pr + m_pr, y_poz_2 * m_pr + ots, (x_poz_2+1) * m_pr + m_pr,
                                          y_poz_2 * m_pr + 2 * m_pr, width=4, tags='ramaDV')
                        doska.create_line((x_poz_2+1) * m_pr + ots, y_poz_2 * m_pr + 2 * m_pr, (x_poz_2+1) * m_pr + m_pr,
                                          y_poz_2 * m_pr + 2 * m_pr, width=4, tags='ramaDV2')
                        if kx == 1:  # исключения для красоты :3
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                            for i in range(abs(1)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                        else:  # остальные случаи
                            for i in range(abs(2)):
                                for ii in range(int(m_pr / vrange)):
                                    b = 1
                                    doska.move(ani3, vkx * kx, vky * ky)
                                    doska.move(ani4, vkx * kx, vky * ky)
                                    doska.move(ramakub1, vkx * kx, vky * ky)
                                    doska.move(ramakub2, vkx * kx, vky * ky)
                                    doska.move('DV', vkx * kx, vky * ky)
                                    doska.move('ramaDV', vkx * kx, vky * ky)
                                    doska.move('ramaDV2', vkx * kx, vky * ky)
                                    doska.update()  # обновление
                                    time.sleep(0.01)
                    # fix
                    elif pole[y_poz_2][x_poz_2] == 0 and (poz3 != 0 or poz5 != 0):
                        doska.create_rectangle(x_poz_2 * m_pr + 3 + m_pr, y_poz_2 * m_pr + 3,
                                               x_poz_2 * m_pr + m_pr - 3 + m_pr, y_poz_2 * m_pr + 2 * m_pr - 3,
                                               fill=svet)
                # если пусто место для хода
                elif pole[y_poz_2][x_poz_2] == 0 and vector_kv == 1:
                    if pole[y_poz_2 + 1][x_poz_2] == 0 and pole[y_poz_2][x_poz_2 + 1] == 0:
                        for i in range(abs(2)):
                            for ii in range(int(m_pr / vrange)):
                                b = 1
                                doska.move(ani3, vkx * kx, vky * ky)
                                doska.move(ani4, vkx * kx, vky * ky)
                                doska.move(ramakub1, vkx * kx, vky * ky)
                                doska.move(ramakub2, vkx * kx, vky * ky)
                                doska.update()  # обновление
                                time.sleep(0.01)
                # если квадрат противника
                elif pole[y_poz_2][x_poz_2] == par_kvadro:  # and poz3 ==  poz4 == poz33 == poz44
                    list_k = [1, 7]
                    kub_par = 0
                    doska.create_line(x_poz_2 * m_pr + ots_r, y_poz_2 * m_pr + 2 * m_pr - ots + 1,
                                      x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + 2 * m_pr - ots + 1,
                                      width=m_pr / 15.2, tags='ramaDV')
                    doska.create_line(x_poz_2 * m_pr + 2 * m_pr - ots + 1, y_poz_2 * m_pr + ots_r,
                                      x_poz_2 * m_pr + 2 * m_pr - ots + 1, y_poz_2 * m_pr + 2 * m_pr - m_pr / 200,
                                      width=m_pr / 15.2, tags='ramaDV2')
                    if pole[y_poz_2][x_poz_2] == 9 or pole[y_poz_2][x_poz_2] == 13:
                        dv2 = pole[y_poz_2][x_poz_2]
                        dv = doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots,
                                                    x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                                    y_poz_2 * m_pr + m_pr - 1.5 * ots,
                                                    fill=svet)
                        dv1 = doska.create_rectangle(x_poz_2 * m_pr + ots, (y_poz_2 + 1) * m_pr + ots,
                                                     x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                                     (y_poz_2 + 1) * m_pr + m_pr - 1.5 * ots, fill=svet)
                    elif pole[y_poz_2][x_poz_2] == 11 or pole[y_poz_2][x_poz_2] == 15:
                        dv2 = pole[y_poz_2][x_poz_2]
                        dv = doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots,
                                                    x_poz_2 * m_pr + m_pr - 1.5 * ots,
                                                    y_poz_2 * m_pr + 2 * m_pr - 1.5 * ots,
                                                    fill=svet)
                        dv1 = doska.create_rectangle((x_poz_2 + 1) * m_pr + ots, y_poz_2 * m_pr + ots,
                                                     (x_poz_2 + 1) * m_pr + m_pr - 1.5 * ots,
                                                     y_poz_2 * m_pr + 2 * m_pr - 1.5 * ots, fill=svet)

                    if (dv2 == par_kvadro_gor or dv2 == par_kvadro_vert) and poz3 == poz4 == poz33 == poz44:
                        kub_par = 1
                    elif (dv2 == par_kvadro_gor or dv2 == par_kvadro_vert) and poz3 == poz4 == 0\
                            and (y_poz_2 in list_k or x_poz_2 in list_k):
                        kub_par = 1
                    if kub_par:
                        for i in range(abs(2)):
                            for ii in range(int(m_pr / vrange)):
                                b = 1
                                doska.move(ani3, vkx * kx, vky * ky)
                                doska.move(ani4, vkx * kx, vky * ky)
                                doska.move(ramakub1, vkx * kx, vky * ky)
                                doska.move(ramakub2, vkx * kx, vky * ky)
                                doska.move(dv, vkx * kx, vky * ky)
                                doska.move(dv1, vkx * kx, vky * ky)
                                doska.move('ramaDV', vkx * kx, vky * ky)
                                doska.move('ramaDV2', vkx * kx, vky * ky)
                                doska.update()  # обновление
                                time.sleep(0.01)
            # если гор фишка на базе
            elif pole[y_poz_2][x_poz_2] == par_fishki and (y_poz_2 == 9 or y_poz_2 == 0):
                doska.create_rectangle(x_poz_2 * m_pr + ots, y_poz_2 * m_pr + ots,
                                       x_poz_2 * m_pr + 2 * m_pr - 1.5 * ots, y_poz_2 * m_pr + m_pr - 1.5 * ots,
                                       fill=svet, tags='DV')
                doska.create_line(x_poz_2 * m_pr + ots_r, y_poz_2 * m_pr + m_pr - ots,
                                  x_poz_2 * m_pr + 2 * m_pr - m_pr / 100, y_poz_2 * m_pr + m_pr - ots,
                                  width=m_pr / 12.5, tags='ramaDV')
                doska.create_line(x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + ots_r,
                                  x_poz_2 * m_pr + 2 * m_pr - ots, y_poz_2 * m_pr + m_pr - m_pr / 100,
                                  width=m_pr / 12.5, tags='ramaDV2')
                for i in range(abs(1)):
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani3, vkx * kx, vky * ky)
                        doska.move(ani4, vkx * kx, vky * ky)
                        doska.move(ramakub1, vkx * kx, vky * ky)
                        doska.move(ramakub2, vkx * kx, vky * ky)
                        doska.move('DV', vkx * kx, vky * ky)
                        doska.move('ramaDV', vkx * kx, vky * ky)
                        doska.move('ramaDV2', vkx * kx, vky * ky)
                        doska.update()  # обновление
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani3, -vkx * kx, -vky * ky)
                        doska.move(ani4, -vkx * kx, -vky * ky)
                        doska.move(ramakub1, -vkx * kx, -vky * ky)
                        doska.move(ramakub2, -vkx * kx, -vky * ky)
                        doska.update()  # обновление
                        time.sleep(0.01)
            # если верт фишка на базе
            elif pole[y_poz_2][x_poz_2] == par_fishki2 and (x_poz_2 == 9 or x_poz_2 == 0):
                doska.create_rectangle(x_poz_2 * m_pr + 3, y_poz_2 * m_pr + 3, x_poz_2 * m_pr + m_pr - 3,
                                       y_poz_2 * m_pr + 2 * m_pr - 3, fill=svet, tags='DV')
                doska.create_line(x_poz_2 * m_pr + m_pr - ots, y_poz_2 * m_pr + ots_r, x_poz_2 * m_pr + m_pr - ots,
                                  y_poz_2 * m_pr + 2 * m_pr - m_pr / 100, width=m_pr / 12.5, tags='ramaDV')
                doska.create_line(x_poz_2 * m_pr + ots_r, y_poz_2 * m_pr + 2 * m_pr - ots,
                                  x_poz_2 * m_pr + m_pr - m_pr / 100, y_poz_2 * m_pr + 2 * m_pr - ots,
                                  width=m_pr / 12.5, tags='ramaDV2')
                for i in range(abs(1)):
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani3, vkx * kx, vky * ky)
                        doska.move(ani4, vkx * kx, vky * ky)
                        doska.move(ramakub1, vkx * kx, vky * ky)
                        doska.move(ramakub2, vkx * kx, vky * ky)
                        doska.move('DV', vkx * kx, vky * ky)
                        doska.move('ramaDV', vkx * kx, vky * ky)
                        doska.move('ramaDV2', vkx * kx, vky * ky)
                        doska.update()  # обновление
                        time.sleep(0.01)
                    for ii in range(int(m_pr / vrange)):
                        b = 1
                        doska.move(ani3, -vkx * kx, -vky * ky)
                        doska.move(ani4, -vkx * kx, -vky * ky)
                        doska.move(ramakub1, -vkx * kx, -vky * ky)
                        doska.move(ramakub2, -vkx * kx, -vky * ky)
                        doska.update()  # обновление
                        time.sleep(0.01)


# выбор клетки для хода 1
def pozici_1(event):
    global poz1_x, poz1_y
    global f1,f12,f2,f22,f3,f33,f4,f44
    x, y = event.x // int(m_pr), event.y // int(m_pr)  # вычисляем координаты клетки
    spisok_k = [2, 4, 6, 8]
    spisok_k1 = [1, 3, 5, 7]
    # функция рамки квадратов
    if f_hi ==1:
        f1 = 1
        f12 = 5
        f2 = 2
        f22 = 7
        f3 = 9
        f33 = 10
        f4 = 11
        f44 = 12
    elif f_hi == 2 or f_hi == 0:
        f1 = 3
        f12 = 6
        f2 = 4
        f22 = 8
        f3 = 13
        f33 = 14
        f4 = 15
        f44 = 16
    def ramka_sokr(x, y, poz1_y, poz1_x):  # что бы не писать код дважды
        if 0 < x < 9 and 0 < y < 9:
            if (y == poz1_y and x == poz1_x - 2) or (y == poz1_y - 2 and x == poz1_x) or (
                    y == poz1_y and x == poz1_x + 2) \
                    or (y == poz1_y + 2 and x == poz1_x):
                if pole[y][x] == 0 and pole[y + 1][x] == 0 and pole[y][x + 1] == 0 and pole[y + 1][x + 1] == 0:
                    doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3,
                                 y * m_pr + 2 * m_pr - 3)
            elif (y == poz1_y and x == poz1_x - 1) or (y == poz1_y - 2 and x == poz1_x + 1) or (
                    y == poz1_y and x == poz1_x + 3) \
                    or (y == poz1_y + 2 and x == poz1_x + 1):
                if pole[y][x] == 0 and pole[y + 1][x] == 0 and pole[y][x - 1] == 0 and pole[y + 1][x - 1] == 0:
                    doska.coords(zel_ramka, x * m_pr + 3 - m_pr, y * m_pr + 3, x * m_pr + 2 * m_pr - 3 - m_pr,
                                 y * m_pr + 2 * m_pr - 3)
            elif (y == poz1_y + 1 and x == poz1_x - 2) or (y == poz1_y - 1 and x == poz1_x) or (
                    y == poz1_y + 1 and x == poz1_x + 2) \
                    or (y == poz1_y + 3 and x == poz1_x):
                if pole[y][x] == 0 and pole[y - 1][x] == 0 and pole[y][x + 1] == 0 and pole[y - 1][x + 1] == 0:
                    doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3 - m_pr, x * m_pr + 2 * m_pr - 3,
                                 y * m_pr + 2 * m_pr - 3 - m_pr)
            elif (y == poz1_y + 1 and x == poz1_x - 1) or (y == poz1_y - 1 and x == poz1_x + 1) or (
                    y == poz1_y + 1 and x == poz1_x + 3) \
                    or (y == poz1_y + 3 and x == poz1_x + 1):
                if pole[y][x] == 0 and pole[y - 1][x] == 0 and pole[y][x - 1] == 0 and pole[y - 1][x - 1] == 0:
                    doska.coords(zel_ramka, x * m_pr + 3 - m_pr, y * m_pr + 3 - m_pr,
                                 x * m_pr + 2 * m_pr - 3 - m_pr, y * m_pr + 2 * m_pr - 3 - m_pr)

    # создание рамок для фигур
    if x < 10 and y < 10:  # ограничение области для исключений
        # рамка для горизонта фишек
        if pole[y][x] == 1 or pole[y][x] == 5 or pole[y][x] == 3 or pole[y][x] == 6:
            if pole[y][x] == 5 or pole[y][x] == 6:
                x = x - 1
            doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3, y * m_pr + m_pr - 3)
        # рамка для верт фишек
        elif pole[y][x] == 2 or pole[y][x] == 7 or pole[y][x] == 4 or pole[y][x] == 8:
            if pole[y][x] == 7 or pole[y][x] == 8:
                y = y - 1
            doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + m_pr - 3, y * m_pr + 2 * m_pr - 3)
        # квадраты горизонт
        elif pole[y][x] == 9 or pole[y][x] == 10 or pole[y][x] == 13 or pole[y][x] == 14:
            if pole[y][x] == 10 or pole[y][x] == 14:
                x = x - 1
            if pole[y][x] == pole[y - 1][x] and y in spisok_k:
                y = y - 1
            doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3, y * m_pr + 2 * m_pr - 3)
        # квадраты вертикаль
        elif pole[y][x] == 11 or pole[y][x] == 12 or pole[y][x] == 15 or pole[y][x] == 16:
            if pole[y][x] == 12 or pole[y][x] == 16:
                y = y - 1
            if pole[y][x] == pole[y][x - 1] and x in spisok_k:
                x = x - 1
            doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3, y * m_pr + 2 * m_pr - 3)
        # рамка хода для горизонтальных одиночных фишек игрока
        elif pole[poz1_y][poz1_x] == f1 or pole[poz1_y][poz1_x] == f12:
            if pole[poz1_y][poz1_x] == f12 and pole[poz1_y][poz1_x - 1] == f1:
                poz1_x = poz1_x - 1
            if (y == poz1_y + 1 and x == poz1_x) or (y == poz1_y + 1 and x == poz1_x + 1) or (
                    y == poz1_y - 1 and x == poz1_x + 1) \
                    or (y == poz1_y - 1 and x == poz1_x) or (y == poz1_y and x == poz1_x - 2) or (
                    y == poz1_y and x == poz1_x - 1) \
                    or (y == poz1_y and x == poz1_x + 2) or (y == poz1_y and x == poz1_x + 3):
                if x in spisok_k:
                    if pole[y][x - 1] == 0 and pole[y][x] == 0:
                        doska.coords(zel_ramka, x * m_pr + 3 - m_pr, y * m_pr + 3, x * m_pr + 2 * m_pr - 3 - m_pr,
                                     y * m_pr + m_pr - 3)
                elif x in spisok_k1:
                    if pole[y][x] == 0 and pole[y][x + 1] == 0:
                        doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3,
                                     y * m_pr + m_pr - 3)
        # рамка хода для вертикальных одиночных фишек игрока
        elif pole[poz1_y][poz1_x] == f2 or pole[poz1_y][poz1_x] == f22:
            if pole[poz1_y][poz1_x] == f22 and pole[poz1_y - 1][poz1_x] == f2:
                poz1_y = poz1_y - 1
            if (y == poz1_y + 2 and x == poz1_x) or (y == poz1_y + 3 and x == poz1_x) or (
                    y == poz1_y - 1 and x == poz1_x) or \
                    (y == poz1_y - 2 and x == poz1_x) or (y == poz1_y and x == poz1_x - 1) or (
                    y == poz1_y + 1 and x == poz1_x - 1) or \
                    (y == poz1_y + 1 and x == poz1_x + 1) or (y == poz1_y and x == poz1_x + 1):
                if y in spisok_k:
                    if pole[y - 1][x] == 0 and pole[y][x] == 0:  # (pole[y][x] == 0 and pole[y + 1][x] == 0) or
                        doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3 - m_pr, x * m_pr + m_pr - 3,
                                     y * m_pr + 2 * m_pr - 3 - m_pr)
                elif y in spisok_k1:
                    if pole[y][x] == 0 and pole[y + 1][x] == 0:
                        doska.coords(zel_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + m_pr - 3,
                                     y * m_pr + 2 * m_pr - 3)
        # рамка хода для горизонтальных квадратов игрока
        elif pole[poz1_y][poz1_x] == f3 or pole[poz1_y][poz1_x] == f33:
            if pole[poz1_y][poz1_x] == f33:
                poz1_x = poz1_x - 1
            if pole[poz1_y][poz1_x] == pole[poz1_y - 1][poz1_x] == f3 and poz1_y in spisok_k:
                poz1_y = poz1_y - 1
            ramka_sokr(x, y, poz1_y, poz1_x)
        # рамка хода для вертикальных квадратов игрока
        elif pole[poz1_y][poz1_x] == f4 or pole[poz1_y][poz1_x] == f44:
            if pole[poz1_y][poz1_x] == f44:
                poz1_y = poz1_y - 1
            if pole[poz1_y][poz1_x] ==  pole[poz1_y][poz1_x - 1] == f4 and poz1_x in spisok_k:
                poz1_x = poz1_x - 1
            ramka_sokr(x, y, poz1_y, poz1_x)


# выбор клетки для хода 2
def pozici_2(event):
    global poz1_x, poz1_y, poz2_x, poz2_y
    global f_hi
    global kub

    if (f_hi == 1 or f_hi==2) and b == 0:# ход игрока и параметр b запрещает дублировать анимацию хода, если тот сделан
        x, y = event.x // int(m_pr), event.y // int(m_pr)  # вычисляем координаты клетки
        if kub:
            # рамка выбора горизонт фигуры игрока
            if x < 10 and y < 10:  # fix щелчка за игровое поле
                if pole[y][x] == f1 or pole[y][x] == f12:
                    if pole[y][x] == f12:
                        x = x - 1
                    doska.coords(kr_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3,
                                 y * m_pr + m_pr - 3)  # рамка в выбранной клетке
                    poz1_x, poz1_y = x, y
                # рамка выбора вертикальных фигур игрока
                elif pole[y][x] == f2 or pole[y][x] == f22:
                    if pole[y][x] == f22:
                        y = y - 1
                    doska.coords(kr_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + m_pr - 3,
                                 y * m_pr + 2 * m_pr - 3)  # рамка в выбранной клетке
                    poz1_x, poz1_y = x, y
                # квадраты игрока
                elif pole[y][x] == f3 or pole[y][x] == f33:
                    if pole[y][x] == f33:
                        x = x - 1
                    if pole[y][x] == pole[y - 1][x] and (y == 2 or y == 4 or y == 6 or y == 8):
                        y = y - 1
                    doska.coords(kr_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3, y * m_pr + 2 * m_pr - 3)
                    poz1_x, poz1_y = x, y
                elif pole[y][x] == f4 or pole[y][x] == f44:
                    if pole[y][x] == f44:
                        y = y - 1
                    if pole[y][x] == pole[y][x - 1] and (x == 2 or x == 4 or x == 6 or x == 8):
                        x = x - 1
                    doska.coords(kr_ramka, x * m_pr + 3, y * m_pr + 3, x * m_pr + 2 * m_pr - 3, y * m_pr + 2 * m_pr - 3)
                    poz1_x, poz1_y = x, y
                # когда выбрана фигура делаем ход
                else:
                    if poz1_x != -1:  # клетка выбрана
                        poz2_x, poz2_y = x, y
                        if kub > 0:
                            k_pole = copy.deepcopy(pole)
                            hod(poz1_x, poz1_y, poz2_x, poz2_y)
                            doska.update()
                            if k_pole != pole:
                                kub -= 1
                                the_end()
                        poz1_x = -1  # клетка не выбрана
                        doska.coords(kr_ramka, -5, -5, -5, -5)  # рамка вне поля
        if kub == 0:  # закончился ход
            if f_hi == 1 and rad == 2: # игра с игроком
                f_hi = 2
            elif f_hi == 1 and rad == 1: # игра с компьютером
                f_hi = 0
            elif f_hi == 2: # игра с игроком
                f_hi = 1
            opredel_hoda(f_hi)


# Переход хода
def opredel_hoda(f_hi):
    global kubiki
    global a
    global kub
    a = 1
    kub = random.randint(1, 6)
    u = mashtab / 10
    doska.update()
    fon.update()
    fon.delete('all')
    fon.create_rectangle(int(1.14 * mashtab), int(0.34 * mashtab), int(1.56 * mashtab), int(0.76 * mashtab), fill='black',
                         outline="black")  # белый фон
    fon.create_rectangle(int(1.15 * mashtab), int(0.35 * mashtab), int(1.55 * mashtab), int(0.75 * mashtab),
                         fill='white', outline="black")  # фон куба
    # кубик
    if kub:
        if f_hi == 1:
            svet = 'red'
        elif f_hi == 0 or f_hi == 2:
            svet = 'green'

        if kub == 1:
            fon.create_oval(int(1.30 * mashtab), int(0.50 * mashtab), int(1.40 * mashtab), int(0.60 * mashtab), fill=svet,
                            outline="black")  # выпало 1
        elif kub == 2:
            fon.create_oval(int(1.21 * mashtab), int(0.50 * mashtab), int(1.31 * mashtab), int(0.60 * mashtab), fill=svet,
                            outline="black")  # выпало 2
            fon.create_oval(int(1.39 * mashtab), int(0.50 * mashtab), int(1.49 * mashtab), int(0.60 * mashtab), fill=svet,
                            outline="black")
        elif kub == 3:
            fon.create_oval(int(1.17 * mashtab), int(0.63 * mashtab), int(1.27 * mashtab), int(0.73 * mashtab), fill=svet,
                            outline="black")  # выпало 3
            fon.create_oval(int(1.30 * mashtab), int(0.50 * mashtab), int(1.40 * mashtab), int(0.60 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.43 * mashtab), int(0.37 * mashtab), int(1.53 * mashtab), int(0.47 * mashtab), fill=svet,
                            outline="black")
        elif kub == 4:
            fon.create_oval(int(1.21 * mashtab), int(0.60 * mashtab), int(1.31 * mashtab), int(0.70 * mashtab), fill=svet,
                            outline="black")  # выпало 4
            fon.create_oval(int(1.39 * mashtab), int(0.60 * mashtab), int(1.49 * mashtab), int(0.70 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.21 * mashtab), int(0.40 * mashtab), int(1.31 * mashtab), int(0.50 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.39 * mashtab), int(0.40 * mashtab), int(1.49 * mashtab), int(0.50 * mashtab), fill=svet,
                            outline="black")
        elif kub == 5:
            fon.create_oval(int(1.30 * mashtab), int(0.50 * mashtab), int(1.40 * mashtab), int(0.60 * mashtab), fill=svet,
                            outline="black")  # выпало 5
            fon.create_oval(int(1.21 * mashtab), int(0.60 * mashtab), int(1.31 * mashtab), int(0.70 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.39 * mashtab), int(0.60 * mashtab), int(1.49 * mashtab), int(0.70 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.21 * mashtab), int(0.40 * mashtab), int(1.31 * mashtab), int(0.50 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.39 * mashtab), int(0.40 * mashtab), int(1.49 * mashtab), int(0.50 * mashtab), fill=svet,
                            outline="black")
        elif kub == 6:
            fon.create_oval(int(1.17 * mashtab), int(0.60 * mashtab), int(1.27 * mashtab), int(0.70 * mashtab), fill=svet,
                            outline="black")  # выпало 6
            fon.create_oval(int(1.30 * mashtab), int(0.60 * mashtab), int(1.40 * mashtab), int(0.70 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.43 * mashtab), int(0.60 * mashtab), int(1.53 * mashtab), int(0.70 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.17 * mashtab), int(0.40 * mashtab), int(1.27 * mashtab), int(0.50 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.30 * mashtab), int(0.40 * mashtab), int(1.40 * mashtab), int(0.50 * mashtab), fill=svet,
                            outline="black")
            fon.create_oval(int(1.43 * mashtab), int(0.40 * mashtab), int(1.53 * mashtab), int(0.50 * mashtab), fill=svet,
                            outline="black")

    if f_hi == 0:
        fon.create_text(int(1.35 * mashtab), int(0.2 * mashtab), text='ХОД КОМПЬЮТЕРА', justify=CENTER,
                        font=f'Helvetica 30 bold',fill='black')
        fon.create_text(int(1.35 * mashtab), int(0.26 * mashtab), text=kub, justify=CENTER,
                        font=f'Verdana {int(u / 2.5)}',fill='black')
        if kub:
            hod_comp(kub)

    elif f_hi == 1:  # ход игрока
        fon.create_text(int(1.35 * mashtab), int(0.2 * mashtab), text='ХОД ИГРОКА', justify=CENTER,
                        font=f'Helvetica 30 bold',fill='black')
        fon.create_text(int(1.35 * mashtab), int(0.26 * mashtab), text=kub, justify=CENTER,
                        font=f'Aesthetic {int(u / 2.5)}',fill='black')
        if kub:
            doska.bind("<Button-1>", pozici_2)
    elif f_hi == 2:  # ход второго игрока
        fon.create_text(int(1.35 * mashtab), int(0.2 * mashtab), text='ХОД ВТОРОГО ИГРОКА', justify=CENTER,
                        font=f'Helvetica 30 bold',fill='black')
        fon.create_text(int(1.35 * mashtab), int(0.26 * mashtab), text=kub, justify=CENTER,
                        font=f'Aesthetic {int(u / 2.5)}',fill='black')
        if kub:
            doska.bind("<Button-1>", pozici_2)


# Распределение ходов
def hod(poz1_x, poz1_y, poz2_x, poz2_y):
    global pole
    global f_hi
    global kub
    global pole

    vivod(poz1_x, poz1_y, poz2_x, poz2_y, 1)  # рисуем игровое поле
    if f_hi == 1 or f_hi == 2:
        if pole[poz1_y][poz1_x] == f1 or pole[poz1_y][poz1_x] == f3:
            pravila_gor(poz1_x, poz1_y, poz2_x, poz2_y)
        elif pole[poz1_y][poz1_x] == f12 and pole[poz1_y][poz1_x - 1] == f1 \
                or pole[poz1_y][poz1_x] == f33 and pole[poz1_y][poz1_x - 1] == f3:
            poz1_x = poz1_x - 1
            pravila_gor(poz1_x, poz1_y, poz2_x, poz2_y)
        elif pole[poz1_y][poz1_x] == f2 or pole[poz1_y][poz1_x] == f4:
            pravila_vert(poz1_x, poz1_y, poz2_x, poz2_y)
        elif pole[poz1_y][poz1_x] == f22 and pole[poz1_y - 1][poz1_x] == f2 \
                or pole[poz1_y][poz1_x] == f44 and pole[poz1_y - 1][poz1_x] == f4:
            poz1_y = poz1_y - 1
            pravila_vert(poz1_x, poz1_y, poz2_x, poz2_y)
    elif f_hi == 0:
        if pole[poz1_y][poz1_x] == 3 or pole[poz1_y][poz1_x] == 13:
            pravila_gor(poz1_x, poz1_y, poz2_x, poz2_y)
        elif pole[poz1_y][poz1_x] == 4 or pole[poz1_y][poz1_x] == 15:
            pravila_vert(poz1_x, poz1_y, poz2_x, poz2_y)
    doska.update()
    vivod(poz1_x, poz1_y, poz2_x, poz2_y, 0)  # рисуем игровое поле после хода


# ход компьютера
def hod_comp(kub1):
    global f_hi, end_game
    global pole, end_p
    end_game = 0
    time.sleep(0.5)
    iz = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, -2], [-2, 0], [0, 2], [2, 0]]
    # print(pole[0], pole[1], pole[2], pole[3], pole[4], pole[5], pole[6], pole[7], pole[8], pole[9], sep='\n')
    end_game = 0
    while kub1 > 0:  # ход компьютера отсюда все ходы кубика
        iy = random.randint(0, 9)  #
        ix = random.randint(0, 9)  # 36 48 1314 1516
        print(end_game,kub1)
        end_game += 1
        list = [13, 15]

        if end_game == 1500:
            soobsenie(3)
            break
        the_end()
        if end_p:
            break


        # если рандом горизонтальная фишка
        if pole[iy][ix] == 3:  # для горизонтальных фишек
            h1 = random.choice((iz[1], iz[3], iz[4], iz[6]))  # рандом хода ↓ 1 ↑ 1  ← 2 → 2
            h2 = random.choice((iz[4], iz[6]))  # ← 2 → 2
            trans = 0
            spisok = [2, 4, 6, 8]
            if kub > 0:
                # ↑ 24 ↓ 25 → 26 ← 27
                # if (rad == 1 or rad == 2 or rad == 3): #проверяем сложность компьютера
                # ходы внизу
                if iy == 9 or iy == 8 or iy == 7:  # ↓
                    # выбивание на базе снизу, поворот на углу и трансформация в куб
                    if iy == 9 or iy == 8:
                        # выбивание если противник слева на базе ↑ ← ↓
                        if pole[iy][ix - 2] == 1 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy - 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy - 1][ix] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy - 1, ix - 2, iy - 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy - 1][ix - 2] == 3:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix - 2, iy - 1, ix - 2, iy)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # выбивание если противник справа на базе ↑ → ↓
                        elif pole[iy][ix + 2] == 1 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy - 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy - 1][ix] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy - 1, ix + 2, iy - 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy - 1][ix + 2] == 3:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix - 2, iy - 1, ix - 2, iy)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif iy == 8:
                            # толкаем противника с базы ↓
                            if pole[iy + 1][ix] == 1:
                                k_pole1 = pole
                                hod(ix, iy, ix, iy + 1)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                            # если загородили путь своей фишкой, делаем квадрат 1↑ 2↑
                            elif pole[iy + 1][ix] == 3 and (rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix, iy - 1)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix, iy + 1, ix, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                        # поворот на углу снизу
                        elif iy == 9:
                            if (pole[iy - 1][ix] == 1 or pole[iy - 1][ix] == 9 or pole[iy - 1][ix] == 11) and (
                                    rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix + h2[1], iy + h2[0])
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                    # выводим противника к базе снизу
                    if (iy == 7 or iy == 8) and kub1 > 0:
                        # справа снизу → ↓
                        if pole[iy + 1][ix + 2] == 1:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix + 2, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix + 2] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix + 2, iy, ix + 2, iy + 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                        # слева снизу ← ↓
                        elif pole[iy + 1][ix - 2] == 1:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix - 2, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix - 2] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix - 2, iy, ix - 2, iy + 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                # ходы сверху
                elif iy == 2 or iy == 1 or iy == 0:  # ↑
                    # выбивание на базе сверху, поворот на углу и трансформация в куб
                    if iy == 1 or iy == 0:
                        # выбивание если противник справа на базе ↓ → ↑
                        if pole[iy][ix + 2] == 1 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy + 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy + 1][ix] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy + 1, ix + 2, iy + 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy - 1][ix + 2] == 3:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix + 2, iy + 1, ix + 2, iy)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # выбивание если противник слева на базе ↓ ← ↑
                        elif pole[iy][ix - 2] == 1 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy + 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy + 1][ix] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy + 1, ix + 2, iy - 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy + 1][ix + 2] == 3:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix + 2, iy + 1, ix + 2, iy)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif iy == 1:
                            # толкаем противника с базы ↑
                            if pole[iy - 1][ix] == 1:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix, iy - 1)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                            # если загородили путь своей, делаем квадрат 1↓ 2↓
                            elif pole[iy - 1][ix] == 3 and (rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix, iy + 1)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix, iy - 1, ix, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                        # уход от противника и на угол
                        elif iy == 0:
                            if (pole[iy + 1][ix] == 1 or pole[iy + 1][ix] == 9 or pole[iy + 1][ix] == 11) and (
                                    rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix + h2[1], iy + h2[0])
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                    # выводим противника к базе сверху
                    if (iy == 1 or iy == 2) and kub1 > 0:
                        # сверху слева ← ↑
                        if pole[iy - 1][ix - 2] == 1:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix - 2, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix - 2] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix - 2, iy, ix - 2, iy - 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                        # сверху справа → ↑
                        elif pole[iy - 1][ix + 2] == 1:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix + 2, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix + 2] == 3:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix + 2, iy, ix + 2, iy - 1)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # уходим если наш квадрат может выбить противника
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and (rad == 2 or rad == 3):
                    if ix == 1 and pole[iy][ix - 1] == 2 and pole[iy][ix + 2] in list:
                        if iy in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy + 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                        elif iy not in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy - 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                    elif ix == 7 and pole[iy][ix + 2] == 2 and pole[iy][ix - 2] in list:
                        if iy in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy + 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                        elif iy not in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy - 1)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # ходы влево и вправо для разбития или трансформации
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and rad == 3:
                    # вправо →
                    if pole[iy][ix + 2] == 9:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                    # влево ←
                    elif pole[iy][ix - 2] == 9:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix - 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                    # трансформация в куб ← верхняя
                    elif pole[iy + 1][ix - 2] == 3 and iy not in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix - 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ← нижняя
                    elif pole[iy - 1][ix - 2] == 3 and iy in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix - 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб → верхняя
                    elif pole[iy + 1][ix + 2] == 3 and iy not in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб → нижняя
                    elif pole[iy - 1][ix + 2] == 3 and iy in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб ↑
                if (iy == 3 or iy == 5 or iy == 7 or iy == 9) and kub1 > 0 and trans == 0 and (rad == 2 or rad == 3):
                    if pole[iy - 2][ix] == 3:  # подъем для квадрата, нельзя равняться 1
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy - 1)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб ↓
                if (iy == 0 or iy == 2 or iy == 4 or iy == 6) and kub1 > 0 and trans == 0 and (rad == 2 or rad == 3):
                    if pole[iy + 2][ix] == 3:  # спуск для квадрата, нельзя равняться 8
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy + 1)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # когда нет вышеупомянутых ходов, есть ходы и фишка на том же месте
                if 0 < ix + h1[1] < 9 and 0 <= iy + h1[0] <= 9 and kub1 > 0 and pole[iy][ix] == 3:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + h1[1], iy + h1[0])
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
        # если рандом вертикальная фишка
        elif pole[iy][ix] == 4:

            h1 = random.choice((iz[0], iz[2], iz[5], iz[-1]))  # рандом первого хода
            h2 = random.choice((iz[5], iz[-1]))
            trans = 0
            spisok = [2, 4, 6, 8]
            # ↑ 24 ↓ 25 → 26 ← 27
            if kub > 0:
                # ходы справа
                if ix == 9 or ix == 8 or ix == 7:
                    # выбивание на базе справа, поворот на углу и трансформация в куб
                    if ix == 9 or ix == 8:
                        # выбивание если противник сверху на базе ← ↑ →
                        if pole[iy - 2][ix] == 2 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix - 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix - 1] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix - 1, iy, ix - 1, iy - 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy - 2][ix - 1] == 4:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix - 1, iy - 2, ix, iy - 2)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # выбивание если противник снизу на базе ← ↓ →
                        elif pole[iy + 2][ix] == 2 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix - 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix - 1] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix - 1, iy, ix - 1, iy + 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy + 2][ix - 1] == 4:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix - 1, iy + 2, ix, iy + 2)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif ix == 8:
                            # толкаем противника с базы →
                            if pole[iy][ix + 1] == 2:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix + 1, iy)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                            # если загородили путь своей, делаем квадрат
                            elif pole[iy][ix + 1] == 4 and (rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix - 1, iy)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix + 1, iy, ix, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                        elif ix == 9:
                            if (pole[iy][ix - 1] == 2 or pole[iy][ix - 1] == 9 or pole[iy][ix - 1] == 11) and (
                                    rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix + h2[1], iy + h2[0])
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                    # выводим противника к базе справа
                    if (ix == 7 or ix == 8) and kub1 > 0:
                        # справа снизу
                        if pole[iy + 2][ix + 1] == 2:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy + 2)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy + 2][ix] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy + 2, ix + 1, iy + 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                        # справа сверху
                        elif pole[iy - 2][ix + 1] == 2:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy - 2)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy - 2][ix] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy - 2, ix + 1, iy - 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                # ходы слева
                elif ix == 2 or ix == 1 or ix == 0:
                    # выбивание на базе слева, поворот на углу и трансформация в куб
                    if ix == 1 or ix == 0:
                        # выбивание если противник справа на базе ↓ → ↑
                        if pole[iy - 2][ix] == 2 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix + 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix + 1] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix + 1, iy, ix + 1, iy - 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy - 2][ix + 1] == 4:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix + 1, iy - 2, ix, iy - 2)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # выбивание если противник слева на базе ↓ ← ↑
                        elif pole[iy + 2][ix] == 2 and (rad == 2 or rad == 3):
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix + 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy][ix + 1] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix + 1, iy, ix + 1, iy + 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                                        if kub1 > 0 and pole[iy + 2][ix + 1] == 4:
                                            k_pole1 = copy.deepcopy(pole)
                                            hod(ix + 1, iy + 2, ix, iy + 2)
                                            if k_pole1 != pole:
                                                kub1 = kub1 - 1
                        # рядом с базой
                        elif ix == 1:
                            # толкаем противника с базы
                            if pole[iy][ix - 1] == 2:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix - 1, iy)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                            # если загородили путь своей, делаем квадрат
                            elif pole[iy][ix - 1] == 4 and (rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix + 1, iy)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix - 1, iy, ix, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                        # уход от противника и на угол
                        elif ix == 9:
                            if (pole[iy][ix + 1] == 2 or pole[iy][ix + 1] == 9 or pole[iy][ix + 1] == 11) and (
                                    rad == 2 or rad == 3):
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy, ix + h2[1], iy + h2[0])
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                    if (ix == 1 or ix == 2) and kub1 > 0:  # выводим противника к базе слева
                        # слева сверху
                        if pole[iy - 2][ix - 1] == 2:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy - 2)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy - 2][ix] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy - 2, ix - 1, iy - 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                        # слева снизу
                        elif pole[iy + 2][ix - 1] == 2:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix, iy + 2)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                                if kub1 > 0 and pole[iy + 2][ix] == 4:
                                    k_pole1 = copy.deepcopy(pole)
                                    hod(ix, iy + 2, ix - 1, iy + 2)
                                    if k_pole1 != pole:
                                        kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # уходим если наш квадрат может выбить противника
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and (rad == 2 or rad == 3):
                    if iy == 1 and pole[iy - 1][ix] == 1 and pole[iy + 2][ix] in list:
                        if ix in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix + 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                        elif ix not in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix - 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                    elif iy == 7 and pole[iy + 2][ix] == 2 and pole[iy - 2][ix] in list:
                        if ix in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix + 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                        elif ix not in spisok:
                            k_pole1 = copy.deepcopy(pole)
                            hod(ix, iy, ix - 1, iy)
                            if k_pole1 != pole:
                                kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # ходы вниз и вверх для разбития или трансформации
                if (iy != 0 and ix != 0) and (iy != 9 and ix != 9) and kub1 > 0 and rad == 3:
                    # вниз ↓
                    if pole[iy + 1][ix] == 11:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                    # вверх ↑
                    elif pole[iy][ix - 2] == 11:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix - 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                    # трансформация в куб ↓ правая
                    elif pole[iy + 2][ix + 1] == 4 and ix not in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy + 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ↓ левая
                    elif pole[iy + 2][ix - 1] == 4 and ix in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy + 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ↑ правая
                    elif pole[iy - 2][ix + 1] == 4 and ix not in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy - 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                    # трансформация в куб ↑ левая
                    elif pole[iy - 2][ix - 1] == 4 and ix in spisok and trans == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy - 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб
                if (ix == 3 or ix == 5 or ix == 7 or ix == 9) and kub1 > 0 and trans == 0 and (
                        rad == 2 or rad == 3):  # трансформация в куб left
                    if pole[iy][ix - 2] == 4:  # берем влево для квадрата, нельзя равняться 1
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix - 1, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            trans = 1
                the_end()
                if end_p:
                    break
                # трансформация в куб
                if (ix == 0 or ix == 2 or ix == 4 or ix == 6) and kub1 > 0 and trans == 0 and (
                        rad == 2 or rad == 3):  # трансформация в куб right
                    if pole[iy][ix + 2] == 4:  # берем вправо для квадрата, нельзя равняться 8
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 1, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                the_end()
                if end_p:
                    break
                # когда нет вышеупомянутых ходов, есть ходы и фишка на том же месте
                if 0 <= ix + h1[1] <= 9 and 0 < iy + h1[0] < 9 and kub1 > 0 and pole[iy][ix] == 4:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + h1[1], iy + h1[0])
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
        # если рандом квадрат и выбираем только голову куба
        elif pole[iy][ix] == 13 and pole[iy + 1][ix] == 13 and (iy == 1 or iy == 3 or iy == 5 or iy == 7) \
                or pole[iy][ix] == 15 and pole[iy][ix + 1] == 15 and (ix == 1 or ix == 3 or ix == 5 or ix == 7):
            h1 = random.choice((iz[4], iz[5], iz[-2], iz[-1]))
            spisok_kvdr = [1, 2, 9, 11]
            # квадрат выталкивает влево фигуры к базе
            if ix == 3 and pole[iy][ix - 3] == 0:
                if pole[iy][ix - 2] in spisok_kvdr or pole[iy + 1][ix - 2] == 1 or pole[iy][ix - 1] == 2:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if ix == 3 and pole[iy][ix - 3] == 2 and kub1 > 0 and (rad == 2 or rad == 3):
                if pole[iy][ix - 2] == pole[iy + 1][ix - 2] == pole[iy][ix - 1] == 0:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # квадрат выталкивает вверх фигуры к базе
            if iy == 3 and pole[iy - 3][ix] == 0 and kub1 > 0:
                if pole[iy - 2][ix] in spisok_kvdr or pole[iy - 1][ix] == 1 or pole[iy - 2][ix + 1] == 2:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if iy == 3 and pole[iy - 3][ix] == 1 and kub1 > 0 and (rad == 2 or rad == 3):
                if pole[iy - 2][ix] == pole[iy - 1][ix] == pole[iy - 2][ix + 1] == 0:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # квадрат выталкивает вправо фигуры к базе
            if ix == 5 and pole[iy][ix + 4] == 0 and kub1 > 0:
                if pole[iy][ix + 2] in spisok_kvdr or pole[iy + 1][ix + 2] == 1 or pole[iy][ix + 3] == 2:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if ix == 5 and pole[iy][ix + 4] == 2 and kub1 > 0 and (rad == 2 or rad == 3):
                if pole[iy][ix + 2] == pole[iy + 1][ix + 2] == pole[iy][ix + 3] == 0:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # квадрат выталкивает вниз фигуры к базе
            if iy == 5 and pole[iy + 4][ix] == 0 and kub1 > 0:
                if pole[iy + 2][ix] in spisok_kvdr or pole[iy + 3][ix] == 1 or pole[iy + 2][ix + 1] == 2:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy + 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            if iy == 5 and pole[iy + 4][ix] == 1 and kub1 > 0 and (rad == 2 or rad == 3):
                if pole[iy + 2][ix] == pole[iy + 3][ix] == pole[iy + 2][ix + 1] == 0:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy + 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # слева
            if ix == 1 and kub1 > 0:
                # квадрат слева у базы. на базе враг
                if pole[iy][ix - 1] == 2:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 1, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy - 1][ix] == 1 and iy == 1:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 1)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy + 2][ix] == 1 and iy == 7:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy + 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # ограждение противника сверху
                elif pole[iy - 2][ix - 1] == 2 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # ограждение противника снизу
                elif pole[iy + 2][ix - 1] == 2 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy + 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (pole[iy][ix + 2] == 9 or pole[iy][ix + 2] == 11) and rad == 3:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                    else:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy + 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                # обходим противника вправо вниз влево
                if pole[iy + 2][ix] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy + 2][ix - 1] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy][ix + 2] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix + 2, iy, ix + 2, iy + 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy + 2][ix + 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix + 2, iy + 2, ix, iy + 2)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                # обходим противника вправо вверх влево
                if pole[iy - 2][ix] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy - 2][ix - 1] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy][ix + 2] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix + 2, iy, ix + 2, iy - 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy - 2][ix + 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix + 2, iy - 2, ix, iy - 2)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # сверху
            if iy == 1 and kub1 > 0:
                # квадрат сверху у базы. на базе враг
                if pole[iy - 1][ix] == 1:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 1)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy][ix - 1] == 2 and ix == 1:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 1, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy][ix + 2] == 2 and ix == 7:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # ограждение противника сверху
                elif pole[iy - 1][ix - 2] == 1 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # ограждение противника сверху
                elif pole[iy - 1][ix + 2] == 1 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (pole[iy + 2][ix] == 9 or pole[iy + 2][ix] == 11) and rad == 3:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                    else:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                # обходим противника вниз право вверх
                if pole[iy][ix + 2] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy - 1][ix + 2] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy + 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy + 2][ix] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy + 2, ix + 2, iy + 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy + 2][ix + 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix + 2, iy + 2, ix + 2, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                # обходим противника вниз влево вверх
                if pole[iy][ix - 2] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy - 1][ix - 2] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy + 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy + 2][ix] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy + 2, ix - 2, iy + 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy + 2][ix - 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix - 2, iy + 2, ix - 2, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # справа
            if ix == 7 and kub1 > 0:
                # квадрат справа у базы. на базе враг
                if pole[iy][ix + 2] == 2:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy + 2][ix] == 1 and iy == 7:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy + 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy - 1][ix] == 1 and iy == 1:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 1)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # ограждение противника справа
                elif pole[iy + 2][ix + 2] == 2 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy + 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy - 2][ix + 2] == 2 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (pole[iy][ix - 2] == 9 or pole[iy][ix - 2] == 11) and rad == 3:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy - 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                    else:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy + 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                # обходим противника влево вниз вправо
                if pole[iy + 2][ix] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy + 2][ix + 2] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix - 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy][ix - 2] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix - 2, iy, ix - 2, iy + 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy + 2][ix - 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix - 2, iy + 2, ix, iy + 2)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                # обходим противника влево вверх вправо
                if pole[iy - 2][ix] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy - 2][ix + 2] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix - 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy][ix - 2] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix - 2, iy, ix - 2, iy - 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy - 2][ix - 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix - 2, iy - 2, ix, iy - 2)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # снизу
            if iy == 7 and kub1 > 0:  # квадрат снизу у базы. на базе враг
                if pole[iy + 2][ix] == 1:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix, iy + 2)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy][ix + 2] == 2 and ix == 7:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy][ix - 1] == 2 and ix == 1:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 1, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # ограждение противника снизу
                elif pole[iy + 2][ix + 2] == 1 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix + 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                elif pole[iy + 2][ix - 2] == 1 and (rad == 2 or rad == 3):
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                # уходим от выталкивания
                elif (pole[iy - 2][ix] == 9 or pole[iy - 2][ix] == 11) and rad == 3:
                    k_pole1 = copy.deepcopy(pole)
                    hod(ix, iy, ix - 2, iy)
                    if k_pole1 != pole:
                        kub1 = kub1 - 1
                    else:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix + 2, iy)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                # обходим противника вверх вправо вниз
                if pole[iy][ix + 2] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy + 2][ix + 2] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy - 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy - 2][ix] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy - 2, ix + 2, iy - 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy - 2][ix + 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix + 2, iy - 2, ix + 2, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
                # обходим противника вверх влево вниз
                if pole[iy][ix - 2] == spisok_kvdr and rad == 3 and kub1 > 0:
                    if pole[iy + 2][ix - 2] == 0:
                        k_pole1 = copy.deepcopy(pole)
                        hod(ix, iy, ix, iy - 2)
                        if k_pole1 != pole:
                            kub1 = kub1 - 1
                            if kub1 > 0 and pole[iy - 2][ix] in list:
                                k_pole1 = copy.deepcopy(pole)
                                hod(ix, iy - 2, ix - 2, iy - 2)
                                if k_pole1 != pole:
                                    kub1 = kub1 - 1
                                    if kub1 > 0 and pole[iy - 2][ix - 2] in list:
                                        k_pole1 = copy.deepcopy(pole)
                                        hod(ix - 2, iy - 2, ix - 2, iy)
                                        if k_pole1 != pole:
                                            kub1 = kub1 - 1
            the_end()
            if end_p:
                break
            # когда нет вышеупомянутых ходов, есть ходы и фишка на том же месте
            if 0 < ix + h1[1] < 9 and 0 < iy + h1[0] < 9 and kub1 > 0:
                k_pole1 = copy.deepcopy(pole)
                hod(ix, iy, ix + h1[1], iy + h1[0])
                if k_pole1 != pole:
                    kub1 = kub1 - 1

    time.sleep(0.01)
    doska.update()
    f_hi = 1
    opredel_hoda(f_hi)


# определение какая фишка среди горизонтальных
def pravila_gor(poz1_x, poz1_y, poz2_x, poz2_y):
    if 0 < poz1_y < 9 and pole[poz1_y][poz1_x] == pole[poz1_y + 1][poz1_x] and (
            poz1_y == 1 or poz1_y == 3 or poz1_y == 5 or poz1_y == 7):
        # проверка, что фишка не на базе, рядом есть ещё одна фишка и позиция нечетная
        vmeste(poz1_x, poz1_y, poz2_x, poz2_y)
    else:
        pravila_gor2(poz1_x, poz1_y, poz2_x, poz2_y)


# правила хода горизонтальных одиночных фишек
def pravila_gor2(poz1_x, poz1_y, poz2_x, poz2_y):
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
    spisok = [2, 4, 6, 8]
    if f_hi:
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
    if f_hi == 0 or f_hi == 2:
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
            if pole[poz1_y + 1][poz1_x] == g_par_gor and pole[poz1_y + 1][poz1_x + 1] == g_par_gor2:
                pole[poz1_y + 1][poz1_x] = 0
                pole[poz1_y + 1][poz1_x + 1] = 0
            elif pole[poz1_y + 1][poz1_x] == 0 and pole[poz1_y + 1][poz1_x + 1] == 0:
                pole[poz1_y + 1][poz1_x] = pole[poz1_y][poz1_x]
                pole[poz1_y + 1][poz1_x + 1] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
        else:  # остальные случаи
            if poz1_y + 1 != 9:
                # проверка пустых клеток снизу
                if pole[poz1_y + 2][poz1_x] == pole[poz1_y + 2][poz1_x + 1] == 0 or pole[poz1_y + 1][poz1_x] == \
                        pole[poz1_y + 1][poz1_x + 1] == 0:
                    # фикс для компа если снизу своя фишка
                    if pole[poz1_y + 1][poz1_x] == g_svoi and pole[poz1_y + 1][poz1_x + 1] == g_svoi2:
                        pass
                    # проверка, что нет вертикальных чужих
                    elif pole[poz1_y + 1][poz1_x] != g_par_vert and pole[poz1_y + 1][poz1_x + 1] != g_par_vert:
                        # проверка что нет вертикальных своих
                        if pole[poz1_y + 1][poz1_x] != g_ugol1 and pole[poz1_y + 1][poz1_x + 1] != g_ugol1:
                            # смещение фигур врага рядом
                            if pole[poz2_y][poz2_x] == g_par_gor or pole[poz2_y][poz2_x] == g_par_gor2:
                                if pole[poz2_y][poz2_x] == g_par_gor2:  # смещение значения
                                    poz2_x -= 1
                                pole[poz2_y + 1][poz2_x] = pole[poz2_y][poz2_x]
                                pole[poz2_y + 1][poz2_x + 1] = pole[poz2_y][poz2_x + 1]
                            pole[poz1_y + 1][poz1_x] = pole[poz1_y][poz1_x]
                            pole[poz1_y + 1][poz1_x + 1] = pole[poz1_y][poz1_x + 1]
                            pole[poz1_y][poz1_x] = 0
                            pole[poz1_y][poz1_x + 1] = 0
                            # если рядом фигура на четном месте, то соединение фигур
                            if pole[poz1_y + 1][poz1_x] == pole[poz1_y + 2][poz1_x] and (
                                    poz1_y + 1 == 1 or poz1_y + 1 == 3 or poz1_y + 1 == 5 or poz1_y + 1 == 7):
                                pole[poz1_y + 1][poz1_x] = g_par_kv1
                                pole[poz1_y + 1][poz1_x + 1] = g_par_kv12
                                pole[poz1_y + 2][poz1_x] = g_par_kv1
                                pole[poz1_y + 2][poz1_x + 1] = g_par_kv12
    # ПРОВЕРКА ХОДА ВВЕРХ
    elif (poz2_y == poz1_y - 1 and poz2_x == poz1_x) or (poz2_y == poz1_y - 1 and poz2_x == poz1_x + 1):
        if poz1_y - 1 == 0:  # выброс врага с базы
            if pole[poz1_y - 1][poz1_x] == g_par_gor and pole[poz1_y - 1][poz1_x + 1] == g_par_gor2:
                pole[poz1_y - 1][poz1_x] = 0
                pole[poz1_y - 1][poz1_x + 1] = 0
            elif pole[poz1_y - 1][poz1_x] == 0 and pole[poz1_y - 1][poz1_x + 1] == 0:
                pole[poz1_y - 1][poz1_x] = pole[poz1_y][poz1_x]
                pole[poz1_y - 1][poz1_x + 1] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
        else:  # остальные случаи
            if pole[poz1_y - 2][poz1_x] == pole[poz1_y - 2][poz1_x + 1] == 0 or \
                    pole[poz1_y - 1][poz1_x] == pole[poz1_y - 1][poz1_x + 1] == 0:  # проверка пустых клеток сверху
                # фикс для компа если сверху своя фишка
                if pole[poz1_y - 1][poz1_x] == g_svoi and pole[poz1_y - 1][poz1_x + 1] == g_svoi2:
                    pass
                # проверка, что нет вертикальных чужих
                elif pole[poz1_y - 1][poz1_x] != g_par_vert2 and pole[poz1_y - 1][poz1_x + 1] != g_par_vert2:
                    # проверка что нет вертикальных своих
                    if pole[poz1_y - 1][poz1_x] != g_ugol2 and pole[poz1_y - 1][poz1_x + 1] != g_ugol2:
                        # смещение фигур врага рядом
                        if pole[poz2_y][poz2_x] == g_par_gor or pole[poz2_y][poz2_x] == g_par_gor2:
                            if pole[poz2_y][poz2_x] == g_par_gor2:
                                poz2_x -= 1
                            pole[poz2_y - 1][poz2_x] = pole[poz2_y][poz2_x]
                            pole[poz2_y - 1][poz2_x + 1] = pole[poz2_y][poz2_x + 1]
                        pole[poz1_y - 1][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y - 1][poz1_x + 1] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
                        # если рядом фигура на нечетном месте, то соединение фигур
                        if pole[poz1_y - 1][poz1_x] == pole[poz1_y - 2][poz1_x] and (
                                poz1_y - 1 == 2 or poz1_y - 1 == 4 or poz1_y - 1 == 6 or poz1_y - 1 == 8):
                            pole[poz1_y - 1][poz1_x] = g_par_kv1
                            pole[poz1_y - 1][poz1_x + 1] = g_par_kv12
                            pole[poz1_y - 2][poz1_x] = g_par_kv1
                            pole[poz1_y - 2][poz1_x + 1] = g_par_kv12
    # ПРОВЕРКА ХОДА ВЛЕВО
    elif (poz2_y == poz1_y and poz2_x == poz1_x - 1) or (poz2_y == poz1_y and poz2_x == poz1_x - 2):
        if poz1_x - 2 != 0 and poz1_x - 1 != 0:  # фикс выхода на базу вертикальную
            # проверка пустых клеток слева
            if pole[poz1_y][poz1_x - 2] == 0 and pole[poz1_y][poz1_x - 1] == 0:
                pole[poz1_y][poz1_x - 2] = pole[poz1_y][poz1_x]
                pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if pole[poz1_y][poz1_x - 2] == pole[poz1_y + 1][poz1_x - 2] and (
                            poz1_y == 1 or poz1_y == 3 or poz1_y == 5 or poz1_y == 7):
                        pole[poz1_y][poz1_x - 2] = g_par_kv1
                        pole[poz1_y][poz1_x - 1] = g_par_kv12
                        pole[poz1_y + 1][poz1_x - 2] = g_par_kv1
                        pole[poz1_y + 1][poz1_x - 1] = g_par_kv12
                    elif pole[poz1_y][poz1_x - 2] == pole[poz1_y - 1][poz1_x - 2] and (
                            poz1_y == 2 or poz1_y == 4 or poz1_y == 6 or poz1_y == 8):
                        pole[poz1_y][poz1_x - 2] = g_par_kv1
                        pole[poz1_y][poz1_x - 1] = g_par_kv12
                        pole[poz1_y - 1][poz1_x - 2] = g_par_kv1
                        pole[poz1_y - 1][poz1_x - 1] = g_par_kv12
            # если слева квадрат противника и стоим не впритык
            elif pole[poz1_y][poz1_x - 2] == g_kvad and poz1_x != 3:
                # если слева есть место для выталкивания
                if pole[poz1_y][poz1_x - 3] == 0 and pole[poz1_y][poz1_x - 4] == 0:
                    if pole[poz1_y + 1][poz1_x - 2] == g_kvad and poz1_y not in spisok:  # если остальная часть снизу
                        pole[poz1_y][poz1_x - 4] = g_par_gor
                        pole[poz1_y][poz1_x - 3] = g_par_gor2
                        pole[poz1_y + 1][poz1_x - 2] = g_par_gor
                        pole[poz1_y + 1][poz1_x - 1] = g_par_gor2
                        pole[poz1_y][poz1_x - 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
                    elif pole[poz1_y - 1][poz1_x - 2] == g_kvad and poz1_y in spisok:  # если остальная часть сверху
                        pole[poz1_y][poz1_x - 4] = g_par_gor
                        pole[poz1_y][poz1_x - 3] = g_par_gor2
                        pole[poz1_y - 1][poz1_x - 2] = g_par_gor
                        pole[poz1_y - 1][poz1_x - 1] = g_par_gor2
                        pole[poz1_y][poz1_x - 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
            # если слева квадрат противника и стоим впритык к базе
            elif pole[poz1_y][poz1_x - 2] == g_kvad and poz1_x == 3:
                if pole[poz1_y][poz1_x - 3] == 0:
                    if pole[poz1_y + 1][poz1_x - 2] == g_kvad and poz1_y not in spisok:
                        pole[poz1_y + 1][poz1_x - 2] = g_par_gor
                        pole[poz1_y + 1][poz1_x - 1] = g_par_gor2
                        pole[poz1_y][poz1_x - 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
                    elif pole[poz1_y - 1][poz1_x - 2] == g_kvad and poz1_y in spisok:
                        pole[poz1_y - 1][poz1_x - 2] = g_par_gor
                        pole[poz1_y - 1][poz1_x - 1] = g_par_gor2
                        pole[poz1_y][poz1_x - 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 9 and pole[8][0] == 0 and pole[7][0] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            pole[7][0] = g_ugol1
            pole[8][0] = g_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 0 and pole[1][0] == 0 and pole[2][0] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            pole[1][0] = g_ugol1
            pole[2][0] = g_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y][poz1_x + 1] = 0
    # ПРОВЕРКА ХОДА ВПРАВО
    elif (poz2_y == poz1_y and poz2_x == poz1_x + 2) or (poz2_y == poz1_y and poz2_x == poz1_x + 3):
        if poz1_x + 2 != 9 and poz1_x + 1 != 9:
            if pole[poz1_y][poz1_x + 2] == 0 and pole[poz1_y][poz1_x + 3] == 0:
                pole[poz1_y][poz1_x + 2] = pole[poz1_y][poz1_x]
                pole[poz1_y][poz1_x + 3] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if pole[poz1_y][poz1_x + 2] == pole[poz1_y + 1][poz1_x + 2] and (
                            poz1_y == 1 or poz1_y == 3 or poz1_y == 5 or poz1_y == 7):
                        pole[poz1_y][poz1_x + 2] = g_par_kv1
                        pole[poz1_y][poz1_x + 3] = g_par_kv12
                        pole[poz1_y + 1][poz1_x + 2] = g_par_kv1
                        pole[poz1_y + 1][poz1_x + 3] = g_par_kv12
                    elif pole[poz1_y][poz1_x + 2] == pole[poz1_y - 1][poz1_x + 2] and (
                            poz1_y == 2 or poz1_y == 4 or poz1_y == 6 or poz1_y == 8):
                        pole[poz1_y][poz1_x + 2] = g_par_kv1
                        pole[poz1_y][poz1_x + 3] = g_par_kv12
                        pole[poz1_y - 1][poz1_x + 2] = g_par_kv1
                        pole[poz1_y - 1][poz1_x + 3] = g_par_kv12
            # если справа квадрат противника и стоим не впритык
            elif pole[poz1_y][poz1_x + 2] == g_kvad and poz1_x != 5:
                # если слева есть место для выталкивания
                if pole[poz1_y][poz1_x + 4] == 0 and pole[poz1_y][poz1_x + 5] == 0:
                    if pole[poz1_y + 1][poz1_x + 2] == g_kvad and poz1_y not in spisok:  # если остальная часть снизу
                        pole[poz1_y][poz1_x + 4] = g_par_gor
                        pole[poz1_y][poz1_x + 5] = g_par_gor2
                        pole[poz1_y + 1][poz1_x + 2] = g_par_gor
                        pole[poz1_y + 1][poz1_x + 3] = g_par_gor2
                        pole[poz1_y][poz1_x + 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x + 3] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
                    elif pole[poz1_y - 1][poz1_x + 2] == g_kvad and poz1_y in spisok:  # если остальная часть сверху
                        pole[poz1_y][poz1_x + 4] = g_par_gor
                        pole[poz1_y][poz1_x + 5] = g_par_gor2
                        pole[poz1_y - 1][poz1_x + 2] = g_par_gor
                        pole[poz1_y - 1][poz1_x + 3] = g_par_gor2
                        pole[poz1_y][poz1_x + 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x + 3] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
            elif pole[poz1_y][poz1_x + 2] == g_kvad and poz1_x == 5:  # если справа квадрат противника и стоим впритык
                if pole[poz1_y][poz1_x + 4] == 0:
                    if pole[poz1_y + 1][poz1_x + 2] == g_kvad and poz1_y not in spisok:
                        pole[poz1_y + 1][poz1_x + 2] = g_par_gor
                        pole[poz1_y + 1][poz1_x + 3] = g_par_gor2
                        pole[poz1_y][poz1_x + 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x + 3] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
                    elif pole[poz1_y - 1][poz1_x + 2] == g_kvad and poz1_y in spisok:
                        pole[poz1_y - 1][poz1_x + 2] = g_par_gor
                        pole[poz1_y - 1][poz1_x + 3] = g_par_gor2
                        pole[poz1_y][poz1_x + 2] = pole[poz1_y][poz1_x]
                        pole[poz1_y][poz1_x + 3] = pole[poz1_y][poz1_x + 1]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 9 and pole[8][9] == 0 and pole[7][9] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            pole[7][9] = g_ugol1
            pole[8][9] = g_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y][poz1_x + 1] = 0
        elif poz1_y == 0 and pole[1][9] == 0 and pole[2][9] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            pole[1][9] = g_ugol1
            pole[2][9] = g_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y][poz1_x + 1] = 0


# определение какая фишка среди вертикальных
def pravila_vert(poz1_x, poz1_y, poz2_x, poz2_y):
    if 0 < poz1_x < 9 and pole[poz1_y][poz1_x] == pole[poz1_y][poz1_x + 1] and (
            poz1_x == 1 or poz1_x == 3 or poz1_x == 5 or poz1_x == 7):
        vmeste(poz1_x, poz1_y, poz2_x, poz2_y)
    else:
        pravila_vert2(poz1_x, poz1_y, poz2_x, poz2_y)


# правила хода вертикальных одиночных фишек
def pravila_vert2(poz1_x, poz1_y, poz2_x, poz2_y):
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
    spisok = [2, 4, 6, 8]
    if f_hi:
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
    if f_hi == 0 or f_hi ==2:
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
            if pole[poz1_y][poz1_x + 1] == v_par_vert and pole[poz1_y + 1][poz1_x + 1] == v_par_vert2:
                pole[poz1_y][poz1_x + 1] = 0
                pole[poz1_y + 1][poz1_x + 1] = 0
            elif pole[poz1_y][poz1_x + 1] == 0 and pole[poz1_y + 1][poz1_x + 1] == 0:
                pole[poz1_y][poz1_x + 1] = pole[poz1_y][poz1_x]
                pole[poz1_y + 1][poz1_x + 1] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y + 1][poz1_x] = 0
        else:  # остальные случаи
            if poz1_x + 1 != 9:
                if pole[poz1_y][poz1_x + 2] == pole[poz1_y + 1][poz1_x + 2] == 0 or \
                        pole[poz1_y][poz1_x + 1] == pole[poz1_y + 1][poz1_x + 1] == 0:  # проверка пустых клеток справа
                    # фикс для компа если справа своя фишка
                    if pole[poz1_y][poz1_x + 1] == v_svoi and pole[poz1_y + 1][poz1_x + 1] == v_svoi2:
                        pass
                    # если справа горизонтальная фишка, то ничего не происходит
                    elif pole[poz1_y][poz1_x + 1] != v_par_gor and pole[poz1_y + 1][poz1_x + 1] != v_par_gor:
                        if pole[poz1_y][poz1_x + 1] != v_ugol1 and pole[poz1_y + 1][poz1_x + 1] != v_ugol1:
                            # смещение фигур врага рядом
                            if pole[poz2_y][poz2_x] == v_par_vert or pole[poz2_y][poz2_x] == v_par_vert2:
                                if pole[poz2_y][poz2_x] == v_par_vert2:
                                    poz2_y -= 1
                                pole[poz2_y][poz2_x + 1] = pole[poz2_y][poz2_x]
                                pole[poz2_y + 1][poz2_x + 1] = pole[poz2_y + 1][poz2_x]
                            pole[poz1_y][poz1_x + 1] = pole[poz1_y][poz1_x]
                            pole[poz1_y + 1][poz1_x + 1] = pole[poz1_y + 1][poz1_x]
                            pole[poz1_y][poz1_x] = 0
                            pole[poz1_y + 1][poz1_x] = 0
                            # если рядом фигура на нечетном месте, то соединение фигур
                            if pole[poz1_y][poz1_x + 1] == pole[poz1_y][poz1_x + 2] and (
                                    poz1_x + 1 == 1 or poz1_x + 1 == 3 or poz1_x + 1 == 5 or poz1_x + 1 == 7):
                                pole[poz1_y][poz1_x + 1] = v_par_kv2
                                pole[poz1_y + 1][poz1_x + 1] = v_par_kv22
                                pole[poz1_y][poz1_x + 2] = v_par_kv2
                                pole[poz1_y + 1][poz1_x + 2] = v_par_kv22

    # ПРОВЕРКА ВЛЕВО
    elif (poz2_y == poz1_y and poz2_x == poz1_x - 1) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x - 1):
        if poz1_x - 1 == 0:  # выброс врага с базы
            if pole[poz1_y][poz1_x - 1] == v_par_vert and pole[poz1_y + 1][poz1_x - 1] == v_par_vert2:
                pole[poz1_y][poz1_x - 1] = 0
                pole[poz1_y + 1][poz1_x - 1] = 0
            elif pole[poz1_y][poz1_x - 1] == 0 and pole[poz1_y + 1][poz1_x - 1] == 0:
                pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x]
                pole[poz1_y + 1][poz1_x - 1] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y + 1][poz1_x] = 0
        else:  # остальные случаи
            if pole[poz1_y][poz1_x - 2] == pole[poz1_y + 1][poz1_x - 2] == 0 or \
                    pole[poz1_y][poz1_x - 1] == pole[poz1_y + 1][poz1_x - 1] == 0:  # проверка пустых клеток слева
                # фикс для компа если слева своя фишка
                if pole[poz1_y][poz1_x - 1] == v_svoi and pole[poz1_y + 1][poz1_x - 1] == v_svoi2:
                    pass
                # если слева горизонтальная фишка, то ничего не происходит
                elif pole[poz1_y][poz1_x - 1] != v_par_gor2 and pole[poz1_y + 1][poz1_x - 1] != v_par_gor2:
                    if pole[poz1_y][poz1_x - 1] != v_ugol2 and pole[poz1_y + 1][poz1_x - 1] != v_ugol2:
                        if pole[poz2_y][poz2_x] == v_par_vert or pole[poz2_y][poz2_x] == v_par_vert2:
                            if pole[poz2_y][poz2_x] == v_par_vert2:
                                poz2_y -= 1
                            pole[poz2_y][poz2_x - 1] = pole[poz2_y][poz2_x]
                            pole[poz2_y + 1][poz2_x - 1] = pole[poz2_y + 1][poz2_x]
                        pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x]
                        pole[poz1_y + 1][poz1_x - 1] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
                        # если рядом фигура на четном месте, то соединение фигур
                        if pole[poz1_y][poz1_x - 1] == pole[poz1_y][poz1_x - 2] and (
                                poz1_x - 1 == 2 or poz1_x - 1 == 4 or poz1_x - 1 == 6 or poz1_x - 1 == 8):
                            pole[poz1_y][poz1_x - 1] = v_par_kv2
                            pole[poz1_y + 1][poz1_x - 1] = v_par_kv22
                            pole[poz1_y][poz1_x - 2] = v_par_kv2
                            pole[poz1_y + 1][poz1_x - 2] = v_par_kv22

    # ПРОВЕРКА ХОДА ВВЕРХ
    elif (poz2_y == poz1_y - 1 and poz2_x == poz1_x) or (poz2_y == poz1_y - 2 and poz2_x == poz1_x):
        if poz1_y - 2 != 0 and poz1_y - 1 != 0:  #
            if pole[poz1_y - 1][poz1_x] == 0 and pole[poz1_y - 2][poz1_x] == 0:  # проверка пустых клеток сверху
                pole[poz1_y - 2][poz1_x] = pole[poz1_y][poz1_x]
                pole[poz1_y - 1][poz1_x] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y + 1][poz1_x] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if pole[poz1_y - 2][poz1_x] == pole[poz1_y - 2][poz1_x - 1] and (
                            poz1_x == 2 or poz1_x == 4 or poz1_x == 6 or poz1_x == 8):
                        pole[poz1_y - 2][poz1_x] = v_par_kv2
                        pole[poz1_y - 1][poz1_x] = v_par_kv22
                        pole[poz1_y - 2][poz1_x - 1] = v_par_kv2
                        pole[poz1_y - 1][poz1_x - 1] = v_par_kv22
                    elif pole[poz1_y - 2][poz1_x] == pole[poz1_y - 2][poz1_x + 1] and (
                            poz1_x == 1 or poz1_x == 3 or poz1_x == 5 or poz1_x == 7):
                        pole[poz1_y - 2][poz1_x] = v_par_kv2
                        pole[poz1_y - 1][poz1_x] = v_par_kv22
                        pole[poz1_y - 2][poz1_x + 1] = v_par_kv2
                        pole[poz1_y - 1][poz1_x + 1] = v_par_kv22
            # если сверху квадрат противника и стоим не впритык
            elif pole[poz1_y - 2][poz1_x] == v_kvad and poz1_y != 3:
                # если сверху есть место для выталкивания
                if pole[poz1_y - 3][poz1_x] == 0 and pole[poz1_y - 4][poz1_x] == 0:
                    if pole[poz1_y - 2][poz1_x - 1] == v_kvad and poz1_x in spisok:  # если остальная часть слева
                        pole[poz1_y - 4][poz1_x] = v_par_vert
                        pole[poz1_y - 3][poz1_x] = v_par_vert2
                        pole[poz1_y - 2][poz1_x - 1] = v_par_vert
                        pole[poz1_y - 1][poz1_x - 1] = v_par_vert2
                        pole[poz1_y - 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y - 1][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
                    elif pole[poz1_y - 2][poz1_x + 1] == v_kvad and poz1_x not in spisok:  # если остальная часть справа
                        pole[poz1_y - 4][poz1_x] = v_par_vert
                        pole[poz1_y - 3][poz1_x] = v_par_vert2
                        pole[poz1_y - 2][poz1_x + 1] = v_par_vert
                        pole[poz1_y - 1][poz1_x + 1] = v_par_vert2
                        pole[poz1_y - 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y - 1][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
            elif pole[poz1_y - 2][poz1_x] == v_kvad and poz1_y == 3:  # если сверху квадрат противника и стоим впритык
                if pole[poz1_y - 3][poz1_x] == 0:
                    if pole[poz1_y - 2][poz1_x - 1] == v_kvad and poz1_x in spisok:
                        pole[poz1_y - 2][poz1_x - 1] = v_par_vert
                        pole[poz1_y - 1][poz1_x - 1] = v_par_vert2
                        pole[poz1_y - 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y - 1][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
                    elif pole[poz1_y - 2][poz1_x + 1] == v_kvad and poz1_x not in spisok:
                        pole[poz1_y - 2][poz1_x + 1] = v_par_vert
                        pole[poz1_y - 1][poz1_x + 1] = v_par_vert2
                        pole[poz1_y - 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y - 1][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 9 and pole[0][8] == 0 and pole[0][7] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            pole[0][7] = v_ugol1
            pole[0][8] = v_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 0 and pole[0][1] == 0 and pole[0][2] == 0:  # poz1_x - 2 != 17 or poz1_x - 1 != 17:
            pole[0][1] = v_ugol1
            pole[0][2] = v_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y + 1][poz1_x] = 0
    # ПРОВЕРКА ХОДА ВНИЗ
    elif (poz2_y == poz1_y + 2 and poz2_x == poz1_x) or (poz2_y == poz1_y + 3 and poz2_x == poz1_x):
        if poz1_y + 2 != 9 and poz1_y + 1 != 9:  #
            if pole[poz1_y + 2][poz1_x] == 0 and pole[poz1_y + 3][poz1_x] == 0:  # проверка пустых клеток снизу
                pole[poz1_y + 2][poz1_x] = pole[poz1_y][poz1_x]
                pole[poz1_y + 3][poz1_x] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y + 1][poz1_x] = 0
                if 0 < poz1_x < 9 and 0 < poz1_y < 9:
                    if pole[poz1_y + 2][poz1_x] == pole[poz1_y + 2][poz1_x - 1] and (
                            poz1_x == 2 or poz1_x == 4 or poz1_x == 6 or poz1_x == 8):
                        pole[poz1_y + 2][poz1_x] = v_par_kv2
                        pole[poz1_y + 3][poz1_x] = v_par_kv22
                        pole[poz1_y + 2][poz1_x - 1] = v_par_kv2
                        pole[poz1_y + 3][poz1_x - 1] = v_par_kv22
                    elif pole[poz1_y + 2][poz1_x] == pole[poz1_y + 2][poz1_x + 1] and (
                            poz1_x == 1 or poz1_x == 3 or poz1_x == 5 or poz1_x == 7):
                        pole[poz1_y + 2][poz1_x] = v_par_kv2
                        pole[poz1_y + 3][poz1_x] = v_par_kv22
                        pole[poz1_y + 2][poz1_x + 1] = v_par_kv2
                        pole[poz1_y + 3][poz1_x + 1] = v_par_kv22
            # если снизу квадрат противника и стоим не впритык
            elif pole[poz1_y + 2][poz1_x] == v_kvad and poz1_y != 5:
                # если снизу есть место для выталкивания
                if pole[poz1_y + 5][poz1_x] == pole[poz1_y + 4][poz1_x] == 0:
                    if pole[poz1_y + 2][poz1_x - 1] == v_kvad and poz1_x in spisok:  # если остальная часть слева
                        pole[poz1_y + 4][poz1_x] = v_par_vert
                        pole[poz1_y + 5][poz1_x] = v_par_vert2
                        pole[poz1_y + 2][poz1_x - 1] = v_par_vert
                        pole[poz1_y + 3][poz1_x - 1] = v_par_vert2
                        pole[poz1_y + 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y + 3][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
                    elif pole[poz1_y + 2][poz1_x + 1] == v_kvad and poz1_x not in spisok:  # если остальная часть справа
                        pole[poz1_y + 4][poz1_x] = v_par_vert
                        pole[poz1_y + 5][poz1_x] = v_par_vert2
                        pole[poz1_y + 2][poz1_x + 1] = v_par_vert
                        pole[poz1_y + 3][poz1_x + 1] = v_par_vert2
                        pole[poz1_y + 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y + 3][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
            elif pole[poz1_y + 2][poz1_x] == v_kvad and poz1_y == 5:  # если снизу квадрат противника и стоим впритык
                if pole[poz1_y + 4][poz1_x] == 0:
                    if pole[poz1_y + 2][poz1_x - 1] == v_kvad and poz1_x in spisok:
                        pole[poz1_y + 2][poz1_x - 1] = v_par_vert
                        pole[poz1_y + 3][poz1_x - 1] = v_par_vert2
                        pole[poz1_y + 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y + 3][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
                    elif pole[poz1_y + 2][poz1_x + 1] == v_kvad and poz1_x not in spisok:
                        pole[poz1_y + 2][poz1_x + 1] = v_par_vert
                        pole[poz1_y + 3][poz1_x + 1] = v_par_vert2
                        pole[poz1_y + 2][poz1_x] = pole[poz1_y][poz1_x]
                        pole[poz1_y + 3][poz1_x] = pole[poz1_y + 1][poz1_x]
                        pole[poz1_y][poz1_x] = 0
                        pole[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 9 and pole[9][8] == 0 and pole[9][7] == 0:
            pole[9][7] = v_ugol1
            pole[9][8] = v_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y + 1][poz1_x] = 0
        elif poz1_x == 0 and pole[9][1] == 0 and pole[9][2] == 0:
            pole[9][1] = v_ugol1
            pole[9][2] = v_ugol2
            pole[poz1_y][poz1_x] = 0
            pole[poz1_y + 1][poz1_x] = 0


# Функция для всех квадратов. Правила хода
def vmeste(poz1_x, poz1_y, poz2_x, poz2_y):
    a1 = 0  # параметр для событий
    par_gor = 0
    par_vert = 0
    par_kv1 = 0
    par_kv2 = 0
    if f_hi:  # если ход игрока
        par_gor = 3
        par_vert = 4
        par_kv1 = 13
        par_kv2 = 15
    if f_hi == 0 or f_hi ==2:  # если ход компьютера
        par_gor = 1
        par_vert = 2
        par_kv1 = 9
        par_kv2 = 11
    # ДВИЖЕНИЕ ВНИЗ down
    if ((poz2_y == poz1_y + 2 and poz2_x == poz1_x) or (poz2_y == poz1_y + 3 and poz2_x == poz1_x) or (
            poz2_y == poz1_y + 2 and poz2_x == poz1_x + 1) or (poz2_y == poz1_y + 3 and poz2_x == poz1_x + 1)):
        if poz1_y != 7:  # проверка выхода квадрата на базу +
            # если снизу горизонтальная фишка внизу квадрата
            if pole[poz1_y + 3][poz1_x] == par_gor and pole[poz1_y + 2][poz1_x] == 0:
                if pole[poz1_y + 4][poz1_x] == pole[poz1_y + 4][poz1_x + 1] == 0:  # проверка места для сдвига
                    pole[poz1_y + 4][poz1_x] = pole[poz1_y + 3][poz1_x]
                    pole[poz1_y + 4][poz1_x + 1] = pole[poz1_y + 3][poz1_x + 1]
                    a1 = 1
            # если снизу горизонтальная фишка сверху квадрата
            elif pole[poz1_y + 2][poz1_x] == par_gor and pole[poz1_y + 3][poz1_x] == 0:
                if pole[poz1_y + 4][poz1_x] == pole[poz1_y + 4][poz1_x + 1] == 0:  # проверка места для сдвига
                    pole[poz1_y + 4][poz1_x] = pole[poz1_y + 2][poz1_x]
                    pole[poz1_y + 4][poz1_x + 1] = pole[poz1_y + 2][poz1_x + 1]
                    a1 = 1
            # если снизу вертикальная фишка слева в квадрате
            elif pole[poz1_y + 2][poz1_x] == par_vert and pole[poz1_y + 2][poz1_x + 1] == 0:
                if poz1_y + 4 != 9:
                    if pole[poz1_y + 4][poz1_x] == 0 and pole[poz1_y + 5][poz1_x] == 0:
                        pole[poz1_y + 4][poz1_x] = pole[poz1_y + 2][poz1_x]
                        pole[poz1_y + 5][poz1_x] = pole[poz1_y + 3][poz1_x]
                        a1 = 1
                else:
                    if pole[poz1_y + 4][poz1_x] == pole[poz1_y + 4][poz1_x + 1]:
                        a1 = 1
            # если снизу вертикальная фишка справа в квадрате
            elif pole[poz1_y + 2][poz1_x + 1] == par_vert and pole[poz1_y + 2][poz1_x] == 0:
                if poz1_y + 4 != 9:
                    if pole[poz1_y + 4][poz1_x + 1] == 0 and pole[poz1_y + 5][poz1_x + 1] == 0:
                        pole[poz1_y + 4][poz1_x + 1] = pole[poz1_y + 2][poz1_x + 1]
                        pole[poz1_y + 5][poz1_x + 1] = pole[poz1_y + 3][poz1_x + 1]
                        a1 = 1
                else:
                    if pole[poz1_y + 4][poz1_x] == pole[poz1_y + 4][poz1_x + 1]:
                        a1 = 1
            # если снизу квадрат противника 13 14 15 16
            elif pole[poz1_y + 2][poz1_x] == par_kv1 or pole[poz1_y + 2][poz1_x] == par_kv2:
                if poz1_y + 4 != 9:
                    if pole[poz1_y + 4][poz1_x] == pole[poz1_y + 4][poz1_x + 1] == pole[poz1_y + 5][poz1_x]:
                        pole[poz1_y + 4][poz1_x] = pole[poz1_y + 2][poz1_x]
                        pole[poz1_y + 4][poz1_x + 1] = pole[poz1_y + 2][poz1_x + 1]
                        pole[poz1_y + 5][poz1_x] = pole[poz1_y + 3][poz1_x]
                        pole[poz1_y + 5][poz1_x + 1] = pole[poz1_y + 3][poz1_x + 1]
                        a1 = 1
                else:
                    if pole[poz1_y + 4][poz1_x] == pole[poz1_y + 4][poz1_x + 1]:
                        a1 = 1
            # проверка пустых клеток снизу
            elif pole[poz1_y + 3][poz1_x] == pole[poz1_y + 2][poz1_x] == 0:
                if pole[poz1_y + 3][poz1_x + 1] == pole[poz1_y + 2][poz1_x + 1] == 0:
                    a1 = 1
            if a1 == 1:  # если хотя бы одно произошло событие сверху, то происходит ход.
                pole[poz1_y + 2][poz1_x] = pole[poz1_y][poz1_x]
                pole[poz1_y + 2][poz1_x + 1] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y + 3][poz1_x] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y + 3][poz1_x + 1] = pole[poz1_y + 1][poz1_x + 1]
                pole[poz1_y + 1][poz1_x + 1] = 0
                pole[poz1_y + 1][poz1_x] = 0
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if pole[poz1_y + 2][poz1_x] == par_gor:  # pole[poz1_y + 2][poz1_x+1] == 6
                pole[poz1_y + 2][poz1_x] = 0
                pole[poz1_y + 2][poz1_x + 1] = 0
    # ДВИЖЕНИЕ ВВЕРХ up
    elif ((poz2_y == poz1_y - 1 and poz2_x == poz1_x) or (poz2_y == poz1_y - 2 and poz2_x == poz1_x) or (
            poz2_y == poz1_y - 1 and poz2_x == poz1_x + 1) or (poz2_y == poz1_y - 2 and poz2_x == poz1_x + 1)):
        if poz1_y - 1 != 0:  # проверка выхода квадрата на базу
            # если сверху горизонтальная фишка внизу квадрата
            if pole[poz1_y - 1][poz1_x] == par_gor and pole[poz1_y - 2][poz1_x] == 0:
                if pole[poz1_y - 3][poz1_x] == 0 and pole[poz1_y - 3][poz1_x + 1] == 0:
                    pole[poz1_y - 3][poz1_x] = pole[poz1_y - 1][poz1_x]
                    pole[poz1_y - 3][poz1_x + 1] = pole[poz1_y - 1][poz1_x + 1]
                    a1 = 1
            # если сверху горизонтальная фишка сверху квадрата
            elif pole[poz1_y - 2][poz1_x] == par_gor and pole[poz1_y - 1][poz1_x] == 0:
                if pole[poz1_y - 3][poz1_x] == 0 and pole[poz1_y - 3][poz1_x + 1] == 0:
                    pole[poz1_y - 3][poz1_x] = pole[poz1_y - 2][poz1_x]
                    pole[poz1_y - 3][poz1_x + 1] = pole[poz1_y - 2][poz1_x + 1]
                    a1 = 1
            # если сверху вертикальная фишка слева в квадрате
            elif pole[poz1_y - 2][poz1_x] == par_vert and pole[poz1_y - 2][poz1_x + 1] == 0:
                if poz1_y - 3 > 0:
                    if pole[poz1_y - 3][poz1_x] == 0 and pole[poz1_y - 4][poz1_x] == 0:
                        pole[poz1_y - 3][poz1_x] = pole[poz1_y - 1][poz1_x]
                        pole[poz1_y - 4][poz1_x] = pole[poz1_y - 2][poz1_x]
                        a1 = 1
                else:
                    if pole[poz1_y - 3][poz1_x] == pole[poz1_y - 3][poz1_x + 1]:
                        a1 = 1
            # если сверху вертикальная фишка справа в квадрате
            elif pole[poz1_y - 2][poz1_x + 1] == par_vert and pole[poz1_y - 2][poz1_x] == 0:
                if poz1_y - 3 > 0:
                    if pole[poz1_y - 3][poz1_x + 1] == 0 and pole[poz1_y - 4][poz1_x + 1] == 0:
                        pole[poz1_y - 3][poz1_x + 1] = pole[poz1_y - 1][poz1_x + 1]
                        pole[poz1_y - 4][poz1_x + 1] = pole[poz1_y - 2][poz1_x + 1]
                        a1 = 1
                else:
                    if pole[poz1_y - 3][poz1_x] == pole[poz1_y - 3][poz1_x + 1]:
                        a1 = 1
            # если сверху квадрат противника 13 14 15 16
            elif pole[poz1_y - 2][poz1_x] == par_kv1 or pole[poz1_y - 2][poz1_x] == par_kv2:
                if poz1_y - 3 > 0:
                    if pole[poz1_y - 3][poz1_x] == pole[poz1_y - 4][poz1_x] == pole[poz1_y - 4][poz1_x + 1] == 0:
                        pole[poz1_y - 4][poz1_x] = pole[poz1_y - 2][poz1_x]
                        pole[poz1_y - 4][poz1_x + 1] = pole[poz1_y - 2][poz1_x + 1]
                        pole[poz1_y - 3][poz1_x] = pole[poz1_y - 1][poz1_x]
                        pole[poz1_y - 3][poz1_x + 1] = pole[poz1_y - 1][poz1_x + 1]
                        a1 = 1
                else:
                    if pole[poz1_y - 3][poz1_x] == pole[poz1_y - 3][poz1_x + 1]:
                        a1 = 1
            # проверка пустых клеток сверху
            elif pole[poz1_y - 2][poz1_x] == pole[poz1_y - 1][poz1_x] == 0:
                if pole[poz1_y - 2][poz1_x + 1] == pole[poz1_y - 1][poz1_x + 1] == 0:
                    a1 = 1
            if a1 == 1:  # если хоть одно произошло событие сверху, то происходит ход.
                pole[poz1_y - 2][poz1_x] = pole[poz1_y][poz1_x]
                pole[poz1_y - 2][poz1_x + 1] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y - 1][poz1_x] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y - 1][poz1_x + 1] = pole[poz1_y + 1][poz1_x + 1]
                pole[poz1_y + 1][poz1_x + 1] = 0
                pole[poz1_y + 1][poz1_x] = 0
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if pole[poz1_y - 1][poz1_x] == par_gor:
                pole[poz1_y - 1][poz1_x] = 0
                pole[poz1_y - 1][poz1_x + 1] = 0
    # ДВИЖЕИЕ ВЛЕВО left
    elif ((poz2_y == poz1_y and poz2_x == poz1_x - 1) or (poz2_y == poz1_y and poz2_x == poz1_x - 2) or (
            poz2_y == poz1_y + 1 and poz2_x == poz1_x - 1) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x - 2)):
        if poz1_x != 1:  # заход на базу
            # если слева вертикальная фишка слева квадрата
            if pole[poz1_y][poz1_x - 2] == par_vert and pole[poz1_y][poz1_x - 1] == 0:
                if pole[poz1_y][poz1_x - 3] == 0 and pole[poz1_y + 1][poz1_x - 3] == 0:
                    pole[poz1_y][poz1_x - 3] = pole[poz1_y][poz1_x - 2]
                    pole[poz1_y + 1][poz1_x - 3] = pole[poz1_y + 1][poz1_x - 2]
                    a1 = 1
            # если слева вертикальная фишка справа квадрата
            elif pole[poz1_y][poz1_x - 1] == par_vert and pole[poz1_y][poz1_x - 2] == 0:
                if pole[poz1_y][poz1_x - 3] == 0 and pole[poz1_y + 1][poz1_x - 3] == 0:
                    pole[poz1_y][poz1_x - 3] = pole[poz1_y][poz1_x - 1]
                    pole[poz1_y + 1][poz1_x - 3] = pole[poz1_y + 1][poz1_x - 1]
                    a1 = 1
            # если слева горизонтальная фишка сверху в квадрате
            elif pole[poz1_y][poz1_x - 2] == par_gor and pole[poz1_y + 1][poz1_x - 2] == 0:
                if poz1_x - 3 > 0:  # fix
                    if pole[poz1_y][poz1_x - 3] == 0 and pole[poz1_y][poz1_x - 4] == 0:
                        pole[poz1_y][poz1_x - 3] = pole[poz1_y][poz1_x - 1]
                        pole[poz1_y][poz1_x - 4] = pole[poz1_y][poz1_x - 2]
                        a1 = 1
                else:
                    if pole[poz1_y][poz1_x - 3] == pole[poz1_y + 1][poz1_x - 3]:
                        a1 = 1
            # если слева горизонтальная фишка снизу в квадрате
            elif pole[poz1_y + 1][poz1_x - 2] == par_gor and pole[poz1_y][poz1_x - 2] == 0:
                if poz1_x - 3 > 0:
                    if pole[poz1_y + 1][poz1_x - 3] == 0 and pole[poz1_y + 1][poz1_x - 4] == 0:
                        pole[poz1_y + 1][poz1_x - 3] = pole[poz1_y + 1][poz1_x - 1]
                        pole[poz1_y + 1][poz1_x - 4] = pole[poz1_y + 1][poz1_x - 2]
                        a1 = 1
                else:
                    if pole[poz1_y][poz1_x - 3] == pole[poz1_y + 1][poz1_x - 3]:
                        a1 = 1
            # если слева квадрат противника 13 14 15 16
            elif pole[poz1_y][poz1_x - 2] == par_kv1 or pole[poz1_y][poz1_x - 2] == par_kv2:
                if poz1_x - 3 > 0:
                    if pole[poz1_y][poz1_x - 3] == pole[poz1_y][poz1_x - 4] == pole[poz1_y + 1][poz1_x - 4] == 0:
                        pole[poz1_y][poz1_x - 4] = pole[poz1_y][poz1_x - 2]
                        pole[poz1_y + 1][poz1_x - 4] = pole[poz1_y + 1][poz1_x - 2]
                        pole[poz1_y][poz1_x - 3] = pole[poz1_y][poz1_x - 1]
                        pole[poz1_y + 1][poz1_x - 3] = pole[poz1_y + 1][poz1_x - 1]
                        a1 = 1
                else:
                    if pole[poz1_y][poz1_x - 3] == pole[poz1_y + 1][poz1_x - 3]:
                        a1 = 1
            # проверка пустых клеток слева
            elif pole[poz1_y][poz1_x - 2] == pole[poz1_y][poz1_x - 1] == 0:
                if pole[poz1_y + 1][poz1_x - 2] == pole[poz1_y + 1][poz1_x - 1] == 0:
                    a1 = 1
            if a1 == 1:  # если хоть одно произошло событие сверху, то происходит ход.
                pole[poz1_y][poz1_x - 2] = pole[poz1_y][poz1_x]
                pole[poz1_y][poz1_x - 1] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y + 1][poz1_x - 2] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y + 1][poz1_x - 1] = pole[poz1_y + 1][poz1_x + 1]
                pole[poz1_y + 1][poz1_x + 1] = 0
                pole[poz1_y + 1][poz1_x] = 0
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if pole[poz1_y][poz1_x - 1] == par_vert:
                pole[poz1_y][poz1_x - 1] = 0
                pole[poz1_y + 1][poz1_x - 1] = 0
    # ДВИЖЕИЕ ВПРАВО right
    elif ((poz2_y == poz1_y and poz2_x == poz1_x + 2) or (poz2_y == poz1_y and poz2_x == poz1_x + 3) or (
            poz2_y == poz1_y + 1 and poz2_x == poz1_x + 2) or (poz2_y == poz1_y + 1 and poz2_x == poz1_x + 3)):
        if poz1_x != 7:
            # если справа вертикальная фишка справа квадрата
            if pole[poz1_y][poz1_x + 3] == par_vert and pole[poz1_y][poz1_x + 2] == 0:
                if pole[poz1_y][poz1_x + 4] == 0 and pole[poz1_y + 1][poz1_x + 4] == 0:
                    pole[poz1_y][poz1_x + 4] = pole[poz1_y][poz1_x + 3]
                    pole[poz1_y + 1][poz1_x + 4] = pole[poz1_y + 1][poz1_x + 3]
                    a1 = 1
            # если справа вертикальная фишка слева квадрата
            elif pole[poz1_y][poz1_x + 2] == par_vert and pole[poz1_y][poz1_x + 3] == 0:
                if pole[poz1_y][poz1_x + 4] == 0 and pole[poz1_y + 1][poz1_x + 4] == 0:
                    pole[poz1_y][poz1_x + 4] = pole[poz1_y][poz1_x + 2]
                    pole[poz1_y + 1][poz1_x + 4] = pole[poz1_y + 1][poz1_x + 2]
                    a1 = 1
            # если справа горизонтальная фишка сверху в квадрате
            elif pole[poz1_y][poz1_x + 2] == par_gor and pole[poz1_y + 1][poz1_x + 2] == 0:
                if poz1_x + 4 != 9:  # чтобы исключения не выдавало
                    if pole[poz1_y][poz1_x + 5] == 0 and pole[poz1_y][poz1_x + 4] == 0:
                        pole[poz1_y][poz1_x + 5] = pole[poz1_y][poz1_x + 3]
                        pole[poz1_y][poz1_x + 4] = pole[poz1_y][poz1_x + 2]
                        a1 = 1
                else:
                    if pole[poz1_y][poz1_x + 4] == pole[poz1_y + 1][poz1_x + 4]:
                        a1 = 1
            # если справа горизонтальная фишка снизу в квадрате
            elif pole[poz1_y + 1][poz1_x + 2] == par_gor and pole[poz1_y][poz1_x + 2] == 0:
                if poz1_x + 4 != 9:  # чтобы исключения не выдавало
                    if pole[poz1_y + 1][poz1_x + 5] == 0 and pole[poz1_y + 1][poz1_x + 4] == 0:
                        pole[poz1_y + 1][poz1_x + 5] = pole[poz1_y + 1][poz1_x + 3]
                        pole[poz1_y + 1][poz1_x + 4] = pole[poz1_y + 1][poz1_x + 2]
                        a1 = 1
                else:
                    if pole[poz1_y][poz1_x + 4] == pole[poz1_y + 1][poz1_x + 4]:
                        a1 = 1
            # если справа квадрат противника 13 14 15 16
            elif pole[poz1_y][poz1_x + 2] == par_kv1 or pole[poz1_y][poz1_x + 2] == par_kv2:
                if poz1_x + 4 != 9:
                    if pole[poz1_y][poz1_x + 5] == pole[poz1_y + 1][poz1_x + 4] == 0 == pole[poz1_y][poz1_x + 4]:
                        pole[poz1_y][poz1_x + 4] = pole[poz1_y][poz1_x + 2]
                        pole[poz1_y + 1][poz1_x + 4] = pole[poz1_y + 1][poz1_x + 2]
                        pole[poz1_y][poz1_x + 5] = pole[poz1_y][poz1_x + 3]
                        pole[poz1_y + 1][poz1_x + 5] = pole[poz1_y + 1][poz1_x + 3]
                        a1 = 1
                else:
                    if pole[poz1_y][poz1_x + 4] == pole[poz1_y + 1][poz1_x + 4]:
                        a1 = 1
            # проверка пустых клеток справа
            elif pole[poz1_y][poz1_x + 2] == pole[poz1_y][poz1_x + 3] == 0:
                if pole[poz1_y + 1][poz1_x + 2] == pole[poz1_y + 1][poz1_x + 3] == 0:
                    a1 = 1
            if a1 == 1:  # если хоть одно произошло событие сверху, то происходит ход.
                pole[poz1_y][poz1_x + 2] = pole[poz1_y][poz1_x]
                pole[poz1_y][poz1_x + 3] = pole[poz1_y][poz1_x + 1]
                pole[poz1_y + 1][poz1_x + 2] = pole[poz1_y + 1][poz1_x]
                pole[poz1_y + 1][poz1_x + 3] = pole[poz1_y + 1][poz1_x + 1]
                pole[poz1_y + 1][poz1_x] = 0
                pole[poz1_y + 1][poz1_x + 1] = 0
                pole[poz1_y][poz1_x] = 0
                pole[poz1_y][poz1_x + 1] = 0
        else:  # выбиваем врага с базы
            if pole[poz1_y][poz1_x + 2] == par_vert:
                pole[poz1_y][poz1_x + 2] = 0
                pole[poz1_y + 1][poz1_x + 2] = 0


# определяет параметры запуска
def clicked_start():
    global mashtab, res1
    global par_V
    global res
    if rad == 2: # игра с игроком. f_hi 1 f_hi 2
        res = txt.get()
        res = int(res)
        res1 = '{}'.format(combo.get())
    elif rad == 1: # игра с компьютером. f_hi 1 f_hi 0
        res = txt1
        res = int(res)
        res1 = combo1

    if 600 <= res <= 1000:
        mashtab = res
        if res1 == '0 - Медленный вариант':
            par_V = 0
        elif res1 == '1 - Стандартный вариант':
            par_V = 1
        elif res1 == '2 - Быстрый вариант':
            par_V = 2
        root.geometry(f'{int(1.8 * res)}x{int(res * 1.1)}')
        nachalo()
    else:
        messagebox.showinfo('Оповещение', 'Введите значение от 600 до 1000')



# вывод второго окна при игре с компом
def clicked_pvc():
    global btn1 , txt1, combo1
    global selected
    if rad == 1:
        txt1= txt.get()
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

        selected = IntVar()  # параметры для функции complexity
        rad1 = Radiobutton(root, text='Первый', value=1, variable=selected, command=complexity)  # light
        rad2 = Radiobutton(root, text='Второй', value=2, variable=selected, command=complexity)  # Medium
        rad3 = Radiobutton(root, text='Третий', value=3, variable=selected, command=complexity)  # Hard

        lbl_0 = Label(root, text="                   \n\n", font=("Arial Bold", 20))
        lbl_01 = Label(root, text="                   ", font=("Arial Bold", 5))
        lbl_02 = Label(root, text="                   ", font=("Arial Bold", 10))
        lbl_1 = Label(root, anchor=CENTER, text="Укажи уровень сложности компьютера", font=("Arial Bold", 20))
        btn1 = Button(root, text="Готово", command=clicked_start, state=DISABLED)  #
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
def clicked_vibor():
    global rad
    btn.configure(state=NORMAL)
    rad = selected_1.get()


# определяет сложность компьютера
def complexity():
    global rad1
    btn1.configure(state=NORMAL)
    rad1 = selected.get()


# создание окна
root = Tk()
root.title("Добро пожаловать в приложение 'Yurki v(1.0)'")  # тайтл окна
root.geometry('800x500')  # размер окна

combo = Combobox(root, width=50, height=50, font=20, justify=CENTER)  # панель выбора скорости игры
combo['values'] = ('0 - Медленный вариант', '1 - Стандартный вариант', '2 - Быстрый вариант')
combo.current(1)

txt = Entry(root, width=20, justify=CENTER, font=20)  # state='disabled' # панель выбора размера окна
txt.focus()
txt.insert(0, '700')

selected_1 = IntVar() # параметры выбора режима
rad_1 = Radiobutton(root, text='Игрок vs Компьютер', value=1, variable=selected_1, command=clicked_vibor)
rad_2 = Radiobutton(root, text='Игрок vs Игрок', value=2, variable=selected_1, command=clicked_vibor)

lbl = Label(root, text="      \n", font=("Arial Bold", 20))
lbl.grid(column=0, row=0)
lbl1 = Label(root, text="Укажи удобный для тебя масштаб окна от 600 до 1000", font=("Arial Bold", 20))
lbl1.grid(column=1, row=1)
txt.grid(column=1, row=2)
lbl2 = Label(root, text="      \n", font=("Arial Bold", 5))
lbl2.grid(column=1, row=3)
lbl3 = Label(root, text="Выбери скорость анимации фигур", font=("Arial Bold", 20))
lbl3.grid(column=1, row=4)
combo.grid(column=1, row=5)
lbl4 = Label(root, text="      \n", font=("Arial Bold", 5))
lbl4.grid(column=1, row=7)

lbl5 = Label(root, text="Выбери режим:", font=("Arial Bold", 20))
lbl5.grid(column=1, row=8)
rad_1.grid(column=1, row=9)
rad_2.grid(column=1, row=10)

lbl = Label(root, text="      \n", font=("Arial Bold", 5))
lbl.grid(column=1, row=12)
btn = Button(root, text="Готово", command=clicked_pvc, state=DISABLED) #
btn.grid(column=1, row=13)

root.mainloop()  # цикл отображения окна
