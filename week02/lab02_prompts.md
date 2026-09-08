# Lab 02 CLI comparison journal

Do not include passwords, tokens, API keys, or complete authentication output.

## Tool check

### GitHub Copilot CLI

I installed and authenticated GitHub Copilot CLI successfully. I verified that it runs from the terminal without displaying any authentication errors. Copilot CLI 1.0.82.

### Antigravity CLI

I installed and authenticated Antigravity CLI successfully. I verified that it runs from the terminal without displaying any authentication errors. Antigravity CLI 1.1.23

## Shared task

### Shared prompt



```text
Create a Python function named count_vowels(text: str) -> int that counts the vowels a, e, i, o, and u in a string without regard to uppercase or lowercase. Do not count y as a vowel. Keep the solution simple and explain how it works. 
```

### Copilot CLI observations

Copilot CLI suggested creating a set containing the five vowels and then checking each character of the provided text against that set. It used the lower method so uppercase and lowercase vowels would both be counted. The solution appeared concise, but I would want to verify that it returns the correct number for uppercase text, empty strings, text without vowels, and words containing the letter y. 

### Antigravity CLI observations

Antigravity CLI also suggested creating a set containing a, e, i, o, and u. It converted the entire input to lowercase and used a generator expression to add one for every vowel it found. Antigravity gave a more detailed explanation of how each part of the code worked. I would still verify the solution with tests to make sure uppercase vowels, empty strings, and the letter y are handled correctly.


### Comparison

Both Copilot CLI and Antigravity CLI suggested similar and correct approaches for the count_vowels function. Both used a set containing a, e, i, o, and u and handled uppercase letters by converting characters to lowercase. The main difference was how they counted the vowels. Copilot summed Boolean results, while Antigravity explicitly added one whenever a vowel was found. Antigravity also provided a much more detailed explanation of how its code worked, which made its response easier for me to understand. Copilot's response was shorter and more direct, but it assumed more knowledge about how Python handles True and False values. I preferred Antigravity's approach because the counting process was more obvious and easier to follow.

## Test-guided implementation

After completing the three required functions, I ran the provided pytest command to check my implementation. All nine tests for the Python functions passed. The tests checked the greeting function with simple names, multiword names, and an empty name. They also tested even and odd numbers, including zero and negative values. For count_vowels, the tests verified uppercase and lowercase vowels, text with no vowels, and empty text. I compared the two CLI suggestions and selected Antigravity's approach because I found its counting method easier to understand. Since all of the Python behavior tests passed, I did not need to revise the functions further. The results confirmed that my final code matches the required function contracts.



## Preferred tool combination

Browser chat, GitHub Copilot in VS Code, Copilot CLI, and Antigravity CLI can each help me in different ways. Browser chat is useful when I need a detailed explanation or step-by-step help with something I do not understand. GitHub Copilot in VS Code is convenient because it can suggest code while I am already working on a file. Copilot CLI is useful for working directly from the terminal and making changes to files in a repository. Antigravity CLI was helpful because it gave a detailed explanation of the code it suggested and how each part worked. Right now, I prefer using VS Code along with browser chat and Antigravity because I can work on my files while getting explanations. As I learn more Python, I may prefer Copilot because I might need less explanation and want faster code suggestions.

