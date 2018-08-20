#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: get_location.py
@desc: 利用正则匹配提取地址
@time: 2018/08/08
"""



import re


def get_add(judge_res):
    addr = ''
    pattern1 = re.compile(
        r'.*(坐落于|坐落位置？|坐落在|位于|名下的?|所有的?)(.*?)(幢?|栋?|室?|号?|层?|单元?|店面?)(住房|住宅|营业场所|写字楼|商品房|房地产|的?不动产|使用权|土地|公寓|办公楼?|门面房?|商铺|楼房|仓库|工业用地|工业厂房|承包地|商住楼|车库|车位|亩).*?')
    match_addr1 = re.search(pattern1, judge_res)
    match_addr2 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?室)',judge_res)
    # match_addr2 = re.search(r'(坐落于|坐落在|位于|名下的|所有的)(.*?)(.*?室)', judge_res)
    match_addr3 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?号)(.*?村)(.*?区)(.*?楼)(.*?单元)', judge_res)
    match_addr4 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?号)(.*?层)(.*?座)', judge_res)
    match_addr5 = re.search(r'(坐落于|坐落在|坐落位置？|位于|名下的?|所有的?)(.*?房)(.*?楼)(.*?层)',judge_res)
    match_addr6 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?栋)',judge_res)
    match_addr7 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?房屋)',judge_res)
    match_addr8 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?店)',judge_res)
    match_addr9 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?号楼)(.*?单元)(.*?楼)(.*?户)', judge_res)
    # match_addr9 = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?号)', judge_res)

    if (match_addr1):
        addr = match_addr1.groups(2)

        # return match_addr1.groups(2)
    if (match_addr2):
        addr = match_addr2.groups(2)
        # return match_addr2.group(2)
    if (match_addr3):
        addr = match_addr3.groups(5)
        # return match_addr3.groups(5)
    if (match_addr4):
        addr = match_addr4.groups(3)
        # return match_addr4.groups(3)
    if (match_addr5):
        addr = match_addr5.groups(3)
        # return match_addr5.groups(3)
    if (match_addr6):
        addr = match_addr6.group(2)
        # return match_addr6.group(2)
    if (match_addr7 ):
        addr = match_addr7.groups(2)
        # return match_addr7.group(2)
    if (match_addr8):
        addr = match_addr8.groups(4)
        # return match_addr8.groups(4)
    if (match_addr9):
        addr = match_addr9.group(2)
        # return match_addr8.groups(2)
    if addr is not None:
        af_text = wash_LOC(addr)
        LOC_RES = cut_addr(af_text)
    else:
        LOC_RES = ''

    # match_addr = re.search(r'(坐落于|坐落在|位于|名下的?|所有的?)(.*?号)(.*?村)(.*?区)(.*?楼)(.*?单元)(.*?号)(.*?层)(.*?座)(.*?房)(.*?楼)(.*?层)(.*?栋)(.*?店)(.*?号楼)(.*?单元)(.*?楼)(.*?户)',judge_res)
    # af_text = match_addr.groups()

    return LOC_RES

def cut_addr(text):
    '''
    :param text:
    :return:
    '''
    # cut_list = ['坐落于', '坐落位置', '坐落在', '位于', '名下的', '所有的']
    s_loc = []  # 存放处理后的单个地址
    str_text = text[0]
    pattern = re.compile(r'(.*?坐落于|.*?坐落位置|.*?坐落在|.*?位于|.*?名下的|.*?所有的)')
    try:
        match = re.search(pattern, str_text).group(0)
        if match is not None:
            loc = str_text.strip(match)
            s_loc.append(loc)
        else:
            s_loc = text
    except:
        pass
    return s_loc

def wash_LOC(addr):
    '''
    将正则匹配的地址合并，并且去掉不需要的部分
    :param tuple:
    :return:
    '''
    # cut_text = get_add(t)
    af_text = ''  # 用来存储提取后的合并的地址信息
    addr_list = []
    for i in range(len(addr)):
        txt = addr[i]
        af_text += txt
    addr_list.append(af_text)
    # loc = cut_add(af_text)

    return addr_list

if __name__ == '__main__':
    # str = "被执行人名下位于我市潘集区珠江路北侧泰府名郡小区20栋101至112、201至212房产予以查封（扣押）"
    # str = "对被告窦永宗所有的位于芜湖市镜湖区天和苑X幢XXX室予以查封"
    # str = "（遂昌县妙街道北街13弄177号54室）,位于昆山开发区XX广场XX号楼XX室,"
    # str = "房屋坐落于沈阳市铁西区北一西路37-15号2-3-2,遂昌县妙街道北街13弄177号54室"
    # str = "位于哈尔滨市道外区景阳街178号3层F座拍卖"
    # str = "青阳县杨田镇农贸市场5#商住楼,将坐落于崇明县星村公路XXX弄XXX号XXXX养殖场编号为A42—A44、B40—B42共计71.77亩鱼塘"
    # str = "2008年6月16日凌晨1时30分左右，受害人唐勇路过沱江旱冰场门口时，被几名男子持刀威胁，抢走唐身上现金110元。"
    # str = "被告冯亮亮名下位于东莞市南城区西平村金地格林花园碧桐院6座202号）变卖"
    # str = "若被告温州市金钻国际贸易有限公司未按期履行上述第一项条款中的债务，则依法拍卖、变卖被告夏薇华提供抵押的坐落于温州市鹿城区矮凳桥××号××幢205室、209室的房屋（房屋所有权证号分别为：××、××），所得价款由原告中国工商银行股份有限公司温州城西支行优先受偿，但其对包括本案债务在内的2011年城西抵字0513号《最高额抵押合同》项下所有主债务的优先受偿总额以321.8万元为限；"
    str = "被告宁夏隆安房地产开发有限公司于本判决生效后十日内，按照合同约定的交付条件向原告冯利强交付位于银川市金凤区房屋；"
    # str = "房屋位于郎溪县十字镇零点商业街1幢6单元512室"
    # str = "位于长沙市韶山路162号018栋101房（长房权证天心字第713051588号）"
    # str = "即位于湖南省长沙市开福区福元西路99号珠江花城一期二组团11栋101房拍卖,坐落位置：冠亚星城A16号楼东单元8层东户；面积：161.1平方米）"
    # str = "位于福州市鼓楼区水部街道六一中路28号佳盛广场A、B、C座连体4层整层，权属证书及编号：榕房权证R字第1156232号）,"
    # str = "位于县城兆兴花城30号楼2单元2楼西户单元房一套归被告所有，被告给付原告应得份额119272.5元，该房屋剩余的银行按揭贷款76329.9元由被告负责偿还。三、驳回原告的其他诉讼请求。案件受理费300元，"
    # str =  "将原属被执行人黄华润所有的坐落于福州市晋安区岳峰镇连江北路116号二化新村三区5#楼301单元作价1100813元时起转移；"
           # "位于江东路136号阳光城世纪广场办公楼B#楼18层13办公楼（YR1308058）及坐落于福州市马尾区马尾镇儒江东路136号阳"
           # "、泊位一个3200㎡、二层综合楼1121.4㎡、伙房及餐厅174.72㎡、锅炉房29㎡、大门一个（保全标的额270万元）,坐落于黑龙江省依安县中世纪雅苑小区6号楼15号车库" \
           # "位于鸣凤镇花园村9组（原季家村4组）“肖家湾”的13亩林地,位于钦州市河东工业园区小江工业园明月园3#3栋内,位于临河区利民西街（欧式街）杨虎烧烤店门头下面通道的玻璃门" \
           # "位于靖江市新桥镇三太村十组下节的2.13亩承包地,位于双辽市辽南街华申理想城邦花园小区18号楼1层1807A室," \
           # "位于玉林市华商国际E区29栋B单元402号房,名下位于海口市金融贸易区富南公寓X幢XXX房,位于汕头市澄海区盐鸿镇建民桥工业区房地产,位于翠屏区建设路131-133号1层营业用房" \
           # "位于南宁市江南区白沙大道19号金湾花城19号楼3单元1层3—101号房的查封,位于石家庄市鹿泉区获鹿镇龙海花园24栋1单元603室房及地下室,名下位于融信.幸福海岸A子地块地下室地下一层B45号," \
           # "除位于广州市花都区新雅街新村雅新南街57号的花基泥地,龙游县龙洲街道县学街3号平房一间,位于儋州市排浦镇黑石村委会镇远村6.72亩" \
           # "名下位于新乡市牧野大道金色奥园F7号楼1单元1101室"
    # str = "所有的位于浙江省杭州市江干区景芳五区39幢201室"
    result = get_add(str)
    print(result)

    # 测试cut_addr
    # acc_addr = cut_addr(str)
    # print(acc_addr)


dict1 = {'address': None, 'value': None, 'name': '翟成应于本判决生效之日起二十日内向原告信阳市燃料公司返还'}
dict2 = {'address': '信阳市平桥区平中大道东段信阳市燃料公司平桥货场三角高站台处的'}


