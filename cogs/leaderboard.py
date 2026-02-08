import discord
from discord.ext import commands
from utils.database import get_top_players, get_user_stats
from config import COLOR_SUCCESS, COLOR_PRIMARY
import asyncio

class Leaderboard(commands.Cog):
    """Leaderboard system to display player rankings and stats"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="leaderboard", aliases=["lb", "top"])
    async def leaderboard(self, ctx, scope: str = "global"):
        """
        Display the leaderboard
        
        Args:
            scope: "global" for all players or "server" for guild only
        """
        if scope == "server":
            players = get_top_players(guild_id=ctx.guild.id, limit=10)
            title = f"🏆 CLASSEMENT - {ctx.guild.name}"
        else:
            players = get_top_players(limit=10)
            title = "🏆 CLASSEMENT GLOBAL"
        
        if not players:
            await ctx.send("❌ Aucun joueur dans le classement pour le moment!")
            return
        
        embed = discord.Embed(
            title=title,
            color=COLOR_SUCCESS
        )
        
        medals = ["🥇", "🥈", "🥉"]
        
        description = ""
        for idx, player in enumerate(players):
            medal = medals[idx] if idx < 3 else f"`{idx+1}.`"
            user = await self.bot.fetch_user(player['user_id'])
            username = user.name if user else "Utilisateur inconnu"
            
            description += f"{medal} **{username}**\n"
            description += f"    • Points: {player['points']} | Victoires: {player['wins']}\n"
        
        embed.description = description
        embed.set_footer(text="Utilisez /stats pour voir vos statistiques personnelles")
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="stats")
    async def stats(self, ctx, member: discord.Member = None):
        """
        Display stats for a user
        
        Args:
            member: The member to check stats for (defaults to command user)
        """
        target = member or ctx.author
        
        stats = get_user_stats(target.id, ctx.guild.id)
        
        if not stats:
            await ctx.send(f"❌ Aucune statistique disponible pour {target.name}")
            return
        
        embed = discord.Embed(
            title=f"📊 Statistiques de {target.name}",
            color=COLOR_PRIMARY
        )
        
        embed.add_field(
            name="Points totaux",
            value=f"🎯 {stats['points']}",
            inline=True
        )
        embed.add_field(
            name="Victoires",
            value=f"✅ {stats['wins']}",
            inline=True
        )
        embed.add_field(
            name="Défaites",
            value=f"❌ {stats['losses']}",
            inline=True
        )
        
        total_games = stats['wins'] + stats['losses']
        winrate = (stats['wins'] / total_games * 100) if total_games > 0 else 0
        
        embed.add_field(
            name="Parties jouées",
            value=f"🎮 {total_games}",
            inline=True
        )
        embed.add_field(
            name="Taux de victoire",
            value=f"📈 {winrate:.1f}%",
            inline=True
        )
        embed.add_field(
            name="Rang",
            value=f"🏅 #{stats.get('rank', 'N/A')}",
            inline=True
        )
        
        embed.set_thumbnail(url=target.display_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
