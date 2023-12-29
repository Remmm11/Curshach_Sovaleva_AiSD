import os
import hashlib
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def dismiss(win):
    win.grab_release()
    win.destroy()


class Checkers:
    def __init__(self, main):
        self.deck = None
        self.first_click = True
        self.main = main
        self.users = {}
        self.account = {}
        self.entry_login = ttk.Entry(width=30, justify='center')
        self.entry_password = ttk.Entry(width=30, justify='center')
        self.txt_login = Label(text='Логин', font='Arial 14 bold')
        self.txt_password = Label(text='Пароль', font='Arial 14 bold')
        self.button_registration = ttk.Button(text='Зарегистрироваться', command=lambda: self.regist())
        self.txt = Label(text='Для игры введите ваш логин и пароль', font='Arial 14 bold')
        self.button_autorisation = ttk.Button(text='Авторизоваться', command=lambda: self.authorization())

        self.txt.place(x=180, y=70)
        self.txt_login.place(x=230, y=120)
        self.txt_password.place(x=230, y=150)
        self.entry_login.place(x=310, y=123)
        self.entry_password.place(x=310, y=153)
        self.button_autorisation.place(x=260, y=210)
        self.button_registration.place(x=360, y=210)

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.field_model = [[0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                            [-1,  0, -1,  0, -1,  0, -1,  0, -1,  0],
                            [ 0, -1,  0, -1,  0, -1,  0, -1,  0, -1],
                            [-1,  0, -1,  0, -1,  0, -1,  0, -1,  0],
                            [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                            [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                            [ 0,  1,  0,  1,  0,  1,  0,  1,  0,  1],
                            [ 1,  0,  1,  0,  1,  0,  1,  0,  1,  0],
                            [ 0,  1,  0,  1,  0,  1,  0,  1,  0,  1],
                            [ 1,  0,  1,  0,  1,  0,  1,  0,  1,  0]]

        self.white_checker = PhotoImage(file="sprites/White.png")
        self.black_checker = PhotoImage(file="sprites/Black.png")
        self.white_queen = PhotoImage(file="sprites/White_Queen.png")
        self.black_queen = PhotoImage(file="sprites/Black_Queen.png")
        self.capture = PhotoImage(file="sprites/capture.png")
        self.field = PhotoImage(file="sprites/board.png")
        self.white_move = True
        self.black_move = False
        self.first_move = True
        self.move_without_attack = False

    # Методы для регистрации и авторизации.

    def authorization(self):
        login = self.entry_login.get()
        password = self.entry_password.get()
        password_code = hashlib.sha256(password.encode()).hexdigest()

        if len(login) == 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин и пароль")

        elif len(login) == 0 and len(password) != 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин")

        elif len(login) != 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите пароль")

        else:
            file = open('save/accounts.txt', 'r+')
            a = file.readline()[:-1].split(' ')

            while True:
                if a != ['']:
                    self.users[a[0]] = a[1]
                    a = file.readline()[:-1].split(' ')
                else:
                    break

            flag_reg = False
            flag_password = True
            for i in self.users.items():
                login_check, password_check = i
                if login == login_check and password_code == password_check:
                    flag_reg = True
                    break
                elif login == login_check and password_code != password:
                    flag_password = False

            if flag_reg:
                for widget in self.main.winfo_children():
                    widget.destroy()

                win = Toplevel()
                win.geometry('400x120+760+420')
                win.title('Успех')
                win.grab_set()
                win.protocol('WM_DELETE_WINDOW', lambda: dismiss(win))

                Label(win, text='Вы успешно авторизовались', font='Arial 14 bold').place(x=60, y=20)
                ttk.Button(win, text='Играть', command=lambda: self.drawing_field(win)).place(x=160, y=70)

            elif not flag_password:
                messagebox.showwarning(title="Ошибка", message="Неверный пароль")
            else:
                messagebox.showwarning(title="Ошибка", message="Такого аккаунта не существует")

    def regist(self):
        def registrate():
            s_l = login.get()
            s_p = password.get()
            password_code = hashlib.sha256(s_p.encode()).hexdigest()

            if len(s_l) == 0 or len(s_p) == 0:
                messagebox.showwarning(title='Ошибка', message='Поле заполнения пусто')
            else:
                file = open('save/accounts.txt', 'r+')
                a = file.readline()[:-1].split(' ')

                while True:
                    if a != ['']:
                        self.account[a[0]] = a[1]
                        a = file.readline()[:-1].split(' ')
                    else:
                        break

                f_reg = False

                for i in self.account.items():
                    l, p = i
                    if s_l == l:
                        f_reg = True

                if not f_reg:
                    file = open('save/accounts.txt', 'r+')
                    file.seek(0, os.SEEK_END)
                    file.write(f'{s_l} {password_code}\n')
                    file.close()

                    for widget in win.winfo_children():
                        widget.destroy()

                    Label(win, text='Вы успешно зарегистрировались', font='Arial 14 bold').place(x=140, y=120)
                    win.after(800, lambda: (win.destroy(), win.grab_release()))
                else:
                    messagebox.showwarning(title='Ошибка', message='Такой аккаунт уже существует')

        win = Toplevel()
        win.geometry('600x300+660+350')
        win.title('Регистрация')
        win.resizable(False, False)
        win.protocol('WM_DELETE_WINDOW', lambda: dismiss(win))
        win.grab_set()

        login = ttk.Entry(win, width=30, justify='center')
        password = ttk.Entry(win, width=30, justify='center')
        txt_login = Label(win, text='Логин', font='Arial 14 bold')
        txt_password = Label(win, text='Пароль', font='Arial 14 bold')
        txt = Label(win, text='Введите желаемые логин и пароль', font='Arial 14 bold')
        button_reg = ttk.Button(win, text='Зарегистрироваться', command=lambda: registrate())

        txt.place(x=135, y=70)
        txt_login.place(x=170, y=120)
        txt_password.place(x=170, y=150)
        login.place(x=250, y=123)
        password.place(x=250, y=153)
        button_reg.place(x=245, y=210)

    # Метод для вывода доски

    def drawing_field(self, win=None):
        win.after(200, lambda: (win.destroy(), win.grab_release()))
        self.main.title("Фризские шашки")
        self.main.geometry("870x870+500+50")
        cell_sz = 80
        row = 10
        col = 10

        self.deck = Canvas(self.main, width=870, height=870)
        cell_colors = ["#FFDDBB", "#552B00"]
        color_index = 0

        self.deck.create_image(0, 0, anchor="nw", image=self.field)

        for rows in range(row):
            for cols in range(col):
                x1, y1 = cols * cell_sz, rows * cell_sz
                cell = self.field_model[rows][cols]
                if cell < 0:
                    if cell == -1:
                        self.deck.create_image(x1 + 37, y1 + 37, anchor="nw", image=self.black_checker)
                    else:
                        pass

                elif cell > 0:
                    if cell == 1:
                        self.deck.create_image(x1 + 37, y1 + 37, anchor="nw", image=self.white_checker)
                    else:
                        pass

        self.deck.pack()
        self.interact()

    # Метод для отрисовки ходов

    def drawing_move(self):
        self.deck.delete("all")
        cell_colors = ["#FFDDBB", "#552B00"]
        color_index = 0
        cell_sz = 80
        row = 10
        col = 10

        self.deck.create_image(0, 0, anchor="nw", image=self.field)

        for rows in range(row):
            for cols in range(col):
                x1, y1 = cols * cell_sz, rows * cell_sz
                cell = self.field_model[rows][cols]
                if cell < 0:
                    if cell == -1:
                        self.deck.create_image(x1 + 37, y1 + 37, anchor="nw", image=self.black_checker)
                    elif cell == -2:
                        self.deck.create_image(x1 + 37, y1 + 37, anchor="nw", image=self.black_queen)

                elif cell > 0:
                    if cell == 1:
                        self.deck.create_image(x1 + 37, y1 + 37, anchor="nw", image=self.white_checker)
                    elif cell == 2:
                        self.deck.create_image(x1 + 37, y1 + 37, anchor="nw", image=self.white_queen)

        self.deck.pack()
        self.checkers_end()

    # Метод для взаимодействия с пользователями

    def interact(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        def queen_check(x2, y2):
            if self.white_move:
                if self.x2 == 0:
                    self.field_model[x2][y2] = 2
            else:
                if self.x2 == 9:
                    self.field_model[x2][y2] = -2

        def attack_check(x1, y1, x2, y2):
            coord_checkers_user = [x1, y1, x2, y2]
            coord_checkers = []
            if self.white_move:
                flag_white_attack = False
                for x in range(10):
                    for y in range(10):
                        if self.field_model[x][y] == 1:
                            for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1), (0, 2), (0, -2), (2, 0), (-2, 0):
                                if 0 <= (x + i) <= 9 and 0 <= (y + j) <= 9:
                                    if self.field_model[x + i][y + j] == -1 or self.field_model[x + i][y + j] == -2:
                                        if 0 <= (x + i * 2) <= 9 and 0 <= (y + j * 2) <= 9:
                                            if self.field_model[x + i + i][y + j + j] == 0:
                                                flag_white_attack = True
                                                coord_checkers.append([x, y, x + i + i, y + j + j])

                        elif self.field_model[x][y] == 2:
                            for d in range(4):
                                h = 0
                                if d == 0:
                                    i = 1
                                    j = 1
                                elif d == 1:
                                    i = 1
                                    j = -1
                                elif d == 2:
                                    i = -1
                                    j = 1
                                elif d == 3:
                                    i = -1
                                    j = -1

                                while 0 <= x + (i * h) + i <= 9 and 0 <= y + (j * h) + j <= 9:
                                    if self.field_model[x + (i * h)][y + (j * h)] == -1 or \
                                            self.field_model[x + (i * h)][y + (j * h)] == -2:
                                        if self.field_model[x + (i * h) + i][y + (j * h) + j] == 0:
                                            flag_white_attack = True
                                            h += 1
                                            while 0 <= x + (i * h) <= 9 and 0 <= y + (j * h) <= 9:
                                                if self.field_model[x + (i * h)][y + (j * h)] == 0:
                                                    coord_checkers.append([x, y, x + (i * h), y + (j * h)])
                                                else:
                                                    break
                                                h += 1
                                        else:
                                            break
                                    h += 1

                if not flag_white_attack:
                    return True
                else:
                    if coord_checkers_user in coord_checkers:
                        return True

            else:
                flag_black_attack = False
                for x in range(10):
                    for y in range(10):
                        if self.field_model[x][y] == -1:
                            for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1), (0, 2), (0, -2), (2, 0), (-2, 0):
                                if 0 <= (x + i) <= 9 and 0 <= (y + j) <= 9:
                                    if self.field_model[x + i][y + j] == 1 or self.field_model[x + i][y + j] == 2:
                                        if 0 <= (x + i * 2) <= 9 and 0 <= (y + j * 2) <= 9:
                                            if self.field_model[x + i + i][y + j + j] == 0:
                                                flag_black_attack = True
                                                coord_checkers.append([x, y, x + i + i, y + j + j])
                        elif self.field_model[x][y] == -2:
                            for d in range(4):
                                h = 0
                                if d == 0:
                                    i = 1
                                    j = 1
                                elif d == 1:
                                    i = 1
                                    j = -1
                                elif d == 2:
                                    i = -1
                                    j = 1
                                elif d == 3:
                                    i = -1
                                    j = -1

                                while 0 <= x + (i * h) + i <= 9 and 0 <= y + (j * h) + j <= 9:
                                    if self.field_model[x + (i * h)][y + (j * h)] == 1 or \
                                            self.field_model[x + (i * h)][y + (j * h)] == 2:
                                        if self.field_model[x + (i * h) + i][y + (j * h) + j] == 0:
                                            flag_black_attack = True
                                            h += 1
                                            while 0 <= x + (i * h) <= 9 and 0 <= y + (j * h) <= 9:
                                                if self.field_model[x + (i * h)][y + (j * h)] == 0:
                                                    coord_checkers.append([x, y, x + (i * h), y + (j * h)])
                                                else:
                                                    break
                                                h += 1
                                        else:
                                            break
                                    h += 1

                if not flag_black_attack:
                    return True
                else:
                    if coord_checkers_user in coord_checkers:
                        return True
                    else:
                        return False

        def multijump_check(x2, y2):
            if self.white_move:
                if self.field_model[x2][y2] == 1:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1), (0, 2), (0, -2), (2, 0), (-2, 0):
                        if 0 < (x2 + i) < 9 and 0 < (y2 + j) < 9:
                            if self.field_model[x2 + i][y2 + j] == -1 or self.field_model[x2 + i][y2 + j] == -2:
                                if 0 <= (x2 + i * 2) <= 9 and 0 <= (y2 + j * 2) <= 9:
                                    if self.field_model[x2 + i + i][y2 + j + j] == 0:
                                        return True
                elif self.field_model[x2][y2] == 2:
                    for d in range(4):
                        if d == 0:
                            i = 1
                            j = 1
                        elif d == 1:
                            i = 1
                            j = -1
                        elif d == 2:
                            i = -1
                            j = 1
                        elif d == 3:
                            i = -1
                            j = -1

                        for h in range(1, 9):
                            if 0 < x2 + (i * h) < 9 and 0 < y2 + (j * h) < 9:
                                if self.field_model[x2 + (i * h)][y2 + (j * h)] == -1 or \
                                        self.field_model[x2 + (i * h)][y2 + (j * h)] == -2:
                                    if self.field_model[x2 + (i * h) + i][y2 + (j * h) + j] == 0:
                                        return True
                                    else:
                                        break
                            else:
                                break

            else:
                if self.field_model[x2][y2] == -1:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1), (0, 2), (0, -2), (2, 0), (-2, 0):
                        if 0 < (x2 + i) < 9 and 0 < (y2 + j) < 9:
                            if self.field_model[x2 + i][y2 + j] == 1 or self.field_model[x2 + i][y2 + j] == 2:
                                if 0 <= (x2 + i * 2) <= 9 and 0 <= (y2 + j * 2) <= 9:
                                    if self.field_model[x2 + i + i][y2 + j + j] == 0:
                                        return True
                elif self.field_model[x2][y2] == -2:
                    for d in range(4):
                        if d == 0:
                            i = 1
                            j = 1
                        elif d == 1:
                            i = 1
                            j = -1
                        elif d == 2:
                            i = -1
                            j = 1
                        elif d == 3:
                            i = -1
                            j = -1

                        for h in range(1, 9):
                            if 0 < x2 + (i * h) < 9 and 0 < y2 + (j * h) < 9:
                                if self.field_model[x2 + (i * h)][y2 + (j * h)] == 1 or \
                                        self.field_model[x2 + (i * h)][y2 + (j * h)] == 2:
                                    if self.field_model[x2 + (i * h) + i][y2 + (j * h) + j] == 0:
                                        return True
                                    else:
                                        break
                            else:
                                break
            return False

        def move_check(x1, y1, x2, y2):
            self.move_without_attack = False
            if self.field_model[x2][y2] != 0:
                return False

            if self.field_model[x1][y1] == 2 or self.field_model[x1][y1] == -2:
                if abs(x1 - x2) == abs(y1 - y2):
                    count_queen = 0
                    coord_checker = []
                    i = 0
                    j = 0

                    if x1 < x2:
                        i = 1
                    elif x2 < x1:
                        i = -1
                    if y1 < y2:
                        j = 1
                    elif y2 < y1:
                        j = -1

                    for h in range(1, abs(x2 - x1) + 1):
                        if self.field_model[x1 + (i * h)][y1 + (j * h)] == 1 or self.field_model[x1 + (i * h)][
                            y1 + (j * h)] == 2:
                            if self.field_model[x1][y1] == 2:
                                return False
                            else:
                                count_queen += 1
                                coord_checker = [x1 + (i * h), y1 + (j * h)]

                        if self.field_model[x1 + (i * h)][y1 + (j * h)] == -1 or self.field_model[x1 + (i * h)][
                            y1 + (j * h)] == -2:
                            if self.field_model[x1][y1] == -2:
                                return False
                            else:
                                count_queen += 1
                                coord_checker = [x1 + (i * h), y1 + (j * h)]
                    print(count_queen, "г")
                    if count_queen == 1:
                        self.field_model[coord_checker[0]][coord_checker[1]] = 0
                        self.field_model[x2][y2] = self.field_model[x1][y1]
                        self.field_model[x1][y1] = 0
                        return True

                    elif count_queen > 1:
                        return False

                    else:
                        if attack_check(self.x1, self.y1, self.x2, self.y2):
                            self.field_model[x2][y2] = self.field_model[x1][y1]
                            self.field_model[x1][y1] = 0
                            self.move_without_attack = True
                            return True

            else:
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    if self.black_move:
                        if x2 < x1 and self.field_model[x1][y1] == -1:
                            return False
                    elif self.white_move:
                        if x1 < x2 and self.field_model[x1][y1] == 1:
                            return False
                    if attack_check(self.x1, self.y1, self.x2, self.y2):
                        self.field_model[x2][y2] = self.field_model[x1][y1]
                        self.field_model[x1][y1] = 0
                        self.move_without_attack = True
                        return True
                elif abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                    if self.field_model[(x1 + x2) // 2][(y1 + y2) // 2] == 0 or self.field_model[(x1 + x2) // 2][
                        (y1 + y2) // 2] == self.field_model[x1][y1]:
                        return False
                    self.field_model[x2][y2] = self.field_model[x1][y1]
                    self.field_model[x1][y1] = 0
                    self.field_model[(x1 + x2) // 2][(y1 + y2) // 2] = 0
                    return True
                elif abs(x2 - x1) == 4 and abs(y2 - y1) == 0:
                    if self.field_model[(x1 + x2) // 2][(y1 + y2) // 2] == 0 or self.field_model[(x1 + x2) // 2][
                        (y1 + y2) // 2] == self.field_model[x1][y1]:
                        return False
                    self.field_model[x2][y2] = self.field_model[x1][y1]
                    self.field_model[x1][y1] = 0
                    self.field_model[(x1 + x2) // 2][(y1 + y2) // 2] = 0
                    return True
                elif abs(x2 - x1) == 0 and abs(y2 - y1) == 4:
                    if self.field_model[(x1 + x2) // 2][(y1 + y2) // 2] == 0 or self.field_model[(x1 + x2) // 2][
                        (y1 + y2) // 2] == self.field_model[x1][y1]:
                        return False
                    self.field_model[x2][y2] = self.field_model[x1][y1]
                    self.field_model[x1][y1] = 0
                    self.field_model[(x1 + x2) // 2][(y1 + y2) // 2] = 0
                    return True
                return False

        def click_event_capt(event):
            if 35 < event.x < 835 and 0 < event.y < 835:
                self.y2 = (event.x - 35) // 80
                self.x2 = (event.y - 35) // 80
                if self.first_move:
                    if self.x1 == self.x2 and self.y1 == self.y2:
                        self.main.bind("<Button-1>", click_event)
                        self.drawing_move()

                    else:
                        if move_check(self.x1, self.y1, self.x2, self.y2):
                            print((self.x1, self.y1, self.x2, self.y2))
                            queen_check(self.x2, self.y2)
                            self.drawing_move()
                            if not self.move_without_attack:
                                if multijump_check(self.x2, self.y2):
                                    self.first_move = False
                                    self.x1, self.y1 = self.x2, self.y2
                                    self.deck.create_image(self.y1 * 80 + 35, self.x1 * 80 + 35, anchor="nw",
                                                           image=self.capture)
                                    self.main.bind("<Button-1>", click_event_capt)
                                else:
                                    self.white_move, self.black_move = not self.white_move, not self.black_move
                                    self.interact()
                            else:
                                self.white_move, self.black_move = not self.white_move, not self.black_move
                                self.interact()

                elif not self.first_move:
                    if move_check(self.x1, self.y1, self.x2, self.y2) and not self.move_without_attack:
                        queen_check(self.x2, self.y2)
                        self.drawing_move()
                        if multijump_check(self.x2, self.y2):
                            self.x1, self.y1 = self.x2, self.y2
                            self.deck.create_image(self.y1 * 80 + 35, self.x1 * 80 + 35, anchor="nw",
                                                   image=self.capture)
                            self.main.bind("<Button-1>", click_event_capt)
                        else:
                            self.drawing_move()
                            self.first_move = True
                            self.white_move, self.black_move = not self.white_move, not self.black_move
                            self.interact()

        def click_event(event):
            if 35 < event.x < 835 and 35 < event.y < 835:

                self.y1 = (event.x - 35) // 80
                self.x1 = (event.y - 35) // 80

                if self.white_move and (
                        self.field_model[self.x1][self.y1] == 1 or self.field_model[self.x1][self.y1] == 2):
                    self.deck.create_image(self.y1 * 80 + 35, self.x1 * 80 + 35, anchor="nw", image=self.capture)
                    self.main.bind("<Button-1>", click_event_capt)

                elif self.black_move and (
                        self.field_model[self.x1][self.y1] == -1 or self.field_model[self.x1][self.y1] == -2):
                    self.deck.create_image(self.y1 * 80 + 35, self.x1 * 80 + 35, anchor="nw", image=self.capture)
                    self.main.bind("<Button-1>", click_event_capt)

        self.main.bind("<Button-1>", click_event)

    # Метод для проверки окончания игры

    def checkers_end(self):
        flag_white_move = False
        flag_black_move = False
        for x in range(10):
            for y in range(10):
                if self.field_model[x][y] == 1 or self.field_model[x][y] == 2:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                        if 0 <= (x + i) <= 7 and 0 <= (y + j) <= 9:

                            if self.field_model[x + i][y + j] == -1 or self.field_model[x + i][y + j] == -2:
                                if 0 <= (x + i * 2) <= 7 and 0 < (y + j * 2) <= 9:
                                    if self.field_model[x + i + i][y + j + j] == 0:
                                        flag_white_move = True
                                        break
                            elif self.field_model[x + i][y + j] == 0:
                                flag_white_move = True
                                break

                elif self.field_model[x][y] == -1 or self.field_model[x][y] == -2:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                        if 0 <= (x + i) <= 7 and 0 <= (y + j) <= 9:
                            if self.field_model[x + i][y + j] == 1 or self.field_model[x + i][y + j] == 2:
                                if 0 <= (x + i * 2) <= 7 and 0 <= (y + j * 2) <= 9:
                                    if self.field_model[x + i + i][y + j + j] == 0:
                                        flag_black_move = True
                                        break
                            elif self.field_model[x + i][y + j] == 0:
                                flag_black_move = True
                                break

        if not flag_white_move:
            self.end_game("Чёрных")
        elif not flag_black_move:
            self.end_game("Белых")
        elif not flag_white_move and not flag_black_move:
            self.end_game("Ничья")

    # Метод для вывода результатов окончания игры

    def end_game(self, winner):
        winner_window = Tk()
        winner_window.geometry("150x150+600+300")
        winner_window.protocol('WM_DELETE_WINDOW', lambda: dismiss(winner_window))
        winner_window.grab_set()

        self.white_move = False
        self.black_move = True
        self.first_move = True

        self.field_model = [[0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                            [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
                            [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                            [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]

        if winner == "Ничья":
            Label(winner_window, text="Ничья").pack()
        else:
            Label(winner_window, text=f"Победа {winner}").pack()
        ttk.Button(winner_window, text="Заново",
                   command=lambda: (winner_window.grab_release(), winner_window.destroy(), self.drawing_move())).pack()


root = Tk()
root.title("Авторизация")
root.geometry('720x300+600+350')
root.resizable(False, False)

Checkers(root)

root.mainloop()
