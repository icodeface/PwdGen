# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from functools import reduce
from collections import OrderedDict

# the rule sequence reflects the priority
rules = {
    'common': [
        '{string.name}{number.birthday}',
        '{string.name}{number.key}',
        '{string.name}{number.phone}',
        '{string.key}{number.birthday}',
        '{string.key}{number.key}',
        '{string.key}{number.phone}',
        
        '{string.name}{string.key}',
        '{string.name}{special.suffix}',

        '{string}{number.key}',
        '{string}{string.key}',
        '{string.key}{string}',
        '{string.name}',

        '{number.birthday}{string.name}',
        '{number.key}{string}',
        '{number}{string.key}',
        '{number.phone}',
        '{number.birthday}',

        '{string.lover}520',
        '{string.lover}1314520',

        'love{number.lover}',
        'ilove{number.lover}',
        'loveu{number.lover}',
        'woai{number.lover}',
        'aini{number.lover}',
        'woaini{number.lover}',

        'love{string.lover}',
        'ilove{string.lover}',
        'loveu{string.lover}',
        'woai{string.lover}',
        'aini{string.lover}',
        'woaini{string.lover}',

        '{string.name}love{number.lover}',
        '{string.name}love{string.lover}',
        '520{string.lover}',

        '{string.name}{string.name}',
        '{string.name}{special.join}{string.name}',
        '{string.name}{special.join}{number.birthday}',
        '{string.name}{special.join}{number.key}',
        '{string.name}{special.join}{string.key}',
        '{string.key}{special.join}{number.key}',
        '{string.key}{special.join}{number.birthday}',
        '{number.birthday}{special.join}{string.name}',

        '{special.prefix}{number.key}',
        '{special.prefix}{number.phone}',
        '{special.prefix}{number.birthday}',
        '{special.prefix}{string.name}',

        '{special.prefix}{string.name}{special.suffix}',
        '{special.prefix}{number.key}{special.suffix}',
        '{special.prefix}{number.phone}{special.suffix}',
        '{special.prefix}{number.birthday}{special.suffix}',

        '{string.name}{number.birthday}{special.suffix}',
        '{string.key}{special.join}{string.key}',
        '{string.key}{special.join}{string.key}{special.suffix}',
    ],
    'full': [
        '{string}{string}',
        '{string}{number}',
        '{number}{string}',
        '{string}{special}',
        '{number}{special}',
        '{number}{number}',

        '{string}{number}{string}',
        '{number}{string}{number}',

        '{string}{string}{special}',
        '{string}{number}{special}',
        '{number}{string}{special}',
        '{number}{number}{special}',
        '{string}{special}{string}',
        '{string}{special}{number}',
        '{number}{special}{string}',
        '{number}{special}{number}',

        '{string}{string}{number}',
        '{string}{number}{number}',
        '{number}{number}{string}',
        '{number}{string}{string}',

        '{special}{string}',
        '{special}{number}',

        '{special}{string}{string}',
        '{special}{string}{number}',
        '{special}{number}{string}',
        '{special}{number}{number}',
    ]
}


