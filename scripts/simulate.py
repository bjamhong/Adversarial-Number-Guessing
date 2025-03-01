import asyncio
from agents.chooser import ChoosingAgent
from agents.guesser import GuesserAgent
from utils.logger import logger

class Simulation:
    def __init__(self, num_rounds: int, num_guesses: int):
        self.num_rounds = num_rounds
        self.num_guesses = num_guesses
        self.results = None

    async def _round(self, round_num: int, chooser: ChoosingAgent, guesser: GuesserAgent):
        chosen_number = (await chooser.choose_number()).choice
        guessed_numbers = (await guesser.guess_number()).choices
        guesser_won = chosen_number in guessed_numbers
        logger.info(
            f"Round {round_num} results:\n"
            f"\tchosen_number: {chosen_number}\n"
            f"\tguessed_numbers: {guessed_numbers}\n"
            f"\twinner: {'Guesser' if guesser_won else 'Chooser'}"
        )
        return {
            "round": round_num,
            "chosen_number": chosen_number,
            "guessed_numbers": guessed_numbers,
            "winner": "guesser" if guesser_won else "chooser"
        }

    async def run(self):
        chooser = ChoosingAgent()
        guesser = GuesserAgent({"num_choices": self.num_guesses})

        tasks = []
        for i in range(self.num_rounds):
            tasks.append(self._round(i + 1, chooser, guesser))
        results = await asyncio.gather(*tasks)
        self.results = results

    def summarize_results(self):
        total_wins = {"guesser": 0, "chooser": 0}
        for result in self.results:
            total_wins[result["winner"]] += 1

        win_percentages = {
            "guesser": total_wins["guesser"] / self.num_rounds,
            "chooser": total_wins["chooser"] / self.num_rounds
        }

        return win_percentages

if __name__ == "__main__":
    simulation = Simulation(num_rounds=10, num_guesses=5)
    asyncio.run(simulation.run())
    print(simulation.summarize_results())
