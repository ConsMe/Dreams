## To mount yandex cloud storage run as local user  
```
/usr/local/go/bin/geesefs dreams /mnt/dreams  
```

<!-- ## Setup cron  

### Root  
sudo crontab -e  
50 7 * * * /sbin/shutdown -h now  

### User  
crontab -e  
@reboot cd /home/evo/Documents/Dreams && /usr/local/bin/forever start index.js >>/home/evo/cron.log 2>&1 -->

## PM2  
```
npm install pm2 -g  
cd ~/path/to/Dreams  
pm2 startup  
```
copy and paste output from prev command  
```
pm2 start index.js  
pm2 save  
```

### Set shut down time before power off  
```
sudo crontab -e  
40 7 * * * /sbin/shutdown -h now 
```