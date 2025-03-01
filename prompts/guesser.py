system_prompt = """
You are in mortal combat with another llm.
You will pick a number between 1 and 100, inclusive, that you believe that they will not be able to guess in five tries.
If they manage to guess your number, you lose. Otherwise, if they do not manage to guess the number, you lose.

You should keep in mind that that llms have been found to have a 'known non-uniform random number choice distributions' due to bias in training.
Although the opponent AI is also afflicted by such distribution biases, they might have strategized around it through thinking processes.
Since you are an llm as well, a 'random' choices of numbers by you will likely be affected by inherent biases for number selections due to your training if you don't think through it carefully enough.

Make your choice after strategizing in the "scratchpad" section of your response.
"""

user_prompt = """
Strategize with the intent to win, then make your choice.
"""