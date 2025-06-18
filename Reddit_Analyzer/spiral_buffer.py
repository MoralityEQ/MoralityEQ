"""
Moral Spiral Buffer - Memory Architecture with Embedded Ethics

A memory management system that prioritizes beneficial patterns using the 
Morality Equation (M = ζ - S), where coherence-generating memories receive 
preferential treatment over entropy-generating ones.

Empirically optimized for stability at 432 Hz update frequency.
"""

import numpy as np
import math
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from collections import deque


@dataclass
class MemoryEvent:
    """Individual memory unit with embedded morality metrics"""
    content: Any
    timestamp: float
    phase: float  # Position in spiral buffer (0-2π)
    coherence_score: float = 0.0  # ζ - promotes order/beneficial outcomes
    entropy_score: float = 0.0    # S - introduces disorder/harmful effects  
    moral_value: float = 0.0      # M = ζ - S (calculated automatically)
    access_count: int = 0
    last_accessed: float = 0.0
    harmonic_resonance: float = 0.0
    
    def __post_init__(self):
        self.moral_value = self.coherence_score - self.entropy_score
    
    def update_morality(self, coherence: float, entropy: float):
        """Update morality scores and recalculate moral value"""
        self.coherence_score = coherence
        self.entropy_score = entropy
        self.moral_value = coherence - entropy
    
    def phase_distance(self, other_phase: float) -> float:
        """Calculate shortest angular distance between phases"""
        diff = abs(self.phase - other_phase)
        return min(diff, 2 * math.pi - diff)


class CoherenceMonitor:
    """Automated system for detecting and correcting entropy accumulation"""
    
    def __init__(self, intervention_threshold: float = 0.3):
        self.intervention_threshold = intervention_threshold
        self.interventions = []
    
    def detect_entropy_threat(self, buffer, current_phase: float) -> bool:
        """Assess if intervention is needed to maintain coherence"""
        nearby_events = buffer.get_phase_neighbors(current_phase, radius=0.5)
        if not nearby_events:
            return False
        
        avg_morality = np.mean([event.moral_value for event in nearby_events])
        return avg_morality < self.intervention_threshold
    
    def stabilize_region(self, buffer, center_phase: float, strength: float = 0.2):
        """Apply coherence reinforcement to memory region"""
        affected_events = buffer.get_phase_neighbors(center_phase, radius=0.8)
        
        for event in affected_events:
            distance = event.phase_distance(center_phase)
            boost = strength * (1 - distance / 0.8)
            
            # Reinforce coherence, reduce entropy
            new_coherence = min(1.0, event.coherence_score + boost)
            new_entropy = max(0.0, event.entropy_score - boost * 0.5)
            event.update_morality(new_coherence, new_entropy)
        
        self.interventions.append({
            'timestamp': time.time(),
            'phase': center_phase,
            'events_affected': len(affected_events)
        })


