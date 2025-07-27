from trade import get_person_file_paths, load_data

# import matplotlib.pyplot as plt
# import matplotlib.ticker as mtick
# import os

# def plot_percentage_curve(dates, percentages, title="收益率变化曲线", xlabel="日期", ylabel="收益率", save_path="output.png"):
#     """
#     绘制百分比变化图，并保存为图片

#     参数:
#     - dates: list[str]，横坐标，如 ["2024-08-01", "2024-08-02", ...]
#     - percentages: list[float]，纵坐标，例如 [0.01, -0.02, 0.05] 表示 +1%, -2%, +5%
#     - title: 图表标题
#     - xlabel: 横坐标标签
#     - ylabel: 纵坐标标签（默认是"收益率"）
#     - save_path: 图片保存路径，例如 "figs/plot.png"
#     """
#     plt.figure(figsize=(10, 5))
#     plt.plot(dates, percentages, marker='o', linestyle='-', color='blue')
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)

#     # 设置 y 轴为百分比格式
#     plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

#     # 自动旋转日期标签
#     plt.xticks(rotation=45)

#     plt.grid(True)
#     plt.tight_layout()

#     # 自动创建保存目录（如果需要）
#     os.makedirs(os.path.dirname(save_path), exist_ok=True)

#     # 保存图片
#     plt.savefig(save_path, dpi=300)

#     # 同时展示（如不需要可注释掉）
#     # plt.show()
def calculate_value(person, stock_code, start_date):
    stocks_file, trades_file = get_person_file_paths(person)
    
    stocks = load_data(stocks_file)
    trades = load_data(trades_file)
    
    # 计算所有股票的综合收益
    total_value = 0
    total_cost = 0  # 计算从start_date起的买入成本
    
    if stock_code is None:
        # 计算所有股票的综合市值和收益
        all_stocks =  stocks.get(person, {}).items()
        for stock_code, stock in all_stocks:
            if stock_code != 'cash':  # 排除现金
                # 计算股票的市值
                total_value += stock['quantity'] * stock['cur_price']
                
        # 计算该股票从 start_date 起的买入成本
        all_tractions = trades.get(person, [])
        for transaction in all_tractions:
            if transaction['date'] >= start_date:
                value = transaction['quantity'] * transaction['price']
                total_cost+=13
                if transaction['action'] == 'buy':
                    # print(f"{person} 在 {transaction['date']} BUY : {transaction['price']}元/股， {transaction['quantity']}股， 共 {value} ")
                    total_cost += value
                elif transaction['action'] == 'sell':
                    # print(f"{person} 在 {transaction['date']} SELL : {transaction['price']}元/股， {transaction['quantity']}股， 共 {value} ")
                    total_cost -= value
    else:
        # 计算指定股票的市值和收益
        if person not in stocks or stock_code not in stocks[person]:
            print(f"{person} 没有持有股票 {stock_code}")
            return
        
        stock = stocks[person][stock_code]
        total_value = stock['quantity'] * stock['cur_price']
        
        # 计算从 start_date 起的买入成本
        for transaction in trades.get(person, []):
            if transaction['date'] >= start_date:
                if transaction['action'] == 'buy':
                    total_cost += transaction['quantity'] * transaction['price']
                elif transaction['action'] == 'sell':
                    total_cost -= transaction['quantity'] * transaction['price']
    
    # 计算综合收益
    keep_profit = total_value - total_cost
    keep_profit_rate = keep_profit / total_value if total_value != 0 else 0
    
    cash = stocks[person]['cash']
    all_profit = total_value - total_cost
    all_profit_rate = all_profit / (total_value + cash ) if (total_value + cash ) != 0 else 0
    
    print(f"{person} 当前市值: {total_value} 元, 当前现金：{cash} 元, 总共{total_value+cash} 元")
    print(f"从 {start_date} 开始的收益: {all_profit} 元")
    print(f"持仓收益率: {keep_profit_rate * 100:.2f}%")
    print(f"总收益率: {all_profit_rate * 100:.2f}%")
    print("+++++++++++++++++++++")
    
if __name__ == "__main__":
    calculate_value(person="wzj", stock_code=None, start_date="2024-01-01")
    calculate_value(person="jhh", stock_code=None, start_date="2024-01-01")
