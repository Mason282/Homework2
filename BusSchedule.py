#BusSchedule.py
#Name: Mason Rodgers
#Date: 03/13/25
#Assignment: Bus Schedule 

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from TimeHelpers import isLater, getHours, getMinutes

def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless")
  
  driver = webdriver.Chrome(options=chrome_options)
  
  driver.get(url)
  text = driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return text

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  file = open("testPage.txt", 'r')
  text = file.read()
  file.close()
  return text

def loadBusTimes(filename):
  """
  Reads the bus stop times from a text file and returns a list of times
  """
  file = open(filename, 'r')
  lines = file.readlines()
  file.close()
  
  bus_times_list = []
  for line in lines:
    line = line.strip()
    if ":" in line:
      if "AM" in line or "PM" in line:
        bus_times_list.append(line)

  return bus_times_list

def convertToCentralTime():
  """
  Converts time from GMT to Central time
  """
  now = datetime.datetime.now()
  month_right_now = now.month
  day_today = now.day

  if month_right_now > 3 and month_right_now < 11:
    hour_offset = -5
  elif month_right_now == 3 and day_today >= 8:
    hour_offset = -5
  elif month_right_now == 11 and day_today < 7:
    hour_offset = -5
  else:
    hour_offset = -6
  
  new_time = now + datetime.timedelta(hours=hour_offset)
  return new_time.strftime("%I:%M %p")
  


def main():
  direction_bus_is_going = "EAST"
  bus_stop_code = "2269"
  bus_route_number = "11"


  url = "https://myride.ometro.com/Schedule?stopCode=" + bus_stop_code + "&routeNumber=" + bus_route_number + "&directionName=" + direction_bus_is_going
  
  print("Getting the bus schedule...")

  current_time_right_now = convertToCentralTime()
  filename_with_bus_times = "BusTimes.txt"
  bus_times_we_loaded = loadBusTimes(filename_with_bus_times)

  next_bus_time = None
  second_bus_time = None


  for bus_time in bus_times_we_loaded:
    if isLater(bus_time, current_time_right_now):
      next_bus_time = bus_time
      break


  if next_bus_time != None:
    for bus_time in bus_times_we_loaded:
      if isLater(bus_time, next_bus_time):
        second_bus_time = bus_time
        break


  if next_bus_time != None:
    next_bus_minutes_away = (getHours(next_bus_time) *60 + getMinutes(next_bus_time)) - (getHours(current_time_right_now) *60 + getMinutes(current_time_right_now))
    if next_bus_minutes_away < 0:
      next_bus_minutes_away = next_bus_minutes_away +1440
  else:
    next_bus_minutes_away = "N/A"
  
  if second_bus_time != None:
    second_bus_minutes_away = (getHours(second_bus_time) * 60 +getMinutes(second_bus_time)) - (getHours(current_time_right_now) *60 + getMinutes(current_time_right_now))
    if second_bus_minutes_away < 0:
      second_bus_minutes_away = second_bus_minutes_away + 1440
  else:
    second_bus_minutes_away = "N/A"

  print("Current Time: " + current_time_right_now)
  print("The Next bus will arrive in: " + str(next_bus_minutes_away) + " minutes.")
  print("the following bus will arrive in: " + str(second_bus_minutes_away) + " minutes.")

if __name__ == "__main__":
  main()
