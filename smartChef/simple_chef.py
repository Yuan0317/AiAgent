"""
SmartChef Simplified Version - Direct OpenAI API Call
"""
import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import httpx

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("没有设置OPENAI_API_KEY环境变量。请在.env文件中设置。")

# 从环境变量获取配置目录
RECIPES_DIR = os.environ.get('RECIPES_DIR', 'recipes')
IMAGES_DIR = os.environ.get('IMAGES_DIR', 'images')

# 创建OpenAI客户端
http_client = httpx.Client()
client = OpenAI(api_key=openai_api_key, http_client=http_client)

# 确保recipes目录存在
os.makedirs(RECIPES_DIR, exist_ok=True)

def generate_recipe(ingredients, cuisine_type, special_requirements=None):
    """使用OpenAI API生成食谱"""
    
    print(f"📋 Generating {cuisine_type} recipe")
    print(f"Ingredients: {ingredients}")
    if special_requirements:
        print(f"Special requirements: {special_requirements}")
    
    # 构建提示词
    prompt = f"""Create a detailed {cuisine_type} recipe using the following ingredients:
    
    Available ingredients: {ingredients}
    
    {'Special requirements: ' + special_requirements if special_requirements else ''}
    
    Please provide:
    1. Creative dish name
    2. Detailed ingredients list (with quantities)
    3. Step-by-step preparation and cooking instructions
    4. Cooking tips and tricks
    5. Estimated preparation and cooking time
    
    Please use Markdown format and ensure the recipe follows {cuisine_type} style.
    """
    
    try:
        # 调用OpenAI API
        print("🤖 Calling OpenAI API to generate recipe...")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional chef skilled at creating delicious recipes from available ingredients."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # 提取生成的食谱
        recipe_markdown = response.choices[0].message.content.strip()
        
        # 计算并显示API调用时间
        elapsed_time = time.time() - start_time
        print(f"✅ Recipe generation complete! (Time: {elapsed_time:.2f} seconds)")
        
        return recipe_markdown
        
    except Exception as e:
        print(f"❌ OpenAI API call failed: {str(e)}")
        print("⚠️ Using pre-set mock data as fallback...")
        
        # 返回模拟数据
        return generate_mock_recipe(ingredients, cuisine_type, special_requirements)

