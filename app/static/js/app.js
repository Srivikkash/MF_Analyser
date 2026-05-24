const toggle = document.getElementById('themeToggle');
if (toggle) toggle.onclick = () => {
  const html = document.documentElement;
  html.setAttribute('data-bs-theme', html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark');
};
const chartEl = document.getElementById('navChart');
if (chartEl && window.navData) {
  new Chart(chartEl, {type: 'line', data: {labels: window.navDates, datasets: [{label: 'NAV', data: window.navData, borderColor: '#0d6efd'}]}});
}
