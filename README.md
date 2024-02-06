# Nissan-Frontier-Off-Road-Inclinometer
A simple Raspberry Pi Pico program that uses micropython to display the pitch and roll of my Nissan Frontier. Pieces and parts were pulled from other folks' libraries.

## Hardware
* Raspberry Pi Pico
* ILI9341 touchscreen
* MPU9250 Gyroscope

## What is in these folders?
* Backup is everything that is on the Pi pico when it runs (just a copy of its storage)

## Screen and front end
By far the biggest pain of this project was getting the screen to cooperate. I made most of these pictures from scratch in GIMP. Any picture displayed on the screen I used had to be in a very specific format and size (320x240, I think). I used a helper python program called img2rgb565.py which someone else on here made and I made some modifications to.

## Power Supply
behind the USB outlet there is a mini USB that plugs into the port, I split that with a splitter and fed it through the back of the small cubby next to the traction control switch.

## Questions?
Reach out to me via email (jackskupien@gmail.com) and I will do my best to answer.

### NOTE:
This code is extremely messy. There is a lot I could have done better, if this was a super-serious project. Personally, the function of this inclinometer is not a huge concern of mine. I just wanted a fun project and something to fill this empty cubby.

