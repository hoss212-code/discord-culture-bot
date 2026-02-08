import discord
from discord.ext import commands
from utils.questions imporget_unique_question
from utils.database import add_points
from config import COLOR_PRIMARY, COLOR_ERROR, COLOR_SUCCESS, THEMES
import asyncio

class Duel(commands.Cog):
    """Multiplayer duel with Hawk mechanic - 1v1, 2v2, 3v3"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_duels = {}
    
    @commands.command(name='duel')
    async def duel(self, ctx, mode: str, *players):
        """
        Lance un duel: +duel 1v1 | +duel 2v2 @p1 @p2 @p3 | +duel 3v3 @p1-6
        Mécanique Épervier: joueurs "en prison" jusqu'à salvation par teammate
        Système de points:
        - 1 joueur correct = 2 pts
        - Tous correct = 2 × nombre de joueurs (bonus x2)
        """
        
        if mode not in ['1v1', '2v2', '3v3']:
            return await ctx.send("❌ Modes: `1v1`, `2v2`, `3v3`")
        
        embed = discord.Embed(
            title="🤝 DUEL EN ATTENTE",
            description=f"Mode: {mode}\nRejoignez le duel!",
            color=COLOR_PRIMARY
        )
        
        message = await ctx.send(embed=embed)
        # À implémenter: logique complète du duel

async def setup(bot):
    await bot.add_cog(Duel(bot))
