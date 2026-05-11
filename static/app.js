let userId = localStorage.getItem('cv_user_id');
if (!userId) {
    userId = generateUUID();
    localStorage.setItem('cv_user_id', userId);
}

let selectedFile = null;

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewArea = document.getElementById('previewArea');
const previewImage = document.getElementById('previewImage');
const btnRemove = document.getElementById('btnRemove');
const btnIdentify = document.getElementById('btnIdentify');
const resultSection = document.getElementById('resultSection');
const resultList = document.getElementById('resultList');
const historyList = document.getElementById('historyList');
const historyEmpty = document.getElementById('historyEmpty');
const loadingOverlay = document.getElementById('loadingOverlay');

uploadArea.addEventListener('click', () => {
    if (!selectedFile) {
        fileInput.click();
    }
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith('image/')) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

btnRemove.addEventListener('click', (e) => {
    e.stopPropagation();
    clearSelection();
});

btnIdentify.addEventListener('click', async () => {
    if (!selectedFile) return;

    showLoading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/classify', {
            method: 'POST',
            headers: {
                'X-User-ID': userId
            },
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            showResults(data.results);
            clearSelection();
            loadHistory();
        } else {
            alert('识别失败: ' + (data.detail || '未知错误'));
        }
    } catch (error) {
        alert('网络错误，请稍后重试');
    } finally {
        showLoading(false);
    }
});

function handleFile(file) {
    if (file.size > 10 * 1024 * 1024) {
        alert('图片大小不能超过 10MB');
        return;
    }

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        showPreview(true);
        btnIdentify.disabled = false;
    };
    reader.readAsDataURL(file);
}

function showPreview(show) {
    const uploadContent = uploadArea.querySelector('.upload-content');
    if (show) {
        uploadContent.hidden = true;
        previewArea.hidden = false;
    } else {
        uploadContent.hidden = false;
        previewArea.hidden = true;
    }
}

function clearSelection() {
    selectedFile = null;
    fileInput.value = '';
    showPreview(false);
    btnIdentify.disabled = true;
    resultSection.hidden = true;
}

function showResults(results) {
    resultSection.hidden = false;
    resultList.innerHTML = '';

    const rankClasses = ['gold', 'silver', 'bronze'];

    results.forEach((result, index) => {
        const item = document.createElement('div');
        item.className = 'result-item';

        const rankClass = rankClasses[index] || 'default';
        const percentage = (result.score * 100).toFixed(2);

        item.innerHTML = `
            <div class="result-rank ${rankClass}">${index + 1}</div>
            <div class="result-info">
                <div class="result-label">${formatLabel(result.label)}</div>
                <div class="result-confidence">
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: 0%"></div>
                    </div>
                    <div class="confidence-value">${percentage}%</div>
                </div>
            </div>
        `;

        resultList.appendChild(item);

        setTimeout(() => {
            item.querySelector('.confidence-fill').style.width = percentage + '%';
        }, 100);
    });
}

function formatLabel(label) {
    const parts = label.split(',');
    if (parts.length > 1) {
        return parts[0].trim();
    }
    return label.split('/').pop().replace(/_/g, ' ');
}

function showLoading(show) {
    loadingOverlay.hidden = !show;
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history', {
            headers: {
                'X-User-ID': userId
            }
        });
        const data = await response.json();

        const records = data.records || [];

        if (records.length === 0) {
            historyEmpty.style.display = 'block';
            return;
        }

        historyEmpty.style.display = 'none';
        historyList.innerHTML = '';

        records.slice(0, 10).forEach(record => {
            const item = document.createElement('div');
            item.className = 'history-item';

            const topResult = record.results[0];
            const confidence = topResult ? (topResult.score * 100).toFixed(2) : '0';
            const label = topResult ? formatLabel(topResult.label) : '未知';
            const time = formatTime(record.time);

            item.innerHTML = `
                <div class="history-thumb">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <path d="M21 15l-5-5L5 21"/>
                    </svg>
                </div>
                <div class="history-info">
                    <div class="history-name">${record.image_name}</div>
                    <div class="history-result">${label}</div>
                    <div class="history-confidence">置信度: ${confidence}%</div>
                </div>
                <div class="history-time">${time}</div>
            `;

            historyList.appendChild(item);
        });
    } catch (error) {
        console.error('加载历史记录失败:', error);
    }
}

function formatTime(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) {
        return '刚刚';
    } else if (diff < 3600000) {
        return Math.floor(diff / 60000) + '分钟前';
    } else if (diff < 86400000) {
        return Math.floor(diff / 3600000) + '小时前';
    } else {
        return date.toLocaleDateString('zh-CN', {
            month: 'numeric',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

loadHistory();
