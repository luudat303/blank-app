import requests
import datetime
import logging
import os, sys, json 

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format)
logger = logging.getLogger('Similar-Web')
logger.setLevel(logging.INFO)
class similarweb():
 
    def __init__(self, domain, cookies):
        self.url = "https://pro.similarweb.com"
        self.domain = domain
        self.cookies = cookies
        self.session = requests.Session()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.207.132.170 Safari/537.36",
            'sec-ch-ua': 'Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
            }
        self.cookies = cookies
        self.toDate, self.fromDate = self.getToDateAndFromDate()
    
    def getToDateAndFromDate(self):
        # get last day of previous month
        date = datetime.now()
        last_day = date.replace(month=(date.month - int(self.month_back))).replace(day=1) - timedelta(days=1)
        toDate = last_day.strftime("%Y|%m|%d")
        # get first day of last 3 months
        date = datetime.now() 
        first_day = date.replace(month=(date.month - 3 - int(self.month_back))).replace(day=1) 
        fromDate = first_day.strftime("%Y|%m|%d")
    
        return toDate, fromDate
    
    def send(self, uri, params):
        url = f"{self.url}/{uri}" 
        try:
            rtn = self.session.get(url ,params=params)
            if rtn.status_code == 200:
                return rtn.json()
            else: 
                logger.error(f"Can't authenticate with Similarweb : {self.url}")

        except Exception as e : 
            logger.error(e)
        return None

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
        params = { "domain": self.domain,
                  "mainDomainOnly": True,
                  "includeCrossData": False
                }
        data = self.send(path, params)
        domain = list(data.keys())[0]
        return {
            'site': self.domain,
            'tags': data[domain]['tags'],
            'title': data[domain]['title'],
            'description': data[domain]['description'],
            'category': data[domain]['category'],      
            'yearFounded': data[domain]['category'],
            'globalRanking': data[domain]['globalRanking']
            }
        
    def ApiWebsiteOverview_EngagementOverview(self):
        path = "widgetApi/WebsiteOverview/EngagementOverview/Table"
        params= {
            "country": 999,
            "to": self.toDate ,
            "from": self.fromDate,
            "isWindow": False,
            "webSource": 'Total',
            "isDurationChanged": "null",
            "isCountryChanged": "null",
            "ignoreFilterConsistency": False,
            "includeSubDomains": True,
            "timeGranularity": "Monthly",
            "keys": self.domain,
            "ShouldGetVerifiedData": False
        }
        data = self.send(path,params)['Data'][0]
        rtn = {}
        for opt in ['BounceRate', 'AvgMonthVisits', 
                    'AvgVisitDuration','PagesPerVisit','TotalPagesViews']:
            try: 
                rtn[opt] = data[opt]
            except:
                rtn[opt]=  None 
        return rtn
    
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
      
        data = self.send(path,params)['Data'][0]
        return {
            'Desktop': data['Desktop'][self.domain]['Desktop'],
            'MobileWeb': data['Desktop'][self.domain]['MobileWeb'],
            'Total': data['Desktop'][self.domain]['Total'],
        }
    
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
        
        
        data = list(self.send(path,params)['Data'].values())[0]
        return {
            'NoneBranded': data['NoneBranded'],
            'Branded': data['Branded'],
        }
    
    def ApiNewSearchKeywordsWorldWide_Keyword(self,country=999):
        path = 'widgetApi/SearchKeywords/NewSearchKeywordsWorldWide/WebsitePerformance/Table'
        params =  {
            "country": country,
            "to": self.toDate ,
            "from": self.fromDate,
            "isWindow": False,
            "includeSubDomains": True,
            "timeGranularity": 'Monthly',
            "keys": self.domain,
            "webSource": 'Total',
            "duration": '3m'
        }
        return {
            'NoneBranded': "{:.2f}".format(NoneBranded/sum *100),
            'Branded': "{:.2f}".format(Branded/sum*100)
        }
    
    def getSearchKeywordsWeight(self):
        
        uri = 'widgetApi/TrafficSourcesSearch/SearchBrandedKeywordsWorldWide/PieChart'
        params = {
            "country": 999,
            "to": self.toDate ,
            "from": self.fromDate,
            "isWindow": False,
            "includeSubDomains": True,
            "timeGranularity": 'Monthly',
            "keys": self.domain,
            "webSource": 'Total',
            "duration": '3m'
        }
        rtn = list(self.makeRequest(uri, params)['Data'].values())[0]
        
        NoneBranded = rtn['NoneBranded']
        Branded = rtn['Branded']
        sum = NoneBranded + Branded
        logger.debug("Get search keyword weight: ")
        logger.debug("NoneBranded: {:.2f}".format(NoneBranded/sum *100))
        logger.debug("Branded: {:.2f}".format(Branded/sum*100))
        return {
            'NoneBranded': "{:.2f}".format(NoneBranded/sum *100),
            'Branded': "{:.2f}".format(Branded/sum*100)
        }
    
    def getPaidSearchAds(self):
        uri = 'api/WebsitePaidSearchAds/Table?'
        today = datetime.now()
        from_date =  today.replace(month=(today.month - 1 - int(self.month_back))).replace(day=1).strftime("%Y|%m|%d")
        params = {
            'country': 999,
            'to': self.toDate ,
            'from': from_date,
            'isWindow': False,
            'includeSubDomains': True,
            'webSource': 'Desktop',
            'key': self.domain
        }
        
        rtn = self.makeRequest(uri, params)
        logger.debug(f"Get total number paids ads: {rtn['TotalCount']}")
        return { 'TotalAdsCount': rtn['TotalCount'] }
    
    def getSearchKeywords(self):
        uri = 'widgetApi/SearchKeywords/NewSearchKeywordsWorldWide/Table'
        params = {
            'country': 999,
            'to': self.toDate,
            'from': self.fromDate,
            'isWindow': False,
            'includeSubDomains': False,
            'webSource': 'Desktop',
            'keys': self.domain,
            'IncludeOrganic': False,
            'IncludePaid': True,
            'IncludeBranded': True,
            'IncludeNoneBranded': True,
            'pageSize': 10
        }
        data = []
        # make list Paid and branded  keywords
        params['IncludeOrganic'] = False 
        params['IncludePaid'] = True
        params['IncludeBranded'] = True
        params['IncludeNoneBranded'] = False
        logger.debug("List Paid and Branded  keywords")
        rtn = self.makeRequest(uri, params)['Data']
        for k  in rtn : 
            if k['SearchTerm'] != 'grid.upgrade': 
                tmp = {
                    'SearchTerm': k['SearchTerm'],
                    'CPC': k['CPC'],
                    'KwVolume': k['KwVolume']
                }
                if tmp not in data:
                    data.append(tmp)
        # make list Paid and None-branded keywords
        params['IncludeOrganic'] = False 
        params['IncludePaid'] = True
        params['IncludeBranded'] = False
        params['IncludeNoneBranded'] = True
        rtn = self.makeRequest(uri, params)['Data']
        logger.debug("List Paid and None-branded keywords:")
        logger.debug(rtn)
        for k  in rtn : 
            if k['SearchTerm'] !=  'grid.upgrade': 
                tmp= {
                    'SearchTerm': k['SearchTerm'],
                    'CPC': k['CPC'],
                    'KwVolume': k['KwVolume']
                }
                if tmp not in data:
                    data.append(tmp)
        # make list Organic and branded keywords
        params['IncludeOrganic'] = True 
        params['IncludePaid'] = False
        params['IncludeBranded'] = True
        params['IncludeNoneBranded'] = False
        rtn = self.makeRequest(uri, params)['Data']
        logger.debug("List Organic and branded keywords:")
        logger.debug(rtn)
        for k  in rtn : 
            if k['SearchTerm'] != 'grid.upgrade': 
                tmp = {
                    'SearchTerm': k['SearchTerm'],
                    'CPC': k['CPC'],
                    'KwVolume': k['KwVolume']
                }
                if tmp not in data:
                    data.append(tmp)
        # make list Organic and None-branded keywords
        params['IncludeOrganic'] = True 
        params['IncludePaid'] = False
        params['IncludeBranded'] = False
        params['IncludeNoneBranded'] = True
        rtn = self.makeRequest(uri, params)['Data']
        logger.debug("List Organic and None-branded keywords:")
        logger.debug(rtn)
        for k  in rtn : 
            if k['SearchTerm'] != 'grid.upgrade': 
                tmp = {
                    'SearchTerm': k['SearchTerm'],
                    'CPC': k['CPC'],
                    'KwVolume': k['KwVolume']
                }
                if tmp not in data:
                    data.append(tmp)
        logger.debug(data)
        return data
        
    def getReferringIndustries(self):
        uri= 'widgetApi/WebsiteOverviewDesktop/TopReferringCategories/Table'
        params = {
            "country": 999,
            'from': self.fromDate,
            'includeSubDomains': True,
            'isWindow': False,
            'keys': self.domain,
            'timeGranularity': 'Monthly',
            'to': self.toDate,
            'webSource': 'Desktop',
            'orderBy': 'TotalShare desc'
        }
        rtn = self.makeRequest(uri, params)['Data']
        data = []
        for k in rtn: 
            data.append(k['Category'])
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
    
    def mapCountry(self, id, data):
        logger.info(data)
        logger.info(id)
        for d in data:
            if int(id) == int(d['id']):
                return d['text']
        return "Unknown"

        