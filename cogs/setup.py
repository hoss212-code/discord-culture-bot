import discord
from discord.ext import commands
from discord import app_commands
from config import COLOR_PRIMARY
import json
import os

class Setup(commands.Cog):
    """Configuration commands for bot setup"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "guild_configs.json"
        self.load_configs()
    
    def load_configs(self):
        """Load guild configurations from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.configs = json.load(f)
        else:
            self.configs = {}
    
    def save_configs(self):
        """Save guild configurations to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.configs, f, indent=4)
    
    @commands.hybrid_command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """
        Configure bot settings for your server
        Allows admins to set channels, intervals, and battle royale permissions
        """
        embed = discord.Embed(
            title="⚙️ CONFIGURATION DU BOT",
            description="Configurez les paramètres du bot pour votre serveur",
            color=COLOR_PRIMARY
        )
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.configs:
            self.configs[guild_id] = {
                "battle_royale_channel": None,
                "daily_channel": None,
                "leaderboard_channel": None,
                "duel_category": None,
                "daily_interval": 24,
                "battle_royale_admins": []
            }
        
        config = self.configs[guild_id]
        
        embed.add_field(
            name="🎯 Salon Battle Royale",
            value=f"<#{config['battle_royale_channel']}" if config['battle_royale_channel'] else "Non défini",
            inline=False
        )
        embed.add_field(
            name="📅 Salon Questions Quotidiennes",
            value=f"<#{config['daily_channel']}" if config['daily_channel'] else "Non défini",
            inline=False
        )
        embed.add_field(
            name="🏆 Salon Classement",
            value=f"<#{config['leaderboard_channel']}" if config['leaderboard_channel'] else "Non défini",
            inline=False
        )
        embed.add_field(
            name="⏰ Intervalle Questions (heures)",
            value=f"{config['daily_interval']}h",
            inline=True
        )
        embed.add_field(
            name="🔒 Admins Battle Royale",
            value=f"{len(config['battle_royale_admins'])} admins",
            inline=True
        )
        
        view = SetupView(self, ctx.guild.id)
        await ctx.send(embed=embed, view=view)
    
    @commands.hybrid_command(name="set_br_channel")
    @commands.has_permissions(administrator=True)
    async def set_br_channel(self, ctx, channel: discord.TextChannel):
        """Set the Battle Royale channel"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.configs:
            self.configs[guild_id] = {}
        
        self.configs[guild_id]['battle_royale_channel'] = channel.id
        self.save_configs()
        
        await ctx.send(f"✅ Salon Battle Royale défini: {channel.mention}")
    
    @commands.hybrid_command(name="set_daily_channel")
    @commands.has_permissions(administrator=True)
    async def set_daily_channel(self, ctx, channel: discord.TextChannel):
        """Set the Daily Questions channel"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.configs:
            self.configs[guild_id] = {}
        
        self.configs[guild_id]['daily_channel'] = channel.id
        self.save_configs()
        
        await ctx.send(f"✅ Salon Questions Quotidiennes défini: {channel.mention}")
    
    @commands.hybrid_command(name="add_br_admin")
    @commands.has_permissions(administrator=True)
    async def add_br_admin(self, ctx, member: discord.Member):
        """Add a Battle Royale admin"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.configs:
            self.configs[guild_id] = {'battle_royale_admins': []}
        
        if 'battle_royale_admins' not in self.configs[guild_id]:
            self.configs[guild_id]['battle_royale_admins'] = []
        
        if member.id not in self.configs[guild_id]['battle_royale_admins']:
            self.configs[guild_id]['battle_royale_admins'].append(member.id)
            self.save_configs()
            await ctx.send(f"✅ {member.mention} ajouté comme admin Battle Royale")
        else:
            await ctx.send(f"⚠️ {member.mention} est déjà un admin Battle Royale")

class SetupView(discord.ui.View):
    def __init__(self, setup_cog, guild_id):
        super().__init__(timeout=300)
        self.setup_cog = setup_cog
        self.guild_id = str(guild_id)

async def setup(bot):
    await bot.add_cog(Setup(bot))
