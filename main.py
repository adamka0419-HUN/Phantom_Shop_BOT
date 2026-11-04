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
    print(f"Shop/Ticket bot sikeresen bejelentkezett mint {bot1.user}")

# --- ÖSSZES CSATORNA ÉS KATEGÓRIA TÖRLÉSE (!clear_all) ---
@bot1.command(name="clear_all")
@commands.has_permissions(administrator=True)
async def clear_all(ctx):
    guild = ctx.guild
    await ctx.send("⚠️ *Minden csatorna és kategória törlése folyamatban...*", delete_after=5)

    try:
        # Először töröljük az összes csatornát
        for channel in guild.channels:
            try:
                await channel.delete()
            except Exception as e:
                print(f"Nem sikerült törölni a csatornát ({channel.name}): {e}")

        print("Minden csatorna sikeresen törölve!")
    except Exception as e:
        print(f"Hiba történt a törlés során: {e}")

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
        print("HIBA: A DISCORD_TOKEN vagy a `DISCORD_TOKEN_2` nincs beállítva a környezeti változók között!")
        return

    async with bot1, bot2:
        await asyncio.gather(
            bot1.start(token1),
            bot2.start(token2)
        )

if __name__ == "__main__":
    asyncio.run(main())
