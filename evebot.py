import xml.etree.ElementTree as ET
import requests
import sys, getopt
import csv
import sys


eve_central_base_url = 'http://api.eve-central.com/api/marketstat'

import discord
from discord.ext.commands import Bot

my_bot = Bot(command_prefix="!")
price = 0;

def query(item_id, system_id, system_name, item_name):
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
    sell_min = sell.findtext('min')
    
    output = "__**" + item_name + "**__:\n"
    output += "The Minimum Sell Order in " + system_name + " is: **" + convert_ISK(sell_min) + "**\n"
    output += "The Median Sell Order in " + system_name + " is: **" + convert_ISK(sell_median) + "**\n"
    output += "The Maximum Buy Order in " + system_name + " is: **" + convert_ISK(buy_max) + "**\n"
    output += "There are __**" + add_commas(sell_vol) + "**__ units in sell orders."
    return output

def queryPlex():
    payload = {
        'typeid': 44992,
        'usesystem': 30000142,
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
    sell_min = sell.findtext('min')

    temp_med = sell_min
    omega = float(temp_med) * 500

    
    output = "__**PLEX:**__\n"
    output += "The Minimum Sell Order in Jita is: **" + convert_ISK(sell_min) + "**\n"
    output += "Based this price it costs around **" + convert_ISK(omega) + "** for an Omega Subscription. \n"
    output += "The Maximum Buy Order in Jita is: **" + convert_ISK(buy_max) + "**\n"
    output += "There are __**" + add_commas(sell_vol) + "**__ on the market." + "\n"

    return output

def find_id(item_name):
    with open('typeids.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            temp = row[1]
            if item_name.upper() == temp.upper():
                return row
        return(item_name + "- NOT FOUND")


def combineArgs(args):
    other = ""
    other+= args[0]
    for i in range(1, len(args)):
        other += " "
        other += args[i]
    return other


def convert_ISK(raw_amount):
    return '{:,.2f} ISK'.format(float(raw_amount))

def add_commas(raw_amount):
    return '{:,}'.format(int(raw_amount))


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
async def plex(*args):
    return await my_bot.say(queryPlex())

@my_bot.command()
async def jita(*args):
    inputString = combineArgs(args)
    found_id = find_id(inputString)
    return await my_bot.say(query(found_id[2], 30000142, "Jita", found_id[1]))

@my_bot.command()
async def amarr(*args):
    inputString = combineArgs(args)
    found_id = find_id(inputString)
    return await my_bot.say(query(found_id[2], 30002187, "Amarr", found_id[1]))


my_bot.run(sys.argv[1])