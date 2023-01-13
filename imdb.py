# Importando os pacotes necessários
from requests import get
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np, pandas as pd
import seaborn as sns

# Define o intervalo de páginas a serem coletadas
pages = np.arange(1, 5, 50)

# Define os headers para a requisição
headers = {'Accept-Language': 'pt-BR,pt;q=0.8'}

# Inicializa as listas vazias para armazenar os dados
titles = []
years = []
genres = []
runtimes = []
imdb_ratings = []
imdb_ratings_standardized = []
votes = []
ratings = []

# Loop para percorrer as páginas
for page in pages:
   # Faz a requisição para a página atual
   response = get("https://www.imdb.com/search/title?genres=sci-fi&" + "start=" + str(page) + "&explore=title_type,genres&ref_=adv_prv", headers=headers)
   
   # Adiciona um delay aleatório para evitar ser bloqueado pelo site
   sleep(randint(8,15))
   
   # Verifica se a resposta da requisição foi de sucesso
   if response.status_code != 200:
       # Em caso de erro, exibe uma mensagem de aviso
       warn('Muito erradinho: {}; Status code: {}'.format(requests, response.status_code))
   
   # Transforma o conteúdo HTML da página em um objeto BeautifulSoup
   page_html = BeautifulSoup(response.text, 'html.parser')
      
   # Encontra todos os elementos HTML com a classe 'lister-item mode-advanced'
   movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
   
   # Loop para percorrer cada elemento encontrado
   for container in movie_containers:
        # Verifica se o elemento possui a classe 'ratings-metascore'
        if container.find('div', class_ = 'ratings-metascore') is not None:
           # Armazena o título do filme
           title = container.h3.a.text
           titles.append(title)
           
           # Verifica se o elemento possui a classe 'lister-item-year text-muted unbold'
           if container.h3.find('span', class_= 'lister-item-year text-muted unbold') is not None:
             # Armazena o ano do filme
             year = container.h3.find('span', class_= 'lister-item-year text-muted unbold').text
             years.append(year)    

           else:
             years.append(None) 
           if container.p.find('span', class_ = 'certificate') is not None:
             rating = container.p.find('span', class_ = 'certificate').text
             ratings.append(rating)

           else:
             ratings.append("")

           if container.p.find('span', class_ = 'genre') is not None:
             genre = container.p.find('span', class_ = 'genre').text.replace("\n", "").rstrip().split(',')
             genres.append(genre)
          
           else:
             genres.append("")

           if container.p.find('span', class_ = 'runtime') is not None:
             time = int(container.p.find('span', class_ = 'runtime').text.replace(" min", "")) 
             runtimes.append(time)

           else:
             runtimes.append(None)

           if container.strong.text is not None:
             imdb = float(container.strong.text.replace(",", "."))
             imdb_ratings.append(imdb)

           else:
             imdb_ratings.append(None)
              
              
           #Este comando está verificando se existe um elemento 'span' com o atributo 'name' igual a 'nv' dentro do elemento 'container'. 
           #Se ele existir, ele extrai o valor do atributo 'data-value' desse elemento 'span' e o converte para inteiro. 
           #Em seguida, adiciona esse valor convertido à lista 'votes'. Se esse elemento 'span' não for encontrado, o código não fará nada.
           if container.find('span', attrs = {'name':'nv'})['data-value'] is not None:
             vote = int(container.find('span', attrs = {'name':'nv'})['data-value'])
             votes.append(vote)

           else:
               votes.append(None)
              
# Criação do DataFrame com as informações coletadas
sci_fi_df = pd.DataFrame({'filme': titles,
                      'ano': years,
                      'genero': genres,
                      'tempo': runtimes,
                      'imdb': imdb_ratings,
                      'votos': votes}
                      )

# Formata o ano para remover o texto "Movie" 
sci_fi_df.loc[:, 'ano'] = sci_fi_df['ano'].str[-5:-1]

# Adiciona uma nova coluna "nota_imdb" que é igual a nota imdb multiplicada por 10
sci_fi_df['nota_imdb'] = sci_fi_df['imdb'] * 10

# Remove linhas com ano = "Movie"
final_df = sci_fi_df.loc[sci_fi_df['ano'] != 'Movie']

# Formata a coluna "ano" para numerica
final_df.loc[:, 'ano'] = pd.to_numeric(final_df['ano'])
              
              
              
