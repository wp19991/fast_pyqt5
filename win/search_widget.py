import os
import json
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox
from ui.search_widget import Ui_search_widget as search_wid

from data.zong import get_tk_data


class search_widget(QWidget, search_wid):
    def __init__(self, parent=None):
        super(search_widget, self).__init__(parent)
        self.setupUi(self)

        self.json_data = get_tk_data()

        self.show_json_data_index = 0
        self.match_condition_json_data_index_list = [0]

        self.open_json_file_pushButton.clicked.connect(self.open_json_file_pushButton_event)
        self.show_ans_pushButton.clicked.connect(self.show_ans_pushButton_event)
        self.search_pushButton.clicked.connect(self.search_pushButton_event)
        self.pre_res_pushButton.clicked.connect(self.pre_res_pushButton_event)
        self.next_res_pushButton.clicked.connect(self.next_res_pushButton_event)
        self.copy_simple_json_pushButton.clicked.connect(self.copy_simple_json_pushButton_event)
        self.copy_this_question_json_pushButton.clicked.connect(self.copy_this_question_json_pushButton_event)
        self.copy_this_question_format_pushButton.clicked.connect(self.copy_this_question_format_pushButton_event)
        self.about_pushButton.clicked.connect(self.about_pushButton_event)

        self.res_comboBox.currentIndexChanged.connect(self.res_comboBoxChanged_event)

        self.fresh_select_search_book_comboBox()
        self.fresh_question_info(json_data_index=self.show_json_data_index, is_show_ans=True)
        self.search_pushButton_event()

    def copy_simple_json_pushButton_event(self):
        now_str = json.dumps(get_tk_data(), ensure_ascii=False, indent=4)
        clipboard = QApplication.clipboard()
        clipboard.setText(now_str)

    def about_pushButton_event(self):
        QMessageBox.information(self, "关于软件-现在已经开源",
                                "GitHub:wp19991\n项目地址:https://gitee.com/wp19991/fast_pyqt5"
                                "\n可以自己按照示例的json数据进行导入题目\n支持单选题目，多选题目\n点击复制示例json"
                                "数据后粘贴到文本文档里面\n根据格式创建属于自己的json文件",
                                QMessageBox.Yes)

    def copy_this_question_json_pushButton_event(self):
        now_index_data = self.json_data[self.show_json_data_index]
        now_str = json.dumps(now_index_data, ensure_ascii=False, indent=4)
        clipboard = QApplication.clipboard()
        clipboard.setText(now_str)

    def copy_this_question_format_pushButton_event(self):
        now_index_data = self.json_data[self.show_json_data_index]
        temp_ans = ''
        temp_abcd = ['A', 'B', 'C', 'D']
        for d in now_index_data['答案']:
            temp_ans += temp_abcd[d]
        format_res = '''题目：{}\nA.{}\nB.{}\nC.{}\nD.{}\n\n参考答案：{}\n解析：{}\n''' \
            .format(now_index_data['题目'],
                    now_index_data['选项'][0],
                    now_index_data['选项'][1],
                    now_index_data['选项'][2],
                    now_index_data['选项'][3],
                    temp_ans,
                    now_index_data['解析'])
        clipboard = QApplication.clipboard()
        clipboard.setText(format_res)

    def res_comboBoxChanged_event(self):
        now_index = int(self.res_comboBox.currentText().split('-')[0])
        self.show_json_data_index = now_index
        self.fresh_question_info(json_data_index=now_index)

    def pre_res_pushButton_event(self):
        now_current_index = self.res_comboBox.currentIndex()
        pre_current_index = now_current_index - 1 if now_current_index - 1 >= 0 else now_current_index
        self.res_comboBox.setCurrentIndex(pre_current_index)
        now_index = int(self.res_comboBox.currentText().split('-')[0])
        self.show_json_data_index = now_index
        self.fresh_question_info(json_data_index=now_index)

    def next_res_pushButton_event(self):
        now_current_index = self.res_comboBox.currentIndex()
        next_current_index = now_current_index + 1 if now_current_index + 1 < len(
            self.match_condition_json_data_index_list) else now_current_index
        self.res_comboBox.setCurrentIndex(next_current_index)
        now_index = int(self.res_comboBox.currentText().split('-')[0])
        self.show_json_data_index = now_index
        self.fresh_question_info(json_data_index=now_index)

    def search_pushButton_event(self):
        search_book = self.select_search_book_comboBox.currentText()
        search_keyword = self.search_keyword_lineEdit.text()
        if search_keyword is None:
            search_keyword = ''
        self.match_condition_json_data_index_list = []
        for i, d in enumerate(self.json_data):
            if search_book not in [d['书本'], '全部']:
                continue
            d_str = str(json.dumps(d, ensure_ascii=False))
            if search_keyword in d_str:
                self.match_condition_json_data_index_list.append(i)
        if len(self.match_condition_json_data_index_list) == 0:
            self.search_nums_label.setText(str(len(self.match_condition_json_data_index_list)) + '条记录')
            self.fresh_question_info(json_data_index=0)
            return
        # 更新搜索到多少条
        print(str(len(self.match_condition_json_data_index_list)) + '条记录')
        self.search_nums_label.setText(str(len(self.match_condition_json_data_index_list)) + '条记录')
        # 更新res_comboBox
        self.res_comboBox.currentIndexChanged.disconnect()
        self.res_comboBox.clear()
        temp_res_combox = []
        for i, d in enumerate(self.match_condition_json_data_index_list):
            if search_keyword != '':
                temp_add_item = str(d) + "-..."
                temp_add_item += str(json.dumps(self.json_data[d], ensure_ascii=False)).split(search_keyword)[0][-10:] + \
                                 search_keyword + \
                                 str(json.dumps(self.json_data[d], ensure_ascii=False)).split(search_keyword)[1][:10]
            else:
                temp_add_item = str(d) + "-..." + json.dumps(self.json_data[d], ensure_ascii=False)
            temp_res_combox.append(temp_add_item[:30] + '...')
        self.res_comboBox.addItems(temp_res_combox)
        self.res_comboBox.currentIndexChanged.connect(self.res_comboBoxChanged_event)

        # 默认展示第0条
        self.fresh_question_info(json_data_index=self.match_condition_json_data_index_list[0])

    def show_ans_pushButton_event(self):
        self.fresh_question_info(json_data_index=self.show_json_data_index, is_show_ans=True)

    def fresh_question_info(self, json_data_index=0, is_show_ans=False):
        json_data_temp = self.json_data[json_data_index]
        # 问题是单选还是多选
        question_type = '题目-单选' if len(json_data_temp['答案']) == 1 else '题目-多选'
        self.question_groupBox.setTitle(question_type)
        # 章节信息
        self.local_chapter_label.setText(json_data_temp['书本'] + '-' + json_data_temp['章节'])
        # 题目
        self.question_label.setText('题目：' + json_data_temp['题目'])
        # 选项1
        self.A_checkBox.setText('A.' + json_data_temp['选项'][0])
        # 选项2
        self.B_checkBox.setText('B.' + json_data_temp['选项'][1])
        # 选项3
        self.C_checkBox.setText('C.' + json_data_temp['选项'][2])
        # 选项4
        self.D_checkBox.setText('D.' + json_data_temp['选项'][3])

        if is_show_ans or self.is_auto_show_ans_checkBox.isChecked():
            # 更新答案
            temp_ans = '正确答案：'
            temp_abcd = ['A', 'B', 'C', 'D']
            for d in json_data_temp['答案']:
                temp_ans += temp_abcd[d]
            self.ans_label.setText(temp_ans)
            # 更新解析
            self.analysis_label.setText('解析：' + json_data_temp['解析'])
            return
        self.ans_label.setText('正确答案：')
        # 更新解析
        self.analysis_label.setText('解析：')

    def fresh_select_search_book_comboBox(self):
        # 更新书本的选择
        book_item = set()
        for i in self.json_data:
            book_item.add(i["书本"])
        book_item = ['全部'] + list(book_item)
        self.select_search_book_comboBox.clear()
        self.select_search_book_comboBox.addItems(book_item)

    def open_json_file_pushButton_event(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   caption="选择json文件路径",
                                                   directory=os.path.join(os.path.expanduser("~"), 'Desktop'),
                                                   filter='json文件(*.json *.txt)')
        if file_path == "":
            self.json_file_path_lineEdit.setText('请选择json文件路径')
            return
        self.json_file_path_lineEdit.setText(file_path)
        with open(self.json_file_path_lineEdit.text(), 'r', encoding='utf-8') as f:
            temp_json_data = json.loads(''.join(f.readlines()))
        # 对json文件进行格式检查 TODO
        self.json_data = temp_json_data
        self.show_json_data_index = 0
        # 更新书本的选择
        self.fresh_select_search_book_comboBox()
        # 显示第一题
        self.fresh_question_info(json_data_index=self.show_json_data_index)
        # 进行搜索
        self.search_pushButton_event()
