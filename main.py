from cal_values import calculate_value
from trade import update_trade, create_directory
# 示例用法
if __name__ == "__main__":
    # 创建存储文件夹
    create_directory("stock_data")
    
    # 记录买卖
    update_trade(person="jhh", stock_code="300063", stock_name="天龙集团", quantity=2600, price=11.18, action="buy", date="2025-02-24")
    update_trade(person="jhh", stock_code="002346", stock_name="拓中股份", quantity=1000, price=11.51, action="buy", date="2025-02-26")
    update_trade(person="jhh", stock_code="300063", stock_name="天龙集团", quantity=1000, price=10.44, action="buy", date="2025-02-26")
    update_trade(person="jhh", stock_code="300077", stock_name="国民技术", quantity=1000, price=29.50, action="buy", date="2025-02-27")
    update_trade(person="jhh", stock_code="300276", stock_name="三丰智能", quantity=1000, price=15.73, action="buy", date="2025-02-27")

    update_trade(person="wzj", stock_code="AAPL", stock_name="Apple", quantity=5, price=160, action="sell", date="2025-07-10")

    
    # 计算市值和收益
    calculate_value(person="wzj", stock_code=None, start_date="2025-07-01")

