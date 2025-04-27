from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import base64
import requests
from simple_chef import generate_recipe, generate_image, save_recipe
from openai import OpenAI
from dotenv import load_dotenv
import time
import json
from flask_cors import CORS
import httpx

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("没有设置OPENAI_API_KEY环境变量。请在.env文件中设置。")

# 从环境变量获取配置
FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.environ.get('FLASK_PORT', 5001))
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
IMAGES_DIR = os.environ.get('IMAGES_DIR', 'images')
RECIPES_DIR = os.environ.get('RECIPES_DIR', 'recipes')

# 创建OpenAI客户端
http_client = httpx.Client()
client = OpenAI(api_key=openai_api_key, http_client=http_client)

app = Flask(__name__)
CORS(app)

@app.route('/')
# def index():
#     # Serve the HTML page
#     return send_from_directory('.', 'web_interface.html')

def generate_recipe_image(recipe_name, recipe_description):
    """使用OpenAI DALL-E 3生成食谱图片"""
    try:
        # 清除文件名中的特殊字符
        clean_name = recipe_name.replace("*", "").replace("\"", "").replace("?", "").replace(":", "").replace("<", "").replace(">", "").replace("|", "").replace("/", "_").replace("\\", "_")
        
        # 构建提示词
        prompt = f"Minimalist style infographic of {recipe_name} preparation steps on white background. Include labeled photos of all ingredients, connect with dotted lines to cooking step icons (such as mixing bowl, frying pan, stirring icons). Bottom of infographic shows final plated {recipe_name}. {recipe_description} Clean layout with soft shadows, neat typography, modern minimalist style."
        
        print(f"Generating minimalist style infographic for {recipe_name}...")
        
        # 调用DALL-E 3 API生成图片
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # 获取图片URL
        image_url = response.data[0].url
        print(f"✅ Image generation successful!")
        
        # 在本地保存图片
        try:
            img_data = requests.get(image_url).content
            # 创建图片目录
            os.makedirs(IMAGES_DIR, exist_ok=True)
            # 生成文件名
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{IMAGES_DIR}/{clean_name}_{timestamp}.png"
            # 保存图片
            with open(filename, 'wb') as handler:
                handler.write(img_data)
            print(f"✅ Image saved to: {filename}")
            
            # 返回本地图片路径和原始URL
            return {
                "local_path": filename,
                "url": image_url
            }
        except Exception as e:
            print(f"❌ Failed to save image: {str(e)}")
            # 如果保存失败，仍返回在线URL
            return {
                "url": image_url
            }
        
    except Exception as e:
        print(f"❌ Image generation failed: {str(e)}")
        # 使用备用方法生成图片URL
        fallback_url = generate_image(recipe_name)
        return {
            "url": fallback_url,
            "fallback": True
        }

