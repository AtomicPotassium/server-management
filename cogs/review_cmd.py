import disnake
from disnake.ext import commands
import config
from supabase import Client, create_client
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class ReviewCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def review(self, inter: disnake.ApplicationCommandInteraction, title: str, description: str, star: int):
        
        if inter.user.id != config.owner_id:
            await inter.response.send_message("You do not have the permission to run this command!", ephemeral=True)
            return
        
        if star > 5 or star < 1:
            await inter.response.send_message("A range of 1-5 is allowed in stars!", ephemeral=True)
            return

        mongodb_client = MongoClient(os.environ["M_URL"])

        db = mongodb_client["AT_POT"]
        
        review = db.get_collection("reviews")

        user_data = review.find_one({"_id": inter.user.id})

        if not user_data:
            review.insert_one({"_id": inter.user.id, "points": 0})
            user_data = review.find_one({"_id": inter.user.id})

        if user_data["points"] == 0:
            await inter.response.send_message("You don't have enough points to leave a review!", ephemeral=True)
            return

        review_channel = inter.guild.get_channel(config.review_id)

        embed = disnake.Embed(title=title, description=description)

        stars_str = ""

        for _ in range(0, star):
            stars_str = stars_str + "⭐"

        embed.add_field(name="Stars (out of 5):", value=stars_str)

        review.update_one({"_id": inter.user.id}, {"$set": {"points": user_data["points"] - 1}})

        await review_channel.send(inter.user.mention, embed=embed)

        await inter.response.send_message("Thank you for your review!", ephemeral=True)

    @commands.slash_command()
    async def add_review_points(self, inter: disnake.ApplicationCommandInteraction, user: disnake.user.User, amount: int):
        
        if inter.user.id != config.owner_id:
            await inter.response.send_message("You do not have the permission to run this command!", ephemeral=True)
            return
        
        embed = disnake.Embed(
            title="Open a ticket!",
            description="Open a ticket if you want to report, support regarding your product or if you want to hire me for work!",
            color=660000
        )

        mongodb_client = MongoClient(os.environ["M_URL"])

        db = mongodb_client["AT_POT"]
        
        review = db.get_collection("reviews")

        exists = review.find_one({"_id": user.id})

        if not exists:
            review.insert_one({"_id": user.id, "points": 0})
            exists = review.find_one({"_id": user.id})

        review.update_one({"_id": user.id}, {"$set": {"points": exists["points"] + amount}})

        await inter.response.send_message(f"Changed {inter.user.mention}'s point from {exists["points"]} to {exists["points"] + amount}!")

    @commands.slash_command()
    async def sub_review_points(self, inter: disnake.ApplicationCommandInteraction, user: disnake.user.User, amount: int):
        
        if inter.user.id != config.owner_id:
            await inter.response.send_message("You do not have the permission to run this command!", ephemeral=True)
            return

        mongodb_client = MongoClient(os.environ["M_URL"])

        db = mongodb_client["AT_POT"]
        
        review = db.get_collection("reviews")

        exists = review.find_one({"_id": user.id})

        if not exists:
            review.insert_one({"_id": user.id, "points": 0})
            exists = review.find_one({"_id": user.id})

        if exists["points"] == 0:
            await inter.response.send_message("The user has no review points!", ephemeral=True)
            return

        if exists["points"] - amount < 0:
            review.update_one({"_id": user.id, "points": 0})
            await inter.response.send_message(f"Changed {inter.user.mention}'s point from {exists["points"]} to 0!", ephemeral=True)
            return
        else:
            review.update_one({"_id": user.id}, {"$set": {"points": exists["points"] - amount}})
            await inter.response.send_message(f"Changed {inter.user.mention}'s point from {exists["points"]} to {exists["points"] - amount}!", ephemeral=True)
            return
        

    @commands.slash_command()
    async def see_points(self, inter: disnake.ApplicationCommandInteraction, user: disnake.user.User):
        
        if inter.user.id != config.owner_id:
            await inter.response.send_message("You do not have the permission to run this command!", ephemeral=True)
            return

        mongodb_client = MongoClient(os.environ["M_URL"])

        db = mongodb_client["AT_POT"]
        
        review = db.get_collection("reviews")

        exists = review.find_one({"_id": user.id})

        if not exists:
            review.insert_one({"_id": user.id, "points": 0})
            exists = review.find_one({"_id": user.id})
        
        await inter.response.send_message(f"{user.mention} currently has: {exists["points"]} review points!", ephemeral=True)
        

def setup(bot: commands.Bot):
    bot.add_cog(ReviewCommand(bot))