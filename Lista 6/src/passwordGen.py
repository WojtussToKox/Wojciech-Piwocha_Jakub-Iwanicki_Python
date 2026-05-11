import string
import random
class PasswordGenerator:
    def __init__(self, length: int, count: int, charset: list[str] = string.ascii_letters + string.digits):
        if length <= 0:
            raise ValueError("Długość hasła musi być liczbą dodatnią")
        if count <= 0:
            raise ValueError("Maksymalna liczba haseł musi być liczbą dodatnią")
        
        self.length = length
        self.count = count
        self.charset = charset
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count <= 0:
            raise StopIteration
        
        self.count -= 1
        
        return "".join(random.choices(self.charset, k=self.length))
    
def main():
    print("TESTOWANIE GENERATORA")
    
    lim_gen = PasswordGenerator(3, 3,['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    def_gen = PasswordGenerator(10, 10)
    
    
    print("\nLIMITED GEN\n")
    for password in lim_gen:
        print(password)
    
    
    print("\nDEFAUTL GEN\n")
    for password in def_gen:
        print(password)
        
    print("\nTESTOWANIE NEXT\n")
    gen = PasswordGenerator(10, 5)
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    #print(next(gen))
    #test_gen = PasswordGenerator(-2, -10)
    
        
if __name__ == "__main__":
    main()