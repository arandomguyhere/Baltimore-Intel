<p align="center">
    <img alt="Baltimore Intel" src="https://img.shields.io/badge/Baltimore-Intel-0066cc?style=for-the-badge&logo=radar&logoColor=white" height="60">
</p>

<p align="center">
    <strong>Critical Infrastructure Intelligence Platform for the Port of Baltimore</strong>
</p>

<p align="center">
    <a href="https://arandomguyhere.github.io/Baltimore-Intel/">
        <img src="https://img.shields.io/badge/Project-Page-success?style=for-the-badge&logo=github&logoColor=white" alt="Project Page">
    </a>
    <a href="https://github.com/arandomguyhere/Baltimore-Intel/actions">
        <img src="https://img.shields.io/github/actions/workflow/status/arandomguyhere/Baltimore-Intel/test.yml?style=for-the-badge&logo=github" alt="Build Status">
    </a>
    <a href="https://github.com/arandomguyhere/Baltimore-Intel">
        <img src="https://img.shields.io/github/stars/arandomguyhere/Baltimore-Intel?style=for-the-badge&logo=github" alt="Stars">
    </a>
    <a href="./LICENSE">
        <img src="https://img.shields.io/github/license/arandomguyhere/Baltimore-Intel?style=for-the-badge" alt="License">
    </a>
</p>

<p align="center">
    Real-time monitoring of maritime, rail, and critical infrastructure with AI-powered threat detection.
</p>

---

## Overview

Baltimore Intel aggregates multiple intelligence sources into a unified platform for monitoring the Port of Baltimore and surrounding critical infrastructure.

| Source | Type | Frequency |
|--------|------|-----------|
| **AISstream** | Vessel positions | Real-time WebSocket |
| **Broadcastify** | Scanner transcripts | Real-time |
| **Google-News-Scraper** | News + entities | 4 hours |
| **OpenRailwayMap** | Rail network | Hourly |
| **Amtraker** | Passenger rail | 5 min |
| **Commodity APIs** | Coal, LNG, grain | 30 min |

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    GitHub Pages Dashboard                       │
│              arandomguyhere.github.io/Baltimore-Intel           │
└────────────────────────────────────────────────────────────────┘
                               ▲
┌────────────────────────────────────────────────────────────────┐
│                      baltimore_intel/                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ AIS Tracker  │ │ Rail Monitor │ │ Scanner Feed │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Commodities  │ │Infrastructure│ │  Historical  │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                    Intelligence Hub                             │
└────────────────────────────────────────────────────────────────┘
                               ▲
┌────────────────────────────────────────────────────────────────┐
│                      Watcher Engine                             │
│  NER Pipeline │ Notifications │ TheHive/MISP │ Trend Detection │
└────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/arandomguyhere/Baltimore-Intel.git
cd Baltimore-Intel
docker-compose -f docker-compose.full.yml up -d
```

**Services:**
| Service | URL |
|---------|-----|
| Watcher UI | http://localhost:9002 |
| Baltimore Intel API | http://localhost:8082 |
| AIS Tracker | http://localhost:8080 |

### CLI

```bash
./run.py docker   # Start all services
./run.py api      # API only
./run.py test     # Run tests
./run.py check    # Check dependencies
```

---

## Baltimore Port Coverage

### Terminals
| Terminal | Type | Coordinates |
|----------|------|-------------|
| Seagirt | Containers | 39.2558, -76.5528 |
| Dundalk | RoRo, Breakbulk | 39.2467, -76.5256 |
| CNX Marine | Coal Export | 39.2089, -76.5847 |
| Fairfield | Automobiles | 39.2156, -76.5678 |

### Rail Corridors
- **CSX** - Howard Street Tunnel (capacity bottleneck)
- **Norfolk Southern** - Bayview Yard
- **Amtrak NEC** - Penn Station

### Scanner Feeds
| Feed | Broadcastify ID |
|------|-----------------|
| Baltimore Terminal Railroad | 43356 |
| CSX/NS Regional | 14954 |
| Baltimore Marine | 42710 |
| Coast Guard Sector Baltimore | 31547 |

### Top Commodities
| Export | Value | Import | Value |
|--------|-------|--------|-------|
| Coal | $2.86B | Automobiles | $12.7B |
| LNG | $1.88B | Machinery | $3.2B |
| Soybeans | $1.2B | Consumer Goods | $2.8B |

---

## Features

### Intelligence Collection
- **Vessel Tracking** - Real-time AIS with arrival/departure detection
- **Scanner Analysis** - NLP on Broadcastify transcripts
- **Freight Inference** - Extract cargo types from radio traffic
- **News Monitoring** - Entity extraction from 100+ sources

### AI-Powered Analysis
- **BERT NER** - Extract organizations, locations, threat actors
- **FLAN-T5** - Generate breaking news summaries
- **Trend Detection** - Identify emerging patterns
- **Historical Analysis** - 6 months of archived data

### Alerting & Integration
- **Multi-Channel** - Slack, Email, Citadel (Matrix)
- **TheHive** - Incident case management
- **MISP** - Threat intelligence sharing
- **Webhooks** - Custom integrations

---

## API Reference

### Intelligence Hub (`:8082`)

```bash
# Get recent events
curl http://localhost:8082/api/events

# Get correlations
curl http://localhost:8082/api/correlations

# Infrastructure status
curl http://localhost:8082/api/infrastructure

# Active vessels
curl http://localhost:8082/api/vessels
```

### Watcher Engine (`:9002`)

```bash
# Trending keywords
curl http://localhost:9002/api/trendy_words

# Recent articles
curl http://localhost:9002/api/posts

# AI summaries
curl http://localhost:9002/api/summary
```

---

## Configuration

### Environment Variables

```bash
# Required
AISSTREAM_API_KEY=your_aisstream_key

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
EMAIL_HOST=smtp.example.com
EMAIL_FROM=alerts@example.com

# Threat Intel
THEHIVE_URL=https://thehive.example.com
THEHIVE_API_KEY=your_key
MISP_URL=https://misp.example.com
MISP_API_KEY=your_key
```

---

## Related Projects

| Project | Description |
|---------|-------------|
| [Google-News-Scraper](https://github.com/arandomguyhere/Google-News-Scraper) | News aggregation with entity extraction |
| [AIS_Tracker](https://github.com/arandomguyhere/AIS_Tracker) | Vessel tracking dashboard |
| [Drone_news](https://github.com/arandomguyhere/Drone_news) | Aviation/drone news feed |
| [geopolitical-threat-mapper](https://github.com/arandomguyhere/geopolitical-threat-mapper) | Threat visualization |
| [ScannerTranscribe](https://github.com/arandomguyhere/ScannerTranscribe) | Scanner audio transcription |

---

## Testing

```bash
cd baltimore_intel
pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## Credits

- **Watcher Engine** - [Thales Group CERT](https://github.com/thalesgroup-cert/Watcher)
- **AISstream** - [aisstream.io](https://aisstream.io/)
- **Amtraker** - [amtraker.com](https://amtraker.com/)

---

<p align="center">
    <sub>Built for situational awareness of the Port of Baltimore and surrounding critical infrastructure.</sub>
</p>
