import discord
from discord.ext import commands, tasks
import os
from config import BOT_TOKEN, BOT_PREFIX
from utils.database import init_database
from utils.questions import load_questions

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Initialize database
    await init_database()
    
    # Load questions
    await load_questions()
    
    # Load cogs
    await load_cogs()
    
    print('Bot is fully loaded!')

async def load_cogs():
    """Load all cogs from cogs directory"""
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
        return
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                cog_name = filename[:-3]
                await bot.load_extension(f'cogs.{cog_name}')
                print(f'Loaded cog: {cog_name}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')

@bot.command()
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
