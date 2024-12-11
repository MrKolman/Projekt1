'''
LagerLand.PY: Ett program som ska hantera en csv fil med "produkter" och med simpelt gränssnitt kunna radera, editera, lägga till och felhantera.

__author__  = "Alfred Kållberg"
__version__ = "1.0.0"
__email__   = "alfred.kallberg@elev.ga.ntig.se"
'''

import csv
import os
import locale
from time import sleep

def load_data(filename): 
    products = [] 
    
    with open(filename, 'r', encoding="UTF-8") as file: #Laddar in cvs filen
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id']) 
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append( 
                {   
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

#gör en funktion som hämtar en produkt

def add_products(products, name, desc, price, quantity):    #Denna funktion skapar datastrukturen för products

    max_id = max(products, key = lambda x: x['id'])
    new_id = max_id['id'] + 1

    new_product = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }

    products.append(new_product)

    with open('products.csv', 'a') as fd:
        fd.write(f"\n{new_id},{name},{desc},{price},{quantity}")

    return f"Du la till produkt {name} med id: {new_id}"

def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break

    if temp_product:
        products.remove(temp_product)

        with open('products.csv', 'w', newline='') as file:
            fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for product in products:
                writer.writerow(product)
        
        return f"Produkt med id: {id + 1} har tagits bort"
    else:
        return f"Produkt med id: {id + 1} hittades inte"

def edit_product(products, id, name, desc, price, quantity):
    edit = None

    for product in products:
        if product['id'] == id:
            edit = product
            break

    if edit != None:
        edit['name'] = name
        edit['desc'] = desc
        edit['price'] = price
        edit['quantity'] = quantity

        with open('products.csv', 'w', newline='') as file:
            fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()

            for product in products:
                writer.writerow(product)

        return f"Produkt med id: {id + 1} har ändrats"
    
    return f"Produkt med id: {id + 1} hittades inte"


def view_product(products, id):
    for product in products:
        if product["id"] == id:
            # Visar upp produktens namn och beskrivining
            return f"Visar produkt: {product['name']} {product['desc']}"
    
    # Error medelande ifall att produkten inte finns
    return "Produkten hittas inte"


def view_products(products):
    product_list = []
    name_width = 25
    desc_width = 45
    price_width = 5

    header = f"{'Id':<6} {'Name':<{name_width}} {'Description':<{desc_width}} {'Price':>{price_width}}"
    product_list.append(header)

    product_list.append("_______________________________________________________________________________________\n")

    for index, product in enumerate(products, 1):   #Gör så att om texten är för lång så gör den ... istället för att skriva ut allt
        name = product['name'] if len(product['name']) <= 15 else product['name'][:15] + "..."
        desc = product['desc'] if len(product['desc']) <= 30     else product['desc'][:30] + "..."
        
        product_info = f"{index:<5} {name:<{name_width}} {desc:<{desc_width}} {locale.currency(product['price'], grouping=True):>{price_width}}"
        product_list.append(product_info)

    product_list.append("_______________________________________________________________________________________")
    
    return "\n".join(product_list)

def get_product(products, id): #Tar fram den vala produkten
    for product in products:
        if product["id"] == id:
            return product
        
    return "Produkten finns ej"

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')    #Gör så att konsolen ser snyggish ut
products = load_data('products.csv')
while True:                                         #Huvudloopen av programmet
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))  # Visar listan av produkter

        choice = input("\n(L)ägg till \n(Ä)ndra \n(V)isa \n(T)a bort \n").strip().upper()

        if choice == "L":

            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))

            print(add_products(products, name, desc, price, quantity))
            sleep(1)

        elif choice in ["Ä", "V", "T"]:
            try:
                index = int(input("Enter product ID: "))

            except ValueError:
                print("Välj produkt-id med siffror")
                sleep(1)
                continue

            if 1 <= index <= len(products):
                selected_product = products[index - 1]
                id = selected_product['id']

            if choice == "Ä":
                placeholder = get_product(products, id)

                name = input(f"Nytt namn: ({placeholder['name']})   ")
                desc =  input(f"Ny beskrivning på produkten: ({placeholder['desc']}) ")
                price = float(input(f"Nytt pris: ({placeholder['price']})   "))
                quantity = int(input(f"Ny mängd av produkten: ({placeholder['quantity']})    "))

                edit_product(products, id, name, desc, price, quantity)

            if choice == "V":   #visa
                if 1 <= index <= len(products):  #  Ser till så att indexet är inom rätt "gränser"
                    selected_product = products[index - 1]  # Får produkten genom att använda index
                    id = selected_product['id']  # Tar ur id från produkten
                    print(view_product(products, id)) 
                    done = input()
                    
                else:
                    print("Ogiltig produkt")
                    sleep(1)

            elif choice == "T": #ta bort
                if 1 <= index <= len(products):  #  Ser till så att indexet är inom rätt "gränser"
                    selected_product = products[index - 1]  # Får produkten genom att använda index
                    id = selected_product['id']  

                    print(remove_product(products, id)) 
                    sleep(1)        

            elif choice == "S":
                None

            else:
                print("Ogiltig produkt")
                sleep(1)
        
    except ValueError:
        print("Välj en produkt med siffor")
        sleep(1)

