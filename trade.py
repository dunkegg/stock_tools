import json
import os
from datetime import datetime

# 创建目录
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 加载数据
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 保存数据
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 获取个人文件路径
def get_person_file_paths(person):
    return f"stock_data/{person}_stocks.json", f"stock_data/{person}_trades.json"
def update_trade(person, stock_code, stock_name, quantity, price, action, date):
    stocks_file, trades_file = get_person_file_paths(person)
    
    # 加载持仓数据和交易记录
    stocks = load_data(stocks_file)
    trades = load_data(trades_file)
    
    # 确保该人存在
    if person not in stocks:
        stocks[person] = {'cash': 1000000.0}
    if person not in trades:
        trades[person] = []
    
    # 确保该股票存在
    if stock_code not in stocks[person]:
        if action == 'buy':
            stocks[person][stock_code] = {'name': stock_name, 'quantity': 0, 'avg_price': 0.0, 'cur_price': 0.0}
        else:
            print(f"没有股票 {stock_code} : {stock_name}，操作未执行。")

    stock = stocks[person][stock_code]
    cash = stocks[person]['cash']  # 当前现金
    
    if action == 'buy':
        # 买入时，检查现金是否足够
        total_cost = price * quantity
        if cash < total_cost:
            print(f"警告: {person} 现金不足，无法买入 {quantity} 股 {stock_name}，操作未执行。")
            return
        # 买入时，更新股数和均价，扣除现金
        total_cost = stock['avg_price'] * stock['quantity'] + price * quantity
        stock['quantity'] += quantity
        stock['avg_price'] = total_cost / stock['quantity']
        stocks[person]['cash'] -= total_cost
        trades[person].append({'action': action, 'quantity': quantity, 'price': price, 'date': date})
        stock['cur_price'] = price
    elif action == 'sell':
        # 卖出时，检查是否有足够的数量
        if stock['quantity'] < quantity:
            print(f"警告: 卖出的股票数量超过了持有的数量 ({stock['quantity']} 股)，操作未执行。")
            return
        # 卖出时，更新股数，增加现金
        stock['quantity'] -= quantity
        cash_received = price * quantity
        stocks[person]['cash'] += cash_received
        
        # 重新计算均价（只考虑剩余股票）
        if stock['quantity'] > 0:
            remaining_cost = stock['avg_price'] * (stock['quantity'] + quantity) - cash_received
            stock['avg_price'] = remaining_cost / stock['quantity']
        else:
            stock['avg_price'] = 0.0  # 如果卖完了，均价置为0
        
        trades[person].append({'action': action, 'quantity': quantity, 'price': price, 'date': date})
        stock['cur_price'] = price
    # 保存数据
    save_data(stocks_file, stocks)
    save_data(trades_file, trades)

