import os, can

def stop_can():
  os.system('sudo ifconfig can0 down')

PID_RPM             = 0x0C
PID_VEHICLE_SPEED   = 0x0D
PID_COOLANT_TEMP    = 0x05
PID_FUEL_LEVEL      = 0x2F

if __name__ == '__main__':
  # setup can
  os.system('sudo ip link set can0 type can bitrate 500000')
  os.system('sudo ifconfig can0 up')
  can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native
  a_listener = can.BufferedReader()
  notifier = can.Notifier(can0, [a_listener])

  rpm = 0
  speed_kph = 0
  water_c = 0
  fuel_level = 0

  while True:
    updated = False
    # update the values
    m = a_listener.get_message(0)
    while m:
      print(m)
      updated = True
      if (m.arbitration_id == PID_RPM):
        rpm = (m.data[0]*256 + m.data[1]) / 4
      elif (m.arbitration_id == PID_VEHICLE_SPEED):
        speed_kph = m.data[0]
      elif (m.arbitration_id == PID_COOLANT_TEMP):
        water_c = m.data[0] - 40
      elif (m.arbitration_id == PID_FUEL_LEVEL):
        fuel_level = m.data[0] * 100. / 255
      m = a_listener.get_message(0)

    if updated:
      print("rpm: {}, speed: {}, water: {}, fuel: {}".format(rpm,speed_kph,water_c,fuel_level))
