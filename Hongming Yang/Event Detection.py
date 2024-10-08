import re

# 假设这是游戏的日志数据，包含玩家的行动记录
log_data = """
[10:15:00] Player1 crafted a rare item
[10:16:00] Player2 entered high-risk zone
[10:17:00] Player1 collected resources
"""

# 定义用于检测稀有行为的正则表达式
rare_item_pattern = re.compile(r"crafted a rare item")
high_risk_zone_pattern = re.compile(r"entered high-risk zone")

def detect_rare_events(log_data):
    rare_events = []
    
    for line in log_data.split('\n'):
        if rare_item_pattern.search(line):
            rare_events.append(f"检测到稀有物品制作: {line}")
        elif high_risk_zone_pattern.search(line):
            rare_events.append(f"检测到高风险区域探索: {line}")
    
    return rare_events

# 检测日志中的稀有事件
rare_events = detect_rare_events(log_data)
for event in rare_events:
    print(event)