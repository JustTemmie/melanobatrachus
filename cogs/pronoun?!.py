import discord
from discord import app_commands, Embed
from discord.ext import commands

import time 

class roles(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="He/Him", style=discord.ButtonStyle.grey)
    async def he(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "He/Him"
        self.stop()

    @discord.ui.button(label="She/Her", style=discord.ButtonStyle.grey)
    async def she(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "She/Her"
        self.stop()
    
    @discord.ui.button(label="They/Them", style=discord.ButtonStyle.grey)
    async def they(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "They/Them"
        self.stop()
    
    @discord.ui.button(label="Any", style=discord.ButtonStyle.grey)
    async def any(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "Any"
        self.stop()

    @discord.ui.button(label="All", style=discord.ButtonStyle.grey)
    async def all(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "All"
        self.stop()

    @discord.ui.button(label="Ask me", style=discord.ButtonStyle.grey)
    async def ask(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "Ask me"
        self.stop()
    
    @discord.ui.button(label="Neo", style=discord.ButtonStyle.grey)
    async def neo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "Neo"
        self.stop()
    
    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "Exit"
        self.stop()





class pronoun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def stuff(self, interaction, phase, pronouns):
        embed = Embed()
        embed.title = f"Please select your **{phase}** pronouns"
        thing = [
            "primary pronoun:",
            "secondary pronoun:",
            "tertiary pronoun:",
            "quaternary pronoun:",
        ]
        for i, pronoun in enumerate(pronouns):
            embed.add_field(name=thing[i], value=pronoun, inline=False)

        view = roles()

        for i in pronouns:
            for i, child in enumerate(view.children):
                if child.label in pronouns:
                    view.remove_item(view.children[i])
                    break

        if phase == "primary":
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.edit_original_response(embed=embed, view=view)
        await view.wait()
        if view.value is None:
            print('Timed out...')
        else:
            pronouns.append(view.value)
        return pronouns

    @app_commands.command(name = "pronouns", description = "omg you use pronouns too?!")
    async def nya(self, interaction: discord.Interaction):
        print("test")
        pronouns = []

        currentPronoun = 1

        pronouns = await self.stuff(interaction, "primary", pronouns)
        if "Exit" not in pronouns:
            pronouns = await self.stuff(interaction, "secondary", pronouns)
        if "Exit" not in pronouns:
            pronouns = await self.stuff(interaction, "tertiary", pronouns)
        if "Exit" not in pronouns:
            pronouns = await self.stuff(interaction, "quaternary", pronouns)
        
        if "Exit" in pronouns:
            pronouns.pop(len(pronouns)-1)
        
        if len(pronouns) == 0:
            return
        
        embed = Embed()
        embed.title = f"Your prefered pronouns"
        thing = [
            "primary pronouns:",
            "secondary pronouns:",
            "tertiary pronouns:",
            "quaternary pronouns:",
        ]
        for i, pronoun in enumerate(pronouns):
            embed.add_field(name=thing[i], value=pronoun, inline=False)

        await interaction.edit_original_response(embed=embed, view=discord.ui.View())
        

    
async def setup(bot):
    await bot.add_cog(pronoun(bot), guilds = [discord.Object(id = 1016777760305320036)])
