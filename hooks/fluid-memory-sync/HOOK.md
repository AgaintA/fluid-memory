---
name: fluid-memory-sync
description: "Automatically sync conversation to Fluid Memory when messages are sent"
homepage: https://github.com/yourusername/fluid-memory
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "events": ["message:sent"],
      "requires": { "bins": ["node"] }
    }
  }
---

# Fluid Memory Sync Hook

Automatically syncs conversation to Fluid Memory vector store when the AI sends a message.

## What It Does

1. Listens for `message:sent` events (every time the AI replies)
2. Extracts the conversation from the event context
3. Calls `fluid_increment_summarize` to accumulate and store memory
4. When threshold is reached (default 3 rounds), writes to ChromaDB

## Requirements

- Fluid Memory skill must be installed
- Python with chromadb must be available
- Configuration in `config.yaml`:

```yaml
summarize_threshold: 3  # rounds before writing to vector DB
```

## Events

- `message:sent`: Triggered after every AI response

## How It Works

```
User message → AI responds → Hook fires → Update buffer →
3 rounds reached → Write to ChromaDB → Clear buffer
```

## Disable

```bash
# Edit config or remove the hook directory
```
