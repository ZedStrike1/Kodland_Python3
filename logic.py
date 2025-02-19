import aiohttp
import random
from random import randint
import asyncio  # Add asyncio to handle asynchronous code

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        if pokemon_trainer not in self.pokemons:
            self.pokemons[pokemon_trainer] = self

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
        return f"""Nama Pokemon kamu: {self.name}
                Kekuatan Pokemon: {self.power}
                HP Pokemon: {self.hp}"""

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

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Pokemon Penyihir menggunakan perisai dalam pertarungan"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertarungan @{self.pokemon_trainer} melawan @{enemy.pokemon_trainer}\nHP @{enemy.pokemon_trainer} sekarang {enemy.hp}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!"


class Wizard(Pokemon):
    # Kelas ini dapat menambahkan method dan properti khusus untuk penyihir
    pass


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPetarung menggunakan serangan super dengan kekuatan:{super_power}"


# async def main():
#     wizard = Wizard("username1")
#     fighter = Fighter("username2")

#     print(await wizard.info())  # Await here to get the result of the coroutine
#     print("#" * 10)
#     print(await fighter.info())  # Await here as well
#     print("#" * 10)
#     # You can also await attacks if needed
#     print(await wizard.attack(fighter))
#     print(await fighter.attack(wizard))


# # Run the main function inside an event loop
# asyncio.run(main())
