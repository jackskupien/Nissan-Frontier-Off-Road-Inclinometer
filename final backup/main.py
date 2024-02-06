from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI, I2C, ADC
from xglcd_font import XglcdFont

from mpu9250 import MPU9250
from math import sqrt, atan2, pi, copysign, sin, cos, radians

# addresses  
MPU = 0x68
i2c = I2C(id=0, sda=Pin(0),scl=Pin(1))
orn = color565(255,128,0)
pitch_bias = 0.0
roll_bias = 0.0

# Scan the bus
print(i2c.scan())
m = MPU9250(i2c)

# For low pass filtering
filtered_x_value = 0.0 
filtered_y_value = 0.0

p1=0
r1=0

# declination = 40

def degrees_to_heading(degrees):
    heading = ""
    if (degrees > 337) or (degrees >= 0 and degrees <= 22):
            heading = 'N'
    if degrees >22 and degrees <= 67:
        heading = "NE"
    if degrees >67 and degrees <= 112:
        heading = "E"
    if degrees >112 and degrees <= 157:
        heading = "SE"
    if degrees > 157 and degrees <= 202:
        heading = "S"
    if degrees > 202 and degrees <= 247:
        heading = "SW"
    if degrees > 247 and degrees <= 292:
        heading = "W"
    if degrees > 292 and degrees <= 337:
        heading = "NW"
    return heading

def get_reading()->float:
    ''' Returns the readings from the sensor '''
    global filtered_y_value, filtered_x_value
    x = m.acceleration[0] 
    y = m.acceleration[1]
    z = m.acceleration[2] 

    # Pitch and Roll in Radians
    roll_rad = atan2(-x, sqrt((z*z)+(y*y)))
    pitch_rad = atan2(z, copysign(y,y)*sqrt((0.01*x*x)+(y*y)))

    # Pitch and Roll in Degrees
    pitch = pitch_rad*180/pi
    roll = roll_rad*180/pi

    # Get soft_iron adjusted values from the magnetometer
    mag_x, mag_y, magz = m.magnetic

    filtered_x_value = low_pass_filter(mag_x, filtered_x_value)
    filtered_y_value = low_pass_filter(mag_y, filtered_y_value)

    az =  90 - atan2(filtered_y_value, filtered_x_value) * 180 / pi

    # make sure the angle is always positive, and between 0 and 360 degrees
    if az < 0:
        az += 360
        
    # Adjust for original bias
    pitch -= pitch_bias
    roll -= roll_bias

    heading = degrees_to_heading(az)

    return x, y, z, pitch, roll, az, heading

def low_pass_filter(raw_value:float, remembered_value):
    ''' Only applied 20% of the raw value to the filtered value '''
    
    # global filtered_value
    alpha = 0.8
    filtered = 0
    filtered = (alpha * remembered_value) + (1.0 - alpha) * raw_value
    return filtered

# reset orientation to zero
x,y,z, pitch_bias, roll_bias, az, az_raw = get_reading()

def update(x,deg):
    global p1,r1
    num=160
    num2=190
    num3=160
    if(x==0):#if pitch
        if(deg>=5):
            if deg>=25 and (p1!=30):
                display.draw_image('p30.raw', 0, num, num2, num3)
                p1=30
            elif deg>=15 and (p1!=20):
                display.draw_image('p20.raw', 0, num, num2, num3)
                p1=20
            elif p1!=10:
                display.draw_image('p10.raw', 0, num, num2, num3)
                p1=10
        elif(deg<=-5):
            if deg<=-25 and (p1!=-30):
                display.draw_image('p-30.raw', 0, num, num2, num3)
                p1=-30
            elif deg<=-15 and (p1!=-20):
                display.draw_image('p-20.raw', 0, num, num2, num3)
                p1=-20
            elif p1!=-10:
                display.draw_image('p-10.raw', 0, num, num2, num3)
                p1=-10
        else:
            display.draw_image('p.raw', 0, num, num2, num3)
            p1=0
    if(x==1):#if roll
        if(deg>=5):
            if deg>=25 and (r1!=30):
                display.draw_image('r30.raw', 0, 0, num2, num3)
                r1=30
            elif deg>=15 and (r1!=20):
                display.draw_image('r20.raw', 0, 0, num2, num3)
                r1=20
            elif r1!=10:
                display.draw_image('r10.raw', 0, 0, num2, num3)
                r1=10
        elif(deg<=-5):
            if deg<=-25 and (r1!=-30):
                display.draw_image('r-30.raw', 0, 0, num2, num3)
                r1=-30
            elif deg<=-15 and (r1!=-20):
                display.draw_image('r-20.raw', 0, 0, num2, num3)
                r1=-20
            elif r1!=-10:
                display.draw_image('r-10.raw', 0, 0, num2, num3)
                r1=-10
        else:
            display.draw_image('r.raw', 0, 0, num2, num3)
            r1=0
    
    #update p1 and r1
    p1=deg
    r1=deg
            
        


