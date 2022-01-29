import threading
import gameboard
import time
    





class keyboardReader(threading.Thread):
  def __init__(self, shared, *args, **kwargs):
    super(keyboardReader,self).__init__(*args, **kwargs)
    self.shared = shared

  def run(self):
    MasterBoard = self.shared
    MasterBoard.keyboard_listener()
    time.sleep(MasterBoard.get_speed() * 0.5)
    print('\n\t|***********************|\n\t|keyboardReader [closed]|\n\t|***********************|')

    

class gameboardRunner(threading.Thread):
  def __init__(self, shared, *args, **kwargs):
    super(gameboardRunner,self).__init__(*args, **kwargs)
    self.shared = shared

  def run(self):
    MasterBoard = self.shared
    MasterBoard.play()
    # val = 4
    # status = MasterBoard.animate(val)
    # while status:
    #   val += 1
    #   status = MasterBoard.animate(val % 6)
      
    print('\n\t|************************|\n\t|gameboardRunner [closed]|\n\t|************************|')







def main(Debug=False,Speed=0.5):
  
  shared_obj = gameboard.Board(25,15, speed=Speed, debug=Debug)

  threads = [ gameboardRunner(shared=shared_obj,
              name='gameboard_runner'), keyboardReader(shared=shared_obj, name='key_board_reader')
            ]


  for thread in threads:
      thread.start()
  for thread in threads:
      thread.join()
