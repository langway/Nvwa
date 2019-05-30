-- Database: Nvwa

DROP DATABASE "Nvwa";

CREATE DATABASE "Nvwa"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Chinese (Simplified)_China.936'
    LC_CTYPE = 'Chinese (Simplified)_China.936'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE "Nvwa"
    IS '人工智能Nvwa';


-- Table: public."tbl_metaData"

-- DROP TABLE public."tbl_metaData";

CREATE TABLE public."tbl_metaData"
(
    mid character(32) COLLATE pg_catalog."default" NOT NULL,
    type integer,
    mvalue text COLLATE pg_catalog."default" NOT NULL,
    weight double precision,
    recognized boolean DEFAULT true,
    remark text COLLATE pg_catalog."default",
    priority integer,
    isforgetable boolean DEFAULT true,
    isdel boolean DEFAULT false,
    createtime timestamp with time zone,
    updatetime timestamp with time zone,
    lasttime timestamp with time zone DEFAULT now(),
    CONSTRAINT metadata_pkey PRIMARY KEY (mid),
    CONSTRAINT metadata_mvalue_key UNIQUE (mvalue)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."tbl_metaData"
    OWNER to postgres;
COMMENT ON TABLE public."tbl_metaData"
    IS '女娲中的MetaData输入
语义载体经过《MetaData网》进行分词，分词之后的词组存入到MetaData表中。';

COMMENT ON COLUMN public."tbl_metaData".mid
    IS '词组ID';

COMMENT ON COLUMN public."tbl_metaData".type
    IS '词组载体类型，
100：文字类型
200：声音类型
300：图像类型
注意：需要和程序中的枚举类对应上。';

COMMENT ON COLUMN public."tbl_metaData".mvalue
    IS '媒体值，
当type为文字时，保存的是文字字符串
当type为声音或图像时，保存的是声音或图像的URI或对象地址';

COMMENT ON COLUMN public."tbl_metaData".weight
    IS '在元数据网中出现的频率';

COMMENT ON COLUMN public."tbl_metaData".remark
    IS '备注说明，程序中无实际意义。';

COMMENT ON COLUMN public."tbl_metaData".priority
    IS '优先级。';

COMMENT ON COLUMN public."tbl_metaData".isforgetable
    IS '是否可以遗忘的标记， 不可遗忘的是真理。';

COMMENT ON COLUMN public."tbl_metaData".isdel
    IS '逻辑删除标记';

COMMENT ON COLUMN public."tbl_metaData".createtime
    IS '创建时间。（使用trigger）';

COMMENT ON COLUMN public."tbl_metaData".updatetime
    IS '更新时间。（使用trigger）';

COMMENT ON COLUMN public."tbl_metaData".lasttime
    IS '最近的使用时间。（使用trigger。）';

COMMENT ON COLUMN public."tbl_metaData".recognized
    IS '是否识别的标志。
在系统运行中，经常会出现未能提取，但被截取出来的情况，例如：‘住房市级备案’，住房、备案可能都已识别，经过切割，市级也会被切割出来，但不属于已识别，需要等待后续的，例如反问等进行处理。';
-- Table: public."tbl_metaNet"

DROP TABLE public."tbl_metaNet";

CREATE TABLE public."tbl_metaNet"
(
    mnid character(32) COLLATE pg_catalog."default" NOT NULL,
    startid character(32) COLLATE pg_catalog."default",
    stype integer,
    endid character(32) COLLATE pg_catalog."default",
    etype integer,
    weight double precision,
    related_meta character(32) COLLATE pg_catalog."default",
    related_knowledge character(32) COLLATE pg_catalog."default",
    t_graph text COLLATE pg_catalog."default",
    t_chain text COLLATE pg_catalog."default",
    s_chain text COLLATE pg_catalog."default",
    m_chain text COLLATE pg_catalog."default",
    createtime timestamp with time zone,
    updatetime timestamp with time zone,
    lasttime timestamp with time zone DEFAULT now(),
    isdel boolean DEFAULT false,
    isforgetable boolean DEFAULT false,
    CONSTRAINT "tbl_metaNet_pkey" PRIMARY KEY (mnid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."tbl_metaNet"
    OWNER to postgres;
COMMENT ON TABLE public."tbl_metaNet"
    IS '元数据网络，用于记录一个句子之间的元数据的关联（n元丁字型结构的字符块链表）
相当于Ngram中字符块之间的二元、三元关系的记录：
二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解
目前使用邻接匹配法——ngram，根据“元数”，进行二元、三元关系计算，对匹配出来的字符块链进行排序
# 传统的可能性（路径L的概率[路径依赖]）计算公式为：
    # 【二元】P(L) = P(w2|w1) * P(w3|w2) * P(w4|w3) *……* P(wk|w(k-1))*P(w1) * P(w2) * P(w3)…… * P(wk)
    # 【三元】P(L) = P(w3|w1w2) * P(w4|w3w2) * P(w5|w4w3) *……* P(wk|w(k-2)w(k-1))*P(w1) * P(w2) * P(w3)…… * P(wk)
    # 这里考虑以下几点：
    # 当前元数的可能性，应与该元数关系的可能性正相关，与该元数所包含字符块的可能性之和正相关，而不应仅仅是乘积关系
    # 而各字符链的可能性之间的关系，应该是累加的
    # 同时，这种概率还与词块的长度正相关，实际词频应该为：词块词频*词块长度
    # 所以，这里将上述公式修改为：
    # 【二元】P(L) = P(w2|w1) * （P(w1)*len(w1) + P(w2)*len(w2)） +
    #                P(w3|w2) * （P(w2)*len(w2) + P(w3)*len(w3)）+ …… +
    #                P(wk|w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1))
    # 【三元】P(L) = P(w3|w1w2) * （P(w1)*len(w1) + P(w2)*len(w1)+ P(w3)*len(w3)） +
    #                P(w4|w2w3) * （P(w2)*len(w2) + P(w3)*len(w3)+ P(w4)*len(w4)）+ …… +
    #                P(wk|w(k-2)w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)+P(w(k-2)*len(wk-2))
    # 另外，要避免分词多反而造成可能性大的情况，所以要对可能性进行加权平均
    # 【二元】P(L) = (P(w2|w1) * （P(w1)*len(w1) + P(w2)*len(w2)） +
    #                P(w3|w2) * （P(w2)*len(w2) + P(w3)*len(w3)）+ …… +
    #                P(wk|w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)))/(k-1)
    # 【三元】P(L) = P(w3|w1w2) * （P(w1)*len(w1) + P(w2)*len(w1)+ P(w3)*len(w3)） +
    #                P(w4|w2w3) * （P(w2)*len(w2) + P(w3)*len(w3)+ P(w4)*len(w4)）+ …… +
    #                P(wk|w(k-2)w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)+P(w(k-2)*len(wk-2))/(k-2)';

COMMENT ON COLUMN public."tbl_metaNet".startid
    IS '起点ID';

COMMENT ON COLUMN public."tbl_metaNet".stype
    IS '起点ID的类型（元数据，或元数据网）';

COMMENT ON COLUMN public."tbl_metaNet".etype
    IS '终点ID的类型（元数据，或元数据网）';

COMMENT ON COLUMN public."tbl_metaNet".weight
    IS '权重，相当于Ngram中的词块的连接值';

COMMENT ON COLUMN public."tbl_metaNet".related_meta
    IS '相关连的元数据，例如：中国-人民-解放军，关联的元数据就是“中国人民解放军”';

COMMENT ON COLUMN public."tbl_metaNet".related_knowledge
    IS '元数据网相关的知识网。
[我,知道,中国,人民,解放军,是,最棒,的]相关的知识网：
[我,知道,[[中国,人民,解放军],是,[最棒,的]]]';

COMMENT ON COLUMN public."tbl_metaNet".t_graph
    IS '   1、 t_graph 是一个T字型结构的由metaData、metaNetItem的Id组成的数组(嵌套代表一条metaNet)。
   2、 t_chain 是一个T字型结构的由metaData的Id组成的数组(嵌套代表一条metaNet)。
    3、s_chain  是一个未经T字型结构处理的由metaData的Id组成序列数组
    4、m_chain 是一个由外域（可能是个知识链，也可能是实际对象）、知识链的mnid组成的序列数组。

    eg:
    1、t_graph = [情人节,(mn8,[(mn7,[(mn6,[小明, 给]), 小丽]), (mn5,[(mn1,[一, 朵]), (mn4,[(mn3,[红色, 的]), (mn2,[玫瑰, 花]]))])])]
    2、t_chain = [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]
    3、s_chain = [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    4、m_chain =[情人节,mn8,mn5,mn4,mn2]';

COMMENT ON COLUMN public."tbl_metaNet".t_chain
    IS '   1、 t_graph 是一个T字型结构的由metaData、metaNetItem的Id组成的数组(嵌套代表一条metaNet)。
   2、 t_chain 是一个T字型结构的由metaData的Id组成的数组(嵌套代表一条metaNet)。
    3、s_chain  是一个未经T字型结构处理的由metaData的Id组成序列数组
    4、m_chain 是一个由外域（可能是个知识链，也可能是实际对象）、知识链的mnid组成的序列数组。

    eg:
    1、t_graph = [情人节,(mn8,[(mn7,[(mn6,[小明, 给]), 小丽]), (mn5,[(mn1,[一, 朵]), (mn4,[(mn3,[红色, 的]), (mn2,[玫瑰, 花]]))])])]
    2、t_chain = [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]
    3、s_chain = [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    4、m_chain =[情人节,mn8,mn5,mn4,mn2]';

COMMENT ON COLUMN public."tbl_metaNet".s_chain
    IS '   1、 t_graph 是一个T字型结构的由metaData、metaNetItem的Id组成的数组(嵌套代表一条metaNet)。
   2、 t_chain 是一个T字型结构的由metaData的Id组成的数组(嵌套代表一条metaNet)。
    3、s_chain  是一个未经T字型结构处理的由metaData的Id组成序列数组
    4、m_chain 是一个由外域（可能是个知识链，也可能是实际对象）、知识链的mnid组成的序列数组。

    eg:
    1、t_graph = [情人节,(mn8,[(mn7,[(mn6,[小明, 给]), 小丽]), (mn5,[(mn1,[一, 朵]), (mn4,[(mn3,[红色, 的]), (mn2,[玫瑰, 花]]))])])]
    2、t_chain = [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]
    3、s_chain = [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    4、m_chain =[情人节,mn8,mn5,mn4,mn2]';

COMMENT ON COLUMN public."tbl_metaNet".m_chain
    IS '   1、 t_graph 是一个T字型结构的由metaData、metaNetItem的Id组成的数组(嵌套代表一条metaNet)。
   2、 t_chain 是一个T字型结构的由metaData的Id组成的数组(嵌套代表一条metaNet)。
    3、s_chain  是一个未经T字型结构处理的由metaData的Id组成序列数组
    4、m_chain 是一个由外域（可能是个知识链，也可能是实际对象）、知识链的mnid组成的序列数组。

    eg:
    1、t_graph = [情人节,(mn8,[(mn7,[(mn6,[小明, 给]), 小丽]), (mn5,[(mn1,[一, 朵]), (mn4,[(mn3,[红色, 的]), (mn2,[玫瑰, 花]]))])])]
    2、t_chain = [情人节,[[[小明, 给], 小丽], [[一, 朵], [[红色, 的], [玫瑰, 花]]]]
    3、s_chain = [情人节,小明, 给, 小丽,一, 朵,红色, 的, 玫瑰, 花]
    4、m_chain =[情人节,mn8,mn5,mn4,mn2]';

COMMENT ON COLUMN public."tbl_metaNet".createtime
    IS '创建时间。（使用trigger）';

COMMENT ON COLUMN public."tbl_metaNet".updatetime
    IS '更新时间。（使用trigger）';

COMMENT ON COLUMN public."tbl_metaNet".lasttime
    IS '最后使用时间。（使用trigger）';

COMMENT ON COLUMN public."tbl_metaNet".isdel
    IS '是否删除的标记。';

COMMENT ON COLUMN public."tbl_metaNet".isforgetable
    IS '是否可以遗忘的标记。不可删除是永久的。';
-- Table: public."tbl_realObject"

-- DROP TABLE public."tbl_realObject";

CREATE TABLE public."tbl_realObject"
(
    pk_id character(32) COLLATE pg_catalog."default" NOT NULL,
    fk_pattern character varying(255) COLLATE pg_catalog."default",
    fk_meaning text COLLATE pg_catalog."default",
    remark text COLLATE pg_catalog."default",
    type integer,
    isforgetable boolean DEFAULT true,
    isdel boolean DEFAULT false,
    lasttime date DEFAULT now(),
    CONSTRAINT realobject_pkey PRIMARY KEY (pk_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."tbl_realObject"
    OWNER to postgres;
COMMENT ON TABLE public."tbl_realObject"
    IS '女娲中的实际对象表示。';

COMMENT ON COLUMN public."tbl_realObject".pk_id
    IS '实际对象ID。';

COMMENT ON COLUMN public."tbl_realObject".fk_pattern
    IS 'RealObject的模式。';

COMMENT ON COLUMN public."tbl_realObject".fk_meaning
    IS '含义（指的是），当RealObject为动词时。';

COMMENT ON COLUMN public."tbl_realObject".remark
    IS '备注说明，程序中无实际意义。';

COMMENT ON COLUMN public."tbl_realObject".type
    IS 'RealObject类型，包括：
实对象 SOLID
虚对象 VIRTUAL
动作 ACTION
修限 MOTIFY
集合 COLLECTION。
';

COMMENT ON COLUMN public."tbl_realObject".isforgetable
    IS '是否可以遗忘的标记， 不可遗忘的是真理。';

COMMENT ON COLUMN public."tbl_realObject".isdel
    IS '逻辑删除标记';

COMMENT ON COLUMN public."tbl_realObject".lasttime
    IS '最后使用时间。';

-- Table: public."rel_metaData_realObject"

-- DROP TABLE public."rel_metaData_realObject";

CREATE TABLE public."rel_metaData_realObject"
(
    "metaData_id" character(32) COLLATE pg_catalog."default" NOT NULL,
    "realObject_id" character(32) COLLATE pg_catalog."default" NOT NULL,
    threshold double precision DEFAULT 100.0,
    isforgetable boolean DEFAULT true,
    isdel boolean DEFAULT false,
    lasttime date DEFAULT now(),
    remark character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT metareal_pkey PRIMARY KEY ("metaData_id", "realObject_id")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."rel_metaData_realObject"
    OWNER to postgres;
COMMENT ON TABLE public."rel_metaData_realObject"
    IS 'MetaData与RealObject的关系表，两者是多对多关系，
例如：
    MetaData[牛] -- RealObject[动物牛, 形容词牛]
    RealObject[动物牛] -- MetaData[牛, cow, 图片牛]
';

COMMENT ON COLUMN public."rel_metaData_realObject"."metaData_id"
    IS '元数据ID';

COMMENT ON COLUMN public."rel_metaData_realObject"."realObject_id"
    IS '实际对象ID';

COMMENT ON COLUMN public."rel_metaData_realObject".threshold
    IS '阀值，表示MetaData与RealObject的紧密关系程度。
例如：
    MetaData[牛] --0.1-- RealObject[动物牛]
    MetaData[牛] --0.8-- RealObject[形容词牛]
    阀值越小表示关系越紧密，或表示该语义越常用。
';

COMMENT ON COLUMN public."rel_metaData_realObject".isforgetable
    IS '是否可以遗忘的标记， 不可遗忘的是真理。';

COMMENT ON COLUMN public."rel_metaData_realObject".isdel
    IS '逻辑删除标记';

COMMENT ON COLUMN public."rel_metaData_realObject".lasttime
    IS '最后使用时间。';

COMMENT ON COLUMN public."rel_metaData_realObject".remark
    IS '备注（用来记录元数据的字符串）';



