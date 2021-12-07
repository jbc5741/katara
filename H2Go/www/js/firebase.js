import { initializeApp } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-app.js";
import { getDatabase, ref, onChildAdded, query, limitToLast, onValue } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-database.js";


const firebaseConfig = {
    apiKey: "AIzaSyAgHQhbQPFDCUiHI5DQMvOJkLMxdDgfgBM",
    authDomain: "h2go-575f0.firebaseapp.com",
    databaseURL: "https://h2go-575f0-default-rtdb.firebaseio.com",
    projectId: "h2go-575f0",
    storageBucket: "h2go-575f0.appspot.com",
    messagingSenderId: "466823744518",
    appId: "1:466823744518:web:a36030c3c07f5853738787"
  };


const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const readings_ref = ref(database, 'readings')
let wi_node = document.getElementById('water_intake');
// Recent readings
const NUM_READS = 5;
const query_ref = query(readings_ref, limitToLast(NUM_READS));


console.log(datapoints)

document.addEventListener("DOMContentLoaded", function(e) {
    console.log(JSON.stringify(datapoints))
})

const data = {
    datasets: [{
        data: datapoints,
    }]
 };
const config = {
    type: 'line',
    data: data,
    options: {
        parsing: {
            xAxisKey: 'x',
            yAxisKey: 'y'
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'minute'
                }
            }
        }
    }
};

 let myChart = new Chart(
      document.getElementById('myChart').getContext('2d'),
      config
  );

  console.log("Hello!")

  function addData(chart, time, weight) {
      datapoints.push({x:time, y:weight})
      if (datapoints.length > 25) {
          datapoints.shift()
      }
      chart.update();
  }

  onChildAdded(query_ref, (data) => {
    let dataobj = JSON.parse(data.val());
    let water_intake = dataobj.water;
    let water_time = moment(dataobj.datetime, 'YYYYMMDDHHmmss');

    document.getElementById('file').setAttribute('value', water_intake);

    if (water_intake < 0) {
        water_intake = 0
    }
  
    addData(myChart, water_time.valueOf(), water_intake)
  
    let listnode = document.createElement('li');
    let textnode = document.createTextNode(`${water_time.format('MM-DD-YYYY | HH:mm')} [${water_intake} ml]`);
    listnode.appendChild(textnode);
    wi_node.appendChild(listnode);
    console.log(datapoints)
  });
