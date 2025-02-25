# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import uuid
from .utils import getDBConnection
import hashlib


class WebscrapingPipeline:
    def process_item(self, item, spider):
        return item


class SavingToPostgreSqlPipeline(object):

    def __init__(self):
        self.connection = getDBConnection()
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def if_any_change(self, id, item):
        query_string = "SELECT id FROM product where id = %s AND price = %s AND sizes = %s"
        query_set = (id, item['price'], self.to_curly_brackets(item['sizes']),)
        self.curr.execute(query_string, query_set)
        id = self.curr.fetchall()
        if len(id) > 0:
            print("change not found")
            return False
        else:
            print("change found")
            return True

    def to_curly_brackets(self, arr):
        return '{' + ','.join(arr) + '}'

    def store_db(self, item):
        try:
            query_string = "SELECT id FROM product WHERE link = %s"
            link = (item['link'],)

            self.curr.execute(query_string, link)
            id = self.curr.fetchall()

            if len(id) > 0:
                self.update_db(item, id[0])
            else:
                self.insert_db(item)

        except Exception as e:
            print("Error msg : ", e)
        finally:
            pass

    def update_db(self, item, id):
        try:
            if self.if_any_change(id, item):
                #  if there is a any change update the DB
                query_string = "UPDATE product SET availability = %s , price = %s, sizes = %s WHERE id = %s;"
                update_set = (item['availability'], item['price'], self.to_curly_brackets(item['sizes']), id,)

                # execute query and commit data
                self.curr.execute(query_string, update_set)
                self.connection.commit()
                print("successfully updated")
                # add that item to new table
                self.insert_new(id)
                print("add into the new")
        except Exception as e:
            self.connection.rollback()
            print("Update Error : ", e)
        finally:
            pass
        return item

    def insert_db(self, item):
        try:
            # query to insert data to product table
            query_string = "INSERT INTO product (id,title, shop_name, price, availability, description, sizes, images, link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"

            # we want to pass set of parameters. here are the parameters
            item_set = (
                str(uuid.uuid4()) ,item['title'], item['shop_name'], item['price'], item['availability'], item['description'],
                self.to_curly_brackets(item['sizes']), self.to_curly_brackets(item['images']), item['link'],)
            print(item_set)
            # execute and commit the query data
            self.curr.execute(query_string, item_set)
            self.connection.commit()

            # after insertion add data to new item table
            id = self.curr.fetchall()[0]
            self.insert_new(id)
            print("successfully inserted and add to new")
        except Exception as e:
            self.connection.rollback()
            print("Insertion Error : ", e)
        finally:
            pass
        return item

    def insert_new(self, id):
        new_table_insert_query_string = "INSERT INTO new (product_id) VALUES(%s);"
        id_set = (id,)
        try:
            # execute query and commit data
            self.curr.execute(new_table_insert_query_string, id_set)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Insertion of new table Error: ", e);
