import json
import os


def update_position_json(position_file, stock_code, name, quantity, avg_price, cur_price):
    """
    更新持仓文件，添加或更新股票持仓信息。
    """
    if os.path.exists(position_file):
        with open(position_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    data[stock_code] = {
        "name": name,
        "quantity": quantity,
        "avg_price": avg_price,
        "cur_price": cur_price
    }

    with open(position_file, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def check_and_update_market_json(position_file, market_file, person_key):
    """
    检查 market_file 中对应 person_key 的股票信息：
        - 若 quantity 为 0，则移除该条目；
        - 若 quantity 与 position_file 不一致或 avg_price 相差 > 0.1，则报错；
        - 否则将 position 中的 cur_price 写入 market_file。
    """
    with open(position_file, 'r') as f:
        positions = json.load(f)

    with open(market_file, 'r') as f:
        market_data = json.load(f)

    if person_key not in market_data:
        raise KeyError(f"{person_key} not found in market file.")


    for code, pos in positions.items():
        if code not in market_data[person_key]:
            # raise ValueError(f"{code} not found in market file under {person_key}.")
            continue

        market_entry = market_data[person_key][code]

        if pos['quantity'] == 0:
            continue

        # 1. check quantity
        if market_entry['quantity'] > pos['quantity']:
            raise ValueError(f"Quantity mismatch for {code}: {market_entry['quantity']} (market) vs {pos['quantity']} (position)")

        # 2. check avg_price tolerance
        # if abs(market_entry['cur_price'] - pos['cur_price']) > 0.1:
            # raise ValueError(f"Cur price mismatch for {code}: {market_entry['cur_price']} (market) vs {pos['cur_price']} (position)")

        # 3. skip if quantity == 0


        # # 4. update
        # updated_data[code] = {
        #     "name": pos["name"],
        #     "quantity": pos["quantity"],
        #     "avg_price": pos["avg_price"],
        #     "cur_price": pos["cur_price"]
        # }
        market_data[person_key][code]["avg_price"] = pos["avg_price"]
        market_data[person_key][code]["cur_price"] = pos["cur_price"]


    

    with open(market_file, 'w') as f:
        json.dump(market_data, f, indent=4, ensure_ascii=False)

    print(f"[✔] {person_key} 校验成功并已更新 cur_price。")


if __name__ == "__main__":
    update_position_json("keep.json", stock_code="510300", name="沪深300ETF",quantity= 2000,avg_price= 4.426, cur_price=4.225)
    update_position_json("keep.json", stock_code="600150", name="中国船舶",quantity= 300,avg_price= 35.054, cur_price=34.94)
    update_position_json("keep.json", stock_code="600456", name="宝钛股份",quantity= 200,avg_price= 32.015, cur_price=31.97)
    update_position_json("keep.json", stock_code="600707", name="彩虹股份",quantity= 500,avg_price= 7.76, cur_price=6.3)
    update_position_json("keep.json", stock_code="600760", name="中航沈飞",quantity= 100,avg_price= 64.321, cur_price=65.85)
    update_position_json("keep.json", stock_code="600988", name="赤峰黄金",quantity= 400,avg_price= 24.92, cur_price=23.28)
    update_position_json("keep.json", stock_code="603078", name="长城军工",quantity= 200,avg_price= 30.845, cur_price=29.94)
    
    update_position_json("keep.json", stock_code="603078", name="江化微",quantity= 1700,avg_price= 18.889, cur_price=18.76)
    update_position_json("keep.json", stock_code="603496", name="恒为科技",quantity= 1800,avg_price= 27.306, cur_price=28.62)
    update_position_json("keep.json", stock_code="603893", name="瑞芯微",quantity= 100,avg_price= 162.742, cur_price=166.71)
    update_position_json("keep.json", stock_code="000333", name="美的集团",quantity= 100,avg_price= 73.23, cur_price=71.13)
    update_position_json("keep.json", stock_code="000519", name="中兵红箭",quantity= 700,avg_price= 21.731, cur_price=22.26)
    update_position_json("keep.json", stock_code="000547", name="航天发展",quantity= 4000,avg_price= 7.853, cur_price=8.28)
    
    update_position_json("keep.json", stock_code="000733", name="振华科技",quantity= 700,avg_price= 49.861, cur_price=48.89)
    update_position_json("keep.json", stock_code="002050", name="三花智控",quantity= 1000,avg_price= 26.457, cur_price=27.13)
    update_position_json("keep.json", stock_code="002261", name="拓维信息",quantity= 1400,avg_price= 31.37, cur_price=32.13)
    update_position_json("keep.json", stock_code="002594", name="比亚迪",quantity= 1800,avg_price= 344.498, cur_price=111.43)
    update_position_json("keep.json", stock_code="002860", name="星帅尔",quantity= 400,avg_price= 13.343, cur_price=12.78)
    
    # update_position_json("keep.json", stock_code="300003", name="乐普医疗",quantity= 2300,avg_price= 38.136, cur_price=37.98)
    update_position_json("keep.json", stock_code="300063", name="天龙集团",quantity= 4100,avg_price= 10.681, cur_price=8.56)
    update_position_json("keep.json", stock_code="300077", name="国民技术",quantity= 1200,avg_price= 24.471, cur_price=25.52)
    update_position_json("keep.json", stock_code="300229", name="拓尔思",quantity= 500,avg_price= 22.72, cur_price=24.11)
    
    update_position_json("keep.json", stock_code="300276", name="三丰智能",quantity= 1500,avg_price= 14.478, cur_price=10.1)
    update_position_json("keep.json", stock_code="300293", name="蓝英装备",quantity= 1600,avg_price= 25.881, cur_price=26.49)
    update_position_json("keep.json", stock_code="300576", name="容大感光",quantity= 2700,avg_price= 35.314, cur_price=38.15)
    update_position_json("keep.json", stock_code="300624", name="万兴科技",quantity= 400,avg_price= 73.82, cur_price=78.9)
    
    update_position_json("keep.json", stock_code="300688", name="创业黑马",quantity= 100,avg_price= 36.34, cur_price=33.31)
    # update_position_json("keep.json", stock_code="00981", name="中芯国际",quantity= 2300,avg_price= 38.136, cur_price=37.98)
    update_position_json("keep.json", stock_code="01024", name="快手-W",quantity= 400,avg_price= 107.74, cur_price=71)
    update_position_json("keep.json", stock_code="09868", name="小鹏汽车-W",quantity= 200,avg_price= 67.63, cur_price=74.45)
    update_position_json("keep.json", stock_code="09988", name="阿里巴巴-W",quantity= 400,avg_price= 107.74, cur_price=119.4)

    check_and_update_market_json('keep.json', 'stock_data/wzj_stocks.json', 'wzj')
    check_and_update_market_json('keep.json', 'stock_data/jhh_stocks.json', 'jhh')