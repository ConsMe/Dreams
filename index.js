const express = require('express')
const { spawn } = require('child_process');
var bodyParser = require('body-parser')
var CronJob = require('cron').CronJob;
var kill  = require('tree-kill');
const app = express()
const port = 3000

const TZ = 'Europe/Moscow';
process.env.TZ = TZ;

app.use(express.static('public'))

app.use(express.json()); 
app.use(bodyParser.json())

app.post('/api', (req, res) => {
 
 var dataToSend;
 let python;
 const comm = req.body.comm.split(' ');
 if (comm.length === 1) {
   python = spawn(comm[0]);
 } else {
   python = spawn(comm[0], comm.slice(1));
 }
 python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
 });
 python.on('close', (code) => {
 console.log(`child process close all stdio with code ${code}`);
 res.send(dataToSend)
 });
 
})
// app.listen(port, () => console.log(new Date().toString(), `Example app listening on port 
// ${port}!`))

let recordShouldBeRunning = true;
let recordScript;
let storeScript;

function startRecord() {
  recordScript = spawn('python3', ['record.py']);
  recordScript.on('close', () => {
    console.log(new Date().toString(), 'record stopped no usb', 'recordShouldBeRunning', recordShouldBeRunning);
    recordScript = undefined;
    if (recordShouldBeRunning) startRecord();
  });
}
function stopRecord() {
  if (recordScript !== undefined) {
    recordShouldBeRunning = false;
    kill(recordScript.pid);
    recordScript = undefined;
  }
}

function store() {
  if (storeScript === undefined) {
    storeScript = spawn('python3', ['store.py']);
    storeScript.on('close', () => {
      storeScript = undefined;
    });
  }
}
startRecord();
// new CronJob('0 0 * * *', () => {
//   console.log(new Date().toString(), 'record started');
//   recordShouldBeRunning = true;
//   startRecord();
// }, null, true, TZ);
new CronJob('30 7 * * *', () => {
  console.log(new Date().toString(), 'record stopped by cron');
  stopRecord();
}, null, true, TZ);
new CronJob('*/5 * * * *', () => {
  store();
}, null, true, TZ);