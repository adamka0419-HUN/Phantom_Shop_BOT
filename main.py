import asyncio
import discord
from discord.ext import commands

# --- 1. BOT BEÁLLÍTÁSAI ---
# Ide írd be a két botod tokenjét a "" közé
TOKEN_1 = "AZ_1._BOT_TOKENE"
TOKEN_2 = "A_2._BOT_TOKENE"

# Ide pedig a vouch csatornád ID-ját (számok)
VOUCH_CHANNEL_ID = 123456789012345678

# --- 2. ELSŐ BOT (Shop & Ticket & Stats) ---
intents_1 = discord.Intents.default()
intents_1.message_content = True
bot1 = commands.Bot(command_prefix="!", intents=intents_1)

@bot1.event
async def on_ready():
    print(f"Bejelentkezett az 1. bot: {bot1.user}")

@bot1.tree.command(name="setup-shop", description="Shop felépítése")
async def setup_shop(interaction: discord.Interaction):
    await interaction.response.send_message("Shop csatornák létrehozva!", ephemeral=True)

@bot1.tree.command(name="setup-ticket", description="Ticket rendszer létrehozása")
async def setup_ticket(interaction: discord.Interaction):
    await interaction.response.send_message("Ticket rendszer kész!", ephemeral=True)

# --- 3. MÁSODIK BOT (Vouch & Értékelés) ---
intents_2 = discord.Intents.default()
intents_2.message_content = True
bot2 = commands.Bot(command_prefix="!", intents=intents_2)

@bot2.event
async def on_ready():
    print(f"Bejelentkezett a 2. bot: {bot2.user}")

@bot2.tree.command(name="vouch", description="Értékelés küldése")
async def vouch(interaction: discord.Interaction,uzenet: str):
    channel = bot2.get_channel(VOUCH_CHANNEL_ID)
    if channel:
        await channel.send(f"Új vouch **{interaction.user.mention}**-től: {uzenet}")
        await interaction.response.send_message("Köszönjük az értékelést!", ephemeral=True)
    else:
        await interaction.response.send_message("A vouch csatorna nem található!", ephemeral=True)

# --- 4. A KÉT BOT PÁRHUZAMOS INDÍTÁSA ---
async def main():
    async with bot1, bot2:
        await asyncio.gather(
            bot1.start(),
            bot2.start()
        )

if __name__ == "__main__":
    asyncio.run(main())
