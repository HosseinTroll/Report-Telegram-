from telethon import TelegramClient
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.errors import FloodWaitError, RPCError
import asyncio
import getpass

async def main():
    print("Telegram Channel Spam Report Tool")
    print("=================================\n")

    # Get credentials from user
    api_id = input("Enter your API ID: ").strip()
    api_hash = getpass.getpass("Enter your API Hash (input hidden): ").strip()
    phone = input("Enter phone number (with country code, e.g. +989123456789): ").strip()

    channel_input = input("\nEnter channel username or ID (e.g. @channel or -1001234567890): ").strip()

    # Clean channel input
    if channel_input.startswith('@'):
        channel = channel_input[1:]
    else:
        channel = channel_input

    print("\nConnecting to Telegram...\n")

    # Create client
    client = TelegramClient('report_session', api_id, api_hash)

    try:
        await client.start(phone=phone)
        print("Login successful")

        entity = await client.get_entity(channel)

        title = entity.title if hasattr(entity, 'title') else channel
        print(f"Target: {title}")

        print("\nSending spam report...")

        # Send spam report
        result = await client(ReportSpamRequest(peer=entity))

        if result:
            print("Spam report sent successfully")
        else:
            print("Report sent (no detailed result returned)")

    except FloodWaitError as e:
        wait_min = round(e.seconds / 60, 1)
        wait_hour = round(e.seconds / 3600, 1)
        print(f"Flood wait error: You must wait {e.seconds} seconds (~{wait_min} min / ~{wait_hour} hours)")
    except RPCError as e:
        print(f"Telegram error: {e}")
        error_str = str(e).lower()
        if "peer_id_invalid" in error_str:
            print("→ Invalid channel username or ID")
        elif "user_not_participant" in error_str or "chat_write_forbidden" in error_str:
            print("→ You need to be a member of the channel to report it")
        elif "auth_key_unregistered" in error_str:
            print("→ Incorrect api_id or api_hash")
    except Exception as e:
        print(f"Unexpected error: {type(e).name}")
        print(str(e))

    finally:
        await client.disconnect()
        print("\nSession disconnected.")

# Run the script
if name == 'main':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    except Exception as e:
        print(f"Critical error: {e}")