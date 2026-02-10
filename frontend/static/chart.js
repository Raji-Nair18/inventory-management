fetch("/sales_data")
.then(res => res.json())
.then(data => {
    new Chart(document.getElementById("salesChart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Sales",
                data: data.values
            }]
        }
    });
});
