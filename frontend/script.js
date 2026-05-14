async function getWeather(){

    const city=document.getElementById("cityInput").value

    const resultDiv=document.getElementById("result")

    if(city.trim()===""){

        resultDiv.innerHTML=`
        <div class="error">
            Please enter a city name
        </div>
        `

        return

    }

    resultDiv.innerHTML=`
    <div class="loading">
        Fetching live weather data...
    </div>
    `

    try{

        const response=await fetch(
            `http://127.0.0.1:8000/predict-live?city=${city}`
        )

        const data=await response.json()

        console.log(data)

        if(data.error){

            resultDiv.innerHTML=`
            <div class="error">
                ${data.error}
            </div>
            `

            return

        }

        let predictionText="No Rain Expected ☀️"

        let predictionClass="no-rain"

        if(data.prediction===1){

            predictionText="Rain Likely 🌧️"

            predictionClass="rain"

        }

        resultDiv.innerHTML=`

        <div class="weather-main">

            <h2>${data.city}</h2>

            <div class="temperature">
                ${data.weather.tavg}°C
            </div>

            <div class="prediction ${predictionClass}">
                ${predictionText}
            </div>

        </div>

        <div class="weather-grid">

            <div class="card">

                <div class="card-title">
                    Rain Probability
                </div>

                <div class="card-value">
                    ${(data.rain_probability*100).toFixed(1)}%
                </div>

            </div>

            <div class="card">

                <div class="card-title">
                    Pressure
                </div>

                <div class="card-value">
                    ${data.weather.pres} hPa
                </div>

            </div>

            <div class="card">

                <div class="card-title">
                    Minimum Temp
                </div>

                <div class="card-value">
                    ${data.weather.tmin}°C
                </div>

            </div>

            <div class="card">

                <div class="card-title">
                    Maximum Temp
                </div>

                <div class="card-value">
                    ${data.weather.tmax}°C
                </div>

            </div>

        </div>

        `

    }

    catch(error){

        console.log(error)

        resultDiv.innerHTML=`
        <div class="error">
            Backend connection failed
        </div>
        `

    }

}