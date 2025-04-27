import React, { useState } from 'react';
import './App.css';



function RecipePage() {
  const [ingredients, setIngredients] = useState('');
  const [cuisine, setCuisine] = useState('Chinese');
  const [requirements, setRequirements] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [recipeData, setRecipeData] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const generateRecipe = async (isRegenerate = false) => {
    if (!ingredients) {
      alert("Please enter ingredients!");
      return;
    }

    setLoading(true);
    setErrorMessage('');
    setRecipeData(null);
    setShowConfirmation(false);

    try {
      const apiUrl = isRegenerate
        ? "/api/regenerate-recipe"
        : "/api/generate-recipe";

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ingredients: ingredients,
          cuisine_type: cuisine,
          special_requirements: requirements,
          generate_ai_image: true,
          generate_image_now: false,
        }),
      });

      if (!response.ok) {
        throw new Error("Error generating recipe, please try again later");
      }

      const data = await response.json();
      console.log("Recipe API response:", data); // 添加调试日志
      setRecipeData(data);
      setShowConfirmation(data.needUserConfirmation || false);
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const acceptRecipe = async () => {
    if (!recipeData) return;

    setLoading(true);
    setShowConfirmation(false);

    try {
      const response = await fetch("/api/generate-recipe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ingredients: ingredients,
          cuisine_type: cuisine,
          special_requirements: requirements,
          generate_ai_image: true,
          generate_image_now: true,
          recipe_markdown: recipeData.markdown,
        }),
      });

      if (!response.ok) {
        throw new Error("Error generating image, please try again later");
      }

      const data = await response.json();
      console.log("Recipe with image response:", data); // 添加调试日志
      setRecipeData(data);
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const regenerateRecipe = () => {
    generateRecipe(true);
  };

  const RecipeDisplay = ({ recipe }) => {
    if (!recipe) return null;

    return (

      <div id="recipe-result">
        <h2>{recipe.name}</h2>

        <h3>Ingredients:</h3>
        <ul>
          {recipe.ingredients?.map((ingredient, index) => (
            <li key={index}>{ingredient}</li>
          ))}
        </ul>

        <h3>Cooking Steps:</h3>
        <ol>
          {recipe.steps?.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>

        <h3>Cooking Tips:</h3>
        <ul>
          {recipe.tips?.map((tip, index) => (
            <li key={index}>{tip}</li>
          ))}
        </ul>

        <p><strong>Prep Time:</strong> {recipe.prepTime} minutes</p>
        <p><strong>Cooking Time:</strong> {recipe.cookTime} minutes</p>

        {recipe.imageUrl && (
          <>
            <h3>
              Final Dish
              {recipe.aiImageGenerated && (
                <span className="ai-image-badge">AI Generated</span>
              )}
            </h3>
            <img
              id="recipe-img"
              src={recipe.imageUrl}
              alt={recipe.name}
              loading="lazy"
            />
          </>
        )}

        {recipe.savedFile && (
          <p><small>Recipe saved to: {recipe.savedFile}</small></p>
        )}
      </div>
    );
  };

  return (
    <div className="container">
      <h1>Smart Chef Assistant</h1>
      <div className="form-group">
        <label htmlFor="ingredients">Available Ingredients (comma separated):</label>
        <textarea
          id="ingredients"
          rows="3"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          placeholder="Example: eggs, tomatoes, bell peppers"
        ></textarea>
      </div>
      <div className="form-group">
        <label htmlFor="cuisine">Desired Cuisine:</label>
        <select
          id="cuisine"
          value={cuisine}
          onChange={(e) => setCuisine(e.target.value)}
        >
          <option value="Chinese">Chinese</option>
          <option value="Western">Western</option>
          <option value="Japanese">Japanese</option>
          <option value="Korean">Korean</option>
          <option value="Southeast Asian">Southeast Asian</option>
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="requirements">Special Requirements (optional):</label>
        <input
          type="text"
          id="requirements"
          value={requirements}
          onChange={(e) => setRequirements(e.target.value)}
          placeholder="Example: low calorie, sugar-free, vegetarian"
        />
      </div>
      <button
        id="generate-btn"
        onClick={() => generateRecipe()}
        disabled={loading}
      >
        Generate Recipe
      </button>

      {loading && (
        <div id="loading">
          <p>AI is carefully creating your recipe, please wait...</p>
          <div className="spinner"></div>
        </div>
      )}

      {errorMessage && (
        <div id="error-message" className="error">
          {errorMessage}
        </div>
      )}

      {recipeData && <RecipeDisplay recipe={recipeData} />}

      {showConfirmation && (
        <div id="confirmation-buttons" style={{ marginTop: "20px" }}>
          <div style={{ display: "flex", gap: "10px" }}>
            <button
              id="accept-btn"
              style={{ backgroundColor: "#4caf50", flex: 1 }}
              onClick={acceptRecipe}
            >
              Accept this Recipe
            </button>
            <button
              id="regenerate-btn"
              style={{ backgroundColor: "#f39c12", flex: 1 }}
              onClick={regenerateRecipe}
            >
              Try Another Recipe
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default RecipePage;