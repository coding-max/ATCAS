#!/usr/bin/python3
import os
from os.path import exists

def clean_input(file_name):
  """
  converts a flight position file (.csv) to a .json file
  where there are only the positions located within the airspace
  and the time is simplified so there are no seconds other than 00 or 30
  returns a .json file with the filtered and modified data
  """
  try:
    #load the csv file and convert it to a list
    with open(file_name + '.csv', 'r') as input_data:
      data = []
      for line in input_data:
        data.append((line.strip()).split(','))
      data.pop(0)
      for status in data:
        status.pop(0)
        status[2] = float(status[2][1:])
        status[3] = float(status[3][:-1])
      
      #filters positions, entries that have positions outside the airspace are removed from the list
      #and those that are within the airspace have the time modified to make it simpler
      i = 0
      lenght = len(data)
      while i < lenght:
        lat = data[i][2]
        lon = data[i][3]
        if (((lat > -35.15 and lat < -34.65) and (lon > -57.20 and lon < -53.25))
            or ((lat > -34.65 and lat < -34.25) and (lon > -58.15 and lon < -53.25))
            or ((lat > -34.25 and lat < -33.05) and (lon > -58.75 and lon < -53.25))
            or ((lat > -33.05 and lat < -31.40) and (lon > -58.50 and lon < -54.30))
            or ((lat > -33.05 and lat < -32.50) and (lon > -54.30 and lon < -52.95))
            or ((lat > -32.50 and lat < -31.75) and (lon > -54.30 and lon < -53.50))
            or ((lat > -31.40 and lat < -30.00) and (lon > -58.15 and lon < -56.00))
            or ((lat > -31.40 and lat < -30.75) and (lon > -56.00 and lon < -54.80))):
          seconds = int(data[i][0][17:-1])
          if (seconds >= 0 and seconds < 30):
            data[i][0] = data[i][0][:16] + ':00Z'
          else:
            data[i][0] = data[i][0][:16] + ':30Z'
          i += 1
        else:
          data.pop(i)
          lenght -=1
        if i == len(data):
          break
      callsign = data[0][1]
      for status in data:
        status.pop(1)

    #reorder already filtered list and write it to json file
    with open(file_name + '.json', 'w') as output_data:
      output_data.write('{' + '\n  "callsign": "{}",\n  "Path": [\n'.format(callsign))
      for i in range(len(data)):
        output_line = '    {\n'
        output_line = output_line + '      "latitude": {},\n'.format(data[i][1])
        output_line = output_line + '      "longitude": {},\n'.format(data[i][2])
        output_line = output_line + '      "altitude": {},\n'.format(int(data[i][3]))
        output_line = output_line + '      "speed": {},\n'.format(int(data[i][4]))
        output_line = output_line + '      "truck": {},\n'.format(int(data[i][5]))
        output_line = output_line + '      "time": "{}"\n'.format(data[i][0])
        if i < len(data) - 1:
          output_line = output_line + '    },\n'
        else:
          output_line = output_line + '    }\n  ]\n}\n'
        output_data.write(output_line)
  except FileNotFoundError:
    print("error: file not found")


if __name__ == '__main__':
  file_name = input('file_name: ')
  clean_input(file_name)
