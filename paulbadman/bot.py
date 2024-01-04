import discord
from discord.ext import commands
import botconstants
from programmed_responses import check_for_triggers

"""

    Bot Configs

"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=botconstants.COMMAND_PREFIX,
                   description=botconstants.BOT_DESCRIPTION, intents=intents)

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
    async def rights(self, ctx):
        await ctx.send(botconstants.RIGHTS)


"""

    Bot commands

    Category: Attachments

"""


"""

    Bot Events

"""


@bot.event
async def on_ready():
    await bot.add_cog(Funny(bot))
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

bot.run('')
