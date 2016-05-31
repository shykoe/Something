from bs4 import BeautifulSoup
from bs4 import NavigableString
import string

class parser(object):
    def __init__(self,file_id,column_id,path):
        self.text=[]
        self.soup = BeautifulSoup(open(path,'r',encoding='gb2312',errors='ignore'),"html5lib")
        self.keywords = self.soup.find('meta',attrs={"name":"keywords"})['content']
        self.des = self.soup.find('meta',attrs={"name":"description"})['content'].replace('\n','')
        self.content = self.soup.find('div',attrs={"class":"neirbox3"})


        # self.content.find('div',attrs={"class":"wz_a"}).decompose()
        # for child in self.content.children:
        #     if(hasattr(child,'prettify')):
        #         self.text.append(child.prettify())
        #     else:
        #         temp = str(child).replace('\t','').replace(' ','')
        #         self.text.append(temp)
        self.title = self.soup.select(".neirbox > h1")[0].text
        self.file_id = file_id
        self.column_id = column_id
    def deal_text(self):
        for child in self.content.children:
            if not isinstance(child,NavigableString):
                self.text.append(child)
        # for child in self.content.children:
        #     if not isinstance(child,NavigableString):
        #         if child.has_attr('class') and ('conbot' in child['class']):
        #             break
        #         else:
        #             self.text.append(child)
        #     else:
        #         continue
        # self.text = self.text[1:-1]
        self.text = ''.join(list(map(lambda x : x.span.wrap(self.soup.new_tag("p")).prettify().replace('\n','　') if len(x.get_text()) > 5 else '',self.text)))
    def to_sql(self):
        self.deal_text()
        self.sql_1 = "insert IGNORE into `dede_addonarticle` (`aid`,`typeid`,`body`) values('%d','%d','%s')" %(self.file_id,self.column_id,self.text)
        self.sql_2 = "insert IGNORE into `dede_archives` (`id`,`typeid`,`sortrank`,`title`,`writer`,`source`,`pubdate`,`senddate`,`mid`,`keywords`,`notpost`,`description`,`dutyadmin`,`weight`) values ('%d','%d','1463550000','%s','佚名','未知','1463550000','1463550000','1','%s','1','%s','1','100')"%(self.file_id,self.column_id,self.title,self.keywords,self.des)
        self.sql_3 = "insert IGNORE into `dede_arctiny` (`id`,`typeid`,`channel`,`senddate`,`sortrank`,`mid`) VALUES('%d','%d','1','1463550000','1463550000','1')" %(self.file_id,self.column_id)
        

if __name__ =='__main__':
    ss=[]
    pas = parser(458, 11, '.\\by\\458.html')
   

    pas.to_sql()
    f = open('test.sql','w+',encoding='utf-8')
    f.write(pas.sql_1+';\n')
    f.write(pas.sql_2+';\n')
    f.write(pas.sql_3+';\n')
    f.close()
