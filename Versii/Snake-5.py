import sys
import time
import random
import curses
from curses import textpad

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)

    # Инициализация цветовых пар
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Для головы змейки

    # Начальные параметры
    direction = curses.KEY_RIGHT
    score = 0
    start_time = time.time()
    difficulty = 1
    map_size = 'medium'
    paused = False
    apple_count = 2  # Начальное количество яблок
    apple_types = ['normal', 'big']  # Начальные типы яблок

    def create_apple(snake, box):
        while True:
            apple = [random.randint(box[0][0] + 1, box[1][0] - 1), random.randint(box[0][1] + 1, box[1][1] - 1)]
            if apple not in snake:
                return apple

    def create_apples(snake, box, apple_count, apple_types):
        apples = []
        for _ in range(apple_count):
            while True:
                apple = [random.randint(box[0][0] + 1, box[1][0] - 1), random.randint(box[0][1] + 1, box[1][1] - 1)]
                if apple not in snake and apple not in [a[0] for a in apples]:
                    apple_type = random.choice(apple_types)
                    apples.append((apple, apple_type))
                    break
        return apples

    def show_menu():
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        if h < 20 or w < 60:
            stdscr.addstr(0, 0, "Пожалуйста, измените размер окна терминала.")
            stdscr.refresh()
            stdscr.getch()
            sys.exit()

        # ASCII Art для "Snake Game"
        title = [
            "   _____             _         _____                      ",
            "  / ____|           | |       / ____|                     ",
            " | (___   __ _ _ __ | |_ ___ | |  __  __ _ _ __ ___   ___ ",
            "  \\___ \\ / _` | '_ \\| __/ _ \\| | |_ |/ _` | '_ ` _ \\ / _ \\",
            "  ____) | (_| | | | | ||  __/| |__| | (_| | | | | | |  __/",
            " |_____/ \\__,_|_| |_|\\__\\___| \\_____|\\__,_|_| |_| |_|\\___|"
        ]
        for i, line in enumerate(title):
            stdscr.addstr(h//2 - len(title) - 8 + i, max(0, w//2 - len(line)//2), line)

        menu_items = [
            "+---------------------------+",
            "|      ГЛАВНОЕ МЕНЮ         |",
            "+---------------------------+",
            "| 1. Начать игру            |",
            "| 2. Информация об игре     |",
            "| 3. Установить сложность   |",
            "| 4. Установить размер карты|",
            "| 5. Установить количество яблок|",
            "| 6. Установить типы яблок  |",
            "| 7. Выйти                  |",
            "+---------------------------+"
        ]
        for i, line in enumerate(menu_items):
            stdscr.addstr(h//2 + i, max(0, w//2 - len(line)//2), line)

        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('1'):
                return 'play'
            elif key == ord('2'):
                return 'info'
            elif key == ord('3'):
                return 'difficulty'
            elif key == ord('4'):
                return 'map_size'
            elif key == ord('5'):
                return 'apple_count'
            elif key == ord('6'):
                return 'apple_types'
            elif key == ord('7'):  # Исправлено
                return 'exit'

    def show_info():
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        info = [
            "Игра Змейка",
            "Разработчик: Stervar",
            "Описание : Классическая игра Змейка.",
            "Управление: W/↑ - вверх, S/↓ - вниз,",
            "A/← - влево, D/→ - вправо",
            "Пауза: P",
            "",
            "Нажмите любую клавишу, чтобы вернуться в меню."
        ]
        for i, line in enumerate(info):
            stdscr.addstr(h//2 - len(info)//2 + i, max(0, w//2 - len(line)//2), line)
        stdscr.refresh()
        stdscr.getch()

    def set_difficulty():
        nonlocal difficulty
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        options = [
            "+---------------------------+",
            "|     Выберите сложност:    |",
            "| 1. Легко                  |",
            "| 2. Средне                 |",
            "| 3. Сложно                 |",
            "+---------------------------+"
        ]
        for i, line in enumerate(options):
            stdscr.addstr (h//2 - len(options)//2 + i, max(0, w//2 - len(line)//2), line)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('1'):
                difficulty = 1
                return
            elif key == ord('2'):
                difficulty = 1.5
                return
            elif key == ord('3'):
                difficulty = 2
                return

    def set_map_size():
        nonlocal map_size
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        options = [
            "+---------------------------+",
            "|   Выберите размер карты:  |",
            "| 1. Маленький              |",
            "| 2. Средний                |",
            "| 3. Большой                |",
            "+---------------------------+"
        ]
        for i, line in enumerate(options):
            stdscr.addstr(h//2 - len(options)//2 + i, max(0, w//2 - len(line)//2), line)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('1'):
                map_size = 'small'
                return
            elif key == ord('2'):
                map_size = 'medium'
                return
            elif key == ord('3'):
                map_size = 'large'
                return

    def set_apple_count():
        nonlocal apple_count
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        options = [
            "+---------------------------+",
            "|  Выберите количество яблок:|",
            "| 1. 1                       |",
            "| 2. 2                       |",
            "| 3. 3                       |",
            "| 4. 4                       |",
            "| 5. 5                       |",
            "+---------------------------+"
        ]
        for i, line in enumerate(options):
            stdscr.addstr(h//2 - len(options)//2 + i, max(0, w//2 - len(line)//2), line)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('1'):
                apple_count = 1
                return
            elif key == ord('2'):
                apple_count = 2
                return
            elif key == ord('3'):
                apple_count = 3
                return
            elif key == ord('4'):
                apple_count = 4
                return
            elif key == ord('5'):
                apple_count = 5
                return

    def set_apple_types():
        nonlocal apple_types
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        options = [
            "+---------------------------+",
            "|  Выберите типы яблок:     |",
            "| 1. Обычные                |",
            "| 2. Обычные и большие      |",
            "| 3. Обычные, большие и супер|",
            "+---------------------------+"
        ]
        for i, line in enumerate(options):
            stdscr.addstr(h//2 - len(options)//2 + i, max(0, w//2 - len(line)//2), line)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('1'):
                apple_types = ['normal']
                return
            elif key == ord('2'):
                apple_types = ['normal', 'big']
                return
            elif key == ord('3'):
                apple_types = ['normal', 'big', 'super']
                return

    while True:
        action = show_menu ()
        if action == 'play':
            break
        elif action == 'info':
            show_info()
        elif action == 'difficulty':
            set_difficulty()
        elif action == 'map_size':
            set_map_size()
        elif action == 'apple_count':
            set_apple_count()
        elif action == 'apple_types':
            set_apple_types()
        elif action == 'exit':
            sys.exit()

    if map_size == 'small':
        sh, sw = 20, 40
    elif map_size == 'medium':
        sh, sw = 30, 60
    else:
        sh, sw = 40, 80

    w = sw - 2
    h = sh - 2

    box = [[1, 1], [h, w]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [[sh//2, sw//2]]
    apples = create_apples(snake, box, apple_count, apple_types)
    last_move_time = time.time()

    while True:
        current_time = time.time()
        stdscr.clear()
        textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
        stdscr.addstr(0, 0, f"Счет: {score} | Время: {int(current_time - start_time)} сек.")
        stdscr.addstr(0, w-5, "Выход: Q | Пауза: P")

        for i, (y, x) in enumerate(snake):
            if i == 0:
                stdscr.addch(y, x, '@', curses.color_pair(4))  # Голова
            else:
                stdscr.addch(y, x, '#', curses.color_pair(1))  # Тело

        for apple, apple_type in apples:
            if apple_type == 'normal':
                stdscr.addch(apple[0], apple[1], '*', curses.color_pair(2))
            elif apple_type == 'big':
                stdscr.addch(apple[0], apple[1], '*', curses.color_pair(3))
            elif apple_type == 'super':
                stdscr.addch(apple[0], apple[1], '*', curses.color_pair(4))

        stdscr.refresh()

        key = stdscr.getch()
        if key != -1:
            if key == ord('q'):
                break
            elif key == ord('p'):
                paused = not paused
                while paused:
                    stdscr.addstr(sh//2, sw//2 - 5, "Пауза. Нажмите P, чтобы продолжить.")
                    stdscr.refresh()
                    key = stdscr.getch()
                    if key == ord('p'):
                        paused = False
                        break
            elif key in [curses.KEY_UP, ord('w')] and direction != curses.KEY_DOWN:
                direction = curses.KEY_UP
            elif key in [curses.KEY_DOWN, ord('s')] and direction != curses.KEY_UP:
                direction = curses.KEY_DOWN
            elif key in [curses.KEY_LEFT, ord('a')] and direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT
            elif key in [curses.KEY_RIGHT, ord('d')] and direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT

        if current_time - last_move_time > 0.1 / difficulty and not paused:
            last_move_time = current_time
            head = snake[0]
            if direction == curses.KEY_UP:
                new_head = [head[0] -  1, head[1]]
                time.sleep(0.01)  # Добавить небольшую задержку для вертикального движения
            elif direction == curses.KEY_DOWN:
                new_head = [head[0] + 1, head[1]]
                time.sleep(0.01)  # Добавить небольшую задержку для вертикального движения
            elif direction == curses.KEY_LEFT:
                new_head = [head[0], head[1] - 1]
            elif direction == curses.KEY_RIGHT:
                new_head = [head[0], head[1] + 1]

            if new_head[0] < box[0][0] + 1:
                new_head[0] = box[1][0] - 1
            elif new_head[0] > box[1][0] - 1:
                new_head[0] = box[0][0] + 1
            if new_head[1] < box[0][1] + 1:
                new_head[1] = box[1][1] - 1
            elif new_head[ 1] > box[1][1] - 1:
                new_head[1] = box[0][1] + 1

            snake.insert(0, new_head)

            if snake[0] in snake[1:]:
                stdscr.addstr(sh//2, sw//2 - 5, "Вы проиграли!")
                stdscr.refresh()
                time.sleep(2)
                break
            for apple, apple_type in apples:
                if snake[0] == apple:
                    score += 1
                    apples.remove((apple, apple_type))
                    apples.append(create_apple(snake, box))
                    if apple_type == 'super':
                        snake.insert(0, [snake[0][0], snake[0][1]])  # Добавить дополнительный сегмент
                    break
            else:
                snake.pop()

        if len(snake) == w * h:
            stdscr.addstr(sh//2, sw//2 - 5, "Вы выиграли!")
            stdscr.refresh()
            time.sleep(2)
            break

curses.wrapper(main)