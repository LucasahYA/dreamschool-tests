def replace_repeated_chars(input_string, k):
    # 初始化输出字符串和一个字典，用于跟踪字符及其上次出现的位置
    output = ""
    last_seen = {}

    # 遍历输入字符串中的每个字符
    for i, char in enumerate(input_string):
        # 如果这个字符之前出现过，并且当前位置与上次出现位置的差值小于等于k，则用'-'替换
        if char in last_seen and i - last_seen[char] <= k:
            output += "-"
        else:
            output += char

        # 更新该字符的最后出现位置
        last_seen[char] = i

    return output


text_input = input('input：')
text = text_input.split(' ')[0]
k = float(text_input.split(' ')[1])
# 使用提供的示例测试函数
result = replace_repeated_chars(text, k)
print(f'output:{result}')

# 样例：
# Input: abcdefaxc 10
# Output abcdef-x-
#
# Input: abcdefaxcqwertba 10
# Output abcdef-x-qw-rtb-

