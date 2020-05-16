#!/usr/bin/python3
import os, commandModule
import sqlite3
import goblinSpy
import discord
from dotenv import load_dotenv
from discord.ext import commands

class Bot:
    def __init__(self):
        self.client = commands.Bot(os.getenv('DISCORD_PREFIX'))
        self.token = os.getenv('DISCORD_TOKEN')
        self.client.remove_command('help')
        @self.client.event
        async def on_ready():
            print('Bot up!')
        @self.client.command()
        async def help(ctx):
            await commandModule.Commands(ctx).help()
        @self.client.command()
        async def config(ctx):
            await commandModule.Commands(ctx).configure()
        @self.client.command()
        async def reset(ctx):
            await commandModule.Commands(ctx).reset()
        @self.client.command()
        async def teams(ctx):
            await commandModule.Commands(ctx).teams()
        @self.client.command()
        async def round(ctx):
            await commandModule.Commands(ctx).round()

    def run(self):
        self.client.run(self.token)

if __name__ == "__main__":
    load_dotenv()
    Bot().run()

