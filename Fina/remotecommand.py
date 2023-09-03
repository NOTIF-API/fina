
import discord
import asyncio
from bot import bot
from bot import irh

async def BotPresense(name):
    """"""
    await bot.change_presence(activity=discord.Game(name=name))

while True:
    command = input("Wait command: ", )
    splited: list = command.split(' ')
    if splited[0] == "bot" and splited[1] == "name":
        splited.remove("bot")
        splited.remove("name")
        result = ""
        for i in splited:
            result += i + " "
        asyncio.run(BotPresense(result))
    if splited[0] == "bot" and splited[1] == "exit":
        irh.exit_from_program()