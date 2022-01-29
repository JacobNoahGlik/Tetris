class ColorPalette:
  __GREY__ = -1
  __NA__ = 0
  __YELLOW__ = 1
  __BLUE__ = 2
  __MAGENTA__ = 3
  __CYAN__ = 4
  __GREEN__ = 5
  __RED__ = 6
  __WHITE__ = 7

  def getColor(color_id):
    if color_id == 1: return 'yellow'
    if color_id == 2: return 'blue'
    if color_id == 3: return 'magenta'
    if color_id == 4: return 'cyan'
    if color_id == 5: return 'green'
    if color_id == 6: return 'red'
    if color_id == 7: return 'white'

    return 'grey'




class Square:
  def __init__(self, row, col):
    self.marker = (row,col)
  

  def getSurfaceArea(self):
    row,col = self.marker
    return [(row,col), (row,col+1), (row+1,col), (row+1,col+1)]


  def getColor(self):
    return ColorPalette.__YELLOW__


  # def getTouchSpace(self):
  #   row,col = self.marker
  #   return [(row,col), (row+1,col)]

  def rotate(self, rotate_clockwise=True):
    pass


  def move_down(self):
    row,col = self.marker
    self.marker = row - 1,col

    
  def move_up(self):
    row,col = self.marker
    self.marker = row+1,col

  def move_left(self):
    row,col = self.marker
    self.marker = row, col - 1
  
  def move_right(self):
    row,col = self.marker
    self.marker = row, col + 1



class Straight:
  __HORIZONTAL__ = 1 #1
  __VERTICAL__ = 0   #2

  __TOTAL_ROTATIONS__ = 2

  def __init__(self, row, col):
    self.marker = (row-1,col)
    self.rotation = Straight.__VERTICAL__
  

  def getColor(self):
    return ColorPalette.__BLUE__


  def getSurfaceArea(self):
    row,col = self.marker
    if self.rotation == Straight.__VERTICAL__:
      return [(row-1,col), (row,col), (row+1,col), (row+2,col)]
    else:
      return [(row,col), (row,col+1), (row,col+2), (row,col+3)]


  # def getTouchSpace(self):
  #   row,col = self.marker
  #   if self.rotation == Straight.__VERTICAL__:
  #     return [(row,col)]
  #   else:
  #     return [(row-1,col),(row,col),(row+1,col),(row+2,col)]
  

  def rotate(self, rotate_clockwise=True):
    self.rotation = (self.rotation + 1) % Straight.__TOTAL_ROTATIONS__


    
  def move_down(self):
    row,col = self.marker
    self.marker = row-1,col

    
  def move_up(self):
    row,col = self.marker
    self.marker = row+1,col

  def move_left(self):
    row,col = self.marker
    self.marker = row, col - 1
  
  def move_right(self):
    row,col = self.marker
    self.marker = row, col + 1


class Tee:
  __HORIZONTAL__ = 0
  __RIGHT__ = 1
  __UPSIDOWN__ = 2
  __LEFT__ = 3
  __TOTAL_ROTATIONS__ = 4

  def __init__(self, row, col):
    self.marker = (row,col)
    self.rotation = Tee.__HORIZONTAL__
  

  def getColor(self):
    return ColorPalette.__MAGENTA__


  def getSurfaceArea(self):
    row,col = self.marker
    if self.rotation == Tee.__HORIZONTAL__:
      return [(row-1,col), (row,col-1), (row,col), (row,col+1)]
    elif self.rotation == Tee.__RIGHT__:
      return [(row-1,col), (row,col), (row,col+1), (row+1,col)]
    elif self.rotation == Tee.__UPSIDOWN__:
      return [(row,col-1), (row,col), (row,col+1), (row+1,col)]
    else:
      return [(row-1,col), (row,col-1), (row,col), (row+1,col)]


  # def getTouchSpace(self):
  #   row,col = self.marker
  #   if self.rotation == Tee.__HORIZONTAL__:
  #     return [(row-1,col), (row,col), (row+1,col)]
  #   elif self.rotation == Tee.__RIGHT__:
  #     return [(row,col-1), (row+1,col)]
  #   elif self.rotation == Tee.__UPSIDOWN__:
  #     return [(row-1,col), (row,col-1), (row+1,col)]
  #   else:
  #     return [(row-1,col), (row,col-1)]
  

  def rotate(self, rotate_clockwise=True):
    if rotate_clockwise:
      self.rotation = (self.rotation + 1) % Tee.__TOTAL_ROTATIONS__
    else:
      self.rotation = (self.rotation + Tee.__TOTAL_ROTATIONS__ - 1) % Tee.__TOTAL_ROTATIONS__

    
  def move_down(self):
    row,col = self.marker
    self.marker = row-1,col

    
  def move_up(self):
    row,col = self.marker
    self.marker = row+1,col

  def move_left(self):
    row,col = self.marker
    self.marker = row, col - 1
  
  def move_right(self):
    row,col = self.marker
    self.marker = row, col + 1



