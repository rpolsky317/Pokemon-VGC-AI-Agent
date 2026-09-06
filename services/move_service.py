
class MoveService:

    def __init__(self, move_repository, pokeapi_client):
        self.move_repository = move_repository
        self.pokeapi_client = pokeapi_client


    def get_move_info(self, move_name):

        # First, check the local database
        move = self.move_repository.get(move_name)

        # If it's already cached, return it
        if move is not None:
            return move

        # Otherwise, retrieve it from PokéAPI
        move = self.pokeapi_client.get_move(move_name)

        # Save it locally for future requests
        self.move_repository.save(move)

        return move