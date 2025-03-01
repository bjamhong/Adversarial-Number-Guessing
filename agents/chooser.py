from llm.open_ai import ChatGPTClient
from prompts.chooser import system_prompt, user_prompt
from schemas.agents import NumberChoicesResponse

class ChoosingAgent:
    def __init__(self, args: dict, model: str = "gpt-4o-mini"):
        self.model = ChatGPTClient(model=model)
        self.num_choices = args["num_choices"]

    def choose_number(self):
        response = self.model.query(
            messages=[
                {"role": "system", "content": system_prompt.format(num_choices=self.num_choices)},
                {"role": "user", "content": user_prompt.format()}
            ],
            response_format=NumberChoicesResponse
        )
        if not self._verify_response(response):
            return self.choose_number()
        return response
        
    def _verify_response(self, response: NumberChoicesResponse):
        choices = response.choices
        if len(choices) != 1:
            return False
        num = choices[0]
        if num < 1 or num > 100:
            return False
        return True
