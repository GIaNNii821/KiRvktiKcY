# 代码生成时间: 2025-09-21 23:52:31
# inventory_management.py
# 使用Bottle框架创建一个简单的库存管理系统

from bottle import route, run, request, response
import json

# 模拟数据库，使用字典存储库存数据
inventory = {
    'item1': {'quantity': 100},
    'item2': {'quantity': 150},
    'item3': {'quantity': 200}
}

# 获取库存信息
@route('/inventory/<item_id>')
def get_inventory(item_id):
    try:
        # 检查项目是否存在
        if item_id not in inventory:
            response.status = 404
            return json.dumps({'error': 'Item not found'})
        # 返回项目库存信息
        return json.dumps(inventory[item_id])
    except Exception as e:
        response.status = 500
        return json.dumps({'error': 'Internal Server Error', 'message': str(e)})

# 更新库存数量
@route('/inventory/<item_id>', method='PUT')
def update_inventory(item_id):
    try:
        # 解析JSON请求体
        data = request.json
        if 'quantity' not in data:
            response.status = 400
            return json.dumps({'error': 'Missing quantity parameter'})
        # 更新库存数量
        if item_id in inventory:
            inventory[item_id]['quantity'] = data['quantity']
            return json.dumps(inventory[item_id])
        else:
            response.status = 404
            return json.dumps({'error': 'Item not found'})
    except Exception as e:
        response.status = 500
        return json.dumps({'error': 'Internal Server Error', 'message': str(e)})

# 主函数，启动Bottle服务器
def main():
    run(host='localhost', port=8080)

if __name__ == '__main__':
    main()