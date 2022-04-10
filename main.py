"""
Title: Kirkland Brand Flow 
Description: Puzzle game to connect the colors, leave no blank space 
Brought to you by: Team Not Sponsored
Beach Hacks 2022 Submission
"""
import pygame
import os
import sys
import copy
pygame.init()
WIDTH, HEIGHT = 500,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kirkland Brand Flow")
clock = pygame.time.Clock()

#load in assets------------------
background_1 = pygame.image.load(os.path.join('assets','grid.png'))
end_screen = pygame.image.load(os.path.join('assets','end scr.png'))
redd = pygame.image.load(os.path.join('assets', 'reddot.png'))
popup1 = pygame.image.load(os.path.join('assets', 'pop1.png'))
popup2 = pygame.image.load(os.path.join('assets', 'pop2.jpg'))
popup3 = pygame.image.load(os.path.join('assets', 'pop3.jpg'))
popup4 = pygame.image.load(os.path.join('assets', 'pop4.jpg'))

popup1 = pygame.transform.scale(popup1,(485,230))
popup2 = pygame.transform.scale(popup2,(280,470))
popup3 = pygame.transform.scale(popup3,(260,490))
popup4 = pygame.transform.scale(popup4,(500,350))
rd = pygame.transform.scale(redd, (80, 80))
bg1 = pygame.transform.scale(background_1, (500, 500))
BACKGROUND = bg1

screen_num = 0

user_grid = [['#', '#', '#', '#', '#'],
             ['#', '#', '#', '#', '#'],
             ['#', '#', '#', '#', '#'],
             ['#', '#', '#', '#', '#'],
             ['#', '#', '#', '#', '#']]

dot_coords = [[(50,50), (150,50), (250,50), (350,50), (450,50)],
              [(50,150),(150,150),(250,150),(350,150),(450,150)],
              [(50,250),(150,250),(250,250),(350,250),(450,250)],
              [(50,350),(150,350),(250,350),(350,350),(450,350)],
              [(50,450),(150,450),(250,450),(350,450),(450,450)]]

hl_coords = [[(0,0), (100,0), (200,0), (300,0), (400,0)],
             [(0,100),(100,100),(200,100),(300,100),(400,100)],
             [(0,200),(100,200),(200,200),(300,200),(400,200)],
             [(0,300),(100,300),(200,300),(300,300),(400,300)],
             [(0,400),(100,400),(200,400),(300,400),(400,400)]]

def level_select(choice):
  lvl1 = [['r', 'x', 'g', 'x' ,'y'],
          ['x', 'x', 'b', 'x', 'o'],
          ['x', 'x', 'x', 'x' ,'x'],
          ['x', 'g', 'x', 'y', 'x'],
          ['x', 'r', 'b', 'o', 'x']]
  
  lvl1ans =[['r', 'gl', 'g', 'yl' ,'y'],
            ['rl', 'gl', 'b', 'yl', 'o'],
            ['rl', 'gl', 'bl', 'yl' ,'ol'],
            ['rl', 'g', 'bl', 'y', 'ol'],
            ['rl', 'r', 'b', 'o', 'ol']]
  
  lvl2 = [['r', 'x', 'x', 'x', 'r'],
          ['x', 'b', 'g', 'b', 'y'],
          ['x', 'x', 'x', 'x', 'x'],
          ['x', 'g', 'x', 'x', 'x'],
          ['x', 'x', 'x', 'y', 'x']]
  
  lvl2ans = [['r', 'rl', 'rl', 'rl', 'r'],
            ['bl', 'b', 'g', 'b', 'y'],
            ['bl', 'gl', 'gl', 'bl', 'yl'],
            ['bl', 'g', 'bl', 'bl', 'yl'],
            ['bl', 'bl', 'bl', 'y', 'yl']]
                   
  lvl3 = [['b', 'x', 'x', 'x', 'y'],
          ['x', 'x', 'x', 'x', 'x'],
          ['x', 'r', 'g', 'x', 'x'],
          ['x', 'x', 'b', 'x', 'x'],
          ['g', 'r', 'y', 'x', 'x']]
  
  lvl3ans = [['b', 'bl', 'bl', 'bl', 'y'],
             ['gl', 'gl', 'gl', 'bl', 'yl'],
             ['gl', 'r', 'g', 'bl', 'yl'],
             ['gl', 'rl', 'b', 'bl', 'yl'],
             ['g', 'r', 'y', 'yl', 'yl']]
  if(choice == 1):
    user_grid = copy.deepcopy(lvl1) 
    return lvl1, lvl1ans
  elif(choice == 2):
    user_grid = copy.deepcopy(lvl2) 
    return lvl2, lvl2ans
  elif(choice == 3):
    user_grid = copy.deepcopy(lvl3)
    return lvl3, lvl3ans
  else:
    return 

