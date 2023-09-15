// app.js

const path = require("path");
const express = require("express");
const { exec } = require('child_process');
const app = express();
const cors = require("cors");  // Add this line
app.use(cors());

app.use(express.json());

function genericResponse(res,success,data, message) {
    return  res.json({
      success : success,
      data : data,
      message :  message
    })
  }


app.post("/api/avatar", (req, res) => {    
    const text = req.body.text
    const scriptPath = path.join(__dirname, 'spectre.py');  
    if (text){
    exec(`py "${scriptPath}" "${text}"`, { timeout: 5000 }, async (error, stdout, stderr) => {
        if (stdout)
        {
            return genericResponse(res, false, stdout,"Success request");
        }
        else {
          console.error(`An error occurred: ${error}`);
          return genericResponse(res, false, null,error || 'Something was wrong...');
        }  
    })  
    } else {
      return genericResponse(res, false, null, 'Text is required..');
    }        
});

const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});