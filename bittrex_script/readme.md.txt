# Bitterex Script
A script to monitor BTC Markets data and dispatch an email to users upon choosen increase rate

### How to run
This script is written in python 2.7 so you need to have python 2.7 installed and properly configured. Follow the steps
to run the script:

1. Install the script's required libs by "pip install -r requirements.txt" or you can install them one by one using pip.
2. Run the script using "python script.py"

### Instructions for email:
I have used gmail as server as per your requirements so in order to send emails by this script you have two scenarios:
1. Normal Gmail Account: On normal gmail accounts you have to allow less secure apps in your account, you can consult
   here (https://support.google.com/accounts/answer/6010255?hl=en)

2. Accounts with two factors authentications: Accounts on which two factors auth is enabled you have to generate a new
   password for this app to access then use this password with you user email in the script, you can consult here
   (https://support.google.com/accounts/answer/185833?hl=en)