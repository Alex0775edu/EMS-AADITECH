document.addEventListener('DOMContentLoaded', () => {
    initPageAnimations();

    const attendanceChartEl = document.getElementById('attendanceTrendChart');
    const performanceChartEl = document.getElementById('performanceTrendChart');
    if (attendanceChartEl && performanceChartEl && window.Chart && window.dashboardChartPayload) {
        const data = window.dashboardChartPayload;
        const rootStyles = getComputedStyle(document.documentElement);
        const primary = rootStyles.getPropertyValue('--primary').trim() || '#2563eb';
        const accent = rootStyles.getPropertyValue('--accent').trim() || '#14b8a6';
        const border = rootStyles.getPropertyValue('--border').trim() || '#d9e2ef';
        const textSubtle = rootStyles.getPropertyValue('--text-subtle').trim() || '#52637a';
        const surface = rootStyles.getPropertyValue('--card').trim() || '#ffffff';

        Chart.defaults.color = textSubtle;
        Chart.defaults.font.family = "'Inter', 'Segoe UI', sans-serif";
        Chart.defaults.borderColor = border;

        new Chart(attendanceChartEl, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Attendance %',
                    data: data.attendance,
                    borderColor: primary,
                    backgroundColor: 'rgba(37, 99, 235, 0.12)',
                    fill: true,
                    pointBackgroundColor: surface,
                    pointBorderColor: primary,
                    pointRadius: 4,
                    pointHoverRadius: 5,
                    pointBorderWidth: 2,
                    borderWidth: 3,
                    tension: 0.4
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        suggestedMax: 100,
                        ticks: {
                            callback: (value) => `${value}%`
                        }
                    }
                }
            }
        });
        new Chart(performanceChartEl, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Performance %',
                    data: data.performance,
                    backgroundColor: [primary, accent, primary, accent, primary, accent],
                    borderRadius: 14,
                    maxBarThickness: 34
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        suggestedMax: 100,
                        ticks: {
                            callback: (value) => `${value}%`
                        }
                    }
                }
            }
        });
    }

    initStudentChatbot();
});

function initPageAnimations() {
    const targets = document.querySelectorAll('.dashboard-kpi, .chart-card, .card, .table-responsive');
    targets.forEach((el, index) => {
        el.classList.add('animatable');
        el.style.transitionDelay = `${Math.min(index * 35, 260)}ms`;
    });

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12 }
    );

    targets.forEach((el) => observer.observe(el));
}

function initStudentChatbot() {
    const trigger = document.getElementById('chatbotTrigger');
    const panel = document.getElementById('chatbotWindow');
    const closeBtn = document.getElementById('chatbotClose');
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSend');
    const messages = document.getElementById('chatMessages');
    if (!trigger || !panel || !input || !sendBtn || !messages) return;

    trigger.addEventListener('click', () => panel.classList.toggle('open'));
    if (closeBtn) closeBtn.addEventListener('click', () => panel.classList.remove('open'));
    sendBtn.addEventListener('click', () => sendChatMessage(input, messages));
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendChatMessage(input, messages);
        }
    });
}

function sendChatMessage(input, messages) {
    const text = input.value.trim();
    if (!text) return;
    appendBubble(messages, text, 'user');
    input.value = '';

    fetch('/dashboard/chatbot/ask/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ message: text }),
    })
        .then((r) => r.json())
        .then((data) => appendBubble(messages, data.reply || 'No response', 'bot'))
        .catch(() => appendBubble(messages, 'Assistant is unavailable.', 'bot'));
}

function appendBubble(container, text, kind) {
    const div = document.createElement('div');
    div.className = `bubble ${kind}`;
    div.textContent = text;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function getCsrfToken() {
    const cookie = document.cookie.split('; ').find((row) => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}
