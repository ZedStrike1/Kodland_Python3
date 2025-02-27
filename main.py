import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random
import asyncio
from datetime import datetime, timedelta


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Gagal memuat gambar Pokémon.")
    else:
        await ctx.send("Anda sudah memiliki Pokémon!")

@bot.command()
async def attack(ctx, target: discord.Member = None):
    # If no target is provided, ask the user to mention a target
    if target is None:
        await ctx.send("Tetapkan pemain yang ingin Anda serang dengan menyebutnya.")
        return
    
    # Check if both players have a Pokémon
    if target.name not in Pokemon.pokemons or ctx.author.name not in Pokemon.pokemons:
        await ctx.send("Kedua pemain harus memiliki Pokémon untuk bertarung!")
        return

    # Get the attacker and the enemy Pokémon objects
    attacker = Pokemon.pokemons[ctx.author.name]
    enemy = Pokemon.pokemons[target.name]

    # Check if either Pokémon's HP is 0
    if attacker.hp == 0:
        await ctx.send(f"{ctx.author.name}, Pokémon Anda sudah kehabisan HP! Anda tidak bisa menyerang.")
        return
    if enemy.hp == 0:
        await ctx.send(f"{target.name}'s Pokémon sudah kehabisan HP! Mereka tidak bisa diserang.")
        return

    # Set turn if not set yet
    if not attacker.turn_event.is_set() and not enemy.turn_event.is_set():
        attacker.turn_event.set()

    # Execute the attack if it's the attacker's turn
    if attacker.turn_event.is_set():
        await attacker.attack(ctx, enemy)
    else:
        await ctx.send("⏳ Tunggu giliranmu untuk menyerang!")




@bot.command()
async def info(ctx, member: discord.Member = None):
    # If no member is specified, use the command author
    if member is None:
        member = ctx.author
        is_self = True 
    else:
        is_self = False

    author_name = member.name

    if author_name in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author_name]
        await ctx.send(f"Informasi Pokémon {author_name}:\n{await pokemon.info()}")
    else:
        if is_self:
            await ctx.send(f"Sepertinya Anda tidak memiliki Pokemon. Ketik `!go` untuk membuat Pokemon mu!")    

        else:
            await ctx.send(f"{author_name} tidak memiliki Pokémon.")

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        response = await pokemon.feed()
        await ctx.send(response)
    else:
        await ctx.send("Sepertinya Anda tidak memiliki Pokemon. Ketik `!go` untuk membuat Pokemon mu!")    


bot.run(token)