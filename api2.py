import requests
import json

def getRandomImage():
	url='https://dog.ceo/api/breeds/image/random'
	response=requests.get(url)
	

	if response.status_code==200:
		data=response.json()
		print ('image:',data['message'])
	
	else:
		print ('İstek başarısız, Durum Kodu:',response.status_code)



if __name__=="__main__":
	getRandomImage()

