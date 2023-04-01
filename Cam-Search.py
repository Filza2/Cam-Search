from rich.console import Console
from requests import get
import re,os
console=Console();total_cam_count=list()


headers={'Host': 'www.insecam.org','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'ar,en-US;q=0.7,en;q=0.3','Accept-Encoding': 'gzip, deflate','Connection': 'close','Cookie': 'Tweakpy=vv1ck','Upgrade-Insecure-Requests': '1'}


def header():
    os.system("cls" if os.name=="nt" else "clear");print("""
 ██████╗ █████╗ ███╗   ███╗      ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
██╔════╝██╔══██╗████╗ ████║      ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
██║     ███████║██╔████╔██║█████╗███████╗█████╗  ███████║██████╔╝██║     ███████║
██║     ██╔══██║██║╚██╔╝██║╚════╝╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
╚██████╗██║  ██║██║ ╚═╝ ██║      ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
 ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
 
                    By @Tweakpy - @vv1ck 
""")
    
    
def Main():
    try:
        header()
        console.print('''
Sort By :

1  - Countries
2  - Place
3  - Camera Manufacturers
        ''')
        sort_by=int(input("Enter Option ID : "))
        if sort_by==1:
            header()
            all_or_one=int(input('1 - One Country\n2 - All Countries\n\nEnter an option from list above : '))
            if all_or_one==1:One_Country()
            elif all_or_one==2:All_Countries()
            else:console.print('- [bold red]Error, option is Not Found ! [/bold red]');exit()
        elif sort_by==2:Place()
        elif sort_by==3:Manufacturers()
        else:console.print('- [bold red]Error, option is Not Found ! [/bold red]');exit()
        
    except Exception as e:
        console.print('- [bold red]Error, this input takes only number ! [/bold red]');exit()
        
        
def One_Country():
    header();cs=['SA','KW','AE','QA','SD','EG','JO','SY','LB','MA','PS','US','GB','CN','JP','TR','FR','SG','SG','RU','DE','UA','ES','-']
    console.print("""
                          [ Country ]
                                       
- Saudi Arabia    [[bold red]SA[/bold red]]                    - United States   [[bold red]US[/bold red]]
- Kuwait          [[bold red]KW[/bold red]]                    - United Kingdom  [[bold red]GB[/bold red]]  
- Palestinian     [[bold red]PS[/bold red]]                    - China           [[bold red]CN[/bold red]]       
- Qatar           [[bold red]QA[/bold red]]                    - Japan           [[bold red]JP[/bold red]]
- Sudan           [[bold red]SD[/bold red]]                    - Turkey          [[bold red]TR[/bold red]]               
- Egypt           [[bold red]EG[/bold red]]                    - France          [[bold red]FR[/bold red]]
- Jordan          [[bold red]JO[/bold red]]                    - Singapore       [[bold red]SG[/bold red]]         
- Syria           [[bold red]SY[/bold red]]                    - Russian         [[bold red]RU[/bold red]]
- Lebanon         [[bold red]LB[/bold red]]                    - Germany         [[bold red]DE[/bold red]]
- Morocco         [[bold red]MA[/bold red]]                    - Ukraine         [[bold red]UA[/bold red]]
- Unknown/Mix     [[bold red]-[/bold red]]                     - Spain           [[bold red]ES[/bold red]]
""")
    country_code=input("Enter Country Code :  ").strip().upper()
    
    if country_code in cs:header()
    else:console.print('- [bold red]Error, Country Code is Not Found ! [/bold red]');exit()
    try:# Get Pages Count or "last page number"
        r=get(f"http://www.insecam.org/en/bycountry/{country_code}",headers=headers)
        pages_count=re.findall(r'pagenavigator\("\?page=", (\d+)',r.text)[0]
    except IndexError:console.print('- [bold red]No Cams Found in index for now , Try another Country ! [/bold red]\n');exit()
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    
    try:# Get Camera Count
        r=get('http://www.insecam.org/en/jsoncountries/',headers=headers)
        if 'success' in r.text:data=r.json()['countries']
        else:console.print('- [bold red]Error, in Getting Count ! [/bold red]\n')
        value=re.findall("'"+country_code+"': {'country': '(.*?)', 'count': (.*?)}",str(data))[0]
        country=str(value[0]);cam_count=str(value[1])
        if country=='-':country='Unknown Mix'
        console.print(f'- Country : [ [bold red]{country}[/bold red] ] Cam Count [ [bold red]{cam_count}[/bold red] ] Country Code : [ [bold red]{country_code}[/bold red] ] \n')
    except Exception as e:pass
    
    try:# Get the cam ip
        for page in range(int(pages_count)):
            r=get(f"http://www.insecam.org/en/bycountry/{country_code}/?page={page}",headers=headers)
            all_cams=re.findall(r"http://\d+.\d+.\d+.\d+:\d+",r.text)
            for cam in all_cams:
                console.print(f'- Camera [bold red]iP[/bold red] : [ [bold red]{cam}[/bold red] ]')
                with open(f'{country}.txt', 'a') as f:
                    f.write(f'{cam}\n')

    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    

def get_pages_count(country_code,country,count):
    try:
        r=get(f"http://www.insecam.org/en/bycountry/{country_code}",headers=headers)
        pages_count=re.findall(r'pagenavigator\("\?page=", (\d+)',r.text)[0]
        get_cam_ip(pages_count=pages_count,country_code=country_code,country=country,count=count)
    except IndexError:get_cam_ip(pages_count=None,country_code=None,country=None,count=None)
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
def get_cam_ip(pages_count,country_code,country,count):
    try:
        header()
        if pages_count==None:pass
        if country=='-':country='Unknown Mix'
        else:
            console.print(f'- Country : [ [bold red]{country}[/bold red] ] Cam Count [ [bold red]{count}[/bold red] ] Country Code : [ [bold red]{country_code}[/bold red] ] ')
            for page in range(int(pages_count)):
                r=get(f"http://www.insecam.org/en/bycountry/{country_code}/?page={page}",headers=headers)
                all_cams=re.findall(r"http://\d+.\d+.\d+.\d+:\d+",r.text)
                for cam in all_cams:
                    console.print(f'\r- Camera [bold red]iP[/bold red] : [ [bold red]{cam}[/bold red] ]',end='\r');total_cam_count.append(cam)
                    with open(f'{country}.txt', 'a') as f:
                        f.write(f'{cam}\n')
    except IndexError:pass
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit() 
def All_Countries():
    header()
    try:
        r=get('http://www.insecam.org/en/jsoncountries/',headers=headers)
        if 'success' in r.text:data=r.json()['countries']
        else:console.print('- [bold red]Error ! [/bold red]');exit()
        for country_code,value in data.items():    
            get_pages_count(country_code=country_code,country=str(value['country']),count=str(value["count"]))
        header();console.print(f'- [bold green]Done[/bold green], The Total Number of extracted cameras : [ [bold red]{len(total_cam_count)}[/bold red] ] .');exit('\n')
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    

def Place():
    header();console.print("""
                                                     [ Place ]
                                       
- Advertisement    [0]              - Education      [11]              - Marina     [22]              - Server    [33]      
- Airliner         [1]              - Entertainment  [12]              - Mountain   [23]              - Service   [34]
- Animal           [2]              - Farm           [13]              - Nature     [24]              - Shop      [35]
- Architecture     [3]              - Hotel          [14]              - Office     [25]              - Sport     [36]
- Barbershop       [4]              - House          [15]              - Park       [26]              - Street    [37]
- Bird             [5]              - Hq             [16]              - Parking    [27]              - Surfing   [38]
- Bridge           [6]              - Kitchen        [17]              - Pool       [28]              - Traffic   [39]
- Cafe             [7]              - Lake           [18]              - Printer    [29]              - Village   [40]
- City             [8]              - Landscape      [19]              - Restaurant [30]              - Warehouse [41]
- Computer         [9]              - Laundry        [20]              - River      [31]              - Weather   [42]
- Construction     [10]             - Mall           [21]              - Road       [32]              - Tv        [43]
""")
    try:place=int(input("Enter Place ID :  "))
    except Exception as e:console.print('- [bold red]Error, this input takes only number ! [/bold red]');exit()
    try:
        pl=[
        'Advertisement','Airliner','Animal','Architecture','Barbershop','Bird',
        'Bridge','Cafe','City','Computer','Construction','Education','Entertainment','Farm',
        'Hotel','House','Hq','Kitchen','Lake','Landscape','Laundry','Mall','Marina',
        'Mountain','Nature','Office','Park','Parking','Pool','Printer','Restaurant',
        'River','Road','Server','Service','Shop','Sport','Street','Surfing','Traffic',
        'Village','Warehouse','Weather','Tv']       
        place=pl[place];place=str(place).strip()
    except IndexError:console.print('- [bold red]Error, Option is Not Found ! [/bold red] ');exit()
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    
    try:# Get Pages Count or "last page number"
        r=get(f"http://www.insecam.org/en/bytag/{place}/",headers=headers)
        pages_count=re.findall(r'pagenavigator\("\?page=", (\d+)',r.text)[0]
    except IndexError:console.print('- [bold red]No Cams Found in index for now , Try another Tag ! [/bold red]\n');exit()
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    
    try:# Get the cam ip
        for page in range(int(pages_count)):
            r=get(f"http://www.insecam.org/en/bytag/{place}/?page={page}",headers=headers)
            all_cams=re.findall(r"http://\d+.\d+.\d+.\d+:\d+",r.text)
            for cam in all_cams:
                console.print(f'- Camera [bold red]iP[/bold red] : [ [bold red]{cam}[/bold red] ]')
                with open(f'{place}.txt', 'a') as f:
                    f.write(f'{cam}\n')
           
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    

def Manufacturers():
    header();console.print("""
                                        [ Manufacturers ]
                                       
- Android-Ipwebcam    [0]              - Foscam         [11]              - Sony           [22]              
- Axis                [1]              - Foscamipcam    [12]              - Sony-Cs3       [23]              
- Axis2               [2]              - Fullhan        [13]              - Stardot        [24]              
- Axismkii            [3]              - Gk7205         [14]              - Streamer       [25]              
- Blueiris            [4]              - Hi3516         [15]              - Sunellsecurity [26]             
- Bosch               [5]              - Linksys        [16]              - Toshiba        [27]            
- Canon               [6]              - Megapixel      [17]              - Tplink         [28]             
- Channelvision       [7]              - Mobotix        [18]              - Vije           [29]              
- Defeway             [8]              - Motion         [19]              - Vivotek        [30]              
- Dlink               [9]              - Panasonic      [20]              - Webcamxp       [31]              
- Dlink-Dcs-932      [10]              - Panasonichd    [21]              - Wificam        [32]             
""")
    try:Manufacturers=int(input("Enter Place ID :  "))
    except Exception as e:console.print('- [bold red]Error, this input takes only number ! [/bold red]');exit()
    try:
        mn=[
        'Android-Ipwebcam','Axis','Axis2','Axismkii',
        'Blueiris','Bosch','Canon','Channelvision',
        'Defeway','Dlink','Dlink-Dcs-932','Foscam',
        'Foscamipcam','Fullhan','Gk7205','Hi3516',
        'Linksys','Megapixel','Mobotix','Motion',
        'Panasonic','Panasonichd','Sony','Sony-Cs3',
        'Stardot','Streamer','Sunellsecurity','Toshiba',
        'Tplink','Vije','Vivotek','Webcamxp','Wificam']   
        Manufacturers=mn[Manufacturers];Manufacturers=str(Manufacturers).strip()
    except IndexError:console.print('- [bold red]Error, Option is Not Found ! [/bold red] ');exit()
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    
    try:# Get Pages Count or "last page number"
        r=get(f"http://www.insecam.org/en/bytype/{Manufacturers}/",headers=headers)
        pages_count=re.findall(r'pagenavigator\("\?page=", (\d+)',r.text)[0]
    except IndexError:console.print('- [bold red]No Cams Found in index for now , Try another Tag ! [/bold red]\n');exit()
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    
    try:# Get the cam ip
        for page in range(int(pages_count)):
            r=get(f"http://www.insecam.org/en/bytype/{Manufacturers}/?page={page}",headers=headers)
            all_cams=re.findall(r"http://\d+.\d+.\d+.\d+:\d+",r.text)
            for cam in all_cams:
                console.print(f'- Camera [bold red]iP[/bold red] : [ [bold red]{cam}[/bold red] ]')
                with open(f'{Manufacturers}.txt', 'a') as f:
                    f.write(f'{cam}\n')
           
    except Exception as e:console.print('- [bold red]Error ! [/bold red]\n');exit()
    
    

Main()
