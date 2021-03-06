var AWS = require("aws-sdk");
var fs = require('fs');

AWS.config.update({region: "us-east-1"});

var docClient = new AWS.DynamoDB.DocumentClient();

console.log("Importing Sample Data into Test DynamoDB Schema");

var allQuotes = JSON.parse(fs.readFileSync('sample_zip.json', 'utf8'));
allQuotes.forEach(function(zip) {
    var params = {
        TableName: "sample_zip",
        Item: {
            "id": zip.id,
      			"zip": zip.zip,
      			"date": zip.date,
            "complete" : 0
              }
    };

    docClient.put(params, function(err, data) {
       if (err) {
           console.error("Unable to add date", quote.author, ". Error JSON:", JSON.stringify(err, null, 2));
       } else {
           console.log("PutItem succeeded:", quote.author);
       }
    });
});
