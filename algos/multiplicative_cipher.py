#!/usr/bin/python3

from utilities.tools import clear
from utilities.colors import color

keys = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
def encrypt(plain,key):

    if key not in keys:
        raise ValueError()

    plainASCII = [ord(char) for char in plain]
    cipherASCII = []

    for i in range(len(plain)):
        if plain[i].isalpha():
            if plainASCII[i] in range(65,91):
                cipherASCII.append(((plainASCII[i]-65)*key)%26+65)
            else:
                cipherASCII.append(((plainASCII[i]-97)*key)%26+97)
        else:
            cipherASCII.append(plainASCII[i])

    cipher = ''.join(map(chr,cipherASCII))
    return cipher

def inverse(key):
    return [x for x in range(27) if (x*key)%26==1][0]

def decrypt(cipher,key=None):    
    cipherASCII = [ord(char) for char in cipher]    
    plainASCII = []

    # bruteforce decryption
    
    if not key:
        for key in keys:
            plainASCII = []
            for i in range(len(cipher)):
                if cipher[i].isalpha():
                    if cipherASCII[i] in range(65,91):
                        plainASCII.append(((cipherASCII[i]-65)*inverse(key))%26+65)
                    else:
                        plainASCII.append(((cipherASCII[i]-97)*inverse(key))%26+97)
                else:
                    plainASCII.append(cipherASCII[i])
            plain = ''.join(map(chr,plainASCII))
            print('{}[+]{} {}Key={}{}\t:\t{}{}{}'.format(color.GREEN,color.END,color.YELLOW,key,color.END,color.RED,plain,color.END))
        return None

    # normal decryption
    if key in keys:
        for i in range(len(cipher)):
            if cipher[i].isalpha():
                if cipherASCII[i] in range(65,91):
                    plainASCII.append(((cipherASCII[i]-65)*inverse(key))%26+65)
                else:
                    plainASCII.append(((cipherASCII[i]-97)*inverse(key))%26+97)
            else:
                plainASCII.append(cipherASCII[i])
    
    else:
        #print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}'.format(color.RED,color.END,color.YELLOW,keys,color.END))
        raise ValueError()

    plain = ''.join(map(chr,plainASCII))
    return plain


def run():
    key=None
    try:
        clear()
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))

        if choice == 'e' or choice == 'E':
            pt = input('{}[?]{} Enter the Plaintext message to encrypt: '.format(color.BLUE,color.END))
            try:
                key = int(input('{}[?]{} Enter the Key to encrypt the message: '.format(color.BLUE,color.END)))
                ciphertext = encrypt(pt, key)
                print('{}[+] The Ciphertext with Key = {}{}{} is: {}{}{}'.format(color.GREEN,color.YELLOW,key,color.GREEN,color.RED,ciphertext,color.END))
            except ValueError:
                print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}'.format(color.RED,color.END,color.YELLOW,keys,color.END))                

        elif choice == 'd' or choice == 'D':
            ct = input('{}[?]{} Enter the Ciphertext message to decrypt: '.format(color.BLUE,color.END))
            try:
                key = int(input('{}[?]{} Enter the Key used to encrypt the message (leave blank to attempt Bruteforce): '.format(color.BLUE,color.END)))
                plaintext = decrypt(ct, key)
                print('{}[+] The Plaintext with Key = {}{}{} is : {}{}{}'.format(color.GREEN,color.YELLOW,key,color.GREEN,color.RED,plaintext,color.END))
            except ValueError:
                if not key:
                    decrypt(ct,None)
                    print('\n{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
                else:
                    print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}'.format(color.RED,color.END,color.YELLOW,keys,color.END))
            
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
        quit()

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))

