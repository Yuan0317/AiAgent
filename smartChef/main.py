import sys
sys.path.append('.')

## 自定义工具
from Tools.RecipeGenerator import RecipeGeneratorAction
from Tools.ImageGenerator import ImageGeneratorAction
from Tools.FileSystem import FileSystemAction

import langfun as lf
import pyglove as pg
from langfun.core.agentic import action, Session
from langfun.core.modalities import Mime

from IPython.display import display, JSON, HTML, Image, Markdown

import asyncio
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# 从环境变量获取API密钥
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("没有设置OPENAI_API_KEY环境变量。请在.env文件中设置。")


## 创建 LLM 模型集
lm_claude = lf.llms.Claude37Sonnet_20250219(api_key=claude_key, temperature=0.2)
lm_openai = lf.llms.Gpt4o_20241120(api_key=openai_key, max_tokens=16384)
lm_deepseek = lf.llms.DeepSeekR1(api_key=deepseek_key)
lm_gemini = lf.llms.Gemini2ProExp_20250205(api_key=gemini_key)

## 创建食谱请求类
class RecipeRequest(pg.Object):
    """用户的食谱请求，包括可用食材、想要的菜系类型和其他特殊要求"""
    
    available_ingredients: str    # 用户家中现有的食材
    cuisine_type: str             # 想要的菜系类型
    dietary_restrictions: str     # 饮食限制（可选）
    cooking_skill: str            # 烹饪技能水平
    special_requirements: str     # 特殊要求

## 数据交换结构
class IngredientAnalysisSchema(pg.Object):
    """食材分析结果"""
    main_ingredients: List[str]
    complementary_ingredients: List[str]
    possible_dishes: List[str]

class RecipeSynthesisSchema(pg.Object):
    """食谱合成结果"""
    dish_name: str
    ingredients: List[str]
    preparation_steps: List[str]
    cooking_tips: List[str]

class Recipe(pg.Object):
    """完整食谱"""
    recipe_content: str
    image_url: str

## 食材分析代理
class IngredientAnalysisAgent(lf.agentic.Action):
    """
    该代理负责分析用户提供的食材，确定可以制作的菜品，
    并根据用户指定的菜系提出合适的搭配食材和可能的菜品。
    """
    content: str
    
    def call(self, session, *, lm=lm_deepseek, **kwargs):
        prompt = """请分析以下食材和菜系要求：{{content}}
                   
                   你的任务是：
                   1. 确定主要食材和可能的辅助食材
                   2. 根据这些食材和指定的菜系，提出3-5个可行的菜品
                   3. 考虑食材的搭配性、口感互补和菜系的特点
                   4. 如果有特殊要求或饮食限制，确保遵循这些要求
                   """
        
        result = session.query(prompt,
                              lm=lm,
                              content=self.content)
        return result

## 食谱合成代理
class RecipeSynthesisAgent(lf.agentic.Action):
    """
    该代理负责合成一个完整的食谱，包括菜名、详细食材清单、
    步骤说明以及烹饪技巧。
    """
    content: str
    
    def call(self, session, *, lm=lm_claude, **kwargs):
        prompt = """基于先前的食材分析：{{content}}
                   
                   请创建一个详细的食谱，包括：
                   1. 创意且吸引人的菜名
                   2. 完整的食材清单（包括数量）
                   3. 逐步的准备和烹饪说明
                   4. 实用的烹饪技巧和窍门
                   5. 注意计时、火候和关键步骤的提示
                   
                   确保食谱符合指定的菜系风格并适合用户的烹饪水平。
                   """
        
        result = session.query(prompt,
                              lm=lm,
                              content=self.content)
        return result

