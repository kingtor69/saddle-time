// setup:
const weatherTable = document.querySelector("#weather-table")
const weatherTableHTML = weatherTable.innerHTML

const testWeatherObj = {
    "city": "Albuquerque",
    "conditions": "Scattered Clouds",
    "weather_icon_url": "http://openweathermap.org/img/wn/03d@2x.png",
    "current_weather_details": {
        "Temperature": "25.0℃",
        "Feels Like": "24.6℃",
        "High": "28.0℃",
        "Low": "16.9℃",
        "Relative Humidity": "39%",
        "Wind Speed": "1.8 km/h",
        "Wind Direction": "33° Northeasterly"
    }
}

const testWeatherHeaderConditionsTh = `<th class="h3" id="weather-conditions">Scattered Clouds</th>`
const testWeatherHeaderIconImg = `<img src="http://openweathermap.org/img/wn/03d@2x.png">`

const testTemperatureTd = '<td class="weather-detail-value">25.0℃</td>'
const testFeelsLikeTd = '<td class="weather-detail-value">24.6℃</td>'
const testWindDirectionTd = '<td class="weather-detail-value">33° Northeasterly</td>'


////////////////////
// TESTS
describe('weather display to home page', function() {
    it('should show the weather conditions and icon', function() {
        expect(updateWeatherDOM(testWeatherObj).indexOf(testWeatherHeaderConditionsTh) !== -1).toBe(true);
        expect(updateWeatherDOM(testWeatherObj).indexOf(testWeatherHeaderIconImg) !== -1).toBe(true);
    });
    it('should show the weather details in the table', function() {
        expect(updateWeatherDOM(testWeatherObj).indexOf(testTemperatureTd) !== -1).toBe(true);
        expect(updateWeatherDOM(testWeatherObj).indexOf(testFeelsLikeTd) !== -1).toBe(true);
        expect(updateWeatherDOM(testWeatherObj).indexOf(testWindDirectionTd) !== -1).toBe(true);
    })
});

///////////////////
// tearDown
// afterAll(function(){
//     weatherTable.innerHTML = weatherTableHTML
// })
// this works, but it breaks the JS on the page
// TODO: see if it can work without doing that
// in the meantime, I'm just leaving it out and knowing that on first load the data onscreen is not current, but is rather test data