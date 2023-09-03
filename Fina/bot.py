from typing import Any, Coroutine
from discord import app_commands
import discord
from discord.ext import commands
import json
import threading
import time
from discord import User
import psutil

mydict = json.load(open("Configs.json"))
botcgf = mydict.get("bot")

class Clients(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.Synchronized = False
    
    async def on_ready(self):
        if self.Synchronized:
            pass
        else:
            a = await tree.sync()
            print(a)
            self.Synchronized = True
            self.Start_background_task()
            
    def _Task(self):
        """"""
        while True:
            active: int = len(super().guilds)
            if active != 2:
                quit(code=2)
            time.sleep(5)
    def Start_background_task(self):
        """"""
        self.process = threading.Thread(target=self._Task)
        self.process.start()
    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        return await super().on_error(event_method, *args, **kwargs)

class Promotion:
    def __init__(self, path):
        self.Path = path
    def CheckMember(self, userid, AmountNewPoints):
        """"""
        a = json.load(open(self.Path))
        if not str(userid) in a:
            return "db-1"
        if str(userid) in a:
            b: str = str(userid)
            out = f"# Таблица рангов\nМл.Администратор - больше 750 очков\nАдминистратор - больше 1500 очков\nСт.Администратор - больше 2250 очков\n## Пользователь <@{userid}>\nТекущий статус: {a[b]['Status']}\nТекущие очки: {a[b]['Points'] + AmountNewPoints}"
            return out
    def GetPoints(self, userid):
        """"""
        a = json.load(open(self.Path))
        if not str(userid) in a:
            return "db-1"
        if str(userid) in a:
            b: str = str(userid)
            out: discord.Embed = discord.Embed(title="Информация о ранге", description=f"# Пользователь <@{userid}>\nОчки: {a[b]['Points']}\nСтатус: {a[b]['Status']}\n# Таблица рангов\nМл.Администратор - больше 750 очков\nАдминистратор - больше 1500 очков\nСт.Администратор - больше 2250 очков\n### Несоотвестивие\nесли количество очков не совподает с рангом предупредите об этом NOTIF#1506", color=0xff0000)
            return out
    def RemovePoint(self, userid, amount):
        """"""
        a = json.load(open(self.Path))
        user: str = str(userid)
        if not user in a:
            return "db-1"
        if user in a:
            a[user]["Points"] -= amount
            json.dump(a, open(self.Path, "w"), indent=3)
            return "done"
    def IsAdmin(self, userid):
        """"""
        a = json.load(open(self.Path))
        if not str(userid) in a:
            return False
        if str(userid) in a:
            return True
        else:
            return "hz ia ebal"
    def IsOwner(self, userid):
        """"""
        a = json.load(open(self.Path))
        if not str(userid) in a:
            return False
        if str(userid) in a:
            if a[str(userid)]["Status"] == "owner [Nya]":
                return True
            else:
                return False

prs = Promotion("Admins.json")
client = Clients()
tree = app_commands.tree.CommandTree(client=client)

@tree.command(name="turn", description="Позволяет отключить бота")
@commands.has_permissions(administrator=True)
async def turn(interaction: discord.Integration, commnd: str):
    """"""
    if prs.IsOwner(interaction.user.id):
        if commnd == "off" and str(interaction.user.id) == "582158218310975499":
            await interaction.response.send_message("Выключаем бота ожидайте исход действия в течение времени", ephemeral=True)
            quit(code=1)
        if commnd == "on":
            await interaction.response.send_message("Событие не произойдет из за её безполезности", ephemeral=True)
        else:
            await interaction.response.send_message("Некоректный ввод каманды мы принимаем off/on каманду\nили вы не создатель бота", ephemeral=True)
            return
    if prs.IsAdmin(interaction.user.id):
        await interaction.response.send_message("иди нахуй", ephemeral=True)

@tree.command(name="allow", description="добовление админа в базу данных")
@commands.has_permissions(administrator=True)
async def allow(interaction: discord.Integration, member: discord.Member):
    """"""
    readed = json.load(open("Admins.json"))
    if prs.IsOwner(interaction.user.id):
        if str(member.id) in readed:
            await interaction.response.send_message("данный игрок уже есть в базе", ephemeral=True)
        if not str(member.id) in readed:
            readed[str(member.id)] = {}
            readed[str(member.id)]["Name"] = member.name
            readed[str(member.id)]["Points"] = 0
            readed[str(member.id)]["Status"] = "helper"
            json.dump(readed, open("Admins.json", "w"), indent=3)
            await interaction.response.send_message("игрок добавлен в базу", ephemeral=True)
        return
    if prs.IsAdmin(interaction.user.id):
        await interaction.response.send_message("иди нахуй", ephemeral=True)

@tree.command(name="addpoint", description="добавить очки за работу админа")
@commands.has_permissions(administrator=True)
async def addpoint(interaction: discord.Integration, member: discord.Member, amount: int):
    """"""
    if prs.IsOwner(interaction.user.id):
        readed = json.load(open("Admins.json"))
        if str(member.id) in readed:
            readed[str(member.id)]["Points"] += amount
            await interaction.response.send_message(f"добавлены очки {amount} к игроку\n{prs.CheckMember(member.id, amount)}", ephemeral=True)
        if not str(member.id) in readed:
            await interaction.response.send_message("игрока нету в базе!", ephemeral=True)
        json.dump(readed, open("Admins.json", "w"), indent=3)
        return
    if prs.IsAdmin(interaction.user.id):
        await interaction.response.send_message("иди нахуй", ephemeral=True)
@tree.command(name="getpoint", description="Позволяет узнать очки администратора")
async def getpoint(interaction: discord.Integration, member: discord.Member):
    """"""
    result = prs.GetPoints(member.id)
    if result == "":
        await interaction.response.send_message("пользователя нету в базе данных администраторов", ephemeral=True)
    else:
        await interaction.response.send_message(embed=result, ephemeral=True)

#@tree.command(name="admins", description="Показывает список админов и их статус")
#async def admins(interaction: discord.Integration):
#    """"""
#    readed = json.load(open("Admins.json"))
#    readed = sorted(readed, key=lambda x: x['Points'], reverse=True)
#    data:str = ""
#    for i in readed:
#        data += f"{i['Name']}: Points [{i['Points']}]\n"
#    emb: discord.Embed = discord.Embed(title="Список админов", color=0xFF0000)

@tree.command(name="removepoint", description="убирает очки у админа")
@commands.has_permissions(administrator=True)
async def removepoint(interaction: discord.Integration, member: discord.Member, amount: int):
    """"""
    if prs.IsOwner(interaction.user.id):
        if prs.IsAdmin(member.id):
            prs.RemovePoint(member.id, amount=amount)
        await interaction.response.send_message("успешно", ephemeral=True)
        return
    if prs.IsAdmin(interaction.user.id):
        await interaction.response.send_message("иди нахуй", ephemeral=True)

@tree.command(name="report", description="Позволяет дать жалобу на админа")
async def report(interaction: discord.Integration, member: discord.Member, reason: str):
    """"""
    b: bool = prs.IsAdmin(member.id)
    if b and prs.IsOwner(member.id) == False:
        prs.RemovePoint(member.id, 20)
        await interaction.response.send_message("жалоба находится на рассмотрение ждите когда админа накажут", ephemeral=True)
        me: User = client.get_user(582158218310975499)
        await me.send(f"жалоба\nнарушитель: {member.name} \nпричина: {reason}")
    else:
        await interaction.response.send_message("пользователь не админ", ephemeral=True)

@tree.command(name="system", description="узнать статус системы хоста")
async def system(interaction: discord.Integration):
    """"""
    cpu = int(psutil.cpu_percent())
    disk_usage = psutil.disk_usage('/')
    memory = psutil.virtual_memory()
    out: discord.Embed = discord.Embed(title="Информация о ресурсах", color=0xff0000, description=None)
    out.add_field(name="Операционная система", value="Ubuntu 22.0.1 (desktop)", inline=False)
    out.add_field(name="Текущие потребление", value=f'нагрузка ЦП: {cpu}/100\nнагрузка оперативной памети: {int(memory.used/(1024*1024))}/{int(memory.total/(1024*1024))} Gb\nПотребление памети диска: {int(disk_usage.used/(1024*1024))}/{int(disk_usage.total/(1024*1024))} Gb \nСвободно ещо место: {int(disk_usage.free/(1024*1024))} Gb', inline=False)
    if prs.IsAdmin(interaction.user.id) or prs.IsOwner(interaction.user.id):
        await interaction.response.send_message(embed=out, ephemeral=True)
    else:
        await interaction.response.send_message("нету прав", ephemeral=True)

client.run(botcgf['Token'])