
from agent.agent_factory import create_agent
from models.pokemon_state import PokemonState

# --------------------------------------------------
# Setup agent
# --------------------------------------------------

my_pokemon=[
            PokemonState(
                name="Froslass-Mega",
                nature="Modest",
                evs={"hp": 32, "spa": 32}
            ),
            PokemonState(
                name="Whimsicott",
                nature="Modest",
                evs={"spd": 32, "spa": 32}
            ),
            PokemonState(
                name="Aerodactyl"
            ),
            PokemonState(
                name="Gholdengo",
                nature="Modest",
                item="Life Orb",
                evs={"spd": 32, "spa": 32}
            ),
            PokemonState(
                name="Raichu"
            ),
            PokemonState(
                name="Pelipper"
            )
        ]
opponent_pokemon=[]

agent = create_agent(my_pokemon, opponent_pokemon)


# --------------------------------------------------
# Interactive session
# --------------------------------------------------

print("VGC Agent interactive session")
print("Type 'exit' or 'quit' to end the session.")
print()

while True:

    try:
        user_input = input("You: ")

    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        break

    user_input = user_input.strip()

    if not user_input:
        continue

    if user_input.lower() in ("exit", "quit"):
        print("Exiting.")
        break

    try:
        response = agent.run(user_input)

        print()
        print("Agent:")
        print(response)
        print()

    except Exception as error:
        print()
        print("ERROR:")
        print(error)
        print()