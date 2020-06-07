
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import urllib
import json
from time import gmtime, strftime, localtime
import time
import datetime
from datetime import date
import calendar
import random
import string
from py_thesaurus import Thesaurus
import pronouncing
import csv
from pathlib import Path
import os


# In[2]:


def get_daily_riddle(daily_riddle_site="https://www.riddles.com/riddle-of-the-day", date=strftime("%m-%d-%Y", gmtime())):

    page = requests.get(daily_riddle_site)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    riddle = soup.find_all('p')[2:6]
    # Riddle matches today's date meaning its a new one and the length means there's a question/answer
    if riddle[0].find(date) != -1 and len(riddle) >= 4:
        question = str(riddle[1])[3:-4]
        answer = str(riddle[2])[3:-4]
        #print(question, answer)
        return question, answer



# In[3]:


def get_daily_horoscopes(sites):
    horoscopes = dict()
    for site in sites:
        page = requests.get(sites[site])
        contents = page.content
        soup = BeautifulSoup(contents, 'html.parser')
        scopes = str(soup.find('p'))
        # +7 for length of </span> and space
        start = scopes.find("</span>") + 7
        if start != -1:
            horoscope = scopes[start:-4]
#             print(site,'\n', horoscope, '\n')
            horoscopes[site] = horoscope

    return horoscopes

def get_today_in_history(amount, site):
    page = requests.get(site)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    events = soup.find_all("li", {"class" : "event"})
    history = dict()
    for event in events:
        if event.text.strip()[3].isdigit():
            history[event.text.strip()[:4]] = event.text.strip()[5:]
        # years 100-999
        elif event.text.strip()[2].isdigit() and event.text.strip()[3] == ' ':
            history[event.text.strip()[:3]] = event.text.strip()[4:]
    return history

def get_daily_quotes(site):
    page = requests.get(site)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    quotes = soup.find_all("div", {"class" : "clearfix"})
    quotes_dict = dict()
    for quote in quotes:
        quote_author = [i for i in quote.text.strip().split('\n') if i]
        quotes_dict[quote_author[1]] = quote_author[0]
    return quotes_dict

def get_famous_birthdays(site):
    page = requests.get(site)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    birthdays = soup.find_all("table", {"class" : "qotdBdTbl"})
    birthday_list = []
    for birthday in birthdays:
        birthday_list = [i for i in birthday.text.strip().split('\n') if i]
    birthday_list = [i for i in birthday_list if i.find(" ") != -1]
    return birthday_list

def get_hourly_forecast(times, site):
    page = requests.get(site)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    current_times = soup.find_all("span", {"class" : "dsx-date"})
    current_temps = soup.find_all("td", {"class" : "temp"})
    current_winds = soup.find_all("td", {"class" : "wind"})
    available_times = []
    temperatures = []
    wind_speeds = []

    for i, t in enumerate(current_times):
        for check in times:
            if t.text.strip() == check:
                available_times.append(t.text.strip())
                temperatures.append(current_temps[i].text.strip())
                wind_speeds.append(current_winds[i].text.strip().strip('mph'))
#     print([available_times, temperatures, wind_speeds])
    return [available_times, temperatures, wind_speeds]

def get_national_days(site):
    page = requests.get(site)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    days = soup.find_all("h3", {"class" : "hed"})
    day = soup.find("div", {"class" : "holiday-title"})
    national_days = []
    try:
        day = day.text.strip()
        day = day[:day.find("–")]
        national_days.append(day)
        for nday in days:
            nDay = nday.text.strip()
            national_days.append(nDay)
    except:
        national_days.append("No National Days Today!")

    return national_days



# In[4]:


def get_bamboozables():
    bamboozable_random_number = str(random.randint(1,60+1))
    bamboozable_img = 'http://www.thinkablepuzzles.com/bamboozables/bamboozable' + bamboozable_random_number + '.jpg'
    bamboozable_answer_site = 'http://www.thinkablepuzzles.com/bamboozables/bamboozable' + bamboozable_random_number + 'answers.shtml'
    page = requests.get(bamboozable_answer_site)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    all_answers = soup.find_all("td")
    answer_list = []
    for answer in all_answers:
        if answer.text.strip().find("bamboozable " + bamboozable_random_number +  " Answers") != -1:
            start = answer.text.strip().find("1.")
            end = answer.text.strip().find("Home", 2)
            answer_nums = answer.text.strip()[start:end]
            answer_list = [answer_nums[answer_nums.find("1. ")+3: answer_nums.find("2. ")].strip(),
                           answer_nums[answer_nums.find("2. ")+3: answer_nums.find("3. ")].strip(),
                           answer_nums[answer_nums.find("3. ")+3: answer_nums.find("4. ")].strip(),
                           answer_nums[answer_nums.find("4. ")+3: answer_nums.find("5. ")].strip(),
                           answer_nums[answer_nums.find("5. ")+3: answer_nums.find("6. ")].strip(),
                           answer_nums[answer_nums.find("6. ")+3:].strip()]

    for i,answer in enumerate(answer_list):
        answer_list[i] = "".join(answer_list[i].split("\\"))
        answer_list[i] = "".join(answer_list[i].split("\r"))
        answer_list[i] = "".join(answer_list[i].split("\n"))
        answer_list[i] = "".join(answer_list[i].split("\t"))
    return bamboozable_img, answer_list


# In[5]:


