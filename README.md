# BD1
BD1 version 1. A poorly 3D printed robot that vaguely resembles BD1 from Jedi Star Wars Fallen Order


Currently this bot is equiped with a 32Longx8High LED matrix, an ultrasonic sensor, a picamera and two servos.
The bot is controlled via discord, however some things are also automated.
In the bd1.py file where most of the stuff happens:

The ultra sonic sensor is constantly checking the distance infront of it, if the distance is ever < 45cm then the bot takes a picture with the picamera and sends that picture to discord. If the distance is <= 15 cm then the bot tells the servo controlling vertical movement to move back, effectively moving the head back otherwise the neck remains upright

The bot can also capture and send a picture on demand using the .capture command in discord.

The bot also checks the price of 3 crypto currencys every half hour and displays it on the LED matrix which is on the back of is head.

The bot can also have text written manually on the LED matrix using the command:
bd1msg YOUR_TEXT_HERE

And finally the bot also has a basically addition and subtraction calulator, which I use to track my spending, which is why its called balance.
.minusbal NUMBER -- minuses that number from the current balance
.addbal NUMBER -- adds that number to the current balance
.balance -- the bot replys with the current balance.


Final note, I've attempted to write the bd1.py asynchronously so that crypto monitor, ultrasonic sensor & discord bot can all run at the same time off of one script.
