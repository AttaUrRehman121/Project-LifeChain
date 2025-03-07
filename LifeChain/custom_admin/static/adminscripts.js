// Sample Data
const donors = [
    { id: 1, name: "John Doe", email: "john@example.com", age: 30, bloodGroup: "A+", location: "New York" },
    { id: 2, name: "Jane Smith", email: "jane@example.com", age: 25, bloodGroup: "B-", location: "Los Angeles" },
  ];
  
  const receptors = [
    { id: 1, name: "Alice Johnson", email: "alice@example.com", age: 40, bloodGroup: "O+", location: "Chicago" },
    { id: 2, name: "Bob Brown", email: "bob@example.com", age: 35, bloodGroup: "AB-", location: "Houston" },
  ];
  
  const userActivity = [
    { userId: 1, name: "John Doe", email: "john@example.com", predictionDate: "2023-10-01", predictionResult: "Match Found" },
    { userId: 2, name: "Jane Smith", email: "jane@example.com", predictionDate: "2023-10-02", predictionResult: "No Match" },
  ];
  
  // Page Navigation
  document.querySelectorAll(".sidebar nav ul li a").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const page = link.getAttribute("data-page");
      showPage(page);
    });
  });
  
  function showPage(page) {
    // Hide all pages
    document.querySelectorAll(".page").forEach(p => p.style.display = "none");
  
    // Show the selected page
    document.getElementById(page).style.display = "block";
  
    // Update page title
    document.getElementById("page-title").textContent = page.charAt(0).toUpperCase() + page.slice(1);
  
    // Render charts for the selected page
    if (page === "donors") renderDonorChart();
    if (page === "receptors") renderReceptorChart();
    if (page === "user-activity") renderActivityChart();
  }
  
  // Show Dashboard by default
  window.onload = () => {
    showPage("dashboard");
    renderDashboardChart();
  };
  
  // Dashboard Chart
  function renderDashboardChart() {
    const ctx = document.getElementById("dashboard-chart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
          label: "User Activity",
          data: [100, 200, 150, 300, 250, 400],
          borderColor: "#3498db",
          borderWidth: 2,
          fill: false,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Monthly User Activity",
            font: {
              size: 16,
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: "#e0e0e0",
            },
          },
          x: {
            grid: {
              display: false,
            },
          },
        },
      },
    });
  }
  
  // Call the function to render the chart
  renderDashboardChart();
  // Enhanced Donor Chart
  function renderDonorChart() {
    const ctx = document.getElementById("donor-chart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["A+", "B+", "O+", "AB+"],
        datasets: [{
          label: "Donors by Blood Group",
          data: [12, 19, 3, 5],
          backgroundColor: ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6"],
          borderColor: ["#2980b9", "#27ae60", "#c0392b", "#8e44ad"],
          borderWidth: 1,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Donor Distribution by Blood Group",
            font: {
              size: 16,
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: "#e0e0e0",
            },
          },
          x: {
            grid: {
              display: false,
            },
          },
        },
      },
    });
  }
  
  // Enhanced Receptor Chart
  function renderReceptorChart() {
    const ctx = document.getElementById("receptor-chart").getContext("2d");
    new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["A+", "B+", "O+", "AB+"],
        datasets: [{
          label: "Receptors by Blood Group",
          data: [8, 15, 7, 10],
          backgroundColor: ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6"],
          borderColor: ["#2980b9", "#27ae60", "#c0392b", "#8e44ad"],
          borderWidth: 1,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Receptor Distribution by Blood Group",
            font: {
              size: 16,
            },
          },
        },
      },
    });
  }
  
  // Enhanced User Activity Chart
  function renderActivityChart() {
    const ctx = document.getElementById("activity-chart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: ["2023-10-01", "2023-10-02", "2023-10-03"],
        datasets: [{
          label: "User Activity",
          data: [10, 20, 15],
          borderColor: "#3498db",
          borderWidth: 2,
          fill: false,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "User Activity Over Time",
            font: {
              size: 16,
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: "#e0e0e0",
            },
          },
          x: {
            grid: {
              display: false,
            },
          },
        },
      },
    });
  }
  
  // Populate Donor Table
  const donorTable = document.getElementById("donor-table").getElementsByTagName("tbody")[0];
  donors.forEach(donor => {
    const row = donorTable.insertRow();
    row.innerHTML = `
      <td>${donor.id}</td>
      <td>${donor.name}</td>
      <td>${donor.email}</td>
      <td>${donor.age}</td>
      <td>${donor.bloodGroup}</td>
      <td>${donor.location}</td>
      <td>
        <button class="btn-view">View</button>
        <button class="btn-update">Update</button>
        <button class="btn-delete">Delete</button>
      </td>
    `;
  });
  
  // Populate Receptor Table
  const receptorTable = document.getElementById("receptor-table").getElementsByTagName("tbody")[0];
  receptors.forEach(receptor => {
    const row = receptorTable.insertRow();
    row.innerHTML = `
      <td>${receptor.id}</td>
      <td>${receptor.name}</td>
      <td>${receptor.email}</td>
      <td>${receptor.age}</td>
      <td>${receptor.bloodGroup}</td>
      <td>${receptor.location}</td>
      <td>
        <button class="btn-view">View</button>
        <button class="btn-update">Update</button>
        <button class="btn-delete">Delete</button>
      </td>
    `;
  });
  
  // Populate User Activity Table
  const activityTable = document.getElementById("activity-table").getElementsByTagName("tbody")[0];
  userActivity.forEach(activity => {
    const row = activityTable.insertRow();
    row.innerHTML = `
      <td>${activity.userId}</td>
      <td>${activity.name}</td>
      <td>${activity.email}</td>
      <td>${activity.predictionDate}</td>
      <td>${activity.predictionResult}</td>
    `;
  });