import random


class Character:
    def __init__(self, name, health, attack_power, armor, crit_chance, dodge_chance):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.armor = armor
        self.crit_chance = crit_chance
        self.dodge_chance = dodge_chance

    def attack(self, other):
        if random.random() < other.dodge_chance:
            print(f"{other.name} dodged the attack")
            return

        damage = self.attack_power

        if random.random() < self.crit_chance:
            damage *= 2
            print("Critical hit")

        damage -= other.armor
        damage = max(0, damage)

        print(f"{self.name} attacks {other.name} for {damage}")
        other.take_damage(damage)

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} has {self.health} HP left")

    def __str__(self):
        return f"{self.name}: HP={self.health}, ATK={self.attack_power}"

    def __add__(self, other):
        return f"Team: {self.name} + {other.name}"

    def __lt__(self, other):
        return self.health < other.health

    def __eq__(self, other):
        return self.health == other.health and self.attack_power == other.attack_power

    def __len__(self):
        return self.health

    def __bool__(self):
        return self.health > 0


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 120, 18, 5, 0.2, 0.1)

    def attack(self, other):
        print(f"{self.name} uses Power Strike")
        damage = self.attack_power + 10

        if random.random() < self.crit_chance:
            damage *= 2
            print("Critical hit")

        damage -= other.armor
        damage = max(0, damage)

        other.take_damage(damage)


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 80, 25, 2, 0.3, 0.15)

    def attack(self, other):
        print(f"{self.name} casts Fireball")

        damage = self.attack_power + 5
        other.take_damage(damage)

        burn = 5
        print(f"{other.name} takes {burn} burn damage")
        other.take_damage(burn)


class Archer(Character):
    def __init__(self, name):
        super().__init__(name, 100, 15, 3, 0.25, 0.25)

    def attack(self, other):
        print(f"{self.name} uses Double Shot")

        for _ in range(2):
            if random.random() < other.dodge_chance:
                print(f"{other.name} dodged")
                continue

            damage = self.attack_power

            if random.random() < self.crit_chance:
                damage *= 2
                print("Critical hit")

            damage -= other.armor
            damage = max(0, damage)

            other.take_damage(damage)


def choose_character():
    while True:
        print("Choose your character:")
        print("1. Warrior")
        print("2. Mage")
        print("3. Archer")

        choice = input("> ")

        if choice == "1":
            return Warrior("Valerius")
        elif choice == "2":
            return Mage("Zephyrus")
        elif choice == "3":
            return Archer("Nightshade")
        else:
            print("Invalid choice\n")


def create_enemy():
    return random.choice([
        Warrior("Enemy Warrior"),
        Mage("Enemy Mage"),
        Archer("Enemy Archer")
    ])


def player_turn(player, enemy):
    while True:
        print("\nChoose action:")
        print("1. Attack")
        print("2. Show stats")

        choice = input("> ")

        if choice == "1":
            player.attack(enemy)
            break
        elif choice == "2":
            print(player)
            print(enemy)
        else:
            print("Invalid input")


def game():
    player = choose_character()
    enemy = create_enemy()

    print("\n--- Characters ---")
    print(player)
    print(enemy)

    print("\n--- Comparison ---")
    print("Player weaker than enemy:", player < enemy)
    print("Player equals enemy:", player == enemy)

    print("\n--- Team creation ---")
    print(player + enemy)

    print("\n--- Health check ---")
    print("Player HP:", len(player))

    input("\nPress Enter to start")

    round_num = 1

    while player and enemy:
        print(f"\n--- Round {round_num} ---")

        player_turn(player, enemy)

        if not enemy:
            print("\nYou win")
            break

        print("\nEnemy turn:")
        enemy.attack(player)

        if not player:
            print("\nYou lose")
            break

        round_num += 1


game()