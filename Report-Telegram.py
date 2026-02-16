from telethon import TelegramClient
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import (
    InputReportReasonSpam,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonChildAbuse,
    InputReportReasonOther,
    InputReportReasonFake,
    InputReportReasonCopyright,
    InputReportReasonGeoIrrelevant,
    InputReportReasonIllegalDrugs,
    InputReportReasonPersonalDetails,
)
from telethon.errors import FloodWaitError, RPCError
import asyncio
import getpass
import random

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

REASONS = {
    "1": ("Spam", InputReportReasonSpam()),
    "2": ("Violence", InputReportReasonViolence()),
    "3": ("Pornography", InputReportReasonPornography()),
    "4": ("Child abuse", InputReportReasonChildAbuse()),
    "5": ("Other", InputReportReasonOther()),
    "6": ("Fake", InputReportReasonFake()),
    "7": ("Copyright", InputReportReasonCopyright()),
    "8": ("Illegal drugs", InputReportReasonIllegalDrugs()),
    "9": ("Personal details / انتشار اطلاعات شخصی", InputReportReasonPersonalDetails()),
    "10": ("Irrelevant geo", InputReportReasonGeoIrrelevant()),
}


async def main():
    print("Telegram Report Tool")
    print("===================\n")

    api_id = input("API ID: ").strip()
    api_hash = getpass.getpass("API Hash (hidden): ").strip()
    phone = input("Phone number (+98...): ").strip()

    channel_input = input("\nChannel (@username or -100xxxxxxxxxx): ").strip()
    if channel_input.startswith('@'):
        channel = channel_input[1:]
    else:
        channel = channel_input

    print("\nنوع گزارش:")
    for k, (name, _) in REASONS.items():
        print(f"  {k:2}) {name}")

    reason_key = input("\nشماره نوع گزارش (مثلاً 9): ").strip()

    if reason_key not in REASONS:
        print(f"{RED}شماره نامعتبر → Spam انتخاب شد{RESET}")
        reason_name, reason_obj = REASONS["1"]
    else:
        reason_name, reason_obj = REASONS[reason_key]

    message_text = input("\nتوضیح گزارش (message):\nاگر خالی بذاری پیش‌فرض می‌ره: ").strip()

    if not message_text or len(message_text) < 8:
        message_text = "Reported via tool - serious violation of rules"
        print("از متن پیش‌فرض استفاده شد")

    try_count = input("\nتعداد گزارش (پیشنهاد: 1 تا 3): ").strip()
    try:
        repeat = max(1, min(int(try_count or 1), 10))
    except:
        repeat = 1

    print(f"\n→ {repeat} گزارش با دلیل: {reason_name}")
    print(f"→ توضیح: {message_text}\n")

    client = TelegramClient('report_session', api_id, api_hash)

    try:
        await client.start(phone=phone)
        print("ورود موفق")

        entity = await client.get_entity(channel)
        title = getattr(entity, 'title', channel)
        print(f"هدف: {title}\n")

        for i in range(1, repeat + 1):
            print(f"تلاش {i}/{repeat} ...")
            try:
                await client(ReportPeerRequest(
                    peer=entity,
                    reason=reason_obj,
                    message=message_text
                ))
                print(f"{GREEN}موفق - گزارش {i} ارسال شد{RESET}")
            except FloodWaitError as e:
                wait = e.seconds
                print(f"{RED}Flood wait → باید {wait} ثانیه صبر کنی (~{wait//60} دقیقه){RESET}")
                await asyncio.sleep(wait)
            except RPCError as e:
                err = str(e).lower()
                print(f"{RED}خطا: {e}{RESET}")
                if "user_not_participant" in err:
                    print("→ باید عضو کانال باشی")
                elif "peer_id_invalid" in err:
                    print("→ آیدی کانال اشتباه است")
                break
            except Exception as e:
                print(f"{RED}خطای غیرمنتظره: {type(e).__name__} - {e}{RESET}")
                break

            await asyncio.sleep(15 + random.uniform(5, 15))  # فاصله ۱۵ تا ۳۰ ثانیه

    except Exception as e:
        print(f"خطای کلی: {e}")

    finally:
        await client.disconnect()
        print("\nاتصال قطع شد.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nمتوقف شد توسط کاربر.")
    except Exception as e:
        print(f"خطای بحرانی: {e}")
