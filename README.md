# The Farmer Was Replaced - 自动化农场脚本

这是我在玩 Steam 游戏 [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/_/) 时编写的自动化脚本集合。

## 🎮 关于游戏

**The Farmer Was Replaced** 是一款编程解谜游戏，玩家需要通过编写 Python 代码来自动化管理农场，种植作物、优化资源、解锁新技术。游戏结合了编程学习和策略优化，非常适合喜欢自动化和算法优化的玩家。

## 📁 项目结构

```
Save0/
├── main.py                 # 主程序入口
├── smart_priority.py       # 智能优先级控制器（推荐使用）
├── config.py               # 🎮 用户配置文件（优先级和阈值）
├── config.example.py       # 配置文件示例
├── utils.py                # 通用工具函数（移动优化、耕地等）
├── crop_grass.py           # 草地收割（获取干草）
├── crop_trees.py           # 树木种植（棋盘模式，避免生长惩罚）
├── crop_carrots.py         # 胡萝卜种植（基础资源）
├── crop_pumpkins.py        # 南瓜种植（巨型南瓜策略，n³产量）
├── crop_sunflowers.py      # 向日葵种植（级联收获，5倍能量）
├── crop_cactus.py          # 仙人掌种植（排序收获，n²产量）
├── crop_mix.py             # 混合种植（伴生植物，5倍产量）
├── crop_weird.py           # 奇异物质收集（感染策略）
├── crop_dinosaur.py        # 🦕 恐龙养殖（n²骨头收益）
└── .gitignore              # Git 忽略配置
```

## 🚀 核心功能

### 1. **智能优先级系统** (`smart_priority.py`)

自动化农场管理系统，根据资源状态智能选择最佳作物。

**特点：**
- 🎯 用户自定义优先级列表
- 📊 动态资源检查
- ⚡ 紧急情况自动响应（能量/资源短缺）
- 🔄 自动循环种植

**使用方法：**
```python
# 编辑 PRIORITY 列表设置优先级
PRIORITY = [
    {"crop": "mixed", "main": Entities.Tree},   # 混合种植
    {"crop": "sunflowers"},                     # 向日葵
    {"crop": "pumpkins"},                       # 南瓜
    ...
]

# 调整资源阈值
THRESHOLDS = {
    "power_low": 100,        # 能量低于此值优先种向日葵
    "power_safe": 200,       # 能量安全值
    "carrot_min": 2000,      # 胡萝卜最低储备
    ...
}
```

### 2. **作物模块**

每种作物都有独立的优化模块：

#### 🌾 **草地** (`crop_grass.py`)
- 最快收割周期
- 自动土地转换
- 获取干草资源

#### 🌳 **树木** (`crop_trees.py`)
- 棋盘种植模式（避免16倍生长惩罚）
- 每棵树5份木材
- 优化的邻接规避策略

#### 🥕 **胡萝卜** (`crop_carrots.py`)
- 快速种植与收获
- 自动清理其他作物
- 基础资源生产

#### 🎃 **南瓜** (`crop_pumpkins.py`)
- 巨型南瓜策略（n×n合并→n³产量，n≥6→n²×6）
- 枯萎南瓜追踪优化
- 只检查枯萎位置，效率提升80%

#### 🌻 **向日葵** (`crop_sunflowers.py`)
- 级联收获策略（花瓣数从大到小）
- 每株都获得5倍能量加成
- 600%能量提升
- 种植时记录花瓣数，避免重复测量

#### 🌵 **仙人掌** (`crop_cactus.py`)
- 高级排序算法（逐行逐列冒泡排序）
- 从左下角递归收获（n²产量）
- 排序完成检测，减少冗余操作
- 只检查第一个位置的成熟状态

#### 🌺 **混合种植** (`crop_mix.py`)
- 伴生植物机制（5倍产量加成）
- 支持 Bush/Tree/Carrot/Grass
- 自动获取伴生需求并优化种植
- Tree 自动使用棋盘模式

#### 🧪 **奇异物质** (`crop_weird.py`)
三种收集策略：
- **基础策略**：草地+肥料，快速收获
- **高产策略**：胡萝卜+多次施肥，最大化产量
- **连锁策略**：利用奇异物质扩散感染，节省肥料

#### 🦕 **恐龙养殖** (`crop_dinosaur.py`)
三种养殖模式：
- **最优模式**：根据仙人掌库存自动选择农场大小
- **填满模式**：S形遍历填满整个当前农场（最大收益）
- **高效模式**：只吃指定数量苹果（快速获取骨头）
- 收益：尾巴长度的平方（n²根骨头）

### 3. **优化工具** (`utils.py`)

#### 🎯 **移动优化**
```python
move_to(x, y)  # 利用环形世界，自动选择最短路径
```
- 考虑边界环绕
- 减少30%移动距离

#### 🌱 **自动耕地**
```python
tilling()  # 自动处理土地转换
```

## 🎯 优化策略详解

