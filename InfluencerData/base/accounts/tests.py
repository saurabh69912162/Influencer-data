# url = "https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&mine=true&key=ya29.Il-yB1i8Xt1baKvpNP_ZoUdUzW4y3jl_AS1jrW80zVegLdd-o_-YJ1zCZGjaRGiv3Dq-OFYZ4WFRQiwg609tI2iOBtqHsk5s1W4_rx0pDA9HOoEa40sGiDzeBKacxDqDTg"
# text = 'Bearer '+ 'ya29.Il-yB1i8Xt1baKvpNP_ZoUdUzW4y3jl_AS1jrW80zVegLdd-o_-YJ1zCZGjaRGiv3Dq-OFYZ4WFRQiwg609tI2iOBtqHsk5s1W4_rx0pDA9HOoEa40sGiDzeBKacxDqDTg'
# headers = {
# 'Authorization': text,
# }
# import requests
# response = requests.request("GET", url, headers=headers)
# print(response.text)
#
#
#

test = 'Saurabh'
string = 'SAurabh'
if test.casefold() in string.casefold():
    print('1')
else:
    print('2')