class Ell:
  __HORIZONTAL__ = 0
  __RIGHT__ = 1
  __UPSIDOWN__ = 2
  __LEFT__ = 3
  __TOTAL_ROTATIONS__ = 4

  def __init__(self, row, col):
    self.marker = (row,col)
    self.rotation = Ell.__HORIZONTAL__
  

  def getColor(self):
    return ColorPalette.__RED__


  def getSurfaceArea(self):
    row,col = self.marker
    if self.rotation == Ell.__HORIZONTAL__:
      return [(row-1,col), (row,col), (row+1,col-1), (row+1,col)]
    elif self.rotation == Ell.__RIGHT__:
      return [(row-1,col), (row,col), (row,col+1), (row,col+2)]
    elif self.rotation == Ell.__UPSIDOWN__:
      return [(row-1,col), (row-1,col+1), (row,col), (row+1,col)]
    else:
      return [(row,col-1), (row,col), (row,col+1), (row+1,col+1)]


  # def getTouchSpace(self):
  #   row,col = self.marker
  #   if self.rotation == Ell.__HORIZONTAL__:
  #     return [(row-1,col), (row,col)]
  #   elif self.rotation == Ell.__RIGHT__:
  #     return [(row-1,col), (row,col), (row+1,col)]
  #   elif self.rotation == Ell.__UPSIDOWN__:
  #     return [(row,col-1), (row+1,col+1)]
  #   else:
  #     return [(row-1,col), (row,col), (row+1,col-1)]
  

  def rotate(self, rotate_clockwise=True):
    if rotate_clockwise:
      self.rotation = (self.rotation + 1) % Ell.__TOTAL_ROTATIONS__
    else:
      self.rotation = (self.rotation + Ell.__TOTAL_ROTATIONS__ - 1) % Ell.__TOTAL_ROTATIONS__

    
  def move_down(self):
    row,col = self.marker
    self.marker = row-1,col

    
  def move_up(self):
    row,col = self.marker
    self.marker = row+1,col

  def move_left(self):
    row,col = self.marker
    self.marker = row, col - 1
  
  def move_right(self):
    row,col = self.marker
    self.marker = row, col + 1





class Jay:
  __HORIZONTAL__ = 0
  __RIGHT__ = 1
  __UPSIDOWN__ = 2
  __LEFT__ = 3

  __TOTAL_ROTATIONS__ = 4


  def __init__(self, row, col):
    self.marker = (row,col)
    self.rotation = Jay.__HORIZONTAL__
  

  def getColor(self):
    return ColorPalette.__CYAN__


  def getSurfaceArea(self):
    row,col = self.marker
    if self.rotation == Jay.__HORIZONTAL__:
      return [(row-1,col), (row,col), (row+1,col), (row+1,col+1)]
    elif self.rotation == Jay.__RIGHT__:
      return [(row+1,col-1), (row,col-1), (row,col), (row,col+1)]
    elif self.rotation == Jay.__UPSIDOWN__:
      return [(row-1,col-1), (row-1,col), (row,col), (row+1,col)]
    else:
      return [(row,col-1), (row,col), (row,col+1), (row-1,col+1)]



  def rotate(self, rotate_clockwise=True):
    if rotate_clockwise:
      self.rotation = (self.rotation + 1) % Jay.__TOTAL_ROTATIONS__
    else:
      self.rotation = (self.rotation + Jay.__TOTAL_ROTATIONS__ - 1) % Jay.__TOTAL_ROTATIONS__

    
  def move_down(self):
    row,col = self.marker
    self.marker = row-1,col

    
  def move_up(self):
    row,col = self.marker
    self.marker = row+1,col

  def move_left(self):
    row,col = self.marker
    self.marker = row, col - 1
  
  def move_right(self):
    row,col = self.marker
    self.marker = row, col + 1






class Ess:
  __HORIZONTAL__ = 0
  __SIDEWAYS__ = 1

  __TOTAL_ROTATIONS__ = 2


  def __init__(self, row, col):
    self.marker = (row,col)
    self.rotation = Ess.__HORIZONTAL__
  

  def getColor(self):
    return ColorPalette.__GREEN__


  def getSurfaceArea(self):
    row,col = self.marker
    if self.rotation == Ess.__HORIZONTAL__:
      return [(row,col-1), (row,col), (row+1,col), (row+1,col+1)]
    else:
      return [(row,col), (row+1,col), (row,col+1), (row-1,col+1)]



  def rotate(self, rotate_clockwise=True):
    if rotate_clockwise:
      self.rotation = (self.rotation + 1) % Ess.__TOTAL_ROTATIONS__
    else:
      self.rotation = (self.rotation + Ess.__TOTAL_ROTATIONS__ - 1) % Ess.__TOTAL_ROTATIONS__

    
  def move_down(self):
    row,col = self.marker
    self.marker = row-1,col

    
  def move_up(self):
    row,col = self.marker
    self.marker = row+1,col

  def move_left(self):
    row,col = self.marker
    self.marker = row, col - 1
  
  def move_right(self):
    row,col = self.marker
    self.marker = row, col + 1



class Zee:
  __HORIZONTAL__ = 0
  __SIDEWAYS__ = 1

  __TOTAL_ROTATIONS__ = 2


  def __init__(self, row, col):
    self.marker = (row,col)
    self.rotation = Ess.__HORIZONTAL__
  

  def getColor(self):
    return ColorPalette.__RED__


  def getSurfaceArea(self):
    row,col = self.marker
    if self.rotation == Ess.__HORIZONTAL__:
      return [(row+1,col-1), (row,col), (row+1,col), (row,col+1)]
    else:
      return [(row-1,col), (row,col), (row,col+1), (row+1,col+1)]



  def rotate(self, rotate_clockwise=True):
    if rotate_clockwise:
      self.rotation = (self.rotation + 1) % Ess.__TOTAL_ROTATIONS__
    else:
      self.rotation = (self.rotation + Ess.__TOTAL_ROTATIONS__ - 1) % Ess.__TOTAL_ROTATIONS__

    
  def move_down(self):
    row,col = self.marker
    self.marker = row-1,col

    
  def move_up(self):
    row,col = self.marker
    self.marker = row+1,col

  def move_left(self):
    row,col = self.marker
    self.marker = row, col - 1
  
  def move_right(self):
    row,col = self.marker
    self.marker = row, col + 1