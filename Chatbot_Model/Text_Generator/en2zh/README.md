# 中英机器文本翻译

评测中英文本机器翻译的能力。机器翻译语言方向为中文到英文。


## 依赖

- Python 3.5
- PyTorch 0.4

## 数据集

我们使用AI Challenger 2017中的英中机器文本翻译数据集，超过1000万的英中对照的句子对作为数据集合。其中，训练集合占据绝大部分，验证集合8000对，测试集A 8000条，测试集B 8000条。

可以从这里下载：[英中翻译数据集](https://challenger.ai/datasets/translation)

![image](https://github.com/foamliu/Machine-Translation-v2/raw/master/images/dataset.png)

## 用法

### 数据预处理
提取训练和验证样本：
```bash
$ extract.py
$ python pre_process.py
```

### 训练
```bash
$ python train.py
```


### Demo
下载 [预训练模型](https://github.com/foamliu/Machine-Translation-v2/releases/download/v1.0/BEST_checkpoint.tar) 放在 models 目录然后执行:

```bash
$ python demo.py
```

<pre>
> 我们总是记得我们写下来的。
= we remember what we record .
< we always remember what we wrote it .
> 女士们先生们，我，
= ladies and gentlemen i
< and i ladies and gentlemen
> 不需要告诉任何人。
= we do n t have to tell anyone .
< nobody s gon na tell .
> 我不舒服，由于我很聪明。
= i m sick . because i m smart .
< i m m i i m m smart .
> 我没事。抓住她！
= i m fine . get her !
< i m . get her !
> 相信你一定可以找到的。
= i m sure you ll find it soon .
< trust that you can can . .
> 我们打了一架。他赢了。
= we fought . he won .
< we fought a fight . he won .
> 所以你会朝那边走？
= so do we just go that way ?
< so you re going go that way ?
> 你说真的？- 真的吗？
= are you serious ? really ?
< you serious ? really ?
> 我们有8个月时间。
= we had eight months .
< we ve eight eight months .

> 我在你房子前面了！
= i m outside your house !
< i ve in front of your house !
> 总之，我们得多呆上一个礼拜
= anyway we will stay a week more
< well anyway we have a a a week
> 孩子我很好。
= i m fine son .
< boy i m fine .
> 我已经尽力了，真的？
= i have tried have i not ?
< i ve done my best . really ?
> 但别碰我的脸。
= just do n t touch the face .
< but not my face .
> 不会有错？不会
= are you correct on this ? i m correct
< it s be ? ? no no
> 孩子们回来了吗？
= are the kids back yet ?
< the kids come back ?
> 显然你刚写的那张
= apparently the check you wrote them
< it s obvious you you wrote wrote
> 我们需要点蓝色。
= we need some blue .
< we re gon na need some .
> 听好了。不。不！
= just listen to reason . no . no !
< listen to me . no no no !

> 但别碰我的脸。
= just do n t touch the face .
< but not my face .
> 我想要告诉你们，比如，呃，
= i m telling you like um
< i wanted to tell you guys
> 另一天。真的？
= another night . really ?
< another day . really ?
> 我面临着失业。- 你？
= i m getting laid off . you ?
< i ve got the unemployment . you ? ?
> 我有。很好。
= i have it . good .
< i am . good .
> 我们能够开始我们的生活。
= we can start our lives .
< and we can begin to live our lives .
> 我要把这件衣服当成是
= i have to approach it as if i was
< i want to take this dress
> 我们见过这样的案例，
= we have seen cases like this
< we ve ve seen cases like this
> 希望你也能参加。
= so i hope you ll be there .
< i wish you to to . .
> 我对时尚不是很在行
= i m not big on fashion .
< i am very in in fashion fashion

> 就像你耳朵一样有趣
= just as funny as your ear
< it s as funny as you ears
> 咱最好让她喝点咖啡。
= we better get her some coffee .
< we d better let her drink .
> 关掉手机不就没这事了。
= just turn your damn phone off .
< no phones no phone phones off .
> 你想要怎样就说吧。
= just tell us what you want .
< you can what you you . . .
> 不好意思。难道你...
= i m sorry . is there a a . . .
< excuse me . but are you . . .
> 我们无法确认车辆，
= we ca n t make the vehicle from here
< we we ca n t confirm cars cars cars
> 你得保证给我拿回来…
= just make sure i get it back . . .
< you got to to that it . . .
> 我们就没法得到治疗了？
= we just wo n t get the treatment ?
< when we can get get in ?
> 我是个奴隶，好吗。
= i m a slave alright .
< i am a slave okay .
> 冷静点，宝贝，冷静点。
= keep calm sweetie . keep calm .
< cool it baby . easy .

> 她有什么家人或朋友吗？
= we have any family or friends ?
< does she have any family or friends ?
> 我准备要行动了。
= i m gon na make my move .
< i am ready to to . .
> 有没有想过他可能呆在哪？
= any idea where he might be staying ?
< ever ever thought where he d been ?
> 我不否认你说的。
= i m not saying that s not true .
< i wo n t deny you .
> 我们已经和这家伙谈过了。
= we already talked to this guy .
< we ve already talked to this guy .
> 又疯又累，
= i m mad and a whole lot tired
< and crazy tired tired tired
> 你今晚要唱什么？
= i m going to sing alone by heart .
< so what are you gon na sing tonight ?
> 不会的- 不你过来看看。
= oh come on . no you come on .
< no no n t you come here . . .
> 在附近走的时候，要注意。
= keep your eyes open down there .
< when you re close .
> 他想我上他的车。
= he wanted to go to his car .
< he s gon na fuck his car .

> 我在经历一场痛苦的离婚。
= i m going through a terrible divorce .
< i m through a rough divorce .
> 很高兴为你服务，小公主。
= at your service little princess .
< it s nice to you you . princess .
> 我听到你说的了。
= i heard what you said .
< i i hear what you . .
> 我肯定你不会的。
= i m sure you wo n t .
< i sure bet you would n t .
> 我们对她却一无所知。
= we know nothing about her .
< and we do n t know anything about her .
> 我是疯了！因为你！
= i m going insane ! because of you !
< i am crazy ! because of you !
> 我很喜欢我们的会议
= i have so much enjoyed our meetings
< i love enjoyed our meetings
> 只是稍微感到惊讶
= i m a little surprised to see you
< it s just a little bit surprised
> 另一个世界便展现在人们面前。
= another world is revealed .
< the other world in front in people people .
> 明天我们可能都会分开，
= we might all be split tomorrow
< we ll be in be

> 孩子呢？孩子？
= kids ? kids ?
< and the baby ? baby ?
> 得行动了。
= we got to move on this .
< we should get moving .
> 我等不到今晚了！
= oh i ca n t wait for tonight !
< i ca n t wait tonight !
> 四个小组正在寻找。
= we have four teams working on it .
< four team are looking for . .
> 只是我自己，警官。
= oh it s just me officer .
< it s just sir .
> 我可终于见着你了
= at last i see you
< i finally have see you in
> 在告诉其他伙计之前，
= as we told the other guys before
< tell me anyone else
> 是啊，我明白我知道。
= yeah i hear you . i know .
< yeah i i i i that .
> 你不是退休了吗？
= are n t you retired ?
< you retired you retired ?
> 我罪名成立，甜心。
= i m guilty as charged sweetheart .
< i would do that . .

> 快停下！叫保安！
= knock it off now ! call security !
< stop ! call security security ! !
> 我们应该建议他改变一下策略。
= we could suggest a change in strategy .
< we should have him changing his strategy .
> 再见了阳光
= gone their sun
< see you see the good the
> 今晚还想做什么？
= so anything else you want to do tonight ?
< what are you want tonight tonight tonight ?
> 当然，除了你的工作。
= apart from your work of course .
< except besides your job .
> 我要提升你。你要什么？
= i m promoting you . you re what ?
< i want you . what want want ?
> 我看到一些东西-.
= i m seeing things .
< i saw something .
> 别担心我，兄弟。
= do n t worry about me bro .
< do n t worry buddy .
> 再睡会儿……。
= sleep on . . .
< get some sleep . . .
> 孩子们，看谁来了。
= kids look who s here .
< boys we re who we are .

> 我不清楚你在指什么。
= i m not sure what you re suggesting .
< i do n t know what you re talking .
> 我很有兴趣看下医院。
= i m so interested to see the hospital .
< i got to to to to hospital hospital .
> 你能应付吧？
= are you handling it okay ?
< can you handle it ?
> 我没说你读了它。
= i m not saying you read it .
< i never said you read it .
> 所以要没问题了。
= so having to take no question .
< so we re gon na do it .
> 乖乖地等着吧。操！
= just wait . fuck !
< stay tight . . . fuck fuck
> 不管怎样，反正都结束了。
= anyway it s over .
< either way it s over anyway .
> 我们甚至不知道这里是哪儿。
= we do n t even know where here is .
< we even did n t know where .
> 就像我们一家人都在一起一样。
= felt like we were together as a family .
< like we family we we together .
> 噢，艾伦，我-
= oh alien i
< oh the uh i

> 你自己付钱嘛。
= just pay for it yourself .
< you pay for it for yourself .
> 我们找到她了。她没事。
= we have her . she s okay .
< we ve got her . she s fine .
> 临床心理学教授。
= at a certain northern university .
< clinical psychology professor .
> 我讨厌夜晚。
= i hate the nights .
< and i hate the night .
> 坐在办公室盯着电话时，
= sitting watching the phone at the office
< sat at the office at at
> 我们救他出来了。
= we got him out of there .
< we we got him .
> 我刚好是她的
= i happened to be her
< i i the her
> 喔，约翰，不该是你呀！
= oh john not you !
< oh no john you should be !
> 他想要回他的杂志。
= he wants his magazine back .
< he was going back to his magazine .
> 但愿我也能这么说。
= oh i wish i could say that same .
< i wish i could the same .

> 我给你抓一张照片。
= i m shooting you pictures right now .
< i ll take a photograph .
> 我是在改进你的技巧。
= i m improving your technique .
< i was making your technique .
> 所以我得马上扔掉
= so i ll have to throw them out
< and i need to throw away away away
> 我好害怕。我好害怕。
= i m scared . i m so scared .
< i m scared . i m so scared .
> 我去厕所你也跟着啊？
= are you following me in the bathroom ?
< should i go to the the the ? ?
> 就像你杀教授那样吗。
= just like you did the professor .
< like you killed killing professor .
> 你开始明白了吗？
= are you starting to get the picture ?
< you you to ? ?
> 好，我应该有。
= yeah i ought to have something .
< okay i i have . .
> 你们初步调查的结果。
= of your preliminary search .
< you investigation your investigation investigation .
> 因此我和他争吵，不是我。
= so argue with him not me .
< so was arguing with me .

> 我对纸做了碳14分析。
= so i had the paper carbon tested .
< i did it right analysis .
> 所以要很小心。我们走。
= so be careful . let s go .
< so be careful . let s go .
> 你们两个，是在约会吗
= are you two like going together ?
< you guys are dating
> 我就你一个孩子。
= i have just got one child .
< and i m your only kid .
> 我马上就处理完，
= i m gon na finish up
< i will finish in this
> 你我之前从没有过交谈。
= we never really talked before .
< i ve never been been before before before .
> 宝贝，好好唱。
= yeah baby work it out .
< baby just sing .
> 哦，不！该死！
= oh no ! shit !
< oh no ! damn it !
> 所以，回家去吧…
= so go home . . .
< so go home .
> 就像这样... 很简单。
= just like this . . . very simple .
< it s . . . it s .

> 我可啥都没说。
= i m not saying a word .
< i did n t say anything .
> 我认识他儿子，嗯...
= knowing this kid uh . . .
< i know his son and uh . . .
> 我没有经验，
= i have no experience
< i do n t have any experience
> 哦，也没有了。
= oh lost .
< oh there s no .
> 啊，我是说太糟了。
= oh i i mean it s bad .
< ah i mean that s too bad .
> 就在我们关注。
= as we wait to hear the fate .
< it s we . .
> 我们会赢的。就是嘛！
= we can win this . yeah !
< we ll win . it it ! !
> 得找你谈谈又是家庭会议？
= we need to talk . another family meeting ?
< you re a family after a meeting ?
> 你也许看到过
= as you may have read
< you might see
> 我们在那儿留下消息
= we left our messages there
< that we have there

> 噢，听到了吗，亲爱的？
= oh did you hear that darling ?
< oh you hear that honey ?
> 我们跟踪了你。
= we have been tracking you .
< we followed you .
> 我们当时没有答案
= we had never heard before
< we we n t have answers
> 哦，她来了。
= oh and here she is .
< oh there she is .
> 噢，天啊。进去！
= oh god . in !
< oh . jesus . go in !
> 又有一个组织为
= another organization giving you credit
< there s another organization
> 我今天在这里…
= i m here today . . .
< i i here today . . . . . .
> 我有私人办公室。
= i have a private office too .
< i ve got private office .
> 是啊，我是有女朋友。
= yeah i do have a girlfriend .
< yeah . i i a girlfriend girlfriend
> 我们应该被和谐了。
= we just got shut down .
< we should be be . . .

> 我没说他撒谎。
= i m not saying it s a lie .
< i did n t say him .
> 好让我知道你没事。
= so i know you re ok .
< make me know you re okay .
> 但我们已经证实
= we do know this
< but we have have
> 我要教训教训他。
= i m going to fuck him up .
< i ll teach him a lesson .
> 好的。请进。
= of course . please come in .
< okay . come on in .
> 我们可以去我的实验室。
= we can work at my lab .
< we re going to my lab .
> 我没事！我耳朵！
= i m alright ! my ears !
< i m ! my ears !
> 显然，细节很精确。
= apparently the details were accurate .
< clearly the details is accurate .
> 再给我来点肉。
= i m gon na need some meat .
< and get some meat .
> 上帝啊，不要。凶手！
= oh god no . murderer !
< jesus no . the ! !

> 我整天都对着死人。
= i m around dead people all day .
< i ve been dead all day day . .
> 我很好，除了...
= i m fine except . . .
< i i m . . . except . . .
> 剩下的路都要这样？
= are we doing like rest of way home ?
< and the rest of the ? ?
> 把蛋糕包起来吧。
= wrap the cake up .
< let s go the cake .
> 很高兴你能来到这。
= i m glad you could come .
< glad you re you you .
> 孩子们，你们应该记得，
= kids as you ll recall
< boys you should remember
> 我们有了嫌疑犯。
= we got a possible suspect .
< we ve got a suspect .
> 又是玩笑？
= joke ?
< it s ?
> 哦，天哪，这是真的！
= oh god it s true !
< oh my god it s !
> 所以他连这个都知道。
= so he knew that too .
< so he why he knows knows .

> 我可以再等上15分钟。
= so i can wait another minutes .
< i could wait for minutes .
> 哦对了手术是什么时候？
= oh fuck it what time ?
< oh right . when ?
> 我们不投资黄金。
= we do n t invest in gold .
< we re not in our gold .
> 我也喜欢收藏东西。
= i m a pack rat of sorts myself .
< i like to collect things .
> 我准备进去，
= i m gon na go in
< i was going in in
> 天哪。那就有问题了！
= oh my . now that s something !
< jesus . that s a problem !
> 你没想过并不意味着
= just because you did n t mean it
< you do n t think think n t
> 是啊，我也能听到。
= yeah i can hear it too .
< yeah . i can hear it too .
> 你必须得下车
= we have to leave the car
< you have to get get off
> 我没有尽力
= i have not tried hard enough to be saved
< i did n t try my best

> 喔，我很愿意去。
= oh i d love to go .
< well i d love to .
> 我听到你跟他说话。
= i heard you talking to him .
< i i heard you talk to him .
> 我们一起睡着了。
= we fell asleep together
< we re sleeping together .
> 不知道是什么上面的，
= we do n t know what it s from
< i do n t know what it it
> 我离开后有什么新消息吗？
= anything new since i left ?
< did i get anything from the ? ?
> 从第一天起就爱你。
= i have since the day i met you .
< from the first day you . .
> 噢，上帝啊。还好吗？
= oh jesus . pants ?
< oh god . . s ? ?
> 我是新的制作人，
= i m the new executive producer
< i m a new producer
> 像他一样？
= just like he is .
< like him ?
> 我要吃了这只猫。
= i m gon na eat this cat .
< i ll take this cat .

> 只是别利用我。
= just do n t use me to do it .
< only just do n t use me .
> 显然如此。你一定很忙。
= apparently . you must be a real handful .
< obviously obviously . you must be busy .
> 有存款吗？有，当然。
= any family money ? yeah you bet .
< got a savings ? yes of course .
> 作为一个男人，一个丈夫...
= as a man and a husband . . .
< being a man a husband . . .
> 你还算是我的儿子吗？
= are you really my son ?
< you you my my son ? ?
> 噢我们会的，但不是现在。
= oh we do but not just yet .
< oh we will but not now .
> 我们离开香港便安全
= we ll leave and be safe
< we ll be safe from hong kong
> 对，我……恩，
= yeah i know . it s the . . . um
< yes i m . . . um
> 我们都必须整理好自己的生活...
= we both have to sort out our lives . . .
< we ve all had to our . . . life . . .
> 我们现在得去旅馆
= we need to go to the hotel
< we re going to to a hotel

</pre>