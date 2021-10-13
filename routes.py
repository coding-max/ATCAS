#!/usr/bin/python3
import os
from os.path import exists
from datetime import datetime
from datetime import timedelta

def clean_input(file_name):
  try:
    with open(file_name + '.csv', 'r') as input_data:
      with open(file_name + '.json', 'w', encoding='utf=8') as output_data:
        output_data.write('{' + '\n  "Callsign": "{}",\n  "Path": [\n'.format(file_name))
      for line in input_data:
        data = (line.strip()).split(',')
        if ('UTC' in data):
          continue
        lat = float(data[3][1:])
        lon = float(data[4][:-1])
        if (((lat > -35.15 and lat < -34.65) and (lon > -57.20 and lon < -53.25))
            or ((lat > -34.65 and lat < -34.25) and (lon > -58.15 and lon < -53.25))
            or ((lat > -34.25 and lat < -33.05) and (lon > -58.75 and lon < -53.25))
            or ((lat > -33.05 and lat < -31.40) and (lon > -58.50 and lon < -54.30))
            or ((lat > -33.05 and lat < -32.50) and (lon > -54.30 and lon < -52.95))
            or ((lat > -32.50 and lat < -31.75) and (lon > -54.30 and lon < -53.50))
            or ((lat > -31.40 and lat < -30.00) and (lon > -58.15 and lon < -56.00))
            or ((lat > -31.40 and lat < -30.75) and (lon > -56.00 and lon < -54.80))):
          with open(file_name + '.json', 'a', encoding='utf=8') as output_data:
            output_line = '    {\n'
            output_line = output_line + '      "latitude": {},\n'.format(lat)
            output_line = output_line + '      "longitude": {},\n'.format(lon)
            output_line = output_line + '      "altitude": {},\n'.format(data[5])
            output_line = output_line + '      "speed": {},\n'.format(int(data[6]))
            output_line = output_line + '      "truck": {},\n'.format(int(data[7]))
            output_line = output_line + '      "time": "{}"\n'.format(data[1])
            output_line = output_line + '    },\n'
            output_data.write(output_line)
          output_data.close()
      cmd = "cat " + file_name + ".json | head -n-1 > results_" + file_name + ".json"
      os.system(cmd)
      with open('results_' + file_name + '.json', 'a', encoding='utf=8') as output_data:
        output_data.write('    }\n  ]\n}\n')
      if (os.path.exists(file_name + '.json')):
        os.remove(file_name + '.json')
      os.rename('results_' + file_name + '.json', file_name + '.json')
  except FileNotFoundError:
    print("error: file not found")


def clean_output(file_name):
  try:
    with open(file_name + '.csv', 'r') as input_data:
      with open(file_name + '.tmp', 'w', encoding='utf=8') as output_data:
        for line in input_data:
          data = (line.strip()).split(',')
          if ('UTC' in data):
            continue
          seconds = int(data[1][17:-1])
          if (seconds >= 0 and seconds < 15):
            data[1] = data[1][:16] + ':00Z'
          else:
            data[1] = data[1][:16] + ':30Z'
          output_line = data[0]+','+data[1]+','+data[2]+','+data[3]+','+data[4]+','+data[5]+','+data[6]+','+data[7]+'\n'
          output_data.write(output_line)
  except FileNotFoundError:
    print("error: file not found")


def complete_output(file_name):
  try:
    with open(file_name + '_log.csv', 'w', encoding='utf=8') as output_data:
      file_lenght = len(open(file_name + '.tmp', 'r').readlines())
      first_line = open(file_name + '.tmp', 'r').readlines()[0]
      output_data.write(first_line)
      for i in range (1, file_lenght - 1):
        
        curr_line = open(file_name + '.tmp', 'r').readlines()[i]
        data = (curr_line.strip()).split(',')
        curr_time = data[1]
        #curr_time = datetime.strptime(data[1], '%Y-%m-%dT%H:%M:%SZ')

        next_line = open(file_name + '.tmp', 'r').readlines()[i + 1]
        data = (next_line.strip()).split(',')
        next_time = data[1]
        #next_time = datetime.strptime(data[1], '%Y-%m-%dT%H:%M:%SZ')
        
        if (curr_time != next_time):
          output_data.write(next_line)
        clean_input(file_name + '_log')


  except FileNotFoundError:
    print("error: file not found")


if __name__ == '__main__':
  file_name = input('file_name: ')
  clean_input(file_name)
  clean_output(file_name)
  complete_output(file_name)
  