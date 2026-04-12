from abc import ABC, abstractmethod


class CharacterPrototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class Character(CharacterPrototype):
    def __init__(self):
        self.name = ""
        self.char_class = ""
        self.level = 0
        self.abilities = []
        self.equipment = []
        self.health = 0
        self.stamina = 0

    def clone(self):
        import copy
        return copy.deepcopy(self)

class CharacterFactory(ABC):
    
    @abstractmethod
    def create_character(self, name, char_class, level, abilities):
        pass

class WarriorFactory(CharacterFactory):
    def create_character(self, name):
        character = Character()
        character.name = name
        character.char_class = "Warrior"
        character.level = 1
        character.abilities = ["Warrior", "Shield Block", "Heroic Strike"]
        character.equipment = ["Sword", "Shield"]
        return character

class MageFactory(CharacterFactory):
    def create_character(self, name):
        character = Character()
        character.name = name
        character.char_class = "Mage"
        character.level = 1
        character.abilities = ["Mage", "Fireball", "Ice Shard"]
        character.equipment = ["Staff", "Book"]
        return character

class RogueFactory(CharacterFactory):
    def create_character(self, name):
        character = Character()
        character.name = name
        character.char_class = "Rogue"
        character.level = 1
        character.abilities = ["Rogue", "Backstab", "Blade Flurry"]
        character.equipment = ["Dagger", "Sword"]
        return character

class PriestFactory(CharacterFactory):
    def create_character(self, name):
        character = Character()
        character.name = name
        character.char_class = "Priest"
        character.level = 1
        character.abilities = ["Priest", "Heal", "Prayer"]
        character.equipment = ["Holy Symbol", "Book"]
        return character


class CharacterRegistryFactory:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CharacterRegistryFactory, cls).__new__(cls)
            factories = {
                "Warrior": WarriorFactory(),
                "Mage": MageFactory(),
                "Rogue": RogueFactory(),
                "Priest": PriestFactory()
            }
            cls._instance.factories = factories
            cls._instance.created_characters = {}
            cls._instance.template_characters = {}
        return cls._instance
    
    def create_character(self, name, char_class):
        if char_class not in self.factories:
            raise ValueError(f"Invalid character class: {char_class}")
        if name in self.created_characters:
            raise ValueError(f"Character {name} already exists")
        if char_class in self.template_characters:
            print(f"Cloning character {name} of class {char_class}")
            new_character = self.template_characters[char_class].clone()
            new_character.name = name
            self.created_characters[name] = new_character
            print(f"Created new clone of character {name} of class {char_class}")
            return new_character
        else:
            new_character = self.factories[char_class].create_character(name)
            self.template_characters[char_class] = new_character
            print(f"Created new character {name} of class {char_class}")
            return new_character
