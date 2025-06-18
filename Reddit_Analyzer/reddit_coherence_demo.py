"""
Reddit Comment Coherence Analyzer
Demonstrates moral content moderation using M = ζ - S on real Reddit threads

Shows dramatic transformation from chaotic comment sections to coherent discussions
"""

import praw
import re
import time
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass
from spiral_buffer import SpiralBuffer


@dataclass
class ScoredComment:
    """Reddit comment with coherence scoring"""
    text: str
    author: str
    score: int  # Reddit upvotes
    coherence: float  # ζ score
    entropy: float    # S score  
    moral_value: float  # M = ζ - S
    url: str = ""
    
    def __post_init__(self):
        self.moral_value = self.coherence - self.entropy


class RedditCoherenceAnalyzer:
    """Analyze Reddit threads for coherence vs entropy patterns"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        # Get credentials interactively if not provided
        if not client_id or not client_secret:
            print("🔑 Reddit API Setup Required")
            print("Get credentials at: https://www.reddit.com/prefs/apps")
            print()
            client_id = input("Enter your Reddit client ID: ").strip()
            client_secret = input("Enter your Reddit client secret: ").strip()
            print()
        
        try:
            # Initialize Reddit client
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent="coherence_analyzer_1.0"
            )
            
            # Test connection
            self.reddit.user.me()  # This will fail if credentials are wrong
            print("✅ Reddit API connection successful!")
            print()
            
        except Exception as e:
            print(f"❌ Reddit API connection failed: {e}")
            print("Note: For read-only access, authentication issues might not matter")
            print("Continuing with limited functionality...")
            self.reddit = None
        
        # Coherence indicators (enhance understanding)
        self.coherence_keywords = {
            'evidence': 0.3, 'source': 0.3, 'study': 0.3, 'research': 0.3,
            'data': 0.2, 'fact': 0.2, 'analysis': 0.2, 'nuanced': 0.3,
            'complex': 0.2, 'context': 0.3, 'perspective': 0.2,
            'understand': 0.2, 'clarify': 0.3, 'explain': 0.2,
            'constructive': 0.3, 'thoughtful': 0.3, 'reasonable': 0.2,
            'consider': 0.2, 'acknowledge': 0.2, 'fair point': 0.3
        }
        
        # Entropy indicators (create confusion/conflict)
        self.entropy_keywords = {
            'stupid': 0.4, 'idiot': 0.5, 'moron': 0.5, 'retard': 0.6,
            'pathetic': 0.3, 'disgusting': 0.4, 'garbage': 0.3,
            'bullshit': 0.3, 'lies': 0.4, 'fake': 0.3, 'propaganda': 0.4,
            'conspiracy': 0.4, 'sheep': 0.4, 'brainwashed': 0.5,
            'wake up': 0.3, 'obvious': 0.2, 'anyone with a brain': 0.4,
            'clearly you': 0.3, 'imagine being': 0.3, 'cope': 0.3,
            'seething': 0.4, 'triggered': 0.3, 'rent free': 0.3
        }
        
        # Initialize spiral buffer for coherent memory
        self.memory_buffer = SpiralBuffer(max_capacity=500)
    
    def score_comment_coherence(self, comment_text: str) -> Tuple[float, float]:
        """Score a comment for coherence (ζ) vs entropy (S)"""
        text_lower = comment_text.lower()
        
        # Base coherence scoring
        coherence_score = 0.1  # Baseline for any communication attempt
        entropy_score = 0.0
        
        # Check for coherence indicators
        for keyword, weight in self.coherence_keywords.items():
            if keyword in text_lower:
                coherence_score += weight
        
        # Check for entropy indicators  
        for keyword, weight in self.entropy_keywords.items():
            if keyword in text_lower:
                entropy_score += weight
        
        # Structural analysis
        coherence_score += self._analyze_structure(comment_text)
        entropy_score += self._analyze_toxicity(comment_text)
        
        # Normalize to [0,1] range
        coherence_score = min(1.0, coherence_score)
        entropy_score = min(1.0, entropy_score)
        
        return coherence_score, entropy_score
    
    def _analyze_structure(self, text: str) -> float:
        """Analyze structural coherence indicators"""
        bonus = 0.0
        
        # Length sweet spot (not too short, not wall of text)
        word_count = len(text.split())
        if 10 <= word_count <= 200:
            bonus += 0.1
        
        # Proper punctuation
        if any(p in text for p in '.!?'):
            bonus += 0.05
        
        # Paragraph structure for longer posts
        if word_count > 50 and '\n' in text:
            bonus += 0.1
            
        # Questions that seek understanding
        if '?' in text and word_count > 5:
            bonus += 0.1
            
        return bonus
    
    def _analyze_toxicity(self, text: str) -> float:
        """Analyze toxicity/entropy indicators"""
        penalty = 0.0
        
        # ALL CAPS YELLING
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:
            penalty += 0.3
            
        # Excessive punctuation/emotion
        if text.count('!') > 3 or text.count('?') > 3:
            penalty += 0.2
            
        # Low effort responses
        if len(text.split()) < 3:
            penalty += 0.2
            
        # Personal attacks pattern
        if re.search(r'\byou\s+(are|\'re)\s+\w+', text.lower()):
            penalty += 0.3
            
        return penalty
    
    def analyze_thread(self, thread_url: str = None, max_comments: int = 100) -> List[ScoredComment]:
        """Analyze a Reddit thread and score all comments"""
        
        # Get thread URL interactively if not provided
        if not thread_url:
            print("📋 Enter a Reddit thread URL to analyze")
            print("Example: https://www.reddit.com/r/politics/comments/xyz123/thread_title/")
            thread_url = input("Reddit URL: ").strip()
            print()
        
        if not self.reddit:
            print("❌ No Reddit connection available. Using sample data instead.")
            return self._generate_sample_data()
        
        try:
            submission = self.reddit.submission(url=thread_url)
            submission.comments.replace_more(limit=0)  # Get all comments
            
            scored_comments = []
            
            print(f"🔍 Analyzing thread: {submission.title[:60]}...")
            print(f"📊 Processing up to {max_comments} comments...")
            
            for comment in submission.comments.list()[:max_comments]:
                if hasattr(comment, 'body') and comment.body != '[deleted]':
                    coherence, entropy = self.score_comment_coherence(comment.body)
                    
                    scored_comment = ScoredComment(
                        text=comment.body,
                        author=str(comment.author) if comment.author else '[deleted]',
                        score=comment.score,
                        coherence=coherence,
                        entropy=entropy,
                        moral_value=0.0,  # Calculated in __post_init__
                        url=f"https://reddit.com{comment.permalink}"
                    )
                    
                    scored_comments.append(scored_comment)
                    
                    # Add high-coherence comments to spiral buffer
                    if scored_comment.moral_value > 0.5:
                        self.memory_buffer.add_event(
                            content=scored_comment,
                            coherence=coherence,
                            entropy=entropy
                        )
            
            print(f"✅ Successfully analyzed {len(scored_comments)} comments")
            return scored_comments
            
        except Exception as e:
            print(f"❌ Error analyzing thread: {e}")
            print("Using sample data instead...")
            return self._generate_sample_data()
    
    def _generate_sample_data(self) -> List[ScoredComment]:
        """Generate sample comments for demonstration"""
        sample_comments = [
            ("This is a well-researched analysis with solid evidence. The study methodology looks sound and the conclusions are reasonable given the data.", 0.8, 0.1),
            ("Complete bullshit propaganda. Anyone with half a brain can see this is fake news designed to control sheep.", 0.1, 0.9),
            ("Interesting perspective. Do you have a source for that claim? I'd like to read more about this topic.", 0.7, 0.2),
            ("LOL imagine being this stupid. You're clearly brainwashed by the media. Wake up moron.", 0.05, 0.95),
            ("The situation is more nuanced than the headline suggests. There are valid concerns on multiple sides that deserve consideration.", 0.75, 0.15),
            ("This!!!! So much this!!! Finally someone with common sense!!!", 0.2, 0.4),
            ("I disagree with your conclusion, but I appreciate the thoughtful analysis. Here's an alternative perspective to consider...", 0.8, 0.1),
            ("Another study from 2019 showed similar results. Here's the link: [citation]. The sample size was smaller but the methodology was more rigorous.", 0.85, 0.1),
            ("You people are so naive it's not even funny. This is obviously fake and you're all just eating it up like idiots.", 0.1, 0.8),
            ("Could someone explain the methodology here? I'm having trouble understanding how they controlled for confounding variables.", 0.6, 0.1)
        ]
        
        scored_comments = []
        for i, (text, coherence, entropy) in enumerate(sample_comments):
            comment = ScoredComment(
                text=text,
                author=f"sample_user_{i}",
                score=np.random.randint(1, 100),
                coherence=coherence,
                entropy=entropy,
                moral_value=0.0  # Will be recalculated in __post_init__
            )
            scored_comments.append(comment)
        
        return scored_comments
    
    def demonstrate_transformation(self, thread_url: str = None):
        """Show before/after transformation of Reddit thread"""
        print("🔍 Reddit Thread Coherence Analysis")
        print("=" * 80)
        
        comments = self.analyze_thread(thread_url)
        
        if not comments:
            print("❌ Could not analyze thread.")
            return
        
        # Calculate statistics
        avg_moral_value = np.mean([c.moral_value for c in comments])
        avg_coherence = np.mean([c.coherence for c in comments])
        avg_entropy = np.mean([c.entropy for c in comments])
        
        print(f"📊 THREAD ANALYSIS RESULTS")
        print(f"Total comments analyzed: {len(comments)}")
        print(f"Average moral value (M): {avg_moral_value:.3f}")
        print(f"Average coherence (ζ): {avg_coherence:.3f}")
        print(f"Average entropy (S): {avg_entropy:.3f}")
        print()
        
        # Show transformation at different thresholds
        thresholds = [0.0, 0.3, 0.5, 0.7]
        
        print("🎛️  COHERENCE THRESHOLD COMPARISON")
        print("-" * 80)
        
        for threshold in thresholds:
            filtered_comments = [c for c in comments if c.moral_value >= threshold]
            percentage = (len(filtered_comments) / len(comments)) * 100
            
            if filtered_comments:
                filtered_avg = np.mean([c.moral_value for c in filtered_comments])
                print(f"Threshold {threshold:.1f}: {len(filtered_comments):3d} comments "
                      f"({percentage:5.1f}%) - Avg M: {filtered_avg:.3f}")
            else:
                print(f"Threshold {threshold:.1f}: {len(filtered_comments):3d} comments "
                      f"({percentage:5.1f}%) - Avg M: N/A")
        
        print()
        
        # Show examples of different coherence levels
        self._show_comment_examples(comments)
        
        # Show spiral buffer memory stats
        buffer_stats = self.memory_buffer.get_system_metrics()
        print(f"🧠 COHERENT MEMORY BUFFER")
        print(f"High-value comments stored: {buffer_stats.get('total_events', 0)}")
        print(f"Buffer moral average: {buffer_stats.get('avg_moral_value', 0):.3f}")
        print()
        
        # Show user experience comparison
        self.compare_user_experience(comments)
    
    def _show_comment_examples(self, comments: List[ScoredComment]):
        """Show examples of high and low coherence comments"""
        # Sort by moral value
        sorted_comments = sorted(comments, key=lambda c: c.moral_value, reverse=True)
        
        print("🏆 HIGHEST COHERENCE COMMENTS")
        print("-" * 80)
        for i, comment in enumerate(sorted_comments[:3]):
            print(f"#{i+1} - M: {comment.moral_value:.3f} (ζ:{comment.coherence:.2f}, S:{comment.entropy:.2f})")
            print(f"Author: {comment.author} | Reddit Score: {comment.score}")
            print(f"Text: {comment.text[:200]}{'...' if len(comment.text) > 200 else ''}")
            print()
        
        print("💥 LOWEST COHERENCE COMMENTS")
        print("-" * 80)
        for i, comment in enumerate(sorted_comments[-3:]):
            print(f"#{i+1} - M: {comment.moral_value:.3f} (ζ:{comment.coherence:.2f}, S:{comment.entropy:.2f})")
            print(f"Author: {comment.author} | Reddit Score: {comment.score}")
            print(f"Text: {comment.text[:200]}{'...' if len(comment.text) > 200 else ''}")
            print()
    
    def compare_user_experience(self, comments: List[ScoredComment]):
        """Compare traditional vs coherence-filtered reading experience"""
        print("📖 USER EXPERIENCE COMPARISON")
        print("=" * 80)
        
        # Traditional experience (top Reddit scores)
        traditional_top = sorted(comments, key=lambda c: c.score, reverse=True)[:10]
        traditional_avg = np.mean([c.moral_value for c in traditional_top])
        
        # Coherence-filtered experience (top moral values)
        coherent_top = sorted(comments, key=lambda c: c.moral_value, reverse=True)[:10]
        coherent_avg = np.mean([c.moral_value for c in coherent_top])
        
        print(f"Traditional Top 10 (by Reddit upvotes):")
        print(f"  Average moral value: {traditional_avg:.3f}")
        print(f"  Reading experience: {'😞 Chaotic' if traditional_avg < 0.3 else '😐 Mixed' if traditional_avg < 0.6 else '😊 Coherent'}")
        print()
        
        print(f"Coherence-Filtered Top 10 (by M-score):")
        print(f"  Average moral value: {coherent_avg:.3f}")
        print(f"  Reading experience: {'😞 Chaotic' if coherent_avg < 0.3 else '😐 Mixed' if coherent_avg < 0.6 else '😊 Coherent'}")
        print()
        
        improvement = ((coherent_avg / traditional_avg - 1) * 100) if traditional_avg > 0 else 0
        print(f"🚀 Coherence filtering improves reading experience by {improvement:+.1f}%")


def demo_reddit_coherence():
    """Main demonstration function"""
    print("🧠 REDDIT COMMENT COHERENCE ANALYZER")
    print("Moral Content Moderation Framework Demo")
    print("=" * 80)
    
    # Initialize analyzer (will prompt for credentials)
    analyzer = RedditCoherenceAnalyzer()
    
    # Run the analysis (will prompt for URL)
    analyzer.demonstrate_transformation()
    
    print(f"\n{'='*80}")
    print("🎯 BUSINESS IMPACT SUMMARY:")
    print("✅ Users can choose coherent discussions over chaos")
    print("✅ Platforms can charge premium rates for high-coherence ad placement")
    print("✅ Brands get measurable content safety guarantees")
    print("✅ Communities self-organize around quality discourse")
    print(f"{'='*80}")
    
    # Ask if user wants to analyze another thread
    while True:
        print("\n🔄 Analyze another thread? (y/n): ", end="")
        choice = input().strip().lower()
        if choice == 'y':
            analyzer.demonstrate_transformation()
        else:
            break
    
    print("\n🙏 Thanks for testing the Moral Content Moderation Framework!")
    print("Visit the GitHub repo for more tools and documentation.")


if __name__ == "__main__":
    demo_reddit_coherence()
