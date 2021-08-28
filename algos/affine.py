#!/usr/bin/python3

import argparse
from utilities.tools import clear
from utilities.colors import color

keys = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
def encrypt(plain,key,step):

    if key not in keys:
        raise ValueError()

    plainASCII = [ord(char) for char in plain]
    cipherASCII = []

    for i in range(len(plain)):
        if plain[i].isalpha():
            if plainASCII[i] in range(65,91):
                cipherASCII.append((((plainASCII[i]-65)*key)+step)%26+65)
            else:
                cipherASCII.append((((plainASCII[i]-97)*key)+step)%26+97)
        else:
            cipherASCII.append(plainASCII[i])

    cipher = ''.join(map(chr,cipherASCII))
    return cipher

def inverse(key):
    return [x for x in range(27) if (x*key)%26==1][0]

def decrypt(cipher,key=None,step=None):
    cipherASCII = [ord(char) for char in cipher]    
    plainASCII = []

    # bruteforce decryption
    
    if not key:
        for key in keys:
            print('\n{}[!] {}Key = {}{}'.format(color.BLUE,color.ORANGE,key,color.END))
            print('===============\n')
            for step in range(26):
                plainASCII = []
                for i in range(len(cipher)):
                    if cipher[i].isalpha():
                        if cipherASCII[i] in range(65,91):
                            plainASCII.append(((cipherASCII[i]-65-step)*inverse(key))%26+65)
                        else:
                            plainASCII.append(((cipherASCII[i]-97-step)*inverse(key))%26+97)
                    else:
                        plainASCII.append(cipherASCII[i])
                plain = ''.join(map(chr,plainASCII))
                print('{}[+]{} {}Step={}{}\t:\t{}{}{}'.format(color.GREEN,color.END,color.YELLOW,step,color.END,color.RED,plain,color.END))
        return None

    # normal decryption
    if key in keys:
        for i in range(len(cipher)):
            if cipher[i].isalpha():
                if cipherASCII[i] in range(65,91):
                    plainASCII.append(((cipherASCII[i]-65-step)*inverse(key))%26+65)
                else:
                    plainASCII.append(((cipherASCII[i]-97-step)*inverse(key))%26+97)
            else:
                plainASCII.append(cipherASCII[i])
    
    else:
        #print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}'.format(color.RED,color.END,color.YELLOW,keys,color.END))
        raise ValueError()

    plain = ''.join(map(chr,plainASCII))
    return plain


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
    key=None
    try:
        clear()
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            # whether to load a file for the plaintext or type it from the console
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                pt = input('{}[?]{} Enter the Plaintext message to encrypt: '.format(color.BLUE,color.END))
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                pt = parsefile(filename)
            try:
                key = int(input('{}[?]{} Enter the Key to encrypt the message: '.format(color.BLUE,color.END)))
                step = int(input('{}[?]{} Enter the shift step of the message: '.format(color.BLUE,color.END)))
                ciphertext = encrypt(pt, key, step)
                print('{}[+] The Ciphertext with Key = {}{}{} and a Shift of {}{}{} is: {}{}{}'.format(color.GREEN,color.YELLOW,key,color.END,color.ORANGE,step,color.END,color.RED,ciphertext,color.END))
            except ValueError:
                print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}\n{}[-] Please ensure to provide a numeric value for steps (0 for no shift){}'.format(color.RED,color.END,color.YELLOW,keys,color.END,color.RED,color.END))
            
        elif choice == 'd' or choice == 'D':
            # whether to load a file for the plaintext or type it from the console
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                ct = input('{}[?]{} Enter the Ciphertext message to decrypt: '.format(color.BLUE,color.END))
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                ct = parsefile(filename)
            try:
                key = int(input('{}[?]{} Enter the Key used to encrypt the message (leave blank to attempt Bruteforce): '.format(color.BLUE,color.END)))
                if key:
                    step = int(input('{}[?]{} Enter the shift step of the message: '.format(color.BLUE,color.END)))
                plaintext = decrypt(ct, key, step)
                print('{}[+] The Plaintext with Key = {}{}{} and a Shift of {}{}{} is : {}{}{}'.format(color.GREEN,color.YELLOW,key,color.END,color.ORANGE,step,color.END,color.RED,plaintext,color.END))
            except ValueError:
                if not key:
                    decrypt(ct,None)
                    print('\n{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
                else:
                    print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}\n{}[-] Please ensure to provide a numeric value for steps (0 for no shift){}'.format(color.RED,color.END,color.YELLOW,keys,color.END,color.RED,color.END))
            
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
        quit()

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))


