import pygame, sys, math
from pygame.locals import *
from random import randint

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
ORANGE = (255, 153, 0)

def draw_text(surface,text,fontObj,color,pos,position="center"):
  textSurfaceObj = fontObj.render(text,True,color,BLACK)
  textSurfaceObj.set_colorkey(BLACK)
  textRectObj = textSurfaceObj.get_rect()
  if position is "center":
    textRectObj.center = pos
  elif position is "topright":
    textRectObj.topright = pos
  elif position is "bottomright":
    textRectObj.bottomright = pos
  elif position is "topleft":
    textRectObj.topleft = pos

  surface.blit(textSurfaceObj,textRectObj)

def draw_grid(surface):
  # horizontal lines
  pygame.draw.line(surface,WHITE,(20,440),(780,440))

  # vertical lines
  pygame.draw.line(surface,WHITE,(30,440),(30,480))
  pygame.draw.line(surface,WHITE,(210,440),(210,480))
  pygame.draw.line(surface,WHITE,(769,440),(769,480))
  pygame.draw.line(surface,WHITE,(649,440),(649,480))

last_rpm = 7000
rpm_diff = 100
def get_rpm():
  global last_rpm, rpm_diff
  last_rpm += rpm_diff
  if last_rpm > 9000:
    last_rpm = 9000
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

last_fuel = 0
fuel_diff = 0.1
fuel_max = 100
fuel_min = 0
def get_fuel():
  global last_fuel, fuel_diff
  last_fuel += fuel_diff
  if last_fuel > fuel_max:
    last_fuel = fuel_max
    fuel_diff = -1 * fuel_diff
  elif last_fuel < fuel_min:
    last_fuel = fuel_min
    fuel_diff = -1 * fuel_diff
  return last_fuel

last_temp = 133
temp_diff = 1.2
temp_max = 220
temp_min = 100
def get_temp():
  global last_temp, temp_diff
  last_temp += temp_diff
  if last_temp > temp_max:
    last_temp = temp_max
    temp_diff = -1 * temp_diff
  elif last_temp < temp_min:
    last_temp = temp_min
    temp_diff = -1 * temp_diff
  return last_temp



class FuelLevel:
  def __init__(self):
    self.fontL = pygame.font.Font('Roboto/Roboto-Regular.ttf', 60)
    self.fontS = pygame.font.Font('Roboto/Roboto-Regular.ttf', 40)

  def draw(self, surface, level):
    level_text = "{0:.1f}".format(level)
    color = GREEN
    if level < 10:
      color = RED
    elif level < 20:
      color = ORANGE
    draw_text(surface,"FUEL",self.fontS,color,(230,140),"topright")
    draw_text(surface,level_text,self.fontL,color,(380,140),"topright")

class WaterTemp:
  def __init__(self):
    self.font = pygame.font.Font('Roboto/Roboto-Regular.ttf', 60)

  def draw(self, surface, temp):
    level_text = "{0:.1f}°F".format(temp)
    color = ORANGE
    if temp > 212:
      color = RED
    elif temp > 185:
      color = GREEN
    draw_text(surface,level_text,self.font,color,(380,360),"bottomright")

# assume 800x480 drawing surface
class Tachometer:
  def __init__(self):
    self.font = pygame.font.Font('Roboto/Roboto-Regular.ttf', 100)

  def draw(self, surface, rpm):
    rpm_text = "{0:>4}".format(rpm)
    draw_text(surface,rpm_text,self.font,WHITE,(769,340),"bottomright")
    values = list(range(6000,9000,250))
    idx = 0
    while idx < len(values) and values[idx] < rpm:
      color = GREEN
      if (idx >= 8):
        color = BLUE
      elif (idx >= 4):
        color = RED
      pointlist = [(16+(idx*64)+4,4),(16+(idx*64)+60,4),(16+(idx*64)+60,60)]
      pygame.draw.polygon(surface, color, pointlist)
      idx += 1


class Spedometer:
  def __init__(self):
    self.font = pygame.font.Font('Roboto/Roboto-Regular.ttf', 200)

  def draw(self, surface, speed):
    speed_text = "{0:>3}".format(speed)
    draw_text(surface,speed_text,self.font,ORANGE,(769,280),"bottomright")

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
    surface.blit(self.turn_signal_left, (0,440))
    surface.blit(self.turn_signal_right, (769,440))
    surface.blit(self.battery, (30,440))
    surface.blit(self.oil, (90,440))
    surface.blit(self.check_engine, (150,440))
    surface.blit(self.low_beams, (649,440))
    surface.blit(self.high_beams, (709,440))


if __name__ == '__main__':
  pygame.init()
  pygame.mouse.set_visible(False)
  DISPLAYSURF=pygame.display.set_mode((800,480),0,32)
  pygame.display.set_caption('Endurance Honda Dash')
  fpsClock = pygame.time.Clock()

  warningLights = WarningLights()
  tach = Tachometer()
  speedo = Spedometer()
  water = WaterTemp()
  fuel = FuelLevel()

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          pygame.quit()
          sys.exit()

    # fill the screen black
    DISPLAYSURF.fill(BLACK)

    # draw on the display
    draw_grid(DISPLAYSURF)
    speedo.draw(DISPLAYSURF, get_speed())
    tach.draw(DISPLAYSURF, get_rpm())
    water.draw(DISPLAYSURF, get_temp())
    fuel.draw(DISPLAYSURF, get_fuel())
    warningLights.draw(DISPLAYSURF)

    # update the display
    pygame.display.update()
    fpsClock.tick(30)
