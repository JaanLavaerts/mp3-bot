import discord
from discord.ext import commands
from config import TOKEN
from commands import hello, mp3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_command(hello)
bot.add_command(mp3)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

if __name__ == "__main__":
    bot.run(TOKEN)