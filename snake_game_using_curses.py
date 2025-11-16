import random
import curses
import time

# CUSTOM - SETTINGS
import os; os.system("cls" if os.name == "nt" else "clear")
blnFlatEarther = False        # Default = True
blnEmaciatingSnake = True    # Default = False
strSnakeBody = "█"          # Default = "#"
intMillisecondDelay = 100   # Default = 100

#initialize screen
sc = curses.initscr()
h, w = sc.getmaxyx()
win = curses.newwin(h, w, 0, 0)

win.keypad(1)
curses.noecho()   # CUSTOM - Suppresses unwanted terminal output when pressing keys other than the directional arrows.
curses.curs_set(0)

# CUSTOM - Mouse click to start - Useful because it forces the user to bring the terminal into UI focus, so the keyboard inputs actually work.
curses.mousemask(curses.ALL_MOUSE_EVENTS) # Enables mouse clicks
win.addstr(h//2, w//2 - 10, "Click anywhere to begin...")
win.refresh() # Draws any outstanding queues of strings, simultaneously.
while win.getch() != curses.KEY_MOUSE: pass # Loops until mouse click
win.addstr(h // 2, w // 2 - 10, " " * 26)

# Initial Snake and Apple position
snake_head = [10%h,15%w]
snake_position = [[15%h,10%w],[14%h,10%w],[13%h,10%w]]
apple_position = [int(.2*h),int(.2*w)]
score = 0

# display apple
win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)

prev_button_direction = 1
button_direction = 1
key = curses.KEY_RIGHT

def collision_with_apple(score):
    apple_position = [random.randint(1,h-2),random.randint(1,w-2)]
    score += 1
    return apple_position, score

def collision_with_boundaries(snake_head):
    if snake_head[0]>=h-1 or snake_head[0]<=0 or snake_head[1]>=w-1 or snake_head[1]<=0 :
      return 1
    else:
      return 0

def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
      return 1
    else:
      return 0

while True:
    win.border()  # To customise: win.border() takes 8 string parameters to draw a border for each edge and corner. Alternatively: win.border(*["."]*8)
    win.timeout(intMillisecondDelay)  # CUSTOM (changed fixed 100 ms to variable specified integer)

    next_key = win.getch()

    if next_key == -1:
      key = key
    else:
      key = next_key

    # 0-Left, 1-Right, 3-Up, 2-Down
    if key == curses.KEY_LEFT and prev_button_direction != 1:
      button_direction = 0
    elif key == curses.KEY_RIGHT and prev_button_direction != 0:
      button_direction = 1
    elif key == curses.KEY_UP and prev_button_direction != 2:
      button_direction = 3
    elif key == curses.KEY_DOWN and prev_button_direction != 3:
      button_direction = 2
    elif key == 27:   # CUSTOM - End game on the ESC escape key
      break
    else:
      pass

    prev_button_direction = button_direction

    # Change the head position based on the button direction
    if button_direction == 1:
      snake_head[1] += 1
    elif button_direction == 0:
      snake_head[1] -= 1
    elif button_direction == 2:
      snake_head[0] += 1
    elif button_direction == 3:
      snake_head[0] -= 1

    # CUSTOM - Borderless
    if not blnFlatEarther and collision_with_boundaries(snake_head) == 1:
      # h = number of vertical pixels, w = number of horizontal pixels, zero-indexing makes the head position possible from [0...h-1] and [0...w-1]
      snake_head[0] = (snake_head[0] % (h-2) - 1) % (h-2) + 1   # Since the boundary borders are in positions 0 and (h or w)-1, the snake is only permitted in the range [1...(h or w)-2]
      snake_head[1] = (snake_head[1] % (w-2) - 1) % (w-2) + 1   # Genius code: The pair of modulo functions shift an out-of-bounds position back in bounds, at the opposite end. If the axis was already in bounds, it stays in the same position.
    
    # Increase Snake length on eating apple
    if snake_head == apple_position:
      apple_position, score = collision_with_apple(score)
      snake_position.insert(0, list(snake_head))
      win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)

    else:
      snake_position.insert(0, list(snake_head))
      last = snake_position.pop()
      if last != apple_position:          # CUSTOM: Patches the invisible apple glitch
        win.addch(last[0], last[1], ' ')
    
    # CUSTOM - Shrinking Snake
    if blnEmaciatingSnake and collision_with_self(snake_position) == 1:
      snake_position.pop(0)                 # Removes head from the collision position, thus shrinking its length
      snake_head[0], snake_head[1] = snake_position[0][0], snake_position[0][1] # Return head to previous position
      score -= 1                            # Since the length has been decreased by 1, so does the score

    # display snake
    win.addch(snake_position[0][0], snake_position[0][1], strSnakeBody)   # CUSTOM Snake Body Character

    # On collision kill the snake
    if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
      break

sc.addstr(h//2, w//2 - 9, 'Your Score is:  '+str(score))    ## Shifted score position to be centred
sc.refresh()
time.sleep(2)
curses.endwin()