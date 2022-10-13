from discord.ext import commands
import discord
import time
import argparse
import asyncio
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import RPi.GPIO as GPIO
import requests
import json
from picamera import PiCamera
bot = commands.Bot(command_prefix=',')


@bot.event
async def on_ready():
    print('online')
    await asyncio.gather(crypto(), us())


async def crypto():
    while True:
        try:
            text = "bd1msg "
            coin = "bitcoin"
            r = requests.get('https://www.coingecko.com/en/coins/' + coin).text
            price = round(float(r.split('"price": ')[1].split(",")[0]),2)
            text = text + "bitcoin:_$"+str(price)+"___"

            coin = "monero"
            r = requests.get('https://www.coingecko.com/en/coins/' + coin).text
            price = round(float(r.split('"price": ')[1].split(",")[0]), 2)
            text = text + "monero:_$" + str(price) + "___"

            coin = "ethereum"
            r = requests.get('https://www.coingecko.com/en/coins/' + coin).text
            price = round(float(r.split('"price": ')[1].split(",")[0]), 2)
            text = text + "ethereum:_$" + str(price) + "___"

            msg(text)
            await asyncio.sleep(1800)
        except:
            print("crypto error")



def msg(discmsg):
    vrl1 = 'First half off webhook url'
    vrl2 = 'second half of the discord webhook url'
    vrl = vrl1 + vrl2

    data = {}
    data["content"] = discmsg
    data["username"] = "BD1GE"

    result = requests.post(vrl, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


async def demo(n, block_orientation, rotate, inreverse):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90,
                     rotate=0, blocks_arranged_in_reverse_order=False)
    print("Created device")

    # start demo
    f = open('message.txt', 'r')
    msg = f.read()
    f.close()

    print(msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT))
    time.sleep(1)


@bot.event
async def on_message(message):
    if message.content.lower().startswith('.addbal'):
        msg = message.content.lower().split(' ')
        msg = msg[1]
        print(msg)
        f = open('balance.txt', 'r')
        balance = f.read()
        f.close()
        msg = int(msg)
        balance = int(balance)
        balance = balance + msg
        f = open('balance.txt', 'w')
        f.write(str(balance))
        f.close()
        await message.channel.send('Your new balance is: ' +  str(balance))
    if message.content.lower().startswith('.minusbal'):
        msg = message.content.lower().split(' ')
        msg = msg[1]
        print(msg)
        f = open('balance.txt', 'r')
        balance = f.read()
        f.close()
        msg = int(msg)
        balance = int(balance)
        balance = balance- msg
        f = open('balance.txt', 'w')
        f.write(str(balance))
        f.close()
        await message.channel.send('Your new balance is: ' +  str(balance))
    if message.content.lower() == '.balance':
        f = open('balance.txt', 'r')
        bal = f.read()
        f.close()
        await message.channel.send(bal)
    if message.content.lower().startswith('bd1msg'):
        print(message.content)
        msg = message.content.lower().split(' ')
        msg = msg[1]
        f = open('message.txt', 'w')
        f.write(msg)
        f.close()
        await message.channel.send('done')
        parser = argparse.ArgumentParser(description='matrix_demo arguments',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--cascaded', '-n', type=int, default=0, help='Number of cascaded MAX7219 LED matrices')
        parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90],
                            help='Corrects block orientation when wired vertically')
        parser.add_argument('--rotate', type=int, default=1, choices=[0, 1, 2, 3],
                            help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
        parser.add_argument('--reverse-order', type=bool, default=False,
                            help='Set to true if blocks are in reverse order')

        args = parser.parse_args()
        await demo(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)

    if message.content.lower().startswith('.capture'):
        try:
            camera = PiCamera()
            camera.vflip = True
            camera.start_preview()
            time.sleep(2)
            camera.capture("test.jpg")
            camera.close()
            await message.channel.send(file=discord.File('test.jpg'))
        except:
            camera = PiCamera()
            camera.vflip = True
            camera.start_preview()
            time.sleep(2)
            camera.capture("test.jpg")
            camera.close()
            await message.channel.send("Try again!")


async def us():
    Trigger = 17
    Echo = 27

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Trigger, GPIO.OUT)
    GPIO.setup(Echo, GPIO.IN)
    GPIO.setwarnings(False)

    try:
        while True:
            GPIO.output(Trigger, False)
            time.sleep(0.5)

            GPIO.output(Trigger, True)
            time.sleep(0.00001)
            GPIO.output(Trigger, False)

            StartTime = time.time()

            while GPIO.input(Echo) == 0:
                StartTime = time.time()

            while GPIO.input(Echo) == 1:
                StopTime = time.time()
                if StopTime - StartTime >= 0.04:
                    print("too closetocalc")
                    StopTime = StartTime
                    break

            Difference = StopTime - StartTime

            Distance = Difference * 34326

            Distance = Distance / 2

            print("distance: " + str(Distance))
            await bot.change_presence(status=discord.Status.online,activity=discord.Game("distance: " + str(Distance)))

            if Distance <= 15:
                f = open('move1.txt', 'w')
                f.write('back')
                f.close()

            else:
                f = open('move1.txt', 'w')
                f.write('half')
                f.close()
                # time.sleep(0.5)
            if Distance < 45:
                msg('.cam1')
                msg('.capture')


            await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()



bot.run('DISCORD API KEY')

