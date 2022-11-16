import re
import seaborn as sns


#чтение файла
with open("references.txt", "r") as f:
    
    text1 = '\n'.join(f.readlines())

#поиск совпадений
res = re.findall(r"ftp\.[^;\s]+", text1)

#запись в файл
with open('ftps', 'a') as f:
    for i in res:
        if i != None:
            print(i, file=f)


#чтение файла
with open("2430AD.txt", "r") as f:
    
    text2 = '\n'.join(f.readlines())

#поиск чисел
numbers = re.findall(r"[0-9]+", text2)
print(*numbers, sep=', ')


#поиск слов с буквой а
words_a = re.findall(r"\w*a\w*", text2, re.IGNORECASE)
print(*words_a, sep=', ')


#поиск восклицательных предложений
sentences = re.findall(r"\w[^\.!?\"]*[!]", text2, re.IGNORECASE)
print(*sentences, sep='\n')


#поиск уникальных слов
unique_words = re.findall(r"(\b\w+\b)(?![\s\S]*\b\1\b)", text2, re.IGNORECASE)

#создание вектора с длинами слов
l =[len(i) for i in unique_words]

#построение графика
sns.histplot(l).set(xlabel='Длина слова', ylabel='Количество слов');


def translate_to_k(text):
    
    w = re.sub(r"([аоуыэяёюиеАОУЫЭЯЁЮИЕ])", r"\1к\1", str(text))
    
    return w

translate_to_k('Институт биоинформатики')
