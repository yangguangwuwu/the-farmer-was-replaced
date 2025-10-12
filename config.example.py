# ====================================
# 🎮 用户配置文件示例
# ====================================
# 复制此文件为 config.py 并根据你的需求修改

# 优先级列表（数字越小优先级越高）
# 可以随意调整顺序，程序会自动检查资源是否足够
# 混合种植使用字典：{"crop": "mixed", "main": Entities.Bush}
# 奇异物质使用字典：{"crop": "weird", "strategy": "basic"}（basic/advanced/chain）
PRIORITY = [
	{"crop": "weird", "strategy": "advanced"},  # 奇异物质（高产策略）
	{"crop": "mixed", "main": Entities.Tree},   # 混合种植-树木（伴生植物5倍产量）
	{"crop": "grass"},                          # 草地（快速收割）
	{"crop": "sunflowers"},                     # 向日葵（能量）
	{"crop": "pumpkins"},                       # 南瓜（高价值）
	{"crop": "carrots"},                        # 胡萝卜（基础资源）
	{"crop": "trees"},                          # 树木（木材）
	{"crop": "cactus"},                         # 仙人掌（最高产出）
]

# 资源阈值配置（可自定义调整）
THRESHOLDS = {
	"power_low": 100,         # 能量低于此值优先种向日葵
	"power_safe": 200,        # 能量安全值
	"carrot_min": 2000,       # 胡萝卜最低储备
	"wood_min": 3000,         # 木材最低储备
	"hay_min": 1000,          # 干草最低储备
	"fertilizer_min": 5,      # 肥料最低储备（用于奇异物质）
}
