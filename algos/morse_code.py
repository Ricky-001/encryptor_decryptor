#!/usr/bin/python3

from time import sleep
from utilities.colors import color
from utilities.tools import clear
from algos.morse import charsets

def encrypt(pt):
    pt=pt.lower()
    ct = ''

    for char in pt:
        if char in charsets.alpha:
            ct+=charsets.alpha[char]+' '
        elif char in charsets.num:
            ct+=charsets.num[char]+' '
        elif char in charsets.punct:
            ct+=charsets.punct[char]+' '
        else:
            ct+=char+' '

    #print('[+] Morse code is : {}'.format(ct.strip()))
    return ct.strip()


def decrypt(ct):
    ct=ct.lower()
    pt = ''

    for char in ct.split(' '):
        if char in charsets.alpha.values():
            pt+=[key for key,val in charsets.alpha.items() if val==char][0].upper()
        elif char in charsets.num.values():
            pt+=[key for key,val in charsets.num.items() if val==char][0].upper()
        elif char in charsets.punct.values():
            pt+=[key for key,val in charsets.punct.items() if val==char][0].upper()
        else:
            pt+=char

    #print('[+] Plaintext is : {}'.format(pt.strip()))
    return pt.strip()


# plays the Morse code audio 
# fetches the audio files from a folder (required!)
def playSound(code):
    import pygame.mixer, pygame.time
    
    DELAY = 0.2  # Time between sounds
    mixer = pygame.mixer
    mixer.init()

    for char in code:                               # for each character in original message
        flag=0
        PATH = "utilities/morse_code_audio/"        # play the respective morse code audio (files named as "CHARACTER_morse_code.ogg")
        if char == ' ':                             # if character is space
            sleep(7 * DELAY)                        # add delay of 7 units (standard Morse practice)
        else:
        # check if the character is one of the following
        # these audio files are named outside the convention due to file naming restrictions
            if char == ':':
                PATH += 'colon_morse_code.ogg'
            elif char == '/':
                PATH += 'slash_morse_code.ogg'
            elif char == '?':
                PATH += 'question_morse_code.ogg'
            elif char == '"':
                PATH += 'quotation_morse_code.ogg'

        # otherwise, if character is not among the above
            else:
                PATH += char + '_morse_code.ogg'    # follow naming convention and modify path
            
            sound = mixer.Sound(PATH)               # load the sound from path
            beep = sound.play()                     # play the sound and capture the channel as beep
            while beep.get_busy():      # if audio playing (check channel status)
                if not flag:
                    print('{}\t{}\t{}{}'.format(color.BLUE, char.upper(), encrypt(char), color.END))
                    flag=1
                pygame.time.wait(100)   # wait for it to finish
            sleep(3 * DELAY)            # once finished, add delay for next character


# main driver function
# parses arguments 
# prompts the user for necessary inputs if arguments not provided 
def run():
    try:
        clear()
        
        pt,ct = None,None
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            pt = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END))        # plaintext input
            morse = encrypt(pt)                      # calling the enc() function with the input
            print('{}[+]{} The Morse Code is : {}{}{}'.format(color.GREEN,color.END,color.RED,morse,color.END))
        elif choice == 'd' or choice == 'D':
            ct = input('{}[?]{} Enter the Morse Code : '.format(color.BLUE,color.END))       # ciphertext input
            plaintext = decrypt(ct)                       # calling dec() function with the input
            print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
            quit()

        play = input('{}[?]{} Do you want to play the Morse Code? [y/n] : '.format(color.BLUE,color.END))
        if play[0].lower() == 'y':
            if pt:
                playSound(pt)
            elif ct:
                playSound(plaintext)
        quit()

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))

