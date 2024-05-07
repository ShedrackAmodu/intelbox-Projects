


// HTML Elements
const dashboardBtn = document.getElementById('dashboardBtn')
const chartSection = document.getElementById("chartSection")
const formSection = document.getElementById("formSection")
const btnLight = document.querySelector('.btnLight');
let switched = false

  
// Chart Values
let xValues = [];

let xValues_sd = JSON.stringify(xValues);

// localStorage.setItem("xValues", xValues_sd)

let xValues_ds = JSON.parse(localStorage.getItem("xValues"))

let yValues = [];
let barColors = ["aquamarine", "cornflowerblue", "blueviolet"];

// Chart Canvas
const ctx = document.getElementById('myChart');


let storedNameData = JSON.parse(localStorage.getItem('userName')) || [];
let storedSkillData = JSON.parse(localStorage.getItem('skillLevel')) || [];

// Creating the chart
let myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: storedNameData,
    datasets: [{
      label: 'Coding Skill Level',
      backgroundColor: barColors,
      data: storedSkillData
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

btnLight.addEventListener('click', () => {
  document.body.classList.toggle('light-mode');
  if (document.body.classList.contains('light-mode')) {
      localStorage.setItem('theme', 'light-mode');
  } else{
      localStorage.removeItem('theme');
  }
})

// PROPER IMPLEMENTATION OF THE THEME STORAGE
const theme = localStorage.getItem('theme');
if (theme) {
document.body.classList.add('light-mode');
}

console.log(storedNameData);
console.log(storedSkillData);

// myChart.data.labels = storedNameData;
// myChart.data.datasets[0].data[0] = storedSkillData;
