<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [自然语言生成的主要目标](#%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%94%9F%E6%88%90%E7%9A%84%E4%B8%BB%E8%A6%81%E7%9B%AE%E6%A0%87)
  - [尽可能让机器说话更自然](#%E5%B0%BD%E5%8F%AF%E8%83%BD%E8%AE%A9%E6%9C%BA%E5%99%A8%E8%AF%B4%E8%AF%9D%E6%9B%B4%E8%87%AA%E7%84%B6)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



# 自然语言生成的主要目标

- 尽可能让机器说话更自然（更接近人类）
- 尽可能在书写模板所占用的时间和书写规则（代码）的时间平衡，降低总体工作成本

## 尽可能让机器说话更自然

假设机器人需要提供某航班的起飞时间，它可以这么说：

111号航班的起飞时间07:00。

这样好像也没什么太大，问题。
但是如果机器人需要同时提供某航班的起飞和降落时间，它可以这么说：

111号航班的起飞时间07:00，#111航班的降落时间17:00

这样是生硬的把两条信息放到了一起。而人类说它可能会这样：

111号航班于上午7点起飞并于下午5点降落

如何生成更自然的人类语言，则是自然语言生成的研究目标之一。
