import scrapy
import csv   
from scrapy.selector import Selector

class GlassdoorSpider(scrapy.Spider):
    name = "company_review"
   
    def start_requests(self):    
        fields=['company_name','website','headquarter','size','founded','type','industry','revenue','competitors','datetime','title','link','rating','position','pros','cons','adviceMgmt','review_description','opinion1','opinion2','opinion3']
        
        url ='https://www.glassdoor.com/Reviews/singapore-reviews-SRCH_IL.0,9_IM1123_IP1.htm'
        if hasattr(self, 'keyword'):
            if not (self.keyword is None) and len(self.keyword)>0:
                keyword = self.keyword
                keywordLen = len(self.keyword)
                print(url)
                url ='https://www.glassdoor.com/Reviews/singapore-'+keyword+'-reviews-SRCH_IL.0,9_IM1123_KE10,'+str(keywordLen+10)+'_IP1.htm'
                
        file = open('company_reviews.csv', 'w')
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
   
        review_url = response.css('a.reviews::attr(href)').extract_first()
        review_url = 'https://www.glassdoor.com'+review_url
        yield scrapy.Request(url=review_url, callback=self.parse_company_review,
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
		
        
        #interview_url = response.css('a.interviews::attr(href)').extract_first()
        #print('https://www.glassdoor.com'+interview_url)

		
    def parse_company_review(self, response):
        company_name = response.meta.get('company_name')
        website = response.meta.get('website')
        headquarter = response.meta.get('headquarter')
        size = response.meta.get('size')
        founded = response.meta.get('founded')
        type = response.meta.get('type')
        industry = response.meta.get('industry')
        revenue = response.meta.get('revenue')
        competitors = response.meta.get('competitors')
		
        for review in response.css('div.hreview'):
            datetime = review.css('time.date::attr(datetime)').extract_first()
            title = review.css('span.summary::text').extract_first()
            link = 'https://www.glassdoor.com'+review.css('a.reviewLink::attr(href)').extract_first()
            rating = review.css('span.rating').css('span.value-title::attr(title)').extract_first()
            position = review.css('span.authorJobTitle::text').extract_first()
            pros = review.css('p.pros::text').extract_first()
            cons = review.css('p.cons::text').extract_first()
            adviceMgmt = review.css('p.adviceMgmt::text').extract_first()
            review_description = review.css('p.tightBot.mainText::text').extract_first()
            opinion1 = None
            opinion2 = None
            opinion3 = None
            for review_recommend in review.css('div.flex-grid.recommends').css('div.tightLt.col.span-1-3'):
                opinion_2=review_recommend.css('span.middle::text').extract_first()
                opinion_1=review_recommend.css('span.showDesk::text').extract_first()
                if not (opinion_1 is None) and not (opinion_2 is None):
                    opinion = opinion_1+' '+opinion_2
                else:
                    opinion = opinion_2
                if (opinion1 is None):
                    opinion1 = opinion
                else: 
                    if (opinion2 is None):
                        opinion2 = opinion
                    else:
                        if (opinion3 is None):
                            opinion3 = opinion

            print("#######CRAWL COMPANY REVIEW#######")
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
            print(rating)
            print(position)
            print(pros)
            print(cons)
            print(adviceMgmt)
            print(review_description)
            #print(opinion)
            fields=['company_name','website','headquarter','size','founded','type','industry','revenue','competitors','datetime','title','link','rating','position','pros','cons','adviceMgmt','review_description','opinion1','opinion2','opinion3']
     
            file = open('company_reviews.csv', 'a')
            wr = csv.DictWriter(file, fieldnames=fields, lineterminator = '\n')
            wr.writerow({'company_name':company_name,'website':website,'headquarter':headquarter,'size':size,'founded':founded,'type':type,'industry':industry,'revenue':revenue,'competitors':competitors,'datetime':datetime,'title':title,'link':link,'rating':rating,'position':position,'pros':pros,'cons':cons,'adviceMgmt':adviceMgmt,'review_description':review_description,'opinion1':opinion1,'opinion2':opinion2,'opinion3':opinion3})
            file.close()
		  
        next_url = response.css('li.next').css('a::attr(href)').extract_first()
        if not (next_url is None):
            next_url = 'https://www.glassdoor.com'+next_url
            yield scrapy.Request(url=next_url, callback=self.parse_company_review,
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