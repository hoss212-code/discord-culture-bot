import discord
from discord.ext import commands, tasks
from utils.questions imporget_unique_question
from config import THEMES, COLOR_PRIMARY
import asyncio

class DailyQuiz(commands.Cog):
    """Daily quiz send one question to a designated channel at regular intervals"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_sessions = {}
        self.daily_task.start()
    
    @commands.hybrid_command(name="daily", description="Start daily question session")
    @commands.has_permissions(administrator=True)
    async def start_daily(self, ctx):
        """Configure daily questions for a channel"""
        embed = discord.Embed(
            title="🤔 QUIZ QUOTIDIEN - Configuration",
            description="Interval?s disponibles: 12h ou 24h",
            color=COLOR_PRIMARY
        )
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="12 heures", custom_id="daily_12h"))
        view.add_item(discord.ui.Button(label="24 heures", custom_id="daily_24h"))
        
        await ctx.send(embed=embed, view=view)
    
    @tasks.loop(hours=24)
    async def daily_task(self):
        """Send daily question to all active channels"""
        if not self.active_sessions:
            return
        
        for channel_id, config in self.active_sessions.items():
            try:
                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    continue
                
                questionget_unique_question(mode='daily', guild_id=channel.guild.id)
                if question is None:
                    continue
                
                embed = discord.Embed(
                    title="🃄 Question du jour!",
                    description=question["question"],
                    color=COLOR_PRIMARY
                )
                embed.add_field(name="Théme", value=question["theme"], inline=False)
                
                # Add answer buttons
                view = discord.ui.View()
                for idx, answer in enumerate(question["options"]):
                    view.add_item(
                        discord.ui.Button(
                            label=answer,
                            custom_id=f"daily_answer_{idx}",
                            style=discord.ButtonStyle.primary
                        )
                    )
                
                msg = await channel.send(embed=embed, view=view)
                await msg.pin()
                
            except Exception as e:
                print(f"Error in daily task: {e}")
    
    @daily_task.before_loop
    async def before_daily(self):
        """Wait for bot to be ready"""
        await self.bot.wait_until_ready()
    
    async def cog_unload(self):
        """Cancel task on unload"""
        self.daily_task.cancel()

async def setup(bot):
    await bot.add_cog(DailyQuiz(bot))
