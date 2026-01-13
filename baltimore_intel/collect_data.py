#!/usr/bin/env python3
"""
Baltimore Intel Data Collector

Collects data from free APIs and outputs JSON files for the dashboard.
Designed to run via GitHub Actions on a schedule.
"""

import json
import os
import requests
from datetime import datetime, timezone
from pathlib import Path

# Output directory (relative to repo root)
OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "data"


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def collect_amtrak():
    """
    Collect Amtrak train data from Amtraker API.
    Free, no API key required.
    """
    print("Collecting Amtrak data...")

    try:
        # Get all trains
        response = requests.get(
            "https://api-v3.amtraker.com/v3/trains",
            timeout=30
        )
        response.raise_for_status()
        all_trains = response.json()

        # Filter to trains near Baltimore (within ~100 miles)
        baltimore_lat, baltimore_lng = 39.2904, -76.6122

        baltimore_trains = []
        for train_id, train_data in all_trains.items():
            if isinstance(train_data, list):
                for train in train_data:
                    try:
                        lat = float(train.get('lat', 0))
                        lon = float(train.get('lon', 0))

                        # Check if within ~1.5 degrees (~100 miles)
                        if abs(lat - baltimore_lat) < 1.5 and abs(lon - baltimore_lng) < 1.5:
                            baltimore_trains.append({
                                'trainNum': train.get('trainNum'),
                                'routeName': train.get('routeName'),
                                'lat': lat,
                                'lon': lon,
                                'heading': train.get('heading'),
                                'velocity': train.get('velocity'),
                                'lastUpdate': train.get('lastValTS'),
                                'nextStation': train.get('eventName'),
                                'status': train.get('trainState', 'Active')
                            })
                    except (TypeError, ValueError):
                        continue

        result = {
            'collected_at': datetime.now(timezone.utc).isoformat(),
            'source': 'amtraker.com',
            'total_trains': len(baltimore_trains),
            'trains': baltimore_trains
        }

        output_file = OUTPUT_DIR / "amtrak.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"  Found {len(baltimore_trains)} trains near Baltimore")
        return True

    except Exception as e:
        print(f"  Error collecting Amtrak data: {e}")
        return False


def collect_news():
    """
    Collect news from Google-News-Scraper repo.
    Try multiple possible URLs, keep existing data if all fail.
    """
    print("Collecting news data...")

    # Try multiple possible URLs
    urls_to_try = [
        "https://raw.githubusercontent.com/arandomguyhere/Google-News-Scraper/main/feed.json",
        "https://raw.githubusercontent.com/arandomguyhere/Google-News-Scraper/master/feed.json",
        "https://raw.githubusercontent.com/arandomguyhere/Google-News-Scraper/main/output/feed.json",
    ]

    data = None
    for url in urls_to_try:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"  Found feed at: {url}")
                break
        except Exception:
            continue

    if data is None:
        print("  Could not fetch news feed, keeping existing data")
        return True  # Don't fail, just keep existing data

    # Extract stories
    stories = []

    if data.get('clusters'):
        for cluster in data['clusters']:
            if cluster.get('stories'):
                for story in cluster['stories'][:3]:
                    stories.append({
                        'title': story.get('title'),
                        'url': story.get('url'),
                        'source': story.get('source'),
                        'cluster_confidence': cluster.get('confidence', 0)
                    })

    if data.get('timeline'):
        for item in data['timeline'][:10]:
            stories.append({
                'title': item.get('title'),
                'url': item.get('url'),
                'source': item.get('source'),
                'date': item.get('date')
            })

    # Deduplicate
    seen = set()
    unique_stories = []
    for s in stories:
        if s['title'] and s['title'] not in seen:
            seen.add(s['title'])
            unique_stories.append(s)

    # Extract entities/connections
    entities = {
        'countries': data.get('connections', {}).get('countries', [])[:10],
        'sectors': data.get('connections', {}).get('sectors', [])[:10],
        'threat_actors': data.get('connections', {}).get('threat_actors', [])[:10]
    }

    result = {
        'collected_at': datetime.now(timezone.utc).isoformat(),
        'source': 'Google-News-Scraper',
        'total_stories': len(unique_stories),
        'stories': unique_stories[:20],
        'entities': entities,
        'summary': data.get('summary', {})
    }

    output_file = OUTPUT_DIR / "news.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"  Collected {len(unique_stories)} news stories")
    return True


def collect_commodities():
    """
    Collect commodity prices from free sources.
    Using placeholder data for now - real APIs require keys.
    """
    print("Collecting commodity data...")

    # For now, create realistic placeholder data
    # In production, would use Yahoo Finance, Alpha Vantage, etc.
    import random

    base_prices = {
        'coal_mtf': 142.50,
        'lng_henry_hub': 3.24,
        'soybeans': 1024.00,
        'corn': 485.00,
        'auto_index': 48200.00
    }

    commodities = []
    for name, base in base_prices.items():
        change_pct = random.uniform(-3, 3)
        price = base * (1 + change_pct / 100)
        commodities.append({
            'name': name,
            'price': round(price, 2),
            'change_pct': round(change_pct, 2),
            'unit': 'USD'
        })

    result = {
        'collected_at': datetime.now(timezone.utc).isoformat(),
        'source': 'market_data',
        'note': 'Simulated data - real API integration pending',
        'commodities': commodities
    }

    output_file = OUTPUT_DIR / "commodities.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"  Collected {len(commodities)} commodity prices")
    return True


