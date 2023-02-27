def gc_consist(seq):
    
    gc_count = seq.count('G') + seq.count('C') 
    gc_percentage = gc_count/ (len(seq)-1) * 100
    #minus 1 because of '\n'
    
    return gc_percentage


def score(string):
    
    score_all = []
    summ = 0
    
    for symbol in string: #count the quality for each symbol in the string
        
        score_symbol = ord(symbol) - 33
        score_all.append(score_symbol)
    
    mean = sum(score_all) / (len(score_all)-1) #count mean
    #minus 1 because of '\n'
    
    return mean


def filter_gc(file, gc_bounds):
    
    filter_list_gc = []
    nofilter_list = []
    
    with open(file, 'r') as f:
    
        while True:
            
            #getting information about one sequence
            one_seq = []

            for i in range(4):
                one_seq.append(f.readline())

            #check the end of file
            if len(one_seq[1]) == 0:

                break
            
            #filterring by gc
            elif (gc_consist(one_seq[1]) <= gc_bounds[1] and
                  gc_consist(one_seq[1]) >= gc_bounds[0]):

                filter_list_gc.append(one_seq)
            
            else:
                
                nofilter_list.append(one_seq)
                    
    return filter_list_gc, nofilter_list


def filter_score(filter_list_gc, 
                 no_filter_list,
                 quality_threshold):
    
    filter_list_score = []
    
    #getting information about one sequence
    for seq in filter_list_gc:
        
        #filtering by score
        if score(seq[1]) >= quality_threshold:
            filter_list_score.append(seq)
        
        else:
            no_filter_list.append(seq)
   
    return filter_list_score, no_filter_list


def filter_length(filter_list_score, 
                  nofilter_list,
                  length_bounds):
    
    filter_list_length = []
    
    #getting information about one sequence
    for seq in filter_list_score:
        
        #filtering by score
        if (len(seq[1]) <= length_bounds[1]+1 and   #plus 1 because of '\n'
            len(seq[1]) >= length_bounds[0]):
            
            filter_list_length.append(seq)
            
        else:
            
            nofilter_list.append(seq)
    
    return filter_list_length, nofilter_list


def create_name(output_file_prefix):
    
    name_passed = output_file_prefix + "_passed.fastq"
    name_failed = output_file_prefix + "_failed.fastq"
    
    return name_passed, name_failed


def int_to_tuple(variable):
    
    #check if it's a tuple
    if isinstance(variable, int):
        new_variable = (0, variable)
        return new_variable
    
    else:
        return variable
    

def save_to_file(name_file,
                 filter_list):
    
    with open(name_file, 'w') as file:
        
        for seq in filter_list:
            print(*seq, file=file, end='', sep='')
            

def main(input_fastq, 
         output_file_prefix, 
         gc_bounds=(0, 100), 
         length_bounds=(0, 2**32),
         quality_threshold=0,
         save_filtered=False):
    
    #variable formatting
    gc_bounds = int_to_tuple(gc_bounds)
    length_bounds = int_to_tuple(length_bounds)
    
    #create name for final files
    name_passed, name_failed = create_name(output_file_prefix)
    
    #filtering step by step
    #filtering by gc
    after_gc_filter, after_gc_nofilter = filter_gc(input_fastq, gc_bounds)
    
    #filtering by score
    after_score_filter, after_score_nofilter = filter_score(
        after_gc_filter, after_gc_nofilter, quality_threshold)
    
    #filtering by length
    after_length_filter, after_length_nofilter  = filter_length(
        after_score_filter, after_score_nofilter, length_bounds)
    
    #save passed file
    save_to_file(name_passed, after_length_filter)
    
    #save failed file
    if save_filtered:
        save_to_file(name_failed, after_length_nofilter)
