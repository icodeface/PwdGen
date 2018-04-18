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
        self.name = name.lower()
        self.phone = phone
        self.birthday = birthday
        self.words = words
        self.numbers = numbers

    def handle_name(self):
        result = set()
        if not self.name:
            return result
        name_chars = self.name.split('-')

        # 全拼
        result.add(''.join(name_chars))

        # 首字母缩写
        abbr = "".join([x[0] for x in name_chars])
        result.add(abbr)
        result.add(abbr + abbr.upper())
        result.add(abbr.upper() + abbr)
        result.add(abbr + "[]" + abbr.upper())
        result.add(abbr.upper() + "[]" + abbr)
        result.add(abbr[0]+"[]"+abbr[1:])
        result.add(abbr[1:]+"[]"+abbr[0])

        # 姓氏
        first_name = name_chars[0]
        result.add(first_name)
        result.add(first_name[0])
        result.add(first_name[0].upper())

        # 名
        last_name = "".join(name_chars[1:])
        result.add(last_name)

        # 姓 [] 名
        result.add(first_name+"[]"+last_name)
        result.add(last_name+"[]"+first_name)
        result.add(abbr[0]+"[]"+last_name)

        # 全大写\首字母大写
        result |= set([x.upper() for x in result])
        result |= set([x.capitalize() for x in result])

        return result

    def handle_birthday(self):
        result = set()
        if not self.birthday or len(self.birthday) < 1:
            return result

        year = self.birthday[0:4]
        month = self.birthday[4:6]
        day = self.birthday[6:]

        result.add(self.birthday)
        result.add(self.birthday[2:])
        result.add(year)
        result.add(month+day)

        if month[0] == '0':
            result.add(month[1]+day)
            result.add(month[1]+day+year)
            result.add(year+month[1]+day)

        if day[0] == '0':
            result.add(month+day[1])
            result.add(month+day[1]+year)
            result.add(year+month+day[1])
            result.add(month[1]+day[1])
            result.add(month[1]+day[1]+year)
            result.add(year+month[1]+day[1])

        return result

    def generate(self):
        passwords = set()

        alphas = self.handle_name()
        alphas |= set(self.words)

        numbers = set(self.numbers)
        numbers |= self.handle_birthday()
        numbers.add(self.phone)

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
    # with open('password.txt', 'a+') as f:
    #     f.truncate(0)
    #     for password in list(p.generate()):
    #         if len(password) > 5:
    #             f.write(password+'\n')