def getCommonyms(site='http://www.thinkablepuzzles.com/commonyms/commonyms', number_of_puzzles=27):
    answer_list = []
    question_list = []
    quality = True
    while(quality):
        random_number = str(random.randint(1,number_of_puzzles+1))
        question_site =  site + random_number + '.shtml'
        answer_site = site + random_number + 'answers.shtml'
        page = requests.get(question_site)
        contents = page.content
        soup = BeautifulSoup(contents, 'html.parser')
        all_questions = soup.find_all("td")
        for question in all_questions:
            if question.text.strip().find("1.") != -1:
                start = question.text.strip().find("1.")
                end = question.text.strip().find("Home", 2)
                question_nums = question.text.strip()[start:end]
                question_list = [question_nums[question_nums.find("1. ")+3: question_nums.find("2. ")].strip(),
                               question_nums[question_nums.find("2. ")+3: question_nums.find("3. ")].strip(),
                               question_nums[question_nums.find("3. ")+3: question_nums.find("4. ")].strip(),
                               question_nums[question_nums.find("4. ")+3: question_nums.find("5. ")].strip(),
                               question_nums[question_nums.find("5. ")+3: question_nums.find("6. ")].strip(),
                               question_nums[question_nums.find("6. ")+3: question_nums.find("7. ")].strip(),
                               question_nums[question_nums.find("7. ")+3: question_nums.find("8. ")].strip(),
                               question_nums[question_nums.find("8. ")+3: question_nums.find("9. ")].strip(),
                               question_nums[question_nums.find("9. ")+3: question_nums.find("10. ")].strip(),
                               question_nums[question_nums.find("10. ")+3:].strip()]
                break;
        question_list[9] = question_list[9][:question_list[9].find("\n")]
        for i,question in enumerate(question_list):
            question_list[i] = "".join(question_list[i].split("\\"))
            question_list[i] = "".join(question_list[i].split("\r"))
            question_list[i] = "".join(question_list[i].split("\n"))
            question_list[i] = "".join(question_list[i].split("\t"))
            if(len(question_list[i]) == 0):
                quality = False
                break

        if quality == False:
            quality = True
            continue


        page = requests.get(answer_site)
        contents = page.content
        soup = BeautifulSoup(contents, 'html.parser')
        all_answers = soup.find_all("td")
        for answer in all_answers:
            if answer.text.strip().find("1.") != -1:
                start = answer.text.strip().find("1.")
                end = answer.text.strip().find("Home", 2)
                answer_nums = answer.text.strip()[start:end]
                answer_list = [answer_nums[answer_nums.find("1. ")+3: answer_nums.find("2. ")].strip(),
                               answer_nums[answer_nums.find("2. ")+3: answer_nums.find("3. ")].strip(),
                               answer_nums[answer_nums.find("3. ")+3: answer_nums.find("4. ")].strip(),
                               answer_nums[answer_nums.find("4. ")+3: answer_nums.find("5. ")].strip(),
                               answer_nums[answer_nums.find("5. ")+3: answer_nums.find("6. ")].strip(),
                               answer_nums[answer_nums.find("6. ")+3: answer_nums.find("7. ")].strip(),
                               answer_nums[answer_nums.find("7. ")+3: answer_nums.find("8. ")].strip(),
                               answer_nums[answer_nums.find("8. ")+3: answer_nums.find("9. ")].strip(),
                               answer_nums[answer_nums.find("9. ")+3: answer_nums.find("10. ")].strip(),
                               answer_nums[answer_nums.find("10. ")+3:].strip()]
                break
        answer_list[9] = answer_list[9][:answer_list[9].find("\n")]
        for i,answer in enumerate(answer_list):
            answer_list[i] = "".join(answer_list[i].split("\\"))
            answer_list[i] = "".join(answer_list[i].split("\r"))
            answer_list[i] = "".join(answer_list[i].split("\n"))
            answer_list[i] = "".join(answer_list[i].split("\t"))
            if(len(answer_list[i]) == 0):
                quality = True
                break
        else:
            break
#     print(question_list, answer_list)
    return question_list, answer_list



# In[6]:


def create_hink_pink_csv(site='https://www.thinkablepuzzles.com/hinkpinks/hinkpinks', number_of_puzzles=39, name="hinkpink_list.csv"):
    all_questions = []
    all_answers = []
    answer_list = []
    question_list = []
    for i in range(1,number_of_puzzles+1):

        quality = True
        while(quality):
            quality = True
            question_site =  site + str(i) + '.shtml'
            answer_site = site + str(i) + 'answers.shtml'
            page = requests.get(question_site)
            contents = page.content
            soup = BeautifulSoup(contents, 'html.parser')
            all_questions = soup.find_all("p")
            for question in all_questions:
                if question.text.strip().find("1. ") != -1:
                    start = question.text.strip().find("1. ")
                    question_nums = question.text.strip()[start:]
                    question_list += [question_nums[question_nums.find("1. ")+3: question_nums.find("2. ")].strip(),
                                   question_nums[question_nums.find("2. ")+3: question_nums.find("3. ")].strip(),
                                   question_nums[question_nums.find("3. ")+3: question_nums.find("4. ")].strip(),
                                   question_nums[question_nums.find("4. ")+3: question_nums.find("5. ")].strip(),
                                   question_nums[question_nums.find("5. ")+3: question_nums.find("6. ")].strip(),
                                   question_nums[question_nums.find("6. ")+3: question_nums.find("7. ")].strip(),
                                   question_nums[question_nums.find("7. ")+3: question_nums.find("8. ")].strip(),
                                   question_nums[question_nums.find("8. ")+3: question_nums.find("9. ")].strip(),
                                   question_nums[question_nums.find("9. ")+3: question_nums.find("10. ")].strip(),
                                   question_nums[question_nums.find("10. ")+3:].strip()]
                    break;
            for i,question in enumerate(question_list):
                question_list[i] = "".join(question_list[i].split("\\"))
                question_list[i] = "".join(question_list[i].split("\r"))
                question_list[i] = "".join(question_list[i].split("\n"))
                question_list[i] = "".join(question_list[i].split("\t"))
                if(len(question_list[i]) == 0):
                    quality = False
                    break

            if quality == False:
                quality = True
                continue


            page = requests.get(answer_site)
            contents = page.content
            soup = BeautifulSoup(contents, 'html.parser')
            all_answers = soup.find_all("p")
            for answer in all_answers:
                if answer.text.strip().find("1. ") != -1:
                    start = answer.text.strip().find("1. ")
                    answer_nums = answer.text.strip()[start:]
                    answer_list += [answer_nums[answer_nums.find("1. ")+3: answer_nums.find("2. ")].strip(),
                                   answer_nums[answer_nums.find("2. ")+3: answer_nums.find("3. ")].strip(),
                                   answer_nums[answer_nums.find("3. ")+3: answer_nums.find("4. ")].strip(),
                                   answer_nums[answer_nums.find("4. ")+3: answer_nums.find("5. ")].strip(),
                                   answer_nums[answer_nums.find("5. ")+3: answer_nums.find("6. ")].strip(),
                                   answer_nums[answer_nums.find("6. ")+3: answer_nums.find("7. ")].strip(),
                                   answer_nums[answer_nums.find("7. ")+3: answer_nums.find("8. ")].strip(),
                                   answer_nums[answer_nums.find("8. ")+3: answer_nums.find("9. ")].strip(),
                                   answer_nums[answer_nums.find("9. ")+3: answer_nums.find("10. ")].strip(),
                                   answer_nums[answer_nums.find("10. ")+3:].strip()]
                    break
            for i,answer in enumerate(answer_list):
                answer_list[i] = "".join(answer_list[i].split("\\"))
                answer_list[i] = "".join(answer_list[i].split("\r"))
                answer_list[i] = "".join(answer_list[i].split("\n"))
                answer_list[i] = "".join(answer_list[i].split("\t"))
                if(len(answer_list[i]) == 0):
                    quality = True
                    break
            else:
                break

    f = open(name, 'wt')
    try:
        writer = csv.writer(f)

        for i, question in enumerate(question_list):
            writer.writerow((question_list[i], answer_list[i], "thinkable"))
    finally:
        f.close()
        print('DONE writing to file:\t'+name)
    return question_list, answer_list



