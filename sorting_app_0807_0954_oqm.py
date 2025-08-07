# 代码生成时间: 2025-08-07 09:54:49
from bottle import route, run, request, response
from functools import cmp_to_key
import json

# 定义排序算法
# 升序排序
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 降序排序
def bubble_sort_descending(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] < arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 比较函数，用于自定义排序
def compare_strings(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0

# 自定义排序
def custom_sort(arr, compare):
    return sorted(arr, key=cmp_to_key(compare))

# 定义API路由
@route('/sort', method='POST')
def sort_numbers():
    try:
        # 获取请求体中的JSON数据
        data = request.json
        
        # 检查数据是否包含所需的键
        if 'numbers' not in data:
            raise ValueError('Missing key: numbers')
        if 'order' not in data:
            raise ValueError('Missing key: order')
        
        # 获取排序数组和排序方式
        numbers = data['numbers']
        sort_order = data['order'].lower()
        
        # 根据sort_order调用不同的排序函数
        if sort_order == 'ascending':
            sorted_numbers = bubble_sort(numbers.copy())
        elif sort_order == 'descending':
            sorted_numbers = bubble_sort_descending(numbers.copy())
        elif sort_order == 'custom':
            if 'custom_compare' not in data:
                raise ValueError('Missing key for custom sort: custom_compare')
            sorted_numbers = custom_sort(numbers.copy(), data['custom_compare'])
        else:
            raise ValueError('Invalid sort order')
        
        # 设置响应格式为JSON
        response.content_type = 'application/json'
        
        # 返回排序后的数组
        return json.dumps({'sorted_numbers': sorted_numbers})
    except Exception as e:
        # 返回错误信息
        response.status = 400
        return json.dumps({'error': str(e)})

# 运行Bottle应用程序
run(host='localhost', port=8080, debug=True)