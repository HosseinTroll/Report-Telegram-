# Report-Telegram-
# Telegram Spam Reporter

A minimal Python script using **Telethon** to report a Telegram channel as spam (from your own account).

**⚠️ Very important warning**  
Mass / automated / abusive reporting **will permanently ban your Telegram account**.  
Use this **only** for legitimate spam/abuse reports and **very rarely**.

## Features
- Asks for API ID, API Hash, phone number at runtime (nothing hardcoded)
- Supports @username or numeric channel ID (-100xxxxxxxxxx)
- Handles common Telethon errors with clear messages

## Requirements
- Python 3.7+
- Telethon library

## Installation & Usage (Termux / PC)

```bash
# Install dependencies
pip install telethon

# Run the script
python Report-Telegram.py
# or: python3 Report-Telegram.py
