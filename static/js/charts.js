/**
 * Chart.js Visualizations for Kaushal Setu
 * Dark Navy & Teal Palette Styling
 */

function renderSkillRadarChart(canvasId, labels, currentScores, targetScores) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Current Score',
                    data: currentScores,
                    backgroundColor: 'rgba(13, 148, 136, 0.25)',
                    borderColor: '#0d9488',
                    pointBackgroundColor: '#0d9488',
                    pointBorderColor: '#ffffff',
                    pointHoverBackgroundColor: '#ffffff',
                    pointHoverBorderColor: '#0d9488',
                    borderWidth: 2
                },
                {
                    label: 'Target Benchmark',
                    data: targetScores,
                    backgroundColor: 'rgba(15, 23, 42, 0.1)',
                    borderColor: '#0f172a',
                    borderDash: [4, 4],
                    pointBackgroundColor: '#0f172a',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(0, 0, 0, 0.08)' },
                    grid: { color: 'rgba(0, 0, 0, 0.06)' },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: {
                        stepSize: 20,
                        backdropColor: 'transparent',
                        font: { size: 10 }
                    },
                    pointLabels: {
                        font: { size: 11, weight: '600' },
                        color: '#1e293b'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        boxWidth: 14,
                        font: { size: 12, weight: '500' }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}

function renderSkillBarChart(canvasId, labels, currentScores, targetScores) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Current Score',
                    data: currentScores,
                    backgroundColor: '#0d9488',
                    borderRadius: 6
                },
                {
                    label: 'Target Benchmark',
                    data: targetScores,
                    backgroundColor: '#cbd5e1',
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        callback: function (val) { return val + '%'; }
                    },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 11, weight: '500' },
                        color: '#334155'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: { boxWidth: 14 }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}
