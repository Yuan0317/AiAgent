import langfun as lf
from langfun.core.agentic import action
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class FileSystemAction(lf.agentic.Action):
    """文件系统操作工具，用于保存和加载食谱"""
    
    operation: str  # "save_recipe", "load_recipe", "list_recipes", "search_recipes"
    recipe_name: Optional[str] = None
    recipe_content: Optional[str] = None
    recipe_tags: Optional[List[str]] = None
    search_query: Optional[str] = None
    recipes_folder: str = "recipes"
    
    def call(self, session: lf.agentic.Session, *, lm=None, **kwargs):
        """根据操作类型执行不同的文件系统功能"""
        
        # 确保食谱目录存在
        os.makedirs(self.recipes_folder, exist_ok=True)
        
        if self.operation == "save_recipe":
            return self._save_recipe()
        elif self.operation == "load_recipe":
            return self._load_recipe()
        elif self.operation == "list_recipes":
            return self._list_recipes()
        elif self.operation == "search_recipes":
            return self._search_recipes(session, lm=lm)
        else:
            return {"error": f"不支持的操作: {self.operation}"}
    
    def _save_recipe(self):
        """保存食谱到文件系统"""
        
        if not self.recipe_name or not self.recipe_content:
            return {"error": "保存食谱需要提供菜名和食谱内容"}
        
        try:
            # 创建文件名（使用食谱名和时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = self.recipe_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
            filename = f"{self.recipes_folder}/{safe_name}_{timestamp}.md"
            
            # 准备元数据
            metadata = {
                "name": self.recipe_name,
                "created_at": timestamp,
                "tags": self.recipe_tags if self.recipe_tags else []
            }
            
            # 将元数据添加到食谱内容前面作为YAML前置元数据
            yaml_metadata = "---\n"
            for key, value in metadata.items():
                if isinstance(value, list):
                    yaml_metadata += f"{key}: [{', '.join(value)}]\n"
                else:
                    yaml_metadata += f"{key}: {value}\n"
            yaml_metadata += "---\n\n"
            
            content_with_metadata = yaml_metadata + self.recipe_content
            
            # 保存食谱
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content_with_metadata)
            
            return {
                "status": "success",
                "message": f"食谱已保存至 {filename}",
                "filepath": filename
            }
        except Exception as e:
            return {"error": f"保存食谱时出错: {str(e)}"}
    
    def _load_recipe(self):
        """加载特定食谱"""
        
        if not self.recipe_name:
            return {"error": "加载食谱需要提供菜名"}
        
        try:
            # 查找匹配的食谱文件
            matching_files = []
            safe_name = self.recipe_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
            
            for filename in os.listdir(self.recipes_folder):
                if filename.startswith(safe_name) and filename.endswith(".md"):
                    matching_files.append(filename)
            
            if not matching_files:
                return {"error": f"未找到名为 '{self.recipe_name}' 的食谱"}
            
            # 默认加载最新版本（按文件名排序，假设文件名包含时间戳）
            latest_file = sorted(matching_files)[-1]
            filepath = os.path.join(self.recipes_folder, latest_file)
            
            # 读取食谱内容
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 提取元数据和内容
            metadata = {}
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_lines = parts[1].strip().split("\n")
                    for line in yaml_lines:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            metadata[key.strip()] = value.strip()
                    content = parts[2].strip()
            
            return {
                "status": "success",
                "recipe_name": self.recipe_name,
                "content": content,
                "metadata": metadata,
                "filepath": filepath
            }
        except Exception as e:
            return {"error": f"加载食谱时出错: {str(e)}"}
    
    def _list_recipes(self):
        """列出所有保存的食谱"""
        
        try:
            recipes = []
            
            for filename in os.listdir(self.recipes_folder):
                if filename.endswith(".md"):
                    filepath = os.path.join(self.recipes_folder, filename)
                    
                    # 尝试提取元数据
                    metadata = {"filename": filename}
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                            if content.startswith("---"):
                                parts = content.split("---", 2)
                                if len(parts) >= 3:
                                    yaml_lines = parts[1].strip().split("\n")
                                    for line in yaml_lines:
                                        if ":" in line:
                                            key, value = line.split(":", 1)
                                            metadata[key.strip()] = value.strip()
                    except:
                        # 如果无法提取元数据，则只使用文件名
                        pass
                    
                    recipes.append(metadata)
            
            # 按创建时间排序
            recipes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            return {
                "status": "success",
                "recipes": recipes,
                "count": len(recipes)
            }
        except Exception as e:
            return {"error": f"列出食谱时出错: {str(e)}"}
    
    def _search_recipes(self, session: lf.agentic.Session, *, lm=None):
        """搜索食谱"""
        
        if not self.search_query:
            return {"error": "搜索食谱需要提供查询条件"}
        
        try:
            # 首先获取所有食谱
            all_recipes_result = self._list_recipes()
            if "error" in all_recipes_result:
                return all_recipes_result
            
            all_recipes = all_recipes_result["recipes"]
            
            # 准备搜索内容
            search_materials = []
            for recipe_metadata in all_recipes:
                filename = recipe_metadata.get("filename", "")
                filepath = os.path.join(self.recipes_folder, filename)
                
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                        # 跳过YAML元数据部分
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                content = parts[2].strip()
                        
                        search_materials.append({
                            "filename": filename,
                            "metadata": recipe_metadata,
                            "content": content[:500]  # 只使用前500个字符用于搜索
                        })
                except:
                    # 如果无法读取内容，则跳过此食谱
                    continue
            
            # 如果没有可搜索的内容，返回空结果
            if not search_materials:
                return {
                    "status": "success",
                    "message": "没有可搜索的食谱",
                    "matches": []
                }
            
            # 构建搜索提示词
            search_prompt = f"""我有以下食谱集合，请帮我找出与查询条件"{self.search_query}"最相关的食谱:

            {json.dumps(search_materials, ensure_ascii=False, indent=2)}
            
            请返回最相关的食谱文件名列表，按相关性排序，最多返回5个结果。
            只返回文件名列表，不要包含其他内容。每行一个文件名。
            """
            
            # 调用LLM执行语义搜索
            search_result = session.query(search_prompt, lm=lm)
            
            # 解析结果（假设结果是每行一个文件名）
            matched_filenames = [line.strip() for line in search_result.split('\n') if line.strip()]
            
            # 获取匹配食谱的完整信息
            matches = []
            for filename in matched_filenames:
                for recipe in all_recipes:
                    if recipe.get("filename", "") == filename:
                        matches.append(recipe)
                        break
            
            return {
                "status": "success",
                "query": self.search_query,
                "matches": matches,
                "count": len(matches)
            }
        except Exception as e:
            return {"error": f"搜索食谱时出错: {str(e)}"} 