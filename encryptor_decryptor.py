#!/usr/bin/python3

from utilities import banner
from utilities.tools import clear
from utilities.colors import color

def call_EncryptorDecryptor(choice):
    if choice==1:
        from algos import rotational_cipher
        rotational_cipher.run()
    elif choice==2:
        from algos import incremental_rotational_cipher
        incremental_rotational_cipher.run()
    elif choice==3:
        from algos import multiplicative_cipher
        multiplicative_cipher.run()
    elif choice==4:
        from algos import vigenere_cipher
        vigenere_cipher.run()
    elif choice==5:
        from algos import morse_code
        morse_code.run()
    elif choice==6:
        from algos import autokey
        autokey.run()
    elif choice==7:
        from algos import multitap
        multitap.run()
    elif choice==8:
        from algos import rot47
        rot47.run()
    else:
        print('{}[!] Please enter a number between {}1 and {}{}'.format(color.RED,color.ORANGE,len(cipher_types),color.END))

def run():
    try:
        clear()
        banner.show()

        cipher_types = ['Rotational (Caesar) Cipher','Incremental Rotation Cipher','Multiplicative Cipher','Vigenere Cipher','Morse Code (with Audio)','Autokey Cipher','Multitap (SMS Keypad) Code','Rot47',]

        for i in range(len(cipher_types)):
            print('{}({}) {}{}'.format(color.YELLOW, i+1, cipher_types[i], color.END),end='\t')
            if i%2:
                print('')
        print('\n\t\t\t{}(0) EXIT{}'.format(color.YELLOW, color.END),end='\t')
        try:
            type_choice = int(input('\n{}[*] {}Choose the type of Cipher to work with >>>{} '.format(color.BLUE,color.CYAN,color.END)))
            if type_choice not in range(1,len(cipher_types)+1):
                if not type_choice:
                    raise KeyboardInterrupt()
                raise ValueError()
            call_EncryptorDecryptor(type_choice)
        except ValueError:
            print('{}[!] Please enter a number between {}1 and {}{}'.format(color.RED,color.ORANGE,len(cipher_types),color.END))

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))

run()