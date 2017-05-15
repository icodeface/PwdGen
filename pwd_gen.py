# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""


class PwdGen(object):

    def __init__(self, name, phone, birthday, numbers, words):
        """
        :param name: 姓名，例如 'ma-yun'
        :param phone: 手机号
        :param birthday: 生日
        :param numbers: 一些有意义的数字 例如 ['2017', '5']
        :param words: 一些有意义的词语 例如 ['fuck', 'sb']
        :type name: str
        :type phone: str
        :type birthday: str
        :type numbers: list
        :type words: list
        """
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.words = words
        self.numbers = numbers

    def handle_name(self):
        result = []
        if not self.name:
            return result
        name_chars = self.name.split('-')
        # 全拼
        result.append(''.join(name_chars))
        # 首字母缩写
        abbr = "".join([x[0] for x in name_chars])
        result.append(abbr)
        # []会被替换成其他的数字或字词
        result.append(abbr[0]+"[]"+abbr[1:])
        result.append(abbr[1:]+"[]"+abbr[0])
        # 姓氏
        first_name = name_chars[0]
        result.append(first_name)
        # 名
        last_name = "".join(name_chars[1:])
        result.append(last_name)
        # 姓 [] 名
        result.append(first_name+"[]"+last_name)
        result.append(last_name+"[]"+first_name)
        result.append(abbr[0]+"[]"+last_name)
        # 全小写\全大写\首字母大写
        result += [x.upper() for x in result]
        result += [x.capitalize() for x in result]
        result.append(first_name[0])
        result.append(first_name[0].upper())
        return result

    def handle_birthday(self):
        result = []
        if not self.birthday or len(self.birthday) < 1:
            return result

        year = self.birthday[0:4]
        month = self.birthday[4:6]
        day = self.birthday[6:]

        result.append(self.birthday)
        result.append(self.birthday[2:])
        result.append(year)
        result.append(month+day)

        if month[0] == '0':
            result.append(month[1]+day)
            result.append(month[1]+day+year)
            result.append(year+month[1]+day)

        if day[0] == '0':
            result.append(month+day[1])
            result.append(month+day[1]+year)
            result.append(year+month+day[1])
            result.append(month[1]+day[1])
            result.append(month[1]+day[1]+year)
            result.append(year+month[1]+day[1])

        return result

    def generate(self):
        passwords = set()

        alphas = self.handle_name()
        alphas += self.words

        numbers = [self.phone, ]
        numbers += self.handle_birthday()
        numbers += self.numbers

        additions = []
        with open('addition.lst') as af:
            additions += [x.lstrip().rstrip('\n') for x in af.readlines()]

        # alpha + number / number + alpha
        for alpha in alphas:
            passwords.update([alpha.replace("[]", add) if "[]" in alpha else add+alpha for add in additions])
            passwords.update([alpha.replace("[]", num) if "[]" in alpha else ''+num+alpha for num in numbers])
            passwords.update([alpha+num for num in numbers if "[]" not in alpha])

        for pwd in passwords.copy():
            passwords.update([pwd+addition for addition in filter(lambda x: len(x) < 5, additions)])

        return passwords


if __name__ == '__main__':
    name_ = 'ma-yun'
    phone_ = '13888888888'
    birthday_ = '19700521'
    numbers_ = ['1998', '2016']
    words_ = ['taobao', 'tamll', 'ali', 'alibaba']
    p = PwdGen(name=name_, phone=phone_, birthday=birthday_, numbers=numbers_, words=words_)
    with open('password.txt', 'a+') as f:
        f.truncate(0)
        for password in list(p.generate()):
            if len(password) > 5:
                f.write(password+'\n')

