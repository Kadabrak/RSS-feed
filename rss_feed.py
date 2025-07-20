import http.client
import ssl
import os
directory = ""

class Rss_Feed:
    def __init__(self, media_link,file):
        self.connection = http.client.HTTPSConnection(media_link, 443)
        self.connection.request("GET","/"+file)
        self.connection_response = self.connection.getresponse()
        self.all_articles_infos = []
        if self.connection_response.status == 200:
            self.rss_data = str(self.connection_response.read().decode('utf-8'))
            print(f'connection to {media_link} success')
            while 1:
                article_raw_info = self.get_items()
                if article_raw_info != False:
                    article_info = Article(article_raw_info,('title','description','pubDate','dc:creator','link'))
                    self.all_articles_infos.append(article_info.get_article_infos())
                else:
                    break
                
        else:
            print(self.connection_response.status)

    def get_articles_infos(self):
        return self.all_articles_infos
    def get_items(self):
        """
        Get article in the Rss file
        """
        try:
            item_start = '<item>'
            item_end = '</item>'
            article = self.rss_data[self.rss_data.index(item_start):self.rss_data.index(item_end)+len(item_end)]
            self.rss_data = self.rss_data.replace(article,'')
            return article
        except ValueError:
            return False
    
        

class Article:
    def __init__(self,raw_infos,separators):
        """
        !!! Don't forget to put the serators !!!
        """
        self.all_text = raw_infos
        self.all_article_values = {}
        for i in separators:
            self.all_article_values[i] = self.get_the_info(i,[])
    def get_article_infos(self):
        return self.all_article_values
    def get_the_info(self,separator,all_infos=[]):
        """
        Return a list of all infos in link with the separator 
        """
        try:
            separator_start = '<'+separator+'>'
            separator_end = '</'+separator+'>'
            category = self.all_text[(self.all_text.index(separator_start)):self.all_text.index(separator_end)+len(separator_end)]
            all_infos.append(category[len(separator_start):(len(separator_end)*-1)])
            self.all_text = self.all_text.replace(category,'')
            self.get_the_info(separator,all_infos)
        except ValueError:
            pass
        return all_infos
    
def directory_exist(name):
    try:
        os.listdir(name)
    except FileNotFoundError:
        os.mkdir(str(name))
            
with open('rss_flux.txt',"r") as all_rss_flux_links:
    for i in all_rss_flux_links.readlines():
        file = i.strip().split('/',1)[1]
        link = i.strip().split('/',1)[0]
        directory_exist(link)
        for k,i in enumerate(Rss_Feed(link,file).get_articles_infos()):
            with open(link+"/"+(str(k)+"t.txt"),'w', encoding="utf-8") as file:
                for separators,value in i.items():
                    for j in value:
                        file.write(separators+': '+j+'\n')
            file.close()
        

