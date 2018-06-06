import csv
import os
import re # source: https://stackoverflow.com/questions/4138202/using-isdigit-for-floats

def menu(username="@prof-rossetti", products_count=100):

    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Restore the product list.
    Please select an operation: """
    return menu

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            products.append(dict(row))
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader()
        for p in products:
            writer.writerow(p)

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)
    return len(products)

def valid_int_number(dataentry):
    while not dataentry.isdigit():
        dataentry = input("Please enter a whole number: ")
    return dataentry

def valid_float_number(dataentry):
    valid = re.compile('\d+(\.\d+)?')
    while valid.match(dataentry) == None:
        dataentry = input("Please input a price formatted as a number with two decimal places, like 0.77: ")
    return dataentry

def product_match(products, selection, message):
    print("-------------------------------")
    print(message)
    print("-------------------------------")
    matching_products =[p for p in products if int(p["id"])==int(selection)]
    matching_product = matching_products[0]
    print(matching_product)

def get_selection(products):
    selection = int(valid_int_number(input("Please enter the products identifier: ")))
    matching_products =[p for p in products if int(p["id"])==int(selection)]
    while len(matching_products) == 0:
        print("PRODUCT IDENTIFIER DOES NOT EXIST")
        selection = int(valid_int_number(input("Please enter the products identifier: ")))
        matching_products =[p for p in products if int(p["id"])==int(selection)]
    return selection

def run():
    products = read_products_from_file()
    NoProducts = len(products)
    ProdId = int(products[NoProducts - 1]["id"])


    print(menu("@Jared1989", NoProducts))
    selection = input("Please select an operation, or 'DONE' to quit: ")
    if selection.upper() == "LIST":
        print("-------------------------------")
        print("There are", NoProducts, "products:")
        print("-------------------------------")
        for p in products:
            print(" #"+p["id"]+":", p["name"])
    elif selection.upper() == "SHOW":
        selection = get_selection(products)
        product_match(products, selection, "SHOWING A PRODUCT:")
    elif selection.upper() == "CREATE":
        ProdId += 1
        ProdName = input("Please enter the products name: ")
        ProdAisle = input("Please enter the products aisle: ")
        ProdDepartment = input("Please enter the products department: ")
        ProdPrice = float(valid_float_number(input("Please enter the products price: ")))
        New_Value = {"id":ProdId,"name":ProdName,"aisle":ProdAisle,"department":ProdDepartment,"price":ProdPrice}
        products.append(dict(New_Value))
        write_products_to_file("products.csv", products)
        NoProducts += 1
        product_match(products, ProdId, "CREATING A NEW PRODUCT:")
    elif selection.upper() == "UPDATE":
        selection = get_selection(products) - 1
        ProdName = input("What is the product's new 'name' currently: ('" + products[selection]["name"] + "'): ")
        products[selection]["name"] = ProdName
        ProdAisle = input("What is the product's new 'aisle' currently: ('" + products[selection]["aisle"] + "'): ")
        products[selection]["aisle"] = ProdAisle
        ProdDepartment = input("What is the product's new 'department' currently: ('" + products[selection]["department"] + "'): ")
        products[selection]["department"] = ProdDepartment
        ProdPrice = float(valid_float_number(input("What is the product's new 'price' currently: ('" + '${0:.2f}'.format(float(products[selection]["price"])) + "'): ")))
        products[selection]["price"] = ProdPrice
        write_products_to_file("products.csv", products)
        product_match(products, selection + 1, "UPDATED A PRODUCT:")
    elif selection.upper() == "DESTROY":
        selection = get_selection(products)
        product_match(products, selection, "DESTROYING A PRODUCT:")
        products.pop(selection - 1)
        write_products_to_file("products.csv", products)
        NoProducts -= 1
    elif selection.upper() == "RESET":
        NoProducts = reset_products_file()
    else:
        print("Hey, are you sure the operation is correct? Please try again!")

if __name__ == "__main__":
    run()
