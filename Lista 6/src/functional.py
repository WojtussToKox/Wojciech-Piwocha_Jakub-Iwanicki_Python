# Zadanie 1 — Programowanie funkcyjne (bez for/while/if)
from functools import reduce

def acronym(words: list[str]) -> str:
    return "".join(map(lambda x: x[0] if len(x)>0 else "", words))

def median(numbers: list) -> float:
    sorted_nums = sorted(numbers)
    n= len(numbers)
    return(sorted_nums[n//2] if n % 2 == 1 else (sorted_nums[n//2] + sorted_nums[n//2 - 1]) / 2)

def pierwiastek(x: float, epsilon: float = 0.01, y: float = 1) -> float:
    return y if abs(y**2 - x) < epsilon else pierwiastek(x, epsilon, (y + x/y)/2)

def make_alpha_dict(text: str) -> dict:
    return {letter: [word for word in text.split() if letter in word] for letter in set(text) if letter.isalpha()}

def flatten(lst: list) -> list:
    return sum([flatten(element) if isinstance(element, (tuple, list)) else [element] for element in lst],[])
    
def group_anagrams(words: list[str]) -> dict:
    keys = set("".join(sorted(word)) for word in words)
    return {
        key: [word for word in words if "".join(sorted(word)) == key] 
        for key in keys
    }

