from .qcloud.textSentimentSDK import TextSentimentSDK
from urllib import request
from html.parser import HTMLParser
from .tools.date_util import DateUtil

class MyParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.processing = ''
        self.content_tag = ''
        self.time_tag = ''
        self.time_wrap = ''
        self.entity_list = []
        self.content_class = ('class', 'wgtCell_txt')
        self.time_class = ('class', 'link_d')
        self.time_wrap_class = ('class', 'wgtCell_tm')
        self.processing_content = ''
        self.time = ''
        self.is_processing_time = False
        self.is_processing_content = False
        self.start = False
        self.current_entity = {}

    def get_entity(self):
        return self.entity_list

    def handle_starttag(self, tag, attrs):
        self.processing = tag
        if self.content_class in attrs:
            self.processing_content = ''
            self.content_tag = tag
            self.start = True
            self.is_processing_content = True
        if self.time_wrap_class in attrs:
            self.time_wrap = tag
            self.is_processing_time = True

    def handle_endtag(self, tag):
        if self.content_tag == tag and self.start:
            self.is_processing_content = False
            #print(self.processing_content)
            self.current_entity['content'] = self.processing_content
        if self.time_wrap == tag and self.start:
            self.is_processing_time = False
            self.current_entity['time'] = DateUtil.analysis_data(self.time)
            self.entity_list.append(self.current_entity.copy())
            self.start = False


    def handle_charref(self, name):
        pass

    def handle_entityref(self, name):
        pass

    def handle_data(self, data):
        if self.is_processing_content:
            #print(data)
            self.processing_content = self.processing_content + data.strip()
            self.processing_content = self.processing_content.replace('\r\n', '')
        if self.is_processing_time:
            self.time = data

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        pass


class Emotion(object):

    def __init__(self, uuid=''):
        self.sdk = TextSentimentSDK()
        self.uuid = uuid
        self.weibo_service = 'http://service.weibo.com/widget/widget_blog.php?uid='
        self.url = self.weibo_service + self.uuid

    def read_html(self):
        print(self.url)
        resp = request.urlopen(self.url)
        str = resp.read()
        html = str.decode("utf8")
        return html

    def get_entity(self):
        parser = MyParser()
        html = self.read_html()
        parser.feed(html)
        entity_list = parser.get_entity()
        return entity_list

    def analysis(self, entity_list):
        for entity in entity_list:
            content = entity['content']
            time = entity['time']
            #print('时间:' + pub_time)
            #print('内容 ' + content)
            emotions = self.sdk.request_api(content)
            positive_f = float(emotions['positive'])
            negative_f = float(emotions['negative'])
            emotion = positive_f - negative_f
            entity['positive'] = positive_f
            entity['negative'] = negative_f
            entity['emotion'] = "{:.4%}".format(emotion)
        return entity_list