@app.route('/api/generate-recipe', methods=['POST'])
def api_generate_recipe():
    try:
        # Get request data
        data = request.json
        ingredients = data.get('ingredients', '')
        cuisine_type = data.get('cuisine_type', '')
        special_requirements = data.get('special_requirements', '')
        generate_ai_image = data.get('generate_ai_image', True)  # Flag to generate AI image
        generate_image_now = data.get('generate_image_now', False)  # Flag to generate image immediately
        recipe_md = data.get('recipe_markdown', '')  # If request is from "Accept" button, includes already generated recipe
        
        if not ingredients or not cuisine_type:
            return jsonify({'error': 'Please provide ingredients and cuisine type'}), 400
        
        # If recipe already generated, use it, otherwise generate new one
        if generate_image_now and recipe_md:
            recipe_markdown = recipe_md
        else:
            # Call simple_chef.py to generate recipe
            recipe_markdown = generate_recipe(ingredients, cuisine_type, special_requirements)
        
        # Extract dish name
        recipe_name = None
        lines = recipe_markdown.split('\n')
        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                recipe_name = line.replace('#', '').strip()
                break
        
        if not recipe_name:
            recipe_name = "Delicious Recipe"
        
        # Parse recipe content to extract structured data
        ingredients_list = []
        steps_list = []
        tips_list = []
        prep_time = "15"
        cook_time = "30"
        recipe_description = ""
        
        section = None
        for line in lines:
            line = line.strip()
            if line.startswith('## Ingredients') or line.startswith('### Ingredients'):
                section = 'ingredients'
                continue
            elif line.startswith('## Steps') or line.startswith('### Steps') or line.startswith('## Preparation') or line.startswith('### Preparation'):
                section = 'steps'
                continue
            elif line.startswith('## Cooking Tips') or line.startswith('### Cooking Tips'):
                section = 'tips'
                continue
            elif line.startswith('## Time') or line.startswith('### Time'):
                section = 'time'
                continue
            elif line.startswith('##') or line.startswith('###'):
                section = None
                continue
                
            if section == 'ingredients' and line.startswith('-'):
                ingredients_list.append(line[1:].strip())
            elif section == 'steps' and (line.startswith('-') or line.startswith('1.') or line.startswith('1、')):
                # Remove number prefix
                step = line
                if line[0].isdigit():
                    parts = line.split('.', 1) if '.' in line else line.split('、', 1)
                    if len(parts) > 1:
                        step = parts[1].strip()
                elif line.startswith('-'):
                    step = line[1:].strip()
                steps_list.append(step)
            elif section == 'tips' and line.startswith('-'):
                tips_list.append(line[1:].strip())
            elif section == 'time' and ('Preparation time' in line or 'Prep time' in line):
                if 'Preparation time' in line or 'Prep time' in line:
                    prep_parts = line.split(':', 1) if ':' in line else line.split('：', 1)
                    if len(prep_parts) > 1:
                        prep_time = prep_parts[1].strip().split(' ')[0]
                if 'Cooking time' in line:
                    cook_parts = line.split(':', 1) if ':' in line else line.split('：', 1)
                    if len(cook_parts) > 1:
                        cook_time = cook_parts[1].strip().split(' ')[0]
        
        # Build dish description for image generation
        recipe_description = f"A {cuisine_type} dish made with {', '.join(ingredients_list[:3])} and other ingredients."
        
        # If not generating image immediately, return structured data without image
        if not generate_image_now:
            return jsonify({
                'name': recipe_name,
                'ingredients': ingredients_list,
                'steps': steps_list,
                'tips': tips_list,
                'prepTime': prep_time,
                'cookTime': cook_time,
                'markdown': recipe_markdown,
                'needUserConfirmation': True  # Indicate to frontend to show confirmation button
            })
        
        # Based on user choice, decide whether to use AI to generate image
        if generate_ai_image:
            # Use DALL-E to generate more realistic recipe image
            image_result = generate_recipe_image(recipe_name, recipe_description)
            image_url = image_result.get('url')
            local_image_path = image_result.get('local_path', '')
        else:
            # Use Unsplash random image
            image_url = generate_image(recipe_name)
            local_image_path = ""
        
        # Save recipe
        saved_file = save_recipe(recipe_markdown, recipe_name)
        
        # Return structured data
        return jsonify({
            'name': recipe_name,
            'ingredients': ingredients_list,
            'steps': steps_list,
            'tips': tips_list,
            'prepTime': prep_time,
            'cookTime': cook_time,
            'imageUrl': image_url,
            'localImagePath': local_image_path,
            'markdown': recipe_markdown,
            'savedFile': saved_file,
            'aiImageGenerated': generate_ai_image,
            'needUserConfirmation': False  # Already confirmed, no need to show confirmation button
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Error generating recipe: {str(e)}'}), 500

@app.route('/api/regenerate-recipe', methods=['POST'])
def api_regenerate_recipe():
    """API endpoint to regenerate recipe"""
    try:
        # Get request data
        data = request.json
        ingredients = data.get('ingredients', '')
        cuisine_type = data.get('cuisine_type', '')
        special_requirements = data.get('special_requirements', '')
        
        if not ingredients or not cuisine_type:
            return jsonify({'error': 'Please provide ingredients and cuisine type'}), 400
        
        # Call simple_chef.py to generate new recipe
        recipe_markdown = generate_recipe(ingredients, cuisine_type, special_requirements)
        
        # Extract dish name and other structured data
        recipe_name = None
        ingredients_list = []
        steps_list = []
        tips_list = []
        prep_time = "15"
        cook_time = "30"
        
        lines = recipe_markdown.split('\n')
        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                recipe_name = line.replace('#', '').strip()
                break
        
        if not recipe_name:
            recipe_name = "Delicious Recipe"
        
        # Parse recipe content to extract structured data
        section = None
        for line in lines:
            line = line.strip()
            if line.startswith('## Ingredients') or line.startswith('### Ingredients'):
                section = 'ingredients'
                continue
            elif line.startswith('## Steps') or line.startswith('### Steps') or line.startswith('## Preparation') or line.startswith('### Preparation'):
                section = 'steps'
                continue
            elif line.startswith('## Cooking Tips') or line.startswith('### Cooking Tips'):
                section = 'tips'
                continue
            elif line.startswith('## Time') or line.startswith('### Time'):
                section = 'time'
                continue
            elif line.startswith('##') or line.startswith('###'):
                section = None
                continue
                
            if section == 'ingredients' and line.startswith('-'):
                ingredients_list.append(line[1:].strip())
            elif section == 'steps' and (line.startswith('-') or line.startswith('1.') or line.startswith('1、')):
                # Remove number prefix
                step = line
                if line[0].isdigit():
                    parts = line.split('.', 1) if '.' in line else line.split('、', 1)
                    if len(parts) > 1:
                        step = parts[1].strip()
                elif line.startswith('-'):
                    step = line[1:].strip()
                steps_list.append(step)
            elif section == 'tips' and line.startswith('-'):
                tips_list.append(line[1:].strip())
            elif section == 'time' and ('Preparation time' in line or 'Prep time' in line):
                if 'Preparation time' in line or 'Prep time' in line:
                    prep_parts = line.split(':', 1) if ':' in line else line.split('：', 1)
                    if len(prep_parts) > 1:
                        prep_time = prep_parts[1].strip().split(' ')[0]
                if 'Cooking time' in line:
                    cook_parts = line.split(':', 1) if ':' in line else line.split('：', 1)
                    if len(cook_parts) > 1:
                        cook_time = cook_parts[1].strip().split(' ')[0]
        
        return jsonify({
            'name': recipe_name,
            'ingredients': ingredients_list,
            'steps': steps_list,
            'tips': tips_list,
            'prepTime': prep_time,
            'cookTime': cook_time,
            'markdown': recipe_markdown,
            'needUserConfirmation': True  # Needs user confirmation
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Error regenerating recipe: {str(e)}'}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

if __name__ == '__main__':
    # 确保recipes和images目录存在
    os.makedirs(RECIPES_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT, host=FLASK_HOST)