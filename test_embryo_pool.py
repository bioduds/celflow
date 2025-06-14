#!/usr/bin/env python3
"""
Test script for SelFlow Embryo Pool

Simple test to verify that the embryo pool can be created,
embryos can detect patterns, and the system works as expected.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.embryo_pool import EmbryoPool


async def test_embryo_pool():
    """Test the embryo pool functionality"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger('test')
    logger.info("Starting SelFlow Embryo Pool Test...")
    
    # Configuration
    config = {
        'max_concurrent': 5,  # Smaller pool for testing
        'min_survival_threshold': 0.1,
        'embryo_config': {
            'data_buffer_limit_mb': 1  # Smaller buffer for faster testing
        },
        'privacy': {
            'filter_passwords': True,
            'filter_credit_cards': True,
            'filter_personal_info': False  # Allow more data for testing
        }
    }
    
    try:
        # Create and initialize embryo pool
        logger.info("Creating embryo pool...")
        pool = EmbryoPool(config)
        await pool.initialize()
        
        # Test feeding data
        logger.info("Feeding test events to embryos...")
        
        test_events = [
            {
                'type': 'app_launch',
                'app_name': 'VSCode',
                'timestamp': time.time(),
                'window_title': 'Visual Studio Code'
            },
            {
                'type': 'file_create',
                'file_path': '/Users/user/code/test.py',
                'timestamp': time.time(),
                'text_content': 'def hello_world():\n    print("Hello, World!")'
            },
            {
                'type': 'web_navigate',
                'app_name': 'Safari',
                'timestamp': time.time(),
                'window_title': 'GitHub - Neural Networks',
                'text_content': 'machine learning artificial intelligence'
            },
            {
                'type': 'code_edit',
                'file_path': '/Users/user/project/main.py',
                'timestamp': time.time(),
                'text_content': 'import torch\nimport numpy as np\n\nclass NeuralNet:'
            },
            {
                'type': 'app_switch',
                'app_name': 'Terminal',
                'timestamp': time.time(),
                'window_title': 'Terminal - bash',
                'text_content': 'git commit -m "Add neural network implementation"'
            }
        ]
        
        # Feed events multiple times to build up patterns
        for round_num in range(10):
            logger.info(f"Event feeding round {round_num + 1}/10")
            
            for event in test_events:
                event['timestamp'] = time.time()  # Update timestamp
                patterns = await pool.feed_data(event)
                
                if patterns:
                    logger.info(f"Patterns detected: {len(patterns)}")
                    for pattern in patterns:
                        logger.info(f"  - {pattern.get('type')} (confidence: {pattern.get('confidence', 0):.2f})")
                        
            # Check pool status
            status = pool.get_pool_status()
            logger.info(f"Pool status: {status['active_embryos']} active embryos, "
                       f"{status['pool_stats']['patterns_detected']} total patterns")
            
            # Check for birth-ready embryos
            birth_ready = await pool.get_birth_ready_embryo()
            if birth_ready:
                logger.info(f"🎉 Embryo {birth_ready.embryo_id} is ready for agent birth!")
                birth_data = birth_ready.prepare_birth_data()
                logger.info(f"  Specialization: {birth_data['dominant_specialization']}")
                logger.info(f"  Patterns detected: {birth_data['patterns_detected']}")
                logger.info(f"  Fitness score: {birth_data['fitness_score']:.3f}")
                birth_ready.birth_ready = False  # Reset for continued testing
                
            await asyncio.sleep(0.5)  # Small delay between rounds
            
        # Final status
        final_status = pool.get_pool_status()
        logger.info("\n=== FINAL TEST RESULTS ===")
        logger.info(f"Active embryos: {final_status['active_embryos']}")
        logger.info(f"Total patterns detected: {final_status['pool_stats']['patterns_detected']}")
        logger.info(f"Events processed: {final_status['pool_stats']['events_processed']}")
        logger.info(f"Birth queue size: {final_status['birth_queue_size']}")
        logger.info(f"Generation: {final_status['generation']}")
        logger.info(f"Specializations: {final_status['top_specializations']}")
        
        logger.info("\n✅ Embryo Pool Test Completed Successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        

if __name__ == '__main__':
    asyncio.run(test_embryo_pool()) 