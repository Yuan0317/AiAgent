"""
SmartChef 测试脚本 - 使用模拟数据
"""
import os
import time
import random
from datetime import datetime

# 确保recipes目录存在
os.makedirs("recipes", exist_ok=True)

# 模拟食材分析结果
def analyze_ingredients(ingredients, cuisine_type):
    print(f"正在分析食材: {ingredients}")
    print(f"菜系类型: {cuisine_type}")
    time.sleep(1)  # 模拟API调用时间
    
    # 模拟分析结果
    if "鸡肉" in ingredients or "鸡胸肉" in ingredients:
        if cuisine_type == "中餐":
            return {
                "main_ingredients": ["鸡胸肉"],
                "complementary_ingredients": ["葱", "姜", "蒜", "酱油", "料酒"],
                "possible_dishes": ["宫保鸡丁", "辣子鸡", "口水鸡"]
            }
        elif cuisine_type == "西餐":
            return {
                "main_ingredients": ["鸡胸肉"],
                "complementary_ingredients": ["橄榄油", "黑胡椒", "迷迭香", "大蒜"],
                "possible_dishes": ["香煎鸡胸肉", "鸡肉沙拉", "奶油蘑菇鸡"]
            }
    
    if "牛肉" in ingredients:
        if cuisine_type == "中餐":
            return {
                "main_ingredients": ["牛肉"],
                "complementary_ingredients": ["葱", "姜", "蒜", "酱油", "料酒"],
                "possible_dishes": ["红烧牛肉", "水煮牛肉", "青椒炒牛肉"]
            }
        elif cuisine_type == "西餐":
            return {
                "main_ingredients": ["牛肉"],
                "complementary_ingredients": ["黑胡椒", "迷迭香", "橄榄油"],
                "possible_dishes": ["黑椒牛排", "牛肉汉堡", "牛肉意面"]
            }
    
    if "西红柿" in ingredients and "鸡蛋" in ingredients:
        return {
            "main_ingredients": ["西红柿", "鸡蛋"],
            "complementary_ingredients": ["盐", "糖", "葱"],
            "possible_dishes": ["西红柿炒鸡蛋", "番茄蛋汤", "西红柿鸡蛋面"]
        }
    
    # 默认返回
    return {
        "main_ingredients": ingredients.split("、")[:2],
        "complementary_ingredients": ["盐", "糖", "各种调料"],
        "possible_dishes": ["创意料理", "简易快炒", "营养套餐"]
    }

# 模拟食谱合成结果
def synthesize_recipe(analysis_result, special_requirements):
    print("正在创建食谱...")
    time.sleep(1.5)  # 模拟API调用时间
    
    # 从可能的菜品中随机选择一个
    dish = random.choice(analysis_result["possible_dishes"])
    
    if dish == "宫保鸡丁":
        return {
            "dish_name": "宫保鸡丁",
            "ingredients": [
                "鸡胸肉 300克",
                "花生米 50克",
                "干辣椒 8-10个",
                "葱姜蒜 适量",
                "酱油 2勺",
                "醋 1勺",
                "糖 1勺",
                "盐 适量",
                "淀粉 适量"
            ],
            "preparation_steps": [
                "鸡胸肉切丁，用盐、淀粉、料酒腌制10分钟",
                "准备辅料：干辣椒切段，葱姜蒜切末，花生米炒熟",
                "热锅冷油，放入鸡丁快速翻炒至变色",
                "盛出鸡丁，锅中留底油，爆香干辣椒和葱姜蒜",
                "放回鸡丁，加入酱油、醋、糖调味",
                "烹炒均匀后加入花生米，翻炒几下即可出锅"
            ],
            "cooking_tips": [
                "鸡肉不要炒太久，否则会变老",
                "调料可以根据个人口味增减",
                "辣椒的量决定了菜品的辣度",
                "如果怕辣，可以减少辣椒用量或去籽"
            ]
        }
    elif dish == "西红柿炒鸡蛋":
        return {
            "dish_name": "西红柿炒鸡蛋",
            "ingredients": [
                "鸡蛋 3-4个",
                "西红柿 2个",
                "葱花 适量",
                "盐 适量",
                "糖 少许",
                "食用油 适量"
            ],
            "preparation_steps": [
                "西红柿洗净，切成块状",
                "鸡蛋打散，加少许盐搅拌均匀",
                "热锅凉油，倒入鸡蛋液",
                "待鸡蛋半凝固时，用铲子快速翻炒至金黄色",
                "盛出鸡蛋，锅中留少许底油",
                "爆香葱花，放入西红柿翻炒出汁",
                "加入少许盐和糖调味",
                "倒入炒好的鸡蛋，翻炒均匀即可出锅"
            ],
            "cooking_tips": [
                "西红柿炒至出汁，口感更佳",
                "加糖可以提鲜去酸",
                "鸡蛋先炒出锅，再与西红柿同炒，保持口感松软"
            ]
        }
    else:
        # 默认返回通用食谱
        return {
            "dish_name": dish,
            "ingredients": [
                f"{ing} 适量" for ing in analysis_result["main_ingredients"] + analysis_result["complementary_ingredients"][:3]
            ],
            "preparation_steps": [
                "准备所有食材，清洗干净并切好",
                "热锅下油，放入主要食材翻炒",
                "加入调味料，继续翻炒",
                "根据口味调整咸淡，加入其他辅料",
                "翻炒均匀后出锅"
            ],
            "cooking_tips": [
                "火候控制是关键",
                "调料可以根据个人口味增减",
                "注意食材的烹饪顺序"
            ]
        }

