import discord
from discord.ext import commands
import botconstants
import save_attachment
from programmed_responses import check_for_triggers

"""

    Bot Configs

"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=botconstants.COMMAND_PREFIX, description=botconstants.BOT_DESCRIPTION, intents=intents)

"""

    Bot Commands

    Category: Funny
"""
class Funny(commands.Cog):
    """
    
        Funny

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rights(self,ctx):
        await ctx.send(botconstants.RIGHTS)

"""

    Bot commands

    Category: Attachments

"""
class Attachments(commands.Cog):
    """
    
        Commands for Saving Attachments

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def howsave(self,ctx : commands.Context):
        await ctx.send(f"{ctx.author.mention} this how https://media.discordapp.net/attachments/910216279212834907/1186815470691700877/image.png?ex=65949f0a&is=65822a0a&hm=79ee2a37b8a4f90a65c3d1588a418143e44001600f2af0c8aad7059aaf6c15f8&=&format=webp&quality=lossless&width=607&height=687")


    @commands.command()
    async def save(self,ctx : commands.Context, name : str):
        await ctx.send(save_attachment.add_attachment(ctx,name))


    @commands.command()
    async def get(self,ctx : commands.Context, name : str):
        await ctx.send(await save_attachment.get_attachment(ctx,name))

    @commands.command()
    async def la(self,ctx : commands.Context):
        await ctx.send(save_attachment.list_saved(ctx))

"""

    Bot Events

"""
@bot.event
async def on_ready():
    await bot.add_cog(Funny(bot))
    await bot.add_cog(Attachments(bot))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    result = check_for_triggers(message.content)
    if result:
        await message.channel.send(result)  

    


"""

    Run the bot

"""

bot.run('MTExMjkyMDA2NDM3MTQ2NjI4MQ.Gq599P.LIRLrHqV9l25uVR0mZO1gb0R7VtnZFjt0gVI6U')