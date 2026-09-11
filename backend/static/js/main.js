const form = document.getElementById('comment-form');
const errorBox = document.getElementById('error');
const submitBtn = document.getElementById('submit-btn');
const postInput = document.getElementById('post-link');
let chart;

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearError();

  // Basic URL sanity check
  const raw = postInput.value.trim();
  if (!raw || !/^https?:\/\//i.test(raw)) {
    showError('Please enter a valid URL starting with http or https.');
    postInput.focus();
    return;
  }

  setLoading(true);

  const link = raw;

  try {
    const res = await fetch('/fetch_comments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ post_link: link })
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.error || 'Something went wrong.');
      return;
    }

    // Update overall emotion and emoji
    const overallEmotion = data.overall_emotion
      ? data.overall_emotion[0].toUpperCase() + data.overall_emotion.slice(1)
      : '—';
    
    const overallEl = document.getElementById('overall-emotion');
    overallEl.textContent = overallEmotion;
    overallEl.classList.remove('pulse'); // restart animation
    void overallEl.offsetWidth;
    overallEl.classList.add('pulse');
    
    // Set emotion emoji based on overall emotion
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

    // Chart
    const canvas = document.getElementById('emotionChart');
    const ctx = canvas.getContext('2d');
    const dist = data.emotion_distribution || {positive:0,negative:0,neutral:0};
    const chartData = {
      labels: ['Positive', 'Negative', 'Neutral'],
      datasets: [{
        label: 'Emotion Distribution',
        data: [dist.positive||0, dist.negative||0, dist.neutral||0],
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

    // Smooth scroll to chart on update
    const resultsSection = document.querySelector('.results') || canvas;
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    showError('Network error. Check if the server is running.');
  } finally {
    setLoading(false);
  }
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
  if (!submitBtn) return;
  if (isLoading) {
    submitBtn.disabled = true;
    submitBtn.dataset._label = submitBtn.innerText;
    submitBtn.innerText = 'Analyzing…';
  } else {
    submitBtn.disabled = false;
    if (submitBtn.dataset._label) submitBtn.innerText = submitBtn.dataset._label;
  }
}

// Clear error while user types
postInput?.addEventListener('input', () => { if (!errorBox.hidden) clearError(); });
