
import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import load_user_data

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    leaderboard = app_commands.Group(name="leaderboard", description="Display the server leaderboard.")

    @leaderboard.command(name="balance", description="Display the server leaderboard by balance.")
    @app_commands.describe(page="The page of the leaderboard to display.")
    async def balance(self, interaction: discord.Interaction, page: int = 1):
        users = load_user_data()
        sorted_users = sorted(users.items(), key=lambda item: item[1]["balance"], reverse=True)

        items_per_page = 10
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        if page < 1:
            await interaction.response.send_message("Page number cannot be less than 1.")
            return

        if not sorted_users:
            embed = discord.Embed(title="Leaderboard - Balance", description="The leaderboard is empty!", color=discord.Color.gold())
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(title="Leaderboard - Balance", color=discord.Color.gold())

        for i, (user_id, data) in enumerate(sorted_users[start_index:end_index]):
            try:
                user = await self.bot.fetch_user(int(user_id))
                embed.add_field(name=f"#{start_index + i + 1} - {user.name}", value=f"${data['balance']}", inline=False)
            except discord.NotFound:
                embed.add_field(name=f"#{start_index + i + 1} - *Unknown User*", value=f"${data['balance']}", inline=False)

        total_pages = ((len(sorted_users) - 1) // items_per_page) + 1
        embed.set_footer(text=f"Page {page}/{total_pages}")
        await interaction.response.send_message(embed=embed)

    @leaderboard.command(name="fish", description="Display the server leaderboard by fish caught.")
    @app_commands.describe(page="The page of the leaderboard to display.")
    async def fish(self, interaction: discord.Interaction, page: int = 1):
        users = load_user_data()
        sorted_users = sorted(users.items(), key=lambda item: len(item[1]["fish"]), reverse=True)

        items_per_page = 10
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        if page < 1:
            await interaction.response.send_message("Page number cannot be less than 1.")
            return

        if not sorted_users:
            embed = discord.Embed(title="Leaderboard - Fish", description="The leaderboard is empty!", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(title="Leaderboard - Fish", color=discord.Color.blue())

        for i, (user_id, data) in enumerate(sorted_users[start_index:end_index]):
            try:
                user = await self.bot.fetch_user(int(user_id))
                embed.add_field(name=f"#{start_index + i + 1} - {user.name}", value=f"{len(data['fish'])} fish", inline=False)
            except discord.NotFound:
                embed.add_field(name=f"#{start_index + i + 1} - *Unknown User*", value=f"{len(data['fish'])} fish", inline=False)

        total_pages = ((len(sorted_users) - 1) // items_per_page) + 1
        embed.set_footer(text=f"Page {page}/{total_pages}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))
