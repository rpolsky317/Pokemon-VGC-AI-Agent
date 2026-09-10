from models.damage_calc_request import DamageCalculationRequest

class DamageCalcToolDispatcher:

    """
    Provides a list of tools available to the AI agent.
    """

    def __init__(self, damage_calc_service):
        self.damage_calc_service = damage_calc_service

    def dispatch(self, tool_name, arguments):
        """
        Execute a tool requested by the AI agent.
        """
        
        if tool_name == "calculate_damage":
            request = DamageCalculationRequest.from_dict(arguments)

            return self.calculate_damage(
                request=request
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )
    
    def calculate_damage(self, request): 
        """ 
        Calculates damage using the Pokemon Champions damage calculator. 
        """ 
        return self.damage_calc_service.calculate(request)
    
    