'''
Created on June 9, 2016

@author: David Moss and Destry Teeter

Email support@peoplepowerco.com if you have questions!
'''

# LESSON 5 - COMBINING TRIGGERS
# This lesson will demonstrate how to create an bot that is triggered from multiple types
# of triggers.
# 
# VERSION.JSON
# Open up version.json. 
#
# Our trigger is set to Decimal 15.
# 
#     "trigger": 15,
#
# Decimal 11 represents several triggers combined (bitwise-OR'd). Remember our trigger types:
#
#     1'b = 0x1 = Schedule
#     10'b = 0x2 = Location Event (Modes)
#     100'b = 0x4 = Device Alert
#     1000'b = 0x8 = Device Measurement
#     ... and so on.
#
# 11 decimal = 1011'binary
# 1011'binary = 
#     1000'b (Device Measurements) | 10'b (Modes) | 1'b (Schedules)
#
# Therefore, this bot will trigger off of 4 different trigger types: measurements, modes, alerts, and schedules.
#
# We then see the details of each of these triggers down below.
#
# MEASUREMENTS
# Trigger off of Entry Sensors (when the doorStatus parameter is 'true'),
# Water Leak Sensors (when the waterStatus parameter is 'true'),
# and the Virtual Light Switch
# 
#    "deviceTypes": [
#      {
#        "id": 10014,
#        "minOccurrence": 0,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerParamName": "doorStatus",
#        "triggerParamValues": "true",
#        "reason": {
#          "en": "We're going to monitor your doors and windows."
#        }
#      },
#      {
#        "id": 10017,
#        "minOccurrence": 0,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerParamName": "waterStatus",
#        "triggerParamValues": "true",
#        "reason": {
#          "en": "We're going to monitor your water leak detector."
#        }
#      },
#      {
#        "id": 10072,
#        "minOccurrence": 0,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerParamName": "ppc.switchStatus",
#        "triggerParamValues": "0,1",
#        "reason": {
#          "en": "We're going to listen for measurements from your virtual light switch."
#        }
#      },
#
#
# ALERTS
# Trigger when a 'motion' alert is generated by an iOS Presence Camera
#
#      {
#        "id": 24,
#        "minOccurrence": 1,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerAlertType": "motion",
#        "reason": {
#          "en": "Listening for motion recording events"
#        }
#      }
#
# 
# MODES
# Trigger when the user sets their mode to Home, Away, or Vacation. But not sleep.
# 
#    "event": "HOME,AWAY,VACATION",
#
#
# SCHEDULES
# Run once per minute, just to demonstrate it works. Never let a real bot run this fast, forever.
# 
#    "schedule": "0 0/1 * * * ?",
# 
# 


# RUNNING THIS BOT
# First, register your developer account at http://presto.peoplepowerco.com.
#
# This bot will require a device to be connected to your account:
#    Option A:  Buy a Presence Security Pack (http://presencepro.com/store).
#               This is recommended because it will give you a lot more tools
#               to create cool apps with.
#
#    Option B:  Create a virtual light switch locally.
#               Open up another terminal window. In this lesson's directory, run
#               
#               $ python lightSwitch.py
#
#               This will register a new 'Virtual Light Switch' into your account,
#               which you can control manually from its command line.
#               It uses the Device API, and from the point of view of the Ensemble
#               software suite server, is a real device.
# 
#    You will need to have at least 1 entry sensor OR 1 virtual light switch in your
#    account before you can purchase this bot to run it (see below). Otherwise,
#    this bot will be incompatible with your account.
# 
# 
# There are several steps needed to run this bot:
#    1. Create a new directory for your bot, with your own unique bundle ID. Copy all the files into it.
#       Note that bundle ID's are always reverse-domain notation (i.e. com.yourname.YourBot) and cannot
#       be deleted or edited once created.
#    2. Create a new --bot on the server with botengine
#    3. Commit your bot to the server with botengine
#    4. Purchase your bot with botengine
#    5. Run your bot locally
# 
#
# We've automated this for you with a script, 'runlesson.sh'. Run it from your terminal window:
# 
#    $ ./runlesson.sh
#
# 
# This script will automatically do the following for you. 
# From a terminal window *above* this bot's current directory:
# 
# 1. Create a new directory for your bot with your given bundle ID, and copy all the files from this
#    lesson into that new directory.
#
# 
# 2. Create a new bot in your user account with the given bundle ID.
#    
#    botengine --new com.yourname.YourBot
#    
# 
# 3. Commit your bot to the server. 
#    This will push all the code, version information, marketing information, and icon to the server. 
#    The bot will become privately available.
#
#    botengine --commit com.yourname.YourBot
#
# 
# 4. Purchase the bot as if you're an end-user. Note that because your bot is privately available, other end users
#    will not be able to see or access it.
#
#    botengine --purchase com.yourname.YourBot
# 
#    This will return a unique instance ID for your purchased bot, which you may reference to reconfigure the bot instance later.
#    
#    
# 5. Run the bot locally.
#    
#    botengine --run com.yourname.YourBot
#    
#    This will automatically look up your bot instance ID and run the bot, using the real-time streaming data from the server
#    and the code that is on your local computer.
# 

