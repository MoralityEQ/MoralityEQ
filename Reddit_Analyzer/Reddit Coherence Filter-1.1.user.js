// ==UserScript==
// @name         Reddit Coherence Filter
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Real-time content moderation using M = ζ - S (Morality = Coherence - Entropy)
// @author       Moral Framework Developer
// @match        https://www.reddit.com/*
// @match        https://old.reddit.com/*
// @grant        none
// @run-at       document-end
// @noframes
// ==/UserScript==

(function() {
    'use strict';

    console.log('🚀 Tampermonkey Reddit Coherence Filter starting...');
    console.log('📍 URL:', window.location.href);

    // Coherence Framework Implementation
    class CoherenceAnalyzer {
        constructor() {
            console.log('🧠 Initializing Coherence Analyzer...');

            // Coherence indicators (enhance understanding)
            this.coherenceKeywords = {
                'evidence': 0.3, 'source': 0.3, 'study': 0.3, 'research': 0.3,
                'data': 0.2, 'fact': 0.2, 'analysis': 0.2, 'nuanced': 0.3,
                'complex': 0.2, 'context': 0.3, 'perspective': 0.2,
                'understand': 0.2, 'clarify': 0.3, 'explain': 0.2,
                'constructive': 0.3, 'thoughtful': 0.3, 'reasonable': 0.2,
                'consider': 0.2, 'acknowledge': 0.2, 'fair point': 0.3,
                'interesting': 0.15, 'informative': 0.25, 'helpful': 0.25,
                'appreciate': 0.2, 'learn': 0.2, 'question': 0.15
            };

            // Entropy indicators (create confusion/conflict)
            this.entropyKeywords = {
                'stupid': 0.4, 'idiot': 0.5, 'moron': 0.5, 'dumb': 0.4,
                'pathetic': 0.3, 'disgusting': 0.4, 'garbage': 0.3,
                'bullshit': 0.3, 'lies': 0.4, 'fake': 0.3, 'propaganda': 0.4,
                'conspiracy': 0.4, 'sheep': 0.4, 'brainwashed': 0.5,
                'wake up': 0.3, 'obvious': 0.2, 'anyone with a brain': 0.4,
                'clearly you': 0.3, 'imagine being': 0.3, 'cope': 0.3,
                'seething': 0.4, 'triggered': 0.3, 'rent free': 0.3,
                'cringe': 0.3, 'cope harder': 0.4, 'delusional': 0.4
            };

            this.processedComments = new Set();
            this.commentScores = new Map();
            console.log('✅ Analyzer ready with', Object.keys(this.coherenceKeywords).length, 'coherence keywords');
        }

        scoreComment(text) {
            const textLower = text.toLowerCase();

            // Base coherence scoring
            let coherenceScore = 0.1; // Baseline for communication attempt
            let entropyScore = 0.0;

            // Check for coherence indicators
            for (const [keyword, weight] of Object.entries(this.coherenceKeywords)) {
                if (textLower.includes(keyword)) {
                    coherenceScore += weight;
                }
            }

            // Check for entropy indicators
            for (const [keyword, weight] of Object.entries(this.entropyKeywords)) {
                if (textLower.includes(keyword)) {
                    entropyScore += weight;
                }
            }

            // Structural analysis
            coherenceScore += this.analyzeStructure(text);
            entropyScore += this.analyzeToxicity(text);

            // Normalize to [0,1] range
            coherenceScore = Math.min(1.0, coherenceScore);
            entropyScore = Math.min(1.0, entropyScore);

            const moralValue = coherenceScore - entropyScore;

            return {
                coherence: Math.round(coherenceScore * 100) / 100,
                entropy: Math.round(entropyScore * 100) / 100,
                moralValue: Math.round(moralValue * 100) / 100
            };
        }

        analyzeStructure(text) {
            let bonus = 0.0;
            const wordCount = text.split(/\s+/).length;

            // Length sweet spot (not too short, not wall of text)
            if (wordCount >= 10 && wordCount <= 200) {
                bonus += 0.1;
            }

            // Proper punctuation
            if (/[.!?]/.test(text)) {
                bonus += 0.05;
            }

            // Paragraph structure for longer posts
            if (wordCount > 50 && text.includes('\n')) {
                bonus += 0.1;
            }

            // Questions that seek understanding
            if (text.includes('?') && wordCount > 5) {
                bonus += 0.1;
            }

            return bonus;
        }

        analyzeToxicity(text) {
            let penalty = 0.0;

            // ALL CAPS YELLING
            const capsRatio = (text.match(/[A-Z]/g) || []).length / Math.max(text.length, 1);
            if (capsRatio > 0.3) {
                penalty += 0.3;
            }

            // Excessive punctuation/emotion
            const exclamationCount = (text.match(/!/g) || []).length;
            const questionCount = (text.match(/\?/g) || []).length;
            if (exclamationCount > 3 || questionCount > 3) {
                penalty += 0.2;
            }

            // Low effort responses
            if (text.split(/\s+/).length < 3) {
                penalty += 0.2;
            }

            // Personal attacks pattern
            if (/\byou\s+(are|'re)\s+\w+/i.test(text)) {
                penalty += 0.3;
            }

            return penalty;
        }
    }

    // UI Controller
    class CoherenceUI {
        constructor(analyzer) {
            console.log('🎨 Initializing UI Controller...');
            this.analyzer = analyzer;
            this.currentThreshold = 0.0;
            this.isActive = false;
            this.recursiveLift = true; // Default to enabled
            this.controlPanel = null;
            this.commentHierarchy = new Map(); // Track parent-child relationships
            this.liftedComments = new Set(); // Track lifted comments
            this.init();
        }

        init() {
            // Wait a bit for page to fully load
            setTimeout(() => {
                this.createControls();
                this.setupEventListeners();
                console.log('🎛️ UI Controls created and ready!');
            }, 1000);
        }

        createControls() {
            // Remove any existing control panel
            const existing = document.getElementById('coherence-controls');
            if (existing) {
                existing.remove();
            }

            // Create control panel
            this.controlPanel = document.createElement('div');
            this.controlPanel.id = 'coherence-controls';
            this.controlPanel.innerHTML = `
                <div style="
                    position: fixed;
                    top: 10px;
                    right: 10px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                    z-index: 999999;
                    font-family: Arial, sans-serif;
                    min-width: 300px;
                    font-size: 14px;
                    border: 2px solid rgba(255,255,255,0.2);
                ">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <span style="font-weight: bold; font-size: 18px;">🧠 Coherence Filter</span>
                        <button id="coherence-toggle" style="
                            margin-left: auto;
                            background: #dc3545;
                            border: none;
                            color: white;
                            padding: 8px 16px;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 14px;
                            font-weight: bold;
                            transition: all 0.3s ease;
                        ">OFF</button>
                    </div>

                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 8px; font-size: 13px; font-weight: bold;">
                            Threshold: <span id="threshold-value" style="color: #FFD700;">0.0</span> (M = ζ - S)
                        </label>
                        <input type="range" id="coherence-slider"
                               min="-1" max="1" step="0.1" value="0"
                               style="
                                   width: 100%;
                                   margin-bottom: 8px;
                                   height: 6px;
                                   background: rgba(255,255,255,0.3);
                                   border-radius: 3px;
                                   outline: none;
                               ">
                        <div style="display: flex; justify-content: space-between; font-size: 10px; opacity: 0.8;">
                            <span>Show All</span>
                            <span>Balanced</span>
                            <span>High Quality</span>
                        </div>
                    </div>

                    <div id="coherence-stats" style="
                        background: rgba(255,255,255,0.15);
                        padding: 12px;
                        border-radius: 6px;
                        font-size: 12px;
                        display: none;
                        border: 1px solid rgba(255,255,255,0.2);
                    ">
                        <div style="margin-bottom: 5px;"><strong>Visible:</strong> <span id="visible-count">0</span>/<span id="total-count">0</span> comments</div>
                        <div style="margin-bottom: 5px;"><strong>Processed:</strong> <span id="processed-count">0</span> comments</div>
                        <div style="margin-bottom: 5px;"><strong>Avg Quality:</strong> <span id="avg-quality">0.00</span></div>
                        <div style="margin-bottom: 8px;">
                            <button id="debug-btn" style="background: #007bff; color: white; border: none; padding: 4px 8px; border-radius: 3px; font-size: 11px; cursor: pointer;">🐛 Debug</button>
                            <button id="reprocess-btn" style="background: #28a745; color: white; border: none; padding: 4px 8px; border-radius: 3px; font-size: 11px; cursor: pointer; margin-left: 5px;">🔄 Reprocess</button>
                        </div>
                        <div style="margin-bottom: 8px;">
                            <label style="font-size: 11px;">
                                <input type="checkbox" id="recursive-lift" checked style="margin-right: 5px;">
                                🚀 Recursive Coherence Lift
                            </label>
                        </div>
                        <div style="font-size: 10px; opacity: 0.8;">
                            Framework: M = Coherence - Entropy
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(this.controlPanel);
            console.log('✅ Control panel added to page');
        }

        setupEventListeners() {
            const toggle = document.getElementById('coherence-toggle');
            const slider = document.getElementById('coherence-slider');
            const thresholdValue = document.getElementById('threshold-value');

            if (!toggle || !slider || !thresholdValue) {
                console.error('❌ Could not find UI elements');
                return;
            }

            toggle.addEventListener('click', () => {
                this.isActive = !this.isActive;
                toggle.textContent = this.isActive ? 'ON' : 'OFF';
                toggle.style.background = this.isActive ? '#28a745' : '#dc3545';

                const stats = document.getElementById('coherence-stats');
                stats.style.display = this.isActive ? 'block' : 'none';

                if (this.isActive) {
                    console.log('🔍 Coherence filter activated - searching for comments...');
                    this.processAllComments();
                } else {
                    console.log('❌ Coherence filter deactivated');
                    this.resetCommentVisibility();
                }
            });

            slider.addEventListener('input', (e) => {
                this.currentThreshold = parseFloat(e.target.value);
                thresholdValue.textContent = this.currentThreshold.toFixed(1);

                if (this.isActive) {
                    console.log(`🎛️ Threshold changed to ${this.currentThreshold}`);
                    this.filterComments();
                }
            });

            // Debug button
            const debugBtn = document.getElementById('debug-btn');
            if (debugBtn) {
                debugBtn.addEventListener('click', () => {
                    this.debugComments();
                });
            }

            // Reprocess button
            const reprocessBtn = document.getElementById('reprocess-btn');
            if (reprocessBtn) {
                reprocessBtn.addEventListener('click', () => {
                    console.log('🔄 Manual reprocessing triggered...');
                    this.analyzer.processedComments.clear();
                    this.analyzer.commentScores.clear();
                    this.liftedComments.clear();
                    this.commentHierarchy.clear();
                    this.processAllComments();
                });
            }

            // Recursive lift toggle
            const recursiveLiftCheckbox = document.getElementById('recursive-lift');
            if (recursiveLiftCheckbox) {
                recursiveLiftCheckbox.addEventListener('change', (e) => {
                    this.recursiveLift = e.target.checked;
                    console.log(`🚀 Recursive lift ${this.recursiveLift ? 'enabled' : 'disabled'}`);
                    if (this.isActive) {
                        this.filterComments();
                    }
                });
            }

            console.log('✅ Event listeners attached');
        }

        findComments() {
            // Comprehensive comment selectors for different Reddit versions
            const selectors = [
                'div[id^="t1_"]',                    // Reddit comment IDs (most reliable)
                '.thing.comment',                    // Old Reddit
                '[data-testid="comment"]',           // New Reddit
                '.Comment',                          // New Reddit alternative
                '.commentarea .thing',               // Old Reddit comments container
                'shreddit-comment',                  // Very new Reddit
                '.comment'                           // Generic fallback
            ];

            let comments = [];
            console.log('🔍 Searching for comments...');

            for (const selector of selectors) {
                const found = document.querySelectorAll(selector);
                console.log(`   ${selector}: ${found.length} elements`);
                if (found.length > 0) {
                    comments = Array.from(found);
                    console.log(`✅ Using selector: ${selector} (${comments.length} comments)`);
                    break;
                }
            }

            if (comments.length === 0) {
                console.log('❌ No comments found with any selector');
                console.log('🌐 Current URL:', window.location.href);
                console.log('📄 Page title:', document.title);
            }

            return comments;
        }

        getCommentText(commentElement) {
            // Comprehensive text extraction for different Reddit layouts
            const textSelectors = [
                '.usertext-body .md',               // Old Reddit markdown
                '.usertext-body',                   // Old Reddit body
                '[data-testid="comment-content"]',  // New Reddit
                '.Comment-body',                    // New Reddit
                '.md',                              // Markdown content
                'p',                                // Any paragraphs
                '.comment-content',                 // Generic content
                '.entry .usertext-body'             // Old Reddit entry
            ];

            for (const selector of textSelectors) {
                const textElement = commentElement.querySelector(selector);
                if (textElement) {
                    const text = textElement.innerText || textElement.textContent || '';
                    if (text.trim().length > 5) { // Make sure we got real content
                        return text.trim();
                    }
                }
            }

            // Last resort: get all text but try to filter out UI elements
            const allText = commentElement.innerText || commentElement.textContent || '';
            return allText.trim();
        }

        processAllComments() {
            console.log('🔄 Processing all comments...');
            const comments = this.findComments();
            let processedCount = 0;

            console.log(`📊 Found ${comments.length} comment elements`);

            // First pass: Build hierarchy map
            this.buildCommentHierarchy(comments);

            comments.forEach((comment, index) => {
                const commentId = this.getCommentId(comment);

                if (!this.analyzer.processedComments.has(commentId)) {
                    const text = this.getCommentText(comment);

                    if (text && text.length > 10) { // Only process substantial comments
                        console.log(`📝 Comment ${index + 1}: "${text.substring(0, 50)}..."`);

                        const scores = this.analyzer.scoreComment(text);
                        console.log(`📊 Scores - M:${scores.moralValue}, ζ:${scores.coherence}, S:${scores.entropy}`);

                        this.analyzer.commentScores.set(commentId, scores);
                        this.analyzer.processedComments.add(commentId);
                        this.addScoreDisplay(comment, scores);
                        processedCount++;
                    }
                }
            });

            console.log(`✅ Processed ${processedCount}/${comments.length} comments`);
            this.updateStats();
            this.filterComments();
        }

        buildCommentHierarchy(comments) {
            console.log('🏗️ Building comment hierarchy...');

            comments.forEach((comment) => {
                const commentId = this.getCommentId(comment);

                // Find parent comment by checking nesting level and DOM position
                const parentComment = this.findParentComment(comment, comments);
                if (parentComment) {
                    const parentId = this.getCommentId(parentComment);
                    this.commentHierarchy.set(commentId, parentId);
                    console.log(`📍 Comment ${commentId} → Parent ${parentId}`);
                }
            });

            console.log(`🏗️ Built hierarchy with ${this.commentHierarchy.size} parent-child relationships`);
        }

        findParentComment(comment, allComments) {
            // Reddit nesting is usually indicated by margin/padding indentation
            const commentRect = comment.getBoundingClientRect();
            const commentLeft = commentRect.left;

            // Look for comments above this one with less left indentation
            let parentCandidate = null;
            let parentLeft = -1;

            for (const otherComment of allComments) {
                if (otherComment === comment) continue;

                const otherRect = otherComment.getBoundingClientRect();
                const otherTop = otherRect.top;
                const otherLeft = otherRect.left;

                // Must be above current comment and less indented
                if (otherTop < commentRect.top && otherLeft < commentLeft) {
                    // Find the closest parent (highest top position among valid parents)
                    if (otherTop > parentLeft) {
                        parentLeft = otherTop;
                        parentCandidate = otherComment;
                    }
                }
            }

            return parentCandidate;
        }

        recursiveCoherenceLift(commentId, scores) {
            console.log(`🔍 Checking lift for comment ${commentId} with M:${scores.moralValue}`);

            if (!this.recursiveLift) {
                console.log(`❌ Recursive lift disabled`);
                return null;
            }

            if (scores.moralValue < this.currentThreshold) {
                console.log(`❌ Comment M:${scores.moralValue} below threshold ${this.currentThreshold}`);
                return null; // Comment itself doesn't meet threshold
            }

            const liftPath = [];
            let currentId = commentId;

            console.log(`🔍 Tracing ancestry for comment ${commentId}...`);

            // Trace back through ancestry to find burial depth
            while (this.commentHierarchy.has(currentId)) {
                const parentId = this.commentHierarchy.get(currentId);
                const parentScores = this.analyzer.commentScores.get(parentId);

                console.log(`📍 Parent ${parentId} has scores:`, parentScores);

                if (parentScores && parentScores.moralValue < this.currentThreshold) {
                    liftPath.push(parentId);
                    console.log(`💔 Parent M:${parentScores.moralValue} below threshold - adding to lift path`);
                    currentId = parentId;
                } else {
                    console.log(`✅ Found acceptable parent or reached root`);
                    break; // Found acceptable parent or root
                }
            }

            if (liftPath.length > 0) {
                console.log(`🚀 LIFT REQUIRED: Comment ${commentId} buried ${liftPath.length} levels deep`);
                console.log(`🎯 Lift path:`, liftPath);
                this.liftedComments.add(commentId);
                return liftPath.length;
            } else {
                console.log(`👍 No lift needed - comment has acceptable ancestry`);
            }

            return null;
        }

        getCommentId(commentElement) {
            // Generate unique ID for comment
            return commentElement.id ||
                   commentElement.dataset.fullname ||
                   commentElement.dataset.commentId ||
                   'comment-' + Array.from(commentElement.parentNode.children).indexOf(commentElement);
        }

        addScoreDisplay(commentElement, scores) {
            // Remove existing score if present
            const existingScore = commentElement.querySelector('.coherence-score');
            if (existingScore) {
                existingScore.remove();
            }

            // Create score badge
            const scoreDisplay = document.createElement('div');
            scoreDisplay.className = 'coherence-score';
            scoreDisplay.style.cssText = `
                display: inline-block !important;
                background: ${scores.moralValue > 0.5 ? '#4CAF50' :
                            scores.moralValue > 0 ? '#FF9800' : '#F44336'} !important;
                color: white !important;
                padding: 3px 8px !important;
                border-radius: 12px !important;
                font-size: 11px !important;
                font-weight: bold !important;
                margin: 3px 5px 3px 0 !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
                font-family: monospace !important;
                z-index: 1000 !important;
                position: relative !important;
            `;
            scoreDisplay.innerHTML = `M:${scores.moralValue}`;

            // Try multiple insertion strategies for better compatibility
            const insertionStrategies = [
                // Strategy 1: Old Reddit tagline
                () => {
                    const tagline = commentElement.querySelector('.tagline');
                    if (tagline) {
                        tagline.appendChild(scoreDisplay);
                        return true;
                    }
                    return false;
                },

                // Strategy 2: After author name
                () => {
                    const author = commentElement.querySelector('.author');
                    if (author && author.parentNode) {
                        author.parentNode.insertBefore(scoreDisplay, author.nextSibling);
                        return true;
                    }
                    return false;
                },

                // Strategy 3: Entry div
                () => {
                    const entry = commentElement.querySelector('.entry');
                    if (entry) {
                        entry.insertBefore(scoreDisplay, entry.firstChild);
                        return true;
                    }
                    return false;
                },

                // Strategy 4: Comment body
                () => {
                    const body = commentElement.querySelector('.usertext-body');
                    if (body) {
                        body.insertBefore(scoreDisplay, body.firstChild);
                        return true;
                    }
                    return false;
                },

                // Strategy 5: Top of comment element
                () => {
                    if (commentElement.firstChild) {
                        commentElement.insertBefore(scoreDisplay, commentElement.firstChild);
                        return true;
                    }
                    return false;
                }
            ];

            // Try each strategy until one works
            let success = false;
            for (let i = 0; i < insertionStrategies.length; i++) {
                try {
                    if (insertionStrategies[i]()) {
                        success = true;
                        console.log(`✅ Badge added using strategy ${i + 1} for score ${scores.moralValue}`);
                        break;
                    }
                } catch (error) {
                    console.log(`⚠️ Strategy ${i + 1} failed:`, error);
                }
            }

            if (!success) {
                console.error(`❌ Failed to add badge for comment with score ${scores.moralValue}`);
                console.log('Comment element:', commentElement);
            }
        }

        filterComments() {
            const comments = this.findComments();
            let visibleCount = 0;
            let liftedCount = 0;
            let filteredOut = [];

            console.log(`🔍 Filtering ${comments.length} comments with threshold ${this.currentThreshold}`);
            console.log(`🚀 Recursive lift: ${this.recursiveLift ? 'ENABLED' : 'DISABLED'}`);

            comments.forEach((comment, index) => {
                const commentId = this.getCommentId(comment);
                const scores = this.analyzer.commentScores.get(commentId);

                if (scores) {
                    let shouldShow = scores.moralValue >= this.currentThreshold;
                    let liftDepth = null;

                    // Check for recursive coherence lift BEFORE applying threshold
                    if (this.recursiveLift && scores.moralValue >= this.currentThreshold) {
                        // This comment meets threshold - check if it should be lifted due to buried ancestry
                        liftDepth = this.recursiveCoherenceLift(commentId, scores);
                        if (liftDepth !== null) {
                            shouldShow = true;
                            liftedCount++;
                            console.log(`🚀 LIFTED: Comment with M:${scores.moralValue} rescued from ${liftDepth} level burial`);

                            // Add lift annotation to the comment
                            this.addLiftAnnotation(comment, liftDepth);
                        }
                    }

                    if (!shouldShow) {
                        filteredOut.push({
                            index: index + 1,
                            moralValue: scores.moralValue,
                            text: this.getCommentText(comment).substring(0, 50)
                        });
                    }

                    comment.style.display = shouldShow ? '' : 'none';
                    if (shouldShow) visibleCount++;
                } else {
                    // Show unprocessed comments by default
                    comment.style.display = '';
                    visibleCount++;
                    console.log(`⚠️ Comment ${index + 1} not processed - showing by default`);
                }
            });

            if (liftedCount > 0) {
                console.log(`🚀 COHERENCE LIFT: Rescued ${liftedCount} high-quality comments from burial!`);
            }

            if (filteredOut.length > 0) {
                console.log(`📋 Filtered out ${filteredOut.length} comments:`, filteredOut);
            }

            this.updateStats();
        }

        addLiftAnnotation(commentElement, liftDepth) {
            // Remove existing lift annotation
            const existingAnnotation = commentElement.querySelector('.lift-annotation');
            if (existingAnnotation) {
                existingAnnotation.remove();
            }

            // Create lift annotation
            const liftAnnotation = document.createElement('div');
            liftAnnotation.className = 'lift-annotation';
            liftAnnotation.style.cssText = `
                background: linear-gradient(45deg, #ff6b6b, #ffa500) !important;
                color: white !important;
                padding: 2px 6px !important;
                border-radius: 8px !important;
                font-size: 10px !important;
                font-weight: bold !important;
                margin: 2px 5px 2px 0 !important;
                display: inline-block !important;
                animation: pulse 2s infinite !important;
            `;
            liftAnnotation.innerHTML = `🚀 LIFTED ${liftDepth} level${liftDepth > 1 ? 's' : ''}`;

            // Add CSS animation
            if (!document.querySelector('#lift-animation-style')) {
                const style = document.createElement('style');
                style.id = 'lift-animation-style';
                style.textContent = `
                    @keyframes pulse {
                        0% { transform: scale(1); }
                        50% { transform: scale(1.05); }
                        100% { transform: scale(1); }
                    }
                `;
                document.head.appendChild(style);
            }

            // Find the score display and add annotation next to it
            const scoreDisplay = commentElement.querySelector('.coherence-score');
            if (scoreDisplay && scoreDisplay.parentNode) {
                scoreDisplay.parentNode.insertBefore(liftAnnotation, scoreDisplay.nextSibling);
            } else {
                // Fallback: add to top of comment
                const target = commentElement.querySelector('.tagline') ||
                              commentElement.querySelector('.entry') ||
                              commentElement.firstElementChild;
                if (target) {
                    target.appendChild(liftAnnotation);
                }
            }
        }

        debugComments() {
            console.log('🐛 === DEBUG REPORT ===');
            const comments = this.findComments();

            console.log(`📊 Total comments found: ${comments.length}`);
            console.log(`📊 Comments processed: ${this.analyzer.processedComments.size}`);
            console.log(`📊 Comments scored: ${this.analyzer.commentScores.size}`);

            console.log('\n📝 Processing status for each comment:');
            comments.forEach((comment, index) => {
                const commentId = this.getCommentId(comment);
                const text = this.getCommentText(comment);
                const scores = this.analyzer.commentScores.get(commentId);
                const hasScoreBadge = comment.querySelector('.coherence-score') !== null;

                console.log(`Comment ${index + 1}:`, {
                    id: commentId,
                    textLength: text.length,
                    processed: this.analyzer.processedComments.has(commentId),
                    scores: scores,
                    hasVisibleBadge: hasScoreBadge,
                    isVisible: comment.style.display !== 'none',
                    preview: text.substring(0, 50) + '...'
                });

                // Special check for missing badges on scored comments
                if (scores && !hasScoreBadge) {
                    console.error(`🚨 MISSING BADGE: Comment ${index + 1} has score ${scores.moralValue} but no badge!`);
                    console.log('Comment HTML structure:', comment.innerHTML.substring(0, 200));

                    // Try to re-add the badge
                    console.log('🔧 Attempting to re-add badge...');
                    this.addScoreDisplay(comment, scores);
                }
            });

            console.log('\n📊 Score distribution:');
            const allScores = Array.from(this.analyzer.commentScores.values());
            const scoreBuckets = {
                'Negative (< 0)': allScores.filter(s => s.moralValue < 0).length,
                'Low (0-0.3)': allScores.filter(s => s.moralValue >= 0 && s.moralValue < 0.3).length,
                'Medium (0.3-0.6)': allScores.filter(s => s.moralValue >= 0.3 && s.moralValue < 0.6).length,
                'High (0.6+)': allScores.filter(s => s.moralValue >= 0.6).length
            };
            console.log(scoreBuckets);

            // Check for specific threshold around 0.35
            console.log('\n🎯 Comments around 0.35 threshold:');
            allScores.forEach((score, index) => {
                if (score.moralValue >= 0.3 && score.moralValue <= 0.4) {
                    const commentId = Array.from(this.analyzer.commentScores.keys())[
                        Array.from(this.analyzer.commentScores.values()).indexOf(score)
                    ];
                    const comment = comments.find(c => this.getCommentId(c) === commentId);
                    const hasBadge = comment ? comment.querySelector('.coherence-score') !== null : false;

                    console.log(`Score ${score.moralValue}: Badge present = ${hasBadge}`);
                }
            });
        }

        updateStats() {
            const comments = this.findComments();
            const totalCount = comments.length;
            let visibleCount = 0;
            let totalMoralValue = 0;
            let scoredCount = 0;

            comments.forEach((comment) => {
                if (comment.style.display !== 'none') {
                    visibleCount++;
                }

                const commentId = this.getCommentId(comment);
                const scores = this.analyzer.commentScores.get(commentId);
                if (scores) {
                    totalMoralValue += scores.moralValue;
                    scoredCount++;
                }
            });

            const avgQuality = scoredCount > 0 ? (totalMoralValue / scoredCount) : 0;

            const visibleElement = document.getElementById('visible-count');
            const totalElement = document.getElementById('total-count');
            const processedElement = document.getElementById('processed-count');
            const avgElement = document.getElementById('avg-quality');

            if (visibleElement) visibleElement.textContent = visibleCount;
            if (totalElement) totalElement.textContent = totalCount;
            if (processedElement) processedElement.textContent = scoredCount;
            if (avgElement) avgElement.textContent = avgQuality.toFixed(2);
        }

        resetCommentVisibility() {
            const comments = this.findComments();
            comments.forEach((comment) => {
                comment.style.display = '';
                const scoreDisplay = comment.querySelector('.coherence-score');
                if (scoreDisplay) {
                    scoreDisplay.remove();
                }
            });
        }
    }

    // Initialize the system
    function initializeCoherenceFilter() {
        console.log('🔧 Initializing Coherence Filter System...');

        // Check if we're on Reddit
        if (!window.location.href.includes('reddit.com')) {
            console.log('❌ Not on Reddit - script will not run');
            return;
        }

        console.log('✅ On Reddit - creating system...');

        try {
            const analyzer = new CoherenceAnalyzer();
            const ui = new CoherenceUI(analyzer);

            // Make UI globally accessible for debugging
            window.coherenceUI = ui;

            console.log('🎉 Reddit Coherence Filter fully loaded!');
            console.log('📊 Framework: M = ζ - S (Morality = Coherence - Entropy)');
            console.log('🎛️ Look for the control panel in the top-right corner');
            console.log('🐛 Debug access: window.coherenceUI');

        } catch (error) {
            console.error('💥 Error initializing coherence filter:', error);
        }
    }

    // Handle different loading states
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeCoherenceFilter);
    } else {
        initializeCoherenceFilter();
    }

    console.log('📜 Script loaded successfully');

})();