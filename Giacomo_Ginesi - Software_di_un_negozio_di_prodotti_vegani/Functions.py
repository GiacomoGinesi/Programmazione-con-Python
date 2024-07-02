#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import os
from datetime import datetime



def help_cmd():

  """
  Function that prints an help message with informations on the available commands to use to run the software
  """
  
  print("\nI comandi disponibili sono i seguenti:\n"+
        "aggiungi: aggiungi un prodotto al magazzino\n"+
        "elenca: elenca i prodotti in magazzino\n"+
        "vendita: registra una vendita effettuata\n"+
        "profitti: mostra i profitti totali\n"+
        "aiuto: mostra i possibili comandi\n"+
        "chiudi: esci dal programma")

    





def stock_info():

  """
  Function that generates a file csv called Stock, opened in write mode to record sales
  """
  
  with open("Magazzino.csv","r") as csv_file:        
        csv_reader = csv.DictReader(csv_file)
        list_dict = []
        for row in list(csv_reader):
            list_dict.append(row)

        for i,line in enumerate(list_dict):
            prev_lines = []
            for j in range(i):
                prev_lines.append(list_dict[j]["PRODOTTO"])
            for k,prev_line in enumerate(prev_lines):
                if line["PRODOTTO"] == prev_line:
                    list_dict[k]["QUANTITÀ"] = int(list_dict[k]["QUANTITÀ"]) + int(line["QUANTITÀ"])
                else:
                    continue

        tmp = {}           
        for i,row in enumerate(list_dict):
            prev_lines = []
            for j in range(i):
                prev_lines.append(list_dict[j]["PRODOTTO"])
    
            if not row["PRODOTTO"] in prev_lines:

                info = {}
                info["Quantità"] = int(row["QUANTITÀ"])
                info["Prezzo d'acquisto"] = float(row["PREZZO D'ACQUISTO"])
                info["Prezzo di vendita"] = float(row["PREZZO DI VENDITA"])
                tmp[row["PRODOTTO"]] = info
            else:
                continue
        return tmp 
    
    






def add(product_name,quantity):
    
    """
    Function that adds the purchased products to the stock.
    """

    with open("Magazzino.csv","a+",newline="") as csv_file:
        columns = ["PRODOTTO","QUANTITÀ","PREZZO D'ACQUISTO","PREZZO DI VENDITA","OPERAZIONE","DATA E ORA"]
        csv_reader = csv.DictReader(csv_file)
        csv_writer = csv.DictWriter(csv_file,fieldnames = columns)

        
        fileEmpty = os.stat("Magazzino.csv").st_size == 0
        if fileEmpty:
            csv_writer.writeheader()  

        
        list_products = []
        csv_file.seek(0)
        for row in csv_reader:
            list_products.append(row["PRODOTTO"])
            
        
        if not product_name in set(list_products):
            purchase_price,selling_price = None,None
            while purchase_price == None or purchase_price <= 0:
                try:
                    purchase_price = float(input("Prezzo d'acquisto: "))
                    if purchase_price <= 0:
                        print(f"\nIl valore inserito {purchase_price} è minore o uguale a zero. Inserire un nuovo valore positivo per il prezzo d'acquisto")
                except ValueError:
                    print("\nPrezzo d'acquisto non valido: inserire numero decimale")
            while selling_price == None or selling_price <= 0:
                try:        
                    selling_price = float(input("Prezzo di vendita: "))
                    if selling_price <=0 :
                        print(f"\nIl valore inserito {selling_price} è minore o uguale a zero. Inserire un nuovo valore positivo per il prezzo di vendita")
                except ValueError:
                    print("\nPrezzo di vendita non valido: inserire numero decimale")

            
            csv_writer.writerow({"PRODOTTO":product_name,"QUANTITÀ":quantity,"PREZZO D'ACQUISTO":purchase_price,"PREZZO DI VENDITA":selling_price,"OPERAZIONE":"acquisto","DATA E ORA":datetime.strftime(datetime.now(), "%d-%m-%Y %H.%M.%S")})

        
        else:
            csv_file.seek(0)
            list_lines = []
            for row in list(csv_reader)[1:]:
                list_lines.append(row)
            for i,product in enumerate(list_products):
                if product_name == product:
                    z = i
                    break
                else:
                    continue
            
            csv_writer.writerow({"PRODOTTO":product_name,"QUANTITÀ":quantity,"PREZZO D'ACQUISTO":list_lines[z]["PREZZO D'ACQUISTO"],"PREZZO DI VENDITA":list_lines[z]["PREZZO DI VENDITA"],"OPERAZIONE":"acquisto","DATA E ORA":datetime.strftime(datetime.now(), "%d-%m-%Y %H.%M.%S")})
        
        print(f"AGGIUNTO {quantity} X {product_name}")
    
    stock_info()
        









