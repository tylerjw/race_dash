import pygame, sys, math
from pygame.locals import *
from random import randint

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

def draw_text(surface,text,fontObj,color,center):
  textSurfaceObj = fontObj.render(text,True,color,BLACK)
  textSurfaceObj.set_colorkey(BLACK)
  textRectObj = textSurfaceObj.get_rect()
  textRectObj.center = center
  surface.blit(textSurfaceObj,textRectObj)

# assume 800x480 drawing surface
def draw_tach(surface, rpm, fontSm):
  #draw redline
  RedLine = 6500
  RedLineXpos = math.floor(RedLine/10)
  pygame.draw.line(surface,RED,(RedLineXpos,0),(RedLineXpos,100),2)
  # draw legend
  for xpos in range(100,800,100):
    color = WHITE if xpos < RedLineXpos else RED
    pygame.draw.line(surface,color,(xpos,0),(xpos,100),2)
    draw_text(surface,str(math.floor(xpos/100)),fontSm,color,(xpos,110))

  tach_width = math.floor(rpm/10)
  for xpos in range(2,tach_width,4):
    color = WHITE if xpos < RedLineXpos else RED
    pygame.draw.line(surface,color,(xpos,0),(xpos,90),2)

def draw_grid(surface):
  pygame.draw.line(surface,WHITE,(0,125),(799,125))
  pygame.draw.line(surface,WHITE,(0,300),(799,300))
  pygame.draw.line(surface,WHITE,(0,400),(799,400))
  pygame.draw.line(surface,WHITE,(400,125),(400,400))

def draw_speedo(surface, speed, fontXl, fontSm):
  speed_text = "{0:>3}".format(speed)
  draw_text(surface,speed_text,fontXl,WHITE,(200,200))
  draw_text(surface,'mph',fontSm,WHITE,(200,280))

def draw_warnings(surface):
  turn_signal_left = pygame.image.load('images/turn_signal_left.png').convert()
  turn_signal_left.set_colorkey(BLACK)
  turn_signal_right = pygame.image.load('images/turn_signal_right.png').convert()
  turn_signal_right.set_colorkey(BLACK)
  battery = pygame.image.load('images/battery.png').convert()
  battery.set_colorkey(BLACK)
  oil = pygame.image.load('images/oil.png').convert()
  oil.set_colorkey(BLACK)

  surface.blit(turn_signal_left, (0,400))
  surface.blit(turn_signal_right, (740,400))
  surface.blit(battery, (60,400))
  surface.blit(oil, (180,400))

last_rpm = 7000
rpm_diff = 100
def get_rpm():
  global last_rpm, rpm_diff
  last_rpm += rpm_diff
  if last_rpm > 8000:
    last_rpm = 8000
    rpm_diff = -100
  elif last_rpm < 0:
    last_rpm = 0
    rpm_diff = 100

  return last_rpm

last_speed = 0
speed_diff = 1
def get_speed():
  global last_speed, speed_diff
  last_speed += speed_diff
  if last_speed > 140:
    last_speed = 140
    speed_diff = -1
  elif last_speed < 0:
    last_speed = 0
    speed_diff = 1

  return last_speed

if __name__ == '__main__':
  pygame.init()
  DISPLAYSURF=pygame.display.set_mode((800,480),0,32)
  pygame.display.set_caption('Endurance Honda Dash')
  fpsClock = pygame.time.Clock()

  # create font objects
  fontObjXl = pygame.font.Font('Roboto/Roboto-Regular.ttf', 160)
  fontObjSm = pygame.font.Font('Roboto/Roboto-Regular.ttf', 24)

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

    # fill the screen black
    DISPLAYSURF.fill(BLACK)

    # draw on the display
    draw_grid(DISPLAYSURF)
    draw_tach(DISPLAYSURF, get_rpm(), fontObjSm)
    draw_speedo(DISPLAYSURF, get_speed(), fontObjXl, fontObjSm)
    draw_warnings(DISPLAYSURF)

    # update the display
    pygame.display.update()
    fpsClock.tick(30)
