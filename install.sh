#!/bin/bash
#Installs dependencies
echo "Is this your first time running install.sh or are you reinstalling/modifying the install?"
read A

if [ "$A" = "y" ]; then
	echo "Do you have the BeautifulSoup python module installed? (y/n) "
	read A
	if [ "$A" = "n" ]; then
		pip install BeautifulSoup
	fi
	echo "Do you have the python-crontab python module installed? (y/n) "
	read A
	if [ "$A" = "n" ]; then
		pip install python-crontab
	fi

	echo "Is a cronjob already scheduled to check for coffee?"
	read A
	if [ "$A" = "n" ]; then
		#Inserts a cron job to check for commands from Google Voice account every minute
		echo "


		"
		echo "Adding cron job to check for check messages every second



		"
		crontab -l >> tmp
		echo "* * * * * python $PWD/checkforcoffee.py >> $PWD/coffeecron.log 2>&1 #coffeecheck" >> tmp
		crontab tmp
		rm tmp
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
fi

echo "
------------------------------------------------------


If you haven't already, please log in to your
Raspberry Pi Google Voice Account then visit
https://accounts.google.com/DisplayUnlockCaptcha
and allow access to third-party applications without
the need for Captcha verification.


------------------------------------------------------


Has update.sh been run already? (y/n) "
read ANSWER

if [ "$ANSWER" = 'n' ]; then
        ./update.sh
fi
