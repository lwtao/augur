from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *

engine = create_engine('mysql+pymysql://root:@172.21.104.241/augur?charset=utf8')
DBSession = sessionmaker(bind=engine)


def query_stock_hist(stock_code, ktype, start_date):
    session = DBSession()
    result = session.query(StockHist).filter(StockHist.ktype == ktype, StockHist.code == stock_code,
                                             StockHist.date > start_date).order_by('date').all()
    session.close()
    return result


def query_limit_up_stocks():
    session = DBSession()
    sql = '''
SELECT 
  t4.code
FROM
  hist_data t4 
  JOIN 
    (SELECT 
      MAX(DATE) DATE,
      CODE 
    FROM
      hist_data t3 
    WHERE `ktype` = 'D' 
    GROUP BY CODE) t5 
    ON t4.code = t5.code 
    AND t4.date = t5.date 
  JOIN 
    (SELECT 
      t1.code,
      t1.high 
    FROM
      hist_data t1 
      JOIN 
        (SELECT 
          CODE,
          MIN(DATE) DATE 
        FROM
          hist_data t 
        WHERE t.p_change >= 9.9 
          AND t.`ktype` = 'D' 
          AND t.date > DATE_FORMAT(
            DATE_SUB(NOW(), INTERVAL 3 MONTH),
            '%Y-%m-%d'
          ) 
        GROUP BY CODE 
        HAVING COUNT(1) BETWEEN 1 
          AND 4) t2 
        ON t1.code = t2.code 
        AND t1.date = t2.date 
    WHERE t1.`ktype` = 'D') t6 
    ON t4.code = t6.code 
WHERE t4.`ktype` = 'D' 
  AND t4.high < t6.high ;
    '''
    result = session.execute(sql)
    session.close()
    return [row['code'] for row in result]

def query_deal_date_more_than_250(codes):
    codes_in_str = ''
    for i,code in enumerate(codes):
        if i == 0:
            codes_in_str = code
        else:
            codes_in_str = codes_in_str + ',' + code
    sql = 'SELECT code FROM hist_data where code in(' + codes_in_str +') and ktype=\'d\' GROUP BY code HAVING count(1)>250;'
    session = DBSession()
    result = session.execute(sql)
    session.close()
    return [row['code'] for row in result]

def query_all_stocks():
    session = DBSession()
    sql = '''
SELECT 
  DISTINCT code
FROM
  hist_data ;
    '''
    result = session.execute(sql)
    session.close()
    return [row['code'] for row in result]

# print(query_deal_date_more(['600111','002282','600777']))
# print(len(query_limit_up_stocks()))