# In[7]:


def getMadGabs(site='http://www.thinkablepuzzles.com/madgabs/madgabs', number_of_puzzles=51):
    answer_list = []
    question_list = []
    quality = True
    while(quality):
        random_number = str(random.randint(1,number_of_puzzles+1))
        question_site =  site + random_number + '.shtml'
        answer_site = site + random_number + 'answers.shtml'
        page = requests.get(question_site)
        contents = page.content
        soup = BeautifulSoup(contents, 'html.parser')
        all_questions = soup.find_all("p")
        for question in all_questions:
            if question.text.strip().find("1.") != -1:
                start = question.text.strip().find("1.")
                end = question.text.strip().find("Home", 2)
                question_nums = question.text.strip()[start:end]
                question_list = [question_nums[question_nums.find("1. ")+3: question_nums.find("2. ")].strip(),
                               question_nums[question_nums.find("2. ")+3: question_nums.find("3. ")].strip(),
                               question_nums[question_nums.find("3. ")+3: question_nums.find("4. ")].strip(),
                               question_nums[question_nums.find("4. ")+3: question_nums.find("5. ")].strip(),
                               question_nums[question_nums.find("5. ")+3:].strip()]
                break;
        question_list[4] = question_list[4][:question_list[4].find("\n")]
        for i,question in enumerate(question_list):
            question_list[i] = "".join(question_list[i].split("\\"))
            question_list[i] = "".join(question_list[i].split("\r"))
            question_list[i] = "".join(question_list[i].split("\n"))
            question_list[i] = "".join(question_list[i].split("\t"))
            if(len(question_list[i]) == 0):
                quality = False
                break

        if quality == False:
            quality = True
            continue

        if question_list[0].find("s?d=1227") != -1:
            quality= True
            continue

        page = requests.get(answer_site)
        contents = page.content
        soup = BeautifulSoup(contents, 'html.parser')
        all_answers = soup.find_all("td")
        for answer in all_answers:
            if answer.text.strip().find("1.") != -1:
                start = answer.text.strip().find("1.")
                end = answer.text.strip().find("Home", 2)
                answer_nums = answer.text.strip()[start:end]
                answer_list = [answer_nums[answer_nums.find("1. ")+3: answer_nums.find("2. ")].strip(),
                               answer_nums[answer_nums.find("2. ")+3: answer_nums.find("3. ")].strip(),
                               answer_nums[answer_nums.find("3. ")+3: answer_nums.find("4. ")].strip(),
                               answer_nums[answer_nums.find("4. ")+3: answer_nums.find("5. ")].strip(),
                               answer_nums[answer_nums.find("5. ")+3:].strip()]
                break
        answer_list[4] = answer_list[4][:answer_list[4].find("\n")]
        for i,answer in enumerate(answer_list):
            answer_list[i] = "".join(answer_list[i].split("\\"))
            answer_list[i] = "".join(answer_list[i].split("\r"))
            answer_list[i] = "".join(answer_list[i].split("\n"))
            answer_list[i] = "".join(answer_list[i].split("\t"))
            if(len(answer_list[i]) == 0):
                quality = True
                break
        else:
            break
#     print(question_list, answer_list)
    return question_list, answer_list
getMadGabs()


# In[8]:


'''
General process:
1. Get random word
2. Look up word that rhymes with it
3. Look up synonyms for both of the words
'''
def get_word(random_word=''):
    stats = False
    while stats == False:
        if(random_word == ''):
            time.sleep(0.2)
            word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
            response = requests.get(word_site)
            WORDS = response.content.splitlines()
            random_word = WORDS[random.randrange(0,len(WORDS))].decode("utf-8")

        encoded_query = urllib.parse.quote(random_word)
        params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
        params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
        time.sleep(0.2)
        response = requests.get('https://api.phrasefinder.io/search?' + params)

        assert response.status_code == 200
        response = json.loads(json.dumps(response.json()))
        stats = get_word_stats(response)
        if stats == False:
            continue
        else:
            break
    return random_word, stats
def get_word_stats(word_response):
    try:
        stats = [
            word_response["phrases"][0]["mc"],
            word_response["phrases"][0]["vc"],
            word_response["phrases"][0]["sc"]
        ]
        return stats
    except:
        False

