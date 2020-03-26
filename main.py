import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
import bots

run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Zerg, bots.ZerglingRush()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)
