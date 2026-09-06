import requests

from models.damage_calc_request import DamageCalculationRequest
from models.damage_result import DamageCalculationResponse


class DamageCalcClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def calculate(
        self,
        request: DamageCalculationRequest
    ) -> DamageCalculationResponse:

        response = requests.post(
            f"{self.base_url}/calculate",
            json=request.to_dict(),
        )

        print("Damage Calc Status:", response.status_code)
        print("Damage Calc Response:", response.text)

        response.raise_for_status()

        return DamageCalculationResponse.from_dict(
            response.json()
        )