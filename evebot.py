import xml.etree.ElementTree as ET
import requests
import sys, getopt
import csv

eve_central_base_url = 'http://api.eve-central.com/api/marketstat'

import discord
from discord.ext.commands import Bot

my_bot = Bot(command_prefix="!")
price = 0;

def query(item_id, system_id):
    payload = {
        'typeid': item_id,
        'usesystem': system_id,
    }

    req = requests.post(eve_central_base_url, data=payload)
    response = req.text

    tree = ET.fromstring(response)
    marketstat = tree.find('marketstat')
    type_ = marketstat.find('type')
    buy = type_.find('buy')
    buy_max = buy.findtext('max')
    sell = type_.find('sell')
    sell_vol = sell.findtext('volume')
    sell_median = sell.findtext('median')
    output = "The Median Price in Jita is:       " + sell_median + "\n"
    output += "The Sell Volume is:                     " + sell_vol
    return output

def find_id(item_name):
    with open('typeids.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if item_name == row[1]:
                return row[2]
        return(item_name + "- NOT FOUND")


def combineArgs(args):
    other = ""
    other+= args[0]
    for i in range(1, len(args)):
        other += " "
        other += args[i]
    return other



@my_bot.event
async def on_read():
    print("Client logged in")

@my_bot.command()
async def commands(*args):
    return await my_bot.say("!jita <item name> \n!amarr <item name>")

@my_bot.command()
async def testargs(*args):
    other = combineArgs(args)
    found_id = find_id(other)
    return await my_bot.say(query(found_id, 30000142))

@my_bot.command()
async def jita(*args):
    inputString = combineArgs(args)
    found_id = find_id(inputString)
    return await my_bot.say(query(found_id, 30000142))

@my_bot.command()
async def amarr(*args):
    inputString = combineArgs(args)
    found_id = find_id(inputString)
    return await my_bot.say(query(found_id, 30002187))


my_bot.run(fuck you bruh)



