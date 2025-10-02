from gpiozero import DistanceSensor
us = DistanceSensor(echo = 17, trigger = 4)
while True:
  us.wait_for_in_range()
  print(us.distance)
  us.wait_for_out_of_range()
  print('Out of range')


