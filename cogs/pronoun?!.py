import discord
from discord import app_commands, Embed
from discord.ext import commands

import time 

roleDict = {
#   Internal ID - Role ID - Human readable pronoun
    "she1": [919712351870140456, "she"],
    "they1": [1047416277339230248, "they"],
    "he1": [919712259461230713, "he"],
    "she2": [1047516866911948822, "she"],
    "they2": [919712390357057538, "they"],
    "he2": [1047516928589180948, "he"],
    "she3": [1047516960486871050, "she"],
    "all": [1047517002832556154, "all"],
    "any": [919712423873773619, "any"],
    "ask": [919712464592056341, "ask me"],
}

roleIDs = [
    919712351870140456,
    1047416277339230248,
    919712259461230713,
    1047516866911948822,
    919712390357057538,
    1047516928589180948,
    1047516960486871050,
    919712423873773619,
    1047517002832556154,
    919712464592056341,
]

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

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "Exit"
        self.stop()


class pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def stuff(self, interaction, phase, pronouns):
        embed = Embed()
        embed.title = f"Please select your **{phase}** pronouns"
        thing = [
            "primary pronoun:",
            "secondary pronoun:",
        ]
        # add your prefered pronouns to the embed
        for i, pronoun in enumerate(pronouns):
            embed.add_field(name=thing[i], value=pronoun, inline=False)

        # reset the loaded prounouns
        view = roles()

        # remove selected pronouns from the list of available ones 
        for i in pronouns:
            for i, child in enumerate(view.children):
                if child.label in pronouns:
                    view.remove_item(view.children[i])
                    break
        
        # if it the first time looping you have to send the message before being able to edit it
        if phase == "primary":
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.edit_original_response(embed=embed, view=view)

        # await an answer
        await view.wait()
        if view.value is None:
            await interaction.edit_original_response("sorry, you timed out")
        else:
            pronouns.append(view.value)
        return pronouns

    @app_commands.command(name = "pronouns", description = "omg you use pronouns too?!")
    async def nya(self, interaction: discord.Interaction):
        pronouns = []

        pronouns = await self.stuff(interaction, "primary", pronouns)
        if "Exit" not in pronouns and "Any" not in pronouns and "All" not in pronouns and "Ask me" not in pronouns:
            pronouns = await self.stuff(interaction, "secondary", pronouns)
        if "Exit" not in pronouns and "Any" not in pronouns and "All" not in pronouns and "Ask me" not in pronouns:
            pronouns = await self.stuff(interaction, "tertiary", pronouns)
        
        # remove the "exit" pronoun if present
        if "Exit" in pronouns:
            pronouns.pop(len(pronouns)-1)
        
        # if you just pressed exit, exit the command
        if len(pronouns) == 0:
            return
        
        embed = Embed()
        embed.title = f"Your prefered pronouns"
        thing = [
            "primary pronouns:",
            "secondary pronouns:",
            "tertiary pronouns:",
        ]
        # list the prefered pronouns in the embed
        for i, pronoun in enumerate(pronouns):
            embed.add_field(name=thing[i], value=pronoun, inline=False)

        await interaction.edit_original_response(embed=embed, view=discord.ui.View())

        rolesToGiveOut = []
        rolesToRemove = []

        for i in roleIDs:
            rolesToRemove.append(i)

        for i in pronouns:
            for j in roleDict:
                if roleDict[j][1] == i.split("/")[0].lower():
                    rolesToGiveOut.append(roleDict[j][0])
                    break
  
        for i in rolesToGiveOut:
            for n, j in enumerate(rolesToRemove):
                if i == j:
                    print(f"{rolesToRemove[n]} go pop")
                    rolesToRemove.pop(n)
                    break
    
        roles = tuple(discord.utils.get(interaction.guild.roles, id=i) for i in roleIDs)
        await interaction.user.remove_roles(*roles)

        roles = tuple(discord.utils.get(interaction.guild.roles, id=i) for i in rolesToGiveOut)
        await interaction.user.add_roles(*roles)
        print("a")
        await interaction.edit_original_response("your roles have been updated!")

            

    
async def setup(bot):
    await bot.add_cog(pronouns(bot))#, guilds = [discord.Object(id = 1016777760305320036)])