import datetime

def run(botengine):
    # Initialize
    logger = botengine.get_logger()                  # Debug logger
    inputs = botengine.get_inputs()                  # Information input into the bot
    triggerType = botengine.get_trigger_type()       # What type of trigger caused the bot to execute this time
    trigger = botengine.get_trigger_info()           # Get the information about the trigger
    measures = botengine.get_measures_block()        # Capture new measurements, if any
    access = botengine.get_access_block()            # Capture info about all things this bot has permission to access
    alerts = botengine.get_alerts_block()            # Capture new alerts, if any
    
    logger.debug("Inputs: " + str(inputs));     # Save it to our logging debug file, just to show you what's going on. You'll have to run with --console to see this.
    

    if triggerType == 1:
        print("\nExecuting on schedule")
        
        unixTimeMs = int(inputs['time'])
        unixTimeSec = unixTimeMs / 1000
        
        print("\t=> Unix timestamp in milliseconds = " + str(unixTimeMs))
        print("\t=> Human readable timestamp: " + datetime.datetime.fromtimestamp(unixTimeSec).strftime('%Y-%m-%d %H:%M:%S'))

    elif triggerType == 2:
        print("\nExecuting on a change of mode")
        mode = trigger['location']['event']
        print("Your current mode is " + mode)
        
    elif triggerType == 4:
        print("\nExecuting on a device alert")
        for focused_alert in alerts:
            alertType = focused_alert['alertType']
            deviceName = trigger['device']['description']
            
            print("\n\nGot a '" + alertType + "' alert from your '" + deviceName +"'!")
            
            for parameter in focused_alert['params']:
                print("\t" + parameter['name'] + " = " + parameter['value'])
            
    elif triggerType == 8:
        print("\nExecuting on a new device measurement")
        
        deviceType = trigger['device']['deviceType']
        deviceName = trigger['device']['description']
        
        if deviceType == 10014:
            print("\t=> It's an Entry Sensor")
            doorStatus = botengine.get_property(measures, "name", "doorStatus", "value")
            
            if doorStatus == "true":
                print("\t=> Your '" + deviceName + "' opened")
                botengine.execute_again_in_n_seconds(5)
                
            else:
                print("\t=> Your '" + deviceName + "' closed")
        
            
        elif deviceType == 10017:
            print("\t=> It's a Water Sensor")
            waterLeak = botengine.get_property(measures, "name", "waterLeak", "value")
            
            if waterLeak == "true":
                print("\t=> Your '" + deviceName + "' got wet")
                
            else:
                print("\t=> Your '" + deviceName + "' dried up")
                     
    
        elif deviceType == 10072:
            print("\t=> It's a Virtual Light Switch")
            switchStatus = botengine.get_property(measures, "name", "ppc.switchStatus", "value")
            
            if int(switchStatus) > 0:
                print("Your '" + deviceName + "' switched on")
                botengine.execute_again_in_n_seconds(5)
                
            else:
                print("Your '" + deviceName + "' switched off")
                
    elif triggerType == 64:
        print("\nExecuting again, because a device previously triggered the bot and then we called 'botengine.execute_again_in_n_seconds(5)', which you'll learn about in Lesson 8  :)")  
        

