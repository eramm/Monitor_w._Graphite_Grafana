#!/usr/bin/python3.4
import random
import subprocess

menu = {'bread': '25', 'fish': '25', 'milk': '25', 'nothing': '0'}



catfood = random.choice(list(menu))

serving = menu.get(catfood)

post2carbon = "echo \"pets.cat.food.count " + serving + " `date +%s` \" | nc -q0 127.0.0.1 2003"

#print(post2carbon)

#subprocess.call('echo \"pets.cat.count " + serving + " `date +%s` \" | nc -q0 127.0.0.1 2003', shell=True)

subprocess.call(post2carbon, shell=True)
