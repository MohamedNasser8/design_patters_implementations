from src.schema import CharacterFactory

def main():
    character_factory = CharacterFactory()
    character_factory.create_character("John", "Warrior")
    character_factory.create_character("Jane", "Mage")
    character_factory.create_character("Jim", "Rogue")
    character_factory.create_character("Jill", "Priest")

    character_factory.create_character("Luke", "Warrior")

    character_factory.create_character("Luke", "Mage")



if __name__ == "__main__":
    main()
