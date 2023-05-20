import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

response = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mp_mv250")

# Парсим HTML-код
soap = BeautifulSoup(response.content, "html.parser")

# Находим таблицу с фильмами
table = soap.find("table")

#получаем информацию
names_info = table.find_all("a", title=True) # name and director 
years_info = table.find_all("span", class_="secondaryInfo")
ratings = table.find_all("strong") 

# Создаем список для хранения данных о фильмах
films = []

for names, years, ratings in zip(names_info, years_info, ratings):
    name = names.string
    director = names.get("title").split("(")[0].strip()
    year = years.string[1:-1]
    rating = ratings.string
    n_reviews = ratings.get("title").split(" ")[3].replace(",", "")
    films.append([name, year, director, rating, n_reviews])

df_films = pd.DataFrame(films, columns=["name", "year", "director", "rating", "n_reviews"])
df_films['rank'] = list(range(1,251))
df_films = df_films.iloc[:, [5, 0, 1, 3, 4, 2  ]]
df_films.to_csv ('top250films.csv', index= False )

#топ-4 фильма по количеству оценок пользователей и количество этих оценок
df_films['n_reviews'] = df_films['n_reviews'].astype(int)
df_films.nlargest(4, 'n_reviews')[['name', 'n_reviews']]

#топ-4 лучших года (по среднему рейтингу фильмов в этом году) и средний рейтинг
df_films['rating'] = df_films['rating'].astype(float)
pd.DataFrame(df_films.groupby('year')['rating'].mean().nlargest(4))

#отсортированный barplot, где показано количество фильмов из списка для каждого режисёра (только для режиссёров с более чем 2 фильмами в списке)

top_directors = df_films['director'].value_counts()
top_directors = top_directors[top_directors > 2]

plt.bar(top_directors.index, top_directors.values)
plt.xlabel('Режиссер')
plt.ylabel('Количество фильмов')

plt.xticks(rotation=75)
plt.show()

#Выведите топ-4 самых популярных режиссёра (по общему числу людей оценивших их фильмы) 
pd.DataFrame(df_films.groupby('director')['n_reviews'].sum().nlargest(4))
