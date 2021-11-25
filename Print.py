
from autoscraper import AutoScraper
# Data training to get similar results 
scrape_data=[
    ('https://theprint.in/category/india/',["India"]), 
    ('https://theprint.in/category/india/',["Cracks appear in Samyukt Kisan Morcha as some unions make ‘political moves’ ahead of Punjab 2022"]),
    ('https://theprint.in/category/india/',["Fake customer care numbers, OTP access — how a gang in Jamtara cheated over 1,000 people"]),
    ('https://theprint.in/category/india/',["25 November, 2021"]),
]
scrapper=AutoScraper()

# India's section
for specific_url,data1 in scrape_data:
    # build() - Learns a set of rules represented as scrape_data based on the wanted_list,
     # which is  reused for scraping similar elements from other pages in the In PRINT
    scrapper.build(url=specific_url,wanted_list=data1,update=True,text_fuzz_ratio=1)
    result=scrapper.get_result_similar("https://theprint.in/category/india/?ref=hp",unique=True)
print(result,"\n")

# Politics section
for specific_url,data1 in scrape_data:
    
    scrapper.build(url=specific_url,wanted_list=data1,update=True,text_fuzz_ratio=1)
    result=scrapper.get_result_similar("https://theprint.in/category/politics/?ref=hp",unique=True)
print(result,"\n") 

# Defence section
for specific_url,data1 in scrape_data:
    
    scrapper.build(url=specific_url,wanted_list=data1,update=True,text_fuzz_ratio=1)
    result=scrapper.get_result_similar("https://theprint.in/category/defence/",unique=True,keep_order=True)
print(result,"\n")

# Goverance section 
for specific_url,data1 in scrape_data:
    
    scrapper.build(url=specific_url,wanted_list=data1,update=True,text_fuzz_ratio=1)
    result=scrapper.get_result_similar("https://theprint.in/category/india/governance/",unique=True,keep_order=True)
print(result,"\n")

#Economics Section 
for specific_url,data1 in scrape_data:
    
    scrapper.build(url=specific_url,wanted_list=data1,update=True,text_fuzz_ratio=1)
    result=scrapper.get_result_similar("https://theprint.in/category/economy/",unique=True,keep_order=True)
print(result,"\n")

# Science & Tech
for specific_url,data1 in scrape_data:
    
    scrapper.build(url=specific_url,wanted_list=data1,update=True,text_fuzz_ratio=1)
    result=scrapper.get_result_similar("https://theprint.in/category/science/",unique=True,keep_order=True)
    result1=scrapper.get_result_similar("https://theprint.in/category/tech/",unique=True,keep_order=True)
print(result,"\n",result1)

# Sports

for specific_url,data1 in scrape_data:
    
    scrapper.build(url=specific_url,wanted_list=data1,update=True,text_fuzz_ratio=1)
    result=scrapper.get_result_similar("https://theprint.in/category/sport/",unique=True,keep_order=True)
print(result,"\n")

# Homepage news : Latest , Latest on covid19, Top stories
#                 World News, Pakistan ,Opinion, IN DEPTH analysis       
scrape_data1=[
    ("https://theprint.in",["Japan envoy holds talks with senior Taliban members in Kabul"]),
    ("https://theprint.in",["India records 9,119 new Covid cases, active infections lowest in 539 days"]),
    ("https://theprint.in",["Farm laws debate missed a lot. Neither supporters nor Modi govt identified the real problem"]),
    ("https://theprint.in",["Punjab’s Dalits are shifting state politics, flocking churches, singing Chamar pride"]),
]
for get_url,data in scrape_data1:
    scrapper.build(url=get_url,wanted_list=data,update=True)
    Main_news=scrapper.get_result_similar(url="https://theprint.in",grouped=True,unique=True)
       
print(Main_news)
scrapper.save("Scraping\result_print.json")




