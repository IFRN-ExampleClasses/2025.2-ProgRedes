import threading

def mostrar_primos(n: int):
    for val in range(2, n+1):
        ndiv = 0
        for d in range (1, val+1):
            if val % d == 0:
                ndiv += 1
        if ndiv == 2:
            print (f"{val} eh primo.")
            
def collatz(n : int):
    for val in range(1, n+1):
        n = val
        tam = 1
        while (n != 1):
            if n%2 == 0:
                n //= 2
            else:
                n = 3 * n +1
            tam += 1
        print (f"O tamnho da sequencia de collatz para {val} eh {tam}. ")

t1 = threading.Thread(target=mostrar_primos, args=(100, ))
t1.start()
t2 = threading.Thread(target=collatz, args=(100, ))
t2.start()
#collatz(10000)
print ("FIM")