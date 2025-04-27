# Smart Recipe Assistant

An intelligent application that generates personalized recipes based on user-provided ingredients and preferences, powered by AI.

## Project Structure

- `/smartChef`: Core Python code
  - `simple_chef.py`: Recipe generation script
  - `web_server.py`: Flask Web server
  - `web_interface.html`: Web interface
- `/recipes`: Directory for generated recipes (automatically created)
- `/images`: Directory for generated recipe images (automatically created)
- `/front-end`: React frontend application
- `/backend-flask`: Flask backend API service (if you're using the advanced version)

## Step-by-Step Installation Guide

### 1. Install Required Dependencies

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/your-username/smartChef.git
cd smartChef

# Install Python dependencies
pip install -r requirements.txt
```

Required packages include:

- flask
- python-dotenv
- openai
- requests
- pillow
- markdown

### 2. Configure Environment Variables

```bash
# Create .env file (or copy from example)
cp .env.example .env

# Edit the .env file with your API keys
# OPENAI_API_KEY=sk-your-openai-api-key
```

**Important:** The `.env` file is ignored in `.gitignore` to protect your API keys.

### 3. Backend Setup

```bash
# Start the Flask server (simple version)
python smartChef/web_server.py

# The server will run at http://localhost:5001
```

For advanced backend setup:

```bash
# Navigate to backend directory
cd backend-flask

# Install specific backend dependencies (if any)
pip install -r requirements.txt

# Start the server
python app.py
```

### 4. Frontend Setup

For the React frontend:

```bash
# Navigate to frontend directory
cd front-end

# Install Node.js dependencies
npm install

# Start the development server
npm run dev

# The frontend will run at http://localhost:3000
```

## How to Use

1. Open the application in your web browser
2. Enter ingredients you have on hand
3. Select cuisine preferences (Chinese, Italian, etc.)
4. Add any dietary restrictions or preferences
5. Generate your recipe
6. Save or print the resulting recipe with its image

## Features

- Generate creative recipes based on available ingredients
- Multiple cuisine options
- Dietary restriction support (vegetarian, gluten-free, low-fat, etc.)
- Beautiful AI-generated recipe images
- Recipe history saved locally
- Printable recipe cards

## Example Generated Recipes

The application has successfully generated recipes like:

- Chinese Tomato and Egg Stir-Fry
- Spicy Szechuan Beef Stir-Fry
- Hearty Beef and Tomato Stew
- Silken Egg Custard with Soy Sauce Glaze

## Tech Stack

- **Frontend**: React, HTML/CSS/JavaScript
- **Backend**: Flask, Python
- **AI**: OpenAI API (GPT for recipe generation, DALL-E for images)

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly formatted in the `.env` file
- **Image Generation Fails**: Check your OpenAI account has DALL-E access and sufficient credits
- **Recipe Not Generating**: Ensure you've provided at least 2-3 ingredients

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