#Player class--------------------------------------
class Player:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.level = 1
    self.color = ''
    self.matrix = []
    self.direction = ""
    
  def trace_location(self,start):
    player_matrix, ans_matrix = level_select(start)
    for x in range(0,5,1):
      for y in range(0,5,1):
        draw_dot(player_matrix[x][y],x,y)
    pygame.display.update()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          if (player_matrix[self.x][self.y] != 'x'):
            self.color = select(player_matrix,self.x,self.y)
        if event.key == pygame.K_UP:
          if self.x <= 0: # Not go out of bounds
            print("y cannot be negative")
          else:
            self.x = self.x-1
            self.direction = "up"
            if (player_matrix[self.x][self.y] == 'x') and (self.color != 'x'):
              draw_dot(self.color,self.x,self.y)
              pygame.display.update()
              player_matrix[self.x][self.y] = self.color + 'l'
              user_grid[self.x][self.y] = self.color + 'l'
              pygame.draw.circle(WIN,(255,255,255),dot_coords[self.x][self.y],8)
              self.remove_dot(self.x, self.y)
              pygame.display.update()
        elif event.key == pygame.K_DOWN:
          if self.x >= 4:
            print("y cannot be greater than 4")
          else:	
            self.x = self.x+1
            self.direction = "down"
            if (player_matrix[self.x][self.y] == 'x') and (self.color != 'x'):
              draw_dot(self.color,self.x,self.y)
              pygame.display.update()
              player_matrix[self.x][self.y] = self.color + 'l'
              user_grid[self.x][self.y] = self.color + 'l'
              pygame.draw.circle(WIN,(255,255,255),dot_coords[self.x][self.y],8)
              self.remove_dot(self.x, self.y)
              pygame.display.update()
        elif event.key == pygame.K_RIGHT:
          if self.y >= 4:
            print("x cannot be greater than 4")
          else:
            self.y = self.y+1
            self.direction = "right"
            if (player_matrix[self.x][self.y] == 'x') and (self.color != 'x'):
              draw_dot(self.color,self.x,self.y)
              player_matrix[self.x][self.y] = self.color + 'l'
              user_grid[self.x][self.y] = self.color + 'l'
              pygame.draw.circle(WIN,(255,255,255),dot_coords[self.x][self.y],8)
              self.remove_dot(self.x, self.y)
              pygame.display.update()
        elif event.key == pygame.K_LEFT:
          if self.y <= 0:
            print("x cannot be negative")
          else:
            self.y = self.y-1
            self.direction = "left"
            if (player_matrix[self.x][self.y] == 'x') and (self.color != 'x'):
              draw_dot(self.color,self.x,self.y)
              pygame.display.update()
              player_matrix[self.x][self.y] = self.color + 'l'
              user_grid[self.x][self.y] = self.color + 'l'
              pygame.draw.circle(WIN,(255,255,255),dot_coords[self.x][self.y],8)
              self.remove_dot(self.x, self.y)
              pygame.display.update()
        elif event.key == pygame.K_r:
          for x in range(0,5,1):
            for y in range(0,5,1):
              draw_dot(player_matrix[x][y],x,y)
              pygame.display.update()
        elif event.key == pygame.K_z:
          if(self.check_board(user_grid, ans_matrix)):
          #if(self.check_board(player_matrix, ans_matrix)):
            self.level += 1
            if(self.level) > 3:
              WIN.blit(end_screen, (0,0))
              pygame.display.update()
              break
            self.x = 0
            self.y = 0
            WIN.blit(BACKGROUND, (0,0))
            self.trace_location(self.level)
          else:
            wrongans = pygame.Rect(150,100,200,50)
            pygame.draw.rect(WIN,(255,211,0),wrongans)
            draw_text('Wrong Ans',pygame.font.SysFont('Verdana',40),(0,0,0),WIN,150,100)
        print(f"x: {self.y}   y: {self.x}")
        print(player_matrix[self.x][self.y])
    self.matrix = player_matrix

  def remove_dot(self, x, y):
    print("at least i print")
    if self.direction == "up":
      draw_dot(self.color,x+1,y)
    if self.direction == "down":
      draw_dot(self.color,x-1,y)
    if self.direction == "right":
      draw_dot(self.color,x,y-1)
    if self.direction == "left":
      draw_dot(self.color,x,y+1)
      
  def make_ad(self):
    if self.level == 1: 
      WIN.blit(popup1,(5,150))
    elif self.level == 2: 
      WIN.blit(popup2,(125,5))
    elif self.level == 3: 
      WIN.blit(popup3,(130,0))
    pygame.display.update()
    visible = True 
    begin = pygame.time.get_ticks()
    while visible: # timer for ad visiblility 
      if self.level == 3:
        sec = (pygame.time.get_ticks() - begin) / 1000 
        if sec > 2: 
          WIN.blit(popup2,(125,5))
          pygame.display.update()
        if sec > 3: 
          WIN.blit(popup1,(5,350))
          pygame.display.update()
        if sec > 5: 
          WIN.blit(popup4, (0,0))
          pygame.display.update()
        if sec > 9:
          visible = False 
          break 
      else: 
        sec = (pygame.time.get_ticks() - begin) / 1000 
        if sec > 5:
          break 
      print(sec)
      
  def check_board(self, player_sol, solution):
    if 'x' in self.matrix:
      return False 
    else: 
      for i in range(5):
        for j in range(5):
          if(solution[i][j] == 'r' or solution[i][j] == 'b' or solution[i][j] == 'g' or solution[i][j] == 'y' or solution[i][j] == 'o'):
            pass 
          elif(solution[i][j] != player_sol[i][j]):
            #print("NAH BRUH")
            return False 
      print("true")
      self.make_ad()
    return True
    
  def display(self):
    for i in range(5):
      for j in range(5):
        print(self.matrix[i][j], end= " ")
      print()
        
  def get_level(self):
    return self.level

