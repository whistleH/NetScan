import re

text = "这是一个网址 http://www.example.com，还有一个 https://other.example.com/path, http://www.1234.cc"

# 定义一个简单的 URL 正则表达式
url_pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

# 在文本中找出所有的 URL
urls = re.findall(url_pattern, text)

# 打印所有的 URL
for url in urls:
    print(url)
