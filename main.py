import requests
from lxml import html
from fake_useragent import UserAgent
from pprint import pprint
import time
import json


ua=UserAgent()
headers={"User-Agent":ua.random} #делаем агента

session = requests.Session()# делаем ссесию. Агент и сессия нужны для предотвращения блокировки сайтом

#Фигачу запрос на главную страницу сайта
url = "https://data.worldbank.org"
response = session.get(url+"/country?_gl=1*j81loa*_gcl_au*MTk0MjI3ODA4NC4xNzI1NzMwNTIw",headers=headers)
# print(response.text)
dom=html.fromstring(response.text) #получаю страницу с перечнем стран



navs=dom.xpath("//section[@class='nav-item']")#страны расположены блоками по алфавиту - чтобы добраться к стране нужно сперва попасть в такой блок
countries=[]
n=0
for nav in navs:#движемся по алфавитным блокам
    a=nav.xpath(".//a")#Хвала небесам! Страны содержаться в ссылках! Получаем их! Иначе как перебором алфавитных блоков к ссылкам со странами не подобраться, т.к. ссылки не имеют селекторов!
    for item in a: # перебераем уже ссылки со странами
        print(item.xpath("./text()")[0],item.xpath("./@href")[0]) #Извлекаем из ссылки ее текстовое содержимое (название страны) и саму ссылку
        sub_response = session.get(url+item.xpath("./@href")[0],headers=headers)#переходим по полученой ссылке
        
        page=html.fromstring(sub_response.text)# получаем эту страницку
        
        indexes=page.xpath("//div[@class='indicator-item__inner']")#получаем блоки с показателями
        arr={}
        num=0
        for index in indexes:#и проходим по блокам с показателями
          
            num+=1
            try:
                index_name=index.xpath(".//div[@class='indicator-item__title']/a/text()")[0] #получаем название показателя
            except Exception as e: 
                index_name = None #или не получаем
                print(f"An error occurred: {e}")
                print("cannot take index")
        
            
            try:
                index_value=index.xpath(".//div[@class='indicator-item__data-info']//text()")[0]# получаем его значение
            except Exception as e:
                index_value = None #или не получаем
                print(f"An error occurred: {e}")
                print("cannot take value of index")
                
            print(index_name,index_value) 
            arr[index_name]=index_value # из полученного формируем словарь: название индекса-ключ, значение -значение
            print(num)
            
            # time.sleep(1)

        temp={}
        temp[item.xpath("./text()")[0]]=arr #кладем словарь в словарь, где сам словарь - значение нового словаря, а ключ - название страны
        countries.append(temp)# кладем последний словарь в список
        time.sleep(1)# спим!



pprint(countries)# выводим список


with open("countries.json","w") as f:
    json.dump(countries,f)# все ложим кладем в файл json. Ща переложу в csv!