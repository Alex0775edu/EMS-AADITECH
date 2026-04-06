document.addEventListener('DOMContentLoaded', () => {
    initPageAnimations();
    initDashboardCharts();
    initStudentChatbot();
});

function initDashboardCharts() {
    const attendanceChartEl = document.getElementById('attendanceTrendChart');
    const performanceChartEl = document.getElementById('performanceTrendChart');

    if ((!attendanceChartEl && !performanceChartEl) || !window.Chart || !window.dashboardChartPayload) {
        return;
    }

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

    if (attendanceChartEl) {
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
    }

    if (performanceChartEl) {
        new Chart(performanceChartEl, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Performance %',
                    data: data.performance,
                    backgroundColor: data.labels.map((_, index) => index % 2 === 0 ? primary : accent),
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
}

function initPageAnimations() {
    const targets = document.querySelectorAll('.dashboard-kpi, .chart-card, .card, .table-responsive');
    if (!targets.length) return;

    targets.forEach((el, index) => {
        el.classList.add('animatable');
        el.style.transitionDelay = `${Math.min(index * 35, 260)}ms`;
    });

    if (!('IntersectionObserver' in window)) {
        targets.forEach((el) => el.classList.add('in-view'));
        return;
    }

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

    const setOpen = (open) => {
        panel.classList.toggle('open', open);
        panel.setAttribute('aria-hidden', open ? 'false' : 'true');
        trigger.setAttribute('aria-expanded', open ? 'true' : 'false');

        if (open) {
            requestAnimationFrame(() => input.focus());
        } else {
            trigger.focus();
        }
    };

    trigger.setAttribute('aria-controls', 'chatbotWindow');
    trigger.setAttribute('aria-expanded', 'false');
    panel.setAttribute('aria-hidden', 'true');

    trigger.addEventListener('click', () => setOpen(!panel.classList.contains('open')));

    if (closeBtn) {
        closeBtn.addEventListener('click', () => setOpen(false));
    }

    sendBtn.addEventListener('click', () => sendChatMessage(input, messages, sendBtn));

    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendChatMessage(input, messages, sendBtn);
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && panel.classList.contains('open')) {
            setOpen(false);
        }
    });
}

function sendChatMessage(input, messages, sendBtn) {
    const text = input.value.trim();
    if (!text || sendBtn.disabled) return;

    appendBubble(messages, text, 'user');
    input.value = '';
    input.disabled = true;
    sendBtn.disabled = true;

    fetch('/dashboard/chatbot/ask/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ message: text }),
    })
        .then(async (response) => {
            let data = {};
            try {
                data = await response.json();
            } catch (error) {
                data = {};
            }

            if (!response.ok) {
                throw new Error(data.error || 'Assistant is unavailable.');
            }

            appendBubble(messages, data.reply || 'No response', 'bot');
        })
        .catch(() => appendBubble(messages, 'Assistant is unavailable.', 'bot'))
        .finally(() => {
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        });
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
