import scrapy
import json
import re

class NcLegBillSpider(scrapy.Spider):
    name = "bills"
    houseBills = 'http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?BillID=H%num%&Session=2017'
    billStart = 1
    debug = True
    

    # Begins the request loop
    def start_requests(self):
        while self.billStart > 0:
            yield scrapy.Request(url=self.houseBills.replace('%num%',str(self.billStart)), callback=self.parse)
            self.billStart += 1
            # Set debug = False to run to completion; otherwise limits to 20 items
            if (self.debug == True and self.billStart == 20):
                self.billStart = -1
        
    # Turns a delimited list into an array with each entry stripped       
    def clean_and_split(object, input, delim = ';'):
        result = input.strip()
        result = re.sub(re.escape(delim) + r' ', delim, result)
        return result.split(delim)
    
    # Simple interface for regex find/replace
    def replace_words(object, input, find, replace):
        result = input.strip()
        result = re.sub(re.escape(find), replace, result)
        return result.strip()

    # Parse results of the request
    def parse(self, response):
        if len(response.xpath('//div[@id = "title"]/text()').re('Not Found')) > 0:
            self.billStart = -1
            return
        
        # Build base results object
        result = {
            'number': int(response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\d+')[0]),
            'chamberOrigin': response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\w+')[0],
            'session': self.replace_words(response.xpath('//div[@id = "mainBody"]/div[3]/text()').extract_first(), 'Session', ''),
            'title': response.xpath('//div[@id = "title"]/a/text()').extract_first(),
            'sponsors': response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[2]/td[@class = "tableText"]/a/text()').extract() or [''],
            'attributes': self.clean_and_split(response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[3]/td[2]/text()').extract_first()) or [''],
            'statutes': self.clean_and_split(response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[5]/td/div/text()').extract_first()) or [''],
            'keywords': self.clean_and_split(response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[6]/td/div/text()').extract_first(), ',') or [''],
            'votes': {}
        }
        
        # House Vote data may or may not be present
        houseDate = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[1]/text()').extract_first() or ''
        houseSubject = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[2]/text()').extract_first() or ''
        houseRcsNumber = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[3]/text()').extract_first() or '0'
        houseAye = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[4]/text()').extract_first() or '0'
        houseNo = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[5]/text()').extract_first() or '0'
        houseNv = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[6]/text()').extract_first() or '0'
        houseAbs = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[7]/text()').extract_first() or '0'
        houseExcVote = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[8]/text()').extract_first() or '0'
        houseTotal = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[9]/text()').extract_first() or '0'
        houseResult = response.xpath('//div[@id = "mainBody"]/table[3]/tr[3]/td[10]/a/text()').extract_first() or ''
        
        # Senate Vote data may or may not be present
        senateDate = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[1]/text()').extract_first() or ''
        senateSubject = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[2]/text()').extract_first() or ''
        senateRcsNumber = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[3]/text()').extract_first() or '0'
        senateAye = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[4]/text()').extract_first() or '0'
        senateNo = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[5]/text()').extract_first() or '0'
        senateNv = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[6]/text()').extract_first() or '0'
        senateAbs = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[7]/text()').extract_first() or '0'
        senateExcVote = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[8]/text()').extract_first() or '0'
        senateTotal = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[9]/text()').extract_first() or '0'
        senateResult = response.xpath('//div[@id = "mainBody"]/table[3]/tr[4]/td[10]/a/text()').extract_first() or ''
        
        # Remove house object if it doesn't contain data
        if (houseDate != '' and houseDate != 'Viewing Last 1 Vote(s)'):
            result['votes']['house'] = {
                'date': houseDate,
                'subject': houseSubject.strip(),
                'rcsNumber': int(re.sub(r'\D', "", houseRcsNumber)),
                'aye': int(houseAye),
                'no': int(houseNo),
                'nv': int(houseNv),
                'abs': int(houseAbs),
                'excVote': int(houseExcVote),
                'total': int(houseTotal),
                'result': houseResult,
            }
        
        # Remove senate object if it doesn't contain data
        if (senateDate != '' and senateDate != 'Viewing Last 1 Vote(s)'):
            result['votes']['senate'] = {
                'date': senateDate,
                'subject': senateSubject,
                'rcsNumber': int(re.sub(r'\D', "", senateRcsNumber)),
                'aye': int(senateAye),
                'no': int(senateNo),
                'nv': int(senateNv),
                'abs': int(senateAbs),
                'excVote': int(senateExcVote),
                'total': int(senateTotal),
                'result': senateResult,
            }        

        # Output results to file
        yield result
