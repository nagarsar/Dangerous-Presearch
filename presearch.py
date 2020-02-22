from bs4 import BeautifulSoup
from random import randrange
from datetime import datetime
import random
import requests
import os
import csv
import time
import json

#--------------------------------------------------------#
# INSTRUCTIONS                                           #
# - Faire beaucoup de comptes sur presearch.org          #
# - Mettre un crontab quotidien :                        #
# 0 0 * * * cd /root && python presearch.py              #
# outil : https://crontab.guru/                          #
# renseigner le bon nombre de comptes que vous avez      #
# cela correspond aux nombreDinscrit                     #
# - Activer ACTIVE_PRESEARCH                             #
# - garder 32 requetes !                                 #
#--------------------------------------------------------#

#--------------------------------------------------------#
# Variables globales                                     #
#--------------------------------------------------------#
ACTIVE_PRESEARCH = True          # active le programme Presearch /!\ risque de baniement, controlez
ACTIVE_DEBUG     = False         # affiche les requetes deja envoyees
OPEN             = False         # csv n'a plus besoin d etre ouvert apres
nombreDinscrits  = 5            # depend motivation a creer des comptes a la chaine
nombreRequetes   = 32            # 8 / 0.25 = 32
nombreTitres     = 400            # titre d'articles reddit multiple de 25 (max 425)
h_debut          = "07:00"       # matin
h_fin            = "23:00"       # soir
filePath         = 'items.json'  # liste des userss

