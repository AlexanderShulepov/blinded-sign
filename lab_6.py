import random
from sugar import *
import gost
class owner():
		def __init__(self):
			pass

		def set_text(self,text):
			self.text=text

		def set_keys(self,keys):
			self.n=keys['n']
			self.d=keys['d']

		def encrypt(self):
			self.k=get_k(self.n)
			#print('k',self.k)
			return (self.text*pow(self.k,self.d,self.n))%self.n, self.k

		def decrypt(self,S):
			return (S*inverse_of(self.k,self.n))%self.n
		
		def get_dec_key(self,k):
			return pow(k,inverse_of(self.d,self.n),self.n)


		
class trans():
	def __init__(self):
		pass
	def generateKeys(self):
		self.p=gost.generate()
		self.q=gost.generate()

		phi=(self.p-1)*(self.q-1)
		e = random.randrange(1, phi)
		g=gcd(e,phi)
		while g != 1:
			e = random.randrange(1, phi)
			g = gcd(e, phi)
		d=inverse_of(e,phi)
		self.e=e
		self.d=d
		return {'n':self.p*self.q,'d':d}
	def sign(self,msg):
		return pow(msg,self.e,self.p*self.q)

	def get_keys_info(self):
		return {'secret':(self.e,self.p*self.q),'open':(self.d,self.p*self.q)}

	def validate_sign(self,x,sign):
		if pow(x,self.e,(self.p*self.q))==pow(x,self.e,(self.p*self.q)):
			return True
		else:
			return False
	def get_Zs(self, Zs):
		self.Zs=Zs
		return random.randint(0,len(Zs))
def blind_sign():
	x=879749327239
	print('text',x)
	A=owner()
	A.set_text(x)
	T=trans()
	A.set_keys(T.generateKeys())
	print(T.get_keys_info())
	z=A.encrypt()
	print(z)
	s=T.sign(z)
	y=A.decrypt(s)
	print ('sign',y)
	###############
	print('sign is ',T.validate_sign(x,y))
	print('---------------')

def blinded_sign():
	A=owner()
	T=trans()
	A.set_keys(T.generateKeys())
	Zs=[]
	for i in range(8):
		A.set_text(2**i)
		Zs.append(A.encrypt())

	k=T.get_Zs(list(map((lambda x:x[1]),Zs)))
	keys=[]
	for i in Zs:
		keys.append(A.get_dec_key())
	sign=T.sign
blinded_sign()
#(3*pow(32,31,77)*inverse_of(pow(32,31,77),77))%77