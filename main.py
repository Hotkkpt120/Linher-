import os
from colorama import Back, Fore, Style
from requests import post, Session, get
from random import choice
import random
import threading
from discord.ext import commands
import requests as ru
import discord
from discord import ui
import time
import platform
from datetime import datetime
from discord import app_commands
from discord_webhooks import DiscordWebhooks
from discord.ext.commands import Bot
import uuid
from typing import Literal
import json
from bs4 import BeautifulSoup as bs
from pystyle import Colors, Colorate
import itertools
from discord import SyncWebhook
import requests
from discord import Activity, ActivityType, Status
from datetime import datetime, timedelta
import json
import asyncio
import aiohttp
from myserver import server_on
#from discord_webhook import DiscordWebhook, DiscordEmbed

print(os.getenv("MY_SECRET"))

avatarbot = "https://cdn.discordapp.com/attachments/1282601980870787084/1290566193870274612/IMG_6477.jpg?ex=66fe3e6e&is=66fcecee&hm=5b7baf8852f1a40bc8b95f4474ebffe93ac6888f80f798c0c372afbf25de9879&"
with open('settings.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)
IDROLE = data["IDROLE"]
my_secret = [(os.getenv("MY_SECRET"))]
VOICE_ID = data["VOICE_ID"]
ALERT = data["ALERT"]
LOGVERIFY = data["LOGVERIFY"]


class verifysuccess(discord.ui.View):

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="・ ยืนยันตัวตน",
                       emoji="✅",
                       style=discord.ButtonStyle.green,
                       custom_id="verifysuccess1")
    async def verifysuccess(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        role_id_to_add = IDROLE

        member = interaction.guild.get_member(interaction.user.id)

        if discord.utils.get(member.roles, id=role_id_to_add):
            await interaction.response.send_message(
                content="```คุณเคยรับบทบาทแล้ว```", ephemeral=True)
        else:
            try:
                user = interaction.user
                await member.add_roles(discord.Object(id=role_id_to_add))
                embed = discord.Embed(
                    title="",
                    description=
                    f"__ข้อมูลการยืนยันตัวตน__\n\nคุณ ได้ยืนยันตัวตนเสร็จสิ้นและได้รับบทบาท\n > <@&{role_id_to_add}>",
                    color=0xff33cc)
                embed.set_author(name=f"{interaction.guild.name}",
                                 url="",
                                 icon_url=avatarbot)
                await interaction.response.send_message(embed=embed,
                                                        ephemeral=True)
                embed = discord.Embed(
                    title="",
                    description=
                    f"__ข้อมูลการยืนยันตัวตน__\n\nคุณ ได้ยืนยันตัวตนเสร็จสิ้น ขอบคุณมาก",
                    color=0xff33cc)
                embed.set_author(name=f"{interaction.guild.name}",
                                 url="",
                                 icon_url=avatarbot)
                await interaction.user.send(embed=embed)
                channel = client.get_channel(LOGVERIFY)
                embed = discord.Embed(
                    title="รายละเอียดการยืนยัน",
                    description=
                    f"{interaction.user.mention} `:` `ได้ยืนยันเข้าใช้งานเชิฟเวอร์เรียบร้อยแล้วคะ ✅`",
                    color=0xff33cc)
                embed.set_author(name=f"{interaction.guild.name}",
                                 url="",
                                 icon_url=avatarbot)
                await channel.send(embed=embed)
            except discord.Forbidden:
                await interaction.response.send_message(
                    content=
                    "ไม่สามารถเพิ่มบทบาทได้ กรุณาตรวจสอบการตั้งค่าสิทธิ์",
                    ephemeral=True)


class aclient(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'),
                         intents=discord.Intents().all())
        self.role = None

    async def on_ready(self):
        channel = client.get_channel(VOICE_ID)
        prfx = (Back.BLACK + Fore.GREEN +
                time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET +
                Fore.WHITE + Style.BRIGHT)
        activity = discord.Streaming(
            name="my channel",
            url="https://www.tiktok.com/@olympusthai?_t=8qCc1BwjaxL&_r=1")
        await client.change_presence(status=discord.Status.idle,
                                     activity=activity)
        try:
            if channel and isinstance(channel, discord.VoiceChannel):
                voice_channel = await channel.connect()
                print(f'Bot connected to voice channel: {channel.name}')
                print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
                synced = await self.tree.sync()
                print(prfx + " Slash CMDs Synced " + Fore.YELLOW +
                      str(len(synced)) + " Commands")
                self.add_view(verifysuccess())
        except discord.ClientException as e:
            print(f'Error connecting to voice channel: {e}')


client = aclient()


@client.tree.command(name='setupverify',
                     description='Owneronly・สร้างห้องยืนยันตัวตน')
@app_commands.checks.has_permissions(administrator=True)
async def del_code(interaction: discord.Interaction):
    embed = discord.Embed(title="", description="", color=0xff33cc)

    embed.set_author(name=f"{interaction.guild.name}",
                     url="",
                     icon_url=avatarbot)
    embed.add_field(
        name="",
        value=
        f"__วิธีการเข้าใช้งานเชิฟเวอร์ดิสคอร์ด__ \n\n **กดปุ่มด่านล่าง** `✅・ยืนยันตัวตน` **เพิ่อเข้าใช้งานดิสคอร์ด** \n\n ",
        inline=True)
    embed.set_image(
        url=
        "https://media.discordapp.net/attachments/1215793327254011984/1215836285915369503/source.gif?ex=65fe32c7&is=65ebbdc7&hm=9c65f85ad237b2e448822d2bba4b21157abd906963a20e50111d45e75caee501&=&width=1054&height=592"
    )
    await interaction.channel.send(embed=embed, view=verifysuccess())


@del_code.error
async def del_code_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(f"{ALERT}", ephemeral=True)

server_on()

client.run(os.getenv("MY_SECRET"))