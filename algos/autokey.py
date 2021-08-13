#!/usr/bin/python3

from time import sleep
from utilities.colors import color
from utilities.tools import clear

def encrypt(plain,key):
    try:
        key = int(key)       # if user enters number corresponding to letter, add 96 to it to convert to ASCII
    except ValueError:
        try:
            key = ord(key.upper())-65  # if user enters letter, use the lowercase ASCII value
        except TypeError:
            print('{}[-] Please enter a letter between a-z or a number between 1-26 (corresponding to alphabets){}'.format(color.RED,color.END))
            quit()
    if key not in range(1,27):
        print('{}[-] Please enter a letter between a-z or a number between 1-26 (corresponding to alphabets){}'.format(color.RED,color.END))
        quit()

    plainASCII = [ord(char.upper())-65 for char in plain]   # converting to uppercase for ease of use
    keyASCII = [key,]
    keyASCII.extend(plainASCII[:len(plainASCII)-1])
    cipherASCII=[]

    for i in range(len(plainASCII)):
        if plainASCII[i] in range(26):
            cipherASCII.append( (plainASCII[i] + keyASCII[i])%26 )
        else:
            cipherASCII.append(plainASCII[i])
    
    cipher = ''.join(chr(c+65) for c in cipherASCII)
    return cipher


def decrypt(cipher,key):
    try:
        key = int(key)       # if user enters number corresponding to letter, add 96 to it to convert to ASCII
    except ValueError:
        try:
            key = ord(key.upper())-65  # if user enters letter, use the lowercase ASCII value
        except TypeError:
            print('{}[-] Please enter a letter between a-z or a number between 1-26 (corresponding to alphabets){}'.format(color.RED,color.END))
    if key not in range(1,27):
        print('{}[-] Please enter a letter between a-z or a number between 1-26 (corresponding to alphabets){}'.format(color.RED,color.END))
        quit()

    cipherASCII = [ord(char.upper())-65 for char in cipher]   # converting to uppercase for ease of use
    keyASCII = [key,]                                         # add the initial key to the keyASCII list
    plainASCII=[]

    for i in range(1,len(cipherASCII)):                       # calculate the rest of the elements in the keyASCII list
        keyASCII.append(cipherASCII[i-1] - keyASCII[i-1])
    
    for i in range(len(cipherASCII)):
        if cipherASCII[i] in range(26):
            plainASCII.append( (cipherASCII[i] - keyASCII[i])%26 )
        else:
            plainASCII.append(cipherASCII[i])
    
    plain = ''.join(chr(p+65) for p in plainASCII)
    return plain


def enc():
    clear()
    plain = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END)).strip()
    key = input('{}[?]{} Enter the Key (single Letter or corresponding number) {}[ex: A(1); B(2) ... Z(26)]{} : '.format(color.BLUE,color.END, color.YELLOW,color.END))
    if not key:
        print('{}[-] Please enter a key to encrypt!{}'.format(color.RED,color.END))
        quit()
    ct = ''

    for word in plain.split(' '):
        ct += encrypt(word,key) + ' '
    print('{}[+]{} The Ciphertext with {}Autokey of {}{} is {}{}{}'.format(color.GREEN,color.END, color.YELLOW,key,color.END, color.RED,ct.strip(),color.END))


def dec():
    clear()
    plain = input('{}[?]{} Enter the Ciphertext : '.format(color.BLUE,color.END)).strip()
    key = input('{}[?]{} Enter the Key (single Letter or corresponding number) {}[ex: A(1); B(2) ... Z(26)]{}\n{}[!]{} Leave empty to attempt bruteforce : '.format(color.BLUE,color.END, color.YELLOW,color.END, color.YELLOW, color.END))
    pt = ''

    if not key:
        for i in range(26):
            pt=''
            for word in plain.split(' '):
                pt += decrypt(word,i+1) + ' '
            print('{}[+]{} {}Autokey = {} ({}){}\t:\t{}{}{}'.format(color.GREEN,color.END, color.YELLOW,i+1,chr(i+65),color.END, color.RED,pt,color.END))
        print('{}[!]{} The bruteforce attack completed successfully!'.format(color.YELLOW,color.END))
    else:
        for word in plain.split(' '):
            pt += decrypt(word,key) + ' '
        print('{}[+]{} The Plaintext with {}Autokey of {}{} is {}{}{}'.format(color.GREEN,color.END, color.YELLOW,key,color.END, color.RED,pt.strip(),color.END))


def run():
    try:
        clear()
        
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            enc()
        elif choice == 'd' or choice == 'D':
            dec()
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
        quit()

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
