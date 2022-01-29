from termcolor import colored
from shapes import ColorPalette, Square, Straight, Tee, Ell, Jay, Ess, Zee
from pynput import keyboard
import time
import copy
import os
import random

class Board:
  def __init__(self, num_col, num_row, speed=0.5, debug=False, increment=1.1):
    self.max_row = num_row - 1
    self.max_col = num_col - 1
    print(f'{self.max_col = }, {self.max_row = }')
    self.single_col = [0 for _ in range(num_row)]
    self.board = [copy.deepcopy(self.single_col) for _ in range(num_col)]
    self.__speed__ = speed
    self.debug = debug
    self.printed = False
    self.paused = False
    self.quit = False
    self.cur_piece = None
    self.piece_is_printed = False
    self.moves = [0, 0, 0, 0] # [left, right, drop, rotate]
    self.score = 0
    self.level = 1
    self.increment = increment
    self.num_pieces_placed = 0
    if debug:
      self.__EMPTY__ = '0 '
      self.__BLOCK__ = '[]'
    else:
      self.__EMPTY__ = '  '
      self.__BLOCK__ = '██'



  def show_dot_pot(self):
    master_out = ''
    for r,col in enumerate(self.board):
      for c,val in enumerate(col):
        master_out += f'({r},{c}:{val}) '
      master_out += '\n'
    
    print(master_out)

  

  def get_array_fullrows(self):
    master_out = []
    for num_row,col in enumerate(self.board):
      is_full = True
      for val in col:
        if val == 0: 
          is_full = False
          break

      if is_full: master_out.append(num_row)
    
    return master_out

  
  def replace_fullrows(self) -> int:
    fullrows = self.get_array_fullrows()
    rows_removed = 0
    while (len(fullrows) != 0):
      rows_removed += 1
      fullrow = fullrows[0]
      self.board = [copy.deepcopy(self.single_col)] + self.board[0:fullrow] + self.board[fullrow+1:]
      fullrows = self.get_array_fullrows()

    return rows_removed




  def get_speed(self): return self.__speed__

  #__BLOCK__ = '██'
  #__EMPTY__ = '  '

  @staticmethod
  def showARuler():
    print('|  2   4   6   8   10  12  14  16  18  20|')


  def showRuler(self):
    ruler = '  2   4   6   8   10  12  14  16  18  20'
    print('|'+ruler[:-(20-self.max_col - 1) * 2]+'|')

  def getRuler(self):
    ruler = '  2   4   6   8   10  12  14  16  18  20'
    return '|'+ruler[:-(20-self.max_col - 1) * 2]+'|'


  def printBoard(self):
    self.make_seperator()
    for col in self.board:
      print('|',end='')
      for val in col:
        if val == ColorPalette.__NA__: print(self.__EMPTY__,end='')
        else: print(colored(self.__BLOCK__, ColorPalette.getColor(val)), end='')
      print('|')

  def printFastBoard(self):
    master_out = ''
    for col in self.board:
      master_out += '|'
      for val in col:
        if val == ColorPalette.__NA__: master_out += (self.__EMPTY__)
        else:  master_out +=  (colored(self.__BLOCK__, ColorPalette.getColor(val)))
      master_out += '|\n'
    
    master_out += f'Score: {self.score}\nLevel: {self.level}\n'
    self.make_seperator()
    print(master_out)


  def addGraph(self, pair_arr, color):
    for pair in pair_arr:
      if not self.out_of_bounds_for_printing(pair):
        col, row = pair
        self.board[self.max_col - col][row - 1] = color


  def removeGraph(self, pair_arr):
    for pair in pair_arr:
      if not self.out_of_bounds_for_printing(pair):
        col,row = pair
        self.board[self.max_col - col][row - 1] = 0


  def updatePiece(self, Piece, bool_add):
    if bool_add:
      self.printed = True
      self.addGraph(Piece.getSurfaceArea(),Piece.getColor())
    else:
      self.removeGraph(Piece.getSurfaceArea())
      self.printed = False


  def isPiecePrinted(self):
    return self.piece_is_printed

  def getCenter(self):
    return (self.max_col - 1, self.max_row // 2)


  def animate(self, id) -> bool:
    row,col = self.getCenter()
    if not id: self.piece = Square(row,col)
    elif id == 1: self.piece = Straight(row,col)
    elif id == 2: self.piece = Tee(row,col)
    elif id == 3: self.piece = Ell(row,col)
    elif id == 4: self.piece = Jay(row,col)
    elif id == 5: self.piece = Ess(row,col)
    elif id == 6: self.piece = Zee(row,col)
    
    if 0 <= id <= 6:
      return self.run_animation()
    
    print(f'{id = }')
    time.sleep(5)
    return False
    
  
  def play(self):
    status = self.animate(random.randrange(0,6))
    while status: 
      self.num_pieces_placed += 1
      if self.num_pieces_placed % 25 == 0:
        self.level += 1
        self.__speed__ /= self.increment
      status = self.animate(random.randrange(0,7))
      if status == None:
        print('gameOver')
        self.quit = True
        break


  def make_seperator(self):
    if self.debug:
      print('\n\n\n\n\n\n')
    else:
      os.system('cls' if os.name == 'nt' else 'clear')

  def run_animation(self) -> bool:
    if self.makes_contact(self.ignore_top(self.piece.getSurfaceArea())):
      print(f'ENDING GAME ON PIECE {self.piece = }')
      return None
    self.update_move_direct()
    self.updatePiece(self.piece, True)
    backup = copy.deepcopy(self.board)
    self.printFastBoard()
    self.updatePiece(self.piece, False)

    self.piece.move_down()
    while ( self.is_legal(self.piece.getSurfaceArea()) and not self.quit ):
      time.sleep(self.__speed__)
      self.check_for_pause()
      self.update_move_direct()
      self.updatePiece(self.piece, True)
      self.printFastBoard()
      backup = copy.deepcopy(self.board)
      self.updatePiece(self.piece, False)
      self.piece.move_down()
    
    self.board = backup
    val = self.replace_fullrows()
    if val != 0:
      self.score += val * self.level
      self.printFastBoard()

    return not self.quit



  def ignore_top(self, point_list):
    keep = []
    for point in point_list:
      row,col = point
      if 0 < row <= self.max_row:
        keep.append(point)
    return keep


  def is_legal(self, contact_points) -> bool:
    return (not self.out_of_bounds(contact_points)) and (not self.makes_contact(contact_points))


  def make_grey(self, contact_points):
    arr_color = []
    for point in contact_points:
      if not self.out_of_bounds_for_printing(point):
        col, row = point
        arr_color.append(self.board[self.max_col - col][row - 1])
        self.board[self.max_col - col][row - 1] = -1
    return arr_color

  def revert(self, contact_points, arr_color):
    i = 0
    for point in contact_points:
      if not self.out_of_bounds_for_printing(point):
        col, row = point
        self.board[self.max_col - col][row - 1] = arr_color[i]
        i += 1
  


  def out_of_bounds(self, contact_points) -> bool:
    for point in contact_points:
      row,col = point
      if not( 0 <= row):
        return True
      if not( 0 < col <= self.max_col + 1 ):
        return True
    return False

  def out_of_bounds_for_printing(self, contact_point):
    col,row = contact_point
    if not( 0 < row <= self.max_row + 1):
      return True
    if not( 0 <= col <= self.max_col + 1 ):
      return True
    return False


  def makes_contact(self, contact_points) -> bool:
    for point in contact_points:
      col,row = point
      if row <= self.max_row:
        if self.board[self.max_col - col][row - 1] != 0:
          return True
    return False



  def checkClear(self) -> [int]:
    rtrn_arr = []
    for row in range(self.max_row):
      if self.row_complete(row + 1):
        rtrn_arr += row
    return rtrn_arr

  def row_complete(self, row) -> bool:
    for col in range(self.max_col):
      if not self.isFilled(row,col):
        return False
    return True
  
  def isFilled(self, row, col):
    return self.board[self.max_col - col][row - 1] != 0


  
  def on_press(self, key):
    if self.piece != None:
      if self.quit: return False

      try:
        if key.char == 'a' or key.char == 'd' or key.char == 's' or key.char == 'p':
          self.input(key.char)

      except AttributeError:
        if key == keyboard.Key.space:
          self.input(key)


  def on_release(self, key):
    if self.piece != None:
      if self.quit: return False

      if key == keyboard.Key.esc:
        self.quit = True
        # Stop listener
        return False

  # Collect events until released
  def keyboard_listener(self):
    with keyboard.Listener (
        on_press=self.on_press, 
        on_release=self.on_release
        ) as listener:
      listener.join()


  def input(self, key_pressed):

    if key_pressed == 'p' and self.paused:
      self.paused = False
    elif key_pressed == 'p':
      self.paused = True
      return
    
    if key_pressed == 'a' or key_pressed == 'd' or key_pressed == 's' or key_pressed == keyboard.Key.space:
      cp_self = copy.deepcopy(self)
      if cp_self.printed:
        cp_self.updatePiece(cp_self.piece, False)

      if cp_self.move_piece(key_pressed):
        cp_self.updatePiece(cp_self.piece, True)
        cp_self.printFastBoard()
        self.update_move(key_pressed)
    return
      
      

  def move_piece(self, key) -> bool:
    if type(key) == str:
      if key == 'a': return self.move_left()
      if key == 'd': return self.move_right()
      if key == 's': return self.drop()

    elif key == keyboard.Key.space: return self.rotate()


  def move_left(self) -> bool:
    self.piece.move_left()
    return self.is_legal(self.piece.getSurfaceArea())
  
  def move_right(self) -> bool:
    self.piece.move_right()
    return self.is_legal(self.piece.getSurfaceArea())

  def rotate(self) -> bool:
    self.piece.rotate()
    return self.is_legal(self.piece.getSurfaceArea())

  def update_move(self, key):
    if type(key) == str:
      if key == 'a': self.moves[0] += 1 # add a left move
      if key == 'd': self.moves[1] += 1 # add a right move
      if key == 's': self.moves[2] = 1  # set a drop move
    elif key == keyboard.Key.space: self.moves[3] += 1 # add a rotation



  def update_move_direct(self):
    for num_left_moves in range(self.moves[0]):
      self.piece.move_left()
    for num_right_moves in range(self.moves[1]):
      self.piece.move_right()
    for num_rotational_moves in range(self.moves[3]):
      self.piece.rotate()

    if self.moves[2] != 0:
      self.drop()

    self.moves = [0,0,0,0]
    
  
  def drop(self):
    num_down_moves = -1
    while(self.is_legal(self.piece.getSurfaceArea())):
      self.piece.move_down()
      num_down_moves += 1


    if num_down_moves == -1:
      #self.piece.move_up()
      raise DropException("In object_type:Board, function Board.drop: number of legal down moves is -1")

    self.piece.move_up()
    return num_down_moves
    

  def check_for_pause(self):
    while self.paused:
      time.sleep(0.1)
      






class DropException(Exception):
  pass