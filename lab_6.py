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
			return (self.text*pow(self.k,self.d,self.n))%self.n, self.k

		def decrypt(self,S):
			return (S*inverse_of(self.k,self.n))%self.n

		def decrypt(self,key,S):
			return (S*inverse_of(key,self.n))%self.n
		
		def get_dec_key(self,k):
			return inverse_of(pow(k,self.d,self.n),self.n)


		
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

	def sign(self,keys):
		for i in range(len(self.Zs)):

			if (self.Zs[i]*keys[i])%(self.p*self.q)%3==0:
				return ERR('Cheater!')
				
		return OK(pow(self.element_to_sign,self.e,self.p*self.q))

	def get_keys_info(self):
		return {'secret':(self.e,self.p*self.q),'open':(self.d,self.p*self.q)}

	def validate_sign(self,x,sign):
		if pow(x,self.e,(self.p*self.q))==sign:
			return True
		else:
			return False

	def get_Zs(self, Zs):
		self.Zs=Zs
		index=random.randint(0,len(Zs)-1)
		self.element_to_sign=self.Zs.pop(index)
		return index


def blinded_sign():
	A=owner()
	T=trans()
	A.set_keys(T.generateKeys())#p,q,e
	print (T.get_keys_info())
	print ('Preparing texts')
	msgs=[2**i for i in range(0,100)]
	msgs[4]=3
	Zs=[]	#list of encrypted msgs (z,k)
	for m in msgs:
		print(m)
		A.set_text(m)
		Zs.append(A.encrypt())
	k=T.get_Zs(list(map((lambda x:x[0]),Zs)))	#T choose one element to sign
	print('Signing will for ',msgs[k])
	x=msgs[k]
	key=Zs.pop(k)[1]#k of choosen element
	dec_keys=[]
	for i in range(len(Zs)):
		dec_keys.append(A.get_dec_key(Zs[i][1]))# z'=k**(-d) z'*z=x

	sign=T.sign(dec_keys)
	if sign['status']:
		y=A.decrypt(key,sign['value'])
		print('sign is ',T.validate_sign(x,y))
	else:
		print(sign['value'])
	
blinded_sign()
#(3*pow(32,31,77)*inverse_of(pow(32,31,77),77))%77