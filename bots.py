import sc2
from sc2.ids.unit_typeid import UnitTypeId


class WorkerRushBot(sc2.BotAI):
    async def on_step(self, iteration: int):
        if iteration == 0:
            for worker in self.workers:
                self.do(worker.attack(self.enemy_start_locations[0]))


class DroneBuilder(sc2.BotAI):
    def __init__(self, supply_left_to_overlord=2):
        super().__init__()
        self.supply_left_to_overlord = supply_left_to_overlord

    async def on_step(self, iteration: int):
        for loop_larva in self.larva:
            if self.supply_left <= self.supply_left_to_overlord:  # few supply, build overlord for the future

                if self.can_afford(UnitTypeId.OVERLORD):
                    self.do(loop_larva.train(UnitTypeId.OVERLORD), subtract_cost=True, subtract_supply=True)
                else:  # can't train overlord on this step
                    break

            else:  # have many supply, can build drones

                if self.can_afford(UnitTypeId.DRONE):
                    self.do(loop_larva.train(UnitTypeId.DRONE), subtract_cost=True, subtract_supply=True)
                else:  # can't train drons on this step
                    break


