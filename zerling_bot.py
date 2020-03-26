from queue import Queue
from typing import List
import sc2
from sc2 import run_game, maps, Race, Difficulty, UnitTypeId
from sc2.player import Bot, Computer
import bots


class AbstractBot(sc2.BotAI):
    def __init__(self):
        super().__init__()


class ZerglingRush(AbstractBot):

    def __init__(self, army_supply_to_attack=10):
        super().__init__()
        self.supply_to_attack = army_supply_to_attack
        task = Task(lambda bot_api: bot_api.workers.amount <= 20 and bot_api.can_afford(UnitTypeId.DRONE),
                    lambda bot_api: bot_api.do_action(bot_api.larva.random.train(UnitTypeId.DRONE)))
        self.build_order = BuildOrder(self, [task, task, task])

    async def on_step(self, iteration: int):

        if not self.build_order.is_complete():
            self.build_order.do_if_possible()
        else:
            print("finish")

        # if self.workers.amount <= 12 and not self.already_pending(UnitTypeId.DRONE):
        #     self.do_action(self.larva.random.train(UnitTypeId.DRONE))

        # extractors = self.structures.filter(lambda structure: structure.type_id == UnitTypeId.EXTRACTOR).amount
        # if self.workers.amount == 13 and extractors < 1 and self.can_afford(UnitTypeId.EXTRACTOR) \
        #         and not self.already_pending(UnitTypeId.EXTRACTOR):
        #     drone = self.workers.random
        #     target = self.vespene_geyser.closest_to(drone.position)
        #     err = self.do(drone.build(UnitTypeId.EXTRACTOR, target))

        # already_have_pool = self.structures \
        #     .filter(lambda structure: structure.type_id == UnitTypeId.SPAWNINGPOOL and structure.is_ready) \
        #     .amount
        #
        # self.build_pool(already_have_pool)
        #
        # if already_have_pool:
        #     for loop_larva in self.larva:
        #         if self.can_afford(UnitTypeId.ZERGLING):
        #             self.do(loop_larva.train(UnitTypeId.ZERGLING), subtract_cost=True, subtract_supply=True)
        #
        # if self.supply_army >= self.supply_to_attack:
        #     self.attack()

    def do_action(self, action):
        self.do(action, subtract_cost=True, subtract_supply=True)

    def build_pool(self, already_have_pool):
        if self.can_afford(UnitTypeId.SPAWNINGPOOL) \
                and not self.already_pending(UnitTypeId.SPAWNINGPOOL) \
                and not already_have_pool:
            map_center = self.game_info.map_center
            position_towards_map_center = self.start_location.towards(map_center, distance=5)
            self.build(UnitTypeId.SPAWNINGPOOL, near=position_towards_map_center, placement_step=1)

    def attack(self):
        for u in (self.units - self.workers):
            self.do(u.attack(self.enemy_start_locations[0]))


class Task:
    def __init__(self, predicate, action):
        self.predicate = predicate
        self.action = action


class BuildOrder:

    def __init__(self, bot_api, tasks: List[Task]):
        self.queue = tasks
        self.bot = bot_api

    def do_if_possible(self):
        if not self.is_complete() and self.queue[0].predicate(self.bot):
            self.queue[0].action(self.bot)
            self.queue.pop(0)

    def is_complete(self):
        return len(self.queue) == 0


if __name__ == '__main__':
    run_game(maps.get("Abyssal Reef LE"), [
        Bot(Race.Zerg, ZerglingRush()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=True)
