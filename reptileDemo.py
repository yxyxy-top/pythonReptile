# coding:utf-8
from datetime import datetime
import requests
import time
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, DateTime, SMALLINT
from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Comprehensiveexercises(Base):
    __tablename__ = 'comprehensiveexercises'
    stId = Column(Integer, primary_key=True)
    stCourseId = Column(String)
    stChapterId = Column(String)
    stTitle = Column(SMALLINT)
    stNumber = Column(Integer)
    stProblem = Column(String)
    stAnswer = Column(String)
    stCorrectAnswer = Column(String)
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    delStatus = Column(SMALLINT)


def setStTitle(stTitle):
    if stTitle == '单项选择题':
        return 1
    elif stTitle == '多项选择题':
        return 2
    elif stTitle == '判断题':
        return 3
    elif stTitle == '简答题':
        return 4
    elif stTitle == '解析题':
        return 5
    elif stTitle == '应用题':
        return 6
    pass

def comprehensiveexercisesData():

    stChapterId = 'xxxxxx'
    stCourseId = 'xxxxxx'
    address = 'xxxxxxxxxxxxxxxxxxx'
    engine = create_engine("mysql://root:123456@localhost/local?charset=utf8")
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    url = 'xxxxxxxxxxxxxxxxxxx/student/acourse/HomeworkCenter/InstantRnd.asp?CourseID='+stCourseId+'&CID='+stChapterId
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Host": "xxxxxxxxxxxxxxxxx",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.130 Safari/537.36 "
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    currentDate = datetime.now()
    for item in soup.select('#page > div.cont .st'):
        try:
            stTitle = item.select('.st_title')[0].get_text().split('、')[1].replace('\n', "")
            stContTag = item.select('.st_cont')[0]
            stNumber = stContTag.select('td[width="8"]')[0].get_text().replace("【", '').replace("】", '')
            stProblem = stContTag.select('span[class="MsoNormal"]')[0].get_text()
            stAnswer = stContTag.select('span[id="answer"]')[0].get_text().replace(' ', "").replace('答案：', "").replace(
                '\n', "").replace(' ', "")
            stTitlenum = setStTitle(stTitle)
            # 判断题型应用题答案可能为图片
            if stTitlenum == 6:
                # 是否有图片
                if len(soup.select('span[id="answer"] img')) > 0:
                    stAnswerSrc = soup.select('span[id="answer"] img')[0].get('src')
                    # 获取图片路径，保存答案为图片路径
                    if not stAnswerSrc == '' and stAnswerSrc:
                        stAnswer = address + stAnswerSrc
            comprehensiveexercises = Comprehensiveexercises(stCourseId=stCourseId, stChapterId=stChapterId, stTitle=stTitlenum, stNumber=stNumber,
                                                            stProblem=stProblem, stAnswer='', stCorrectAnswer=stAnswer,
                                                            createTime=currentDate, updateTime=currentDate, delStatus=0)
            # 根据stNumber去重判断，未保存过就添加
            if not session.query(exists().where(Comprehensiveexercises.stNumber == stNumber)).scalar():
                print(stNumber)
                session.add(comprehensiveexercises)
                session.commit()
            else:
                print('存在')
        except BaseException:
            continue
if __name__=='__main__':
    while True:
        comprehensiveexercisesData()
        time.sleep(3)