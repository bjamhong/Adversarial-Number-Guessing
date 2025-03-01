from llm.open_ai import ChatGPTClient
from prompts.random_chooser import user_prompt
from schemas.agents import RandomNumberResponse

class RandomChooserAgent:
    def __init__(self, args: dict = {}, model: str = "gpt-4o-mini"):
        self.model = ChatGPTClient(model=model)

    def choose_number(self):
        response = self.model.query(
            messages=[
                {"role": "user", "content": user_prompt.format()}
            ],
            response_format=RandomNumberResponse
        )
        if not self._verify_response(response):
            return self.choose_number()
        return response

    def _verify_response(self, response: RandomNumberResponse):
        num = response.choice
        if num < 1 or num > 100:
            return False
        return True
