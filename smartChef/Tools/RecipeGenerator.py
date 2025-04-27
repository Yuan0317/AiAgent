import langfun as lf
from langfun.core.agentic import action
import os
import json
from typing import Dict, List, Any, Optional

class RecipeGeneratorAction(lf.agentic.Action):
    """基于用户的食材和要求生成食谱的工具"""
    
    operation: str  # "generate_recipe", "suggest_alternatives", "scale_recipe"
    ingredients: List[str]
    cuisine_type: str
    dietary_restrictions: Optional[str] = None
    cooking_skill: Optional[str] = None
    special_requirements: Optional[str] = None
    servings: Optional[int] = None
    time_limit: Optional[int] = None
    
    def call(self, session: lf.agentic.Session, *, lm=None, **kwargs):
        """根据操作类型执行不同的食谱生成功能"""
        
        if self.operation == "generate_recipe":
            return self._generate_recipe(session, lm=lm)
        elif self.operation == "suggest_alternatives":
            return self._suggest_alternatives(session, lm=lm)
        elif self.operation == "scale_recipe":
            return self._scale_recipe(session, lm=lm)
        else:
            return {"error": f"不支持的操作: {self.operation}"}
    
    def _generate_recipe(self, session: lf.agentic.Session, *, lm=None):
        """生成完整的食谱"""
        
        # 构建提示词
        ingredients_text = ", ".join(self.ingredients)
        dietary_text = f"饮食限制: {self.dietary_restrictions}" if self.dietary_restrictions else "无特殊饮食限制"
        skill_text = f"烹饪技能: {self.cooking_skill}" if self.cooking_skill else "中级烹饪技能"
        requirements_text = f"特殊要求: {self.special_requirements}" if self.special_requirements else "无特殊要求"
        time_text = f"时间限制: {self.time_limit} 分钟" if self.time_limit else "无时间限制"
        
        prompt = f"""请根据以下信息创建一个详细的{self.cuisine_type}食谱:
        
        可用食材: {ingredients_text}
        {dietary_text}
        {skill_text}
        {requirements_text}
        {time_text}
        
        请提供:
        1. 有创意的菜名
        2. 详细的食材清单(包括数量)
        3. 准备和烹饪的详细步骤
        4. 烹饪技巧和窍门
        5. 预计准备和烹饪时间
        
        请确保食谱符合指定的菜系风格,并利用所有或大部分列出的食材。
        """
        
        try:
            # 调用 LLM 生成食谱
            recipe = session.query(prompt, lm=lm)
            
            # 返回结果
            return {
                "status": "success",
                "recipe": recipe,
                "cuisine_type": self.cuisine_type,
                "ingredients_used": self.ingredients
            }
        except Exception as e:
            return {"error": f"生成食谱时出错: {str(e)}"}
    
    def _suggest_alternatives(self, session: lf.agentic.Session, *, lm=None):
        """为缺失的食材建议替代品"""
        
        # 构建提示词
        ingredients_text = ", ".join(self.ingredients)
        
        prompt = f"""我有以下食材: {ingredients_text}
        
        我想做{self.cuisine_type}菜系的料理,但可能缺少一些传统食材。
        请为我提供可能缺少的关键食材,以及我可以用手边的食材进行替代的方案。
        
        请列出:
        1. 可能缺少的2-3种关键食材
        2. 每种缺少食材的2-3个可能替代品
        3. 使用替代品时需要注意的事项
        """
        
        try:
            # 调用 LLM 生成替代方案
            alternatives = session.query(prompt, lm=lm)
            
            # 返回结果
            return {
                "status": "success",
                "alternatives": alternatives,
                "cuisine_type": self.cuisine_type,
                "original_ingredients": self.ingredients
            }
        except Exception as e:
            return {"error": f"生成替代方案时出错: {str(e)}"}
    
    def _scale_recipe(self, session: lf.agentic.Session, *, lm=None):
        """调整食谱份量"""
        
        if not self.servings:
            return {"error": "调整食谱份量需要指定份数(servings)"}
        
        # 构建提示词
        recipe_content = "\n".join(self.ingredients)  # 假设ingredients包含整个食谱内容
        
        prompt = f"""请将以下食谱调整为{self.servings}人份:
        
        {recipe_content}
        
        请提供:
        1. 调整后的食材清单(包括准确的数量)
        2. 如果需要,调整烹饪时间或方法的建议
        """
        
        try:
            # 调用 LLM 调整食谱
            scaled_recipe = session.query(prompt, lm=lm)
            
            # 返回结果
            return {
                "status": "success",
                "scaled_recipe": scaled_recipe,
                "servings": self.servings
            }
        except Exception as e:
            return {"error": f"调整食谱份量时出错: {str(e)}"} 