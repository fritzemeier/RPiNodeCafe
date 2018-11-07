#!/bin/bash
#Installs dependencies
echo "Have you installed all of the dependencies already?"
read A

if [ "$A" = "n" ]; then
	echo "The following questions will attempt to run as a sudoer."
	echo "Do you have the BeautifulSoup python module installed? (y/n) "
	read A
	if [ "$A" = "n" ]; then
		sudo pip install BeautifulSoup
	fi
	echo "Do you have the python-crontab python module installed? (y/n) "
	read A
	if [ "$A" = "n" ]; then
		sudo pip install python-crontab
	fi
	echo "Do you have NodeJS installed? (y/n) "
	read A
	if [ "$A" = "n" ]; then
		sudo apt-get install nodejs
	fi

	echo "Have you already installed the pygooglevoice module from https://github.com/pettazz/pygooglevoice?"
	read A
	if [ "$A" = "n" ]; then
		#Downloads and installs pygooglevoice
		cd pygooglevoice
		sudo python setup.py install
		cd ..
	fi

	echo "




	"
	echo "Finished installing all dependencies"
else
	echo "Skipping the installation step."
fi

echo "Is a cronjob already scheduled to check for coffee?"
read A
if [ "$A" = "n" ]; then
	#Inserts a cron job to check for commands from Google Voice account every minute
	echo "



	Adding cron job to check for check messages every second



	"

	crontab -l >> tmp
	echo "* * * * * python $PWD/checkforcoffee.py >> $PWD/coffeecron.log 2>&1 #coffeecheck" >> tmp
	crontab tmp
	rm tmp
fi

echo "
------------------------------------------------------


If you haven't already, please log in to your
Raspberry Pi Google Voice Account then visit
https://accounts.google.com/DisplayUnlockCaptcha
and allow access to third-party applications without
the need for Captcha verification.

	Press enter to continue.


------------------------------------------------------"

read A

echo "Has update.sh been run already? (y/n) "
read ANSWER

if [ "$ANSWER" = 'n' ]; then
        ./update.sh
fi