def main():
    key=None
    try:
        clear()

        # script description
        parser = argparse.ArgumentParser(description='Multiplicative Cipher Encryption & Decryption')
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
        parser.add_argument('-k','--key', default=None, type=int, help='Key used for encryption/ decryption')
        parser.add_argument('-s','--step', default=0, type=int, help='Shift step (default=0)')

        try:
            args = parser.parse_args()
        except:
            choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
            
            if choice == 'e' or choice == 'E':
                # whether to load a file for the plaintext or type it from the console
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    pt = input('{}[?]{} Enter the Plaintext message to encrypt: '.format(color.BLUE,color.END))
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    pt = parsefile(filename)
                try:
                    key = int(input('{}[?]{} Enter the Key to encrypt the message: '.format(color.BLUE,color.END)))
                    step = int(input('{}[?]{} Enter the shift step of the message: '.format(color.BLUE,color.END)))
                    ciphertext = encrypt(pt, key, step)
                    print('{}[+] The Ciphertext with Key = {}{}{} and a Shift of {}{}{} is: {}{}{}'.format(color.GREEN,color.YELLOW,key,color.END,color.ORANGE,step,color.END,color.RED,ciphertext,color.END))
                except ValueError:
                    print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}\n{}[-] Please ensure to provide a numeric value for steps (0 for no shift){}'.format(color.RED,color.END,color.YELLOW,keys,color.END,color.RED,color.END))
            
            elif choice == 'd' or choice == 'D':
                # whether to load a file for the plaintext or type it from the console
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    ct = input('{}[?]{} Enter the Ciphertext message to decrypt: '.format(color.BLUE,color.END))
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    ct = parsefile(filename)
                try:
                    key = int(input('{}[?]{} Enter the Key used to encrypt the message (leave blank to attempt Bruteforce): '.format(color.BLUE,color.END)))
                    if key:
                        step = int(input('{}[?]{} Enter the shift step of the message: '.format(color.BLUE,color.END)))
                    plaintext = decrypt(ct, key, step)
                    print('{}[+] The Plaintext with Key = {}{}{} and a Shift of {}{}{} is : {}{}{}'.format(color.GREEN,color.YELLOW,key,color.END,color.ORANGE,step,color.END,color.RED,plaintext,color.END))
                except ValueError:
                    if not key:
                        decrypt(ct,None)
                        print('\n{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
                    else:
                        print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}\n{}[-] Please ensure to provide a numeric value for steps (0 for no shift){}'.format(color.RED,color.END,color.YELLOW,keys,color.END,color.RED,color.END))
            
            else:
                print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
            quit()

        # parsing command line argumets (provided the necvessary ones are given)
        if args.encrypt:                            # if encrypt flag is on
            if args.decrypt:                        # decrypt flag should be off
                print('{}[-] Please select only one option among Encrypt or Decrypt at a time{}'.format(color.RED,color.END))
                quit()
            if args.brute:                          # bruteforce flag should be off
                print('{}[-] Bruteforce can only be used during Decryption{}'.format(color.RED,color.END))
                quit()
            else:                                   # good to go - call enc() function and display result
                if args.file:
                    pt = parsefile(args.TEXT)
                else:
                    pt = args.TEXT
                try:
                    key = int(args.key)
                    if args.step:
                        step = int(args.step)
                    else:
                        step=0
                    ciphertext = encrypt(pt, key, step)
                    print('{}[+] The Ciphertext with Key = {}{}{} and a Shift of {}{}{} is: {}{}{}'.format(color.GREEN,color.YELLOW,key,color.END,color.ORANGE,step,color.END,color.RED,ciphertext,color.END))
                except ValueError:
                    print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}\n{}[-] Please ensure to provide a numeric value for steps (0 for no shift){}'.format(color.RED,color.END,color.YELLOW,keys,color.END,color.RED,color.END))

        elif args.decrypt:                          # if decrypt flag is on
            if args.brute:                          # if bruteforce option is also on
                if args.file:
                    ct = parsefile(args.TEXT)
                    decrypt(ct,None)
                else:
                    decrypt(args.TEXT,None)             # call decrypt function directly - steps not required
                print('\n{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
            else:                                   # no bruteforce - steps known
                if args.file:
                    ct = parsefile(args.TEXT)
                else:
                    ct = args.TEXT
                try:
                    key = int(args.key)
                    if args.step:
                        step = args.step
                    else:
                        step=0
                    plaintext = decrypt(ct, key, step)
                    print('{}[+] The Plaintext with Key = {}{}{} and a Shift of {}{}{} is : {}{}{}'.format(color.GREEN,color.YELLOW,key,color.END,color.ORANGE,step,color.END,color.RED,plaintext,color.END))
                except ValueError:
                    if not key:
                        decrypt(pt,None)
                        print('\n{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
                    else:
                        print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}\n{}[-] Please ensure to provide a numeric value for steps (0 for no shift){}'.format(color.RED,color.END,color.YELLOW,keys,color.END,color.RED,color.END))
                except TypeError:
                    try:
                        key = int(input('{}[?]{} Enter the Key used to encrypt the message (leave blank to attempt Bruteforce): '.format(color.BLUE,color.END)))
                        if key:
                            step = int(input('{}[?]{} Enter the shift step of the message: '.format(color.BLUE,color.END)))
                        else:
                            step=None
                        plaintext = decrypt(ct, key, step)
                        print('{}[+] The Plaintext with Key = {}{}{} and a Shift of {}{}{} is : {}{}{}'.format(color.GREEN,color.YELLOW,key,color.END,color.ORANGE,step,color.END,color.RED,plaintext,color.END))
                    except ValueError:
                        if not key:
                            decrypt(ct,None)
                            print('\n{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
                        else:
                            print('{}[-] Please enter a valid key{} (one of the following):-\n{}{}{}\n{}[-] Please ensure to provide a numeric value for steps (0 for no shift){}'.format(color.RED,color.END,color.YELLOW,keys,color.END,color.RED,color.END))


        # if no arguments are provided except for positional (TEXT)
        else:
            print('{}[-] At least one of Encryption or Decryption action is required{}'.format(color.RED,color.END))

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
        quit()

if __name__ =='__main__':
    main()

