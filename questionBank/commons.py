"""this file used for some common variables"""
from enum import Enum

grades = ("高{}".format(grade+1) for grade in range(3))
classnums = ("{}班".format(classnum+1) for classnum in range(16))
subject_lists = ("语文", "数学", "外语", "物理", "化学", "生物", "政治", "历史", "地理", "信息技术", "通用技术")
information_technology_question_category = ["01信息与信息技术专题", "02网页邮件专题", "03多媒体概念专题", "04二进制编码专题",
                                            "05容量计算专题", "06人工智能专题", "07Access专题", "08Photoshop专题",
                                            "09Flash专题", "10Word&OCR专题", "11GoldWave专题", "12流程图专题", "13公式函数专题",
                                            "14数论专题", "15文本分析专题", "16去重专题", "17数组应用专题", "18可能不可能专题", "19排序专题",
                                            "20对分专题", "21vb数据库", "22其他", "23Excel填空", "24flash填空", "25VB填空_学考"]

subject_category_dict = {"信息技术": information_technology_question_category}   # used for store the subject categories
# question_types = ["choose", "blanks"]


class QuestionTypes(Enum):
    """corresponding to attribute (question_type) of question model"""

    选择题 = "choose"
    填空题 = "blanks"