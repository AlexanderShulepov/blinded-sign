from math  import sqrt
import random
def OK(value=""):
	return {"status":True,"value":value}

def ERR(value=""):
	return {"status":False,"value":value}

def dot(x,y,z=None):
	return {"x":x,"y":y} if z==None else {"x":x,"y":y,"z":z}




def sqr_is_int(arg):
	return True if sqrt(arg) - int(sqrt(arg))==0 else False

def extended_euclidean_algorithm(a, b):
    """
    Возвращает кортеж из трёх элементов (gcd, x, y), такой, что
    a * x + b * y == gcd, где gcd - наибольший
    общий делитель a и b.

    В этой функции реализуется расширенный алгоритм
    Евклида и в худшем случае она выполняется O(log b).
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(n, p):
    """
    Возвращает обратную величину
    n по модулю p.

    Эта функция возвращает такое целое число m, при котором
    (n * m) % p == 1.
    """
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        # Или n равно 0, или p не является простым.
        return False
    else:
        return x % p
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
def test_q(a,p):
    arr=[]
    for i in range(p-1):
        if pow(a,i,p) in arr:
            return False
        arr.append(pow(a,i,p))
    return True

def getk(p):
    for q in range(1,p):
        if test_q(q,p):
            #print('q',q)
            k=random.randint(1,100)
            #print('k',k)
            return pow(q,k,p)
def get_k(p):
    while  True:
        k=random.randint(1,p)
        if inverse_of(k,p):
            return k  