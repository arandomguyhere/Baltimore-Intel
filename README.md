# Baltimore Intel

**Critical Infrastructure Intelligence Platform for the Port of Baltimore**

Real-time monitoring of maritime, rail, and critical infrastructure with AI-powered threat detection.

## Live Dashboard

**[situation.watch](https://www.situation.watch/)** - Live situational awareness map

## Overview

Baltimore Intel combines multiple intelligence sources into a unified platform:

| Source | Data Type | Update Frequency |
|--------|-----------|------------------|
| AISstream | Vessel positions, arrivals, departures | Real-time WebSocket |
| Broadcastify | Scanner transcripts (rail, marine, coast guard) | Real-time |
| Google-News-Scraper | News with entity extraction | Every 4 hours |
| OpenRailwayMap | Rail network status | Hourly |
| Amtraker API | Passenger rail movements | 5 minutes |
| Commodity APIs | Coal, LNG, grain, auto futures | 30 minutes |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    situation.watch                           │
│              (Leaflet map, live statistics)                  │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                    baltimore_intel/                          │
│  ├── ais_integration.py      # Vessel tracking               │
│  ├── scanner_feeds.py        # Broadcastify transcripts      │
│  ├── rail_tracking.py        # Amtrak + freight inference    │
│  ├── commodities.py          # Port-relevant commodities     │
│  ├── critical_infrastructure.py  # Asset monitoring          │
│  ├── historical_analysis.py  # 6-month trend analysis        │
│  └── intelligence_hub.py     # Correlation engine            │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                    Watcher Engine                            │
│  ├── NER Pipeline (BERT entity extraction)                   │
│  ├── Notification Hub (Slack, Email, TheHive, Citadel)       │
│  ├── Trend Detection (breaking news, weekly summaries)       │
│  └── MISP/TheHive Integration (threat intel sharing)         │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Docker (Recommended)

```bash
docker-compose -f docker-compose.full.yml up -d
```

Services:
- **Watcher UI**: http://localhost:9002
- **Baltimore Intel API**: http://localhost:8082
- **AIS Tracker**: http://localhost:8080

### Development

```bash
# Baltimore Intel module
cd baltimore_intel
pip install -r requirements.txt
python intelligence_hub.py

# Watcher (Django)
cd Watcher
pip install -r requirements.txt
python manage.py runserver
```

## Baltimore-Specific Tracking

### Port Terminals
- Seagirt Marine Terminal (containers)
- Dundalk Marine Terminal (RoRo, breakbulk)
- CNX Marine Terminal (coal export)
- Fairfield Auto Terminal

### Rail Corridors
- CSX - Howard Street Tunnel
- Norfolk Southern - Bayview Yard
- Amtrak NEC - Penn Station

### Commodities
| Export | Import |
|--------|--------|
| Coal ($2.86B) | Automobiles ($12.7B) |
| LNG ($1.88B) | Machinery |
| Soybeans | Consumer goods |
| Corn | |

### Scanner Feeds (Broadcastify)
- Baltimore Terminal Railroad (43356)
- CSX/NS Regional Rail (14954)
- Baltimore Marine (42710)
- Coast Guard Sector Baltimore (31547)

## Key Features

### From Watcher Engine
- **AI Summaries**: FLAN-T5 generates breaking news summaries
- **Entity Extraction**: BERT NER extracts organizations, locations, threat actors
- **Multi-Channel Alerts**: Slack, Email, TheHive, Citadel (Matrix)
- **Trend Detection**: Identifies emerging threats from frequency analysis

### Baltimore Intel Additions
- **Vessel Correlation**: Links AIS data to commodity movements
- **Freight Inference**: Extracts cargo types from scanner transcripts
- **Infrastructure Monitoring**: Tracks critical chokepoints (tunnels, bridges)
- **Historical Analysis**: 6 months of archived news for pattern detection

## Testing

```bash
cd baltimore_intel
pytest tests/ -v --cov=. --cov-report=term-missing
```

## API Endpoints

### Intelligence Hub (port 8082)

| Endpoint | Description |
|----------|-------------|
| `GET /api/events` | Recent intelligence events |
| `GET /api/correlations` | Cross-source correlations |
| `GET /api/infrastructure` | Infrastructure status |
| `GET /api/vessels` | Active vessel tracking |
| `POST /api/alert` | Submit manual alert |

### Watcher (port 9002)

| Endpoint | Description |
|----------|-------------|
| `GET /api/trendy_words` | Trending threat keywords |
| `GET /api/posts` | Recent threat articles |
| `GET /api/summary` | AI-generated summaries |

## Configuration

### Environment Variables

```bash
# AISstream
AISSTREAM_API_KEY=your_key

# Watcher Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
THEHIVE_URL=https://thehive.your-org.com
THEHIVE_API_KEY=your_key
MISP_URL=https://misp.your-org.com
MISP_API_KEY=your_key

# Email
EMAIL_HOST=smtp.your-org.com
EMAIL_FROM=alerts@your-org.com
```

## Data Sources

### Your Repositories
- [Google-News-Scraper](https://github.com/arandomguyhere/Google-News-Scraper) - News with entity extraction
- [Drone_news](https://github.com/arandomguyhere/Drone_news) - Drone/aviation news
- [AIS_Tracker](https://github.com/arandomguyhere/AIS_Tracker) - Vessel tracking
- [geopolitical-threat-mapper](https://github.com/arandomguyhere/geopolitical-threat-mapper) - Threat visualization
- [ScannerTranscribe](https://github.com/arandomguyhere/ScannerTranscribe) - Scanner audio transcription

### External APIs
- [AISstream](https://aisstream.io/) - Real-time AIS data
- [Amtraker](https://amtraker.com/) - Amtrak train positions
- [OpenRailwayMap](https://www.openrailwaymap.org/) - Rail infrastructure
- [TransitDocs](https://asm.transitdocs.com/) - Rail network status

## Credits

- **Watcher Engine**: Originally by [Thales Group CERT](https://github.com/thalesgroup-cert/Watcher)
- **Baltimore Intel**: Custom integration layer for Port of Baltimore intelligence

## License

See [LICENSE](./LICENSE) for details.
