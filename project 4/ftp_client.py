from ftplib import FTP
import getpass

ftp = FTP('')
ftp.connect('192.168.1.9',1470)
username=input()
password=getpass.getpass()
ftp.login(user=username,passwd=password)
direc = input('Enter the path or directory(without filename)')
ftp.cwd(direc)
ftp.retrlines('LIST')


def uploadFile():
	filename = input("Enter filename you wanna upload : ")
	ftp.storbinary('STOR '+filename, open(filename, 'rb'))
	ftp.quit()

def downloadFile():
	filename = input("Enter filename you wanna download : ")
	localfile = open(filename,'wb')
	ftp.retrbinary('RETR '+filename, localfile.write, 1024)
	ftp.quit()
	localfile.close()
#Make required requests here
downloadFile()
