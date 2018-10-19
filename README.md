
# RPiNodeCafe
A NodeJS server and Python scripts to set up a SMS-capable WiFi relay.

A combination of the old RPiCafeLogging (formerly RPiCafe) repo and the ATF-Sonoff-Server

Designed on a Raspberry Pi 3 Model B


# INITIAL STEPS

If you haven't already, a Google account should be created specically for your
 Raspberry Pi.  Then set up Google Voice for the account at voice.google.com.

Afterwards, visit https://accounts.google.com/DisplayUnlockCaptcha and 
allow access to third-party applications without the need for Captcha 
verification.

NOTE: THE SCRIPTS WILL HOLD YOUR GOOGLE PASSWORD IN PLAIN TEXT.
This is why a separate account is suggested.

# Installation Steps
1) Clone the repository onto a Raspberry Pi.

2) Once the repository is cloned, type "./update.sh" into a terminal to run the update and install scripts.

2) Follow the directions.

# Dependencies
The install shell script will ask if you have the dependencies needed before
installing them.

BeautifulSoup

python-crontab

pycurl

StringIO

datetime

pygooglevoice by https://github.com/pettazz

    --- Most updated version of pettazz's project does not work in conjunction, so I've added the correct one to the files ---

# Background
This project was inspired by sleepless nights, impending due dates
and limited financial resources.

The Initial Plan: A Raspberry Pi would control a relay connected to a coffee 
machine. The Pi would receive SMS messages containing key words determining 
whether to toggle the relay immediately or schedule it to execute later.

Cron runs a python script every second to check the Google Voice SMS inbox
for keywords within text messages from the specified sender. Cron will also
log into coffeecron.log in case any errors arise.

Currently, the keywords are "coffee", "cancel" and "schedule coffee TIME" where TIME 
is when the script should run, specified in military time (0000 - 2359).

If the correct keywords are found, the script will execute the command,
log the event in a text file and send an SMS message back to the sender
stating that the operation has been completed.

Similarly, if an incorrect keyword is attempted, the script will log said
phrase in the text file and send a message to the user's specified number.

# Future Possibilities

These scripts may be adjusted to the user's liking, such as changing the
keywords or the specified scripts to be run. It may be possible to run
shell commands on the Pi directly from SMS with simple modifications.
