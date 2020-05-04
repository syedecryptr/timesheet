Move downloaded chrome driver in the same folder.
Current chromedriver present in the repo is for version 80.0.3987.106

Edit creds.txt with your credentials.

## Initiate
	python main.py
	
## For cron job
   

To start script at 2:00pm everyday.
    
    Make the script executable by:
    chmod u+x /path/to/script.py
    
    Open your cron table by
    crontab -e 

    Add the following cron entry:
     0 14 * * * /usr/bin/env python /path/to/main.py
 