## 食谱可视化代理
class RecipeVisualizationAgent(lf.agentic.Action):
    """
    该代理负责将食谱转换为具有吸引力的可视化格式，
    并使用 IMAGE GENERATOR API 生成相应的食谱图片。
    """
    content: str
    
    allow_symbolic_assignment = True
    
    def call(self, session, *, lm=lm_claude, **kwargs):
        prompt = """请将以下食谱内容转换为美观的 Markdown 格式：{{content}}
                   
                   格式要求：
                   1. 使用 Markdown 标题、列表和其他格式元素
                   2. 清晰地分隔食材部分和步骤部分
                   3. 加入表格或其他形式的时间估计
                   4. 使食谱既实用又美观
                   
                   同时，请生成一段描述，用于创建这道菜的图片。描述应该：
                   - 详细描述成品的外观
                   - 提及关键食材的颜色和摆盘
                   - 适合用作图像生成的提示词
                   """
        
        result = session.query(prompt,
                              lm=lm,
                              content=self.content)
        
        # 从结果中提取图片描述用于生成图片
        # 这部分在实际应用中会调用图片生成 API
        
        # 模拟图片生成结果
        image_url = "https://source.unsplash.com/random/1024x1024/?food," + content.split('\n')[0]
        
        # 构建最终食谱（Markdown + 图片URL）
        full_recipe = result + f"\n\n![食谱图片]({image_url})"
        
        return full_recipe

## 任务完成标记
class Done(lf.agentic.Action):
    def call(self, session, *, lm=None, **kwargs):
        return "完成"

## 保存食谱
class SaveRecipe(lf.agentic.Action):
    """保存生成的食谱到文件系统"""
    
    recipe_content: str
    recipe_name: str
    
    allow_symbolic_assignment = True
    
    def call(self, session, *, lm=lm_claude, **kwargs):
        # 创建文件名（使用食谱名和时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recipes/{self.recipe_name.replace(' ', '_')}_{timestamp}.md"
        
        # 确保目录存在
        os.makedirs("recipes", exist_ok=True)
        
        # 保存食谱
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.recipe_content)
        
        return f"食谱已保存至 {filename}"

## 下一步决策
class NextStep(pg.Object):
    step: int
    thoughts: list[str]
    action: IngredientAnalysisAgent | RecipeSynthesisAgent | RecipeVisualizationAgent | None | Done

## 智能厨师代理
class SmartChefAgent(lf.agentic.Action):
    """智能厨师代理，可以根据用户的食材和要求生成完整的食谱"""
    
    recipe_request: RecipeRequest
    rounds: int
    
    allow_symbolic_assignment = True
    
    def call(self, session, *, lm=lf.LanguageModel, **kwargs):
        past_steps = []
        final_recipe = None
        recipe_name = "未命名菜谱"
        
        prompt = """你的任务是帮助用户根据现有食材和要求创建一个完整的食谱。
                    这是用户的请求：{{recipe_request}}
                    你已经完成了这些步骤：{{past_steps}}
                    现在请一步一步思考，确定下一步行动。"""
        
        for round in range(self.rounds):
            next_step = session.query(prompt,
                                     NextStep,
                                     lm=lm,
                                     recipe_request=self.recipe_request,
                                     past_steps=past_steps)
            
            past_steps.append(next_step)
            lf.logging.info(str(next_step))
            next_action = next_step.action
            
            if next_action is not None and not isinstance(next_action, Done):
                current_result = next_action()
                past_steps.append(current_result)
                
                # 如果是最终的 RecipeVisualizationAgent 结果，保存为最终食谱
                if isinstance(next_action, RecipeVisualizationAgent):
                    final_recipe = current_result
                    # 尝试从食谱内容中提取菜名
                    first_line = current_result.split('\n')[0]
                    if first_line.startswith('# '):
                        recipe_name = first_line[2:].strip()
            else:
                break
        
        # 如果有最终食谱，保存它
        if final_recipe:
            save_action = SaveRecipe(recipe_content=final_recipe, recipe_name=recipe_name)
            save_result = save_action(session=session, lm=lm)
            return {"recipe": final_recipe, "save_result": save_result}
        
        return "未能生成完整食谱"

# 示例使用
if __name__ == "__main__":
    # 创建一个示例请求
    sample_request = RecipeRequest(
        available_ingredients="鸡胸肉、西红柿、青椒、洋葱、大蒜、生姜、酱油、醋、糖、盐",
        cuisine_type="中餐",
        dietary_restrictions="无",
        cooking_skill="中级",
        special_requirements="喜欢偏辣口味，希望烹饪时间不超过30分钟"
    )
    
    # 创建智能厨师代理并执行
    chef_agent = SmartChefAgent(recipe_request=sample_request, rounds=4)
    result = chef_agent(lm=lm_claude)
    
    # 显示结果
    print(result) 