from peewee import *
from datetime import date

db = MySQLDatabase('spider',host = '127.0.0.1',port = 3306,user = 'root',password = '123456')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.
        # table_name = 'user'  #指定表名


if __name__ == '__main__':
    db.create_tables([Person])

    # 增删改查(这里的增删改查全是在操作对象 而不是使用sql语句直接操作数据库
    #1、插入数据
    #     #1）使用save()方法
    # uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
    # uncle_bob.save()
    #     #2)使用create()方法
    # grandma = Person.create(name='chenpengfei', birthday=date(1935, 3, 1))
    # herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

    #2、查询数据
        #1)获取单条数据Select.get()、Model.get()
    # chen = Person.select().where(Person.name == 'chenpengfei').get() #get()方法取不到数据时会抛出异常
    #
    # print(chen.birthday)


        #2)、获取所有数据
    Bobs = Person.select().where(Person.name == 'Bob')[1:] # 获取第二条数据
    for Bob in Bobs:
        print(Bob.name + str(Bob.birthday))
    # Bobs = Person.select().where(Person.name == 'Bob')
    # for Bob in Bobs:
    #     print(Bob.name + str(Bob.birthday))

    #3、修改数据
    # Bobs = Person.().where(Person.name == 'Bob')
    # for Bob in Bobs:
    #     Bob.birthday = date(1960,11,17)
    #     Bob.save()

    # 4、删除数据
    Bobs = Person.select().where(Person.name == 'Bob')
    for Bob in Bobs:
        Bob.delete_instance()

    pass


