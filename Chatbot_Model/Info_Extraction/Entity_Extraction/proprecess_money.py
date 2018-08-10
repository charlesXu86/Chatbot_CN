#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: proprecess_money.py
@desc: 金额提取数据预处理
@time: 2018/08/08
"""


import csv
from enum import Enum, unique
import jieba
import re

from Entity_Extraction import log

@unique
class Consts(Enum):
    BUFFER_SIZE = 100


propertyKs = ('.+金$', '.+款$', '.+费用?$', '.+险$', '.+税$','利息')
propertyKeys = ('.+金$', '.+款$', '.+费用?$', '.+险$', '.+税$', '.*损失$', '.+赔偿$', '.+利$')
adjust_src = ['律师代理费', '借款本金', '贷款本金', '欠款本金', '拖运费', '透支款本金','透支的本金','自行够药费']
adjust_dst = ['律师费', '借款', '贷款', '欠款', '托运费', '透支款','透支款','购药费']
abandon_src = ['余款', '费用', '合计', '共计', '总计', '小计', '存款', '包金', '小利','慈利', '价值款', '玉兰费']
abandon_vrb = ['扣除', '再扣除', '总计', '合计', '其中','返还']
pay_vrb = ['偿还', '赔偿', '赔付', '支付']
pay_pattern = r'在?(.*险)(范围|限额)?.*(支付|偿还|赔偿|赔付).*\d元'
abandon_pattern = r'^(合计|总计|共计|去除|除去|扣除|再扣除).*(人民币)?\d*\.?\d\d?(美|日)?元'

num_bits = (3, 5, 7, 10, 12, 14)
spe_bits = (8, 15)
bit_bits = (2, 4, 6, 9, 11, 13)


def repl_2dig(match_obj):
    result = ''
    max_bit = None
    for i in range(2, 20):
        if i in bit_bits:
            group_i = match_obj.group(i)
            if group_i is not None:
                if max_bit is None:
                    max_bit = i
                    continue
                if group_i == '零':
                    result += '0'
            else:
                if max_bit is not None and i > max_bit:
                    result += '0'

        if i in num_bits:
            if match_obj.group(i) is not None:
                result += match_obj.group(i)

        if i in spe_bits:
            if match_obj.group(i) is not None:
                result += match_obj.group(i)
                if max_bit is None:
                    max_bit = i
            elif max_bit is not None and i > max_bit:
                result += '0'

    if match_obj.group(17) is not None:
        result += ('.' + match_obj.group(17))
        if match_obj.group(19) is not None:
            result += match_obj.group(19)
    elif match_obj.group(19) is not None:
        result += ('.0' + match_obj.group(19))
    return result + '元'


def is_property(string):
    """
    判断一个字符串是否是款项类别
    :param string: 一个字符串
    :return:  如果string是以金/款/费/险结尾，或其他可能是款项类别的词语，就会返回True,否则False
    """
    for key in propertyKs:
        match = re.match(key, string)
        if match:
            return True
    return False


def belong_propery(string):
    for key in propertyKeys:
        match = re.match(key, string)
        if match:
            return True
    return False


def is_abandon(string):
    for key in abandon_vrb:
        match = re.match(key, string)
        if match:
            return key
    return None


def is_pay_vrb(string):
    for key in pay_vrb:
        search = re.search(key, string)
        if search:
            return True
    return False


def get_properties_and_values(sentence):
    """
    从一个包含金额的句子中找到对应的款项类别
    :param sentence: 待处理的原句子
    :return: 从sentence中获取到的所有Property:Value的dict
    """
    quick_get_disabled = False
    pv_dict = {}
    # search = re.search(pay_pattern, sentence)
    # if search:
    #     quick_get_disabled = True

    cut_words = jieba.lcut(sentence)
    # if is_abandon(cut_words[0]):
    #     return pv_dict

    values = re.findall(r'(人民币)?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*)(万?)(千?)(亿?)(美?日?元)', sentence)

    last_index = 0
    for j in range(len(values)):
        for i in range(len(cut_words)):
            # value[j][1]是sentence中的第j个金额数字，通过下面这个比较，将得出“金额数字”在分词结果的下标(i)
            if cut_words[i] == values[j][1]:
                v = values[j][1]
                # v3 = values[j][3]
                # v4 = values[j][4]
                if values[j][2] == '万':
                    v = v + '万'
                if values[j][2] == '亿':
                    v += '00000000'
                vrb_index = 0
                pr_index_list = []
                for k in range(1, i - last_index + 1):  # i是金额数字的下标
                    # 从金额数字前的那个词开始，到上一个金额数字的后一个词，
                    # 如果紧挨着的就是property,就立马认可，处理下一个金额数字
                    # 否则记录这些发现的property的下标
                    # 如果发现了要abandon的词，就中止对这个数字金额的处理，继续处理下一个
                    # 如果发现了赔付性动词，则记录这个动词的位置
                    word_index = i - k
                    seg = cut_words[word_index]
                    if is_property(seg):
                        if k in range(5):
                            if not quick_get_disabled:
                                pv_dict[seg] = v
                                log.p(seg)
                                break
                        else:
                            pr_index_list.append(word_index)
                            continue
                    if is_abandon(seg) and k in range(2):
                        break
                    if is_pay_vrb(seg):
                        vrb_index = word_index
                    if belong_propery(seg):
                        if len(seg) < 3:
                            if word_index - 1 > last_index:
                                log.n(cut_words[word_index - 1] + seg)
                        if word_index not in pr_index_list:
                            pr_index_list.append(word_index)
                # end for
                length = len(pr_index_list)
                if vrb_index > 0 and length > 1:
                    count = 0
                    while count < length and pr_index_list[count] > vrb_index:
                        count += 1
                    if count < length:
                        ind = pr_index_list[count]
                        p = cut_words[ind]
                        pv_dict[p] = v
                        log.p(p)
                        last_index = i
                        break
                if length > 0:
                    p = cut_words[pr_index_list[0]]
                    pv_dict[p] = v
                    log.p(p)
                break
    return pv_dict


def wash_data(string):
    """
    去除干扰：数字之间的逗号、数字间的字母、替换汉字数字成阿拉伯数字、去掉括号的内容
    :return 对原字符串清洗后的字符串
    """
    string = re.sub('(（|\()[^（）]*(）|\))', '', string)  # 去除括号括起来的部分
    string = re.sub('【[^【】]*】', '', string)  # 去除圆角中括号括起来的部分
    string = re.sub('\[[^\[\]]*\]', '', string)  # 去除中括号括起来的部分
    string = re.sub('([1-9]\d*)，(?=\d)', '\\1', string)  # 去除数字之间的的逗号
    string = re.sub('(\d)(O|o|〇)(?=\d)', '\\g<1>0', string)  # 替换数字间写错的零成：0
    # 替换汉字数字成阿拉伯数字
    string = re.sub('一|Ⅰ|壹', '1', string)
    string = re.sub('二|Ⅱ|贰', '2', string)
    string = re.sub('三|Ⅲ|叄', '3', string)
    string = re.sub('四|Ⅳ|肆', '4', string)
    string = re.sub('五|Ⅴ|伍', '5', string)
    string = re.sub('六|Ⅵ|陆', '6', string)
    string = re.sub('七|Ⅶ|柒', '7', string)
    string = re.sub('八|Ⅷ|捌', '8', string)
    string = re.sub('九|Ⅸ|玖', '9', string)
    string = re.sub('零', '0', string)
    # 处理汉字数字的进制单位
    pattern = re.compile(
            r'(?<=[^\d\.])(((\d)[千仟])?((\d)[百佰]|零)?((\d)[十拾]|零)?(\d)?万)?((\d)[千仟]|零)?((\d)[百佰]|零)?((\d)[十拾]|零)?(\d)?元零?((\d|零)角|零)?(([1-9])分)?')
    string = re.sub(pattern, repl_2dig, string)
    return string


def split_sentence(article):
    """
    切分出包含数字金额的句子,扣除
    :param article:
    :return: 将article切分，并过滤后的句子的list
    """
    raw_list = re.split('，|。|,|；', article)
    ripe_list = []
    for s in raw_list:
        search = re.search(r'(人民币)?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*)(万?)(千?)(亿?)(美?日?元)', s)
        if search:
            if re.search(abandon_pattern, s):
                continue
            ripe_list.append(s)
    return ripe_list


def adjust(p):
    p.replace('费费', '费')
    p.replace('款款', '款')
    p.replace('金金', '金')
    p.replace('险险', '险')
    p.replace('税税', '税')
    p = re.sub('1', '一', p)
    p = re.sub('2', '二', p)
    p = re.sub('3', '三', p)
    p = re.sub('4', '四', p)
    p = re.sub('5', '五', p)
    p = re.sub('6', '六', p)
    p = re.sub('7', '七', p)
    p = re.sub('8', '八', p)
    p = re.sub('9', '九', p)
    for i in range(len(adjust_src)):
        if re.search(adjust_src[i], p):
            p = adjust_dst[i]
            break
    for i in range(len(abandon_src)):
        if re.search(abandon_src[i], p):
            p = None
            break
    return p


class JIO(object):
    def __init__(self, src_file_name, dst_file_name):
        self.__srcFileName = src_file_name  # initialize input file name
        self.__dstFileName = dst_file_name  # initialize output file name
        self.__resultList = []  # an internal list to store outputs
        # jieba.load_userdict('data/dict.txt')
        with open(src_file_name) as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            for row in f_csv:  # read and manipulate every row in the csv file
                document_id = row[0]  # extract document id
                article = row[1]  # extract article
                washed_article = wash_data(article)
                sentences = split_sentence(washed_article)  # 注意：一句话内可能包含多组property和value
                p_v_dict = {}
                for sentence in sentences:
                    for (p, v) in get_properties_and_values(sentence).items():
                        log.a(document_id, p, v)
                        p = adjust(p)
                        if p is not None:
                            if p in p_v_dict:
                                if p_v_dict[p] < v:
                                    p_v_dict[p] = v
                            else:
                                p_v_dict[p] = v
                for (p, v) in p_v_dict.items():
                    self.__resultList.append((document_id, p, v))

    def write_result(self):  # 将存储结果的内部list写出到文件
        header = ('documentid', 'property', 'value')
        with open(self.__dstFileName, 'w') as w:
            r_csv = csv.writer(w, lineterminator='\n')
            r_csv.writerow(header)
            r_csv.writerows(self.__resultList)
