#!/usr/bin/env python3
"""
SelFlow Embryo Pool

Manages a pool of agent embryos that compete to detect patterns in user data.
Each embryo is a minimal neural network that specializes in different pattern types.
When an embryo fills its data buffer, it triggers agent birth.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json
import uuid
from pathlib import Path

import torch
import torch.nn as nn
import numpy as np
from datetime import datetime, timedelta

from app.core.pattern_detector import PatternDetector
from app.privacy.content_filter import ContentFilter


@dataclass
class EmbryoStats:
    """Statistics for tracking embryo performance"""
    creation_time: datetime
    patterns_detected: int
    specialization_scores: Dict[str, float]
    data_buffer_size_mb: float
    last_activity: datetime
    fitness_score: float


class AgentEmbryo:
    """
    A minimal AI embryo that detects patterns and competes for specialization.
    Each embryo has a small neural network and data buffer.
    """
    
    def __init__(self, embryo_id: str, config: dict):
        self.embryo_id = embryo_id
        self.config = config
        self.logger = logging.getLogger(f'Embryo-{embryo_id[:8]}')
        
        # Neural pattern detector (1M parameters)
        self.pattern_detector = PatternDetector(
            input_dim=512,
            hidden_dim=256,
            output_dim=128,
            max_params=1_000_000
        )
        
        # Data management
        self.data_buffer = []
        self.data_buffer_size_mb = 0.0
        self.data_limit_mb = config.get('data_buffer_limit_mb', 16)
        
        # Specialization tracking
        self.specialization_scores = {
            'file_operations': 0.0,
            'app_launches': 0.0,
            'communication': 0.0,
            'creative_work': 0.0,
            'development': 0.0,
            'web_browsing': 0.0,
            'system_maintenance': 0.0,
            'temporal_patterns': 0.0
        }
        
        # Performance metrics
        self.stats = EmbryoStats(
            creation_time=datetime.now(),
            patterns_detected=0,
            specialization_scores=self.specialization_scores.copy(),
            data_buffer_size_mb=0.0,
            last_activity=datetime.now(),
            fitness_score=0.0
        )
        
        # Competition state
        self.is_active = True
        self.birth_ready = False
        
    async def observe(self, data_event: dict) -> Optional[dict]:
        """
        Process a system event and detect patterns.
        Returns pattern info if detected, None otherwise.
        """
        if not self.is_active:
            return None
            
        try:
            # Filter and process the data
            processed_event = await self._preprocess_event(data_event)
            if not processed_event:
                return None
                
            # Detect patterns using neural network
            pattern_info = await self.pattern_detector.analyze(processed_event)
            
            if pattern_info and pattern_info['confidence'] > 0.3:
                # Add to data buffer
                await self._add_to_buffer(processed_event, pattern_info)
                
                # Update specialization scores
                await self._update_specialization(pattern_info)
                
                # Update stats
                self.stats.patterns_detected += 1
                self.stats.last_activity = datetime.now()
                
                # Check if ready for birth
                if self.data_buffer_size_mb >= self.data_limit_mb:
                    self.birth_ready = True
                    self.logger.info(
                        f"Embryo {self.embryo_id} ready for birth! "
                        f"Buffer: {self.data_buffer_size_mb:.1f}MB, "
                        f"Patterns: {self.stats.patterns_detected}"
                    )
                
                return pattern_info
                
        except Exception as e:
            self.logger.error(f"Error in observe: {e}")
            
        return None
        
    async def _preprocess_event(self, data_event: dict) -> Optional[dict]:
        """Preprocess and validate system event data"""
        try:
            # Basic validation
            if not data_event or 'type' not in data_event:
                return None
                
            # Add timestamp if missing
            if 'timestamp' not in data_event:
                data_event['timestamp'] = time.time()
                
            # Add embryo context
            processed = {
                'embryo_id': self.embryo_id,
                'original_event': data_event,
                'processing_time': time.time()
            }
            
            return processed
            
        except Exception as e:
            self.logger.error(f"Error preprocessing event: {e}")
            return None
            
    async def _add_to_buffer(self, event: dict, pattern: dict):
        """Add event and pattern to data buffer"""
        try:
            buffer_entry = {
                'timestamp': time.time(),
                'event': event,
                'pattern': pattern,
                'embryo_id': self.embryo_id
            }
            
            self.data_buffer.append(buffer_entry)
            
            # Estimate size (rough calculation)
            entry_size = len(json.dumps(buffer_entry)) / (1024 * 1024)
            self.data_buffer_size_mb += entry_size
            self.stats.data_buffer_size_mb = self.data_buffer_size_mb
            
            # Limit buffer size to prevent memory issues
            max_entries = 10000
            if len(self.data_buffer) > max_entries:
                removed = self.data_buffer.pop(0)
                removed_size = len(json.dumps(removed)) / (1024 * 1024)
                self.data_buffer_size_mb -= removed_size
                
        except Exception as e:
            self.logger.error(f"Error adding to buffer: {e}")
            
    async def _update_specialization(self, pattern_info: dict):
        """Update specialization scores based on detected patterns"""
        try:
            pattern_type = pattern_info.get('type', 'unknown')
            confidence = pattern_info.get('confidence', 0.0)
            
            # Map pattern types to specialization categories
            type_mapping = {
                'file_create': 'file_operations',
                'file_move': 'file_operations',
                'file_delete': 'file_operations',
                'app_launch': 'app_launches',
                'app_switch': 'app_launches',
                'email_open': 'communication',
                'calendar_event': 'communication',
                'code_edit': 'development',
                'git_commit': 'development',
                'web_navigate': 'web_browsing',
                'web_search': 'web_browsing',
                'design_work': 'creative_work',
                'media_edit': 'creative_work',
                'system_setting': 'system_maintenance',
                'routine_behavior': 'temporal_patterns'
            }
            
            category = type_mapping.get(pattern_type, 'system_maintenance')
            
            # Update score with exponential moving average
            alpha = 0.1  # Learning rate
            current_score = self.specialization_scores[category]
            self.specialization_scores[category] = (
                alpha * confidence + (1 - alpha) * current_score
            )
            
            # Update stats
            self.stats.specialization_scores = self.specialization_scores.copy()
            
        except Exception as e:
            self.logger.error(f"Error updating specialization: {e}")
            
    def calculate_fitness(self) -> float:
        """Calculate overall fitness score for natural selection"""
        try:
            # Base fitness on pattern detection capability
            detection_score = min(self.stats.patterns_detected / 100.0, 1.0)
            
            # Specialization bonus (reward for finding a niche)
            max_specialization = max(self.specialization_scores.values())
            specialization_bonus = max_specialization * 0.5
            
            # Activity penalty (inactive embryos lose fitness)
            hours_inactive = (datetime.now() - self.stats.last_activity).seconds / 3600
            activity_penalty = min(hours_inactive * 0.1, 0.8)
            
            # Data collection efficiency
            if self.data_buffer_size_mb > 0:
                efficiency = self.stats.patterns_detected / self.data_buffer_size_mb
                efficiency_bonus = min(efficiency / 10.0, 0.3)
            else:
                efficiency_bonus = 0.0
                
            # Calculate final fitness
            fitness = (
                detection_score + 
                specialization_bonus + 
                efficiency_bonus - 
                activity_penalty
            )
            
            self.stats.fitness_score = max(0.0, fitness)
            return self.stats.fitness_score
            
        except Exception as e:
            self.logger.error(f"Error calculating fitness: {e}")
            return 0.0
            
    def get_dominant_specialization(self) -> Tuple[str, float]:
        """Get the embryo's strongest specialization"""
        max_category = max(
            self.specialization_scores.items(),
            key=lambda x: x[1]
        )
        return max_category
        
    def prepare_birth_data(self) -> dict:
        """Prepare data for agent creation"""
        dominant_spec, spec_score = self.get_dominant_specialization()
        
        return {
            'embryo_id': self.embryo_id,
            'creation_time': self.stats.creation_time.isoformat(),
            'data_buffer': self.data_buffer,
            'specialization_scores': self.specialization_scores,
            'dominant_specialization': dominant_spec,
            'specialization_strength': spec_score,
            'patterns_detected': self.stats.patterns_detected,
            'fitness_score': self.stats.fitness_score,
            'neural_weights': self.pattern_detector.get_weights()
        }


