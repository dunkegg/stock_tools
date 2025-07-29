import json
import os
from dataclasses import dataclass, field
from typing import List
from datetime import datetime
import shutil
# 创建目录
def create_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)  # 删除整个目录
    os.makedirs(directory)  # 创建空目录

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
        stocks[person] = {'cash': 770000.0}
    if person not in trades:
        trades[person] = []
    
    # 确保该股票存在
    if stock_code not in stocks[person]:
        if action == 'buy':
            stocks[person][stock_code] = {'name': stock_name, 'quantity': 0, 'avg_price': 0.0, 'cur_price': 0.0}
        else:
            print(f"{person} 没有股票 {stock_code} : {stock_name} 在 {date} ，卖出操作未执行。")

    stock = stocks[person][stock_code]
    cash = stocks[person]['cash']  # 当前现金
    
    if action == 'buy':
        # 买入时，检查现金是否足够
        total_cost = price * quantity
        if cash < total_cost:
            print(f"警告: {person} 现金不足，为{cash}，无法买入 {quantity} 股 {stock_code}:{stock_name} 在 {date}，操作未执行。")
            return
        # 买入时，更新股数和均价，扣除现金
        tmp_value = stock['avg_price'] * stock['quantity'] + price * quantity
        stock['quantity'] += quantity
        stock['avg_price'] = tmp_value / stock['quantity']
        stocks[person]['cash'] -= total_cost
        print(f" {person} 买入 {stock_code}:{stock_name}  {quantity} 股，花费{price*quantity}在 {date},剩余现金{stocks[person]['cash']}。")
        trades[person].append({'action': action, 'quantity': quantity,'stock code': stock_code,'stock name': stock_name,'price': price, 'date': date})
        # trades[person].append({'action': action, 'quantity': quantity, 'price': price, 'date': date})
        stock['cur_price'] = price
    elif action == 'sell':
        # 卖出时，检查是否有足够的数量
        if stock['quantity'] < quantity:
            print(f"警告: {person}卖出{stock_code}:{stock_name}的股票数量超过了持有的数量 ({stock['quantity']} 股) 在 {date}，操作未执行。")
            return
        # 卖出时，更新股数，增加现金
        stock['quantity'] -= quantity
        cash_received = price * quantity
        stocks[person]['cash'] += cash_received
        print(f" {person} 卖出 {stock_code}:{stock_name}  {quantity} 股，获利{price*quantity}在 {date},剩余现金{stocks[person]['cash']}。")
        # 重新计算均价（只考虑剩余股票）
        if stock['quantity'] > 0:
            remaining_cost = stock['avg_price'] * (stock['quantity'] + quantity) - cash_received
            stock['avg_price'] = remaining_cost / stock['quantity']
        else:
            stock['avg_price'] = 0.0  # 如果卖完了，均价置为0
        
        trades[person].append({'action': action, 'quantity': quantity,'stock code': stock_code,'stock name': stock_name,'price': price, 'date': date})
        # trades[person].append({'action': action, 'quantity': quantity, 'price': price, 'date': date})
        stock['cur_price'] = price
    # 保存数据
    save_data(stocks_file, stocks)
    save_data(trades_file, trades)

@dataclass(order=True)
class Trade:
    sort_index: datetime = field(init=False, repr=False)
    person: str
    stock_code: str
    stock_name: str
    quantity: int
    price: float
    action: str  # "buy" or "sell"
    date: str  # Format: "YYYY-MM-DD"

    def __post_init__(self):
        # This enables automatic sorting by date
        self.sort_index = datetime.strptime(self.date, "%Y-%m-%d")

    def __str__(self):
        return (f"{self.date} | {self.person} {self.action.upper()} {self.quantity} 股 "
                f"{self.stock_name} ({self.stock_code}) @ ￥{self.price}")
        
class TradeRecorder:
    def __init__(self):
        # 用于存储交易记录
        self.records = []

    def add_trade(self, person, stock_code, stock_name, quantity, price, action, date):
        """
        添加一条交易记录（不执行），用于后续排序执行。
        """
        self.records.append({
            'person': person,
            'stock_code': stock_code,
            'stock_name': stock_name,
            'quantity': quantity,
            'price': price,
            'action': action,
            'date': date
        })

    def sort_trades_by_date(self):
        """按照日期排序交易记录（升序）"""
        self.records.sort(key=lambda r: datetime.strptime(r['date'], "%Y-%m-%d"))

    def apply_all_trades_by_date(self, update_trade_func):
        """
        将所有记录按日期排序后，依次调用 update_trade_func
        """
        self.sort_trades_by_date()
        for record in self.records:
            update_trade_func(**record)