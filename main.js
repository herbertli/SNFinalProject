// this script gets senate voting data
// for this project, all votes for the current congress up to April 7, 2017 were used

var request = require('request');
var fs = require("fs");

function getData(voteNumber) {
    var url = "https://www.govtrack.us/data/congress/115/votes/2017/s" + voteNumber + "/data.json";
    request(url, function (error, response, body) {
        if (error) {
            return false;
        } else {
            var fileName = "data/" + voteNumber + ".json";
            fs.writeFile(fileName, body, function (err) {
                if (err) {
                    return false;
                } else {
                    return true;
                }
            });
        }
    });
}

function getAllData() {
    for (var i = 1; i <= 111; i++) {
        if (!getData(i)) {
            console.log("Something went wrong with vote " + i);
        }
    }
}