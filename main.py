from cal_values import calculate_value
from trade import update_trade, create_directory
# 示例用法
if __name__ == "__main__":
    # 创建存储文件夹
    create_directory("stock_data")
    
    # 记录买卖
    update_trade(person="wzj", stock_code="AAPL", stock_name="Apple", quantity=10, price=150, action="buy", date="2025-07-01")
    update_trade(person="wzj", stock_code="AAPL", stock_name="Apple", quantity=5, price=160, action="sell", date="2025-07-10")

    
    # 计算市值和收益
    calculate_value(person="wzj", stock_code=None, start_date="2025-07-01")

