import random
from collections import defaultdict

# Helper function to get the correct ordinal suffix
def get_ordinal_suffix(number):
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"

class Unit:
    def __init__(self, unit_type, health, attack, hit_number, nat20_damage, name):
        self.unit_type = unit_type
        self.health = health
        self.attack = attack
        self.hit_number = hit_number
        self.nat20_damage = nat20_damage
        self.name = name
        self.unit_number = 1

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage

    def attack_successful(self, target, leader_bonus):
        roll = random.randint(1, 20)

        # Apply leader bonus to roll
        roll += leader_bonus

        # Spearmen/Pikemen get +2 to hit if target is Cavalry
        if self.name == "Spearmen/Pikemen Battalion" and target.name in ["Heavy Cav Battalion", "Light Cav Battalion"]:
            roll += 2

        if roll == 20:
            return roll, True, self.nat20_damage
        return roll, roll >= self.hit_number, self.attack

    def __repr__(self):
        return f"{self.name} (Health: {self.health})"

class Side:
    def __init__(self, name, units, leader_bonus):
        self.name = name
        self.units = units
        self.leader_bonus = leader_bonus
        self.unit_counts = defaultdict(int)

    def is_defeated(self):
        return all(not unit.is_alive() for unit in self.units)

    def get_living_units(self):
        return [unit for unit in self.units if unit.is_alive()]

    def get_unit_display_name(self, unit):
        return f"{get_ordinal_suffix(unit.unit_number)} {unit.name}"

    def get_units_by_type(self, unit_names):
        return [unit for unit in self.units if unit.name in unit_names and unit.is_alive()]

    def get_non_specific_units(self, exclude_unit_names):
        return [unit for unit in self.units if unit.name not in exclude_unit_names and unit.is_alive()]

    def __repr__(self):
        return f"{self.name}({self.units})"

def update_unit_numbers(units):
    type_count = defaultdict(int)
    for unit in units:
        if unit.is_alive():
            type_count[unit.unit_type] += 1
            unit.unit_number = type_count[unit.unit_type]

def ranged_phase(attacking_side, defending_side):
    for unit in attacking_side.get_units_by_type(['Bowmen Battalion', 'Crossbowmen Battalion']):
        if defending_side.is_defeated():
            break
        target = random.choice(defending_side.get_living_units())
        roll, success, damage = unit.attack_successful(target, attacking_side.leader_bonus)
        attacker_name = attacking_side.get_unit_display_name(unit)
        target_name = defending_side.get_unit_display_name(target)

        if success:
            target.take_damage(damage)
            if target.is_alive():
                print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, "
                      f"attacked {defending_side.name}'s {target_name} and did {damage} damage.")
            else:
                print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, "
                      f"attacked {defending_side.name}'s {target_name}, did {damage} damage, and killed {defending_side.name}'s {target_name}.")
        else:
            print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, and missed {defending_side.name}'s {target_name}.")

def shock_phase(attacking_side, defending_side):
    for unit in attacking_side.get_units_by_type(['Heavy Cav Battalion', 'Light Cav Battalion']):
        if defending_side.is_defeated():
            break
        target = random.choice(defending_side.get_living_units())
        roll, success, damage = unit.attack_successful(target, attacking_side.leader_bonus)
        attacker_name = attacking_side.get_unit_display_name(unit)
        target_name = defending_side.get_unit_display_name(target)

        if success:
            target.take_damage(damage)
            if target.is_alive():
                print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, "
                      f"attacked {defending_side.name}'s {target_name} and did {damage} damage.")
            else:
                print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, "
                      f"attacked {defending_side.name}'s {target_name}, did {damage} damage, and killed {defending_side.name}'s {target_name}.")
        else:
            print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, and missed {defending_side.name}'s {target_name}.")

def melee_phase(attacking_side, defending_side):
    for unit in attacking_side.get_non_specific_units(['Bowmen Battalion', 'Crossbowmen Battalion', 'Heavy Cav Battalion', 'Light Cav Battalion']):
        if defending_side.is_defeated():
            break
        target = random.choice(defending_side.get_living_units())
        roll, success, damage = unit.attack_successful(target, attacking_side.leader_bonus)
        attacker_name = attacking_side.get_unit_display_name(unit)
        target_name = defending_side.get_unit_display_name(target)

        if success:
            target.take_damage(damage)
            if target.is_alive():
                print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, "
                      f"attacked {defending_side.name}'s {target_name} and did {damage} damage.")
            else:
                print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, "
                      f"attacked {defending_side.name}'s {target_name}, did {damage} damage, and killed {defending_side.name}'s {target_name}.")
        else:
            print(f"{attacking_side.name}'s {attacker_name} rolled a {roll}, and missed {defending_side.name}'s {target_name}.")