def synonyms(term, max_length=12, min_length=4, count=10):
    time.sleep(0.2)
    page = requests.get('http://www.thesaurus.com/browse/{}'.format(term))
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    synonyms = [span.text for span in soup.find_all('li')]
    final = []
    for syn in synonyms:
        if syn == 'Acronyms':
            break
        if syn == 'DEFINITIONS' or syn == 'PREVIOUS' or syn == 'NEXT' or syn == "Slang" or syn == "Emoji":
            continue
        if len(syn) <= max_length and len(syn) >= min_length:
            final.append(syn)
        if syn[len(syn)-2:] == "ed":
            continue
        if syn[len(syn)-3:] == "ing":
            continue
        if syn[len(syn)-2:] == "ly":
            continue
    if len(final) > count:
        return final[:count]
    else:
        return final

def rhyme(term, max_length=12, min_length=4, count=10):
    final = []
    rhymes = pronouncing.rhymes(term)
    for rhyme in rhymes:
        if len(rhyme) <= max_length and len(rhyme) >= min_length:
            if rhyme[len(rhyme)-2:] == "ed":
                continue
            if rhyme[len(rhyme)-3:] == "ing":
                continue
            if rhyme[len(rhyme)-2:] == "ly":
                continue
            final.append(rhyme)
    if len(final) > count:
        return final[:count]
    else:
        return final

def validate_hink_pink(mc_threshold=0, vc_threshold=0, sc_frequency_threshold=0, hinkpink=""):
    random_word, stats = get_word(hinkpink)
    if isinstance(stats, type(None)) or len(stats) < 3:
        return False
    if stats[0] < mc_threshold:
        return False
    if stats[1] < vc_threshold:
        return False
    if stats[2] < sc_frequency_threshold:
        return False

    return True


def hink_pink_generator(mc_threshold=0, vc_threshold=0, sc_frequency_threshold=0, count=1, name="static/lists/hinkpink_list.csv", save=True):
    hink_pinks = []
    generating = True
    counter = 0
    working_counter = 1
    start = 75
    print("\n\nHINK PINK GENERATION\nThis may take awhile, but time estimates will keep you updated\n\n")
    start_time = time.time()
    total_time = 0
    while generating:


        random_word_1, word_stats_1 = get_word()
        if str(random_word_1[0]).isupper():
            continue


        random_syns_1 = synonyms(random_word_1)
        if len(random_syns_1) == 0:
            continue
        random_syn_1 = random_syns_1[0]


        random_syns_2 = rhyme(random_syn_1)
        if len(random_syns_2) == 0:
            continue
        random_syn_2 = random_syns_2[0]


        random_words_2 = synonyms(random_syn_2)
        if len(random_words_2) == 0:
            continue
        random_word_2 = random_words_2[0]


        hinkpink = [random_word_1, random_word_2, random_syn_1, random_syn_2]
        for word in hinkpink:
            if not validate_hink_pink(mc_threshold=mc_threshold,
                          vc_threshold=vc_threshold,
                          sc_frequency_threshold=sc_frequency_threshold,
                          hinkpink=word):
                break
        else:
            hink_pinks.append(hinkpink)
            counter += 1
            working_counter = 1
            print(str(start+counter*2.5)+"%")
            elapsed_time = time.time() - start_time
            start_time = time.time()
            total_time += elapsed_time
            update_time = ((total_time/counter)*(count-counter))/60
            print("Estimated time remaining " + str(round(update_time)) + " minutes\n")
            if save:
                f = open(name, 'a')
                try:
                    writer = csv.writer(f)

                    for question in hink_pinks:
                        writer.writerow((question[0]+" "+ question[1], question[2]+" "+question[3], "generated"))
                finally:
                    f.close()
                    print('DONE writing to file:\t'+ name)
                # 10 minute update
        if time.time() - 60*10*working_counter > start_time:
            print("Still working...")
            working_counter += 1
        if counter == count:
            generating = False

    return hink_pinks


# hink_pink_generator(mc_threshold=250000, vc_threshold=100000, sc_frequency_threshold=0.90, count=10)


# In[9]:


def hink_pink_generator_brute(mc_threshold=0, vc_threshold=0, sc_frequency_threshold=0, count=1, name="static/lists/hinkpink_list.csv", save=True):
    hink_pinks = []
    generating = True
    counter = 0
    start = 75
    print("\n\nBRUTE HINK PINK GENERATION\nThis may take awhile, but time estimates will keep you updated\n\n")
    start_time = time.time()
    total_time = 0
    working_counter = 1
    while generating:
        found=False

        random_word_1, word_stats_1 = get_word()
        if str(random_word_1[0]).isupper():
            continue


        random_syns_1 = synonyms(random_word_1)
        if len(random_syns_1) == 0:
            continue
        for syn1 in random_syns_1:
            random_syn_1 = syn1


            random_syns_2 = rhyme(random_syn_1)
            if len(random_syns_2) == 0:
                continue
            for syn2 in random_syns_2:
                random_syn_2 = syn2


                random_words_2 = synonyms(random_syn_2)
                if len(random_words_2) == 0:
                    continue
                for word2 in random_words_2:
                    random_word_2 = word2

                    # 10 minute update
                    if time.time() - 60*10*working_counter > start_time:
                        print("Still working...")
                        working_counter += 1

                    hinkpink = [random_word_1, random_word_2, random_syn_1, random_syn_2]
                    for word in hinkpink:
                        if not validate_hink_pink(mc_threshold=mc_threshold,
                                      vc_threshold=vc_threshold,
                                      sc_frequency_threshold=sc_frequency_threshold,
                                      hinkpink=word):
                            break
                    else:
                        hink_pinks.append(hinkpink)
                        counter += 1
                        print(str(start+counter*2.5)+"%")
                        elapsed_time = time.time() - start_time
                        start_time = time.time()
                        working_counter = 1
                        total_time += elapsed_time
                        update_time = ((total_time/counter)*(count-counter))/60
                        print("Estimated time remaining " + str(round(update_time)) + " minutes\n")
                        found = True
                        if save:
                            f = open(name, 'a')
                            try:
                                writer = csv.writer(f)

                                for question in hink_pinks:
                                    writer.writerow((question[0]+" "+ question[1], question[2]+" "+question[3], "brute-generated"))
                            finally:
                                f.close()
                                print('DONE writing to file:\t'+ name)
                        break

                if found == True:
                    break
            if found == True:
                break

        if found == False:
            continue
        if counter == count:
            generating = False



    return hink_pinks