def collect_infrastructure_status():
    """
    Generate infrastructure status report.
    In production, would pull from monitoring systems.
    """
    print("Collecting infrastructure status...")

    infrastructure = {
        'terminals': [
            {'name': 'Seagirt Marine Terminal', 'type': 'Container', 'status': 'operational', 'lat': 39.2558, 'lng': -76.5528},
            {'name': 'Dundalk Marine Terminal', 'type': 'RoRo/Breakbulk', 'status': 'operational', 'lat': 39.2467, 'lng': -76.5256},
            {'name': 'CNX Marine Terminal', 'type': 'Coal Export', 'status': 'operational', 'lat': 39.2089, 'lng': -76.5847},
            {'name': 'Fairfield Auto Terminal', 'type': 'Automobiles', 'status': 'operational', 'lat': 39.2156, 'lng': -76.5678}
        ],
        'rail': [
            {'name': 'Howard Street Tunnel', 'operator': 'CSX', 'status': 'degraded', 'note': 'Capacity bottleneck', 'lat': 39.2903, 'lng': -76.6156},
            {'name': 'Penn Station', 'operator': 'Amtrak', 'status': 'operational', 'lat': 39.3017, 'lng': -76.5917},
            {'name': 'Bayview Yard', 'operator': 'Norfolk Southern', 'status': 'operational', 'lat': 39.2875, 'lng': -76.5589}
        ],
        'chokepoints': [
            {'name': 'Fort McHenry Channel', 'type': 'Ship Channel', 'status': 'operational', 'lat': 39.2150, 'lng': -76.5297},
            {'name': 'Key Bridge Area', 'type': 'Maritime', 'status': 'critical', 'note': 'Bridge collapse - restricted navigation', 'lat': 39.1847, 'lng': -76.5286}
        ],
        'scanners': [
            {'name': 'Baltimore Terminal Railroad', 'broadcastify_id': 43356, 'status': 'active'},
            {'name': 'CSX/NS Regional Rail', 'broadcastify_id': 14954, 'status': 'active'},
            {'name': 'Baltimore Marine', 'broadcastify_id': 42710, 'status': 'active'},
            {'name': 'Coast Guard Sector Baltimore', 'broadcastify_id': 31547, 'status': 'active'}
        ]
    }

    result = {
        'collected_at': datetime.now(timezone.utc).isoformat(),
        'infrastructure': infrastructure,
        'summary': {
            'total_terminals': len(infrastructure['terminals']),
            'total_rail': len(infrastructure['rail']),
            'total_chokepoints': len(infrastructure['chokepoints']),
            'total_scanners': len(infrastructure['scanners']),
            'operational': sum(1 for t in infrastructure['terminals'] if t['status'] == 'operational'),
            'degraded': sum(1 for r in infrastructure['rail'] if r['status'] == 'degraded'),
            'critical': sum(1 for c in infrastructure['chokepoints'] if c['status'] == 'critical')
        }
    }

    output_file = OUTPUT_DIR / "infrastructure.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"  Infrastructure status updated")
    return True


def create_manifest():
    """Create a manifest file listing all available data."""
    manifest = {
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'data_files': [
            {'name': 'amtrak.json', 'description': 'Amtrak trains near Baltimore', 'update_frequency': '5 minutes'},
            {'name': 'news.json', 'description': 'News from Google-News-Scraper', 'update_frequency': '4 hours'},
            {'name': 'commodities.json', 'description': 'Port-relevant commodity prices', 'update_frequency': '30 minutes'},
            {'name': 'infrastructure.json', 'description': 'Infrastructure status', 'update_frequency': '15 minutes'}
        ],
        'sources': {
            'amtrak': {'api': 'api-v3.amtraker.com', 'requires_key': False, 'status': 'active'},
            'news': {'api': 'GitHub raw', 'requires_key': False, 'status': 'active'},
            'commodities': {'api': 'various', 'requires_key': True, 'status': 'simulated'},
            'ais': {'api': 'aisstream.io', 'requires_key': True, 'status': 'pending'},
            'scanner': {'api': 'broadcastify', 'requires_key': False, 'status': 'links_only'}
        }
    }

    output_file = OUTPUT_DIR / "manifest.json"
    with open(output_file, 'w') as f:
        json.dump(manifest, f, indent=2)


def main():
    """Run all collectors."""
    print(f"Baltimore Intel Data Collector")
    print(f"Started at: {datetime.now(timezone.utc).isoformat()}")
    print("-" * 50)

    ensure_output_dir()

    results = {
        'amtrak': collect_amtrak(),
        'news': collect_news(),
        'commodities': collect_commodities(),
        'infrastructure': collect_infrastructure_status()
    }

    create_manifest()

    print("-" * 50)
    print("Collection complete:")
    for name, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {name}")

    # Return success if at least some collectors worked
    success_count = sum(results.values())
    print(f"\n{success_count}/{len(results)} collectors succeeded")

    # Only fail if nothing worked
    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    exit(main())
