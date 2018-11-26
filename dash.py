import pygame, sys, math
from pygame.locals import *
from random import randint
import signal

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

def signal_handler(signal, frame):
  print 'Signal: {}'.format(signal)
  sleep(1)
  pygame.quit()
  sys.exit(0)

def draw_text(surface,text,fontObj,color,center):
  textSurfaceObj = fontObj.render(text,True,color,BLACK)
  textSurfaceObj.set_colorkey(BLACK)
  textRectObj = textSurfaceObj.get_rect()
  textRectObj.center = center
  surface.blit(textSurfaceObj,textRectObj)

def draw_grid(surface):
  pygame.draw.line(surface,WHITE,(0,125),(799,125))
  pygame.draw.line(surface,WHITE,(0,300),(799,300))
  pygame.draw.line(surface,WHITE,(0,400),(799,400))
  pygame.draw.line(surface,WHITE,(400,125),(400,400))

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

# assume 800x480 drawing surface
class Tachometer:
  def __init__(self):
    self.font = pygame.font.Font('Roboto/Roboto-Regular.ttf', 24)

  def draw(self, surface, rpm):
    #draw redline
    RedLine = 6500
    RedLineXpos = math.floor(RedLine/10)
    pygame.draw.line(surface,RED,(RedLineXpos,0),(RedLineXpos,100),2)
    # draw legend
    for xpos in range(100,800,100):
      color = WHITE if xpos < RedLineXpos else RED
      pygame.draw.line(surface,color,(xpos,0),(xpos,100),2)
      draw_text(surface,str(math.floor(xpos/100)),self.font,color,(xpos,110))

    tach_width = math.floor(rpm/10)
    for xpos in range(2,tach_width,4):
      color = WHITE if xpos < RedLineXpos else RED
      pygame.draw.line(surface,color,(xpos,0),(xpos,90),2)

class Spedometer:
  def __init__(self):
    self.fontXl = pygame.font.Font('Roboto/Roboto-Regular.ttf', 160)
    self.fontSm = pygame.font.Font('Roboto/Roboto-Regular.ttf', 24)

  def draw(self, surface, speed):
    speed_text = "{0:>3}".format(speed)
    draw_text(surface,speed_text,self.fontXl,WHITE,(200,200))
    draw_text(surface,'mph',self.fontSm,WHITE,(200,280))

class WarningLights:
  def __init__(self):
    self.turn_signal_left = pygame.image.load('images/turn_signal_left.png').convert()
    self.turn_signal_left.set_colorkey(BLACK)
    self.turn_signal_right = pygame.image.load('images/turn_signal_right.png').convert()
    self.turn_signal_right.set_colorkey(BLACK)
    self.battery = pygame.image.load('images/battery.png').convert()
    self.battery.set_colorkey(BLACK)
    self.oil = pygame.image.load('images/oil.png').convert()
    self.oil.set_colorkey(BLACK)
    self.coolant_temp = pygame.image.load('images/coolant_temp.png').convert()
    self.coolant_temp.set_colorkey(BLACK)
    self.check_engine = pygame.image.load('images/check_engine.png').convert()
    self.check_engine.set_colorkey(BLACK)
    self.fan = pygame.image.load('images/fan.png').convert()
    self.fan.set_colorkey(BLACK)
    self.fuel = pygame.image.load('images/fuel.png').convert()
    self.fuel.set_colorkey(BLACK)
    self.low_beams = pygame.image.load('images/low_beams.png').convert()
    self.low_beams.set_colorkey(BLACK)
    self.high_beams = pygame.image.load('images/high_beams.png').convert()
    self.high_beams.set_colorkey(BLACK)

  def draw(self, surface):
    surface.blit(self.turn_signal_left, (0,400))
    surface.blit(self.turn_signal_right, (740,400))
    surface.blit(self.battery, (85,400))
    surface.blit(self.oil, (215,400))
    surface.blit(self.check_engine, (345,400))
    surface.blit(self.low_beams, (475,400))
    surface.blit(self.high_beams, (605,400))


if __name__ == '__main__':
  signal.signal(signal.SIGTERM, signal_handler)
  signal.signal(signal.SIGINT, signal_handler)

  pygame.init()
  pygame.mouse.set_visible(false)
  DISPLAYSURF=pygame.display.set_mode((800,480),0,32)
  pygame.display.set_caption('Endurance Honda Dash')
  fpsClock = pygame.time.Clock()

  warningLights = WarningLights()
  tach = Tachometer()
  speedo = Spedometer()

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

    # fill the screen black
    DISPLAYSURF.fill(BLACK)

    # draw on the display
    draw_grid(DISPLAYSURF)
    speedo.draw(DISPLAYSURF, get_speed())
    tach.draw(DISPLAYSURF, get_rpm())
    warningLights.draw(DISPLAYSURF)

    # update the display
    pygame.display.update()
    fpsClock.tick(30)
