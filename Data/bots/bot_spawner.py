# import Snake_bot
import subprocess
import sys

import keyboard

fh = open('Snake_bot.py')
lines = []
for line in fh:
    # in python 2
    #print(line)
    # in python 3
    lines.append(line)
fh.close()
print(lines[-1])
ask_user_ip = str(input('give ip: '))
lines[-1] = "main('" + ask_user_ip + "',4,False)"
print(lines[-1])
f = open('Bot_2.py', "w")
for line in lines:
    f.write(line)
f.close()
ask_how_many_bots = int(input('Give the number of bots you want to spawn: '))
# ask_how_many_bots=3
threads = []
for loop in range(ask_how_many_bots):
    threads.append(subprocess.Popen([sys.executable, "Bot_2.py"]))
while True:  # making a loop
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        print('Terminating Processes')
        for thread in threads:
            thread.kill()
        break  # finishing the loop
    # print('Press q to terminate all bots')
