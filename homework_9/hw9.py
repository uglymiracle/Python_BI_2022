#  Задание1

import datetime

class Chat:
    
    def __init__(self, chat_history=[]):
        self.chat_history = chat_history
    
    def show_last_message(self):
        return self.chat_history[0]
    
    def show_chat(self):
        for sms in self.chat_history[::-1]:
            print(sms, end='\n')
    
    def recieve(self, sms):
        self.chat_history.insert(0, sms)


class Message:
    
    def __init__(self, text, user):
        
        self.text = text
        self.datetime = None
        self.user = user
        
    def show(self):
        return f"{self.datetime} - {self.user.username()}: {self.text}"
    
    def send(self, chat):
        self.datetime = datetime.datetime.now()
        chat.recieve(self)


class User:
    
    def __init__(self, name, surname, age):
        
        self.name = name
        self.surname = surname
        self.age = age
        
    def username(self):
        return self.name + self.surname


telegram = Chat()
Kate = User('Kate', 'Petrenko', 22)
Valeri = User('Valeri', 'Berngardt', 21)
sms = Message('я очень устала делать дз', Kate)

sms.send(telegram)
Message('если бы ты села делать раньше, тебе было бы легче', Valeri).send(telegram)
Message('мы не можем быть больше друзьями,  прощай!', Kate).send(telegram)
telegram.show_chat()

telegram.show_last_message()

#Задание 2

class Args:
    
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs 
        
    def __rlshift__(self, other):
        return other(*self._args, **self._kwargs)

sum << Args([1, 2])
(lambda a, b, c: a**2 + b + c) << Args(1, 2, c=50)

# Задание 3

class StrangeFloat(float):
    
    def __getattr__(self, fun):
        
        action, number = fun.split('_')
        
        if action == 'add':
            return StrangeFloat(self + float(number))
        elif action == 'subtract':
            return StrangeFloat(self - float(number))
        elif action == 'multiply':
            return StrangeFloat(self * float(number))
        elif action == 'divide':
            return StrangeFloat(self / float(number))
        else:
            raise AttributeError

# Задание 4
import numpy as np

matrix = []
for idx in range(0, 100, 10):
    matrix.__iadd__([list(range(idx, idx.__add__(10)))])
    
selected_columns_indices = list(filter(lambda x: x in range(1, 5, 2), range(matrix.__len__())))
selected_columns = map(lambda x: [x[col] for col in selected_columns_indices], matrix)

arr = np.array(list(selected_columns))

mask = arr.__getitem__((slice.__call__(None), 1)).__mod__(3).__eq__(0)
new_arr = arr.__getitem__(mask)

product = new_arr.__matmul__(new_arr.T)

if (product[0].__lt__(1000)).all() and (product[2].__gt__(1000)).any():
    print(product.mean())

# Задание 5

from abc import ABC, abstractmethod

class BiologicalSequence(ABC):
    
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def check_seq(self):
         pass
        
        
class NucleicAcidSequence(BiologicalSequence):
    
    nucleotides_compl = {'a' : 't',
                         't' : 'a',
                         'g' : 'c',
                         'c' : 'g',
                         'u' : 'a'}
    nucls = 'agcut'
    
    def __init__(self, seq):
        self.seq = seq.lower()
    
    def __len__(self):
        return len(self.seq)

    def __getitem__(self, index):
        return self.seq[index]

    def __str__(self):
        return str(self.seq)

    def check_seq(self):
         
        if set(self.seq) <= set(self.nucls):
            return True
        
        else:
            return False
        
    def complement(self):
        
        if type(self) == NucleicAcidSequence:
            raise NotImplementedError
            
        elif self.check_seq():
            return ''.join([self.nucleotides_compl[nucl] for nucl in self.seq])
        
        else:
            raise KeyError('Check your sequence')
    
    def gc_content(self):
        return (self.seq.count('g') + self.seq.count('c')) / len(self.seq) * 100
        

class DNASequence(NucleicAcidSequence):
    
    nucleotides_compl = {'a' : 't',
                  't' : 'a',
                  'g' : 'c',
                  'c' : 'g'}
    
    nucls = 'agct'
    
    def transcribe(self):
        
        nucleotides_transcr = {'a' : 'u',
                             't' : 'a',
                             'g' : 'c',
                             'c' : 'g'}
        
        if self.check_seq():
            return ''.join([nucleotides_transcr[nucl] for nucl in self.seq])
        
        else:
            raise KeyError('Check your sequence')
    
                          
class RNASequence(NucleicAcidSequence):
    
    nucleotides_compl = {'a' : 'u',
                  'u' : 'a',
                  'g' : 'c',
                  'c' : 'g'}
                          
    nucls = 'agcu'
    
class AminoAcidSequence(BiologicalSequence):
    
    aminoacid = 'ARNDCEQGHILKMFPSTWYV'
    def __init__(self, seq):
        self.seq = seq
        
    def __len__(self):
        return len(self.seq)

    def __getitem__(self, index):
        return self.seq[index]

    def __str__(self):
        return str(self.seq)

    def check_seq(self):
         
        if set(self.seq) <= set(self.aminoacid):
            return True
        
        else:
            return False
    
    def protein_weight(self):
        
        weights = {'A': 89, 'R': 174, 'N': 132, 'D': 133, 'C': 121,
                   'E': 147, 'Q': 146, 'G': 75, 'H': 155, 'I': 131,
                   'L': 131, 'K': 146, 'M': 149, 'F': 165, 'P': 115,
                   'S': 105, 'T': 119, 'W': 204, 'Y': 181, 'V': 117}
        
        if self.check_seq():
            return sum([weights[a] for a in self.seq])
        
        else:
            raise KeyError('Check your sequence')   


