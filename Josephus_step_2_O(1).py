import math
def josephus(n):
  # for k=2: n=(2**m)+p, winner=2p+1
  return( 2*(n-pow(2,math.floor(math.log(n,2))))+1)


# n=100, k=2, winner =73
# n=14, k=2, winner =13
# n=5, k=2, winner =3
