from emotion.emotion import Emotion
import time
from emotion.tools.mails import MailsUtil
from emotion.config import cfg
from emotion.config import path
from emotion.tools.date_util import DateUtil


def get_negative(emotions_list):
    ret = []
    for e in emotions_list:
        positive = e['positive']
        negative = e['negative']
        if positive - negative < 0:
            ret.append(e)
    return ret


def get_message(emotions_list):
    message = ""
    temp = "你关注的人发布了一条疑似消极情绪的微博，消极值：%s,内容：%s;<br/>"
    for e in emotions_list:
        message += temp % (e['emotion'], e['content'])
    return message


def write_config(write_time):
    cfg.set('app', 'last_time', DateUtil.date2str(write_time))
    with open(path,'w') as f:
        cfg.write(f)

if __name__ == "__main__":
    last_time = cfg.get('app', 'last_time')
    if last_time:
        last_time = DateUtil.str2date(last_time)
    else:
        last_time = None
    emotion = Emotion(cfg.get('app', 'uid'))
    mail_util = MailsUtil()
    while True:
        new_list = []
        new_last = None
        emotions = []
        entity_list = emotion.get_entity()
        is_set_time = False
        for entity in entity_list:
            if last_time is None or entity['time'] > last_time:
                if not is_set_time:
                    new_last = entity['time']
                    is_set_time = True
                new_list.append(entity)
        if new_last:
            last_time = new_last
            write_config(new_last)
        print(last_time)
        print(new_list)
        if new_list:
            emotions = emotion.analysis(new_list)
        print(emotions)
        if emotions:
            negative_emotion = get_negative(emotions)
            msg = get_message(negative_emotion)
            mail_util.send_mail(msg)
        time.sleep(30)
