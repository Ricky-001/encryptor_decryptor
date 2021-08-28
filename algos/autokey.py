#!/usr/bin/python3

import argparse
from time import sleep
from utilities.colors import color
from utilities.tools import clear

def encrypt(plain,key):

    plain_bak = plain
    plain=''
    for p in plain_bak:
        if p.isalpha():
            plain+=p

    try:
        key = int(key)-1       # if user enters number corresponding to letter, add 96 to it to convert to ASCII
    except ValueError:
        try:
            key = ord(key.upper())-65  # if user enters letter, use the lowercase ASCII value
        except TypeError:
            print('{}[-] Please enter a letter between a-z or a number between 1-26 (corresponding to alphabets){}'.format(color.RED,color.END))
            quit()
    if key not in range(27):
        print('{}[-] Please enter a letter between a-z or a number between 1-26 (corresponding to alphabets){}'.format(color.RED,color.END))
        quit()

    plainASCII = [ord(char.upper())-65 for char in plain]   # converting to uppercase for ease of use
    keyASCII = [key,]
    # generating the key with the given word, excluding the last character
    keyASCII.extend(plainASCII[:len(plainASCII)-1])
    cipherASCII=[]

    for i in range(len(plainASCII)):
        if plainASCII[i] in range(26):
            cipherASCII.append( (plainASCII[i] + keyASCII[i])%26 )
        else:
            cipherASCII.append(plainASCII[i])
    
    cipher = ''.join(chr(c+65) for c in cipherASCII)
    for i in range(len(plain_bak)): 
        if not plain_bak[i].isalpha():
            cipher = cipher[:i] + plain_bak[i] + cipher[i:]
    return cipher


def decrypt(cipher,key):

    cipher_bak = cipher
    cipher=''
    for c in cipher_bak:
        if c.isalpha():
            cipher+=c

    try:
        key = int(key)-1       # if user enters number corresponding to letter, add 96 to it to convert to ASCII
    except ValueError:
        try:
            key = ord(key.upper())-65  # if user enters letter, use the lowercase ASCII value
        except TypeError:
            print('{}[-] Please enter a letter between a-z or a number between 1-26 (corresponding to alphabets){}'.format(color.RED,color.END))
    if key not in range(27):
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
    for i in range(len(cipher_bak)):
        if not cipher_bak[i].isalpha():
            plain = plain[:i] + cipher_bak[i] + plain[i:]
    return plain


def enc(readFile=False):
    if readFile:
        filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
        plain = parsefile(filename)
    else:
        plain = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END)).strip()
    key = input('{}[?]{} Enter the Key (single Letter or corresponding number) {}[ex: A(1); B(2) ... Z(26)]{} : '.format(color.BLUE,color.END, color.YELLOW,color.END))
    if not key:
        print('{}[-] Please enter a key to encrypt!{}'.format(color.RED,color.END))
        quit()
    ct=encrypt(plain,key)
    print('{}[+]{} The Ciphertext with {}Autokey of {}{} is {}{}{}'.format(color.GREEN,color.END, color.YELLOW,key,color.END, color.RED,ct.strip(),color.END))


def dec(readFile=False):
    if readFile:
        filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
        cipher = parsefile(filename)
    else:
        cipher = input('{}[?]{} Enter the Ciphertext : '.format(color.BLUE,color.END)).strip()
    key = input('{}[?]{} Enter the Key (single Letter or corresponding number) {}[ex: A(1); B(2) ... Z(26)]{}\n{}[!]{} Leave empty to attempt bruteforce : '.format(color.BLUE,color.END, color.YELLOW,color.END, color.YELLOW, color.END))
    pt = ''

    if not key:
        for i in range(26):
            pt=''
            #for word in plain.split(' '):
            #    pt += decrypt(word,i+1) + ' '
            pt = decrypt(cipher,i+1)
            print('{}[+]{} {}Autokey = {} ({}){}\t:\t{}{}{}'.format(color.GREEN,color.END, color.YELLOW,i+1,chr(i+65),color.END, color.RED,pt,color.END))
        print('{}[!]{} The bruteforce attack completed successfully!'.format(color.YELLOW,color.END))
    else:
        #for word in plain.split(' '):
        #    pt += decrypt(word,key) + ' '
        pt = decrypt(cipher,key)
        print('{}[+]{} The Plaintext with {}Autokey of {}{} is {}{}{}'.format(color.GREEN,color.END, color.YELLOW,key,color.END, color.RED,pt.strip(),color.END))



def parsefile(filename):
    message = ''
    try:
        with open(filename) as f:
            for line in f:
                message+=line
    except FileNotFoundError:
        print('{}[-] File not found{}\n{}[!] Please make sure the file with the filename exists in the current working directory{}'.format(color.RED,color.END,color.YELLOW,color.END))
        quit()
    return message