#--------------------------------------------------------#
# Scrapper de titres Reddit, collect des phrases         #
# Humaines pour un rendu plus realiste                   #
#--------------------------------------------------------#
def load_reddit_titles():

  url = "https://old.reddit.com/r/datascience/"
  headers = {'User-Agent': 'Mozilla/5.0'}
  page = requests.get(url, headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')

  attrs = {'class': 'thing', 'data-domain': 'self.datascience'}
  counter = 1
  while counter <= nombreTitres:
      for post in soup.find_all("div", attrs=attrs):
          title = post.find("p", class_="title").text
          # j a l o u s i e 
          title=title.replace("Tooling", "",1)
          title=title.replace("Projects", "", 1)
          title=title.replace("Career", "", 1)
          title=title.replace("Discussion", "", 1)
          title=title.replace("Networking", "", 1)
          title=title.replace("Education", "", 1)
          title=title.replace("Job Search", "", 1)
          title=title.replace("Fun/Trivia", "", 1)
          title=title.replace("Meta", "", 1)
          title=title.replace("(self.datascience)", "", 1)
          #print(title)

          post_line = [title]

          with open('output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(post_line)
          
          counter += 1
      
      next_button = soup.find("span", class_="next-button")
      next_page_link = next_button.find("a").attrs['href']
      page = requests.get(next_page_link, headers=headers)
      soup = BeautifulSoup(page.text, 'html.parser')

  f.close()

#--------------------------------------------------------#
#  Charge le fichier csv, scrappe des donnes sur reddit  #
#--------------------------------------------------------#
print("scraping...")
os.remove("output.csv")
load_reddit_titles()

#--------------------------------------------------------#
# Collecte les noms prenoms et forme une mailList        #
#--------------------------------------------------------#
mailList = []
with open(filePath) as file:
    data = json.load(file)
for i in range(len(data)):
    mailList.append(data[i]['first_name'] + '.' + data[i]['last_name'] + data[i]['base'])
print(mailList[random.randint(0,nombreDinscrits-1)])
#print(mailList)

#--------------------------------------------------------#
# chaque id inclus dans [0 - nombreDinscrits-1]          #
# doit effectuer 32 requetes aleatoires par jour         #
# random_datetime = randomDate(h_debut,h_fin)            #
# print(random_datetime)                                 #
#--------------------------------------------------------#
def randomDate(start, end):
    frmt = '%d-%m-%Y %H:%M'

    now = datetime.now()
    base = str(now.day)+"-"+str(now.month)+"-"+str(now.year)

    stime = time.mktime(time.strptime(base+" "+start, frmt))
    etime = time.mktime(time.strptime(base+" "+end, frmt))

    ptime = stime + random.random() * (etime - stime)
    dt = datetime.fromtimestamp(time.mktime(time.localtime(ptime)))
    
    return dt
    # random_datetime = randomDate(h_debut,h_fin)
    # print(random_datetime)

#--------------------------------------------------------#
# Creer un tableau temporaire de 2 dimensions            #
# Ranges des dates aleatoires alant de h_debut a h_fin   #
#--------------------------------------------------------#
planning_tmp = [[]]
for i in range(0, nombreDinscrits):
  planning_tmp.append([])
  for j in range(0,nombreRequetes):
    planning_tmp[i].append( str( randomDate(h_debut, h_fin) ) )

#--------------------------------------------------------#
# trier du plus tot au plus tard chaque requete          #
#--------------------------------------------------------#
planning = [[]]
for i in range(0, nombreDinscrits):
  planning[i] = sorted( planning_tmp[i] )
  planning.append([])

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M") 
# print( planning[nombreDinscrits-1][nombreRequetes-1] )

#--------------------------------------------------------#
# Se connecte avec les identidiants contenus dans le JSON#
# Formule une requete aupres de google                   #
# Indique le nombre de points obtenus                    #
#--------------------------------------------------------#
def formulate_Request(mail_password):
  #email = "albertin6@yopmail.com"
  #password = "albertin6@yopmail.com"
  #mail_password="Maura.Ivamy@yopmail.com" # TEMPORAIRE !!!

  r = requests.Session()
  content = r.get("https://www.presearch.org").content

  soup = BeautifulSoup(content, 'html.parser')
  token = soup.find("input", {
    "name": "_token"
  })["value"]

  payload = "_token={}&login_form=1&email={}&password={}".format(token, mail_password, mail_password)
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  login = r.post("https://www.presearch.org/api/auth/login", data = payload, headers = headers)

  #for x in range(0, 32):
  #words = random.choice(["apple", "life", "hacker", "facebook", "abeyancies", "abeyancy", "abeyant", "abfarad", "abfarads", "abhenries", "abhenry", "abhenrys", "abhominable", "abhor", "abhorred", "abhorrence", "abhorrences", "abhorrencies", "abhorrency", "abhorrent", "abhorrently", "abhorrer", "abhorrers", "abhorring", "abhorrings", "abhors", "abid", "abidance", "abidances", "abidden", "abide", "abided", "abider", "abiders", "abides", "abiding", "abidingly", "abidings", "abies", "abietic", "abigail", "abigails", "abilities", "ability", "abiogeneses", "abiogenesis", "abiogenetic", "abiogenetically", "abiogenic", "abiogenically", "abiogenist", "abiogenists", "abiological", "abioses", "abiosis", "abiotic", "abiotically", "abiotrophic", "abiotrophies", "abiotrophy"])
  words = get_random_title()

  payload = "term={}&provider_id=98&_token={}".format(words, token)
  r.post("https://www.presearch.org/search", data = payload, headers = headers)
  
  print("Term:{} Search done!".format(words))
  #time.sleep(15)
  r = r.get("https://www.presearch.org/")
  soup = BeautifulSoup(r.content, 'html.parser')
  balance = soup.find("span", {
    "class": "number ajax balance"
  })
  print("Dear {}, Your Balance is now: {} PRE".format(str(mail_password), balance.text))

#--------------------------------------------------------#
# Obtention d'une ligne aleatoire depuis le fichier      #
# precedement telecharge                                 #
#--------------------------------------------------------#
def get_random_title():
  # csv file name 
  filename = "output.csv"
  rows = [] 
  global OPEN, REQUEST

  # reading csv file 
  with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile)     
    for row in csvreader: 
      rows.append(row) 
    
    if OPEN == False:
      print("Total no. of rows: %d"%(csvreader.line_num)) 
    OPEN = True
    
  try:
    REQUEST = rows[random.randint(0,nombreTitres)]
  except:
    REQUEST = rows[random.randint(0,nombreTitres)]
        
  return str(REQUEST)

#--------------------------------------------------------#
# Prend toutes les valeurs du planning                   #
# et enleve les lignes des dates deja depassees          #
# permet uniquement de desengorger le programme          #
# doit etre effectuer toutes les minutes                 #
#--------------------------------------------------------#
def refresh_list(t,val_to_check):
  for i in reversed(range(len(t))):
    for j in reversed(range(len(t[i]))):
      if t[i][j] < val_to_check:
        t[i].pop(j)
        if ACTIVE_DEBUG == True :
          print("{} {} deleted".format(  str(t[i][j]) ,t[i][j]) )
  print("planning mis a jour")

#--------------------------------------------------------#
# Lance une requete si le test est verifier              #
# doit etre effectuer toute les 60 secondes              #
#--------------------------------------------------------#
def check_minute(t, timestamp):

  start = time.time()

  count_h = 0
  count_m = 0

  h = timestamp[11:13]
  m = timestamp[14:16]
  print("Il est {}:{} ".format(h, m))

  for i in range(len(t)):
    for j in range(len(t[i])):
      h_t = t[i][j][11:13]
      m_t = t[i][j][14:16]
      #print("depuis loop {}:{} ".format(h_t, m_t))

      if h_t == h:
        count_h+=1
        #print("Dans l heure qui suit")
        if m_t == m:
          count_m+=1
          #print("Dans la minute qui suit")

          """ -----> LANCER LES REQUETES ICI <------ """

          print("id:{} mail:{} prevu a:{}:{} REQUEST ".format( i , mailList[i], h_t, m_t ) )

          if ACTIVE_PRESEARCH == True:
            formulate_Request( mailList[i] )

          """ ----->  FIN DES REQUETES ICI   <------ """
  end     = time.time()
  elapsed = end - start

  print("temps ecoule:{} pour nombreInscrit:{} et nombreRequetes:{}".format(elapsed, nombreDinscrits, nombreRequetes ) )
  print("Au total, {} requetes prevues dans l heure qui suit et {} requetes prevues dans la minute".format(count_h, count_m ) )

#--------------------------------------------------------#
# Indique les requetes qui ont deja ete realiser         #
# na pas lieu d etre dans le programme                   #
# c est simplement pour debugger                         #
#--------------------------------------------------------#
def check_planning(t, val_to_check):
  for i in range(len(t)):
    for j in range(len(t[i])):
      if t[i][j] < val_to_check:
        if ACTIVE_DEBUG == True :
          print("Presearch id:{} deja realisee a : {}".format(i, t[i][j]) )
      
#--------------------------------------------------------#
# Affiche le planning                                    #
#--------------------------------------------------------#
def print_Planning():
  for i in range(len(planning)):
    for j in range(len(planning[i])):
      print("id:{} a : {}".format(i, planning[i][j]) )

#--------------------------------------------------------#
# Setup - n'est appeler qu au lancement du programme     #
#--------------------------------------------------------#
print("planning complet...")
#print_Planning()

print("refresh list...")
refresh_list(planning,timestamp)

""" print("requete restantes...")
print_Planning()

print("verification...")
check_planning(planning,timestamp)

print("planning actuel")
print(planning) """

print("check minute...")
check_minute(planning, timestamp)

print("get_random_title...")
get_random_title()

#--------------------------------------------------------#
# Loops                                                  #
#--------------------------------------------------------#
# time loops                                             #
# Loop1 = 60s                                            #
# Loop2 = 300s                                           #
# Loop3 = 10s                                            #
#--------------------------------------------------------#
start_Loop1= time.time()
start_Loop2= time.time()
start_Loop3= time.time()

while (1):
  
  """ Loop1 = 60s """
  if time.time() - start_Loop1 > 60 :
    print("60 secondes ecoulees")
    if ACTIVE_PRESEARCH == True:
      check_minute(planning, timestamp)
      refresh_list(planning,timestamp)
    start_Loop1 = time.time() 

  """ Loop2 = 300s """
  if time.time() - start_Loop2 > 300 :
    print("300 secondes ecoulees")
    start_Loop2 = time.time() 

  """ Loop3 = 10s """
  if time.time() - start_Loop3 > 10 :
    #if OPEN == True :
      #print( get_random_title() )
    start_Loop3 = time.time() 