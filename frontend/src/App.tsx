import { useCallback } from 'react';
import robotImg from '@/assets/img/lunchtime.gif';
import {
  Header,
  ApiStatusDisplay,
  IngredientForm,
  LoadingDisplay,
  RecipeList,
} from '@/components';
import { useApiStatus, useIngredients, useRecipes } from '@/hooks';

function App() {
  const { apiStatus } = useApiStatus();
  const { ingredients, addIngredient, removeIngredient, clearIngredients } = useIngredients();
  const { recipes, isLoading, generateRecipes, clearRecipes } = useRecipes();

  const handleSubmit = useCallback(async () => {
    try {
      await generateRecipes(ingredients);
    } catch (error) {
      console.error('Failed to generate recipes:', error);
      // TODO: Add proper error handling/toast notification
    }
  }, [ingredients, generateRecipes]);

  const handleTryAgain = useCallback(() => {
    clearIngredients();
    clearRecipes();
  }, [clearIngredients, clearRecipes]);

  const showRobotImage = apiStatus.isReady;
  const showIngredientForm = apiStatus.isReady;
  const showLoadingDisplay = isLoading;
  const showRecipeList = !isLoading && recipes.length > 0;

  return (
    <div className="mx-auto max-w-4xl min-h-screen font-pressstart">
      <Header>
        {showRobotImage && (
          <img src={robotImg} className="block mx-auto max-w-64" alt="Recipe Robot" />
        )}

        {!apiStatus.isReady && <ApiStatusDisplay apiStatus={apiStatus} />}

        {showIngredientForm && (
          <IngredientForm
            ingredients={ingredients}
            onAddIngredient={addIngredient}
            onRemoveIngredient={removeIngredient}
            onClearIngredients={clearIngredients}
            onSubmit={handleSubmit}
          />
        )}
      </Header>

      {showLoadingDisplay && (
        <LoadingDisplay ingredientCount={ingredients.length} />
      )}

      {showRecipeList && (
        <RecipeList
          recipes={recipes}
          onTryAgain={handleTryAgain}
        />
      )}
    </div>
  );
}

export default App;
