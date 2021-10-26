## To mount yandex cloud storage run as local user  

/usr/local/go/bin/geesefs dreams /mnt/dreams  

## Setup cron  

### Root  
sudo crontab -e  
50 7 * * * /sbin/shutdown -h now  

### User  
crontab -e  
