import discord
from discord.ext import commands
from utils.questions imporget_unique_question
from utils.database import add_points
from config import COLOR_PRIMARY, COLOR_ERROR, COLOR_SUCCESS
import asyncio
import random

class BattleRoyale(commands.Cog):
    """Battle Royale game mode - Tous contre tous"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
    
    @commands.command(name='battle-royale', aliases=['br'])
    @commands.has_permissions(administrator=True)
    async def battle_royale(self, ctx):
        """Lance une partie de Battle Royale (Admin only)"""
        
        if ctx.guild.id in self.active_games:
            return await ctx.send(embed=discord.Embed(
                title="⚠️ Partie en cours",
                description="Une partie de Battle Royale est déjà en cours",
                color=COLOR_ERROR
            ))
        
        # Création de l'embed d'invitation
        embed = discord.Embed(
            title="⚔️ BATTLE ROYALE",
            description="Réagis avec ✅ pour participer!\n10 questions, élimination progressive",
            color=COLOR_PRIMARY
        )
        embed.add_field(name="Participants", value="En attente...", inline=False)
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        
        # Attendre les réactions
        await asyncio.sleep(30)
        
        # Récupérer les participants
        message = await ctx.channel.fetch_message(message.id)
        players = set()
        
        for reaction in message.reactions:
            if reaction.emoji == "✅":
                async for user in reaction.users():
                    if not user.bot:
                        players.add(user)
        
        if len(players) < 2:
            return await ctx.send("❌ Pas assez de participants (min 2)")
        
        # Lancer le jeu
        await ctx.send(f"🎮 La partie commence avec {len(players)} joueurs!")
        self.active_games[ctx.guild.id] = True
        
        # À implémenter: logique du jeu
        
        del self.active_games[ctx.guild.id]

async def setup(bot):
    await bot.add_cog(BattleRoyale(bot))