# In[10]:


def get_conversation_starters(count=5, conversations_list="static/lists/conversations_list.csv"):
    conversation_starters = []
    with open(conversations_list) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            conversation_starters.append(row[0])
        csv_file.close()
    random_conversations = []
    for i in range(count):
        random_conversations.append(conversation_starters[random.randrange(0,len(conversation_starters))])
    return random_conversations


# In[11]:


def get_hinkpinks(count=10, hinkpink_list="static/lists/hinkpink_list.csv", kind="thinkable"):
    hinkpinks = {'thinkable': [], 'generated': [], 'brute-generated': []}
    with open(hinkpink_list) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if (len(row) == 0) or row[2] == '':
                continue
            else:
                hinkpinks[row[2]].append([row[0], row[1]])
        csv_file.close()
    random_hinkpinks = []
    random_counter = -1
    while (len(random_hinkpinks) < count):
        if(kind == "random"):
            random_counter = random.randrange(0,3)
        if(kind == "thinkable") or random_counter == 0:
            random_hinkpinks.append(hinkpinks['thinkable'][random.randrange(0,len(hinkpinks['thinkable']))])
            continue
        if(kind == "generated") or random_counter == 1:
            random_hinkpinks.append(hinkpinks['generated'][random.randrange(0,len(hinkpinks['generated']))])
            continue
        if(kind == "brute-generated") or random_counter == 2:
            random_hinkpinks.append(hinkpinks['brute-generated'][random.randrange(0,len(hinkpinks['brute-generated']))])
            continue

    return random_hinkpinks


# In[3]:

def create_nav():
    today = datetime.datetime.now().strftime("%B %d")
    day_of_week = calendar.day_name[datetime.date.today().weekday()]

    todays_date = strftime("%m-%d-%Y", localtime())
    available_vitals = dict()
    header = (
        f'<nav>'
        f'<ul>'
          f'<li id="home-container"><i id="home" class="fas fa-home"></i></li>'
          f'<li class="category">'
            f'<a>Previous Vitals</a>'
            f'<ul class="dropdown">')

    available = os.listdir("templates")
    # Add in today's date
    if Path("templates/index" + todays_date +".html").exists():
        available_dates = []
    else:
        available_dates = [todays_date]
    for date in available[1:]:
        start = date.find("index")+5
        end = date.find(".html")
        available_dates.append(date[start:end])

    for date in available_dates:
        year = date[6:]
        month = date[:2]
        day = date[3:5]
        if year in available_vitals:
            if month in available_vitals[year]:
                available_vitals[year][month].append(day)
            else:
                available_vitals[year][month] = [day]
        else:
            available_vitals[year] = {month : []}
            available_vitals[year][month].append(day)
    for year in available_vitals:
        for month_int in available_vitals[year]:
            try:
                month = datetime.date(int(year), int(month_int), 1).strftime('%B')
            except:
                continue
            header += ( f'<li class="dropdown-subcategory">')
            header += (f'<a>{month} {year}</a>'
                            f'<ul class="dropdown month">')

            for day in available_vitals[year][month_int]:
                index = month_int+"-"+day+"-"+year
                header += (f'<li class="subcategory-item"><a id="{index}" class="day">{day}</a></li>')
            header += (f'</ul>')
            header += (f'</li>')
    header += (f'</ul>')
    header += (f'</li>')


    header += ( f'<li class="category" id="generator"><a>Generate New Vitals</a></li>'
                f'<li class="category" id="new-content"><a>Submit New Content</a></li>'
                # f'<li class="category" id="subscribe"><a>Subscribe</a></li>'
                f'<li class="category" id="subscribe"><a>API Documentation</a></li>'
                f'<li class="category" id="about"><a>About</a></li>'
                f'</ul>'
                f'<a id="github" target="_blank" href="https://github.com/CarsonStevens?tab=repositories"><i class="fab fa-github-square"></i></a>'
                f'<section class="theme-switch-wrapper">'
                    f'<label class="theme-switch" for="checkbox">'
                        f'<input type="checkbox" id="checkbox"  />'
                        f'<span class="slider round"></span>'
                    f'</label>'
                f'</section>'
                f'<span id="theme">Theme</span>'
            f'</nav>')

    try:
        with open('templates/nav.html', 'w', encoding='utf-8') as f:
            f.write(header)
        f.close()
        print("Created new nav bar")
    except:
        print("Saving Error in nav bar")

def save_submitted_content(submit_type, submit_content):
    if submit_type == "hinkpink":
        f = open("static/lists/suggestions/hinkpink_suggestions_list.csv", 'a')
        try:
            writer = csv.writer(f)
            hinkpink = submit_content.split(",")
            writer.writerow((hinkpink[0]+" "+ hinkpink[1], hinkpink[2]+" "+hinkpink[3], "user-suggested"))
        finally:
            f.close()
            print('DONE writing submission to file')
    elif submit_type == "conversation":
        f = open("static/lists/suggestions/conversation_suggestions_list.csv", 'a')
        try:
            writer = csv.writer(f)
            writer.writerow([submit_content])
        finally:
            f.close()
            print('DONE writing submission to file')
    elif submit_type == "madgab":
        f = open("static/lists/suggestions/madgab_suggestions_list.csv", 'a')
        try:
            writer = csv.writer(f)
            madgab = submit_content.split(",")
            writer.writerow((madgab[0],madgab[1]))
        finally:
            f.close()
            print('DONE writing submission to file')
    elif submit_type == "commonym":
        f = open("static/lists/suggestions/commonym_suggestions_list.csv", 'a')
        try:
            writer = csv.writer(f)
            commonym = submit_content.split(",")
            writer.writerow((commonym[0], commonym[1]))
        finally:
            f.close()
            print('DONE writing submission to file')
    elif submit_type == "riddle":
        f = open("static/lists/suggestions/riddle_suggestions_list.csv", 'a')
        try:
            writer = csv.writer(f)
            riddle = submit_content.split("$")
            writer.writerow((riddle[0],riddle[1]))
        finally:
            f.close()
            print('DONE writing submission to file')
    elif submit_type == "suggestion":
            f = open("static/lists/suggestions/suggestions_list.csv", 'a')
            try:
                writer = csv.writer(f)
                writer.writerow([submit_content])
            finally:
                f.close()
                print('DONE writing submission to file')
    else:
        return False
    return True

