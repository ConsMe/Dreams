## To mount yandex cloud storage run as local user  
```
/usr/local/go/bin/geesefs dreams /mnt/dreams  
```

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