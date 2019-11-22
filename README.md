# Doctors_relationship
Find relationship between doctors

### 执行.sql

进入mysql的控制台后，使用source命令执行

Mysql>source 【sql脚本文件的路径全名】

示例：source d:\test\ss.sql


### 字段说明
 字段      | 解释     
 ---------- | -----------  
 VPID             | ID     
 NAME             |医生姓名     
 DEGREE           | 学历<sup>1</sup>     
 UNIVERSITY1       | 毕业学校1     
 GRAD_YEAR1        | 毕业年份1<sup>2</sup>    
 UNIVERSITY2       | 毕业学校2     
 GRAD_YEAR2        | 毕业年份2  
 DISPLAY_TYPE     | 显示医生分类<sup>3</sup>
 TYPE             | 医生分类     
 SPECIALTIES      | 特长     
 CITY             | 城市     
 STATE            | 州     
 ADDRESS          | 地址     
 LATITUDE         | 维度     
 LONGITUDE        | 精度     
 YEAR_EXP         | 从医年限     
 NUMBER_OF_RATINGS| 打分数     
 OVERALL_RATINGS  | 总评     
 COMPANY          | 公司     
 URL              | 医生主页     
 CAMPAIGNS        | 组织<sup>4</sup>     
 OTHERS           | 预留列     
 <sup>注</sup> 主键为 Name|
 <sup>1</sup> 学历不唯一 形如 PHD, DDS |
 <sup>2</sup> 毕业年份为纯年份(1994)或Residency|
 <sup>3</sup> 分类为如下几类|
 Doctor; Dentist; Psychologist;|
 Optometrist; Podiatrist; Chiropractor|
<sup>4</sup> 5531条数据中包括如下组织|
docoordotcom; webmd_ep; zocdoc|

