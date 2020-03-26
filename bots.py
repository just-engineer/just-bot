import sc2
from sc2.ids.unit_typeid import UnitTypeId


class WorkerRushBot(sc2.BotAI):
    async def on_step(self, iteration: int):
        if iteration == 0:
            for worker in self.workers:
                self.do(worker.attack(self.enemy_start_locations[0]))


class DroneBuilder(sc2.BotAI):
    def __init__(self, supply_left_to_overlord=1):
        super().__init__()
        self.supply_left_to_overlord = supply_left_to_overlord

    async def on_step(self, iteration: int):
        for loop_larva in self.larva:

            # at first, check, need we build overlords
            in_production = self.already_pending(UnitTypeId.OVERLORD) > 0
            need_more = self.supply_left <= self.supply_left_to_overlord
            if need_more and not in_production:  # few supply, build overlord for the future
                if self.can_afford(UnitTypeId.OVERLORD):
                    self.do(loop_larva.train(UnitTypeId.OVERLORD), subtract_cost=True, subtract_supply=True)
                else:  # can't train overlord on this step
                    break  # no build anything before overlord

            # have many supply, can build drones
            if self.can_afford(UnitTypeId.DRONE):
                self.do(loop_larva.train(UnitTypeId.DRONE), subtract_cost=True, subtract_supply=True)
            else:  # can't train drons on this step
                break


class ZerglingRush(sc2.BotAI):

    def __init__(self, supply_to_attack):
        super().__init__()
        self.supply_to_attack = supply_to_attack

    

    async def on_step(self, iteration: int):

        already_have_pool = self.structures \
            .filter(lambda structure: structure.type_id == UnitTypeId.SPAWNINGPOOL and structure.is_ready) \
            .amount

        if self.can_afford(UnitTypeId.SPAWNINGPOOL) \
                and not self.already_pending(UnitTypeId.SPAWNINGPOOL) \
                and not already_have_pool:
            map_center = self.game_info.map_center
            position_towards_map_center = self.start_location.towards(map_center, distance=5)
            await self.build(UnitTypeId.SPAWNINGPOOL, near=position_towards_map_center, placement_step=1)

        if already_have_pool:
            for loop_larva in self.larva:
                if self.can_afford(UnitTypeId.ZERGLING):
                    self.do(loop_larva.train(UnitTypeId.ZERGLING), subtract_cost=True, subtract_supply=True)

        if self.supply_army >= self.supply_to_attack:
            # is_attack = True

            for u in (self.units - self.workers):
                self.do(u.attack(self.enemy_start_locations[0]))
