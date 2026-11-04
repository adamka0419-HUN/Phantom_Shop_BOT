import os
import asyncio
import discord
from discord.ext import commands

# 1. Bot (Shop / Ticket / Setup) beállítása
intents_bot1 = discord.Intents.default()
intents_bot1.message_content = True
intents_bot1.guilds = True
intents_bot1.members = True
bot1 = commands.Bot(command_prefix="!", intents=intents_bot1)

@bot1.event
async def on_ready():
    print(f"Shop/Ticket bot sikeresen bejelentkezett mint {bot1.user}")

# --- AUTOMATIKUS SZERVERÉPÍTŐ PARANCS (!setup) ---
@bot1.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    guild = ctx.guild
    await ctx.send("⏳ *A szerver felépítése megkezdődött, kérlek várj...*", delete_after=10)

    # Admin jogok a botnak / lakatoláshoz
    overwrites_locked = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
    }

    try:
        # 1. SERVER STATS
        cat1 = await guild.create_category("📊 ── SERVER STATS ──")
        await guild.create_text_channel("┌───≪•◦•≫───┐", category=cat1, overwrites=overwrites_locked)
        await guild.create_text_channel("👤・all-members", category=cat1, overwrites=overwrites_locked)
        await guild.create_text_channel("👤・members", category=cat1, overwrites=overwrites_locked)
        await guild.create_text_channel("👅・customer", category=cat1, overwrites=overwrites_locked)
        await guild.create_text_channel("🛒・phantomshop.site", category=cat1, overwrites=overwrites_locked)
        await guild.create_text_channel("└───≪•◦•≫───┘", category=cat1, overwrites=overwrites_locked)

        # 2. WELCOME
        cat2 = await guild.create_category("📌 ── WELCOME ──")
        await guild.create_text_channel("╭・🌐 join", category=cat2)
        await guild.create_text_channel("┣・🌐 invites", category=cat2)
        await guild.create_text_channel("┣・🌐 b00st", category=cat2)
        await guild.create_text_channel("╰・⚠️ backup", category=cat2)

        # 3. DETECTION
        cat3 = await guild.create_category("🎯 ── DETECTION ──")
        await guild.create_text_channel("oldclaim", category=cat3)
        await guild.create_text_channel("╭・⏱️ queue", category=cat3)
        await guild.create_text_channel("┣・🎯 claims", category=cat3)
        await guild.create_text_channel("┣・🔔 claim-ping", category=cat3)
        await guild.create_text_channel("┣・🏦 bank", category=cat3)
        await guild.create_text_channel("┣・⭐ r3seller", category=cat3)
        await guild.create_text_channel("╰・🛒 cla1ms-b4y", category=cat3)

        # 4. HELP
        cat4 = await guild.create_category("💥 ── HELP ──")
        await guild.create_text_channel("oldclaim-key", category=cat4)
        await guild.create_text_channel("╭・🚀 find", category=cat4)
        await guild.create_text_channel("┣・❓ redeem", category=cat4)
        await guild.create_text_channel("┣・❓ faq", category=cat4)
        await guild.create_text_channel("┣・❓ r3seller-faq", category=cat4)
        await guild.create_text_channel("╰・❓ redeem-key", category=cat4)

        # 5. TICKET
        cat5 = await guild.create_category("💌 ── TICKET ──")
        await guild.create_text_channel("╭・💗 ticket", category=cat5)
        await guild.create_text_channel("┣・⭐ ticket-review", category=cat5)
        await guild.create_text_channel("╰・🛒 ord3rs", category=cat5)

        # 6. GENERAL (Shop és Üzenetek)
        cat6 = await guild.create_category("💬 ── GENERAL ──")
        await guild.create_text_channel("╭・🔔 announcements", category=cat6)
        await guild.create_text_channel("┣・📦 r3st0ck", category=cat6)
        await guild.create_text_channel("┣・🛒 pr0duct-list", category=cat6)
        await guild.create_text_channel("┣・💸 paym3nts", category=cat6)
        await guild.create_text_channel("┣・🎁 giveaway", category=cat6)
        await guild.create_text_channel("┣・📖 rul3s", category=cat6, overwrites=overwrites_locked)
        await guild.create_text_channel("┣・🔑 r3s3ller", category=cat6)
        await guild.create_text_channel("┣・💬 public-chat", category=cat6)
        await guild.create_text_channel("┣・🤖 bot-cmds", category=cat6)
        await guild.create_text_channel("┣・✨ inv-r3w4rds", category=cat6)
        await guild.create_text_channel("╰・💎 b00st-r3w4rds", category=cat6)

        # 7. CLIENTS (Vouchoknak)
        cat7 = await guild.create_category("💜 ── CLIENTS ──")
        await guild.create_text_channel("┣・💜 v0uch", category=cat7)
        await guild.create_text_channel("╰・💬 chat", category=cat7)

        # 8. PARTNERS
        cat8 = await guild.create_category("👥 ── PARTNERS ──")
        await guild.create_text_channel("╭・💖 promotion", category=cat8)

        await ctx.send("✅ **A szerver sikeresen felépítve! Minden kategória és csatorna elkészült!**")
    except Exception as e:
        await ctx.send(f"❌ Hiba történt: {e}")

# Shop parancs
@bot1.command(name="shop")
async def shop(ctx):
    embed = discord.Embed(
        title="🛒 Phantom Shop - Termékek",
        description="Válassz alábbi kínálatunkból:",
        color=discord.Color.green()
    )
    embed.add_field(name="📦 Termék 1", value="Leírás vagy árak itt... - **1000 Ft**", inline=False)
    embed.add_field(name="📦 Termék 2", value="Leírás vagy árak itt... - **2500 Ft**", inline=False)
    embed.set_footer(text="Vásárláshoz nyiss ticketet a !ticket paranccsal!")
    await ctx.send(embed=embed)

# Ticket nyitó gomb nézet
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Ticket nyitása", style=discord.ButtonStyle.blurple, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
        await interaction.response.send_message(f"Sikeresen létrehoztam a ticketedet: {channel.mention}", ephemeral=True)
        await channel.send(f"Üdvözöllek {interaction.user.mention}! A tulajdonos hamarosan válaszol. Írd meg miben segíthetünk.")

@bot1.command(name="ticket")
async def ticket(ctx):
    embed = discord.Embed(
        title="🎫 Ticket Rendszer",
        description="Kattints az alábbi gombra, ha vásárolni szeretnél vagy hibát szeretnél jelezni!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())


# 2. Bot (Vouch / Rep) beállítása
intents_bot2 = discord.Intents.default()
intents_bot2.message_content = True
bot2 = commands.Bot(command_prefix="!", intents=intents_bot2)

@bot2.event
async def on_ready():
    print(f"Vouch/Rep bot sikeresen bejelentkezett mint {bot2.user}")

@bot2.command(name="vouch")
async def vouch(ctx, *, text: str):
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title="🌟 Új Vouch / Értékelés!",
        description=text,
        color=discord.Color.gold()
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    embed.set_footer(text="Köszönjük a bizalmat!")
    await ctx.send(embed=embed)


# Fő futtató függvény a két bot párhuzamos indításához
async def main():
    token1 = os.getenv("DISCORD_TOKEN")
    token2 = os.getenv("DISCORD_TOKEN_2")

    if not token1 or not token2:
        print("HIBA: A DISCORD_TOKEN vagy a DISCORD_TOKEN_2 nincs beállítva a környezeti változók között!")
        return

    async with bot1, bot2:
        await asyncio.gather(
            bot1.start(token1),
            bot2.start(token2)
        )

if __name__ == "__main__":
    asyncio.run(main())
