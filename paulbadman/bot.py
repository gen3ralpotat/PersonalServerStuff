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

    Bot Events

"""


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(message):
    # Dont respond to own message
    if message.author == bot.user:
        return
    # If someone pings
    if bot.user.mentioned_in(message):
        servercount = str(len(bot.guilds))
        await message.channel.send(f"Hey, I am Paul Badman, law representative of this server! You know, folks, I'm not just in one or two servers, oh no! I'm spreading across a {servercount} servers! That's right, {servercount}! I'm like the multi-server maestro, making sure I'm everywhere you need me to be, a {servercount} times over!")
    # check for other triggers
    result = check_for_triggers(message.content)
    if result:
        await message.channel.send(result)

"""

    Run the bot

"""


bot.run('')