class PwdGen(object):

    def __init__(self, name, nicks, phones, birthday, key_strings, key_numbers,
                 lover_strings, lover_numbers):
        """
        :param name: 姓名
        :param nicks: 网名
        :param phones: 手机号
        :param birthday: 生日
        :param key_strings: 公司名、项目名、网站名、历史密码中喜欢使用的单词
        :param key_numbers: 幸运数字、历史密码中喜欢使用的数字、农历生日
        :param lover_strings: 对象名字、网名
        :param lover_numbers: 对象生日、手机号、QQ
        """
        self.data = {
            'string': {
                'name': set(),  # 姓名相关、网名
                'lover': set(),  # 爱人的姓名、网名
                'key': set(),  # 公司名、项目名、历史密码中喜欢使用的单词
            },
            'number': {
                'birthday': set(),  # 生日相关
                'phone': set(),  # 手机相关
                'lover': set(),  # 爱人的生日、手机
                'key': set()  # 幸运数字、历史密码中喜欢使用的数字
            },
            'special': {
                'prefix': {'a', 'i'},
                'suffix': {'123', '111', '520', '321', '1314', '123456', '888888', '!', '~', '#$'},
                'join': {'@', '#', '_', '-'}
            }
        }
        self.data['string']['name'] |= self.handle_name(name)
        self.data['string']['name'].update(nicks)
        self.data['string']['lover'].update(lover_strings)
        self.data['string']['lover'].update([x.swapcase() for x in lover_strings])
        self.data['string']['key'].update(key_strings)
        self.data['string']['key'].update([x.swapcase() for x in key_strings])
        self.data['string']['key'].update(nicks)

        self.data['number']['phone'] |= self.handle_phones(phones)
        self.data['number']['birthday'] |= self.handle_birthday(birthday)
        self.data['number']['lover'].update(lover_numbers)
        self.data['number']['key'].update(key_numbers)
        self.data['number']['key'].update(lover_numbers)

    @classmethod
    def handle_name(cls, name: str) -> set:
        result = set()
        if not name:
            return result
        name_chars = name.lower().split('-')

        # 缩写
        abbr = "".join([x[0] for x in name_chars])
        result.add(abbr)
        result.add(abbr.upper())

        # 全拼
        result.add(''.join(name_chars))
        result.add(''.join(name_chars).upper())

        # 姓氏
        first_name = name_chars[0]
        result.add(first_name)
        result.add(first_name.upper())
        first_name_upper_first = first_name[0].upper()+first_name[1:]
        result.add(first_name_upper_first)

        # 姓氏首字母
        result.add(first_name[0])
        result.add(first_name[0].upper())

        # 名
        last_name = "".join(name_chars[1:])
        result.add(last_name)
        result.add(last_name.upper())
        result.add(last_name[0].upper()+last_name[1:])

        # 名缩写
        last_name_abbr = "".join([x[0] for x in name_chars[1:]])
        result.add(last_name_abbr)
        result.add(last_name_abbr.upper())

        # 姓全拼 + 名缩写
        result.add(first_name + last_name_abbr)
        result.add(first_name.upper() + last_name_abbr)
        result.add(first_name_upper_first + last_name_abbr)
        result.add(first_name_upper_first + last_name_abbr.upper())

        return result

    @classmethod
    def handle_birthday(cls, birthday: str) -> set:
        result = set()
        if not birthday or len(birthday) < 1:
            return result

        year = birthday[0:4]
        month = birthday[4:6]
        day = birthday[6:]

        result.add(birthday)
        result.add(birthday[2:])
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

    @classmethod
    def handle_phones(cls, phones: list) -> set:
        result = set()
        for phone in phones:
            result.add(phone)
            result.add(phone[-4:])
        return result

    @classmethod
    def parse_rule(cls, rule: str) -> list:
        """
        '{string.name}love{string.lover}'
        =>
        ['{string.name}', 'love', '{string.lover}']
        """
        parsed = []
        last_finish = True
        for char in rule:
            if char == '{':
                parsed.append('')
            elif last_finish:
                parsed.append('')
            parsed[len(parsed) - 1] = parsed[len(parsed) - 1] + char
            if char == '}':
                last_finish = True
                continue
            last_finish = False
        return parsed

    def prepare_items(self, parsed: list) -> list:
        """
        ['{string.name}', 'love', '{string.lover}']
        =>
        [self.data['string']['name'], ['love'], self.data['string']['lover']]
        """
        items = []
        for single_parsed in parsed:
            if single_parsed.startswith('{') and single_parsed.endswith('}'):
                key = single_parsed[1:-1]
                if '.' in key:
                    keys = key.split('.')
                    values = list(self.data.get(keys[0], {}).get(keys[1], []))
                else:
                    values = list(reduce(lambda x, y: x | y, self.data.get(key, {}).values()))
                if not values:
                    return []
                items.append(values)
            else:
                items.append([single_parsed])
        return items

    def generate(self, min_len=8, max_len=16):
        order_dict = OrderedDict()
        for rule in rules['common'] + rules['full']:
            parsed = self.parse_rule(rule)
            items_to_combine = self.prepare_items(parsed)
            length = len(items_to_combine)
            if length == 0:
                continue
            pwds = ['']
            for index, items in enumerate(items_to_combine):
                temp_pwds = []
                if index == length:
                    break
                for first in pwds:
                    for last in items:
                        temp_pwds.append(first + last)
                pwds = temp_pwds
            for pwd in pwds:
                if min_len <= len(pwd) <= max_len:
                    order_dict[pwd] = None
        return order_dict.keys()


if __name__ == '__main__':
    name_ = 'ma-hua-teng'
    nicks_ = ['pony', ]
    phones_ = ['13888888888', '13999999999']
    birthday_ = '19711029'
    key_strings_ = ['ponysoft', 'tencent', 'qq', 'tx']
    key_numbers_ = ['1998', '2018', '2019', '10001']
    lover_strings_ = list(PwdGen.handle_name('luo-yu-feng')) + ['phoenix', ]
    lover_numbers_ = list(PwdGen.handle_birthday('19850923'))

    p = PwdGen(name=name_, nicks=nicks_, phones=phones_, birthday=birthday_,
               key_strings=key_strings_, key_numbers=key_numbers_,
               lover_strings=lover_strings_, lover_numbers=lover_numbers_)

    try:
        from pprint import pprint
        pprint(p.data)
    except ImportError:
        pass

    with open('{}_pwd.txt'.format(name_), 'a+') as f:
        f.truncate(0)
        for password in list(p.generate()):
            f.write(password+'\n')
    print('result write to {}_pwd.txt'.format(name_))


