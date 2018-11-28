import pygame, sys, math
from pygame.locals import *
from random import randint
import os, can

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
ORANGE = (255, 153, 0)

def stop_can():
  os.system('sudo ifconfig can0 down')

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
    level_text = "{0:>3}°C".format(temp)
    color = BLUE
    if temp > 100:
      color = RED
    elif temp > 85:
      color = GREEN
    draw_text(surface,level_text,self.font,color,(380,360),"bottomright")

# assume 800x480 drawing surface
class Tachometer:
  def __init__(self):
    self.font = pygame.font.Font('Roboto/Roboto-Regular.ttf', 100)

  def draw(self, surface, rpm):
    rpm_text = "{}".format(int(rpm))
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
    speed_text = "{}".format(int(speed))
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


PID_RPM             = 0x0C
PID_VEHICLE_SPEED   = 0x0D
PID_COOLANT_TEMP    = 0x05
PID_FUEL_LEVEL      = 0x2F

if __name__ == '__main__':
  # setup can
  os.system('sudo ip link set can0 type can bitrate 500000')
  os.system('sudo ifconfig can0 up')
  can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native
  can0.set_filters([{"can_id": 0x0, "can_mask": 0x0, "extended": False}]) # filter out extended
  a_listener = can.BufferedReader()
  notifier = can.Notifier(can0, [a_listener])

  # setup pygame
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

  rpm = 0
  speed_kph = 0
  water_c = 0
  fuel_level = 0

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        stop_can()
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          stop_can()
          pygame.quit()
          sys.exit()

    # update the values
    m = a_listener.get_message(0)
    while m:
      if (m.arbitration_id == PID_RPM):
        rpm = (m.data[0]*256. + m.data[1]) / 4
      elif (m.arbitration_id == PID_VEHICLE_SPEED):
        speed_kph = int(m.data[0])
      elif (m.arbitration_id == PID_COOLANT_TEMP):
        water_c = m.data[0] - 40
      elif (m.arbitration_id == PID_FUEL_LEVEL):
        fuel_level = m.data[0] * 100. / 255
      m = a_listener.get_message(0)

    # fill the screen black
    DISPLAYSURF.fill(BLACK)

    # draw on the display
    draw_grid(DISPLAYSURF)
    speedo.draw(DISPLAYSURF, speed_kph)
    tach.draw(DISPLAYSURF, rpm)
    water.draw(DISPLAYSURF, water_c)
    fuel.draw(DISPLAYSURF, fuel_level)
    warningLights.draw(DISPLAYSURF)

    # update the display
    pygame.display.update()
    fpsClock.tick(30)
