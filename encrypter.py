# -*- coding: utf-8 -*-
"""
@author: Bhavya/lovelornflamewizard

> Terminology:
    
    FIELDS:
        meat        <--  original message
        bacon       <--  encrypted message
        sauce       <--  encryption password (needed for decryption)
        salt        <--  encryption salt
    
    METHODS:
        sauce_blender   <--  blends sauce after each encryption iteration
        retrace_sauce   <--  retraces sauce used at last stage of encryption, for decryption
        salt_shaker     <--  uses sauce checksum to generate salty salt
        grinder         <--  uses sauce checksum to randomize alphabet-typeset
        marinate        <--  converts num to char and vice versa
        string          <--  converts list to string

"""

alphabet_prototype = list(""" !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~""")
GRINDER_CAPACITY = 95
salt_length = 8


def encrypt(meat, sauce, multiplier, print_mode):
    meat_length = len(meat)
    sauce_length = len(sauce)
    bacon = list(meat)
    alphabet = grinder(sauce)
    
    for instance in range(0, multiplier+0, +1):
        sauce = sauce_blender(sauce, instance)
        salt = salt_shaker(sauce, alphabet)
        
        for i in range(meat_length):
            a = marinate(bacon[i], 'CHAR', alphabet)
            b = marinate(sauce[i%sauce_length], 'CHAR', alphabet)
            c = marinate(salt[i%salt_length], 'CHAR', alphabet)
            n = (a + (b*b) + (c*c*c) + i%sauce_length)%GRINDER_CAPACITY
            
            if(print_mode and instance == multiplier-1):
                print(marinate(n, "NUM", alphabet), end="")
            bacon[i] = marinate(n, 'NUM', alphabet)
    
    if(not print_mode):
        return string(bacon)


def decrypt(bacon, sauce, multiplier, print_mode):
    bacon_length = len(bacon)
    sauce_length = len(sauce)
    meat = list(bacon)
    alphabet = grinder(sauce)
    
    for instance in range(0, multiplier, +1):
        sauce = retrace_sauce(sauce, instance)
        salt = salt_shaker(sauce, alphabet)
    
    for instance in range(multiplier-1, -1, -1):
        for i in range(bacon_length):
            a = marinate(meat[i], 'CHAR', alphabet)
            b = marinate(sauce[i%sauce_length], 'CHAR', alphabet)
            c = marinate(salt[i%salt_length], 'CHAR', alphabet)
            n = (a - (b*b) - (c*c*c) - i%sauce_length)%GRINDER_CAPACITY
            
            if(print_mode and instance == 0):
                print(marinate(n, "NUM", alphabet), end="")
            meat[i] = marinate(n,  'NUM', alphabet)
        
        sauce = sauce_blender(sauce, instance)
        salt = salt_shaker(sauce, alphabet)
    
    if(not print_mode):
        return string(meat)


def sauce_blender(sauce, instance):
    sauce = list(sauce)
    sauce_length = len(sauce)
    
    if(instance == 1 or instance == 3):
        sauce = sauce[::-1]
    if(instance == 2):
        for i in range(sauce_length):
            if(i%2 == 0 and i != sauce_length-1):
                temp_particle = sauce[i];
                sauce[i] = sauce[i+1];
            if(i%2 == 1):
                sauce[i] = temp_particle;
    
    return string(sauce)


def retrace_sauce(sauce, instance):
    sauce = sauce_blender(sauce, instance)
    return sauce


def salt_shaker(sauce, alphabet):
    A = 1; B = 0
    for c in sauce:
        A += marinate(c, 'CHAR', alphabet)
        B += A
    return "{0:08d}".format(((A*B)**2)%99999999)


def grinder(sauce):
    input = list(salt_shaker(sauce, alphabet_prototype))
    input_length = len(input)
    output = []
    
    grease = alphabet_prototype[:]
    
    for i in range(GRINDER_CAPACITY):
        grease_length = len(grease)
        position = 5*i + int(input[i%input_length])
        output.append(grease.pop(position%grease_length))
    
    return output


def marinate(package, package_type, alphabet):
    if(package_type == "CHAR"):
        return alphabet.index(package)
    if(package_type == "NUM"):
        return alphabet[package]


def string(list_):
    return "".join(list_)

def main():
    key = input()
    cipher = encrypt(input(), key, 20, False)
    print(cipher)
    cipher = input()
    plain = decrypt(cipher, key, 20, False)
    print(plain)

if __name__ == "__main__":
    main()