def simulate_battle(side_a, side_b):
    round_number = 1
    while not side_a.is_defeated() and not side_b.is_defeated():
        print(f"Round {round_number}")
        round_number += 1

        # Update unit numbers to reflect the current state
        update_unit_numbers(side_a.get_living_units())
        update_unit_numbers(side_b.get_living_units())

        # Ranged Phase
        print("\nRanged Phase:")
        ranged_phase(side_a, side_b)
        ranged_phase(side_b, side_a)

        # Shock Phase
        print("\nShock Phase:")
        shock_phase(side_a, side_b)
        shock_phase(side_b, side_a)

        # Melee Phase
        print("\nMelee Phase:")
        melee_phase(side_a, side_b)
        melee_phase(side_b, side_a)

        # Remove dead units
        side_a.units = [unit for unit in side_a.units if unit.is_alive()]
        side_b.units = [unit for unit in side_b.units if unit.is_alive()]

        print(f"\nEnd of Round {round_number - 1}")
        print(f"Side A: {[unit for unit in side_a.get_living_units()]}")
        print(f"Side B: {[unit for unit in side_b.get_living_units()]}")
        print()

    if side_a.is_defeated():
        print("Side B wins!")
    else:
        print("Side A wins!")

def get_side_input(side_name, unit_types):
    print(f"Input details for {side_name}:")
    name = input("Name: ")
    leader_bonus = int(input("Leader Bonus (can be positive or negative): "))
    units = []

    for unit_type in unit_types:
        count = int(input(f"Number of {unit_type['name']}s: "))
        for _ in range(count):
            units.append(Unit(
                unit_type=unit_type['name'],
                health=unit_type['health'],
                attack=unit_type['attack'],
                hit_number=unit_type['hit_number'],
                nat20_damage=unit_type['nat20_damage'],
                name=unit_type['name']
            ))

    return Side(name, units, leader_bonus)

def main():
    unit_types = [
        {"name": "Heavy Cav Battalion", "health": 60, "attack": 60, "hit_number": 8, "nat20_damage": 72},
        {"name": "Light Cav Battalion", "health": 30, "attack": 40, "hit_number": 8, "nat20_damage": 48},
        {"name": "Bowmen Battalion", "health": 10, "attack": 40, "hit_number": 14, "nat20_damage": 48},
        {"name": "Crossbowmen Battalion", "health": 15, "attack": 40, "hit_number": 9, "nat20_damage": 48},
        {"name": "Heavy Swordsmen Battalion", "health": 50, "attack": 50, "hit_number": 12, "nat20_damage": 60},
        {"name": "Spearmen/Pikemen Battalion", "health": 20, "attack": 60, "hit_number": 12, "nat20_damage": 72},
        {"name": "Knight Battalion", "health": 80, "attack": 80, "hit_number": 10, "nat20_damage": 96},
        {"name": "Light Swordsmen Battalion", "health": 25, "attack": 25, "hit_number": 10, "nat20_damage": 30},
        {"name": "Peasant Leavy Group", "health": 5, "attack": 10, "hit_number": 14, "nat20_damage": 12},
        {"name": "Shieldman", "health": 100, "attack": 20, "hit_number": 12, "nat20_damage": 24},
        {"name": "Galleys", "health": 100, "attack": 40, "hit_number": 13, "nat20_damage": 48},
        {"name": "Longship", "health": 35, "attack": 25, "hit_number": 15, "nat20_damage": 30},
        {"name": "Carracks", "health": 65, "attack": 60, "hit_number": 11, "nat20_damage": 72},
        {"name": "Liburnian", "health": 50, "attack": 30, "hit_number": 14, "nat20_damage": 36},
    ]

    # Get initial input
    side_a = get_side_input("Side A", unit_types)
    side_b = get_side_input("Side B", unit_types)

    # Start simulation loop
    while True:
        print("\nStarting the battle...\n")
        # Clone sides to reset the state after each run
        side_a_clone = Side(side_a.name, [Unit(unit.unit_type, unit.health, unit.attack, unit.hit_number, unit.nat20_damage, unit.name) for unit in side_a.units], side_a.leader_bonus)
        side_b_clone = Side(side_b.name, [Unit(unit.unit_type, unit.health, unit.attack, unit.hit_number, unit.nat20_damage, unit.name) for unit in side_b.units], side_b.leader_bonus)

        simulate_battle(side_a_clone, side_b_clone)

        # Prompt user for re-running
        repeat = input("\nPress Enter to rerun the simulation or type 'exit' to quit: ").strip().lower()
        if repeat == 'exit':
            break

if __name__ == "__main__":
    main()
