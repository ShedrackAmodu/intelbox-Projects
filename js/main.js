// HTML Elements
const dashboardBtn = document.getElementById('dashboardBtn')
const chartSection = document.getElementById("chartSection")
const formSection = document.getElementById("formSection")
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

// Switching from chart to form
dashboardBtn.onclick = function() {
  if (!switched) {
    dashboardBtn.innerText = "Dashboard"
    switched = true
  }
  else {
    dashboardBtn.innerText = "Add Members"
    switched = false
  }
  chartSection.toggleAttribute('hidden')
  formSection.toggleAttribute('hidden')
}

let storedNameData = JSON.parse(localStorage.getItem('userName')) || [];
let storedSkillData = JSON.parse(localStorage.getItem('skillLevel')) || [];

// Creating the chart
let myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: storedNameData,
    datasets: [{
      label: 'Team Members Coding Skills',
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


console.log(storedNameData);
console.log(storedSkillData);

// myChart.data.labels = storedNameData;
// myChart.data.datasets[0].data[0] = storedSkillData;
