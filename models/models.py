from peewee import *
from datetime import date

db = MySQLDatabase('spider',host = '127.0.0.1',port = 3306,user = 'root',password = '123456')

class BaseModel(Model):
    class Meta:
        database = db

#定义存储话题的table
'''
    设置字符类型时，对于char类型要设置最大长度，
    对于无法确定长度的要实用TextField()
    设计表时，采集到的数据要尽量做格式化处理
'''
class Topic(BaseModel):
    title = TextField()  #话题名称
    content = TextField(default = '') #评论  TextField()允许使用任意长的字符串
    Topic_ID = IntegerField(primary_key=True) #每个话题对应体格ID
    author =  TextField(null = True) #每个作者对应一个ID
    create_time = DateTimeField() #话题创建时间
    answer_num = IntegerField(default = 0) #回答数量
    click_num = IntegerField(default=0) #查看次数
    praised_nums = IntegerField(default=0)  #点赞数
    jtl = TextField(null=True) #结帖率
    score = IntegerField(default=0) #赏分
    status = TextField(null = True) #是否结帖或是满意
    last_answer_time = DateTimeField() #最后回复时间

class Answer(BaseModel):
    topic_id = IntegerField()
    author = TextField(null = True)
    content = TextField(default='')
    create_time = DateTimeField()
    parised_num = IntegerField(default=0)


class  Author(BaseModel):
    name = TextField(null = True)
    id = TextField(null=True)
    click_num = IntegerField(default=0)
    original_num = IntegerField(default=0) #作者的原创数目
    forward_num = IntegerField(default=0) #转发数
    rate = IntegerField(default=0) #排名
    answer_num = IntegerField(default=0) #评论数
    parised_num = IntegerField(default=0) #点赞数
    desc = TextField(null = True) #作者的个人描述，有些作者无个人描述
    industry = TextField(null = True) #作者的行业，有些作者无行业
    location = TextField(null = True)
    fans_num = IntegerField(default=0) #粉丝数
    following_num = IntegerField(default=0) #关注数

if __name__ == '__main__':
    db.create_tables([Topic,Answer,Author])
