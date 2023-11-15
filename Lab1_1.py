import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import re
from collections import Counter

# Etape 1 :
# Fonction "mots_du_texte". Cette fonction va mettre sous forme de liste avec une indication de l'occurence des différents mot du texte que vous allez taper.
def mots_du_texte(texte):
    mots = texte.split()
    occurrences = {}
    for mot in mots:
        if mot in occurrences:
            occurrences[mot] += 1
        else:
            occurrences[mot] = 1
    return occurrences

# La variable "texte" est le texte qu'on donne au programme qui mets la variable sous forme de chaîne de caractères
texte = "Je suis en Bachelor Cybersécurité. Je suis en licence Cybersécurité. Je suis en BAC+3"
dictionnaire = mots_du_texte(texte)
print(dictionnaire)

#Etape 2 :
# ouverture du fichier "mots_parasites.csv qui va voir tout les mots qui doivent être enlevée.
with open('mots_parasites.csv', 'r') as f:
    mots_a_supprimer = [mot.lower()  for  mot  in f.read().splitlines()]

# La méthode split() permet de couper à chaque espace blanc le texte qui se trouve dans le texte.
mots = texte.split()

# Le programme enlève certain mot qui se trouve dans le texte du fichier "Lab1_1" et les déplaces dans le fichier "mot_parasites.csv".
nouveau_texte = ' '.join(mot for mot in mots if mot.lower() not in mots_a_supprimer)
print(nouveau_texte)

# Etape 5 :
# Fonction qui prend une chaîne de caractère au format HTML et qui renvoie le même texte sans les balises HTML.
def remove_html_tags(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    text = soup.get_text()
    return text

html_string = "<h1>Bravo </h1><p>Vous venez d'afficher un texte HTML sans ses balises.</p>"
text = remove_html_tags(html_string)
print(text)

# Etape 6 :
# Fonction qui prend dans une chaîne de caractère le nom d'une balise, le nom d'un attribut et retourne la liste des valeurs associées aux balises.
def get_attribute_values(html_string, tag_name, attribute_name):
    soup = BeautifulSoup(html_string, 'html.parser')
    tags = soup.find_all(tag_name)
    values = [tag.get(attribute_name) for tag in tags if tag.get(attribute_name) is not None]
    return values

tag_name = 'div'
attribute_name = 'id'

values = get_attribute_values(html_string, tag_name, attribute_name)
print(values)  # Affiche : ['div1', 'div2', 'div3']

# Etape 8 :
# Fonction qui permet de donner le nom de domaine d'une page par rapport à son url.
def extract_domain(url):
    domain = urlparse(url).netloc
    return domain
url = 'https://www.crunchyroll.com/fr'
domain = extract_domain(url)
print(domain)  # Affiche : 'www.example.com'

# Etape 9 :
# Fonction qui permet de prendre une chaîne de caractère représentant un nom de domaine, et qui permet de comparer 2 urls de page HTML pour savoir si elle appartient au même domaine.
def filter_urls(domain, urls):
    same_domain = []
    different_domain = []

    for url in urls:
        if urlparse(url).netloc == domain:
            same_domain.append(url)
        else:
            different_domain.append(url)

    return same_domain, different_domain

domain = 'www.crunchyroll.com'
urls = ['https://www.crunchyroll.com/fr', 'https://www.twitch.tv/aypierre']
same_domain, different_domain = filter_urls(domain, urls)
print("URLs in the same domain:", same_domain)
print("URLs in different domains:", different_domain)

#Etape 10 :
# Fonction qui permet d'ouvrir une page HTML depuis une url et de récupérer le texte HTML qui la compose.
def get_html(url):
    response = requests.get(url)
    return response.text

url = 'https://www.crunchyroll.com/fr'
html_text = get_html(url)
text = remove_html_tags(html_text)
print(html_text)

#Etape 11 :
def audit_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouve les mots clés avec les 3 premières valeurs d'occurrences
    text = soup.get_text()
    words = re.findall(r'\w+', text.lower())
    most_common_words = Counter(words).most_common(3)

    # Trouve le nombre de liens entrants et sortants qui se trouvent sur la page HTML
    incoming_links = len(soup.find_all('a', href=True))
    outgoing_links = len([link for link in soup.find_all('a', href=True) if link['href'].startswith('http')])

    # Vérifie la présence de la balises 'alt' et cherche le nombre de fois qu'il y a la balise 'Alt' dans le code HTML de la page.
    alt_tags = len(soup.find_all('img', alt=True))

    print(f"Mots clés avec les 3 premières valeurs d'occurrences: {most_common_words}")
    print(f"Nombre de liens entrants: {incoming_links}")
    print(f"Nombre de liens sortants: {outgoing_links}")
    print(f"Présence de balises alt: {alt_tags}")

# Utilisation de la fonction
url = input("Entrez l'URL de la page à analyser: ")
audit_page(url)
