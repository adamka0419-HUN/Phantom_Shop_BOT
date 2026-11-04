import os
import asyncio
import discord
from discord.ext import commands

# 1. Bot (Shop / Ticket / Stats) beállítása
intents_bot1 = discord.Intents.default()
intents_bot1.message_content = True
bot1 = commands.Bot(command_prefix="!", intents=intents_bot1)

@bot1.event
async def on_ready():
    print(f"Shop/Ticket bot sikeresen bejelentkezett mint {bot1.user}")

@bot1.command(name="shop")
async def shop(ctx):
    await ctx.send("Itt találod a Shop menüt!")


# 2. Bot (Vouch / Rep) beállítása
intents_bot2 = discord.Intents.default()
intents_bot2.message_content = True
bot2 = commands.Bot(command_prefix="!", intents=intents_bot2)

@bot2.event
async def on_ready():
    print(f"Vouch/Rep bot sikeresen bejelentkezett mint {bot2.user}")

@bot2.command(name="vouch")
async def vouch(ctx, *, text: str):
    await ctx.send(f"Köszönjük a vouchot! Értékelés: {text}")


# Fő futtató függvény a két bot párhuzamos indításához
async def main():
    # Tokenek lekérése a Render környezeti változóiból
    token1 = os.getenv("DISCORD_TOKEN")
    token2 = os.getenv("DISCORD_TOKEN_2")

    if not token1 or not token2:
        print("HIBA: A DISCORD_TOKEN vagy a DISCORD_TOKEN_2 nincs beállítva a környezeti változók között!")
        return

    # Mindkét bot indítása egyszerre
    async with bot1, bot2:
        await asyncio.gather(
            bot1.start(token1),
            bot2.start(token2)
        )

if __name__ == "__main__":
    asyncio.run(main())
