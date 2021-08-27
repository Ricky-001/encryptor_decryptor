# encryptor_decryptor
A simplistic implementation of common encryption and decryption mechanisms in Python through an easy-to-use script

Currently, the script utilizes the following encryption/ decryption algorithms:-
- Rotational/ Shift (Caesar) Cipher
- Incremental Rotational Cipher
- Multiplicative Cipher
- Vigenere Cipher
- Autokey Cipher
- ROT47 Cipher
- Multitap (SMS Keypad) Code
- Morse Code (with audio)
(please note that this list is intended to increase over time as more algorithms shall be implemented)

[No dependencies except for the Morse Code, which requires the "pygame" module to play audio]

____________

* Choose the algorithm to use followed by the mode of operation ('E' or 'D' fopr encryption or decryption) and follow the on-screen instructions.
* For algorithms that are feasibly susceptible to brute force attacks, leaving the key empty will trigger a brute force against the ciphertext during the decryption process.
