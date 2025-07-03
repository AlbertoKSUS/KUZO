import asyncio

from bot import KuzoBot
import secret


async def main():
    bot = KuzoBot()
    async with bot:
        await bot.start(secret.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