# 模拟食谱可视化
def visualize_recipe(recipe):
    print("正在生成美观的食谱格式和图片...")
    time.sleep(1)  # 模拟API调用时间
    
    # 构建Markdown格式食谱
    markdown = f"""# {recipe['dish_name']}

## 食材
"""
    
    for ingredient in recipe["ingredients"]:
        markdown += f"- {ingredient}\n"
    
    markdown += "\n## 步骤\n"
    
    for i, step in enumerate(recipe["preparation_steps"], 1):
        markdown += f"{i}. {step}\n"
    
    markdown += "\n## 烹饪技巧\n"
    
    for tip in recipe["cooking_tips"]:
        markdown += f"- {tip}\n"
    
    # 添加烹饪时间估计
    prep_time = random.randint(5, 15)
    cook_time = random.randint(10, 30)
    
    markdown += f"""
## 时间

| 准备时间 | 烹饪时间 | 总时间 |
|---------|---------|-------|
| {prep_time}分钟 | {cook_time}分钟 | {prep_time + cook_time}分钟 |
"""
    
    # 模拟图片URL（实际项目中会调用API生成图片）
    dish_name = recipe["dish_name"].replace(" ", "+")
    image_url = f"https://source.unsplash.com/random/800x600/?food,{dish_name}"
    
    # 添加图片链接
    markdown += f"\n![{recipe['dish_name']}]({image_url})\n"
    
    return markdown

# 保存食谱
def save_recipe(recipe_content, recipe_name):
    print(f"正在保存食谱: {recipe_name}...")
    
    # 创建文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = recipe_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    filename = f"recipes/{safe_name}_{timestamp}.md"
    
    # 添加元数据 - 确保元数据也使用UTF-8编码
    metadata = f"""---
name: {recipe_name}
created_at: {timestamp}
tags: [自动生成]
---

"""
    
    # 保存到文件 - 明确使用UTF-8编码，不带BOM
    with open(filename, "w", encoding="utf-8-sig") as f:
        f.write(metadata + recipe_content)
    
    return filename

# 主流程
def main():
    print("=" * 50)
    print("欢迎使用 SmartChef - 智能食谱助手")
    print("=" * 50)
    
    # 用户输入（这里使用硬编码的示例，实际应用中会从用户获取）
    available_ingredients = "鸡胸肉、青椒、洋葱、大蒜、姜、酱油、醋、糖"
    cuisine_type = "中餐"
    special_requirements = "喜欢偏辣的口味，烹饪时间不超过30分钟"
    
    print("\n📋 您的输入信息:")
    print(f"可用食材: {available_ingredients}")
    print(f"菜系类型: {cuisine_type}")
    print(f"特殊要求: {special_requirements}")
    print("\n正在为您生成食谱，请稍候...\n")
    
    # 步骤1: 食材分析
    analysis_result = analyze_ingredients(available_ingredients, cuisine_type)
    print("\n✅ 食材分析完成")
    print(f"主要食材: {', '.join(analysis_result['main_ingredients'])}")
    print(f"建议搭配: {', '.join(analysis_result['complementary_ingredients'])}")
    print(f"可制作的菜品: {', '.join(analysis_result['possible_dishes'])}")
    
    # 步骤2: 食谱合成
    recipe = synthesize_recipe(analysis_result, special_requirements)
    print("\n✅ 食谱创建完成")
    print(f"菜名: {recipe['dish_name']}")
    print(f"食材数量: {len(recipe['ingredients'])}")
    print(f"烹饪步骤: {len(recipe['preparation_steps'])}步")
    
    # 步骤3: 食谱可视化
    markdown_recipe = visualize_recipe(recipe)
    print("\n✅ 食谱可视化完成")
    
    # 步骤4: 保存食谱
    saved_file = save_recipe(markdown_recipe, recipe["dish_name"])
    print(f"\n✅ 食谱已保存至: {saved_file}")
    
    print("\n" + "=" * 50)
    print("食谱生成完成！您可以查看保存的食谱文件。")
    print("=" * 50)
    
    # 打印食谱预览
    print("\n📝 食谱预览:\n")
    preview_lines = markdown_recipe.split("\n")[:15]  # 只显示前15行
    print("\n".join(preview_lines))
    print("...\n[完整食谱请查看保存的文件]")

if __name__ == "__main__":
    main() 