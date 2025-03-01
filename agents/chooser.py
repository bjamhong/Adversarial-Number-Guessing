from llm.open_ai import ChatGPTClient
from prompts.chooser import system_prompt, user_prompt
from schemas.agents import NumberChoiceResponse

class ChoosingAgent:
    def __init__(self, args: dict = {}, model: str = "gpt-4o-mini"):
        self.model = ChatGPTClient(model=model)
    
    async def choose_number(self):
        response = await self.model.query(
            messages=[
                {"role": "system", "content": system_prompt.format()},
                {"role": "user", "content": user_prompt.format()}
            ],
            response_format=NumberChoiceResponse
        )
        if not self._verify_response(response):
            return self.choose_number()
        return response
        
    def _verify_response(self, response: NumberChoiceResponse):
        num = response.choice
        if num < 1 or num > 100:
            return False
        return True