def run():
    try:
        clear()
        # prompt for choice of action
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            # whether to load a file for the plaintext or type it from the console
            filechoice = 'n'
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                enc(False)
            else:
                enc(True)
        elif choice == 'd' or choice == 'D':
            # whether to load a file for the plaintext or type it from the console
            filechoice = 'n'
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                dec(False)
            else:
                dec(True)
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
        quit()
    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))


def main():
    try:
        clear()
        
        # script description
        parser = argparse.ArgumentParser(description='Autokey Encryption & Decryption')
        # encryption group option (single option --encrypt)
        enc_group = parser.add_argument_group('Encryption Options')
        enc_group.add_argument('-e','--encrypt', help='Encrypt a given Plaintext', default=False, action='store_true')
        # decryption group options (--decrypt and --brute)
        dec_group = parser.add_argument_group('Decryption Options')
        dec_group.add_argument('-d','--decrypt', help='Decrypt a given Ciphertext', default=False, action='store_true')
        dec_group.add_argument('-B','--brute', help='Bruteforce decryption (to be used only with -d, --decrypt)', default=False, action='store_true')
        # file option - whether to load from a file
        parser.add_argument('-f','--file', help='Load the Plaintext/ Ciphertext from a file', default=False, action='store_true')
        # message (either plain or cipher)  -   handled later on based on options
        parser.add_argument('TEXT', help='Plaintext or Ciphertext (based on mode)')
        parser.add_argument('-k','--key', help='Key used to encrypt/decrypt')

        try:        # if all options and positional argument (TEXT) provided
            args = parser.parse_args() 
        except:     # if positional argument TEXT not provided - prompts user with necessary options
            # prompt for choice of action
            choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
            if choice == 'e' or choice == 'E':
                # whether to load a file for the plaintext or type it from the console
                filechoice = 'n'
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    enc(False)
                else:
                    enc(True)
            elif choice == 'd' or choice == 'D':
                # whether to load a file for the plaintext or type it from the console
                filechoice = 'n'
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    dec(False)
                else:
                    dec(True)
            else:
                print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
            quit()

        pt='' ; ct=''
        # parsing command line argumets (provided the necvessary ones are given)
        if args.encrypt:                            # if encrypt flag is on
            if args.decrypt:                        # decrypt flag should be off
                print('{}[-] Please select only one option among Encrypt or Decrypt at a time{}'.format(color.RED,color.END))
                quit()
            if args.brute:                          # bruteforce flag should be off
                print('{}[-] Bruteforce can only be used during Decryption{}'.format(color.RED,color.END))
                quit()
            if not args.key:
                print('{}[-] Please provide a key for encryption!{}'.format(color.RED,color.END))
                quit()
            else:                                   # good to go - call enc() function and display result
                if args.file:
                    pt = parsefile(args.TEXT)
                    ct = encrypt(pt,args.KEY)
                else:
                    ct = encrypt(args.TEXT,args.key)
                print('{}[+]{} The Ciphertext with {}Autokey of {}{} is {}{}{}'.format(color.GREEN,color.END, color.YELLOW,args.key,color.END, color.RED,ct.strip(),color.END))

        elif args.decrypt:                          # if decrypt flag is on
            if args.brute:                          # if bruteforce option is also on
                if args.file:
                    for i in range(26):
                        ct = parsefile(args.TEXT)
                        pt=''
                        pt += decrypt(ct,i+1)
                        print('{}[+]{} {}Autokey = {} ({}){}\t:\t{}{}{}'.format(color.GREEN,color.END, color.YELLOW,i+1,chr(i+65),color.END, color.RED,pt,color.END))
                else:
                    for i in range(26):
                        pt=''
                        pt += decrypt(args.TEXT,i+1)
                        print('{}[+]{} {}Autokey = {} ({}){}\t:\t{}{}{}'.format(color.GREEN,color.END, color.YELLOW,i+1,chr(i+65),color.END, color.RED,pt,color.END))
                print('{}[!]{} The bruteforce attack completed successfully!'.format(color.YELLOW,color.END))
            else:                                   # no bruteforce - key known
                if not args.key:
                    print('{}[-] Please provide a key for decryption!{}'.format(color.RED,color.END))
                    quit()
                if args.file:
                    ct = parsefile(args.TEXT)
                    pt = decrypt(ct,args.key)
                else:
                    pt = decrypt(args.TEXT,args.key)
                print('{}[+]{} The Plaintext with {}Autokey of {}{} is {}{}{}'.format(color.GREEN,color.END, color.YELLOW,args.key,color.END, color.RED,pt.strip(),color.END))

        # if no arguments are provided except for positional (TEXT)
        else:
            print('{}[-] At least one of Encryption or Decryption action is required{}'.format(color.RED,color.END))

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
        quit()


if __name__ == '__main__':
    main()

