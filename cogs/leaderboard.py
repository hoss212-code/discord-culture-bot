import discord
from discord.ext import commands, tasks
from utils.database import get_top_players_by_mode, get_user_stats
from config import COLOR_SUCCESS, COLOR_PRIMARY
import asyncio
import json
import os

class Leaderboard(commands.Cog):
    """Système de classement avec mise à jour automatique"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "guild_configs.json"
        self.leaderboard_messages = {}  # {guild_id: message_id}
        self.load_configs()
        self.update_leaderboards.start()
    
    def load_configs(self):
        """Charger les configurations"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.configs = json.load(f)
        else:
            self.configs = {}
    
    @tasks.loop(minutes=5)  # Refresh toutes les 5 minutes (optimal)
    async def update_leaderboards(self):
        """Mise à jour automatique des classements"""
        for guild_id, config in self.configs.items():
            if 'leaderboard_channel' not in config or not config['leaderboard_channel']:
                continue
            
            try:
                guild = self.bot.get_guild(int(guild_id))
                if not guild:
                    continue
                
                channel = guild.get_channel(config['leaderboard_channel'])
                if not channel:
                    continue
                
                embed = await self.create_leaderboard_embed(guild)
                
                # Récupérer ou créer le message
                if guild_id in self.leaderboard_messages:
                    try:
                        msg = await channel.fetch_message(self.leaderboard_messages[guild_id])
                        await msg.edit(embed=embed)
                    except:
                        # Message supprimé, en créer un nouveau
                        msg = await channel.send(embed=embed)
                        self.leaderboard_messages[guild_id] = msg.id
                else:
                    msg = await channel.send(embed=embed)
                    self.leaderboard_messages[guild_id] = msg.id
                    
            except Exception as e:
                print(f"Erreur lors de la mise à jour du classement pour {guild_id}: {e}")
    
    @update_leaderboards.before_loop
    async def before_update(self):
        """Attendre que le bot soit prêt"""
        await self.bot.wait_until_ready()
    
    async def create_leaderboard_embed(self, guild):
        """Créer l'embed avec 4 colonnes de classement"""
        embed = discord.Embed(
            title="🏆 CLASSEMENT GLOBAL",
            description=f"Mis à jour automatiquement toutes les 5 minutes",
            color=COLOR_SUCCESS
        )
        
        # Récupérer les tops par mode
        top_br = get_top_players_by_mode(guild.id, "battle_royale", limit=5)
        top_daily = get_top_players_by_mode(guild.id, "daily", limit=5)
        top_multi = get_top_players_by_mode(guild.id, "multiplayer", limit=5)
        top_general = get_top_players_by_mode(guild.id, "general", limit=5)
        
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        # Colonne 1: Battle Royale
        br_text = "\n".join([
            f"{medals[i]} {await self.get_username(p['user_id'])} - {p['points']}pts"
            for i, p in enumerate(top_br)
        ]) if top_br else "*Aucun joueur*"
        embed.add_field(name="💥 Battle Royale", value=br_text, inline=True)
        
        # Colonne 2: Daily Quiz
        daily_text = "\n".join([
            f"{medals[i]} {await self.get_username(p['user_id'])} - {p['points']}pts"
            for i, p in enumerate(top_daily)
        ]) if top_daily else "*Aucun joueur*"
        embed.add_field(name="📅 Daily Quiz", value=daily_text, inline=True)
        
        # Colonne 3: Multiplayer
        multi_text = "\n".join([
            f"{medals[i]} {await self.get_username(p['user_id'])} - {p['points']}pts"
            for i, p in enumerate(top_multi)
        ]) if top_multi else "*Aucun joueur*"
        embed.add_field(name="⚔️ Multiplayer", value=multi_text, inline=True)
        
        # Ligne de séparation invisible pour forcer la 4ème colonne en bas
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        
        # Colonne 4: Classement Général (moyenne de tout)
        general_text = "\n".join([
            f"{medals[i]} {await self.get_username(p['user_id'])} - {p['avg_points']:.0f}pts (moy)"
            for i, p in enumerate(top_general)
        ]) if top_general else "*Aucun joueur*"
        embed.add_field(name="🎯 Classement Général", value=general_text, inline=False)
        
        embed.set_footer(text=f"⏱️ Dernière mise à jour")
        embed.timestamp = discord.utils.utcnow()
        
        return embed
    
    async def get_username(self, user_id):
        """Récupérer le nom d'utilisateur"""
        try:
            user = await self.bot.fetch_user(user_id)
            return user.name
        except:
            return "Utilisateur inconnu"
    
    @commands.hybrid_command(name="leaderboard", aliases=["lb", "top"])
    async def leaderboard_command(self, ctx, scope: str = "global"):
        """
        Afficher le classement
        
        Args:
            scope: "global" pour tous les joueurs ou "server" pour le serveur uniquement
        """
        embed = await self.create_leaderboard_embed(ctx.guild)
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="stats")
    async def stats(self, ctx, member: discord.Member = None):
        """
        Afficher les statistiques d'un joueur
        
        Args:
            member: Le membre à vérifier (par défaut: vous)
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
            value=f"🎯 {stats.get('total_points', 0)}",
            inline=True
        )
        embed.add_field(
            name="Victoires",
            value=f"✅ {stats.get('wins', 0)}",
            inline=True
        )
        embed.add_field(
            name="Défaites",
            value=f"❌ {stats.get('losses', 0)}",
            inline=True
        )
        
        # Stats par mode
        embed.add_field(
            name="💥 Battle Royale",
            value=f"{stats.get('br_points', 0)} pts",
            inline=True
        )
        embed.add_field(
            name="📅 Daily Quiz",
            value=f"{stats.get('daily_points', 0)} pts",
            inline=True
        )
        embed.add_field(
            name="⚔️ Multiplayer",
            value=f"{stats.get('multi_points', 0)} pts",
            inline=True
        )
        
        total_games = stats.get('wins', 0) + stats.get('losses', 0)
        winrate = (stats.get('wins', 0) / total_games * 100) if total_games > 0 else 0
        
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
    
    @commands.hybrid_command(name="force_update_leaderboard")
    @commands.has_permissions(administrator=True)
    async def force_update(self, ctx):
        """Forcer la mise à jour du classement (Admin uniquement)"""
        await ctx.send("🔄 Mise à jour du classement...")
        await self.update_leaderboards()
        await ctx.send("✅ Classement mis à jour!")
    
    async def cog_unload(self):
        """Arrêter la boucle lors du déchargement"""
        self.update_leaderboards.cancel()

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