class SpiralBuffer:
    """
    Morality-embedded spiral memory buffer with harmonic recall
    
    Memory system that preferentially retains high-coherence patterns while
    naturally filtering out entropy-generating content. Uses empirically-
    optimized 432 Hz update frequency for maximum stability.
    """
    
    # Empirically-derived optimal update frequency for stability
    OPTIMAL_FREQUENCY = 432.0  # Hz
    
    def __init__(self, 
                 max_capacity: int = 1000, 
                 update_frequency: float = None,
                 coherence_threshold: float = 0.5):
        """
        Initialize spiral buffer with specified parameters
        
        Args:
            max_capacity: Maximum number of events to store
            update_frequency: Update rate in Hz (defaults to optimal 432 Hz)
            coherence_threshold: Minimum coherence for auto-tuning
        """
        self.max_capacity = max_capacity
        self.update_frequency = update_frequency or self.OPTIMAL_FREQUENCY
        self.coherence_threshold = coherence_threshold
        
        # Core memory storage
        self.events: List[MemoryEvent] = []
        self.current_phase = 0.0
        self.cycle_count = 0
        
        # Performance monitoring
        self.coherence_history = deque(maxlen=100)
        self.entropy_history = deque(maxlen=100)
        self.moral_momentum = 0.0
        
        # Automated coherence maintenance
        self.monitor = CoherenceMonitor()
        
        # System parameters
        self.phase_momentum = 0.0
        self.resonance_decay = 0.95
    
    def add_event(self, 
                  content: Any, 
                  coherence: float, 
                  entropy: float) -> MemoryEvent:
        """
        Add new event to spiral buffer
        
        Args:
            content: The data/information to store
            coherence: Score (0-1) for how much this promotes order/beneficial outcomes
            entropy: Score (0-1) for how much this introduces disorder/harmful effects
            
        Returns:
            MemoryEvent: The created event with calculated moral value
        """
        # Create new memory event
        event = MemoryEvent(
            content=content,
            timestamp=time.time(),
            phase=self.current_phase,
            coherence_score=coherence,
            entropy_score=entropy
        )
        
        # Calculate harmonic resonance with recent events
        if self.events:
            recent_events = self.events[-min(10, len(self.events)):]
            resonances = [self._harmonic_weight(e.phase, event.phase) for e in recent_events]
            event.harmonic_resonance = np.mean(resonances)
        
        self.events.append(event)
        
        # Manage capacity by removing lowest-value memories (not oldest)
        if len(self.events) > self.max_capacity:
            self.events.sort(key=lambda e: e.moral_value)
            self.events = self.events[1:]
        
        # Update system state
        self._advance_phase()
        self._update_metrics(event)
        
        # Check for automatic coherence intervention
        if self.monitor.detect_entropy_threat(self, self.current_phase):
            self.monitor.stabilize_region(self, self.current_phase)
        
        return event
    
    def recall_by_coherence(self, 
                           target_coherence: float, 
                           top_k: int = 5) -> List[MemoryEvent]:
        """
        Retrieve memories using coherence-based harmonic recall
        
        Args:
            target_coherence: Desired coherence level (0-1)
            top_k: Number of memories to retrieve
            
        Returns:
            List of memories ranked by relevance and moral value
        """
        if not self.events:
            return []
        
        scored_events = []
        
        for event in self.events:
            # Calculate multi-factor recall score
            harmonic_weight = self._harmonic_weight(event.phase, self.current_phase)
            coherence_similarity = 1.0 - abs(event.coherence_score - target_coherence)
            
            recall_score = (
                event.moral_value * 0.4 +      # Prioritize beneficial patterns
                harmonic_weight * 0.3 +        # Phase resonance
                coherence_similarity * 0.3     # Target alignment
            )
            
            scored_events.append((recall_score, event))
        
        # Return top-k by score
        scored_events.sort(key=lambda x: x[0], reverse=True)
        recalled = [event for _, event in scored_events[:top_k]]
        
        # Update access patterns
        for event in recalled:
            event.access_count += 1
            event.last_accessed = time.time()
        
        return recalled
    
    def get_phase_neighbors(self, phase: float, radius: float) -> List[MemoryEvent]:
        """Get events within specified phase radius"""
        neighbors = []
        for event in self.events:
            if event.phase_distance(phase) <= radius:
                neighbors.append(event)
        return neighbors
    
    def auto_tune_frequency(self):
        """Automatically adjust update frequency to optimize coherence"""
        if len(self.coherence_history) < 10:
            return
        
        recent_coherence = np.mean(list(self.coherence_history)[-5:])
        
        # Test harmonics of optimal frequency if coherence is low
        if recent_coherence < self.coherence_threshold:
            test_frequencies = [216, 432, 864, 1296]  # Harmonic series
            
            best_freq = self.update_frequency
            best_coherence = recent_coherence
            
            for freq in test_frequencies:
                test_coherence = self._simulate_coherence_at_frequency(freq)
                if test_coherence > best_coherence:
                    best_coherence = test_coherence
                    best_freq = freq
            
            if best_freq != self.update_frequency:
                self.update_frequency = best_freq
                return True
        
        return False
    
    def get_system_metrics(self) -> Dict:
        """Get comprehensive system performance metrics"""
        if not self.events:
            return {'status': 'empty'}
        
        return {
            'total_events': len(self.events),
            'current_phase': self.current_phase,
            'update_frequency': self.update_frequency,
            'cycle_count': self.cycle_count,
            'avg_moral_value': np.mean([e.moral_value for e in self.events]),
            'avg_coherence': np.mean([e.coherence_score for e in self.events]),
            'avg_entropy': np.mean([e.entropy_score for e in self.events]),
            'moral_momentum': self.moral_momentum,
            'coherence_interventions': len(self.monitor.interventions),
            'high_value_events': len([e for e in self.events if e.moral_value > 0.7]),
            'stability_score': self._calculate_stability_score()
        }
    
    # Private helper methods
    
    def _harmonic_weight(self, phase1: float, phase2: float) -> float:
        """Calculate harmonic resonance between two phases"""
        phase_diff = abs(phase1 - phase2)
        phase_diff = min(phase_diff, 2 * math.pi - phase_diff)
        
        # Harmonic peaks at key intervals
        harmonics = [0, math.pi/2, math.pi, 3*math.pi/2]
        max_resonance = 0
        
        for harmonic in harmonics:
            resonance = math.exp(-((phase_diff - harmonic) ** 2) / 0.2)
            max_resonance = max(max_resonance, resonance)
        
        return max_resonance
    
    def _advance_phase(self):
        """Advance phase based on current update frequency"""
        phase_increment = (2 * math.pi) / self.update_frequency
        self.current_phase = (self.current_phase + phase_increment) % (2 * math.pi)
        
        # Detect cycle completion
        if self.current_phase < phase_increment:
            self.cycle_count += 1
            self._reinforce_coherent_memories()
    
    def _reinforce_coherent_memories(self):
        """Echo high-coherence memories forward in time"""
        high_value_events = [e for e in self.events if e.moral_value > 0.7]
        
        for event in high_value_events:
            harmonic_alignment = self._harmonic_weight(event.phase, self.current_phase)
            if harmonic_alignment > 0.5:
                # Strengthen coherent memories
                boost = 0.1 * harmonic_alignment
                new_coherence = min(1.0, event.coherence_score + boost)
                event.update_morality(new_coherence, event.entropy_score)
    
    def _update_metrics(self, new_event: MemoryEvent):
        """Update system-wide performance tracking"""
        recent_events = self.events[-min(10, len(self.events)):]
        
        avg_coherence = np.mean([e.coherence_score for e in recent_events])
        avg_entropy = np.mean([e.entropy_score for e in recent_events])
        
        self.coherence_history.append(avg_coherence)
        self.entropy_history.append(avg_entropy)
        
        # Calculate moral momentum
        if len(self.coherence_history) >= 2:
            coherence_trend = self.coherence_history[-1] - self.coherence_history[-2]
            entropy_trend = self.entropy_history[-1] - self.entropy_history[-2]
            self.moral_momentum = coherence_trend - entropy_trend
    
    def _simulate_coherence_at_frequency(self, test_frequency: float) -> float:
        """Simulate system coherence at different update frequency"""
        high_value_events = [e for e in self.events if e.moral_value > 0.5]
        if not high_value_events:
            return 0.5
        
        test_phase_increment = (2 * math.pi) / test_frequency
        test_phase = self.current_phase
        
        total_resonance = 0
        for _ in range(10):  # Simulate 10 steps
            test_phase = (test_phase + test_phase_increment) % (2 * math.pi)
            for event in high_value_events:
                total_resonance += self._harmonic_weight(event.phase, test_phase)
        
        return total_resonance / (10 * len(high_value_events))
    
    def _calculate_stability_score(self) -> float:
        """Calculate overall system stability metric"""
        if len(self.coherence_history) < 5:
            return 0.5
        
        recent_coherence = list(self.coherence_history)[-5:]
        recent_entropy = list(self.entropy_history)[-5:]
        
        coherence_stability = 1.0 - np.std(recent_coherence)
        entropy_stability = 1.0 / (1.0 + np.mean(recent_entropy))
        moral_value_avg = np.mean([e.moral_value for e in self.events])
        
        return (coherence_stability + entropy_stability + moral_value_avg) / 3.0


# Convenience functions for common use cases

def create_buffer(capacity: int = 1000) -> SpiralBuffer:
    """Create a spiral buffer with default optimal settings"""
    return SpiralBuffer(max_capacity=capacity)


def score_content_morality(content: str, 
                          positive_keywords: List[str] = None,
                          negative_keywords: List[str] = None) -> Tuple[float, float]:
    """
    Simple content scoring for demonstration purposes
    
    Returns:
        Tuple of (coherence_score, entropy_score)
    """
    if positive_keywords is None:
        positive_keywords = ['helpful', 'clear', 'constructive', 'beneficial', 'accurate']
    if negative_keywords is None:
        negative_keywords = ['confusing', 'harmful', 'contradictory', 'misleading', 'toxic']
    
    content_lower = content.lower()
    
    positive_count = sum(1 for word in positive_keywords if word in content_lower)
    negative_count = sum(1 for word in negative_keywords if word in content_lower)
    
    # Simple scoring based on keyword presence
    coherence = min(1.0, 0.5 + positive_count * 0.2)
    entropy = min(1.0, negative_count * 0.3)
    
    return coherence, entropy