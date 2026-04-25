# Zadanie 1 — Programowanie funkcyjne (bez for/while/if)
from functools import reduce

def acronym(words: list[str]) -> str:
    return "".join(map(lambda x: x[0] if len(x)>0 else "", words))

def median(numbers: list) -> float:
    n= len(numbers)
    return(numbers[n//2] if n % 2 == 1 else (numbers[n//2] + numbers[n//2 - 1]) / 2)

def pierwiastek(x: float, epsilon: float = 0.01, y: float = 1) -> float:
    return y if abs(y**2 - x) < epsilon else pierwiastek(x, epsilon, (y + x/y)/2)

def make_alpha_dict(text: str) -> dict:
    return {letter: [word for word in text.split() if letter in word] for letter in set(text) if letter.isalpha()}

def flatten(lst: list) -> list:
    return sum([flatten(element) if isinstance(element, (tuple, list)) else [element] for element in lst],[])
    
def group_anagrams(words: list[str]) -> dict:
    return {
        "".join(sorted(base_word)): [w for w in words if sorted(base_word)==sorted(w)] 
            for base_word in words
            }