class EmbryoPool:
    """
    Manages a pool of competing agent embryos.
    Handles natural selection, resource allocation, and agent birth triggers.
    """

    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger('EmbryoPool')

        # Pool configuration
        self.max_embryos = config.get('max_concurrent', 15)
        self.min_survival_threshold = config.get('min_survival_threshold', 0.3)

        # Embryo management
        self.embryos: Dict[str, AgentEmbryo] = {}
        self.birth_queue: List[str] = []

        # Competition metrics
        self.generation = 0
        self.total_births = 0
        self.culling_stats = {
            'total_culled': 0,
            'reasons': {'low_fitness': 0, 'inactivity': 0, 'redundancy': 0}
        }

        # Content filtering
        self.content_filter = ContentFilter(config.get('privacy', {}))

        # Performance tracking
        self.pool_stats = {
            'events_processed': 0,
            'patterns_detected': 0,
            'avg_fitness': 0.0,
            'active_embryos': 0
        }

    async def start(self):
        """Start the embryo pool system"""
        self.logger.info("🧬 Starting Embryo Pool...")
        await self.initialize()
        self.logger.info("✅ Embryo Pool started successfully")

    async def stop(self):
        """Stop the embryo pool system"""
        self.logger.info("🛑 Stopping Embryo Pool...")
        # In a full implementation, would properly shutdown background tasks
        self.logger.info("✅ Embryo Pool stopped")

    async def initialize(self):
        """Initialize the embryo pool with initial embryos"""
        self.logger.info("Initializing embryo pool...")

        try:
            # Create initial embryos
            for i in range(self.max_embryos):
                embryo_id = str(uuid.uuid4())
                embryo = AgentEmbryo(embryo_id, self.config.get('embryo_config', {}))
                self.embryos[embryo_id] = embryo

            self.logger.info(f"Created {len(self.embryos)} initial embryos")

            # Start background tasks
            asyncio.create_task(self._natural_selection_loop())
            asyncio.create_task(self._stats_update_loop())

        except Exception as e:
            self.logger.error(f"Error initializing embryo pool: {e}")
            raise

    async def feed_data(self, data_event: dict) -> List[dict]:
        """
        Feed system event data to all active embryos.
        Returns list of detected patterns.
        """
        patterns = []

        try:
            # Filter sensitive content
            filtered_event = await self.content_filter.filter_event(data_event)
            if not filtered_event:
                return patterns

            # Feed to all active embryos
            tasks = []
            for embryo in self.embryos.values():
                if embryo.is_active:
                    tasks.append(embryo.observe(filtered_event))

            # Collect results
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, dict):
                    patterns.append(result)
                elif isinstance(result, Exception):
                    self.logger.warning(f"Embryo observation error: {result}")

            # Update pool stats
            self.pool_stats['events_processed'] += 1
            self.pool_stats['patterns_detected'] += len(patterns)

            # Check for birth-ready embryos
            await self._check_birth_readiness()

        except Exception as e:
            self.logger.error(f"Error feeding data to embryos: {e}")

        return patterns

    async def _check_birth_readiness(self):
        """Check if any embryos are ready for agent birth"""
        for embryo_id, embryo in self.embryos.items():
            if embryo.birth_ready and embryo_id not in self.birth_queue:
                self.birth_queue.append(embryo_id)
                self.logger.info(f"Embryo {embryo_id} added to birth queue")

    async def get_birth_ready_embryo(self) -> Optional[AgentEmbryo]:
        """Get next embryo ready for agent birth"""
        if not self.birth_queue:
            return None

        embryo_id = self.birth_queue.pop(0)
        embryo = self.embryos.get(embryo_id)

        if embryo and embryo.birth_ready:
            return embryo

        return None

    async def _natural_selection_loop(self):
        """Background task for natural selection and culling"""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                await self._perform_natural_selection()

            except Exception as e:
                self.logger.error(f"Error in natural selection: {e}")

    async def _perform_natural_selection(self):
        """Perform natural selection on embryo pool"""
        self.logger.info("Performing natural selection...")

        try:
            # Calculate fitness for all embryos
            fitness_scores = {}
            for embryo_id, embryo in self.embryos.items():
                fitness_scores[embryo_id] = embryo.calculate_fitness()

            # Identify weak embryos for culling
            weak_embryos = [
                embryo_id for embryo_id, fitness in fitness_scores.items()
                if fitness < self.min_survival_threshold
            ]

            # Cull weak embryos (but keep minimum viable population)
            min_population = max(5, self.max_embryos // 3)
            active_count = len([e for e in self.embryos.values() if e.is_active])

            if active_count > min_population:
                culled_count = 0
                for embryo_id in weak_embryos:
                    if active_count - culled_count > min_population:
                        await self._cull_embryo(embryo_id, 'low_fitness')
                        culled_count += 1

            # Create new embryos to replace culled ones
            await self._spawn_new_embryos()

            # Update generation
            self.generation += 1

            self.logger.info(
                f"Natural selection complete. Generation: {self.generation}, "
                f"Active embryos: {len([e for e in self.embryos.values() if e.is_active])}"
            )

        except Exception as e:
            self.logger.error(f"Error in natural selection: {e}")

    async def _cull_embryo(self, embryo_id: str, reason: str):
        """Remove an embryo from the active pool"""
        if embryo_id in self.embryos:
            embryo = self.embryos[embryo_id]
            embryo.is_active = False

            self.culling_stats['total_culled'] += 1
            self.culling_stats['reasons'][reason] += 1

            self.logger.info(f"Culled embryo {embryo_id} - Reason: {reason}")

    async def _spawn_new_embryos(self):
        """Create new embryos to maintain pool size"""
        active_count = len([e for e in self.embryos.values() if e.is_active])

        while active_count < self.max_embryos:
            embryo_id = str(uuid.uuid4())
            embryo = AgentEmbryo(embryo_id, self.config.get('embryo_config', {}))
            self.embryos[embryo_id] = embryo
            active_count += 1

            self.logger.info(f"Spawned new embryo {embryo_id}")

    async def _stats_update_loop(self):
        """Background task for updating pool statistics"""
        while True:
            try:
                await asyncio.sleep(300)  # Update every 5 minutes
                await self._update_pool_stats()

            except Exception as e:
                self.logger.error(f"Error updating stats: {e}")

    async def _update_pool_stats(self):
        """Update pool-wide statistics"""
        active_embryos = [e for e in self.embryos.values() if e.is_active]

        if active_embryos:
            avg_fitness = sum(e.calculate_fitness() for e in active_embryos) / len(active_embryos)
            self.pool_stats['avg_fitness'] = avg_fitness

        self.pool_stats['active_embryos'] = len(active_embryos)

    def get_pool_status(self) -> dict:
        """Get current pool status for monitoring"""
        active_embryos = [e for e in self.embryos.values() if e.is_active]

        # Prepare embryo data for agent manager
        embryo_data_list = []
        for embryo in active_embryos:
            dominant_spec, spec_strength = embryo.get_dominant_specialization()
            embryo_data_list.append(
                {
                    "embryo_id": embryo.embryo_id,
                    "patterns_detected": embryo.stats.patterns_detected,
                    "fitness_score": embryo.calculate_fitness(),
                    "specialization_scores": embryo.specialization_scores.copy(),
                    "dominant_specialization": dominant_spec,
                    "specialization_strength": spec_strength,
                    "creation_time": embryo.stats.creation_time.isoformat(),
                    "birth_ready": embryo.birth_ready,
                }
            )

        return {
            "total_embryos": len(self.embryos),
            "active_embryos": len(active_embryos),
            "birth_queue_size": len(self.birth_queue),
            "generation": self.generation,
            "total_births": self.total_births,
            "events_processed": self.pool_stats["events_processed"],
            "pool_stats": self.pool_stats,
            "culling_stats": self.culling_stats,
            "top_specializations": self._get_top_specializations(),
            "embryos": embryo_data_list,  # For agent manager
        }

    def _get_top_specializations(self) -> Dict[str, int]:
        """Get count of embryos by their dominant specialization"""
        specializations = {}

        for embryo in self.embryos.values():
            if embryo.is_active:
                dominant, _ = embryo.get_dominant_specialization()
                specializations[dominant] = specializations.get(dominant, 0) + 1

        return specializations

    async def process_event(self, event: dict) -> List[dict]:
        """Process a system event (alias for feed_data for compatibility)"""
        return await self.feed_data(event)

    def process_event_sync(self, event: dict) -> List[dict]:
        """Synchronous wrapper for process_event for high-performance capture"""
        try:
            # Create a new event loop if none exists, or schedule in existing loop
            try:
                loop = asyncio.get_running_loop()
                # If we're in an async context, schedule the coroutine
                future = asyncio.ensure_future(self.feed_data(event))
                # Don't wait for it to complete to avoid blocking
                return []
            except RuntimeError:
                # No running loop, create one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(self.feed_data(event))
                finally:
                    loop.close()
        except Exception as e:
            self.logger.error(f"Error in sync event processing: {e}")
            return []

    async def remove_embryo(self, embryo_id: str):
        """Remove an embryo from the pool"""
        if embryo_id in self.embryos:
            await self._cull_embryo(embryo_id, "agent_birth")
            self.logger.info(f"Embryo {embryo_id} removed - agent born")
