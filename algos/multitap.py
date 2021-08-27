#!/usr/bin/python3

import argparse
from utilities.colors import color
from utilities.tools import clear
from algos.sms import charsets


def encrypt(pt):
    pt=pt.lower()
    ct = ''

    for char in pt:
        if char in charsets.alpha:
            ct+=charsets.alpha[char]+' '
        else:
            ct+=char+' '

    #print('[+] Multitap code is : {}'.format(ct.strip()))
    return ct.strip()

def decrypt(ct):
    
    pt = ''
    lines = ct.split('\n')
    ct=''
    for line in lines:
        ct+=line + ' / '
    
    ct_bak = ct
    ct = ''.join(c if c.isdigit() or c.isspace() else ' '+c[-1] for c in ct_bak)
    #print(ct)
    for char in ct.split(' '):
        if char in charsets.alpha.values():
            pt+=[key for key,val in charsets.alpha.items() if val==char][0].upper()
            flag=0
        else:
            if not flag:
                pt+=char+' '
                flag=1
            else:
                pt+=char



    #print('[+] Plaintext is : {}'.format(pt.strip()))
    return pt.strip()


def parsefile(filename):
    message = ''
    with open(filename) as f:
        for line in f:
            message+=line
    return message



def run():
    try:
        clear()
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            # whether to load a file for the plaintext or type it from the console
            filechoice = 'n'
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                pt = input('{}[?]{} Enter the Plaintext message to encrypt: '.format(color.BLUE,color.END))
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                pt = parsefile(filename)
            ciphertext = encrypt(pt)
            print('{}[+]{} The Ciphertext is: {}{}{}'.format(color.GREEN,color.END,color.RED,ciphertext,color.END))
        elif choice == 'd' or choice == 'D':
            # whether to load a file for the plaintext or type it from the console
            filechoice = 'n'
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                ct = input('{}[?]{} Enter the Ciphertext message to decrypt: '.format(color.BLUE,color.END))
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                ct = parsefile(filename)
            plaintext = decrypt(ct)
            print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
        quit()
    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))


def main():

    try:
        clear()

        # script description
        parser = argparse.ArgumentParser(description='Multitap (Keypad) Code Encryption & Decryption')
        # encryption group option (single option --encrypt)
        enc_group = parser.add_argument_group('Encryption Options')
        enc_group.add_argument('-e','--encrypt', help='Encrypt a given Plaintext', default=False, action='store_true')
        # decryption group options (--decrypt and --brute)
        dec_group = parser.add_argument_group('Decryption Options')
        dec_group.add_argument('-d','--decrypt', help='Decrypt a given Ciphertext', default=False, action='store_true')    
        # file option - whether to load from a file
        parser.add_argument('-f','--file', help='Load the Plaintext/ Ciphertext from a file', default=False, action='store_true')
        # message (either plain or cipher)  -   handled later on based on options
        parser.add_argument('TEXT', help='Plaintext or Ciphertext (based on mode)')

        try:
            args = parser.parse_args()
        except:
            choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
            if choice == 'e' or choice == 'E':
                # whether to load a file for the plaintext or type it from the console
                filechoice = 'n'
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    pt = input('{}[?]{} Enter the Plaintext message to encrypt: '.format(color.BLUE,color.END))
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    pt = parsefile(filename)
                ciphertext = encrypt(pt)
                print('{}[+]{} The Ciphertext is: {}{}{}'.format(color.GREEN,color.END,color.RED,ciphertext,color.END))
            elif choice == 'd' or choice == 'D':
                # whether to load a file for the plaintext or type it from the console
                filechoice = 'n'
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    ct = input('{}[?]{} Enter the Ciphertext message to decrypt: '.format(color.BLUE,color.END))
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    ct = parsefile(filename)
                plaintext = decrypt(ct)
                print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
            else:
                print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
            quit()

        if args.encrypt:                            # if encrypt flag is on
            if args.decrypt:                        # decrypt flag should be off
                print('{}[-] Please select only one option among Encrypt or Decrypt at a time{}'.format(color.RED,color.END))
                quit()        
            else:
                if args.file:
                    pt = parsefile(args.TEXT)
                    ciphertext = encrypt(pt)
                else:
                    ciphertext = encrypt(args.TEXT)
                print('{}[+]{} The Ciphertext is: {}{}{}'.format(color.GREEN,color.END,color.RED,ciphertext,color.END))

        elif args.decrypt:                          # if decrypt flag is on
            if args.file:
                ct = parsefile(args.TEXT)
                plaintext = decrypt(ct)
            else:
                plaintext = decrypt(args.TEXT)
            print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))

        # if no arguments are provided except for positional (TEXT)
        else:
            print('{}[-] At least one of Encryption or Decryption action is required{}'.format(color.RED,color.END))
    
    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
        quit()

if __name__ == '__main__':
    main()

