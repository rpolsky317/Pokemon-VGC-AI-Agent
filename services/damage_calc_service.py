from clients.damage_calc_client import DamageCalcClient
from models.damage_calc_request import DamageCalculationRequest
from models.damage_result import DamageCalculationResponse


class DamageCalcService:
    def __init__(self, client: DamageCalcClient):
        self.client = client

    def calculate(
        self,
        request: DamageCalculationRequest
    ) -> DamageCalculationResponse:

        return self.client.calculate(request)