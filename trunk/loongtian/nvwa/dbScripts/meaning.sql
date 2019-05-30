-- Table: public.metareal

-- DROP TABLE public.metareal;

CREATE TABLE public.tbl_meaning
(
  uid character(32) NOT NULL, -- 上一层(知识链/动作对象)的ID
  utype integer, --上一层(知识链/动作对象)的类型
  kid character(32) NOT NULL, -- 下一层(一定是知识链)的ID
  threshold double precision DEFAULT 100.0, -- 阀值，表示上一层(知识链/动作对象)与下一层(一定是知识链)的紧密关系程度。...
  isforget boolean DEFAULT true, -- 遗忘标记， 不可遗忘的是真理。
  isdel boolean DEFAULT false, -- 逻辑删除标记
  lasttime date DEFAULT now(), -- 最后使用时间。
  CONSTRAINT meaning_pkey PRIMARY KEY (uid, kid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.tbl_meaning
  OWNER TO postgres;
COMMENT ON TABLE public.tbl_meaning
  IS '上一层(知识链/动作对象)与下一层(一定是知识链)在意义上的关联关系';
COMMENT ON COLUMN public.tbl_meaning.uid IS '上一层(知识链/动作对象)的ID';
COMMENT ON COLUMN public.tbl_meaning.utype IS '上一层(知识链/动作对象)的类型';
COMMENT ON COLUMN public.tbl_meaning.kid IS '下一层(一定是知识链)的ID';
COMMENT ON COLUMN public.tbl_meaning.threshold IS '阀值，表示上一层(知识链/动作对象)与下一层(一定是知识链)的紧密关系程度。
例如：
    [牛-有-腿] --0.1-- [牛-所属物-腿]
    [牛-有-腿] --0.8-- [牛-组件-腿]
    阀值越小表示关系越紧密，或表示该语义越常用。
';
COMMENT ON COLUMN public.tbl_meaning.isforget IS '遗忘标记， 不可遗忘的是真理。';
COMMENT ON COLUMN public.tbl_meaning.isdel IS '逻辑删除标记';
COMMENT ON COLUMN public.tbl_meaning.lasttime IS '最后使用时间。';

