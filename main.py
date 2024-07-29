import pandas as pd


class Product():
    def __init__(self, name, price, quantity, product_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.product_id = product_id

    @classmethod
    def load_data(cls, file_path: str,
                  file_name: str):  # cls scroutout (skrót) form class and it means that the method is used in class where it is delarated
        product = []
        df = pd.read_csv(file_path + file_name)
        for _, row in df.iterrows():  # by ' _ ' is marked thad we can't use value of iterator in for
            product.append(cls(row['name'], row['price'], row['quantity'], row['product_id']))
        return product

    @staticmethod
    def to_dataFrame(products):
        data = [{
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'product_id': item.product_id
        } for item in products]
        return pd.DataFrame(data)

    @staticmethod
    def save_data(df, file_path: str, file_name: str):
        df.to_csv(file_path + file_name, index=False)


class Basket():
    def __init__(self, owner):
        self.owner = owner
        self.products_in_basket = []

    def add_to_basket(self, product, quantity):
        pass


class User():
    pass


class Shop():
    def __init__(self, name):
        self.name = name
        # self.products = []

    # TODO: improve to operate on DataFrame
    @staticmethod
    def add_product_logic(list_of_products, name, price, quantity):  # method allows add or update product in database
        is_product_found = False
        # new_product_id = 1

        for product in list_of_products: # checking if the product already exist in database
            if product.name == name:
                product.quantity += quantity
                is_product_found = True
                break

        if not is_product_found:
            existings_ids = [product.product_id for product in list_of_products]
            new_product_id = 1
            while new_product_id in existings_ids: # checking if the product_id are in order
                new_product_id += 1
            new_product = Product(name, price, quantity, new_product_id)
            list_of_products.append(new_product)
        return list_of_products

    # TODO: poprawić tak aby można było usuwac też daną ilość produktu a nie cały rekord
    @staticmethod
    def remove_product_logic(df, name:str, quantity):

        if quantity is None:
            if name in df['name'].values:
                # df = df[df['name'] != name]
                df = df.drop(index=('name', 'Camera'))
                print('Product deleted successfully!')
            else:
                print('''
                ==================================================================
                | Product, that you are trying to delete probably doesn't exist! |
                ==================================================================
                ''')
        else:
            pass

        return df



class UI():
    def __init__(self):
        self.shop = Shop("Name of the shop")
        self.file_path = 'data/'
        self.file_name = 'products.csv'

    @classmethod
    def print_menu(self):
        print('''
        ============== MENU ==============
        1. Display database.
        2. Add product.
        3. Remove product.
        0. Exit
        ''')
        # print('============== MENU ==============')
        # print('1. Display database.')


    def back_to_main_menu(self):
        pass

    def load_database_to_UI_in_DataFrame(self):
        prods = Product.load_data(self.file_path, self.file_name)  # Loading data
        df = Product.to_dataFrame(prods)  # converting to dataFrame
        return df

    def load_database_to_UI_in_list(self):
        prods = Product.load_data(self.file_path, self.file_name)
        return prods

    def display_database(self):
        # prods = Product.load_data(self.file_path, self.file_name)  # Loading data
        # df = Product.to_dataFrame(prods)  # converting to dataFrame
        df = self.load_database_to_UI_in_DataFrame()
        print(df)

    # TODO: improve to operate on DataFrame
    def add_product(self):
        name = input('Enter product name: ')
        quantity = int(input('Enter product quantity: '))
        prods = Product.load_data(self.file_path, self.file_name)
        is_product_exist = any(product.name == name for product in prods)

        if is_product_exist:
            price = None # 'cause product already exist and we don't  have to change his price
        else:
            price = float(input('Enter product price: ')) # price for new products

        prods = self.shop.add_product_logic(prods, name, price, quantity)
        df = Product.to_dataFrame(prods)
        # Product.save_data(df, self.file_path, self.file_name)
        Product.save_data(df, self.file_path, self.file_name)
        print('Product added successfully!')

    def remove_product(self):
        name = input("Enter product name to remove: ")
        df = self.load_database_to_UI_in_DataFrame()
        df = self.shop.remove_product_logic(df, name, None)
        Product.save_data(df, self.file_path, self.file_name)

    def run(self):
        while True:
            self.print_menu()
            x = input('Your choise: ')
            if x == '1':
                ui.display_database()
            elif x == '2':
                self.add_product()
            elif x == '3':
                self.remove_product()

            elif x == '0':
                print('Exiting...')
                exit()
            else:
                print(f'Invalid option. Please try again.')


if __name__ == "__main__":
    ui = UI()  # creation of instance of UI class
    ui.run()
