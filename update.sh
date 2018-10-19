#Updates files with users information
echo "Is this the first time running update or are you changing current info? (y/n) "
read A
echo "Updating files"
if [ "$A" = "y" ]; then
	python initialsetup.py $PWD/tmpfiles/tmpsetup.py setup.py $PWD/tmpfiles/tmpcheckforcoffee.py checkforcoffee.py $PWD/tmpfiles/tmpdeletetextmessages.py deletetextmessages.py $PWD/tmpfiles/tmpjsonconfig $PWD/sonoff-server/sonoff.config.json
	rm initialsetup.py
else
	python setup.py $PWD/tmpfiles/tmpcheckforcoffee.py checkforcoffee.py $PWD/tmpfiles/tmpdeletetextmessages.py deletetextmessages.py
fi

echo "----------------------------------------------


If you haven't already, please log in to your
Raspberry Pi Google Voice Account, then visit
https://accounts.google.com/DisplayUnlockCaptcha
to allow third-party applications to access
the account without a need for Captcha Verification


---------------------------------------------------


Has install.sh been run already? (y/n) "
read ANSWER

if [ "$ANSWER" = 'n' ]; then
	./install.sh
fi
