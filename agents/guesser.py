from llm.open_ai import ChatGPTClient
from prompts.guesser import system_prompt, user_prompt
from schemas.agents import NumberChoicesResponse

class GuesserAgent:
    def __init__(self, args: dict = {}, model: str = "gpt-4o-mini"):
        self.model = ChatGPTClient(model=model)

    async def guess_number(self):
        response = await self.model.query(
            messages=[
                {"role": "system", "content": system_prompt.format(num_choices=self.num_choices)},
                {"role": "user", "content": user_prompt.format(num_choices=self.num_choices)}

            ],
            response_format=NumberChoicesResponse
        )
        if not self._verify_response(response):
            return self.guess_number()
        return response

    def _verify_response(self, response: NumberChoicesResponse):
        choices = response.choices
        if len(choices) != self.num_choices:
            return False
        for num in choices:
            if num < 1 or num > 100:
                return False
        return True
