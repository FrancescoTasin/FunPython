import string
import numpy as np
from unidecode import unidecode as unid

abc='abcdefghijklmnopqrstuvwxyz'

fin=open('frequenze.txt')
freq=[]
for line in fin:
    d=line.strip().split()
    freq.append(float(d[1]))
freq=np.array(freq)

def clean_text(filepath):
    #cleans text (this is adapted for italian txt files)
    fin=open(filepath, 'r', encoding='utf-8')
    text=fin.read().strip()
    if '’' not in string.punctuation:
        punctuation=string.punctuation+'’'
    else:
        punctuation=string.punctuation

    for i in punctuation:
        text=text.replace(i, ' ')
        
    text=unid(text)
    t=text.lower().split()
    return ''.join(t)

def letter_freq(text):
    #returns letter frequencies in target text (as list of frequencies)
    f=dict()
    for letter in abc:
        f[letter]=0
    for letter in text:
        f[letter]=f.get(letter)+1
    total=len(text)
    return [f[letter]/total for letter in abc]

def find_likely_shift(freq_dict):
    #finds most likely shift given the current letter frequency (assuming a constant +n shift) returning n (0 to 25)
    MSEs=np.zeros((26, 1))
    for i in range(26):
        new_freq=np.array(freq_dict[i:]+freq_dict[:i])
        diff=freq-new_freq
        MSEs[i]=sum([x**2 for x in diff])
    min_err=MSEs.min()
    return np.where(MSEs==min_err)[0]

def rotate(text, shift):
    new_text=['']*len(text)
    for i in range(len(text)):
        new_text[i]=chr(ord('a')+(((ord(text[i])-97)+shift)%26))
    return ''.join(new_text)

filename='C:\\Users\\mediaworld\\Documents\\OXFORD\\programming\\python\\FunPython\\VingenereDecoder_ITA\\VingenereDecoder_ITA\\Dante_cifrato.txt'
cleaned_text=clean_text(filename)
frequencies=letter_freq(cleaned_text)
shift=int(find_likely_shift(frequencies))
print(shift)
print(rotate(cleaned_text, -shift))


def find_repeat(text, leng, n):
    #returns greatest common divisor of distances of successive instances of the same letter sequence (it starts from sequences of length
    #'leng', which is reduced by 1 until either (a) at least n different distances are found or (b) leng goes below 3)
    if leng<=2:
        return 'impossible to find solution'
    sequences_observed=dict()
    distances=[]
    for i in range (len(text)-leng):
        sequences_observed[text[i:i+leng]]=sequences_observed.get(text[i:i+leng], [0, i])
        if sequences_observed[text[i:i+leng]][0]!=0:
            distances.append(i-sequences_observed[text[i:i+leng]][1])
            sequences_observed[text[i:i+leng]][1]=i
        sequences_observed[text[i:i+leng]][0]=sequences_observed[text[i:i+leng]][0]+1
    if len(np.unique(np.array(distances)))>=n:
        sol=np.gcd.reduce(distances)
    else:
        sol=find_repeat(text, leng-1, n)
    return sol



def decode_vingenere(text, str_len, n):
    #finds decoded text and key, based on text, starting string length for pattern search (at least 3), and number of different distances to find before giving solution
    key=[]
    key_len=find_repeat(text, str_len, n)
    
    shifts=dict()
    letter_groups=dict()
    for i in range(len(text)):
        letter_groups[i%key_len]=letter_groups.get(i%key_len, [])
        letter_groups[i%key_len].append(text[i])
    
    for group in letter_groups:
        frequencies=letter_freq(letter_groups[group])
        shift=int(find_likely_shift(frequencies))
        shifts[group]=shift
        print(shift)
        key.append(rotate('a', shift))
    
    solution=[]
    for i in range(len(text)):
        solution.append(rotate(text[i], -shifts[i%key_len]))

    return ''.join(key), ''.join(solution)


cleaned_text=clean_text('Dante_vingenere.txt')
decode_vingenere(cleaned_text, 7, 3)