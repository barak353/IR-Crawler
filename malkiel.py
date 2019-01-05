# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import requests
from collections import defaultdict
from collections import OrderedDict
import os
import csv
import math

path = r'%s' % os.getcwd().replace('\\', '/')

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

links = []

pages_splits = []

word_dict=[]

terms = ["security", "camera"]



def save_all_links_as_html(from_page, to_page, results_per_page):

    print("Saving all links as html files...")

    count = 0

    for i in range(from_page, to_page + 1):
        source = requests.get("http://www.dx.com/s/security+camera?cateId=0&cateName=All%20Categories&PageIndex=" + str(i) + "#sortBar", headers=agent).text
        soup = BeautifulSoup(source)

        links = []

        for k in range(0, results_per_page):
            results = soup.findAll("a", {"id": "content_ProductList1_rpProducts_lnkShortHeadLine1_"+str(k)})
            links.append(results[0]["href"])

            source2 = requests.get(links[k], headers=agent).text
            soup2 = BeautifulSoup(source2)

            with open("dxHTML/" + str(count) + ".html", "w") as file:
                file.write(str(soup2))

            print(count)


            count = count + 1


def scan_links(number_of_html_files):

    print("Scaning links...")


    for j in range(0, number_of_html_files):

        soup2 = BeautifulSoup(open(path+"/dxHTML/" + str(j) + ".html"))


        results2 = soup2.findAll("p", {"class": "short_tit"})
        if (len(results2) > 0):
            print(results2[0].text)

            text = results2[0].text.lower().replace('&amp;', '').replace(":", ' ').replace("(", ' ').replace(")", ' ').replace(";", ' ')


            split_text = text.split(" ")


            for w in range(len(split_text)):
                split_text[w] = split_text[w].strip("+").strip("-").strip(",").strip(".").replace("/", "")

            pages_splits.append(split_text)

            for word in split_text:
                word_dict.append(word)

        else:
            pages_splits.append([])



def create_index(data):
    index = defaultdict(list)
    for i, tokens in enumerate(data):
        for token in tokens:
            index[token].append(i)
    return index


def create_inverted_index():

    index = create_index(pages_splits)
    distinct_words = list(set(word_dict))

    ordered_index = OrderedDict(sorted(index.items(), key=lambda item: len(item[1]), reverse=True))

    print(ordered_index)

    # csv file for inverted index
    csv_file = open('inverted_index.csv', 'w+')
    writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

    for word in distinct_words:
        if word in ordered_index:

            writer.writerow([str(word), str(ordered_index[word]), len(ordered_index[word])])

    print("Inverted index was created")

    return index




def calculate_tf_idf(index_array, max_documents, terms):

    # csv file for calculating tf-idf of each word
    csv_file = open('tf_idf.csv', 'w+')
    writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

    tf_idf_row_per_term = [0] * max_documents

    row_1 = ["TERM"]
    for i in range(0, max_documents):
        row_1.append(i)
    writer.writerow(row_1)

    for term in terms:

        if term in index_array:


            for number_of_page in index_array[term]:

                num_that_word_repeats_in_page = 0

                for k in range(0, len(pages_splits[number_of_page])):
                    if pages_splits[number_of_page][k] == term:
                        num_that_word_repeats_in_page = num_that_word_repeats_in_page + 1


                tf_idf_row_per_term[number_of_page] = num_that_word_repeats_in_page


    for term in terms:

        row_x = [term]


        for i in range(0, max_documents):

            tf_idf = 0

            if term in index_array and tf_idf_row_per_term[i] is not 0:
                print(tf_idf_row_per_term)
                number_of_pages_that_word_occurred = len(list(set(index_array[term]))) # set - for distinct pages
                num_that_word_repeats_in_page = tf_idf_row_per_term[i]
                tf_idf = (1 + math.log(num_that_word_repeats_in_page, 10)) * math.log((max_documents / number_of_pages_that_word_occurred), 10)

            row_x.append(tf_idf)

        writer.writerow(row_x)






save_all_links_as_html(1, 1, 20) # save all links to 'dxHTML' folder

scan_links(20) # scans links and created dictionaries of words and sentences

# create_inverted_index() - creates inverted_index list and csv file of word, repeats number, which pages
calculate_tf_idf(create_inverted_index(), 20, terms) # calculate tf-idf for each term in 'terms' list
