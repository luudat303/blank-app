import requests

from datetime import timedelta, datetime
import logging
import os, sys, json 
from http.client import HTTPConnection
HTTPConnection.debuglevel = 1

# logging.basicConfig()

# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format)
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger('Similar-Web')
logger.setLevel(logging.INFO)
class SimilarWeb():
    month_back = os.environ.get('SW_MONTH_BACK',0)
    def __init__(self ):
        self.url = "https://pro.similarweb.com"
        self.session = requests.Session()
        self.cookies= {}
        self.headers = {
            "dnt": "1",
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://pro.similarweb.com/',
            'sec-ch-ua': '''"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"''',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0""",
            'x-requested-with': 'XMLHttpRequest' ,
            'x-sw-page': 'https://pro.similarweb.com/#/digitalsuite/websiteanalysis/overview/website-performance/*/999/1m?webSource=Total&key=theluxurycloset.com',
            'x-sw-page-view-id': '5dce44d1-bf27-4b19-8524-e01c12ea9ba9',
            'accept': "application/json",
            "content-type": "application/json; charset=utf-8",
            "cache-control": "no-cache"
            }
        self.toDate, self.fromDate = self.getToDateAndFromDate()
    
    
    def set_domain(self, domain):
        self.domain = domain
         
    def getToDateAndFromDate(self):
        # get last day of previous month
        date = datetime.now()
        last_day = date.replace(month=(date.month - int(self.month_back))).replace(day=1) - timedelta(days=1)
        toDate = last_day.strftime("%Y|%m|%d")
        # get first day of last 3 months
        date = datetime.now() 
        first_day = date.replace(month=(date.month - 1 - int(self.month_back))).replace(day=1) 
        fromDate = first_day.strftime("%Y|%m|%d")
    
        return toDate, fromDate
    
    def set_cookies(self,cookies):
        if isinstance(cookies, str):
            tmp = {}
            cookies = cookies.split("; ")
            if len(cookies) < 2:
                return ""
            
            for cookie in cookies:
                print(cookie)
                cookie = cookie.strip()
                key ,_, value  = cookie.partition("=")
                self.cookies[key] = value
            
        elif isinstance(cookies, dict):
            self.cookies =  cookies
            
    
    def send(self, uri, params):
        url = f"{self.url}/{uri}" 
        try:
            rtn = self.session.get(url ,params=params, headers=self.headers,cookies=self.cookies)
            if rtn.status_code == 200:
                data = rtn.json()
                data['success'] = True
                return data
            
            else: 
                logger.error(f"Can't authenticate with Similarweb : {self.url}")

        except Exception as e : 
            logger.error(e)
            
        return {
            'success': False,
            'return_code': rtn.status_code,
            'status': False
        }

    def country_converted(self, country_code):
        country ={ 
            840: "United States", 276: "Germany", 76: "Brazil", 643: "Russia",
            826: "United Kingdom", 764: "Thailand", 356: "India", 380: "Italy",
            250: "France", 724: "Spain", 616: "Poland", 528: "Netherlands",  36: "Australia",
            124: "Canada", 158: "Taiwan", 348: "Hungary", 392: "Japan", 484: "Mexico", 410: "Korea, Republic of", 
            752: "Sweden", 360: "Indonesia", 578: "Norway", 682: "Saudi Arabia", 398: "Kazakhstan",   704: "Vietnam",
            608: "Philippines", 246: "Finland", 208: "Denmark", 792: "Turkey", 620: "Portugal", 642: "Romania",
            156: "China", 40: "Austria", 218: "Ecuador", 32: "Argentina", 702: "Singapore", 604: "Peru", 756: "Switzerland",
            170: "Colombia", 203: "Czech Republic", 458: "Malaysia", 112: "Belarus", 804: "Ukraine", 818: "Egypt",
            586: "Pakistan", 710: "South Africa", 56: "Belgium", 368: "Iraq", 784: "United Arab Emirates", 554: "New Zealand",
            152: "Chile", 344: "Hong Kong", 50: "Bangladesh", 376: "Israel", 372: "Ireland", 504: "Morocco", 703: "Slovakia",
            414: "Kuwait", 300: "Greece", 288: "Ghana", 566: "Nigeria", 100: "Bulgaria", 428: "Latvia", 233: "Estonia", 634: "Qatar",
            191: "Croatia", 144: "Sri Lanka", 404: "Kenya", 440: "Lithuania", 600: "Paraguay", 231: "Ethiopia", 705: "Slovenia",
            688: "Serbia", 862: "Venezuela", 524: "Nepal", 12: "Algeria", 400: "Jordan", 388: "Jamaica", 788: "Tunisia",
            512: "Oman", 320: "Guatemala", 214: "Dominican Republic", 116: "Cambodia", 558: "Nicaragua",
            196: "Cyprus", 887: "Yemen", 31: "Azerbaijan", 70: "Bosnia and Herzegovina", 68: "Bolivia", 807: "Macedonia, the former Yugoslav Republic of"
            }
        try:
            return country[country_code]
        except:
            return country_code
            
    
    def ApiWebsiteOverview_header(self):
        path = "api/WebsiteOverview/getheader"
        params = { "key": self.domain,
                  "mainDomainOnly": True,
                  "includeCrossData": False
                }
        data = self.send(path, params)
        if data['success']:
            domain = list(data.keys())[0]
            return {
                'site': self.domain,
                'tags': data[domain]['tags'],
                'title': data[domain]['title'],
                'description': data[domain]['description'],
                'category': data[domain]['category'],      
                'yearFounded': data[domain]['yearFounded'],
                'globalRanking': data[domain]['globalRanking']
                }
        return None
        
    def ApiWebsiteOverview_EngagementOverview(self,country=999, webSource="Total"):
        #limit data 1 month
        date = datetime.now()
        from_date = date.replace(month=(date.month - 1 - int(self.month_back))).replace(day=1)
        
        path = "widgetApi/WebsiteOverview/EngagementOverview/Table"
        params= {
            "country": country,
            "to": self.toDate ,
            "from": from_date.strftime("%Y|%m|%d"),
            "isWindow": False,
            "webSource": webSource,
            "isDurationChanged": "true",
            "ignoreFilterConsistency": False,
            "includeSubDomains": False,
            "timeGranularity": "Monthly",
            "keys": self.domain,
            "ShouldGetVerifiedData": False
        }
        data = self.send(path,params)
        if data['success']:
            data =  data['Data'][0]
     
            rtn = {}
            for opt in ['BounceRate', 'AvgMonthVisits', 
                        'AvgVisitDuration','PagesPerVisit','TotalPagesViews']:
                try: 
                    rtn[opt] = data[opt]
                except:
                    rtn[opt]=  None 
            return rtn

        return None
    
    def ApiMarketingMixTotal_TrafficSourcesOverview(self, country=999):
        path = 'widgetApi/MarketingMixTotal/TrafficSourcesOverview/PieChart'
        params = {
            "country": country,
            "to": self.toDate ,
            "from": self.fromDate,
            "isWindow": False,
            "includeSubDomains": True,
            "timeGranularity": 'Monthly',
            "keys": self.domain
        }
      
        data = self.send(path,params)
        if data['success']:
            data =  data['Data']

            return {
                'Desktop': data['Desktop'][self.domain],
                'MobileWeb': data['MobileWeb'][self.domain],
                'Total': data['Total'][self.domain],
            }
        return None
    
    def ApiSearchBrandedKeywordsWorldWide_Branded(self,country=999,webSource="Total"):
        path = 'widgetApi/TrafficSourcesSearch/SearchBrandedKeywordsWorldWide/WebsitePerformance/PieChart'
        params =  {
            "country": country,
            "to": self.toDate ,
            "from": self.fromDate,
            "isWindow": False,
            "includeSubDomains": False,
            "timeGranularity": 'Monthly',
            "keys": self.domain,
            "webSource": webSource,
            "duration": '3m'
        }
        
        
        data = self.send(path,params)
        if data['success']:         
            data = list(data['Data'].values())[0]
            return {
                'NoneBranded': data['NoneBranded'],
                'Branded': data['Branded'],
            }
        return None
    
    def ApiNewSearchKeywordsWorldWide_Keyword(self,country=999,webSource='webSource'):
        path = 'widgetApi/SearchKeywords/NewSearchKeywordsWorldWide/WebsitePerformance/Table'
        params = {
            'country': country,
            'to': self.toDate,
            'from': self.fromDate,
            'isWindow': False,
            'includeSubDomains': False,
            'webSource': 'webSource',
            'keys': self.domain,
            'IncludeOrganic': False,
            'IncludePaid': True,
            'IncludeBranded': False,
            'IncludeNoneBranded': True,
            'pageSize': 20,
            # "orderBy": "Share+desc"
        }
        keywords = {}
        data = self.send(path,params)
        logger.error(data)
        logger.error("########################################################")
        if data['success']:
            data = data['Data']
            for k  in data : 
                if k['SearchTerm'] != 'grid.upgrade': 
                       keywords[k['SearchTerm']] = {
                           'CPC': k['CPC'],
                            'KwVolume': k['KwVolume']
                    }    
                
        params['IncludeBranded'] = True 
        params['IncludeNoneBranded'] = True
        data = self.send(path,params)
        logger.error(data)
        if data['success']:
            data = data['Data']
        for k  in data : 
            if k['SearchTerm'] != 'grid.upgrade': 
                keywords[k['SearchTerm']] = {
                    'CPC': k['CPC'],
                    'KwVolume': k['KwVolume'],
                    'TotalShare': k['TotalShare'],
                    'Paid': k['Paid']
 

                }
        return keywords
                    
    def ApiWebsitePaidSearchAds(self,country=999,webSource='Desktop'):
        uri = 'api/WebsitePaidSearchAds/Table?'
        today = datetime.now()
        from_date =  today.replace(month=(today.month - 1 - int(self.month_back))).replace(day=1).strftime("%Y|%m|%d")
        params = {
            'country': country,
            'to': self.toDate ,
            'from': from_date,
            'isWindow': False,
            'includeSubDomains': True,
            'webSource': webSource,
            'key': self.domain
        }
              
        data = self.send(uri, params)
        return data       
   
    def getTopCountry(self):
        uri = 'widgetApi/WebsiteGeography/Geography/Table'
        params = {
            'country': 999,
            'includeSubDomains': True,
            'webSource': 'Total',
            'timeGranularity': 'Monthly',
            'orderBy': 'TotalShare desc',
            'keys': self.domain,
            'pageSize': 5,
            'from': self.fromDate,
            'to': self.toDate,
            'isWindow': False
        }
        rtn = self.makeRequest(uri, params)
        data = rtn['Data']
        Country = rtn['Filters']['country']
        report = []  
        for k in data: 
            tmp = {
                'Country':  self.mapCountry(k['Country'], Country),
                'Share': self.formatNum(k['Share']*100)
            }
            report.append(tmp)
        return report
    

        