def generate_mock_recipe(ingredients, cuisine_type, special_requirements=None):
    """Generate mock recipe data when API call fails"""
    
    # Parse ingredients
    ingredient_list = [i.strip() for i in ingredients.split(',')]
    
    # Choose appropriate mock recipe based on ingredients and cuisine
    if "eggs" in ingredient_list:
        if cuisine_type == "Chinese":
            if "milk" in ingredient_list:
                return """# Steamed Milk Custard

## Ingredients
- 3 eggs
- 200ml milk
- 1/4 teaspoon salt
- Green onion (for garnish)

## Steps
1. Beat eggs in a bowl, mix evenly but avoid creating bubbles
2. Heat milk until warm (do not boil)
3. Slowly pour warm milk into beaten eggs while stirring
4. Add salt to taste, continue stirring
5. Strain the mixture to remove impurities
6. Pour mixture into a heat-resistant container
7. Steam for 15 minutes (medium-low heat after water boils)
8. Sprinkle with green onion before serving

## Cooking Tips
- Do not uncover while steaming to keep the surface smooth
- Straining helps create a silky texture
- Milk temperature should not be too high to avoid premature coagulation
- A few drops of sesame oil can enhance flavor

## Time
- Preparation time: 10 minutes
- Cooking time: 15 minutes
- Total time: 25 minutes

## Nutrition Information
This steamed milk custard is low in calories and rich in protein, perfect for a low-calorie diet."""
            else:
                return """# Steamed Eggs with Green Onion

## Ingredients
- 3 eggs
- 240ml water
- 1/4 teaspoon salt
- Green onion, chopped
- Sesame oil, few drops

## Steps
1. Beat eggs in a bowl with chopsticks until evenly mixed
2. Add water and salt, using a 1:1.3 ratio (eggs:water)
3. Continue mixing, then strain once
4. Pour mixture into a bowl, sprinkle with green onion
5. Steam for 10-15 minutes (medium-low heat after water boils)
6. Add a few drops of sesame oil before serving

## Cooking Tips
- Do not uncover while steaming to keep the surface smooth
- Straining helps create a silky texture
- Water should not be too hot to avoid premature coagulation
- You can line the bowl with plastic wrap for easy removal

## Time
- Preparation time: 5 minutes
- Cooking time: 15 minutes
- Total time: 20 minutes

## Nutrition Information
This steamed egg dish is low in calories and rich in protein, perfect for a low-calorie diet."""
        elif cuisine_type == "Western":
            return """# Low-Calorie French Scrambled Eggs

## Ingredients
- 2 eggs
- 50ml milk
- Black pepper, to taste
- Salt, to taste
- 5ml olive oil
- Parsley, for garnish

## Steps
1. Crack eggs into a bowl, add milk, salt, and black pepper
2. Lightly mix with a fork
3. Heat a non-stick pan on low heat, add olive oil
4. Pour in egg mixture, continuously stir with a rubber spatula
5. When eggs become thick but still moist, remove from heat
6. Residual heat will continue cooking the eggs, maintaining a creamy texture
7. Serve immediately, garnish with parsley

## Cooking Tips
- Use low heat throughout to prevent eggs from becoming tough
- Constant stirring creates small, delicate curds
- Remove from heat when eggs are 70% done; residual heat will finish cooking
- Add a small amount of chopped vegetables to enhance nutritional value

## Time
- Preparation time: 5 minutes
- Cooking time: 3-5 minutes
- Total time: 10 minutes

## Nutrition Information
These French scrambled eggs are relatively low in calories, especially using a small amount of olive oil instead of butter, making them suitable for a low-calorie diet."""
    
    elif "beef" in ingredient_list:
        if cuisine_type == "Chinese":
            return """# Low-Fat Clear Beef Soup

## Ingredients
- 300g lean beef
- 5 slices ginger
- 3 green onion sections
- 1 star anise
- 1 tablespoon cooking wine
- Salt to taste
- 1500ml water

## Steps
1. Wash beef and cut into 4cm cubes
2. Add water to pot, add beef and bring to boil
3. Skim off foam, add ginger, green onion, star anise and cooking wine
4. Turn to low heat and simmer for 1.5 hours until beef is tender
5. Season with salt to taste

## Cooking Tips
- Select lean beef cuts to reduce fat intake
- Sufficient cooking time is needed for tender beef
- You can make this a day ahead, chill it, and remove solidified fat before reheating
- Do not add oil, rely on the natural flavor of beef

## Time
- Preparation time: 15 minutes
- Cooking time: 90 minutes
- Total time: 105 minutes

## Nutrition Information
This clear beef soup adds no extra oil and uses lean beef cuts, making it a low-fat, high-protein healthy dish."""
    
    # Default return generic recipe
    return f"""# Simple {cuisine_type} Healthy Meal

## Ingredients
{', '.join('- ' + ing for ing in ingredient_list)}
- Salt to taste
- Black pepper to taste

## Steps
1. Prepare all ingredients, wash thoroughly
2. Choose appropriate cooking method based on ingredients
3. Control oil usage, preferably use steaming, boiling, or stewing methods
4. Season appropriately, focus on natural flavors of ingredients

## Cooking Tips
- Reduce oil and salt to lower calorie intake
- Preserve natural flavors of ingredients, use fewer seasonings
- Add herbs for flavor to reduce salt usage

## Time
- Preparation time: 10 minutes
- Cooking time: 20 minutes
- Total time: 30 minutes

## Nutrition Information
This is a healthy recipe that meets low-calorie requirements while preserving nutritional value and reducing unnecessary calorie intake."""

