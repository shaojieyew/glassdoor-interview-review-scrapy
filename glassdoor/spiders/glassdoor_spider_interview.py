import scrapy
import csv   
from scrapy.selector import Selector

class GlassdoorSpider(scrapy.Spider):
    name = "company_interview"
   
    def start_requests(self):    
        fields=['company_name','website','headquarter','size','founded','type','industry','revenue','competitors','datetime','title','link','location','interview_details','interview_question','result1','result2','result3']
     
        url ='https://www.glassdoor.com/Reviews/singapore-reviews-SRCH_IL.0,9_IM1123_IP1.htm'
        if hasattr(self, 'keyword'):
            if not (self.keyword is None) and len(self.keyword)>0:
                keyword = self.keyword
                keywordLen = len(self.keyword)
                print(url)
                url ='https://www.glassdoor.com/Reviews/singapore-'+keyword+'-reviews-SRCH_IL.0,9_IM1123_KE10,'+str(keywordLen+10)+'_IP1.htm'
                
        file = open('company_interviews.csv', 'w')
        wr = csv.DictWriter(file, fieldnames=fields, lineterminator = '\n')
        wr.writeheader()
        file.close()
        yield scrapy.Request(url=url, callback=self.parse_companies_list)



    def parse_companies_list(self, response):
        for quote in response.css('div.margBotXs'):
            company_name = quote.css('a.tightAll::text').extract_first()
            href =  quote.css('a.tightAll::attr(href)').extract_first()
            url = ('https://www.glassdoor.com'+href)
            #print(company_name)
			
            #print("#######CRAWL COMPANY#######")
            yield scrapy.Request(url=url, callback=self.parse_company_detail,meta={'company_name': company_name})

        next_url = response.css('li.next').css('a::attr(href)').extract_first()
        if not (next_url is None):
            next_url = 'https://www.glassdoor.com'+next_url
            yield scrapy.Request(url=next_url, callback=self.parse_companies_list)
			
    def parse_company_detail(self, response):
        company_name = response.meta.get('company_name')
        website = response.xpath('//div[@class=\'infoEntity\']//a[@class=\'link\']/text()').extract_first()
        headquarter = response.xpath('//div[@class=\'infoEntity\' and label/text()[1]=\'Headquarters\']/span[@class=\'value\']/text()').extract_first()
        size = response.xpath('//div[@class=\'infoEntity\' and label/text()[1]=\'Size\']/span[@class=\'value\']/text()').extract_first()
        founded = response.xpath('//div[@class=\'infoEntity\' and label/text()[1]=\'Founded\']/span[@class=\'value\']/text()').extract_first()
        type = response.xpath('//div[@class=\'infoEntity\' and label/text()[1]=\'Type\']/span[@class=\'value\']/text()').extract_first()
        industry = response.xpath('//div[@class=\'infoEntity\' and label/text()[1]=\'Industry\']/span[@class=\'value\']/text()').extract_first()
        revenue = response.xpath('//div[@class=\'infoEntity\' and label/text()[1]=\'Revenue\']/span[@class=\'value\']/text()').extract_first()
        competitors = response.xpath('//div[@class=\'infoEntity\' and label/text()[1]=\'Competitors\']/span[@class=\'value\']/text()').extract_first()
   
        #review_url = response.css('a.reviews::attr(href)').extract_first()
        #review_url = 'https://www.glassdoor.com'+review_url
        
        interview_url = 'https://www.glassdoor.com'+response.css('a.interviews::attr(href)').extract_first()
        yield scrapy.Request(url=interview_url, callback=self.parse_company_interview,
		meta={
		'company_name': company_name,
		'website': website,
		'headquarter': headquarter,
		'size': size,
		'founded': founded,
		'type': type,
		'industry': industry,
		'revenue': revenue,
		'competitors': competitors
		})
		
    def parse_company_interview(self, response):
        company_name = response.meta.get('company_name')
        website = response.meta.get('website')
        headquarter = response.meta.get('headquarter')
        size = response.meta.get('size')
        founded = response.meta.get('founded')
        type = response.meta.get('type')
        industry = response.meta.get('industry')
        revenue = response.meta.get('revenue')
        competitors = response.meta.get('competitors')
		
        for review in response.css('li.empReview.cf'):
            datetime = review.css('time.date::attr(datetime)').extract_first()
            title = review.css('span.reviewer::text').extract_first()
            link = 'https://www.glassdoor.com'+review.css('a::attr(href)').extract_first()
            location = review.css('span.authorLocation::text').extract_first()
            interview_details = review.css('p.interviewDetails.mainText::text').extract_first()
            interview_questions = review.css('span.interviewQuestion.noPadVert.truncateThis.wrapToggleStr::text').extract()
            interview_question =''
            for question in interview_questions:
                interview_question=interview_question+question+" "
            result1 = None
            result2 = None
            result3 = None
            for result in review.css('div.interviewOutcomes').css('span.middle::text').extract():
                if (result1 is None):
                    result1 = result
                else: 
                    if (result2 is None):
                        result2 = result
                    else:
                        if (result3 is None):
                            result3 = result

            print(company_name)
            print(website)
            print(headquarter)
            print(size)
            print(founded)
            print(type)
            print(industry)
            print(revenue)
            print(competitors)
            print(datetime)
			
            print(title)
            print(link)
            print(location)
            print(interview_details)
            print(interview_questions)
            print(result1)
            print(result2)
            print(result3)
			
            #print(opinion)
            fields=['company_name','website','headquarter','size','founded','type','industry','revenue','competitors','datetime','title','link','location','interview_details','interview_question','result1','result2','result3']
     
            file = open('company_interviews.csv', 'a')
            wr = csv.DictWriter(file, fieldnames=fields, lineterminator = '\n')
            wr.writerow({'company_name':company_name,'website':website,'headquarter':headquarter,'size':size,'founded':founded,'type':type,'industry':industry,'revenue':revenue,'competitors':competitors,'datetime':datetime,'title':title,'link':link,'location':location,'interview_details':interview_details,'interview_question':interview_question,'result1':result1,'result2':result2,'result3':result3})
            file.close()
		  
        next_url = response.css('li.next').css('a::attr(href)').extract_first()
        if not (next_url is None):
            next_url = 'https://www.glassdoor.com'+next_url
            yield scrapy.Request(url=next_url, callback=self.parse_company_interview,
		meta={
		'company_name': company_name,
		'website': website,
		'headquarter': headquarter,
		'size': size,
		'founded': founded,
		'type': type,
		'industry': industry,
		'revenue': revenue,
		'competitors': competitors
		})