### 南瓜优化 - 枯萎追踪
```python
# 只记录枯萎南瓜位置
withered_positions = [(x, y), ...]

# 只检查枯萎位置，不扫描全场
for pos in withered_positions:
    check_and_replant(pos)
```
**效果**：6×6场地效率提升约80%

### 向日葵优化 - 级联收获
```python
# 种植时记录花瓣数
petal_map = {(x, y): petals, ...}

# 按花瓣数从大到小收获
while petal_map:
    harvest_max_petals()
```
**效果**：600%能量提升（15→14→13→12...每株都是5倍）

### 仙人掌优化 - 智能排序
```python
# 逐行完成排序
for each row:
    bubble_sort_until_complete()

# 逐列完成排序（不破坏行顺序）
for each column:
    bubble_sort_until_complete()
```
**效果**：减少40%排序轮数，减少50%长距离移动

### 混合种植优化 - 伴生策略
```python
# 自动获取伴生需求
companion_type, companion_pos = get_companion()

# 优化种植位置，满足多个主作物需求
plant_best_companion(position_demand)
```
**效果**：5倍产量加成

### 恐龙养殖优化 - S形遍历
```python
# S形路径遍历农场，确保尾巴填满每个格子
y = 0
while y < size:
    if y % 2 == 0:
        # 偶数行：从左到右
        traverse_row_left_to_right()
    else:
        # 奇数行：从右到左
        traverse_row_right_to_left()
    y = y + 1

# 检测尾巴填满
success = move(direction)
if not success:
    # 无法移动 = 尾巴已填满农场
    harvest_bones()
```
**效果**：
- 10×10农场 = 100格 = 10,000根骨头
- 自动根据仙人掌库存选择最优农场大小
- 每吃一个苹果，移动速度提升3%

## 🔧 使用指南

### 快速开始

1. **配置你的策略**
   ```bash
   # 首次使用：复制配置示例文件
   cp config.example.py config.py
   
   # 然后编辑 config.py 设置你的优先级
   ```

2. **自定义优先级**
   ```python
   # 编辑 config.py 中的 PRIORITY 列表
   PRIORITY = [
       {"crop": "sunflowers"},                     # 优先种向日葵
       {"crop": "mixed", "main": Entities.Bush},   # 混合种植灌木
       {"crop": "pumpkins"},                       # 南瓜
   ]
   ```

3. **运行智能控制器**
   ```python
   # 运行 smart_priority.py
   # 系统会自动根据资源状态选择最佳作物
   ```

3. **单独运行作物模块**
   ```python
   import crop_sunflowers
   crop_sunflowers.farm_sunflowers()
   ```

### 高级配置

**在 `config.py` 中配置：**

**奇异物质策略选择：**
```python
{"crop": "weird", "strategy": "basic"}     # 快速策略
{"crop": "weird", "strategy": "advanced"}  # 高产策略
{"crop": "weird", "strategy": "chain"}     # 节省肥料
```

**混合种植作物选择：**
```python
{"crop": "mixed", "main": Entities.Bush}    # 灌木（高木材）
{"crop": "mixed", "main": Entities.Tree}    # 树木（棋盘模式）
{"crop": "mixed", "main": Entities.Carrot}  # 胡萝卜
```

**恐龙养殖模式：**
```python
{"crop": "dinosaur", "mode": "optimal"}     # 自动最优（根据仙人掌库存）
{"crop": "dinosaur", "mode": "full"}        # 填满当前农场（最大收益）
{"crop": "dinosaur", "mode": "efficient", "apples": 50}  # 指定苹果数
```

**资源阈值调整：**
```python
THRESHOLDS = {
    "power_low": 100,         # 能量低于此值优先种向日葵
    "power_safe": 200,        # 能量安全值
    "carrot_min": 2000,       # 胡萝卜最低储备
    "wood_min": 3000,         # 木材最低储备
    "hay_min": 1000,          # 干草最低储备
    "fertilizer_min": 5,      # 肥料最低储备
}
```

## 🎓 学习要点

这个项目展示了以下编程和算法优化技巧：

1. **算法优化**
   - 冒泡排序优化（提前退出、逐行完成）
   - 路径优化（环形世界最短路径）
   - 状态追踪（枯萎位置、排序状态）

2. **游戏机制理解**
   - 树木邻接惩罚（4方向×2倍=16倍）
   - 向日葵5倍机制（≥10株，花瓣数最大）
   - 伴生植物加成（5倍产量）

3. **模块化设计**
   - 每种作物独立模块
   - 统一的工具函数
   - 智能优先级系统

4. **资源管理**
   - 动态成本计算（get_cost）
   - 紧急情况响应
   - 收益评分系统

## 🎮 游戏链接

[Steam: The Farmer Was Replaced](https://store.steampowered.com/app/2060160/_/)

## 📄 许可

个人学习项目，代码可自由使用和修改。

## 🤝 贡献

欢迎提出优化建议和改进方案！

---

**Enjoy farming! 🌾**
