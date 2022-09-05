#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:00:00 2019

@author: scraper
"""
#%%
from re import findall,sub
from lxml import html
from time import sleep
from selenium import webdriver
from xvfbwrapper import Xvfb
from selenium.webdriver.common.action_chains import ActionChains
import random
import re
import time
from selenium.webdriver.common.keys import Keys
import traceback,sys

def set_viewport_size(driver,width,height):
    window_size=driver.execute_script("""
        return [window.outerWidth-window.innerWidth+arguments[0],
        window.outerHeight-window.innerHeight+arguments[1]];                  
    
    """,width,height)
    
    driver.set_window_size(*window_size)

def scroll_shim(passed_in_driver,object):
    x=object.location['x']
    y=object.location['y']
    scroll_by_coord='window.scrollTo(%s,%s);' %(x,y)
    
    scroll_nav_out_of_way='window.scrollBy(0,-120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)
    
    
def randomGSAction(driver):#will roll a random.rand to determine if it is going to make an action or not, default is 1 every 5.
    roll=random.randint(0,100)
    
    if roll<=10:
        performAction=True
    else:
        performAction=False
        
    if performAction==True:
        actionRoll=random.randint(1,8)
        

        if actionRoll==1:
            #scroll to and click on a random article link, wait, then go back
            print('Random 1')
            links=driver.find_elements_by_xpath('//h3[@class="gs_rt"]')
            linkLen=len(links)
            
            selectRoll=random.randint(0,linkLen-1)
            
            link=links[selectRoll]
            
            scroll_shim(driver,link)
            
            a=ActionChains(driver)
            a.move_to_element(link).click(link).pause(1)
            a.perform()
            
            sleep(random.randint(15,30))
            
            driver.back()
        
        if actionRoll==2:
            print('Random 2')
            links=driver.find_elements_by_xpath('//h3[@class="gs_rt"]')
            linkLen=len(links)
            
            selectRoll=random.randint(0,linkLen-1)
            
            link=links[selectRoll]
            
            scroll_shim(driver,link)
            
            a=ActionChains(driver)
            a.move_to_element(link).key_down(Keys.CONTROL).click(link).pause(1).key_up(Keys.CONTROL)
            a.perform()
            
            base=driver.window_handles[0]
            new=driver.window_handles[-1]
            
            driver.switch_to.window(str(new))
            
            sleep(random.randint(15,30))
            
            driver.close()
            driver.switch_to.window(str(base))
            
        if actionRoll==3:
            print('Random 3')
            links=driver.find_elements_by_xpath('//h3[@class="gs_rt"]')
            linkLen=len(links)
            
            selectRoll=random.randint(0,linkLen-1)
            
            link=links[selectRoll]
            
            scroll_shim(driver,link)
            
            a=ActionChains(driver)
            a.move_to_element(link).click_and_hold(link).pause(3).release().pause(1)
            a.perform()
            
            sleep(random.randint(20,45))
            
            driver.back()
            
        if actionRoll==4:
            print('Random 4')
            entries=driver.find_elements_by_xpath('//div[contains(@class,"gs_ri")]')
            entryLen=len(entries)
            
            selectRoll=random.randint(0,entryLen-1)
            
            scroll_shim(driver,entries[selectRoll])
            
            sleep(random.randint(5,15))
            
        if actionRoll==5:
            print('Random 5')
            texts=driver.find_elements_by_xpath('//div[contains(@class,"gs_rs")]')
            textsLen=len(texts)
            
            selectRoll=random.randint(0,textsLen-1)
            
            target=texts[selectRoll]
            scroll_shim(driver,target)
            
            xOff=random.randint(0,200)
            yOff=random.randint(-10,0)
            
            a=ActionChains(driver)
            a.move_to_element_with_offset(target,xOff,yOff).click().pause(1)
            a.perform()
            
            sleep(3)
            
        if actionRoll==6:
            print('Random 6')
            texts=driver.find_elements_by_xpath('//div[contains(@class,"gs_rs")]')
            textsLen=len(texts)
            
            selectRoll=random.randint(0,textsLen-1)
            
            target=texts[selectRoll]
            scroll_shim(driver,target)
            
            xOff=random.randint(0,200)
            yOff=random.randint(-10,0)
            
            a=ActionChains(driver)
            a.move_to_element_with_offset(target,xOff,yOff).double_click().pause(1)
            a.perform()
            
            sleep(5)
         
        if actionRoll==7:
            print('Random 6')
            texts=driver.find_elements_by_xpath('//div[contains(@class,"gs_rs")]')
            textsLen=len(texts)
            
            selectRoll=random.randint(0,textsLen-1)
            
            target=texts[selectRoll]
            scroll_shim(driver,target)
            
            xOff=random.randint(0,200)
            yOff=random.randint(-10,0)
            
            a=ActionChains(driver)
            a.move_to_element_with_offset(target,xOff,yOff).context_click().pause(3).key_down(Keys.ESCAPE).pause(3).key_up(Keys.ESCAPE)
            a.perform()
        
        if actionRoll==8:
            print('Random 8')
            texts=driver.find_elements_by_xpath('//div[contains(@class,"gs_rs")]')
            textsLen=len(texts)
            
            selectRoll=random.randint(0,textsLen-1)
            
            target=texts[selectRoll]
            scroll_shim(driver,target)
            
            xOff=random.randint(0,200)
            yOff=random.randint(-10,0)
            
            xOff2=random.randint(0,100)
            yOff2=random.randint(-5,0)
            
            a=ActionChains(driver)
            a.move_to_element_with_offset(target,xOff,yOff).click_and_hold().pause(1).move_by_offset(xOff2,yOff2).pause(2).release()
            a.click().pause(1)
            a.perform()
            
def fallibleClick(driver,object):#gives clicks a chance to fail by clicking outside of the click link, set to fail one of every 20 clicks, with bad luck protection
    #turned off atm
    count=0
    
    try:
        while True:
            
            if count<7:
                roll=random.randint(0,100)
                
                if roll<=5:#default 5
                    failedClick=True
                else:
                    failedClick=False
            else:
                failedClick=False
                
                
            if failedClick==False:
                print('Succesful Click')
                scroll_shim(driver,object)
                
                a=ActionChains(driver)
                a.move_to_element(object).click().pause(1)
                a.perform()
                break
            
#            if failedClick==True:
#                print('Click Failed')
#                base_url=driver.current_url
#                scroll_shim(driver,object)
#                
#                objectSize=object.size
#                
#                xOff=int(objectSize['width']/2)+random.randint(15,50)
#                yOff=int(objectSize['height']/2)+random.randint(15,50)
#                
#                signRoll=random.random()
#                if signRoll<.5:
#                    xOff=-xOff
#                
#                signRoll=random.random()
#                if signRoll<.5:
#                    yOff=-yOff
#                    
#                a=ActionChains(driver)
#                a.move_to_element_with_offset(object,xOff,yOff).click().pause(3)
#                a.perform()
#                
#                if driver.current_url!=base_url:
#                    sleep(3)
#                    driver.back()
#                
#                count=count+1
    except:
        driver.get_screenshot_as_file('/home/scraper/Downloads/error.png')


def parse(url):
    
    pubList=[]
    searchKey = "author:\"Steven N Gange\"" # Insert physician name
    
    profile=webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0")
    
    
    response = webdriver.Firefox()
    set_viewport_size(response,1920,1080)
    
    response.get(url)
    response.maximize_window()
    
    searchKeyElement = response.find_elements_by_xpath('//*[(@id="gs_hdr_tsi")]')
    submitButton = response.find_elements_by_xpath('//*[(@id="gs_hdr_tsb")]')
    
    if searchKeyElement and submitButton:#input only if you can find all the search elements
        sleep(random.random()*5)
        searchKeyElement[0].send_keys(searchKey)
        
        
        sleep(random.random()*25)
        submitButton[0].click()
        sleep(random.random()*5)
        
        
        while True:

            sleep(random.randint(10,40))
            
            print(response.current_url)
            parser = html.fromstring(response.page_source,response.current_url)

            optionButtons=parser.xpath('//li[@class="gs_inw"]//a')
            buttons=response.find_elements_by_xpath('//li[@class="gs_inw"]//a')
            
            patentCheck=optionButtons[0].attrib.get('aria-checked')
            citationCheck=optionButtons[1].attrib.get('aria-checked')
            

            if patentCheck==True:
                scroll_shim(response,buttons[0])
                buttons[0].click()
                print('Clicked')
                buttons=response.find_elements_by_xpath('//li[@class="gs_inw"]//a')
            
            if citationCheck==True:#Still pulling citations for some reason, not the end of the world, but kind of defeats the whole point of htis
                scroll_shim(response,buttons[1])
                buttons[1].click()
                print('Clicked')
            
#            print(response.current_url)
            parser = html.fromstring(response.page_source,response.current_url)
            publications = parser.xpath('//div[contains(@class,"gs_ri")]')
            focusPublications=response.find_elements_by_xpath('//div[contains(@class,"gs_ri")]')
            
            
            for count,publication in enumerate(publications):
                print("Publication "+str(count))
#                scroll_shim(response,focusPublications[count])
#                sleep(random.random()*5)
                
                
                
                #Pull Article Name
                pubName=publication.xpath('.//*[contains(@class,"gs_rt")]')
                pubName=str(pubName[0].text_content()) if pubName else None
                
                sleep(random.random()*random.randint(0,10))
                citationNum=publication.xpath('.//a[contains(@href,"/scholar?cites=")]')
                citationNum=citationNum[0].text.lstrip('Cited by ') if citationNum else None
                
                #Sleep for random amount of time
                sleep(random.random()*random.randint(0,10))
                
                #Pull Article Summary
                summary=publication.xpath('.//*[contains(@class,"gs_rs")]')
                summary=summary[0].text if summary else None
                sleep(random.random()*random.randint(0,10))
                
                

                #Click on the citation ref to pull Author, journal and publish year
                citeButton=response.find_elements_by_xpath('.//*[contains(@aria-controls,"gs_cit")]')
                sleep(random.random()*5)
                
                

                if citeButton:
                    fallibleClick(response,citeButton[count])
                    
                else:
                    print("Cite Button Not Found")
                    break
                
                sleep(3)

                #Pull Data from popup
#                print(response.current_url)
                parser2=html.fromstring(response.page_source,response.current_url)
                
                citations=parser2.xpath('//div[contains(@class,"gs_md_bdy")]')
                sleep(3)
                citationBody=citations[0].xpath('.//div[contains(@id,"gs_citt")]')
                sleep(random.random()*random.randint(0,10))

                citations=citationBody[0].xpath('.//div[contains(@class,"gs_citr")]')
                
#                print(response.current_url)
#                print(len(citations))
#                print(len(citationBody))
#                
                targetCitation=citations[4].text.split('.')#first one
                sleep(3)
                try:
                    publishDate=re.findall(r"[0-9]{4} [A-Za-z]{3}",targetCitation[3])[0]
                except:
                    publishDate=None
                sleep(random.random()*random.randint(0,10))

                journal=targetCitation[2].lstrip()
                journal=' '.join(journal.split()) if journal else None
                sleep(random.random()*5)
                authorList=targetCitation[0].split(',')
                authorListFinal=[]
                sleep(3)
                if len(authorList)!=0:
                    for author in authorList:
                        author=author.replace('\n','')
                        author=author.lstrip()
                        authorListFinal.append(author)
                else:
                    print('Authors not found')
                    
                    
                sleep(3)
                
                #Find and execute exit button to close popup
                
                
                try:
                    sleep(random.random()*random.randint(0,5))
                    
                    #exit can be either by clicking on the button, or on anywhere outside of the box 
                    
                    exitRoll=random.random()
                    
                    if exitRoll>=.5:
                        exitButton=response.find_elements_by_xpath('.//*[(@id="gs_cit-x")]')
                        exitButton[0].click()
                    else:
                        exitButton=response.find_elements_by_xpath('.//*[(@id="gs_cit-x")]')
                        xOff=random.randint(-100,-50)
                        yOff=random.randint(50,100)
                        
                        a=ActionChains(response)
                        a.move_to_element_with_offset(exitButton[0],xOff,yOff).click().pause(1)
                        a.perform()
                except:
                    response.get_screenshot_as_file('/home/scraper/Downloads/test'+str(count)+'.png')
                    exc_type,exc_value,exc_traceback=sys.exc_info()
                    
                    traceback.print_exception(exc_type,exc_value,exc_traceback,limit=2,file=sys.stdout)
                    

                
                sleep(1)
                
                #publist

                citedByPublications=[]
                citedbyLink=parser.xpath('.//div[contains(@class,"gs_fl")]//a[contains(@href,"/scholar?cites=")]')
                
                try:
                    ref=citedbyLink[count].attrib.get("href")
                except:
                    item={
                        "PublicationName":pubName,
                        "Summary":summary,
                        "Cited By":citationNum,
                        "Publish Date":publishDate,
                        "Journal":journal,
                        "Authors":authorListFinal,
                        "CitedBy":citedByPublications,
                        }
                    pubList.append(item)
                                     
                    continue
                        
                
                sleep(3)
                urladd=ref
                sleep(3)
                url2=url+urladd
                
                
#                # for secondary pull, should still go through the motions of searching for the author, but only click on the links, nothing else
#
#                response2=webdriver.Firefox(profile)
#                set_viewport_size(response2,1920,1080)
#                response2.get(url2)
#                sleep(random.random()*5)
#                
#                sleep(3)
#                parser3=html.fromstring(response2.page_source,response2.current_url)
#                
#                citingPublications = parser3.xpath('//div[contains(@class,"gs_ri")]')
#                sleep(3)
#                
#                
#                while True:
#                    for count2,publication in enumerate(citingPublications):
#                        sleep(random.random()*random.randint(0,10))
#                        print("Citation "+str(count2))
#                        pubNameCiting=publication.xpath('.//*[contains(@class,"gs_rt")]')
#                        pubNameCiting=str(pubNameCiting[0].text_content()) if pubNameCiting else None
#                        sleep(random.random()*5)
#    #                    
#    ##                    randomClick=response2.find_elements_by_xpath('.//*[contains(@class,"gs_rs")]')
#    ##                    if randomClick:
#    ##                        randomClick.click()
#                                           
#                        citeButton=response2.find_elements_by_xpath('.//*[contains(@aria-controls,"gs_cit")]')
#                        print(len(citeButton))
#                        sleep(3)
#                        if citeButton:
#                            sleep(random.random()*random.randint(0,10))
#    
#                            citeButton[count2].click()
#                        else:
#                            print("Cite Button Not Found")
#                            break
#                        
#                        sleep(1)
#    #                    
#    #                    
#                        parser4=html.fromstring(response2.page_source,response2.current_url)
#                        sleep(random.random()*2)
#                        citations_citedBy=parser4.xpath('//div[contains(@class,"gs_md_bdy")]')
#                        sleep(random.random()*3)
#                        citationBody_citedBy=citations_citedBy[0].xpath('.//div[contains(@id,"gs_citt")]')
#                        sleep(random.random()*random.randint(0,10))
#                    
#                        citationsList_citedBy=citationBody_citedBy[0].xpath('.//div[contains(@class,"gs_citr")]')
#                        sleep(3)
#                        targetCitation=citationsList_citedBy[4].text.split('.')
#                        sleep(random.random()*random.randint(0,10))
#                        authorList=targetCitation[0].split(',')
#                        authorListFinal_CitedBy=[]
#                        sleep(random.random()*random.randint(0,10))
#                        
#                        if len(authorList)!=0:
#                            
#                            for author in authorList:
#                                sleep(1)
#                                author=author.replace('\n','')
#                                author=author.lstrip()
#                                authorListFinal_CitedBy.append(author)
#                            
#                        sleep(random.random()*5)
#                        citedPub={
#                                "Name":pubNameCiting,
#                                "Authors":authorListFinal_CitedBy
#                                }
#                        
#                        citedByPublications.append(citedPub)
#                        sleep(1)
#                        exitButton=response2.find_elements_by_xpath('.//*[(@id="gs_cit-x")]')
#                        print(response2.current_url)
#    #                    print(response2.execute_script("return [window.innerWidth,window.innerHeight];"))
#                        
#                        if exitButton:
#                            sleep(random.random()*random.randint(0,10))
#                            exitButton[0].click()
#                        else:
#                            print("Exit Button Not Found")
#                            break
#                        
#                        sleep(1)
#                        
#                    nextButtonCite=response2.find_elements_by_xpath('//td')
#                    nextbuttonVisibleCite=parser4.xpath('//table//tbody//tr//td[@align="left"]//a')
#                
#                    if len(nextbuttonVisibleCite)==0:
#                        print('End Reached')
#                        break
#                    else:
#                        scroll_shim(response,nextButtonCite[-1])
#                        nextButtonCite[-1].click()
#                    
#                    
#                    
#                response2.close()
#                sleep(3)

                item={
                        "PublicationName":pubName,
                        "Summary":summary,
                        "Cited By":citationNum,
                        "Publish Date":publishDate,
                        "Journal":journal,
                        "Authors":authorListFinal,
                        "CitedByLink":url2,
                        }
                
                randomGSAction(response)
                response.get_screenshot_as_file('/home/scraper/Downloads/test'+str(count)+'.png')

                pubList.append(item)
            
            sleep(3)
            nextButton=response.find_elements_by_xpath('//td')
            
            nextbuttonVisible=parser.xpath('//table//tbody//tr//td[@align="left"]//a')
            
            sleep(3)
            
            if len(nextbuttonVisible)==0:
                break
            else:
                fallibleClick(response,nextButton[-1])


        return pubList
        
    else:
        print('Cannot find all elements to search')
        
if __name__ == '__main__':
    vdisplay = Xvfb()
    vdisplay.start()
    
    #for testing
    #df=parse(r'file:///home/Scraper/Downloads/author "Steven N Gange" - Google Scholar.html')
    
    start=time.time()
    df=parse('http://scholar.google.com')
    end=time.time()-start
    vdisplay.stop()
