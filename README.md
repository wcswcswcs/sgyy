# sgyy
《三国演义》知识图谱

## 数据获取

* 自己爬取，已完成
* 中国四大名著人物关系知识图谱和OWL本体（信息少）　[地址](http://openkg.cn/dataset/ch4masterpieces)

## 人物名字提取

* 使用三国志游戏中的人物列表（全且准确）

* 使用三方工具提取

  * `FudanDNN-NLP4.2`复旦深度网络中文自然语言处理系统(Java) [地址](http://openkg.cn/tool/fudandnnnlp)

  * 甲骨(Jiagu)深度学习自然语言处理工具（支持知识图谱开放信息抽取，Python）[地址](http://openkg.cn/tool/jiagu)

    效果差

* 自己写模型提取（难度大且不准确，以后有时间会研究一下）

* 爬取网站数据，得到4500个人物信息。完成

  * 下载对应头像
  * 爬取具体内容
  * 去掉异常数据

## 关系提取

* 使用三方工具提取
  * `DeepKE`：浙江大学基于深度学习的开源中文关系抽取工具(Python) [地址](http://openkg.cn/tool/deepke)