def generate_image(dish_name):
    """Generate food image URL using Unsplash (since OpenAI image generation is paid)"""
    
    # For simplicity, use Unsplash random image API
    # Clean search keywords, remove special characters
    clean_dish_name = dish_name.replace("*", "").replace("\"", "").replace("?", "").replace(":", "").replace("<", "").replace(">", "").replace("|", "")
    dish_name_escaped = clean_dish_name.replace(" ", "+")
    image_url = f"https://source.unsplash.com/random/800x600/?food,{dish_name_escaped}"
    
    return image_url

def save_recipe(recipe_content, recipe_name=None):
    """保存食谱到文件"""
    
    # 如果没有提供菜名，尝试从内容中提取
    if not recipe_name:
        # 尝试从markdown标题中提取菜名
        lines = recipe_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                recipe_name = line[2:].strip()
                break
        
        # 如果仍然没有菜名，使用默认名称
        if not recipe_name:
            recipe_name = "Delicious Recipe"
    
    print(f"💾 Saving recipe: {recipe_name}")
    
    # 创建文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 清除文件名中的特殊字符
    safe_name = recipe_name.replace("*", "").replace("\"", "").replace("?", "").replace(":", "").replace("<", "").replace(">", "").replace("|", "").replace("/", "_").replace("\\", "_").replace(" ", "_")
    filename = f"{RECIPES_DIR}/{safe_name}_{timestamp}.md"
    
    # 添加元数据
    metadata = f"""---
name: {recipe_name}
created_at: {timestamp}
tags: [AI Generated]
---

"""
    
    # 获取菜品图片URL
    image_url = generate_image(recipe_name)
    
    # 在食谱末尾添加图片
    recipe_with_image = recipe_content + f"\n\n![{recipe_name}]({image_url})\n"
    
    # 保存到文件
    try:
        with open(filename, "w", encoding="utf-8-sig") as f:
            f.write(metadata + recipe_with_image)
        print(f"✅ Recipe saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Failed to save recipe: {str(e)}")
        # 如果文件名有问题，使用默认名称
        safe_filename = f"{RECIPES_DIR}/recipe_{timestamp}.md"
        with open(safe_filename, "w", encoding="utf-8-sig") as f:
            f.write(metadata + recipe_with_image)
        print(f"✅ Saved using fallback filename: {safe_filename}")
        return safe_filename

def main():
    """Main function"""
    print("=" * 50)
    print("Welcome to SmartChef - Intelligent Recipe Assistant (Simplified Version)")
    print("=" * 50)
    
    # Get user input
    print("\nPlease enter your available ingredients (comma separated):")
    ingredients = input("> ")
    
    print("\nPlease select cuisine type (e.g., Chinese, Western, Japanese, etc.):")
    cuisine_type = input("> ")
    
    print("\nPlease enter special requirements (optional, e.g., spicy, low-calorie, etc.):")
    special_requirements = input("> ")
    if not special_requirements.strip():
        special_requirements = None
    
    print("\n" + "=" * 50)
    print("Generating your custom recipe, please wait...")
    print("=" * 50 + "\n")
    
    # Generate recipe
    recipe_markdown = generate_recipe(ingredients, cuisine_type, special_requirements)
    
    if recipe_markdown:
        # Extract dish name
        recipe_name = None
        lines = recipe_markdown.split('\n')
        for line in lines:
            if line.startswith('# '):
                recipe_name = line[2:].strip()
                break
        
        # Save recipe
        saved_file = save_recipe(recipe_markdown, recipe_name)
        
        # Print recipe preview
        print("\n📝 Recipe Preview:\n")
        preview_lines = recipe_markdown.split('\n')[:15]  # Only show first 15 lines
        print("\n".join(preview_lines))
        print("...\n[See saved file for complete recipe]")
    else:
        print("❌ Unable to generate recipe, please try again later.")
    
    print("\n" + "=" * 50)
    print("Thank you for using SmartChef!")
    print("=" * 50)

if __name__ == "__main__":
    main()