def test():
    display.clear()
    
    #loading screen
    display.draw_image('nissan.raw', 0, 0, 239, 319)
    
    # Calibration and bias offset
    m.ak8963.calibrate(count=5)
    
    print('Loading espresso_dolce')
    espresso_dolce = XglcdFont('EspressoDolce18x24.c', 18, 24)
    #sleep(1)
    
    display.clear()
    #display.draw_image('background.raw', 0, 0, 239, 319)
    
    #bottom image
    display.draw_image('bottom.raw', 190, 0, 50, 320)

    #pitch image
    display.draw_image('p.raw', 0, 160, 190, 160)
    
    #roll image
    display.draw_image('r.raw', 0, 0, 190, 160)
    
    while True:
        x, y, z, pitch, roll, az, heading_value = get_reading()
        print("Pitch",round(pitch,1), "\nRoll",round(roll, 1),"\n")#"compass", az,"Heading", heading_value)
        p=-1*round(pitch)
        r=-1*(round(roll))
        
        #update graphics
        update(0,p)
        update(1,r)
        
        #update text
        #if p<10 and p>-10:
        display.draw_text(200,290, 'Pitch: {}* '.format(abs(p)), espresso_dolce,color565(255, 255, 255),landscape=True)#,background=color565(0, 0, 0))
        #else:
        #    display.draw_text(200,290, 'Pitch: {}*'.format(abs(p)), espresso_dolce,color565(255, 255, 255),landscape=True)
        
        #if r<10 and r>-10:
        display.draw_text(200,117, 'Roll: {}* '.format(abs(r)), espresso_dolce,color565(255, 255, 255),landscape=True)#,background=color565(0, 0, 0))
        #else:
        #    display.draw_text(200,117, 'Roll: {}*'.format(abs(r)), espresso_dolce,color565(255, 255, 255),landscape=True)#,background=color565(0, 0, 0))
        
        #sleep
        sleep(0.2)#previously 1
    
    '''
    display.draw_hline(10, 319, 229, orn)
    sleep(1)

    display.draw_vline(10, 0, 319, orn)
    sleep(1)

    display.fill_hrect(23, 50, 30, 75, orn)
    sleep(1)

    display.draw_hline(0, 0, 222, orn)
    sleep(1)

    display.draw_line(127, 0, 64, 127, orn)
    sleep(2)

    display.clear()

    coords = [[0, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
    display.draw_lines(coords, color565(0, 255, 255))
    sleep(1)

    display.clear()
    display.fill_polygon(7, 120, 120, 100, color565(0, 255, 0))
    sleep(1)

    display.fill_rectangle(0, 0, 15, 227, color565(255, 0, 0))
    sleep(1)

    display.clear()

    display.fill_rectangle(0, 0, 163, 163, color565(128, 128, 255))
    sleep(1)

    display.draw_rectangle(0, 64, 163, 163, color565(255, 0, 255))
    sleep(1)

    display.fill_rectangle(64, 0, 163, 163, color565(128, 0, 255))
    sleep(1)

    display.draw_polygon(3, 120, 286, 30, color565(0, 64, 255), rotate=15)
    sleep(3)

    display.clear()

    display.fill_circle(132, 132, 70, color565(0, 255, 0))
    sleep(1)

    display.draw_circle(132, 96, 70, color565(0, 0, 255))
    sleep(1)

    display.fill_ellipse(96, 96, 30, 16, color565(255, 0, 0))
    sleep(1)

    display.draw_ellipse(96, 256, 16, 30, color565(255, 255, 0))
    '''
    sleep(1)
    display.cleanup()
 
spi = SPI(0, baudrate=10000000, polarity=1,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(18), mosi=Pin(19),miso=Pin(16))
display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
test()

