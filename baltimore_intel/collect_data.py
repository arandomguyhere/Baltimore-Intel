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
    Collect Baltimore-specific news from Google News RSS.
    Searches for Port of Baltimore, shipping, infrastructure topics.
    """
    import xml.etree.ElementTree as ET
    from urllib.parse import quote

    print("Collecting Baltimore news...")

    # Baltimore-specific search queries
    search_queries = [
        "Port of Baltimore",
        "Baltimore shipping",
        "Baltimore harbor",
        "Maryland transportation infrastructure",
        "Baltimore rail freight",
        "Chesapeake Bay shipping",
    ]

    stories = []
    seen_titles = set()

    for query in search_queries:
        try:
            # Google News RSS feed URL
            encoded_query = quote(query)
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; BaltimoreIntel/1.0)'
            })

            if response.status_code == 200:
                root = ET.fromstring(response.content)

                for item in root.findall('.//item')[:5]:  # Top 5 per query
                    title = item.find('title')
                    link = item.find('link')
                    pub_date = item.find('pubDate')
                    source = item.find('source')

                    title_text = title.text if title is not None else None

                    if title_text and title_text not in seen_titles:
                        seen_titles.add(title_text)
                        stories.append({
                            'title': title_text,
                            'url': link.text if link is not None else None,
                            'source': source.text if source is not None else 'Google News',
                            'date': pub_date.text if pub_date is not None else None,
                            'query': query
                        })

        except Exception as e:
            print(f"  Error fetching '{query}': {e}")
            continue

    if not stories:
        print("  No news found, keeping existing data")
        return True

    # Sort by date (newest first) and limit
    unique_stories = stories[:20]

    entities = {
        'topics': list(set(s.get('query', '') for s in unique_stories)),
        'sources': list(set(s.get('source', '') for s in unique_stories if s.get('source')))[:10]
    }

    result = {
        'collected_at': datetime.now(timezone.utc).isoformat(),
        'source': 'Google News RSS',
        'region': 'Baltimore / Port of Baltimore',
        'total_stories': len(unique_stories),
        'stories': unique_stories,
        'entities': entities
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


def collect_ais():
    """
    Collect AIS vessel data from AISstream.io
    Requires AISSTREAM_API_KEY environment variable.
    """
    print("Collecting AIS vessel data...")

    api_key = os.environ.get('AISSTREAM_API_KEY')
    if not api_key:
        print("  No AISSTREAM_API_KEY set, skipping AIS collection")
        return True  # Don't fail, just skip

    print(f"  API key found (starts with: {api_key[:8]}...)")

    # Expanded bounding box - Baltimore to Chesapeake Bay entrance
    # Covers Port of Baltimore, shipping lanes, and Bay entrance
    bbox = [
        [-76.8, 36.8],  # SW corner (near Norfolk/Bay entrance)
        [-75.8, 39.5]   # NE corner (above Baltimore)
    ]

    try:
        import websocket
        import time

        vessels = []
        message_count = [0]  # Use list to allow mutation in nested function
        ws_url = "wss://stream.aisstream.io/v0/stream"

        # Connect and collect for 30 seconds
        def on_message(ws, message):
            message_count[0] += 1
            data = json.loads(message)
            msg_type = data.get('MessageType')

            if message_count[0] <= 3:
                print(f"  Received message {message_count[0]}: {msg_type}")

            if msg_type == 'PositionReport':
                msg = data.get('Message', {}).get('PositionReport', {})
                meta = data.get('MetaData', {})
                vessels.append({
                    'mmsi': meta.get('MMSI'),
                    'name': meta.get('ShipName', '').strip(),
                    'lat': msg.get('Latitude'),
                    'lon': msg.get('Longitude'),
                    'speed': msg.get('Sog'),  # Speed over ground
                    'course': msg.get('Cog'),  # Course over ground
                    'heading': msg.get('TrueHeading'),
                    'ship_type': meta.get('ShipType'),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                })

        def on_open(ws):
            print(f"  Connected to AISstream, subscribing to bbox: {bbox}")
            subscribe = {
                "APIKey": api_key,
                "BoundingBoxes": [bbox]
            }
            ws.send(json.dumps(subscribe))

        def on_error(ws, error):
            print(f"  WebSocket error: {error}")

        def on_close(ws, close_status, close_msg):
            print(f"  WebSocket closed: {close_status} - {close_msg}")

        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_open=on_open,
            on_error=on_error,
            on_close=on_close
        )

        # Run for 30 seconds to collect vessels
        import threading
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        time.sleep(30)
        ws.close()

        print(f"  Total messages received: {message_count[0]}")
        print(f"  Position reports: {len(vessels)}")

        # Deduplicate by MMSI (keep latest position)
        unique_vessels = {}
        for v in vessels:
            if v['mmsi']:
                unique_vessels[v['mmsi']] = v
        vessels = list(unique_vessels.values())

        result = {
            'collected_at': datetime.now(timezone.utc).isoformat(),
            'source': 'AISstream.io',
            'region': 'Baltimore / Chesapeake Bay',
            'bbox': bbox,
            'vessel_count': len(vessels),
            'vessels': vessels
        }

        output_file = OUTPUT_DIR / "vessels.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"  Collected {len(vessels)} vessels")
        return True

    except ImportError:
        print("  websocket-client not installed, skipping AIS")
        return True
    except Exception as e:
        print(f"  Error collecting AIS data: {e}")
        return True  # Don't fail the whole collection


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
        'infrastructure': collect_infrastructure_status(),
        'ais': collect_ais()
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
