var https = require('https')

function build_path() {
  var postal_code_eq = '22222'
  var country_eq = 'US'
  var key = '12345'
  var date = new Date('1/1/2014').toISOString();
  var api_path = '/v1/' + key + '/history_by_postal_code.json?'
  api_path += 'period=day&postal_code_eq=' + postal_code_eq
  api_path += '&country_eq=' + country_eq
  api_path += '&timestamp_eq=' + date
  api_path += '&&fields=postal_code,country,timestamp,tempMax,tempAvg,tempMin,precip,snowfall,windSpdMax,windSpdAvg,windSpdMin,cldCvrMax,cldCvrAvg,cldCvrMin,dewPtMax,dewPtAvg,dewPtMin,feelsLikeMax,feelsLikeAvg,feelsLikeMin,relHumMax,relHumAvg,relHumMin,sfcPresMax,sfcPresAvg,sfcPresMin,spcHumMax,spcHumAvg,spcHumMin,wetBulbMax,wetBulbAvg,wetBulbMin'
  return api_path
}

console.log(build_path());

var options = {
  host: 'api.weathersource.com',
  port: 443,
  path: build_path()
};

https.request(options, function(res) {
  console.log('STATUS: ' + res.statusCode);
  console.log('HEADERS: ' + JSON.stringify(res.headers));
  res.setEncoding('utf8');
  res.on('data', function (chunk) {
    console.log('BODY: ' + chunk);
  });
}).end();
