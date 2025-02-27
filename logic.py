import aiohttp
import random
import asyncio
from random import randint
from datetime import datetime, timedelta


class Pokemon:
    pokemons = {}  # This should be reset when the bot starts


    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        self.last_feed_time  = datetime.now()
        self.turn_event = asyncio.Event()


        self.pokemons[pokemon_trainer] = self  # Always add the trainer's Pokémon


    async def feed(self, feed_interval=60, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Kesehatan pokemon meningkat. Kesehatan pokemon sekarang: `{self.hp}`"
        else:
            return f"Waktu makan pokemon berikutnya: `{(current_time + delta_time).strftime('%H:%M:%S')}`"
    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"""
**Nama pokemon anda:** `{self.name.capitalize()}`
**Power pokemon anda:** `{self.power}`
**Kesehatan pokemon anda:** `{self.hp}`"""

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url 
                else:
                    return None

    async def attack(self, ctx, enemy):
        if self.hp == 0 or enemy.hp == 0:
            return await ctx.send("Tidak bisa menyerang saat HP Pokemon 0")
        else:
            if {enemy.pokemon_trainer} == {self.pokemon_trainer}:
                return await ctx.send("Ngapain Serang Diri Sendiri????")
            else:
                if not self.turn_event.is_set():
                    await ctx.send("⏳ Tunggu giliranmu untuk menyerang!")
                    return

                if self.hp == 0:
                    await ctx.send(f"{self.pokemon_trainer} tidak bisa menyerang saat HP 0!")
                    return

                if enemy.hp > self.power:
                    enemy.hp -= self.power
                    result = f"⚔️ {self.pokemon_trainer} menyerang {enemy.pokemon_trainer}!\n❤️ HP {enemy.pokemon_trainer} sekarang: `{enemy.hp}`"
                else:
                    enemy.hp = 0
                    await ctx.send(f"🏆 {self.pokemon_trainer} menang dari {enemy.pokemon_trainer}!")
                    return

                await ctx.send(result)



                # **Ganti giliran ke lawan**
                self.turn_event.clear()
                enemy.turn_event.set()

            
class Wizard(Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)

class Fighter(Pokemon):
    async def attack(self, ctx, enemy):
        if {enemy.pokemon_trainer} == {self.pokemon_trainer}:
            return await ctx.send("Ngapain Serang Diri Sendiri????")
        else:
            if self.hp == 0:
                await ctx.send(f"{self.pokemon_trainer} tidak bisa menyerang saat HP 0!")
                return
            
            super_power = randint(5, 15)
            self.power += super_power
            await ctx.send(f"🔥 {self.pokemon_trainer} menggunakan serangan super `{super_power}`!")
            
            result = await super().attack(ctx, enemy)  
            
            return result

    async def feed(self):
        return await super().feed(feed_interval=10)
