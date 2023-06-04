def filter_status(status, keyword, str_list):
    # 首先验证输入的状态码
    if len(status) != 3 or not status[0].isdigit() or int(status[0]) not in [2, 3, 4, 5] or (status[1:] != "xx" and not status[1:].isdigit()):
        return 'Invalid status code'

    result = []
    for string in str_list:
        str_status, url = string.split(',')
        # 检查状态码是否匹配
        if status[1:] == 'xx':
            if str_status[0] != status[0]:
                continue
        else:
            if str_status != status:
                continue
        # 检查URL是否包含关键词
        if keyword not in url:
            continue
        # 如果状态码和关键词都匹配，则将此字符串添加到结果列表中
        result.append(string)

    return result


# 测试函数
str_list = ["203,http://127.0.0.1:80/%EXT%.old",
            "303,http://127.0.0.1:80/%3f/",
            "403,http://127.0.0.1:80/%EXT%",
            "503,http://127.0.0.1:80/%EXT%.tgz",
            "402,http://127.0.0.1:80/%EXT%.bak",
            "404,http://127.0.0.1:80/%EXT%.tar",
            "403,http://127.0.0.1:80/%EXT%.txt",
            "201,http://127.0.0.1:80/%EXT%.php",
            "200,http://127.0.0.1:80/%ff"]
print(filter_status('3xx', '%EXT%', str_list))

with open('log/aHR0cDovLzEyNy4wLjAuMTo4MC0yMDIzLTA2LTA0IDE2OjQ5OjU0LjQ3ODY0Nw==', 'r') as file:
    lines = file.readlines()

print(["1", "2"] == "Invalid status code")
