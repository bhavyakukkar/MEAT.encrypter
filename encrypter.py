# -*- coding: utf-8 -*-
"""
@author: Bhavya/lovelornflamewizard

> Terminology:
    meat        <--  original message
    bacon       <--  encrypted message
    pepper      <--  encryption password
    grinder     <--  char ⇌ num, based on alphabet-ruleset

"""

GRINDER_CAPACITY = 95


def encrypt(meat, pepper, multiplier, print_mode):
    meat_length = len(meat)
    pepper_length = len(pepper)
    bacon = list(meat)
    
    for instance in range(0, multiplier+0, +1):
        pepper = shuffle_pepper(pepper, instance)
        
        for i in range(meat_length):
            a = char_grinder(bacon[i], 'CHAR')
            b = char_grinder(pepper[i%pepper_length], 'CHAR')
            c = (a + b + i%pepper_length)%GRINDER_CAPACITY
            
            if(print_mode and instance == multiplier-1):
                print(char_grinder(c, "NUM"), end="")
            bacon[i] = char_grinder(c, 'NUM')
    
    if(not print_mode):
        return string(bacon)


def decrypt(bacon, pepper, multiplier, print_mode):
    bacon_length = len(bacon)
    pepper_length = len(pepper)
    meat = list(bacon)
    
    for instance in range(0, multiplier, +1):
        pepper = retrace_pepper(pepper, instance)
    
    for instance in range(multiplier-1, -1, -1):
        for i in range(bacon_length):
            a = char_grinder(meat[i], 'CHAR')
            b = char_grinder(pepper[i%pepper_length], 'CHAR')
            c = (a - b - i%pepper_length)%GRINDER_CAPACITY
            
            if(print_mode and instance == 0):
                print(char_grinder(c, "NUM"), end="")
            meat[i] = char_grinder(c,  'NUM')
        
        pepper = shuffle_pepper(pepper, instance)
    
    if(not print_mode):
        return string(meat)


def shuffle_pepper(pepper, instance):
    pepper = list(pepper)
    pepper_length = len(pepper)
    
    if(instance == 1 or instance == 3):
        pepper = pepper[::-1]
    if(instance == 2):
        for i in range(pepper_length):
            if(i%2 == 0 and i != pepper_length-1):
                temp_particle = pepper[i];
                pepper[i] = pepper[i+1];
            if(i%2 == 1):
                pepper[i] = temp_particle;
    
    return string(pepper)


def retrace_pepper(pepper, instance):
    pepper = shuffle_pepper(pepper, instance)
    return pepper


def char_grinder(package, package_type):
    alphabet = list(""" !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~""")
    
    if(package_type == "CHAR"):
        return alphabet.index(package)
    if(package_type == "NUM"):
        return alphabet[package]


def string(list_):
    return "".join(list_)
