import disnake
from disnake.ext import commands
import config
from supabase import Client, create_client
import os

class Close_Ticket(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            label="Close Ticket", emoji="🔴", custom_id="c_ticket"
        )
    
    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.channel.delete()

class Open_Ticket(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            label="Open Ticket", emoji="🎫", custom_id="o_ticket"
        )
    
    async def callback(self, interaction: disnake.MessageInteraction):

        await interaction.response.send_message("Please wait..!", ephemeral=True)

        ticket_category = disnake.utils.get(interaction.user.guild.categories, id=config.ticketcat_id)

        f = open("ticket_no.txt", "rt")

        ticket_no = int(f.read())

        f.close()

        ticket_channel = await ticket_category.create_text_channel(f"Ticket-{ticket_no}")

        await ticket_channel.set_permissions(interaction.user, view_channel=True, send_messages=True)

        await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False, send_messages=False)

        f = open("ticket_no.txt", "w")

        f.write(str(ticket_no + 1))

        f.close()

        await interaction.edit_original_message(f"Created ticket {ticket_channel.mention}, please write your reason for opening the ticket in that channel!")

        embed = disnake.Embed(title=f"We are coming! (Ticket no. {ticket_no})", description="Please wait, one of our support staffs will eventually get in contact with you!")

        view = disnake.ui.View()

        view.add_item(Close_Ticket())

        await ticket_channel.send(interaction.user.mention, embed=embed, view=view)

class TicketCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def ticket(self, inter: disnake.ApplicationCommandInteraction):
        
        if inter.user.id != config.owner_id:
            await inter.response.send_message("You do not have the permission to run this command!", ephemeral=True)
            return
        
        embed = disnake.Embed(
            title="Open a ticket!",
            description="Open a ticket if you want to report, support regarding your product or if you want to hire me for work!",
            color=660000
        )

        view = disnake.ui.View()

        view.add_item(Open_Ticket())
        
        await inter.response.send_message(embed=embed, view=view)

def setup(bot: commands.Bot):
    bot.add_cog(TicketCommand(bot))