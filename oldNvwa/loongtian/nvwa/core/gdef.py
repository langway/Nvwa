#!/usr/bin/env python
# coding: utf-8
"""
全局定义
Project:  nvwa
Title:    gdef 
Created by zheng on 2014/10/16.
UpdateLog:

"""

from loongtian.nvwa.common.utils.singleton import *
from Queue import Queue
from loongtian.nvwa.common.utils.queue import PriorityQueue
from loongtian.nvwa.organs.dispenser import Dispenser

@singleton
class GlobalDefine(object):
    '''
    全局变量定义
    
    cache_dict 公共缓存区
    console_input_queue  控制台输入队列
    console_output_queue  控制台输出队列
    refer_input_queue  指的是输入队列 #TODO 应该和 console_input_queue合并。
    manage_input_queue  管理员输入队列，需权限。
    manage_output_queue  管理员输出队列，需权限。
    rethink_queue  反思引擎队列
    command_msg 命令信息队列，由执行引擎调用。内容是计划中枢输出的计划。
    dispenser 多客户端分发
    collection_input_queue 集合输入队列 #TODO 应该和 console_input_queue合并。
    action_list 动作列表 # TODO 是否应该去掉，由数据库直接读取？
    original_real_object_dict 原始内置的RealObject。
    '''

    def __init__(self):
        self.cache_dict = {}
        self.console_input_queue = Queue()
        self.console_output_queue = Queue()
        self.refer_input_queue = Queue()
        self.manage_input_queue = Queue()
        self.manage_output_queue = Queue()
        self.rethink_queue = Queue()
        self.command_msg = PriorityQueue()
        self.dispenser = Dispenser()
        self.collection_input_queue = Queue()

        # self.action_list = [u'吃', u'喝', u'唱', u'写', u'说', u'读', u'玩', u'擅长', u'走', u'坐', u'看', u'听', u'打', u'拿', u'批评',
        #                     u'宣传', u'保卫', u'学习', u'爱', u'恨', u'怕', u'想', u'喜欢', u'害怕', u'想念', u'觉得', u'在', u'存', u'存在',
        #                     u'出现', u'失去', u'消失', u'能', u'会', u'愿意', u'敢', u'应该', u'要', u'上', u'下', u'进', u'出', u'回',
        #                     u'过', u'起', u'开', u'来', u'上来', u'下来', u'进来', u'出来', u'回来', u'过来', u'起来', u'开来', u'去', u'上去',
        #                     u'下去', u'进去', u'出去', u'回去', u'过去', u'开去']
        #self.action_list = [u"哀求",u"挨",u"爱",u"爱好",u"安",u"安家",u"安排",u"安慰",u"安装",u"按摩",u"暗示",u"暗算",u"暗想",u"扒",u"拔",u"把",u"把持",u"把守",u"把握",u"罢工",u"罢免",u"白搭",u"摆动",u"摆放",u"摆弄",u"摆设",u"摆脱",u"败",u"败露",u"拜访",u"颁发",u"搬动",u"办",u"办案",u"办理",u"拌",u"帮",u"帮忙",u"帮助",u"包",u"包含",u"包括",u"包围",u"包装",u"保持",u"保管",u"保护",u"保留",u"保密",u"保卫",u"保证",u"报仇",u"报答",u"报告",u"报价",u"报名",u"报销",u"报效",u"抱",u"暴动",u"暴露",u"爆发",u"爆炸",u"备课",u"备战",u"背",u"背叛",u"背诵",u"奔赴",u"奔跑",u"奔走",u"迸发",u"蹦",u"逼迫",u"比较",u"比赛",u"比试",u"比喻",u"笔录",u"避开",u"避免",u"编",u"编辑",u"编写",u"编织",u"贬低",u"贬值",u"变",u"变革",u"变化",u"变形",u"辨别",u"辨认",u"辩论",u"标",u"标志",u"表达",u"表明",u"表现",u"表扬",u"憋",u"别",u"濒临",u"并联",u"并吞",u"病",u"病休",u"拨",u"剥",u"剥夺",u"剥落",u"剥削",u"播放",u"播音",u"播种",u"博得",u"搏斗",u"补",u"补偿",u"补充",u"补发",u"补给",u"补贴",u"哺育",u"捕捉",u"布置",u"部署",u"擦",u"猜",u"猜想",u"裁",u"裁决",u"裁军",u"采访",u"采购",u"采纳",u"采用",u"踩",u"参拜",u"参观",u"参加",u"参考",u"参与",u"残杀",u"操持",u"操练",u"操纵",u"侧重",u"测量",u"测验",u"插手",u"查",u"查抄",u"查对",u"查获",u"查看",u"查问",u"查询",u"查阅",u"拆",u"拆除",u"拆散",u"拆卸",u"搀假",u"产生",u"铲",u"铲除",u"阐述",u"颤动",u"长",u"尝",u"偿还",u"畅谈",u"畅销",u"倡议",u"唱",u"抄袭",u"抄写",u"超脱",u"超支",u"超重",u"吵",u"吵闹",u"炒",u"扯",u"撤除",u"撤换",u"撤退",u"撤销",u"沉淀",u"沉思",u"沉醉",u"陈设",u"陈述",u"闯",u"衬托",u"称",u"称呼",u"称赞",u"撑腰",u"成",u"成交",u"成立",u"成为",u"呈现",u"承担",u"承认",u"乘凉",u"惩罚",u"惩治",u"澄清",u"吃",u"吃透",u"迟到",u"持家",u"耻笑",u"充当",u"充满",u"充数",u"冲",u"冲锋",u"冲破",u"崇拜",u"宠",u"宠爱",u"抽查",u"抽调",u"抽签",u"抽烟",u"抽样",u"仇恨",u"仇视",u"筹备",u"酬谢",u"丑化",u"出",u"出版",u"出产",u"出场",u"出动",u"出发",u"出国",u"出击",u"出来",u"出力",u"出卖",u"出让",u"出生",u"出手",u"出售",u"出席",u"出现",u"出征",u"出租",u"除",u"储藏",u"处罚",u"处理",u"处死",u"处置",u"触发",u"揣摩",u"穿",u"穿越",u"传",u"传播",u"传出",u"传递",u"传话",u"传染",u"传授",u"传说",u"传送",u"喘",u"喘气",u"创办",u"创建",u"创新",u"创造",u"创作",u"吹",u"吹捧",u"吹嘘",u"垂直",u"春耕",u"辞退",u"辞职",u"刺",u"刺探",u"从事",u"凑",u"促进",u"簇拥",u"篡改",u"催",u"催促",u"催眠",u"摧残",u"存",u"存储",u"存放",u"存款",u"存在",u"搓",u"磋商",u"挫伤",u"错怪",u"搭救",u"搭配",u"达到",u"答辩",u"答复",u"答理",u"答应",u"打",u"打扮",u"打点",u"打发",u"打击",u"打搅",u"打开",u"打捞",u"打量",u"打破",u"打扰",u"打算",u"打听",u"打印",u"打仗",u"打针",u"大战",u"代",u"代办",u"代表",u"代理",u"代替",u"代销",u"带",u"带动",u"带领",u"待业",u"怠慢",u"逮",u"逮捕",u"担保",u"担任",u"担心",u"耽搁",u"胆敢",u"当",u"当选",u"当做",u"挡",u"导演",u"导致",u"倒",u"倒车",u"倒换",u"捣",u"捣乱",u"祷告",u"到",u"到达",u"到会",u"悼念",u"盗卖",u"盗窃",u"道歉",u"得",u"得到",u"得知",u"得罪",u"登报",u"登记",u"等",u"等待",u"等于",u"低估",u"滴",u"抵",u"抵偿",u"抵达",u"抵抗",u"抵御",u"抵制",u"地震",u"递送",u"缔造",u"颠倒",u"颠覆",u"点",u"点破",u"点燃",u"点缀",u"电贺",u"垫",u"惦挂",u"惦记",u"刁难",u"雕刻",u"钓",u"调",u"调查",u"调动",u"调集",u"调价",u"调节",u"调理",u"调配",u"调试",u"调整",u"掉",u"跌",u"跌倒",u"叠",u"叮嘱",u"盯",u"钉",u"顶替",u"订",u"订购",u"订阅",u"定",u"定货",u"定居",u"定义",u"丢",u"丢掉",u"懂",u"动",u"动手",u"动摇",u"动员",u"冻",u"洞察",u"斗",u"斗争",u"逗",u"逗乐",u"督促",u"读",u"独创",u"独占",u"堵",u"堵截",u"妒忌",u"杜绝",u"度假",u"端正",u"断",u"断定",u"断绝",u"断言",u"锻炼",u"堆",u"堆放",u"对比",u"对待",u"对付",u"对话",u"对抗",u"对照",u"兑换",u"蹲",u"夺",u"夺取",u"躲",u"躲避",u"讹诈",u"扼杀",u"饿",u"遏制",u"发",u"发表",u"发布",u"发动",u"发还",u"发挥",u"发觉",u"发明",u"发难",u"发起",u"发烧",u"发射",u"发生",u"发送",u"发现",u"发泄",u"发行",u"发言",u"发扬",u"发展",u"罚",u"罚款",u"翻",u"翻修",u"翻译",u"翻印",u"繁殖",u"反",u"反对",u"反抗",u"反馈",u"反省",u"反问",u"返航",u"犯",u"犯法",u"犯罪",u"贩卖",u"防备",u"防范",u"防洪",u"防涝",u"防守",u"防御",u"防止",u"妨碍",u"仿效",u"仿造",u"访问",u"纺",u"放",u"放弃",u"放任",u"放松",u"放心",u"放纵",u"飞",u"飞越",u"诽谤",u"废",u"废除",u"费",u"分",u"分布",u"分担",u"分工",u"分化",u"分解",u"分开",u"分裂",u"分配",u"分散",u"分析",u"吩咐",u"粉碎",u"奋斗",u"丰收",u"风行",u"封闭",u"封锁",u"疯",u"缝",u"讽刺",u"奉告",u"奉劝",u"奉献",u"否定",u"否认",u"扶",u"扶持",u"服",u"服侍",u"服务",u"服用",u"浮",u"浮动",u"浮现",u"符合",u"抚养",u"俯视",u"辅导",u"辅助",u"腐蚀",u"付",u"付出",u"负担",u"负责",u"附带",u"附加",u"复辟",u"复核",u"复习",u"复印",u"复制",u"富余",u"赋予",u"该",u"改",u"改变",u"改动",u"改革",u"改换",u"改进",u"改良",u"改善",u"改选",u"改造",u"改正",u"改装",u"盖",u"概括",u"干",u"干扰",u"干预",u"甘心",u"甘愿",u"赶",u"赶赴",u"敢",u"敢于",u"感到",u"感动",u"感觉",u"感冒",u"感染",u"感谢",u"搞",u"告辞",u"告发",u"告诉",u"割",u"割除",u"割让",u"歌颂",u"革命",u"隔",u"隔断",u"给",u"给以",u"给予",u"根治",u"跟",u"跟踪",u"更改",u"更换",u"更新",u"工作",u"公布",u"公审",u"攻击",u"供",u"供认",u"供应",u"巩固",u"共鸣",u"贡献",u"勾搭",u"勾引",u"构成",u"购买",u"购置",u"够",u"估计",u"估算",u"辜负",u"鼓吹",u"鼓励",u"顾忌",u"瓜分",u"挂",u"挂念",u"拐",u"拐骗",u"怪",u"关",u"关心",u"观察",u"观看",u"观赏",u"观望",u"管",u"管教",u"管理",u"贯彻",u"惯",u"灌溉",u"广播",u"逛",u"归还",u"归属",u"规定",u"滚",u"过",u"过来",u"过滤",u"过去",u"过问",u"害",u"害怕",u"含",u"喊",u"捍卫",u"好像",u"号召",u"耗费",u"耗资",u"喝",u"喝彩",u"合并",u"合计",u"合影",u"合作",u"和解",u"核对",u"核实",u"核算",u"恨",u"横穿",u"横扫",u"衡量",u"轰动",u"轰炸",u"哄抢",u"烘托",u"弘扬",u"后悔",u"呼唤",u"呼吸",u"呼吁",u"忽视",u"胡说",u"糊",u"互换",u"护",u"护理",u"护送",u"花",u"花费",u"滑",u"化",u"化验",u"化装",u"划分",u"划清",u"怀抱",u"怀念",u"怀疑",u"欢呼",u"欢送",u"欢迎",u"还",u"还击",u"缓和",u"幻想",u"换",u"换算",u"涣散",u"荒废",u"晃动",u"恢复",u"挥发",u"挥霍",u"挥舞",u"回",u"回避",u"回答",u"回顾",u"回击",u"回去",u"回收",u"回味",u"回想",u"回忆",u"悔恨",u"汇报",u"会",u"会见",u"会面",u"会谈",u"会晤",u"会战",u"绘图",u"绘制",u"贿赂",u"毁",u"毁灭",u"昏迷",u"混淆",u"混杂",u"活",u"活动",u"活跃",u"获得",u"获取",u"获准",u"讥笑",u"击毙",u"击溃",u"积累",u"积攒",u"激发",u"激励",u"急需",u"集合",u"集中",u"嫉妒",u"挤",u"计划",u"计较",u"记",u"记功",u"记录",u"记叙",u"记载",u"纪念",u"忌讳",u"继承",u"寄",u"寄存",u"寄托",u"加",u"加工",u"加剧",u"加强",u"加入",u"加以",u"夹击",u"驾驶",u"架设",u"假定",u"假冒",u"假设",u"坚持",u"坚守",u"坚信",u"歼灭",u"兼并",u"兼任",u"监督",u"监视",u"煎",u"拣",u"捡",u"减",u"减轻",u"减少",u"剪",u"剪辑",u"检查",u"检举",u"检索",u"检讨",u"检修",u"检验",u"见面",u"建成",u"建立",u"建设",u"建议",u"践踏",u"鉴别",u"鉴定",u"讲",u"讲解",u"讲究",u"讲课",u"讲授",u"奖",u"奖励",u"降低",u"降落",u"交待",u"交锋",u"交换",u"交流",u"交纳",u"交涉",u"交往",u"郊游",u"浇",u"矫正",u"搅",u"搅拌",u"缴获",u"叫",u"叫喊",u"叫嚷",u"教",u"教导",u"教训",u"教育",u"接",u"接触",u"接待",u"接见",u"接近",u"接洽",u"接受",u"接送",u"揭发",u"揭露",u"节省",u"节约",u"劫持",u"结合",u"结交",u"结束",u"截获",u"截击",u"竭尽",u"解除",u"解放",u"解决",u"解剖",u"解说",u"解脱",u"解析",u"介入",u"介绍",u"戒严",u"借",u"借口",u"借用",u"借助",u"谨防",u"尽",u"进攻",u"进来",u"进去",u"进入",u"进行",u"浸透",u"禁止",u"经过",u"经受",u"惊动",u"惊叹",u"精通",u"警告",u"警惕",u"竞争",u"敬佩",u"敬献",u"敬重",u"纠缠",u"纠正",u"救",u"救济",u"救援",u"救助",u"就业",u"居留",u"鞠躬",u"举",u"举办",u"举行",u"拒绝",u"具有",u"惧怕",u"捐赠",u"捐助",u"决定",u"觉得",u"觉悟",u"军训",u"开",u"开辟",u"开采",u"开除",u"开导",u"开发",u"开赴",u"开工",u"开会",u"开垦",u"开阔",u"开启",u"开始",u"开脱",u"开学",u"开展",u"刊登",u"刊载",u"勘查",u"砍",u"看",u"看待",u"看见",u"看守",u"看重",u"扛",u"抗衡",u"抗拒",u"抗议",u"考",u"考察",u"考核",u"考虑",u"考取",u"考验",u"靠",u"靠近",u"咳嗽",u"可",u"可能",u"可以",u"渴望",u"克服",u"克制",u"肯",u"肯定",u"恳求",u"空谈",u"恐吓",u"控告",u"控诉",u"控制",u"扣除",u"扣押",u"哭",u"苦练",u"酷爱",u"夸奖",u"垮",u"跨过",u"宽恕",u"旷工",u"亏损",u"窥视",u"馈赠",u"捆",u"扩充",u"扩散",u"扩展",u"拉",u"来",u"来访",u"来往",u"拦",u"浪费",u"捞",u"劳动",u"牢记",u"涝",u"乐意",u"勒索",u"类推",u"累计",u"冷藏",u"冷冻",u"离开",u"犁",u"理发",u"理解",u"力争",u"历经",u"利用",u"利于",u"例如",u"连结",u"联合",u"联欢",u"联络",u"联系",u"联想",u"练",u"练习",u"谅解",u"量",u"聊",u"了",u"了解",u"了却",u"料到",u"料想",u"列入",u"裂",u"邻近",u"吝惜",u"零售",u"领",u"领导",u"领会",u"领取",u"领悟",u"溜走",u"浏览",u"流",u"流传",u"流动",u"流浪",u"流落",u"流失",u"流行",u"留",u"留给",u"留恋",u"留心",u"垄断",u"搂抱",u"漏",u"露",u"露出",u"录取",u"录音",u"路过",u"旅行",u"旅游",u"绿化",u"掠夺",u"轮换",u"轮休",u"论述",u"落实",u"落选",u"麻痹",u"麻烦",u"骂",u"埋",u"埋伏",u"埋怨",u"买",u"卖",u"卖弄",u"瞒",u"满足",u"忙于",u"盲从",u"冒充",u"冒险",u"貌似",u"没",u"没收",u"美化",u"萌发",u"猛攻",u"蒙受",u"梦想",u"弥补",u"迷",u"迷惑",u"迷信",u"密封",u"密谋",u"勉励",u"面临",u"描绘",u"描述",u"瞄准",u"藐视",u"灭",u"明白",u"明确",u"命令",u"摸",u"摸索",u"摸透",u"模仿",u"模拟",u"摩擦",u"磨练",u"默认",u"默写",u"谋划",u"谋求",u"目送",u"拿",u"内销",u"能",u"能够",u"拟定",u"念叨",u"酿成",u"捏造",u"凝聚",u"凝视",u"扭转",u"弄清",u"怒斥",u"虐待",u"挪用",u"殴打",u"爬",u"怕",u"拍卖",u"拍摄",u"拍照",u"徘徊",u"排除",u"排练",u"排泄",u"派",u"派出",u"攀比",u"盘算",u"盘问",u"判断",u"盼",u"盼望",u"旁听",u"抛弃",u"跑",u"泡",u"陪",u"陪伴",u"陪同",u"培训",u"培养",u"赔偿",u"赔款",u"佩服",u"配合",u"配音",u"抨击",u"捧",u"碰",u"碰见",u"碰撞",u"批驳",u"批评",u"批示",u"批准",u"偏爱",u"偏向",u"骗",u"骗取",u"漂泊",u"飘",u"飘扬",u"拼搏",u"拼写",u"聘任",u"平息",u"评",u"评估",u"评价",u"评论",u"评选",u"评议",u"泼",u"迫害",u"迫使",u"破坏",u"扑",u"期待",u"期望",u"欺负",u"欺骗",u"欺压",u"歧视",u"祈祷",u"骑",u"企图",u"启程",u"启发",u"启用",u"起草",u"起伏",u"起来",u"起诉",u"起用",u"气",u"洽谈",u"牵",u"牵扯",u"牵制",u"签署",u"前进",u"潜伏",u"遣返",u"欠",u"强调",u"强迫",u"抢",u"抢劫",u"抢修",u"敲",u"敲诈",u"撬",u"切除",u"切断",u"窃取",u"亲临",u"侵略",u"轻视",u"倾听",u"清查",u"清除",u"清楚",u"清理",u"清洗",u"请",u"请教",u"请求",u"请示",u"庆祝",u"求",u"求教",u"区分",u"驱逐",u"趋向",u"取得",u"取缔",u"取消",u"去",u"权衡",u"劝",u"劝说",u"缺乏",u"缺少",u"确保",u"确定",u"确信",u"燃烧",u"让",u"饶恕",u"扰乱",u"热爱",u"热衷",u"忍",u"忍受",u"认",u"认识",u"任命",u"荣获",u"容许",u"熔化",u"揉",u"如同",u"入场",u"入侵",u"入学",u"撒谎",u"塞",u"赛",u"散",u"散步",u"扫",u"杀",u"杀伤",u"筛选",u"晒",u"删",u"煽动",u"闪开",u"善于",u"擅长",u"伤",u"伤亡",u"商量",u"上",u"上报",u"上当",u"上交",u"上来",u"上去",u"上演",u"烧毁",u"舍得",u"设",u"设法",u"设计",u"涉及",u"摄制",u"申报",u"申请",u"伸",u"伸缩",u"深知",u"审",u"审查",u"审核",u"审理",u"审批",u"审讯",u"渗透",u"升",u"升华",u"生",u"生产",u"生活",u"声明",u"胜",u"胜利",u"胜任",u"省",u"省略",u"盛行",u"剩",u"失败",u"失掉",u"失去",u"失误",u"失踪",u"施工",u"施加",u"施展",u"时兴",u"识别",u"实现",u"实行",u"拾",u"使",u"使唤",u"示意",u"视察",u"试探",u"试图",u"试问",u"试验",u"是",u"适合",u"适应",u"释放",u"收",u"收藏",u"收获",u"收集",u"收买",u"收入",u"收养",u"守护",u"受",u"授予",u"书写",u"抒发",u"疏导",u"输出",u"输送",u"熟悉",u"束缚",u"数",u"刷新",u"摔",u"甩掉",u"拴",u"睡",u"睡觉",u"顺从",u"说",u"说服",u"说明",u"思考",u"思念",u"撕",u"撕毁",u"死",u"饲养",u"松开",u"送",u"送给",u"搜查",u"搜集",u"诉说",u"塑造",u"算",u"算作",u"损害",u"损失",u"缩小",u"锁",u"塌",u"抬",u"贪污",u"摊派",u"谈",u"谈话",u"谈判",u"坦白",u"叹气",u"探明",u"探讨",u"躺",u"烫",u"掏",u"逃避",u"逃跑",u"陶醉",u"淘汰",u"讨论",u"疼爱",u"腾飞",u"剔除",u"踢",u"提拔",u"提倡",u"提出",u"提高",u"提名",u"提示",u"提醒",u"提议",u"体谅",u"体贴",u"体现",u"体验",u"替换",u"添",u"添设",u"填补",u"挑拨",u"挑逗",u"挑衅",u"挑选",u"跳舞",u"贴近",u"听",u"听从",u"听见",u"听说",u"停顿",u"停放",u"停留",u"停止",u"通称",u"通电",u"通缉",u"通知",u"同情",u"同意",u"统称",u"统计",u"统一",u"统治",u"偷窃",u"偷听",u"偷袭",u"投奔",u"投递",u"投靠",u"投入",u"投身",u"透露",u"突出",u"突破",u"图谋",u"涂改",u"团结",u"推",u"推测",u"推迟",u"推动",u"推翻",u"推广",u"推荐",u"推举",u"推敲",u"推想",u"推销",u"推选",u"退",u"退还",u"退换",u"退缩",u"退伍",u"退休",u"吞",u"吞并",u"托付",u"拖欠",u"脱离",u"脱落",u"妥协",u"挖",u"挖苦",u"完",u"完成",u"完善",u"玩",u"挽回",u"挽留",u"忘",u"忘掉",u"忘记",u"望见",u"危害",u"威胁",u"为",u"围攻",u"违抗",u"唯恐",u"维持",u"维护",u"维修",u"委托",u"喂",u"慰问",u"问",u"问候",u"握",u"握手",u"污蔑",u"污染",u"污辱",u"诬蔑",u"无视",u"务求",u"误传",u"误会",u"误解",u"吸",u"吸收",u"吸引",u"希望",u"习惯",u"袭击",u"洗",u"洗澡",u"喜爱",u"喜欢",u"下降",u"下去",u"吓唬",u"掀起",u"嫌",u"嫌弃",u"显得",u"显示",u"限制",u"陷害",u"陷入",u"羡慕",u"献给",u"献身",u"相反",u"相隔",u"相识",u"相信",u"享受",u"想",u"想念",u"想像",u"向往",u"象征",u"像",u"削减",u"消耗",u"消灭",u"消失",u"校对",u"笑",u"协调",u"协商",u"协助",u"携带",u"写",u"写作",u"泄露",u"卸",u"谢",u"谢绝",u"欣赏",u"信",u"信任",u"兴办",u"兴建",u"兴起",u"醒",u"休息",u"休想",u"休养",u"修",u"修补",u"修改",u"修理",u"修饰",u"修造",u"修筑",u"绣",u"虚报",u"虚设",u"需要",u"叙述",u"宣布",u"宣传",u"宣读",u"宣告",u"悬挂",u"选",u"选拔",u"选举",u"选择",u"渲染",u"学",u"学会",u"学习",u"寻求",u"巡逻",u"询问",u"训练",u"压迫",u"压缩",u"压制",u"押送",u"淹",u"延缓",u"严惩",u"研究",u"研制",u"掩护",u"掩饰",u"演",u"演出",u"演示",u"演习",u"验证",u"央求",u"佯攻",u"仰慕",u"养",u"养殖",u"邀请",u"摇",u"摇动",u"舀",u"要",u"要求",u"依靠",u"依赖",u"移交",u"遗漏",u"议论",u"抑制",u"引导",u"引起",u"引诱",u"隐藏",u"隐瞒",u"印刷",u"应当",u"应付",u"应用",u"迎候",u"营造",u"赢",u"赢得",u"影响",u"拥抱",u"拥护",u"用",u"用于",u"邮购",u"游",u"游览",u"游行",u"有",u"有关",u"有心",u"诱导",u"诱惑",u"诱骗",u"予以",u"愚弄",u"预备",u"预测",u"预定",u"预防",u"预计",u"预谋",u"预言",u"预祝",u"遇到",u"遇见",u"援助",u"怨",u"怨恨",u"愿",u"愿意",u"约定",u"约束",u"阅读",u"允许",u"运",u"运动",u"运输",u"运用",u"运载",u"酝酿",u"蕴藏",u"杂交",u"栽培",u"栽种",u"宰",u"在意",u"暂定",u"暂停",u"赞成",u"赞赏",u"赞助",u"遭到",u"遭受",u"遭遇",u"糟蹋",u"造",u"造成",u"造谣",u"责备",u"责问",u"增补",u"增长",u"增加",u"增进",u"增强",u"憎恨",u"赠送",u"诈骗",u"炸",u"榨取",u"摘除",u"摘录",u"瞻仰",u"展出",u"展开",u"展览",u"展示",u"展望",u"展销",u"占领",u"战斗",u"站",u"张",u"张贴",u"掌握",u"招待",u"招呼",u"找",u"召集",u"照",u"照搬",u"照顾",u"照看",u"遮盖",u"折磨",u"折中",u"针对",u"侦察",u"珍惜",u"诊断",u"镇压",u"争",u"争辩",u"争夺",u"争取",u"争执",u"征服",u"征求",u"挣",u"挣脱",u"挣扎",u"拯救",u"整顿",u"整理",u"整修",u"正视",u"证明",u"证实",u"支持",u"支配",u"支援",u"知道",u"执笔",u"执行",u"值得",u"指出",u"指导",u"指挥",u"指控",u"指示",u"指引",u"指责",u"制",u"制裁",u"制定",u"制服",u"制约",u"制止",u"治",u"治理",u"质问",u"致使",u"致以",u"中断",u"中止",u"终止",u"肿",u"种",u"重复",u"重视",u"咒骂",u"株连",u"主持",u"主管",u"主张",u"属",u"属于",u"煮",u"嘱咐",u"助长",u"注定",u"注解",u"注明",u"注视",u"注释",u"注意",u"注重",u"祝贺",u"祝愿",u"抓紧",u"转播",u"转告",u"转换",u"转交",u"转让",u"转送",u"转移",u"转赠",u"赚",u"撰写",u"装饰",u"装卸",u"装修",u"装做",u"撞见",u"追",u"追赶",u"追究",u"追认",u"追随",u"追问",u"准备",u"准许",u"捉",u"着手",u"琢磨",u"资助",u"滋长",u"自称",u"自勉",u"自信",u"自学",u"自愿",u"总结",u"纵容",u"走",u"走私",u"租借",u"阻碍",u"阻止",u"组织",u"醉",u"尊敬",u"尊重",u"遵守",u"作出",u"作废",u"作为",u"坐",u"座谈",u"做"]
        #self.action_list = [u"哀求",u"挨",u"爱",u"爱好",u"安",u"安家",u"安排",u"安慰",u"安装",u"按摩",u"暗示",u"暗算",u"暗想",u"扒",u"拔",u"把",u"把持",u"把守",u"把握",u"罢工",u"罢免",u"白搭",u"摆动",u"摆放",u"摆弄",u"摆设",u"摆脱",u"败",u"败露",u"拜访",u"颁发",u"搬动",u"办",u"办案",u"办理",u"拌",u"帮",u"帮忙",u"帮助",u"包",u"包含",u"包括",u"包围",u"包装",u"保持",u"保管",u"保护",u"保留",u"保密",u"保卫",u"保证",u"报仇",u"报答",u"报告",u"报价",u"报名",u"报销",u"报效",u"抱",u"暴动",u"暴露",u"爆发",u"爆炸",u"备课",u"备战",u"背",u"背叛",u"背诵",u"奔赴",u"奔跑",u"奔走",u"迸发",u"蹦",u"逼迫",u"比较",u"比赛",u"比试",u"比喻",u"笔录",u"避开",u"避免",u"编",u"编辑",u"编写",u"编织",u"贬低",u"贬值",u"变",u"变革",u"变化",u"变形",u"辨别",u"辨认",u"辩论",u"标",u"标志",u"表达",u"表明",u"表现",u"表扬",u"憋",u"别",u"濒临",u"并联",u"并吞",u"病",u"病休",u"拨",u"剥",u"剥夺",u"剥落",u"剥削",u"播放",u"播音",u"播种",u"博得",u"搏斗",u"补",u"补偿",u"补充",u"补发",u"补给",u"补贴",u"哺育",u"捕捉",u"布置",u"部署",u"擦",u"猜",u"猜想",u"裁",u"裁决",u"裁军",u"采访",u"采购",u"采纳",u"采用",u"踩",u"参拜",u"参观",u"参加",u"参考",u"参与",u"残杀",u"操持",u"操练",u"操纵",u"侧重",u"测量",u"测验",u"插手",u"查",u"查抄",u"查对",u"查获",u"查看",u"查问",u"查询",u"查阅",u"拆",u"拆除",u"拆散",u"拆卸",u"搀假",u"产生",u"铲",u"铲除",u"阐述",u"颤动",u"长",u"尝",u"偿还",u"畅谈",u"畅销",u"倡议",u"唱",u"抄袭",u"抄写",u"超脱",u"超支",u"超重",u"吵",u"吵闹",u"炒",u"扯",u"撤除",u"撤换",u"撤退",u"撤销",u"沉淀",u"沉思",u"沉醉",u"陈设",u"陈述",u"闯",u"衬托",u"称",u"称呼",u"称赞",u"撑腰",u"成",u"成交",u"成立",u"成为",u"呈现",u"承担",u"承认",u"乘凉",u"惩罚",u"惩治",u"澄清",u"吃",u"吃透",u"迟到",u"持家",u"耻笑",u"充当",u"充满",u"充数",u"冲",u"冲锋",u"冲破",u"崇拜",u"宠",u"宠爱",u"抽查",u"抽调",u"抽签",u"抽烟",u"抽样",u"仇恨",u"仇视",u"筹备",u"酬谢",u"丑化",u"出",u"出版",u"出产",u"出场",u"出动",u"出发",u"出国",u"出击",u"出来",u"出力",u"出卖",u"出让",u"出生",u"出手",u"出售",u"出席",u"出现",u"出征",u"出租",u"除",u"储藏",u"处罚",u"处理",u"处死",u"处置",u"触发",u"揣摩",u"穿",u"穿越",u"传",u"传播",u"传出",u"传递",u"传话",u"传染",u"传授",u"传说",u"传送",u"喘",u"喘气",u"创办",u"创建",u"创新",u"创造",u"创作",u"吹",u"吹捧",u"吹嘘",u"垂直",u"春耕",u"辞退",u"辞职",u"刺",u"刺探",u"从事",u"凑",u"促进",u"簇拥",u"篡改",u"催",u"催促",u"催眠",u"摧残",u"存",u"存储",u"存放",u"存款",u"存在",u"搓",u"磋商",u"挫伤",u"错怪",u"搭救",u"搭配",u"达到",u"答辩",u"答复",u"答理",u"答应",u"打",u"打扮",u"打点",u"打发",u"打击",u"打搅",u"打开",u"打捞",u"打量",u"打破",u"打扰",u"打算",u"打听",u"打印",u"打仗",u"打针",u"大战",u"代",u"代办",u"代表",u"代理",u"代替",u"代销",u"带",u"带动",u"带领",u"待业",u"怠慢",u"逮",u"逮捕",u"担保",u"担任",u"担心",u"耽搁",u"胆敢",u"当",u"当选",u"当做",u"挡",u"导演",u"导致",u"倒",u"倒车",u"倒换",u"捣",u"捣乱",u"祷告",u"到",u"到达",u"到会",u"悼念",u"盗卖",u"盗窃",u"道歉",u"得",u"得到",u"得知",u"得罪",u"登报",u"登记",u"等",u"等待",u"等于",u"低估",u"滴",u"抵",u"抵偿",u"抵达",u"抵抗",u"抵御",u"抵制",u"地震",u"递送",u"缔造",u"颠倒",u"颠覆",u"点",u"点破",u"点燃",u"点缀",u"电贺",u"垫",u"惦挂",u"惦记",u"刁难",u"雕刻",u"钓",u"调",u"调查",u"调动",u"调集",u"调价",u"调节",u"调理",u"调配",u"调试",u"调整",u"掉",u"跌",u"跌倒",u"叠",u"叮嘱",u"盯",u"钉",u"顶替",u"订",u"订购",u"订阅",u"定",u"定货",u"定居",u"定义",u"丢",u"丢掉",u"懂",u"动",u"动手",u"动摇",u"动员",u"冻",u"洞察",u"斗",u"斗争",u"逗",u"逗乐",u"督促",u"读",u"独创",u"独占",u"堵",u"堵截",u"妒忌",u"杜绝",u"度假",u"端正",u"断",u"断定",u"断绝",u"断言",u"锻炼",u"堆",u"堆放",u"对比",u"对待",u"对付",u"对话",u"对抗",u"对照",u"兑换",u"蹲",u"夺",u"夺取",u"躲",u"躲避"]
        self.action_list = [u"哀求",u"仇视",u"暗算",u"哀求",u"哭",u"参观",u"报名",u"登记",u"查看",u"出场",u"打",u"有"]
        # news_ids = [][u'创建集合']
        # for idInt in self.action_list:
        #     if idInt.encode('utf-8') not in news_ids:
        #         news_ids.append(idInt.encode('utf-8'))
        # print news_ids
        # f = open("c:/v_word_list.txt",'a')
        # f.write(','.join(news_ids))
        # f.close()

        self.original_real_object_dict = {
            u'Refer': [u'指的是', ''],
            u'Next': [u'然后', ''],
            u'And': [u'并且', ''],
            u'InheritFrom': [u'是i', ''],
            u'SymbolInherit': [u'符号继承', ''],
            u'Nothingness': [u'虚无', ''],
            u'InnerSelf': [u'我', ''],
            u'Word': [u'词类', ''],
            u'Object': [u'对象', ''],
            u'NotUnderstood': [u'未理解', ''],
            u'BeModified': [u'被修限', ''],
            u'Receive': [u'接收', ''],
            u'Send': [u'发出', ''],
            u'UnderstoodAs': [u'理解为', ''],
            u'Time': [u'时间', ''],
            u'TimeIs': [u'时间为', ''],
            u'SensorIs': [u'使用的感知器', ''],
            u'FromId': [u'来源账号', ''],
            u'Target': [u'目标', ''],
            u'Console': [u'控制台', ''],
            u'FRestrict': [u'正向限定', ''],
            u'BRestrict': [u'逆向限定', ''],
            u'Attribute': [u'属性', ''],
            u'HasAttribute': [u'有属性', ''],
            u'UnknownBiRelation': [u'双向未知关系', ''],
            u'DefaultClass': [u'默认类', ''],
            u'DefaultAction': [u'默认Act', ''],
            u'Mood': [u'语气', ''],
            u'Declarative': [u'陈述', ''],
            u'Question': [u'疑问', ''],
            u'Number': [u'数字', ''],
            u'Quantifier': [u'量词', ''],
            u'QuantityIs': [u'数量为', ''],
            u'QuantityPair': [u'数量对', ''],
            u'ActOuterPH': [u'act外层占位符', ''],
            u'ObserverIs': [u'观察者是', ''],
            u'Component': [u'组件', ''],
            u'Anonymous': [u'匿名用户', ''],
            u'God': [u'God', ''],
            u'Collection': [u'集合', ''],
            u'CollectionContainItem': [u'包含', ''],
            u'ItemInf': [u'元素继承自', ''],
            u'NextItem':[u'下一个元素',''],
            u'PreviousItem':[u'上一个元素',''],
            u'CountIs': [u'数值为', ''],
            u'QuantifierIs': [u'量词为', ''],
            u'Negate': [u'非', ''],
            u'Multi': [u'多值', ''],
            u'CommonIs': [u'是t', ''],
            u'IsSelf': [u'是s', ''],
            u'Action': [u'Action', ''],  # todo 待删除
            u'SequenceIs': [u'SequenceIs', ''],
            u'StepIs': [u'StepIs', ''],
            u'ActionSemantic':[u'Action语义为',''],
            u'ActionStructure':[u'Action结构为',''],
            u'PlaceHolder':[u'占位符类',''],
            u'FunctionBase':[u'函数类',''],
            u'FunctionName':[u'函数名称',''],
        }

        class OriginalRealObjectName(object):
            '''
            原始内置RealObject名字
            '''
            def __init__(self, id_dict):
                '''
                id_dict ==> original_real_object_dict
                '''
                self._id_dict = id_dict

            def get_all_name(self):
                '''
                获得original_real_object_dict(原始内置的RealObject)的所有的[Key]
                '''
                return self._id_dict.keys()

            @property
            def PlaceHolder(self):
                return self._getter(u'PlaceHolder')

            @property
            def ActionSemantic(self):
                return self._getter(u'ActionSemantic')

            @property
            def ActionStructure(self):
                return self._getter(u'ActionStructure')

            @property
            def Refer(self):
                return self._getter(u'Refer')

            @property
            def Next(self):
                return self._getter(u'Next')

            @property
            def And(self):
                return self._getter(u'And')

            @property
            def SequenceIs(self):
                return self._getter(u'SequenceIs')

            @property
            def StepIs(self):
                return self._getter(u'StepIs')

            @property
            def Action(self):
                return self._getter(u'Action')

            @property
            def IsSelf(self):
                return self._getter(u'IsSelf')

            @property
            def Multi(self):
                return self._getter(u'Multi')

            @property
            def CommonIs(self):
                return self._getter(u'CommonIs')

            @property
            def Negate(self):
                return self._getter(u'Negate')

            @property
            def Collection(self):
                return self._getter(u'Collection')

            @property
            def CollectionContainItem(self):
                return self._getter(u'CollectionContainItem')

            @property
            def NextItem(self):
                return self._getter(u'NextItem')

            @property
            def FunctionBase(self):
                return self._getter(u'FunctionBase')

            @property
            def FunctionName(self):
                return self._getter(u'FunctionName')

            @property
            def PreviousItem(self):
                return self._getter(u'PreviousItem')


            @property
            def ItemInf(self):
                return self._getter(u'ItemInf')

            @property
            def CountIs(self):
                return self._getter(u'CountIs')

            @property
            def QuantifierIs(self):
                return self._getter(u'QuantifierIs')

            @property
            def Anonymous(self):
                return self._getter(u'Anonymous')

            @property
            def God(self):
                return self._getter(u'God')

            @property
            def Component(self):
                return self._getter(u'Component')

            @property
            def ActOuterPH(self):
                return self._getter(u'ActOuterPH')

            @property
            def QuantityIs(self):
                return self._getter(u'QuantityIs')

            @property
            def QuantityPair(self):
                return self._getter(u'QuantityPair')

            @property
            def Quantifier(self):
                return self._getter(u'Quantifier')

            @property
            def Number(self):
                return self._getter(u'Number')

            @property
            def Mood(self):
                return self._getter(u'Mood')

            @property
            def Declarative(self):
                return self._getter(u'Declarative')

            @property
            def Question(self):
                return self._getter(u'Question')

            @property
            def DefaultClass(self):
                return self._getter(u'DefaultClass')

            @property
            def DefaultAction(self):
                return self._getter(u'DefaultAction')

            @property
            def UnknownBiRelation(self):
                return self._getter(u'UnknownBiRelation')

            @property
            def HasAttribute(self):
                return self._getter(u'HasAttribute')

            @property
            def Attribute(self):
                return self._getter(u'Attribute')

            @property
            def Time(self):
                return self._getter(u'Time')

            @property
            def TimeIs(self):
                return self._getter(u'TimeIs')

            @property
            def SensorIs(self):
                return self._getter(u'SensorIs')

            @property
            def ObserverIs(self):
                return self._getter(u'ObserverIs')

            @property
            def FromId(self):
                return self._getter(u'FromId')

            @property
            def Target(self):
                return self._getter(u'Target')

            @property
            def Console(self):
                return self._getter(u'Console')

            @property
            def BeModified(self):
                return self._getter(u'BeModified')

            @property
            def Receive(self):
                return self._getter(u'Receive')

            @property
            def Send(self):
                return self._getter(u'Send')

            @property
            def UnderstoodAs(self):
                return self._getter(u'UnderstoodAs')

            @property
            def InheritFrom(self):
                return self._getter(u'InheritFrom')

            @property
            def SymbolInherit(self):
                return self._getter(u'SymbolInherit')

            @property
            def Nothingness(self):
                return self._getter(u'Nothingness')

            @property
            def InnerSelf(self):
                return self._getter(u'InnerSelf')

            @property
            def Word(self):
                return self._getter(u'Word')

            @property
            def Object(self):
                return self._getter(u'Object')

            @property
            def NotUnderstood(self):
                return self._getter(u'NotUnderstood')

            @property
            def FRestrict(self):
                return self._getter(u'FRestrict')

            @property
            def BRestrict(self):
                return self._getter(u'BRestrict')

            def _getter(self, symbol):
                '''
                根据英文名称返回其新加入的值，和set_id_by_name配合使用。
                '''
                return self._id_dict[symbol][1]

            def set_id_by_name(self, name, object_id):
                '''
                为original_real_object_dict属性添加新Key-[Value]。
                '''
                self._id_dict[name][1] = object_id

            def get_id_by_name(self, name):
                '''
                根据英文名字获得其ID
                '''
                self._id_dict.get(name, None)

            def get_name_by_id(self, object_id):
                '''
                根据ID获得其英文名字
                '''
                for _k, _v in self._id_dict.iteritems():
                    if _v[1] == object_id:
                        return _k

            def get_display(self, name):
                '''
                根据英文名称返回中文名称
                '''
                return self._id_dict[name][0]

        self.original_real_object_name_dict = OriginalRealObjectName(self.original_real_object_dict)

OID = GlobalDefine().original_real_object_name_dict