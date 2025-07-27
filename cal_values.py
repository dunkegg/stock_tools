from trade import get_person_file_paths, load_data
def calculate_value(person, stock_code, start_date):
    stocks_file, trades_file = get_person_file_paths(person)
    
    stocks = load_data(stocks_file)
    trades = load_data(trades_file)
    
    # 计算所有股票的综合收益
    total_value = 0
    total_cost = 0  # 计算从start_date起的买入成本
    profit = 0
    
    if stock_code is None:
        # 计算所有股票的综合市值和收益
        for stock_code, stock in stocks.get(person, {}).items():
            if stock_code != 'cash':  # 排除现金
                # 计算股票的市值
                total_value += stock['quantity'] * stock['cur_price']
                
                # 计算该股票从 start_date 起的买入成本
                for transaction in trades.get(person, []):
                    if transaction['date'] >= start_date:
                        if transaction['action'] == 'buy':
                            total_cost += transaction['quantity'] * transaction['price']
                        elif transaction['action'] == 'sell':
                            total_cost -= transaction['quantity'] * transaction['price']
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
    profit = total_value - total_cost
    profit_rate = profit / total_cost if total_cost != 0 else 0
    
    print(f"{person} 当前市值: {total_value} 元")
    print(f"从 {start_date} 开始的收益: {profit} 元")
    print(f"收益率: {profit_rate * 100:.2f}%")
    
if __name__ == "__main__":
    calculate_value(person="wzj", stock_code=None, start_date="2025-01-01")