class Highlight:
  def __init__(self, x, y, image):
    self.image = image 
    self.rect = image.get_rect() 
    self.rect.x = x 
    self.rect.y = y 

  def translate(self, someX, someY):
    self.rect.move_ip(someX, someY)

  def jump(self, someX, someY):
    self.rect.x = someX
    self.rect.y = someY 

def select(matrix,x,y):
  return matrix[x][y]


def draw_text(text,font,color,surface,x,y):
  textobj = font.render(text,1,color)
  textrect = textobj.get_rect()
  textrect.topleft = (x,y)
  WIN.blit(textobj,textrect)

def draw_dot(char,x,y):
  if (char == 'r') or (char == 'rl'):
    pygame.draw.circle(WIN,(255,0,0),dot_coords[x][y],25)
  if (char == 'g') or (char == 'gl'):
    pygame.draw.circle(WIN,(0,255,0),dot_coords[x][y],25)
  if (char == 'b') or (char == 'bl'):
    pygame.draw.circle(WIN,(0,0,255),dot_coords[x][y],25)
  if (char == 'y') or (char == 'yl'):
    pygame.draw.circle(WIN,(255,255,0),dot_coords[x][y],25)
  if (char == 'o') or (char == 'ol'):
    pygame.draw.circle(WIN,(255,140,0),dot_coords[x][y],25)
  if (char == 'x'):
    pass
  return

def level(user, num): 
  if(num==1):
    ############LEVEL 1
    level_select(1)
    user.trace_location(1)
  elif(num==2):
    ############LEVEL 2
    level_select(2)
    user.trace_location(2)
  elif(num==3):
    ############LEVEL 3
    level_select(3)
    user.trace_location(3)

def esc_menu():
  print("other stuff goes here")

def KirklandBrandFlow(player):
  print("Make Kirkland Brand Flow")
  x = True
  BACKGROUND = bg1
  WIN.blit(BACKGROUND, (0,0))
  lvl, lvlans = level_select(player.get_level())
  for x in range(0,5,1):
    for y in range(0,5,1):
      draw_dot(lvl[x][y],x,y)
  pygame.draw.circle(WIN,(255,255,255),(50,50),8)
  pygame.display.update()
  while x:
    level(player, player.get_level())
    
    
def main():
  user = Player()
  run = True
  menu = True
  click = False
  while run:
    if menu == True:
      WIN.fill((0,0,0))
      draw_text('Kirkland Brand',pygame.font.SysFont('Verdana',12),(255,255,255),WIN,150,10)
      draw_text('f',pygame.font.SysFont('Verdana',60),(255,0,0),WIN,200,20)
      draw_text('l',pygame.font.SysFont('Verdana',60),(0,255,0),WIN,220,20)
      draw_text('o',pygame.font.SysFont('Verdana',60),(0,0,255),WIN,230,20) 
      draw_text('w',pygame.font.SysFont('Verdana',60),(255,255,0),WIN,260,20)
      
      mx, my = pygame.mouse.get_pos()
      
      startbutton = pygame.Rect(150,100,200,50)
      quitbutton = pygame.Rect(150,200,200,50)
      if startbutton.collidepoint((mx,my)):
        if click:
          print("Game Start")
          KirklandBrandFlow(user)
      if quitbutton.collidepoint((mx,my)):
        if click:
          print("Game Exit")
          pygame.quit()
          sys.exit()
      
      pygame.draw.rect(WIN,(255,211,0),startbutton)
      pygame.draw.rect(WIN,(255,211,0),quitbutton)
      draw_text('Start',pygame.font.SysFont('Verdana',40),(0,0,0),WIN,150,100)
      draw_text('Quit',pygame.font.SysFont('Verdana',40),(0,0,0),WIN,150,200)

      draw_text('Tap Space to Select color',pygame.font.SysFont('Verdana',15),(255,255,255),WIN,155,390)
      draw_text('Use Arrow Keys to traverse board',pygame.font.SysFont('Verdana',15),(255,255,255),WIN,130,405)
      draw_text('Click Z to check completed board',pygame.font.SysFont('Verdana',15),(255,255,255),WIN,130,420)
      draw_text('in-game',pygame.font.SysFont('Verdana',15),(255,255,255),WIN,220,435)
      click = False
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        print("A key has been pressed")
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          click = True
    pygame.display.update()
    clock.tick(60)
  pygame.quit()

main()
