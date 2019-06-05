#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: predict.py
@desc: fasttext文本分类预测，加载模型，测试
@time: 2019/05/23
"""

import tensorflow as tf

from Chatbot_Model.Text_Classification.Fasttext.parameters import parameters
from Chatbot_Model.Text_Classification.Fasttext.data_helper import load_json, padding


class Predict():
    def __init__(self, config=parameters, model='/Users/charlesxu/PycharmProjects/Chatbot_CN/Chatbot_Model/Text_Classification/Fasttext/runs/1559647511/', word_to_index='/Users/charlesxu/PycharmProjects/Chatbot_CN/Chatbot_Model/Text_Classification/Fasttext/vocabs/word_to_index.json',
                 index_to_label='/Users/charlesxu/PycharmProjects/Chatbot_CN/Chatbot_Model/Text_Classification/Fasttext/vocabs/index_to_label.json'):
        self.word_to_index = load_json(word_to_index)
        self.index_to_label = load_json(index_to_label)

        graph = tf.Graph()
        with graph.as_default():
            session_conf = tf.ConfigProto(
                allow_soft_placement=config['allow_soft_placement'],
                log_device_placement=config['log_device_placement'])
            self.sess = tf.Session(config=session_conf)
            with self.sess.as_default():
                # Load the saved meta graph and restore variables

                tf.saved_model.loader.load(self.sess, ['tag_string'],model)

                # Get the placeholders from the graph by name
                self.input_x = graph.get_operation_by_name("input_x").outputs[0]

                self.dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

                # Tensors we want to evaluate
                self.predictions = graph.get_operation_by_name("output/predictions").outputs[0]

    def fc_predicts(self, msg):
        input_x = padding(msg, None, parameters, self.word_to_index, None)
        feed_dict = {
            self.input_x: input_x,
            self.dropout_keep_prob: 1.0
        }
        predictions = self.sess.run(self.predictions, feed_dict=feed_dict)
        return [self.index_to_label[str(predictions[0])]]


# if __name__ == '__main__':
#     prediction = Predict(config)
#     result = prediction.predict(
#         ["""黄蜂vs湖人首发：科比带伤战保罗 加索尔救赎之战 新浪体育讯北京时间4月27日，NBA季后赛首轮洛杉矶湖人主场迎战新奥尔良黄蜂，此前的比赛中，双方战成2-2平，因此本场比赛对于两支球队来说都非常重要，赛前双方也公布了首发阵容：湖人队：费舍尔、科比、阿泰斯特、加索尔、拜纳姆黄蜂队：保罗、贝里内利、阿里扎、兰德里、奥卡福[新浪NBA官方微博][新浪NBA湖人新闻动态微博][新浪NBA专题][黄蜂vs湖人图文直播室](新浪体育)""",
#          """上投摩根投资总监孙延群病休基金经理“过劳症”公开第一例：曹元“3月20日还见到他(孙延群)在一个颁奖活动上发言，没想到这么快就申请病休了。”上海一基金公司的人士看到上投摩根基金管理公司(下称上投摩根)的公告感叹着。3月25日，上投摩根基金管理有限公司公告称，投资总监孙延群先生由于健康原因需要治疗，上投摩根根据有关法规和公司制度批准孙延群先生5个月假期的申请，孙延群将因病休养至2009年8月，在此期间孙延群先生暂停履行基金经理职务。实际上，这也是基金业基金经理暂时离职而发信息披露的第一案。而此前，有许多基金经理或因出国留学、或因其他事务暂离工作岗位数月均未见向公众披露。按照现行规定，只要不是离职这些信息不需对外披露。上投摩根此番做法客观上是积极响应即将实施的信息披露新规中的相关条例。“过劳症”公开第一例孙延群2005年加入上投摩根并随后担任阿尔法股票基金经理，在吕俊辞职上投摩根后，他接任该公司投资总监。在上文提及的颁奖活动上，孙虽然双鬓发白，但看起来较有神采，因此外界对孙的突然发病感到吃惊。上投摩根的一纸公告并未披露孙延群患何疾病。该公司市场部人士称因为是孙个人隐私，不便于对外披露。但有知情人透露一个细节，孙去年就因胃病去过医院，他推测孙此次病休可能是因为旧病重犯。实际上，胃病在基金公司投资管理人员并不鲜见。深圳某合资基金公司投资总监介绍，基金投研人员的工作非常不规律，尤其是近期上市公司年报高发期，投研人员没有不加班的。而他本人也是常常半夜收到研究员的上市公司报告。他称，吃饭不规律、休息不充分导致胃病成为这个行业的“职业病”。“这也是这个行业的压力所致。”他补充到。参加3月20日理柏中国基金奖的人士还记得孙延群在会上说过这么一句话：“投资者的信任这也使我们倍感压力。”现在看来，孙的这句话不是套话。事实上基金的投研面临的压力还有多种。2008年，股市遭遇系统性风险，基金公司和其投研人员感受到了从天堂到地狱的极端变化。深圳一位基金经理描述道，2008年春节回家，当亲戚得知他是基金经理赶紧凑过来问东问西；而2009年回家，这种待遇消失了反而开起了近乎讽刺的玩笑。在网络上，投资者对基金经理的失望乃至谩骂也处处可见。这种近乎一边倒的社会舆论直接对基金经理产生压力。另一方面，每年的排名之争直接决定着基金经理在基金持有人心目中的地位；而内部的业绩考核亦决定基金投研人员的职业前景。在舞动数十亿乃至数百亿元资金的同时，伴随的是各方给予的压力。据另一基金公司人士介绍，除了胃病，基金从业人员还常伴有颈椎方面的疾病以及“三高”疾病。对于基金持有者而言，好的消息是大多基金公司建立了比较系统性的投研体系，个别人的暂时离职不会对基金的投资策略带来重大影响。现在基金公司多实行投资决策委员会作为投资策略的决策机构，投资决策由集体智慧产生，而非个人。而基金经理在选择个股和仓位的权利被削弱。不好的一方面是同一基金公司相同类型的基金策略相近，缺乏特色；好的一方面则是投资风险降低，亦不会因人员变动给基金业绩带来太大冲击。还有些公司实行双基金经理制度，这进一步避免了个别投研人员流动带来的风险。基金经理动态更透明行业内，关于基金经理的信息披露中，常以基金经理变动居多，此次孙延群暂时离开工作岗位也进行信息披露尚属行业内首次。这表明基金信息披露更加“阳光”透明。关于基金投研人员的信息披露规定最早的文件是1999年颁布的《证券投资基金信息披露指引》(下称《指引》)，该《指引》于当年3月10日披露之日起实施。这纸《指引》共计16条，3000言，附带4条附件，形成了基金公司信息披露的基础框架。但该指引对基金经理的信息披露规定较为简单。其中第十二条指出基金发生重大事件，有关信息披露义务人应当于第一时间报告中国证监会，并编制临时报告书，经上市的证券交易所核准后予以公告，同时报中国证监会。该条例认为基金管理人的董事长、总经理、基金托管部的总经理变动属于重大事项。不足的是，《指引》中并没有详细规定投资管理人(其中包括基金经理)发生变动需要公告。直至2004年7月1日，《证券投资基金信息披露管理办法》(下称《办法》)正式出台，首次将基金经理的变动规定要做信息披露。《办法》全文共计8章、38条、4900字，较《指引》详实许多。该《办法》也首次规范基金经理的信息披露。其中第二十三条规定，基金发生重大事件，有关信息披露义务人应当在两日内编制临时报告书，予以公告，并在公开披露日分别报中国证监会和基金管理人主要办公场所所在地中国证监会派出机构备案。其中基金管理人的董事长、总经理及其他高级管理人员、基金经理和基金托管人基金托管部门负责人发生变动属于重大事项。但是，《办法》并未对基金高管暂时离开的情况进行规范。事实上，这种情况在基金业中一直存在，甚至发生在一些明星基金经理的身上。比如北京某大型基金公司明星基金经理曾在2002-2003年出国充电，公司未予披露；又有中邮基金投资总监彭旭去年出国半年，亦未见正式披露。2007年10月，彭在接受本报采访时曾说，“等我哪一天去学习了，我一定对外披露。但现在一切要以公告为准。”事实证明，没有制度约束，口头承诺也成一纸空文。3月25日上投摩根披露投资总监孙延群休假5个月在业内算是首创。业内认为，上投摩根首开先例也是为了主动迎合了即将于4月1日实施的基金业信息披露新规。今年3月17日，证监会发布修订后的《基金管理公司投资管理人员管理指导意见》(下称意见)，该意见自2009年4月1日起施行。《意见》第三十六条明确规定：投资管理人员“拟离开工作岗位1个月以上”，督察长应当在知悉该信息之日起3个工作日内，向中国证监会相关派出机构报告。《意见》中也明确说明“投资管理人员”是指公司负责基金投资、研究、交易的人员以及实际履行相应职责的人员，涵盖了基金经理和投资总监。
# """])
#     print(result)