def itemize():
    
    """
    Function that lists the stock.
    """

    try:
        stock = stock_info()
        head_text = ["\nPRODOTTO","QUANTITÀ","PREZZO"]
        print(*head_text)

        for i in range(len(list(stock.keys()))):
            if list(stock.values())[i]["Quantità"] != 0:
                print(f"{list(stock.keys())[i]} "+
                f"{list(stock.values())[i]['Quantità']} "+
                f"€{list(stock.values())[i]['Prezzo di vendita']:.2f} ")
    except FileNotFoundError:
        print("Il registro acquisti/vendite non esiste. Forse il primo acquisto non è stato registrato?")
        
        
        








def sell(product_name,quantity):
    
    """
    Function that adds sales to the stock.
    """

    with open("Magazzino.csv","a+",newline="") as csv_file:
        columns = ["PRODOTTO","QUANTITÀ","PREZZO D'ACQUISTO","PREZZO DI VENDITA","OPERAZIONE","DATA E ORA"]
        csv_reader = csv.DictReader(csv_file)
        csv_writer = csv.DictWriter(csv_file,fieldnames=columns)
        fileEmpty = os.stat("Magazzino.csv").st_size == 0
        if fileEmpty:
            csv_writer.writeheader()  
        
        list_products = []
        csv_file.seek(0)
        for row in csv_reader:
            list_products.append(row["PRODOTTO"])

        if not product_name in set(list_products):
            print("Prodotto non presente in magazzino")
        
        else:
            csv_file.seek(0)
            csv_reader = csv.DictReader(csv_file)
            list_lines = []
            for row in list(csv_reader):
                list_lines.append(row)
            for i,product in enumerate(list_products):
                if product_name == product:
                    z = i
                    break
                else:
                    continue
            
            csv_file.seek(0) 
            csv_reader = csv.DictReader(csv_file)
            list_dict = []
            for row in list(csv_reader):
                list_dict.append(row)
            
            for i,line in enumerate(list_dict):
                prev_lines = []
                for j in range(i):
                    prev_lines.append(list_dict[j]["PRODOTTO"])
                for k,prev_line in enumerate(prev_lines):
                    if line["PRODOTTO"] == prev_line:
                        list_dict[k]["QUANTITÀ"] = int(list_dict[k]["QUANTITÀ"]) + int(line["QUANTITÀ"])
                    else:
                        continue

            tmp={}           
            for i,row in enumerate(list_dict):
                prev_lines = []
                for j in range(i):
                    prev_lines.append(list_dict[j]["PRODOTTO"])

                if not row["PRODOTTO"] in prev_lines:
                    info={}
                    info["Quantità"] = int(row["QUANTITÀ"])
                    info["Prezzo d'acquisto"] = float(row["PREZZO D'ACQUISTO"])
                    info["Prezzo di vendita"] = float(row["PREZZO DI VENDITA"])
                    tmp[row["PRODOTTO"]] = info

                else:
                    continue

            if quantity <= int(tmp[product_name]["Quantità"]):
                csv_writer.writerow({"PRODOTTO":product_name,"QUANTITÀ":-quantity,"PREZZO D'ACQUISTO":list_lines[z]["PREZZO D'ACQUISTO"],"PREZZO DI VENDITA":list_lines[z]["PREZZO DI VENDITA"],"OPERAZIONE":"vendita","DATA E ORA":datetime.strftime(datetime.now(), "%d-%m-%Y %H.%M.%S")})
                stop = 1
            else:
                availability=int(tmp[product_name]["Quantità"])
                print(f"Disponibilità massima in magazzino per il prodotto {product_name}: {availability}")
                stop = 0

            return stop

    stock_info()





    
  
def profit():

  """
  Function that prints the total gross and net profit 
  """

  with open("Magazzino.csv") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        list_lines = []
        buying_cost = 0
        gross_profit = 0
        for row in list(csv_reader):
            list_lines.append(row)
        for line in list_lines:

            if line["OPERAZIONE"] == "acquisto":
                buying_cost += float(line["PREZZO D'ACQUISTO"]) * int(line["QUANTITÀ"])
                
            if line["OPERAZIONE"] == "vendita":
                gross_profit +=- (float(line["PREZZO DI VENDITA"]) *int (line["QUANTITÀ"]))
    
  net_profit = gross_profit-buying_cost
  print(f"Profitto: lordo = {gross_profit:.2f}€, netto = {net_profit:.2f}€")


# In[ ]:




