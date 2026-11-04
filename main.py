import os
import asyncio
import discord
from discord.ext import commands

intents_bot1 = discord.Intents.default()
intents_bot1.message_content = True
intents_bot1.guilds = True
intents_bot1.members = True
bot1 = commands.Bot(command_prefix="!", intents=intents_bot1)

@bot1.event
async def on_ready():
    print(f"Shop/Ticket bot bejelentkezett mint {bot1.user}")

# --- 1. CSATORNÁK TÖRLÉSE ---
@bot1.command(name="clear_all")
@commands.has_permissions(administrator=True)
async def clear_all(ctx):
    guild = ctx.guild
    await ctx.send("⚠️ *Minden csatorna törlése folyamatban...*", delete_after=5)
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Hiba törlésnél ({channel.name}): {e}")
    print("Minden csatorna törölve!")

# --- 2. RESELLER ÉS SHOP SZERVER FELÉPÍTÉSE ---
@bot1.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    guild = ctx.guild
    msg = await ctx.send("⏳ *A Reseller rendszer és a szerverstruktúra építése folyamatban...*")

    try:
        # 1. RANGOK LÉTREHOZÁSA
        await guild.create_role(name="Owner", color=discord.Color.purple(), permissions=discord.Permissions.all())
        await asyncio.sleep(0.5)
        await guild.create_role(name="Lifetime Nitro Boost Sub", color=discord.Color.from_rgb(138, 43, 226))
        await asyncio.sleep(0.5)
        await guild.create_role(name="Premium Customer 100€+", color=discord.Color.gold())
        await asyncio.sleep(0.5)
        await guild.create_role(name="Special Customer 20€+", color=discord.Color.orange())
        await asyncio.sleep(0.5)
        await guild.create_role(name="Customer", color=discord.Color.from_rgb(46, 204, 113))
        await asyncio.sleep(0.5)
        await guild.create_role(name="Reseller", color=discord.Color.from_rgb(0, 206, 209))
        await asyncio.sleep(0.5)
        await guild.create_role(name="Member", color=discord.Color.blue())
        await asyncio.sleep(1)

        overwrites_locked = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }

        # 2. STATS KATEGÓRIA
        cat1 = await guild.create_category("📊 ── SERVER STATS ──")
        await guild.create_text_channel("👤・all-members", category=cat1, overwrites=overwrites_locked)
        await guild.create_text_channel("👅・customer", category=cat1, overwrites=overwrites_locked)
        await guild.create_text_channel("🛒・phantomshop.site", category=cat1, overwrites=overwrites_locked)
        await asyncio.sleep(1)

        # 3. WELCOME KATEGÓRIA
        cat2 = await guild.create_category("📌 ── WELCOME ──")
        await guild.create_text_channel("・join", category=cat2)
        await guild.create_text_channel("・invites", category=cat2)
        await guild.create_text_channel("・boost", category=cat2)
        await asyncio.sleep(1)

        # 4. RESELLER PROGRAM KATEGÓRIA
        cat_reseller = await guild.create_category("💼 ── RESELLER PROGRAM ──")
        await guild.create_text_channel("・reseller-info", category=cat_reseller, overwrites=overwrites_locked)
        await guild.create_text_channel("・reseller-chat", category=cat_reseller)
        await guild.create_text_channel("・reseller-commands", category=cat_reseller)
        await asyncio.sleep(1)

        # 5. SHOP & TICKET KATEGÓRIA
        cat3 = await guild.create_category("🛒 ── SHOP & TICKET ──")
        await guild.create_text_channel("・shop", category=cat3)
        await guild.create_text_channel("・ticket", category=cat3)
        await guild.create_text_channel("・orders", category=cat3)
        await asyncio.sleep(1)

        # 6. GENERAL KATEGÓRIA
        cat4 = await guild.create_category("💬 ── GENERAL ──")
        await guild.create_text_channel("・announcements", category=cat4)
        await guild.create_text_channel("・rules", category=cat4, overwrites=overwrites_locked)
        await guild.create_text_channel("・chat", category=cat4)
        await guild.create_text_channel("・bot-cmds", category=cat4)
        await asyncio.sleep(1)

        # 7. CLIENTS KATEGÓRIA
        cat5 = await guild.create_category("💜 ── CLIENTS ──")
        await guild.create_text_channel("・vouch", category=cat5)

        await msg.edit(content="✅ **A Reseller szerverstruktúra sikeresen elkészült!**")
    except Exception as e:
        await ctx.send(f"❌ Hiba történt: {e}")

# Shop parancs
@bot1.command(name="shop")
async def shop(ctx):
    embed = discord.Embed(title="🛒 Phantom Shop - Termékek", description="Válassz kínálatunkból:", color=discord.Color.green())
    embed.add_field(name="📦 Termék 1", value="Leírás... - **1000 Ft**", inline=False)
    await ctx.send(embed=embed)

# Ticket View & Command
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
        await interaction.response.send_message(f"Sikeresen létrehoztam: {channel.mention}", ephemeral=True)

@bot1.command(name="ticket")
async def ticket(ctx):
    embed = discord.Embed(title="🎫 Ticket Rendszer", description="Kattints a gombra a vásárláshoz!", color=discord.Color.blue())
    await ctx.send(embed=embed, view=TicketView())

# Példa Reseller parancsok vázlata
@bot1.command(name="addcredits")
@commands.has_permissions(administrator=True)
async def addcredits(ctx, member: discord.Member, amount: int):
    embed = discord.Embed(title="💳 Credits Added", description=f"Successfully added **{amount}** credits to {member.mention}.", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot1.command(name="kreditinfo")
async def kreditinfo(ctx, member: discord.Member = None):
    target = member or ctx.author
    embed = discord.Embed(title="📊 Credit Balance", description=f"{target.mention} current balance: **0 Credits**", color=discord.Color.gold())
    await ctx.send(embed=embed)

# 2. Bot (Vouch)
intents_bot2 = discord.Intents.default()
intents_bot2.message_content = True
bot2 = commands.Bot(command_prefix="!", intents=intents_bot2)

@bot2.event
async def on_ready():
    print(f"Vouch bot bejelentkezett mint {bot2.user}")

@bot2.command(name="vouch")
async def vouch(ctx, *, text: str):
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(title="🌟 Új Vouch / Értékelés!", description=text, color=discord.Color.gold())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)

async def main():
    token1 = os.getenv("DISCORD_TOKEN")
    token2 = os.getenv("DISCORD_TOKEN_2")
    if not token1 or not token2:
        print("HIBA: Hiányzó tokenek!")
        return
    async with bot1, bot2:
        await asyncio.gather(bot1.start(token1), bot2.start(token2))

if __name__ == "__main__":
    asyncio.run(main())
