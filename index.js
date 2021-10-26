const express = require('express')
const {spawn} = require('child_process');
const app = express()
const port = 3000

app.use(express.static('public'))

app.get('/api', (req, res) => {
 
 var dataToSend;
 // spawn new child process to call the python script
//  const python = spawn('python3', ['record.py']);
//  const python = spawn('lsusb');
 let python;
 const comm = req.body.split(' ');
 if (comm.length === 1) {
   python = spawn(comm[0]);
 } else {
   python = spawn(comm[0], comm.slice(1));
 }
 // collect data from script
 python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
 });
 // in close event we are sure that stream from child process is closed
 python.on('close', (code) => {
 console.log(`child process close all stdio with code ${code}`);
 // send data to browser
 res.send(dataToSend)
 });
 
})
app.listen(port, () => console.log(`Example app listening on port 
${port}!`))