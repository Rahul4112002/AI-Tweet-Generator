// API URL - automatically uses production URL if deployed, otherwise localhost
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api'
    : 'https://ai-tweet-generator-73ge.onrender.com';

// DOM Elements
const topicInput = document.getElementById('topic');
const generateBtn = document.getElementById('generateBtn');
const errorMessage = document.getElementById('errorMessage');
const loadingSection = document.getElementById('loadingSection');
const resultSection = document.getElementById('resultSection');
const historySection = document.getElementById('historySection');
const finalTweet = document.getElementById('finalTweet');
const evaluationBadge = document.getElementById('evaluationBadge');
const resultTopic = document.getElementById('resultTopic');
const resultIterations = document.getElementById('resultIterations');
const resultLength = document.getElementById('resultLength');
const copyBtn = document.getElementById('copyBtn');
const historyContainer = document.getElementById('historyContainer');

// Generate tweet
generateBtn.addEventListener('click', async () => {
    const topic = topicInput.value.trim();
    
    if (!topic) {
        showError('Please enter a topic');
        return;
    }

    hideError();
    hideResults();
    setLoading(true);

    try {
        const response = await fetch(`${API_URL}/generate-tweet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: topic,
                max_iteration: 3
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate tweet');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to generate tweet. Please try again.');
    } finally {
        setLoading(false);
    }
});

// Copy to clipboard
copyBtn.addEventListener('click', () => {
    const text = finalTweet.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '✅ Copied!';
        copyBtn.style.background = 'var(--black)';
        copyBtn.style.color = 'var(--white)';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = 'var(--white)';
            copyBtn.style.color = 'var(--black)';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
});

// Helper functions
function setLoading(isLoading) {
    if (isLoading) {
        loadingSection.classList.remove('hidden');
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
    } else {
        loadingSection.classList.add('hidden');
        generateBtn.disabled = false;
        generateBtn.textContent = '✨ Generate Tweet';
    }
}

function showError(message) {
    errorMessage.textContent = `⚠️ ${message}`;
    errorMessage.classList.remove('hidden');
}

function hideError() {
    errorMessage.classList.add('hidden');
}

function hideResults() {
    resultSection.classList.add('hidden');
    historySection.classList.add('hidden');
}

function displayResults(data) {
    // Display final tweet
    finalTweet.textContent = data.final_tweet;
    evaluationBadge.textContent = data.evaluation.toUpperCase();
    resultTopic.textContent = data.topic;
    resultIterations.textContent = data.total_iterations;
    resultLength.textContent = data.final_tweet.length;

    resultSection.classList.remove('hidden');

    // Display history
    if (data.history && data.history.length > 0) {
        displayHistory(data.history);
        historySection.classList.remove('hidden');
    }

    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayHistory(history) {
    historyContainer.innerHTML = '';
    
    history.forEach((item) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        historyItem.innerHTML = `
            <div class="history-header">
                <span class="iteration-label">Iteration ${item.iteration}</span>
                <span class="badge">${item.evaluation.toUpperCase()}</span>
            </div>
            <div class="history-tweet">${item.tweet}</div>
            <div class="history-feedback">
                <strong>Feedback:</strong> ${item.feedback}
            </div>
        `;
        
        historyContainer.appendChild(historyItem);
    });
}
