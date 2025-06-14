#!/usr/bin/env python3
"""
SelFlow Clustering Analysis Tool

Test the intelligent clustering system with your real event data.
Analyzes your 60K+ events to discover behavioral patterns.
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from app.intelligence.event_clustering import create_intelligent_clustering
    from app.system.event_persistence import EventDatabase

    CLUSTERING_AVAILABLE = True
except ImportError as e:
    print(f"❌ Clustering system not available: {e}")
    print("Install dependencies: pip install -r requirements-clustering.txt")
    CLUSTERING_AVAILABLE = False
    sys.exit(1)


async def load_recent_events(db_path: str, limit: int = 5000) -> list:
    """Load recent events from the database for analysis"""
    print(f"📊 Loading {limit} recent events from database...")

    try:
        db = EventDatabase(db_path)
        events = db.get_events(limit=limit)

        print(f"✅ Loaded {len(events)} events")
        return events

    except Exception as e:
        print(f"❌ Error loading events: {e}")
        return []


async def analyze_clustering_performance():
    """Comprehensive clustering performance analysis"""
    print("🧠 SelFlow Intelligent Clustering Analysis")
    print("=" * 50)

    # Configuration optimized for your data characteristics
    config = {
        "min_events_for_analysis": 100,  # Lower for testing
        "analysis_interval": 60,
        "pattern_memory_size": 1000,
    }

    # Create clustering system
    clustering_system = create_intelligent_clustering(config)

    # Load your real event data
    db_path = "data/events.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        print("Run the system first to generate event data")
        return

    # Test with different data sizes
    test_sizes = [500, 1000, 2000, 5000]

    for size in test_sizes:
        print(f"\n🔍 Testing with {size} events...")

        # Load events
        events = await load_recent_events(db_path, size)
        if not events:
            continue

        # Convert to expected format
        formatted_events = []
        for event in events:
            formatted_event = {
                "type": event["event_type"],
                "action": event.get("action", "unknown"),
                "ts": event["timestamp"],
                "src": event["source"],
            }

            # Add event-specific data
            data = event["data"]
            if event["event_type"] == "file_op":
                formatted_event.update(
                    {
                        "path": data.get("path", ""),
                        "name": data.get("name", ""),
                        "ext": data.get("ext", ""),
                        "dir": data.get("dir", ""),
                    }
                )
            elif event["event_type"] == "app":
                formatted_event["app"] = data.get("app", "")

            formatted_events.append(formatted_event)

        # Run clustering analysis
        start_time = time.time()
        analysis_result = await clustering_system.analyze_events(formatted_events)
        analysis_time = time.time() - start_time

        if analysis_result:
            # Display results
            print(f"  ✨ Analysis completed in {analysis_time:.2f}s")
            print(f"  📈 Method used: {analysis_result['method_used']}")
            print(f"  🎯 Patterns discovered: {analysis_result['n_clusters']}")
            print(f"  🔇 Noise events: {analysis_result['n_noise']}")

            # Show metrics
            metrics = analysis_result.get("metrics", {})
            if metrics:
                print(
                    f"  📊 Silhouette score: {metrics.get('silhouette_score', 0):.3f}"
                )
                print(
                    f"  📊 Calinski-Harabasz: {metrics.get('calinski_harabasz_score', 0):.1f}"
                )

            # Show insights
            insights = analysis_result.get("insights", [])
            if insights:
                print("  💡 Key insights:")
                for insight in insights[:3]:
                    print(f"    • {insight}")

            # Show top patterns
            patterns = analysis_result.get("patterns", {})
            if patterns:
                print("  🔍 Top patterns:")
                for i, (pattern_id, pattern) in enumerate(list(patterns.items())[:3]):
                    print(f"    {i+1}. {pattern.get('description', 'No description')}")
                    print(f"       Size: {pattern.get('size', 0)} events")
                    print(
                        f"       Intensity: {pattern.get('intensity', 0):.1f} events/min"
                    )
        else:
            print(f"  ❌ Analysis failed")

    # Final statistics
    stats = clustering_system.get_statistics()
    print(f"\n📈 Final Statistics:")
    print(f"  Total analyses: {stats['analyses_performed']}")
    print(f"  Events analyzed: {stats['total_events_analyzed']}")
    print(f"  Avg events/analysis: {stats['avg_events_per_analysis']:.0f}")


async def demonstrate_clustering_methods():
    """Demonstrate different clustering methods on your data"""
    print("\n🎯 Clustering Method Comparison")
    print("=" * 40)

    # Load sample data
    db_path = "data/events.db"
    events = await load_recent_events(db_path, 1000)

    if not events:
        print("❌ No events available for demonstration")
        return

    # Format events
    formatted_events = []
    for event in events:
        formatted_event = {
            "type": event["event_type"],
            "action": event.get("action", "unknown"),
            "ts": event["timestamp"],
            "src": event["source"],
            "path": event["data"].get("path", ""),
            "ext": event["data"].get("ext", ""),
            "dir": event["data"].get("dir", ""),
        }
        formatted_events.append(formatted_event)

    print(f"📊 Analyzing {len(formatted_events)} events with different methods...")

    # Test each clustering method
    config = {"min_events_for_analysis": 100}
    clustering_system = create_intelligent_clustering(config)

    # Run analysis
    analysis_result = await clustering_system.analyze_events(formatted_events)

    if analysis_result:
        print(f"\n🏆 Best method: {analysis_result['method_used']}")
        print(f"🎯 Patterns found: {analysis_result['n_clusters']}")

        # Show method comparison
        all_metrics = clustering_system.clustering_engine.metrics
        print("\n📊 Method Comparison:")
        for method, metrics in all_metrics.items():
            print(f"  {method.upper()}:")
            print(f"    Clusters: {metrics['n_clusters']}")
            print(f"    Noise: {metrics['n_noise']}")
            print(f"    Silhouette: {metrics['silhouette_score']:.3f}")

    print("\n💡 Recommendations for your data:")
    print("  • HDBSCAN: Best for your varying density file operations")
    print("  • K-means: Good for high-level behavior categorization")
    print("  • DBSCAN: Excellent for detecting unusual activity patterns")


async def analyze_your_patterns():
    """Analyze patterns specific to your 60K+ event dataset"""
    print("\n🔬 Your Behavioral Pattern Analysis")
    print("=" * 40)

    db_path = "data/events.db"

    # Load larger sample to capture your patterns
    events = await load_recent_events(db_path, 3000)

    if not events:
        print("❌ No events available")
        return

    # Analyze event distribution (matching your overnight results)
    event_types = {}
    file_extensions = {}
    hourly_activity = {}

    for event in events:
        # Event type distribution
        event_type = event["event_type"]
        event_types[event_type] = event_types.get(event_type, 0) + 1

        # File extension analysis
        if event_type == "file_op":
            ext = event["data"].get("ext", "no_ext")
            file_extensions[ext] = file_extensions.get(ext, 0) + 1

        # Hourly activity
        import datetime

        hour = datetime.datetime.fromtimestamp(event["timestamp"]).hour
        hourly_activity[hour] = hourly_activity.get(hour, 0) + 1

    print(f"📊 Event Type Distribution (from {len(events)} events):")
    total_events = len(events)
    for event_type, count in sorted(
        event_types.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = (count / total_events) * 100
        print(f"  {event_type}: {count} ({percentage:.1f}%)")

    print(f"\n📁 Top File Extensions:")
    for ext, count in sorted(file_extensions.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]:
        print(f"  {ext}: {count}")

    print(f"\n⏰ Peak Activity Hours:")
    for hour, count in sorted(
        hourly_activity.items(), key=lambda x: x[1], reverse=True
    )[:5]:
        print(f"  {hour:02d}:00 - {count} events")

    # Run clustering on this data
    print(f"\n🧠 Running intelligent clustering...")

    # Format for clustering
    formatted_events = []
    for event in events:
        formatted_event = {
            "type": event["event_type"],
            "action": event.get("action", "unknown"),
            "ts": event["timestamp"],
            "src": event["source"],
            "path": event["data"].get("path", ""),
            "name": event["data"].get("name", ""),
            "ext": event["data"].get("ext", ""),
            "dir": event["data"].get("dir", ""),
        }
        formatted_events.append(formatted_event)

    config = {"min_events_for_analysis": 100}
    clustering_system = create_intelligent_clustering(config)

    analysis_result = await clustering_system.analyze_events(formatted_events)

    if analysis_result:
        print(f"✨ Discovered {analysis_result['n_clusters']} behavioral patterns")

        insights = analysis_result.get("insights", [])
        if insights:
            print("\n💡 Behavioral Insights:")
            for insight in insights:
                print(f"  • {insight}")

        patterns = analysis_result.get("patterns", {})
        if patterns:
            print(f"\n🔍 Pattern Details:")
            for pattern_id, pattern in list(patterns.items())[:3]:
                print(f"  Pattern {pattern['cluster_id']}:")
                print(f"    {pattern.get('description', 'No description')}")
                print(f"    Events: {pattern.get('size', 0)}")
                print(f"    Duration: {pattern.get('time_span_hours', 0):.1f}h")


async def main():
    """Main analysis function"""
    if not CLUSTERING_AVAILABLE:
        return

    print("🚀 SelFlow Intelligent Clustering Test Suite")
    print("=" * 50)

    try:
        # Run comprehensive analysis
        await analyze_clustering_performance()

        # Demonstrate different methods
        await demonstrate_clustering_methods()

        # Analyze your specific patterns
        await analyze_your_patterns()

        print("\n🎉 Analysis complete!")
        print("\n📋 Next Steps:")
        print(
            "  1. Install clustering dependencies: pip install -r requirements-clustering.txt"
        )
        print("  2. The system will automatically use clustering for smarter AI agents")
        print("  3. Monitor insights in the dashboard or logs")

    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
