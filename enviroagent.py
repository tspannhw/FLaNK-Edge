import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
from time import sleep
from math import isnan
import time
import sys
import datetime
import subprocess
import sys
import os
from subprocess import PIPE, Popen
import datetime
import traceback
import math
import base64
import json
from time import gmtime, strftime
import random, string
import psutil
import base64
import uuid
import socket
from smbus2 import SMBus
from bme280 import BME280
import logging
from enviroplus.noise import Noise
from pms5003 import PMS5003, ReadTimeoutError
noise = Noise()

pms5003 = PMS5003()
time.sleep(1.0)

currenttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
starttime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
start = time.time()

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559
from enviroplus import gas
import ST7735
from PIL import Image, ImageDraw, ImageFont
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

i = 0

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

# Get MAC address of a local interfaces
def psutil_iface(iface):
    # type: (str) -> Optional[str]
    import psutil
    nics = psutil.net_if_addrs()
    if iface in nics:
        nic = nics[iface]
        for i in nic:
            if i.family == psutil.AF_LINK:
                return i.address
# Random Word
def randomword(length):
 return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()) for i in range(length))

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


# Timer
start = time.time()
packet_size=3000

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
ipaddress = IP_address()

# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25

row = { }
# Create unique id
uniqueid = 'air_uuid_{0}_{1}'.format(randomword(3),strftime("%Y%m%d%H%M%S",gmtime()))
uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
cpu_temps = [get_cpu_temperature()] * 5
cpu_temp = round(get_cpu_temperature(),1)
# Smooth out with some averaging to decrease jitter
cpu_temps = cpu_temps[1:] + [cpu_temp]
avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
raw_temp = bme280.get_temperature()
adjtemp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
adjtemp = round(adjtemp,1)
bme280temp = round(bme280.get_temperature(),1)
adjtempf = (adjtemp * 1.8) + 12
adjtempf = round(adjtempf,1)
temperaturef = (bme280temp*1.8)+12
temperaturef = round(temperaturef,1)
amps = noise.get_amplitudes_at_frequency_ranges([
    (100, 200),
    (500, 600),
    (1000, 1200)
])

low, mid, high, amp = noise.get_noise_profile()
end = time.time()

row['uuid'] =  uniqueid
row['amplitude100'] = round(amps[0],1)
row['amplitude500'] = round(amps[1],1)
row['amplitude1000'] = round(amps[2],1)
row['lownoise'] = round(low,1)
row['midnoise'] = round(mid,1)
row['highnoise'] = round(high,1)
row['amps'] = round(amp,1)
row['ipaddress']=ipaddress
row['host'] = os.uname()[1]
row['host_name'] = host_name
row['macaddress'] = psutil_iface('wlan0')
row['systemtime'] = datetime.datetime.now().isoformat()
row['endtime'] = '{0:.2f}'.format(end)
row['runtime'] = '{0:.2f}'.format(end - start)
row['starttime'] = str(starttime)
row['cpu'] = psutil.cpu_percent(interval=1)
row['cpu_temp'] = str(cpu_temp)
usage = psutil.disk_usage("/")
row['diskusage'] = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
row['memory'] = psutil.virtual_memory().percent
row['id'] = str(uuid2)
row['temperature'] = str(bme280temp)
row['adjtemp'] = str(adjtemp)
row['adjtempf'] = str(adjtempf)
row['temperaturef'] = str(temperaturef)
row['pressure'] =  round(bme280.get_pressure(),1)
row['humidity'] = round(bme280.get_humidity(),1)
row['lux'] = round(ltr559.get_lux(),1)
row['proximity'] = round(ltr559.get_proximity(),1)
readings = gas.read_all()
row['oxidising'] = round(readings.oxidising / 1000,1)
row['reducing']  = round(readings.reducing / 1000,1)
row['nh3'] = round(readings.nh3 / 1000,1)
# AMMONIA NH3 1-500PPM
#Carbon monoxide CO 1 – 1000ppm

row['gasKO'] = str(readings)

pm5data = pms5003.read()
row['pm25'] = pm5data.pm_ug_per_m3(2.5)
row['pm1'] = pm5data.pm_ug_per_m3(1.0)
row['pm10'] = pm5data.pm_ug_per_m3(10)
row['pm1atmos'] = pm5data.pm_ug_per_m3(1.0,atmospheric_environment=True)
row['pm25atmos'] = pm5data.pm_ug_per_m3(2.5,atmospheric_environment=True)
row['pm10atmos'] = pm5data.pm_ug_per_m3(None,atmospheric_environment=True)
row['pmper1l03'] = pm5data.pm_per_1l_air(0.3)
row['pmper1l05'] = pm5data.pm_per_1l_air(0.5)
row['pmper1l1'] = pm5data.pm_per_1l_air(1.0)
row['pmper1l25'] = pm5data.pm_per_1l_air(2.5)
row['pmper1l5'] = pm5data.pm_per_1l_air(5)
row['pmper1l10'] = pm5data.pm_per_1l_air(10)

json_string = json.dumps(row)
json_string = json_string.strip()
print(json_string)

# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display.
disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings.
font_size = 12
font = ImageFont.truetype(UserFont, font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 170)

message = "{} P:{}".format(  ipaddress, row['pm25'] )
size_x, size_y = draw.textsize(message, font)

# Calculate text position
x = (WIDTH - size_x) / 2
y = (HEIGHT / 2) - (size_y / 2)

# Draw background rectangle and write text.
draw.rectangle((0, 0, 160, 80), back_colour)
draw.text((x, y), message, font=font, fill=text_colour)
disp.display(img)
