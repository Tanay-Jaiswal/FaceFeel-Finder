const form = document.getElementById('comment-form');
const errorBox = document.getElementById('error');
const submitBtn = document.getElementById('submit-btn');
const demoBtn = document.getElementById('demo-btn');
const postInput = document.getElementById('post-link');
let chart;

async function runAnalysis(payload) {
  clearError();
  setLoading(true);

  const statusBanner = document.getElementById('status-banner');
  if (statusBanner) {
    statusBanner.textContent = payload?.demo
      ? 'Demo mode active: showing sample sentiment data for local testing.'
      : 'Live mode: using your Facebook token and URL to analyze real comments.';
    statusBanner.style.background = payload?.demo
      ? 'rgba(102,126,234,0.12)'
      : 'rgba(76,175,80,0.08)';
    statusBanner.style.borderColor = payload?.demo
      ? 'rgba(102,126,234,0.25)'
      : 'rgba(76,175,80,0.22)';
  }

  try {
    const res = await fetch('/fetch_comments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      let message = data.error || 'Something went wrong.';
      if (message.includes('ACCESS_TOKEN')) {
        message = 'Missing Facebook access token. Add ACCESS_TOKEN to backend/.env and restart the app.';
      } else if (message.includes('Graph API error')) {
        message = 'Facebook rejected the request. Check your token, permissions, and the Facebook post URL.';
      }
      showError(message);
      return;
    }

    const overallEmotion = data.overall_emotion
      ? data.overall_emotion[0].toUpperCase() + data.overall_emotion.slice(1)
      : '—';

    const overallEl = document.getElementById('overall-emotion');
    overallEl.textContent = overallEmotion;
    overallEl.classList.remove('pulse');
    void overallEl.offsetWidth;
    overallEl.classList.add('pulse');

    const emotionEmoji = document.getElementById('emotion-emoji');
    const emotion = data.overall_emotion?.toLowerCase();
    if (emotion === 'positive') {
      emotionEmoji.textContent = '😊';
    } else if (emotion === 'negative') {
      emotionEmoji.textContent = '😔';
    } else if (emotion === 'neutral') {
      emotionEmoji.textContent = '😐';
    } else {
      emotionEmoji.textContent = '🤔';
    }

    const dist = data.emotion_distribution || { positive: 0, negative: 0, neutral: 0 };
    document.getElementById('positive-count').textContent = dist.positive || 0;
    document.getElementById('negative-count').textContent = dist.negative || 0;
    document.getElementById('neutral-count').textContent = dist.neutral || 0;

    const canvas = document.getElementById('emotionChart');
    const ctx = canvas.getContext('2d');
    const chartData = {
      labels: ['Positive', 'Negative', 'Neutral'],
      datasets: [{
        label: 'Emotion Distribution',
        data: [dist.positive || 0, dist.negative || 0, dist.neutral || 0],
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(200, 200, 200, 0.8)'
        ],
        borderColor: [
          'rgba(102, 126, 234, 1)',
          'rgba(118, 75, 162, 1)',
          'rgba(200, 200, 200, 1)'
        ],
        borderWidth: 2
      }]
    };
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'pie',
      data: chartData,
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: (ti) => `${ti.label}: ${ti.raw} comments`
            }
          }
        }
      }
    });

    const resultsSection = document.querySelector('.results') || canvas;
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    showError('Network error. Check if the server is running.');
  } finally {
    setLoading(false);
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const raw = postInput.value.trim();
  if (!raw || !/^https?:\/\//i.test(raw)) {
    showError('Please enter a valid URL starting with http or https.');
    postInput.focus();
    return;
  }
  runAnalysis({ post_link: raw });
});

demoBtn?.addEventListener('click', () => {
  clearError();
  runAnalysis({ demo: true });
});

function showError(msg){
  errorBox.hidden = false;
  errorBox.textContent = msg;
}

function clearError(){
  errorBox.hidden = true;
  errorBox.textContent = '';
}

function setLoading(isLoading){
  const buttons = [submitBtn, demoBtn].filter(Boolean);
  buttons.forEach((button) => {
    button.disabled = isLoading;
    if (isLoading && button === submitBtn) {
      button.dataset._label = button.innerText;
      button.innerText = 'Analyzing…';
    } else if (!isLoading && button === submitBtn && button.dataset._label) {
      button.innerText = button.dataset._label;
    }
  });
}

postInput?.addEventListener('input', () => { if (!errorBox.hidden) clearError(); });
