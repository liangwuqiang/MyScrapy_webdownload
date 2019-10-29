import string

text = 'I love you,but you do not love me.I feel sad!23333'

# 实例1：删除文中的标点符号
remove = string . punctuation
table1 = str.maketrans('', '', remove)

# 实例2：去掉指定的字符
# remove = "|\\?*<\":>+[]/'" # 替换文件命名中非法字符
remove = 'aeiou123'
table2 = str.maketrans('_', '_', remove)

# 实例3：将指定字符替换成其他字符
remove = 'aeiou'
replace = '12345'
table3 = str.maketrans(remove, replace)

print(text.translate(table1))
print(text.translate(table2))
print(text.translate(table3))
