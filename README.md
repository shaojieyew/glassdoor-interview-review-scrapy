# glassdoor-interview-review-scrapy

glassdoor crawler using scrapy

scraped data is stored in company_review.csv and company_interview.csv

cmd:

crawl all singapore company

	scrapy crawl company_interview	
			
	scrapy crawl company_review

crawl all company with keyword entered

	scrapy crawl company_interview -a keyword=toshiba	

	scrapy crawl company_review -a keyword=toshiba
