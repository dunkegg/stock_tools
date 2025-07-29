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
def calculate_value_all(person, start_date):
    stocks_file, trades_file = get_person_file_paths(person)
    
    stocks = load_data(stocks_file)
    trades = load_data(trades_file)
    
    # 计算所有股票的综合收益
    total_value = 0
    total_cost = 0  # 计算从start_date起的买入成本
    
    
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
            # total_cost+=13
            if transaction['action'] == 'buy':
                # print(f"{person} 在 {transaction['date']} BUY : {transaction['price']}元/股， {transaction['quantity']}股， 共 {value} ")
                total_cost += value
            elif transaction['action'] == 'sell':
                # print(f"{person} 在 {transaction['date']} SELL : {transaction['price']}元/股， {transaction['quantity']}股， 共 {value} ")
                total_cost -= value

    
    # 计算综合收益
    keep_profit = total_value - total_cost
    keep_profit_rate = keep_profit / total_value if total_value != 0 else 0
    
    cash = stocks[person]['cash']
    all_profit = total_value - total_cost
    all_profit_rate = all_profit / (total_value + cash ) if (total_value + cash ) != 0 else 0

    print(f"{person} 当前市值: {total_value} 元, 当前现金：{cash} 元, 总共{total_value+cash} 元")
    print(f"从 {start_date} 开始的收益: {all_profit} 元, 一共交易了{len(all_tractions)} 次")
    print(f"持仓收益率: {keep_profit_rate * 100:.2f}%")
    print(f"总收益率: {all_profit_rate * 100:.2f}%")
    print("+++++++++++++++++++++")
    return all_profit

        

def calculate_value_split(person, cal_stock_code, start_date):
    stocks_file, trades_file = get_person_file_paths(person)
    
    stocks = load_data(stocks_file)
    trades = load_data(trades_file)
    
    
    if person not in stocks:
        raise ValueError(f"没有{person}")
    if cal_stock_code is not None and cal_stock_code not in stocks[person]:
        raise ValueError(f"{person} 未持有 {cal_stock_code}")
    
    
    # 计算所有股票的综合市值和收益
    all_profit = 0
    all_stocks =  stocks.get(person, {}).items()
    for stock_code, stock in all_stocks:
        if stock_code == 'cash':  # 排除现金
            continue
            
        if cal_stock_code is not None:
            if stock_code != cal_stock_code:
                continue
        # stock = stocks[person][stock_code]
        total_value = stock['quantity'] * stock['cur_price']
        total_cost = 0 
        # 计算从 start_date 起的买入成本
        trade_times = 0
        for transaction in trades.get(person, []):
            
            if transaction['stock code'] != stock_code:
                continue
            if transaction['date'] >= start_date:
                trade_times+=1
                value = transaction['quantity'] * transaction['price']
                if transaction['action'] == 'buy':
                    total_cost += value
                elif transaction['action'] == 'sell':
                    total_cost -= value

        # 计算综合收益
        keep_profit = total_value - total_cost
        keep_profit_rate = keep_profit / total_value if total_value != 0 else 0
        all_profit += keep_profit
        # cash = stocks[person]['cash']
        # all_profit = total_value - total_cost
        # all_profit_rate = all_profit / (total_value + cash ) if (total_value + cash ) != 0 else 0

        print(f"{person} 当前持有{stock_code}:{stocks[person][stock_code]['name']} 共{stocks[person][stock_code]['quantity']} 股")
        print(f"当前价格:{stocks[person][stock_code]['cur_price']} , 持有成本:{stocks[person][stock_code]['avg_price']}")
        print(f"从 {start_date} 开始的收益: {keep_profit} 元, 一共交易了{trade_times} 次")
    print(f"所有收益为 {all_profit}")

if __name__ == "__main__":
    calculate_value_all(person="wzj", start_date="2024-01-01")
    # calculate_value_all(person="jhh", start_date="2024-01-01")
    # calculate_value_split(person="jhh", cal_stock_code=None, start_date="2024-01-01")
    calculate_value_split(person="wzj", cal_stock_code=None, start_date="2024-01-01")