def generate_vitals(hinkpink_type="thinkable", hinkpink_count=10, conversation_count=5, custom=False):

    todays_date = strftime("%m-%d-%Y", localtime())
    daily_riddle_site = 'https://www.riddles.com/riddle-of-the-day'
    day_in_history_site = 'https://www.onthisday.com/'
    daily_quote_site = 'https://www.brainyquote.com/quote_of_the_day'
    national_days_site = 'https://nationaltoday.com/what-is-today/'
    hourly_weather_site = 'https://weather.com/weather/hourbyhour/l/8cd1a4fdf1a3fddbdd025b0f20f49602aa7fc5b410cf85c2866e485bd1e375e4'
    daily_chinese_horoscope_sites = {'Ox'     : 'https://www.astrology.com/horoscope/daily-chinese/ox.html',
                                     'Sheep'  : 'https://www.astrology.com/horoscope/daily-chinese/sheep.html',
                                     'Rat'    : 'https://www.astrology.com/horoscope/daily-chinese/rat.html',
                                     'Snake'  : 'https://www.astrology.com/horoscope/daily-chinese/snake.html',
                                     'Dragon' : 'https://www.astrology.com/horoscope/daily-chinese/dragon.html',
                                     'Tiger'  : 'https://www.astrology.com/horoscope/daily-chinese/tiger.html',
                                     'Rabbit'  : 'https://www.astrology.com/horoscope/daily-chinese/rabbit.html',
                                     'Horse'  : 'https://www.astrology.com/horoscope/daily-chinese/horse.html',
                                     'Monkey' : 'https://www.astrology.com/horoscope/daily-chinese/monkey.html',
                                     'Rooster': 'https://www.astrology.com/horoscope/daily-chinese/rooster.html',
                                     'Dog'    : 'https://www.astrology.com/horoscope/daily-chinese/dog.html',
                                     'Pig'    : 'https://www.astrology.com/horoscope/daily-chinese/pig.html'
                                    }
    daily_horoscope_sites = {'Aires'       : 'https://www.astrology.com/horoscope/daily/aries.html',
                             'Taurus'      : 'https://www.astrology.com/horoscope/daily/taurus.html',
                             'Gemini'      : 'https://www.astrology.com/horoscope/daily/gemini.html',
                             'Cancer'      : 'https://www.astrology.com/horoscope/daily/cancer.html',
                             'Leo'         : 'https://www.astrology.com/horoscope/daily/leo.html',
                             'Virgo'       : 'https://www.astrology.com/horoscope/daily/virgo.html',
                             'Libra'       : 'https://www.astrology.com/horoscope/daily/libra.html',
                             'Scorpio'     : 'https://www.astrology.com/horoscope/daily/scorpio.html',
                             'Sagittarius' : 'https://www.astrology.com/horoscope/daily/sagittarius.html',
                             'Capricorn'   : 'https://www.astrology.com/horoscope/daily/capricorn.html',
                             'Aquarius'    : 'https://www.astrology.com/horoscope/daily/aquarius.html',
                             'Pisces'      : 'https://www.astrology.com/horoscope/daily/pisces.html'
                           }



    print("Starting to compile page...")
    conversation_list = get_conversation_starters(count=conversation_count)
    daily_horoscopes_dict = get_daily_horoscopes(daily_horoscope_sites)
    print("10%")
    daily_chinese_horoscope_dict = get_daily_horoscopes(daily_chinese_horoscope_sites)
    print("20%")
    daily_riddle_question, daily_riddle_answer = get_daily_riddle(daily_riddle_site, todays_date)
    print("25%")
    history = get_today_in_history(5, day_in_history_site)
    print("35%")
    daily_quotes_dict = get_daily_quotes(daily_quote_site)
    print("45%")
    daily_famous_birthdays = get_famous_birthdays(daily_quote_site)
    print("50%")
    hourly_forecast = get_hourly_forecast(["8:00 am", "11:00 am", "1:00 pm", "6:00 pm"], hourly_weather_site)
    print("55%")
    national_days = get_national_days(national_days_site)
    print("60%")
    bamboozable_img, bamboozable_answers = get_bamboozables()
    print("70%")
    commonym_questions, commonym_answers = getCommonyms('http://www.thinkablepuzzles.com/commonyms/commonym', 27)
    print("80%")
    madgab_questions, madgab_answers = getMadGabs()
    print("90%")
    hink_pinks = get_hinkpinks(kind=hinkpink_type, count=hinkpink_count)
    print("100%")


    year = datetime.datetime.now().strftime("%Y")
    today = datetime.datetime.now().strftime("%B %d")
    day_of_week = calendar.day_name[datetime.date.today().weekday()]

    todays_date = strftime("%m-%d-%Y", localtime())
    head = "{% include 'head.html' %}"
    nav = "{% include 'nav.html' %}"
    logo = "{{ url_for(\'static\', filename=\'images/ERC-Home-Logo.png\') }}"
    header = (f'<!DOCTYPE html><html lang="en" dir="ltr">')
    header += (
            f'{head}'
            f'{nav}'
            f'<header>'
                f'<table id="heading">'
                    f'<tr>'
                        f'<td>'
                            f'<h1 class="grand title"><img src="{logo}" class="logo" /> Daily Vitals</h1>'
                            f'<h2 class="grand title">{day_of_week}</br>{today}<sup class="th">th</sup>, {year}</h2>'
                        f'</td>'
                        f'<td>'
                            f'<section class="weather">'
                                f'<table class="forecast">'
                                    f'<caption class="title">Weather Forecast</caption>'
                                    f'<tbody>'
                                        f'<tr>'
                                            f'<th>Time</th>'
                                            f'<th>Temperature</th>'
                                            f'<th>Wind</th>'
                                        f'</tr>'
                                        f'<tr>'
                                            f'<td>8:00 <em class="meridiem">am</em></td>')
    missed_times_counter = 0
    try:
        if (len(hourly_forecast[0]) > 3):
            header += (                     f'<td>{hourly_forecast[1][0][:len(hourly_forecast[1][0])-1]}&deg</td>'
                                            f'<td>{hourly_forecast[2][0]}<em class="speed">mph</em></td>'
                                        f'</tr>'
                                        f'<tr>'
                                            f'<td>11:00 <em class="meridiem">am</em></td>')
        else:
            missed_times_counter += 1
            assert(False)
    except:
        header += (                         f'<td>N/A</td>'
                                            f'<td>N/A<em class="speed"></em></td>'
                                        f'</tr>'
                                        f'<tr>'
                                            f'<td>11:00 <em class="meridiem">am</em></td>')
    try:
        if (len(hourly_forecast[0])> 2):
            header += (                     f'<td>{hourly_forecast[1][1-missed_times_counter][:len(hourly_forecast[1][1-missed_times_counter])-1]}&deg</td>'
                                            f'<td>{hourly_forecast[2][1-missed_times_counter]}<em class="speed">mph</em></td>'
                                        f'</tr>'
                                        f'<tr>'
                                            f'<td>1:00 <em class="meridiem">pm</em></td>')
        else:
            missed_times_counter += 1
            assert(False)
    except:
        header += (                         f'<td>N/A</td>'
                                            f'<td>N/A<em class="speed"></em></td>'
                                        f'</tr>'
                                        f'<tr>'
                                            f'<td>1:00 <em class="meridiem">pm</em></td>')
    try:
        if (len(hourly_forecast[0])> 1):
            header += (                     f'<td>{hourly_forecast[1][2-missed_times_counter][:len(hourly_forecast[1][2-missed_times_counter])-1]}&deg</td>'
                                            f'<td>{hourly_forecast[2][2-missed_times_counter]}<em class="speed">mph</em></td>'
                                        f'</tr>'
                                        f'<tr>'
                                            f'<td>6:00 <em class="meridiem">pm</em></td>')
        else:
            missed_times_counter += 1
            assert(False)
    except:
        header += (                         f'<td>N/A</td>'
                                            f'<td>N/A<em class="speed"></em></td>'
                                        f'</tr>'
                                        f'<tr>'
                                            f'<td>6:00 <em class="meridiem">pm</em></td>')
    try:
        if (len(hourly_forecast[0])> 0):
            header += (                         f'<td>{hourly_forecast[1][3-missed_times_counter][:len(hourly_forecast[1][3-missed_times_counter])-1]}&deg</td>'
                                                f'<td>{hourly_forecast[2][3-missed_times_counter]}<em class="speed">mph</em></td>'
                                            f'</tr>'
                                        f'<tbody>'
                                    f'</table>'
                                f'</section>'
                            f'</td>'
                        f'</tr>'
                    f'</table>'
                f'</header>')
        else:
            assert(False)
    except:
        header += (                         f'<td>N/A</td>'
                                            f'<td>N/A<em class="speed"></em></td>'
                                        f'</tr>'
                                    f'<tbody>'
                                f'</table>'
                            f'</section>'
                        f'</td>'
                    f'</tr>'
                f'</table>'
            f'</header>')

    main = (

    f'<main>'
        f'<table class="column-format">'
            f'<tbody>'
                f'<tr>'
                    f'<td colspan="3">'
                        f'<section id="daily-info">'
                            f'<section class="daily-info-wrapper">'
                                f'<section id="national-days">'
                                    f'<h4 class="grand title">National Days</h4>'
                                        f'<ol>'
    )
    for day in national_days:
        main += f'<li>{day}</li>'


    main += (
                                        f'</ol>'
                                    f'</section>'
                                f'</section>'
                                f'<section class="daily-info-wrapper">'
                                    f'<section id="birthdays">'
                                        f'<h4 class="grand title">Famous Birthdays</h4>'
                                        f'<ol>'
    )

    for birthday in daily_famous_birthdays:
        main += f'<li>{birthday}</li>'

    main += (
                                        f'</ol>'
                                    f'</section>'
                                f'</section>'
                            f'<section class="daily-info-wrapper">'
                                f'<section id="riddle">'
                                    f'<h4 class="grand title">Riddle</h4>'
                                    f'<p>{daily_riddle_question}</p>'
                                f'</section>'
                            f'</section>'
                        f'</section>'
                    f'</td>'
                f'</tr>'
                f'<tr>'
                    f'<td colspan="3">'
                        f'<section id="day-in-history">'
                            f'<h3 class="grand title">This Day in History</h3>'
    )

    for date in sorted(history):
        main += (
            f'<section class="history-wrapper">'
                f'<p class="history-context">'
                    f'<strong class="year">{date} ~ </strong>{history[date]}'
                f'</p>'
            f'</section>'
        )

    main += (
                        f'</section>'
                    f'</td>'
                f'</tr>'
                f'<tr>'
                    f'<td colspan="3">'
                        f'<section id="conversation">'
                    f'<h3 class="grand title">Conversation Starters</h3>'
                    f'<ul>'
    )

    for conversation in conversation_list:
        main += f'<li><i class="bullet fas fa-chevron-right"></i> {conversation}</li>'

    main += (
                    f'</ul>'
                f'</section>'
            f'</td>'
        f'</tr>'
        f'<tr>'
            f'<td colspan="3">'
                f'<h3 class="grand title" style="text-align: center">Quotes</h3>'
                f'<section id="quotes">'
    )

    quote_order = [
        'Quote of the Day',
        'Love Quote of the Day',
        'Art Quote of the Day',
        'Nature Quote of the Day',
        'Funny Quote of the Day']

    for i, author in enumerate(daily_quotes_dict):
        main += (
            f'<section class="quote-wrapper">'
                f'<h5 class="grand">{quote_order[i]}</h5>'
                f'<p>{daily_quotes_dict[author]}'
                    f'<span class="poet"> ~ {author}</span>'
                f'</p>'
            f'</section>'
        )
    main += (
                f'</section>'
            f'</td>'
        f'</tr>'
        f'<tr>'
            f'<td colspan="2">'
                f'<section id="horoscope">'
                    f'<h3 class="grand title">Horoscopes</h3>'
    )

    if len(daily_horoscopes_dict) ==12:
        for horoscope in daily_horoscopes_dict:
            main += (
                f'<section class="horoscope">'
                    f'<h4 class="grand">{horoscope}</h4>'
                    f'<p>{daily_horoscopes_dict[horoscope]}</p>'
                f'</section>'
            )
    else:
        assert(False)

    main += (
            f'</section>'
        f'</td>'
        f'<td>'
            f'<section id="chinese">'
                f'<h3 class="grand title" >Chinese Horoscopes</h3>'
    )

    if len(daily_chinese_horoscope_dict) == 12:
        for horoscope in daily_chinese_horoscope_dict:
            main += (
                f'<section class="horoscope">'
                    f'<h4 class="grand">{horoscope}</h4>'
                    f'<p>{daily_chinese_horoscope_dict[horoscope]}</p>'
                f'</section>'
            )
    else:
        assert(False)

    main += (
                f'</section>'
            f'</td>'
        f'</tr>'
        f'<tr>'
            f'<td colspan="3">'
                f'<h3 class="grand title" style="text-align: center">Word Puzzles</h3>'
                f'<section id="word-puzzles">'
                    f'<section class="word-puzzle-wrapper">'
                        f'<section id="hink-pinks">'
                            f'<h4 class="grand">Hink Pinks</h4>'
                            f'<ol>'
    )
    for hinkpink in hink_pinks:
        main += (f'<li>{hinkpink[0]}</li>')


    main += (       f'</ol>'
                f'</section>'
              f'</section>'
              f'<section class="word-puzzle-wrapper">'
                f'<section id="commonyms">'
                  f'<h4 class="grand">Commonyms</h4>'
                  f'<ol>')
    for commonym in commonym_questions:
        main += ((f'<li>{commonym}</li>'))

    main += (
                  f'</ol>'
                f'</section>'
              f'</section>'
              f'<section class="word-puzzle-wrapper">'
                f'<section id="mad-gabs">'
                  f'<h4 class="grand">Mad Gabs</h4>'
                  f'<ol>'
    )

    for gab in madgab_questions:
         main += ((f'<li>{gab}</li>'))

    main += (         f'</ol>'
                    f'</section>'
                  f'</section>'
                f'</section>'
              f'</td>'
            f'</tr>'
            f'<tr>'
              f'<td colspan="3">'
                f'<section id="bamboozables">'
                  f'<h4 class="grand">Bamboozables</h4>'
                  f'<img id="bamboozable-img" class="no-filter" src="{bamboozable_img}" />'
                f'</section>'
              f'</td>'
            f'</tr>'
          f'</tbody>'
        f'</table>'
      f'</main>'
    )

    answers = (
        f'<h3 class="grand title" id="answer-page">Answers</h3>'
        f'<section class="hider">Show Answers!</section>'
        f'<section class="hidden">'
            f'<section id="answers">'
              f'<section class="word-puzzle-wrapper">'
                  f'<h4 class="grand">Hink Pinks</h4>'
                  f'<ol class="answer-style">')

    for hink in hink_pinks:
        answers += (f'<li>{hink[1]}</li>')

    answers += (
            f'</ol>'
          f'</section>'
          f'<section class="word-puzzle-wrapper">'
            f'<h4 class="grand">Commonymns</h4>'
            f'<ol class="answer-style">')

    for answer in commonym_answers:
        answers += (f'<li>{answer}</li>')

    answers += (
            f'<ol>'
          f'</section>'
          f'<section class="word-puzzle-wrapper">'
            f'<h4 class="grand">Mad Gabs</h4>'
            f'<ol class="answer-style">')

    for answer in madgab_answers:
        answers += (f'<li>{answer}</li>')

    answers += (
            f'</ol>'
          f'</section>'
          f'<section class="word-puzzle-wrapper">'
            f'<h4 class="grand">Bamboozables</h4>'
            f'<ol class="answer-style">'
    )

    for answer in bamboozable_answers:
        answers += (f'<li>{answer}</li>')

    theme_toggle_flask = "{{ url_for('static', filename='javascript/darktoggle.js') }}"
    answers += (
                f'</ol>'
              f'</section>'
              f'<section class="word-puzzle-wrapper">'
                f'<h4 class="grand">Riddle</h4>'
                    f'<p>{daily_riddle_answer}</p>'
              f'</section>'
          f'</section>'
      f'</section>'
      f'<footer>'
        f'<p>Information Scraped from: <a href="https://www.riddles.com/riddle-of-the-day">riddles.com</a>, <a href="https://www.onthisday.com/">onthisday.com</a>, <a href="https://www.brainyquote.com/quote_of_the_day">brainyquote.com</a>, <a href="https://nationaltoday.com/what-is-today/">nationaltoday.com</a>, <a href="https://weather.com/weather/hourbyhour/l/8cd1a4fdf1a3fddbdd025b0f20f49602aa7fc5b410cf85c2866e485bd1e375e4">weather.com</a>, <a href="https://www.astrology.com/">astrology.com<a>, <a href="http://www.thinkablepuzzles.com">thinkablepuzzles.com</a></p>'
      f'</footer>'
      f'<script type="text/javascript" src="{theme_toggle_flask}"></script>'
     f'</body>'
    f'</html>'
    )

    if not custom:
        try:
            with open('templates/index'+todays_date+".html", 'w', encoding='utf-8') as f:
                f.write((header+main+answers))
            f.close()
            create_nav()
            print("done\n\n\n\n\n\n\n")
        except:
            print("Saving Error")
    else:
        create_nav()
        return (header+main+answers)
