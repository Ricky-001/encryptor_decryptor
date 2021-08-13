#!/usr/bin/python3

from utilities.colors import color
from utilities.tools import clear

# encryption function that takes the plaintext and number of steps to rotate
# and returns the encrypted text (plaintext rotated by steps no. of ASCII characters)
def encrypt(plain,steps):

    # list with the ASCII values of the plaintext
    plainASCII = [ord(char) for char in plain]
    cipherASCII = []
    # rotating the ASCII values by 'steps' no. of steps
    # x=32 is kept the same to preserve space characters
    
    for x in plainASCII:
        if x in range(97,123):
            if x+steps>122:              # lowercase letters
                cipherASCII.append(x+steps-26)
            else:
                cipherASCII.append(x+steps)
        elif x in range(65,91):          # uppercase letters
            if x+steps>90:
                cipherASCII.append(x+steps-26)
            else:
                cipherASCII.append(x+steps)
        elif x in range(48,58):          # numeric values
            if x+(steps%10)>57:
                cipherASCII.append(47+((steps%10)-(57-x)))
            else:
                cipherASCII.append(x+(steps%10))
        else:
            cipherASCII.append(x)
    
    # coverting the ASCII values of the cipherASCII (rotated) 
    # into their corresponding characters as the ciphertext
    cipher = ''.join(map(chr,cipherASCII))
    #print(cipher)
    return cipher

# decryption function that takes the ciphertext and the number of steps originally rotated
# the step count also remain None (if not explicitly passed by user) - which triggers a brute force from step values -26 to +26
# returns the plaintext based on the given step count or all possible results in case of bruteforce
def decrypt(cipher,steps=None):
    
    # list with the ASCII values of the ciphertext
    cipherASCII = [ord(char) for char in cipher]
    plainASCII = []

    # if step count is given by user
    if steps:
        # reverse rotating the ASCII values by 'steps' no. of steps
        
        for x in cipherASCII:
            if x in range(97,123):
                if x-steps<97:              # lowercase letters
                    plainASCII.append(123-(97-(x-steps)))
                else:
                    plainASCII.append(x-steps)
            elif x in range(65,91):          # uppercase letters
                if x-steps<65:
                    plainASCII.append(91-(65-(x-steps)))
                else:
                    plainASCII.append(x-steps)
            elif x in range(48,58):          # numeric values
                if x-(steps%10)<48:
                    plainASCII.append(58-(48-(x-(steps%10))))
                else:
                    plainASCII.append(x-(steps%10))
            else:
                plainASCII.append(x)

        plain = ''.join(map(chr,plainASCII))
        #print(plain)
        return plain

    # if step count is not provided - bruteforce
    else:
        steps = -26 # initialising steps from -26
        for steps in range(26):
            plainASCII=[]
            for x in cipherASCII:
                if x in range(97,123):
                    if x-steps<97:              # lowercase letters
                        plainASCII.append(123-(97-(x-steps)))
                    else:
                        plainASCII.append(x-steps)
                elif x in range(65,91):          # uppercase letters
                    if x-steps<65:
                        plainASCII.append(91-(65-(x-steps)))
                    else:
                        plainASCII.append(x-steps)
                elif x in range(48,58):          # numeric values
                    if x-(steps%10)<48:
                        plainASCII.append(58-(48-(x-(steps%10))))
                    else:
                        plainASCII.append(x-(steps%10))
                else:
                    plainASCII.append(x)

            plain = ''.join(map(chr,plainASCII))
            # prints all possible combinations for rotation steps -26 to +26
            print('{}[!]{} ROT{} \t:{}{}{}'.format(color.GREEN,color.END,str(steps),color.GREEN,plain,color.END))
            steps+=1
        return

# preparatory function for encryption that takes in the 
# plaintext and step counts from user and calls the encrypting function with those values
# returns the ciphertext as returned from encryption function along with the step count given by user
def enc(plain):

    # taking input for the number of steps to rotate
    # int between -26 to +26 (with or without the signs allowed)
    try:
        steps = int(input('{}[?]{} Enter the number of steps to rotate (+x or -x): '.format(color.BLUE,color.END)))
        # checking if the given input is within the valid range
        if steps not in range(-26,27):
            raise ValueError()
        # calling the encrypt function with the plaintext and steps to rotate        
        ciphertext = encrypt(plain, steps)

    # catching and handling ValueError to end gracefully
    except ValueError:
        print('{}[-]{} Please enter a number between 1-26 with + or - sign'.format(color.RED,color.END))

    finally:
        return ciphertext,steps

# preparatory function for decryption that takes in the 
# ciphertext and step counts (if given) from user and calls the encrypting function with those values
# returns the ciphertext as returned from encryption function along with the step count given by user   -   for known step count
# returns None,None to caller function as bruteforce results are displayed by the decrypting function   -   for bruteforce
def dec(cipher):

    steps = None
    # taking input for the number of steps to reverse rotate
    # int between -26 to +26 (with or without the signs allowed)
    # this is the original number of steps as used during encryption
    try:
        steps = int(input('{}[?]{} Enter the number of steps rotated during encryption \n{}[!]{} Leave empty to try bruteforce (+x or -x): '.format(color.BLUE,color.END,color.CYAN,color.END)))

        # checking if the given input is within the valid range
        if steps not in range(-26,27):
            raise ValueError()
        # calling the encrypt function with the plaintext and steps to rotate        
        plaintext = decrypt(cipher=cipher, steps=steps)

    # catching and handling ValueError to end gracefully
    except ValueError:
        if not steps:            
            decrypt(cipher=cipher,steps=steps)
        else:
            print('{}[-]{} Please enter a number between 1-26 with + or - sign'.format(color.RED,color.END))
    
    finally:
        if steps:
            return plaintext,steps
        else:
            return None,None


# main driver function
# parses arguments 
# prompts the user for necessary inputs if arguments not provided 
def run():
    try:
        clear()
        
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            pt = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END))        # plaintext input
            ciphertext,steps = enc(pt)                      # calling the enc() function with the input
            print('{}[+]{} The Ciphertext with {}{}{} steps is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,steps,color.END,color.RED,ciphertext,color.END))
        elif choice == 'd' or choice == 'D':
            ct = input('{}[?]{} Enter the Ciphertext : '.format(color.BLUE,color.END))       # ciphertext input
            plaintext,steps = dec(ct)                       # calling dec() function with the input
            if steps:                                       # if not bruteforce - then only print results
                print('{}[+]{} The Plaintext with {}{}{} steps is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,steps,color.END,color.RED,plaintext,color.END))
            else:
                print('{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
        quit()

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
