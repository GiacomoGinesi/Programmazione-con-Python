#!/usr/bin/env python
# coding: utf-8

# In[2]:


import csv
import os
from datetime import datetime
from Functions import help_cmd
from Functions import stock_info
from Functions import add
from Functions import itemize
from Functions import sell
from Functions import profit



cmd = None
while cmd!="chiudi":

    cmd = input("\nInserire un comando per eseguire un'azione (digitare aiuto per vedere le funzioni disponibili): ")  
    
    if cmd == "vendita":

        sold_dict = {}
        answer = "si"
        
        while answer.lower() != "no":
            is_string,quantity = False,None

            while is_string == False:
                try:
                    product_name = input("Nome del prodotto: ")  
                    if product_name.isnumeric():
                        is_string == False
                        raise ValueError("\nProdotto non valido: inserito valore numerico")
                        continue
                    else:
                        is_string = True
                except ValueError as e:
                    print(e)

            while quantity == None or quantity <= 0:
                try:
                    quantity = int(input("Quantità: "))
                    if quantity <= 0:
                        print( "\nIl valore inserito è minore o uguale a zero. Inserire un valore positivo per la quantità")
                except ValueError:
                    print("\nQuantità non valida: inserire numero intero")
    
          
            stop = sell(product_name,quantity)
            stock = stock_info()
            
            if stop == 1:
                sold_dict[product_name] = quantity
  
            answer = input("Vendere un altro prodotto?: [si/no]")
        
        if len(list(sold_dict.keys())) != 0:
            print("\nVENDITA REGISTRATA CORRETTAMENTE!: ")
            
        total_sold = 0
        for key in list(sold_dict.keys()):
            print(f"{sold_dict[key]} X {key}: €{stock[key]['Prezzo di vendita']}")
            total_sold += (stock[key]['Prezzo di vendita'] * sold_dict[key])
        print(f"\nTotale: €{total_sold:.2f}")





    elif cmd == "profitti":

        profit()


    
    elif cmd == "aggiungi":
    
        is_string,quantity = False,None
        while is_string == False:
            try:
                product_name = input("Nome del prodotto: ")  
                if product_name.isnumeric():
                    is_string == False
                    raise ValueError("\nInserimento prodotto non valido: valore numerico inserito") 
                    continue
                else:
                    is_string = True
            except ValueError as e:
                print(e)

        while quantity == None or quantity <= 0:
            try:
                quantity = int(input("Quantità: ")) 
                if quantity <= 0:
                    print( "\nIl valore inserito è minore o uguale a zero. Inserire un valore positivo per la quantità")
            except ValueError:
                print("\nQuantità non valida: inserire numero intero")
                    

        add(product_name,quantity)





    elif cmd == "elenca":
    
        itemize()
        



    elif cmd == "aiuto":
    
        help_cmd()




    
    elif cmd == "chiudi":

        print("Bye Bye, ci si vede alla prossima operazione!")
        break
    else:
        print("\nComando non valid")
        help_cmd()

