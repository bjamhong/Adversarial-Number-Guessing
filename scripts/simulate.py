import asyncio
from agents.chooser import ChoosingAgent
from agents.guesser import GuesserAgent

class Simulation:
    def __init__(self, num_rounds: int, num_guesses: int):
        self.num_rounds = num_rounds
        self.num_guesses = num_guesses

    async def run(self):
        for i in range(self.num_rounds):
            # Initialize agents
            chooser = ChoosingAgent({"num_choices": 1})
            guesser = GuesserAgent({"num_choices": self.num_guesses})
            
            # Run round
            chosen_number = (await chooser.choose_number()).choice
            guessed_numbers = (await guesser.guess_number()).choices
            
            # Check if guesser won
            guesser_won = chosen_number in guessed_numbers
            
            # Record results
            round_result = {
                "round": i + 1,
                "chosen_number": chosen_number,
                "guessed_numbers": guessed_numbers,
                "winner": "guesser" if guesser_won else "chooser"
            }
            
            # Add to results list
            if not hasattr(self, "results"):
                self.results = []
            self.results.append(round_result)

    def summarize_results(self):
        # Calculate total wins for each player
        total_wins = {"guesser": 0, "chooser": 0}
        for result in self.results:
            total_wins[result["winner"]] += 1

        # Calculate win percentages
        win_percentages = {
            "guesser": total_wins["guesser"] / self.num_rounds,
            "chooser": total_wins["chooser"] / self.num_rounds
        }

        return win_percentages

if __name__ == "__main__":
    simulation = Simulation(num_rounds=100, num_guesses=5)
    asyncio.run(simulation.run())
    print(simulation.summarize_results())
