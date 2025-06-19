"""
Reddit Coherence Slider Web App
Simple Flask interface for real-time coherence filtering
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from reddit_coherence_demo import RedditCoherenceAnalyzer, ScoredComment
from typing import List, Dict

app = Flask(__name__)

# Global analyzer instance
analyzer = None
current_comments = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_thread():
    global analyzer, current_comments
    
    data = request.json
    thread_url = data.get('url', '')
    
    if not thread_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Initialize analyzer if needed
        if analyzer is None:
            # For demo, use sample data if no Reddit credentials
            analyzer = RedditCoherenceAnalyzer()
        
        # Analyze the thread
        comments = analyzer.analyze_thread(thread_url, max_comments=200)
        current_comments = comments
        
        # Convert to JSON-serializable format
        comment_data = []
        for comment in comments:
            comment_data.append({
                'text': comment.text,
                'author': comment.author,
                'reddit_score': comment.score,
                'coherence': round(comment.coherence, 3),
                'entropy': round(comment.entropy, 3),
                'moral_value': round(comment.moral_value, 3),
                'url': comment.url
            })
        
        # Calculate thread statistics
        stats = {
            'total_comments': len(comments),
            'avg_moral_value': round(sum(c.moral_value for c in comments) / len(comments), 3),
            'avg_coherence': round(sum(c.coherence for c in comments) / len(comments), 3),
            'avg_entropy': round(sum(c.entropy for c in comments) / len(comments), 3)
        }
        
        return jsonify({
            'success': True,
            'comments': comment_data,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/filter', methods=['POST'])
def filter_comments():
    global current_comments
    
    data = request.json
    threshold = data.get('threshold', 0.0)
    
    if not current_comments:
        return jsonify({'error': 'No comments loaded'}), 400
    
    # Filter comments by moral value threshold
    filtered = [c for c in current_comments if c.moral_value >= threshold]
    
    # Convert to JSON format
    filtered_data = []
    for comment in filtered:
        filtered_data.append({
            'text': comment.text,
            'author': comment.author,
            'reddit_score': comment.score,
            'coherence': round(comment.coherence, 3),
            'entropy': round(comment.entropy, 3),
            'moral_value': round(comment.moral_value, 3),
            'url': comment.url
        })
    
    # Calculate filtered statistics
    if filtered:
        filtered_stats = {
            'visible_comments': len(filtered),
            'percentage': round((len(filtered) / len(current_comments)) * 100, 1),
            'avg_moral_value': round(sum(c.moral_value for c in filtered) / len(filtered), 3),
            'avg_coherence': round(sum(c.coherence for c in filtered) / len(filtered), 3),
            'avg_entropy': round(sum(c.entropy for c in filtered) / len(filtered), 3)
        }
    else:
        filtered_stats = {
            'visible_comments': 0,
            'percentage': 0.0,
            'avg_moral_value': 0.0,
            'avg_coherence': 0.0,
            'avg_entropy': 0.0
        }
    
    return jsonify({
        'success': True,
        'comments': filtered_data,
        'stats': filtered_stats,
        'original_count': len(current_comments)
    })

# Create templates directory and HTML template
def create_template():
    os.makedirs('templates', exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reddit Coherence Slider - Moral Content Moderation Demo</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }
        
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .url-input {
            width: 70%;
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
        }
        
        .analyze-btn {
            background: #28a745;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .analyze-btn:hover {
            background: #218838;
        }
        
        .analyze-btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
        }
        
        .slider-container {
            margin: 20px 0;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 10px;
            border-left: 5px solid #2196f3;
        }
        
        .slider {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: #ddd;
            outline: none;
            -webkit-appearance: none;
        }
        
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            background: #2196f3;
            cursor: pointer;
        }
        
        .slider::-moz-range-thumb {
            width: 25px;
            height: 25px;
            border-radius: 50%;
            background: #2196f3;
            cursor: pointer;
            border: none;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #2196f3;
        }
        
        .stat-label {
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }
        
        .comments-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-height: 600px;
            overflow-y: auto;
        }
        
        .comment {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        
        .comment:last-child {
            border-bottom: none;
        }
        
        .comment-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .comment-author {
            font-weight: bold;
            color: #2196f3;
        }
        
        .comment-scores {
            display: flex;
            gap: 15px;
            font-size: 12px;
            color: #666;
        }
        
        .moral-score {
            padding: 2px 8px;
            border-radius: 12px;
            color: white;
            font-weight: bold;
        }
        
        .moral-positive { background: #28a745; }
        .moral-neutral { background: #ffc107; color: #000; }
        .moral-negative { background: #dc3545; }
        
        .comment-text {
            line-height: 1.5;
            margin-top: 10px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .threshold-display {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .threshold-labels {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Reddit Coherence Slider</h1>
        <p>Real-time demonstration of Moral Content Moderation (M = ζ - S)</p>
        <p><strong>Slide to filter comments by coherence threshold</strong></p>
    </div>
    
    <div class="controls">
        <h3>📋 Step 1: Analyze Reddit Thread</h3>
        <input type="text" id="threadUrl" class="url-input" 
               placeholder="Paste Reddit thread URL here (e.g., https://www.reddit.com/r/science/comments/...)">
        <button id="analyzeBtn" class="analyze-btn">Analyze Comments</button>
        
        <div id="error" class="error" style="display: none;"></div>
    </div>
    
    <div id="sliderSection" style="display: none;">
        <div class="slider-container">
            <h3>🎛️ Step 2: Adjust Coherence Threshold</h3>
            <div class="threshold-display">
                Coherence Threshold: <span id="thresholdValue">0.0</span>
            </div>
            <input type="range" id="coherenceSlider" class="slider" 
                   min="-1" max="1" step="0.1" value="0">
            <div class="threshold-labels">
                <span>-1.0 (Show All)</span>
                <span>0.0 (Balanced)</span>
                <span>+1.0 (Highest Quality Only)</span>
            </div>
        </div>
        
        <div id="stats" class="stats"></div>
        
        <div id="commentsContainer" class="comments-container">
            <div class="loading">Loading comments...</div>
        </div>
    </div>

    <script>
        let currentComments = [];
        
        // Elements
        const analyzeBtn = document.getElementById('analyzeBtn');
        const threadUrl = document.getElementById('threadUrl');
        const sliderSection = document.getElementById('sliderSection');
        const coherenceSlider = document.getElementById('coherenceSlider');
        const thresholdValue = document.getElementById('thresholdValue');
        const commentsContainer = document.getElementById('commentsContainer');
        const statsContainer = document.getElementById('stats');
        const errorDiv = document.getElementById('error');
        
        // Event listeners
        analyzeBtn.addEventListener('click', analyzeThread);
        coherenceSlider.addEventListener('input', updateThreshold);
        
        async function analyzeThread() {
            const url = threadUrl.value.trim();
            if (!url) {
                showError('Please enter a Reddit thread URL');
                return;
            }
            
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = 'Analyzing...';
            hideError();
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Analysis failed');
                }
                
                currentComments = data.comments;
                updateStats(data.stats, data.stats);
                filterComments();
                sliderSection.style.display = 'block';
                
            } catch (error) {
                showError('Error: ' + error.message);
                console.error(error);
            } finally {
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = 'Analyze Comments';
            }
        }
        
        async function updateThreshold() {
            const threshold = parseFloat(coherenceSlider.value);
            thresholdValue.textContent = threshold.toFixed(1);
            
            if (currentComments.length === 0) return;
            
            try {
                const response = await fetch('/filter', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({threshold: threshold})
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Filtering failed');
                }
                
                displayComments(data.comments);
                updateStats(data.stats, {total_comments: data.original_count});
                
            } catch (error) {
                showError('Error filtering: ' + error.message);
                console.error(error);
            }
        }
        
        function filterComments() {
            // Initial display with threshold 0
            updateThreshold();
        }
        
        function displayComments(comments) {
            if (comments.length === 0) {
                commentsContainer.innerHTML = '<div class="loading">No comments meet this coherence threshold</div>';
                return;
            }
            
            const html = comments.map(comment => {
                const moralClass = comment.moral_value > 0.5 ? 'moral-positive' : 
                                  comment.moral_value > 0 ? 'moral-neutral' : 'moral-negative';
                
                return `
                    <div class="comment">
                        <div class="comment-header">
                            <span class="comment-author">${comment.author}</span>
                            <div class="comment-scores">
                                <span class="moral-score ${moralClass}">M: ${comment.moral_value}</span>
                                <span>ζ: ${comment.coherence}</span>
                                <span>S: ${comment.entropy}</span>
                                <span>Reddit: ${comment.reddit_score}</span>
                            </div>
                        </div>
                        <div class="comment-text">${comment.text}</div>
                    </div>
                `;
            }).join('');
            
            commentsContainer.innerHTML = html;
        }
        
        function updateStats(filteredStats, originalStats) {
            const html = `
                <div class="stat-card">
                    <div class="stat-value">${filteredStats.visible_comments}</div>
                    <div class="stat-label">Visible Comments</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${filteredStats.percentage}%</div>
                    <div class="stat-label">Of Original</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${filteredStats.avg_moral_value}</div>
                    <div class="stat-label">Avg Moral Value</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${filteredStats.avg_coherence}</div>
                    <div class="stat-label">Avg Coherence (ζ)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${filteredStats.avg_entropy}</div>
                    <div class="stat-label">Avg Entropy (S)</div>
                </div>
            `;
            
            statsContainer.innerHTML = html;
        }
        
        function showError(message) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        function hideError() {
            errorDiv.style.display = 'none';
        }
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    # Create the HTML template
    create_template()
    
    print("🌐 Starting Reddit Coherence Slider Web App")
    print("=" * 50)
    print("📋 Instructions:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Paste a Reddit thread URL")
    print("3. Click 'Analyze Comments'")
    print("4. Use the slider to filter by coherence threshold")
    print("5. Watch chaos transform into coherent discussion!")
    print()
    print("🎯 Research Use: Perfect for demonstrating M = ζ - S")
    print("💡 Business Use: Show advertisers premium coherent environments")
    print("🧠 Education Use: Visual proof of moral content moderation")
    print("=" * 50)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)