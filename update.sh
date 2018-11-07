#Updates files with users information
echo "Enter '1' if this is your first time installing the repo"
echo "Enter '1' if you're changing information"
echo "Enter '2' if you're updating files after pulling down the repo"
echo "Enter any other key if you want to skip this part."

read A
if [ "$A" = "1" ]; then
	echo "Installing files"
	echo "NOTE: YOUR PASSWORDS YOU ENTER WILL BE STORED IN PLAIN TEXT FILES"
	python $PWD/initialsetup.py $PWD/tmpfiles/tmpsetup.py setup.py $PWD/tmpfiles/tmpcheckforcoffee.py checkforcoffee.py $PWD/tmpfiles/tmpdeletetextmessages.py deletetextmessages.py $PWD/tmpfiles/tmpjsonconfig $PWD/sonoff-server/sonoff.config.json
	rm $PWD/initialsetup.py
fi
if [ "$A" = "2" ]; then
	echo "Updating files"
	python $PWD/setup.py $PWD/tmpfiles/tmpsetup.py $PWD/setup.py
 	python $PWD/setup.py $PWD/tmpfiles/tmpcheckforcoffee.py checkforcoffee.py $PWD/tmpfiles/tmpdeletetextmessages.py deletetextmessages.py $PWD/tmpfiles/tmpjsonconfig $PWD/sonoff-server/sonoff.config.json 
else
	echo "Skipping updating/installing files"
fi

echo "----------------------------------------------


If you haven't already, please log in to your
Raspberry Pi Google Voice Account, then visit
https://accounts.google.com/DisplayUnlockCaptcha
to allow third-party applications to access
the account without a need for Captcha Verification


---------------------------------------------------


"
if [ "$A" = "1"]; then
	echo "Has install.sh been run already? (y/n) "
	read ANSWER

	if [ "$ANSWER" = 'n' ]; then
		./install.sh
	fi
fi