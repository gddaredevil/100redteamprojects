def caesarEnc():
	sen = input("Encrypt Message: ")
	key = int(input("Enter the Key: "))
	senan = ''
	for i in sen:
		if(i in charUp):
			senan+=charUp[(charUp.index(i)+key)%26]
		elif(i in charDown):
			senan+=charDown[(charDown.index(i)+key)%26]
		else:
			senan+=i
	print('The Encrypted Message: {}'.format(senan))

def caesarDec():
	sen = input("Decrypt Message: ")
	key = int(input("Enter the Key: "))
	senan=''
	for i in sen:
		if(i in charUp):
			senan+=charUp[(charUp.index(i)-key)%26]
		elif(i in charDown):
			senan+=charDown[(charDown.index(i)-key)%26]
		else:
			senan+=i
	print('The Decrypted Message: {}'.format(senan))

if __name__=='__main__':
	print('1. Caesar Encode')
	print('2. Caesar Decode')
	print('0. Exit')
	charUp = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	charDown = 'abcdefghijklmnopqrstuvwxyz'
	while(True):
		n=int(input('Enter your Choice: '))
		if(n==1):
			caesarEnc()
		elif(n==2):
			caesarDec()
		elif(n==0):
			break
		else:
			print("Invalid Input. Choose a valid option")
