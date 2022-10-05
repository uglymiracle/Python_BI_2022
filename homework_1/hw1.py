dna = {'A' : 'T',
       'T' : 'A',
       'G' : 'C',
       'C' : 'G'}
dna_to_rna = {'A' : 'U',
              'T' : 'A',
              'G' : 'C',
              'C' : 'G'}   
rna_to_rna = {'A' : 'U',
              'U' : 'A',
              'G' : 'C',
              'C' : 'G'} 
commands = ['exit', 'reverse', 'transcribe',
            'complement', 'reverse complement']


def check_seq(seq, dictionary):
    
    seq_up = seq.upper()

    for nucl in seq_up:
        if nucl not in dictionary.values():
            return False
    return True


def transcribe_and_complement(seq, dictionary):
    
    new_seq_draft = ''
    new_seq = ''
    register_var = []
    
    for i in seq:
        new_seq_draft += dictionary[i.upper()]
    for k in range(len(seq)):
        if not seq[k].isupper():
            new_seq += new_seq_draft[k].lower()
        else:
            new_seq += new_seq_draft[k]
            
    return new_seq


def reverse(seq):
    
    new_seq = seq[::-1]
    return new_seq


def main():
    command = ''
    
    while command != 'exit':
        
        command = input('Enter command: ')
        
        while command not in commands: #check command for existence
            print('Invalid command. Try again!')
            command = input('Enter command: ')
        
        if command == 'exit': #end of work
            print("Good bye! Good luck!")
            break
            
        seq = input('Enter sequence: ')
        
        if command == 'transcribe':
            while not check_seq(seq, dna): #check sequence is dna
                print('Invalid alphabet. Try again!')
                print("Make sure that it's DNA")
                seq = input('Enter sequence:')
            print(transcribe_and_complement(seq, dna_to_rna)) #transcribing
        
        elif command == 'reverse':
            #check sequence is dna or rna
            while not check_seq(seq, dna) and not check_seq(seq, rna_to_rna): 
                print('Invalid alphabet. Try again!')
                seq = input('Enter sequence:')
            print(reverse(seq))  
            
        elif command == 'complement':
            #check sequence is dna or rna
            while not check_seq(seq, dna) and not check_seq(seq, rna_to_rna): 
                print('Invalid alphabet. Try again!')
                seq = input('Enter sequence:')
            if seq.upper().count('U') == 0:
                print(transcribe_and_complement(seq, dna_to_dna))  #command for dna
            else:
                print(transcribe_and_complement(seq, rna_to_rna)) #command for rna
             
        elif command == 'reverse complement':
            #check sequence is dna or rna
            while not check_seq(seq, dna) and not check_seq(seq, rna_to_rna): 
                print('Invalid alphabet. Try again!')
                seq = input('Enter sequence:')
            if seq.upper().count('U') == 0:
                print(reverse(transcribe_and_complement(seq, dna_to_dna))) #command for dna
            else:
                print(reverse(transcribe_and_complement(seq, rna_to_rna))) #command for rna

                

import datetime
hi_dict = { "hey" : 
        ('Good morning!', 'Good afternoon!',
                  'Good evening!',
                  "Good nignt! It's already very late to work! Good reminder: to finish type the command 'exit'")}

now = datetime.datetime.now()

if now.hour > 6 and now.hour <= 11 :
    hi = hi_dict["hey"][0]
elif now.hour > 12 and now.hour <= 17 :
    hi = hi_dict["hey"][1]
elif now.hour > 17 and now.hour <= 24 :
    hi = hi_dict["hey"][2]
elif now.hour >= 0 and now.hour <= 6 :
    hi = hi_dict["hey"][3]

print(hi)

if __name__ == '__main__':
    main()
