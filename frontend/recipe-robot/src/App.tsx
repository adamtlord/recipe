import { useEffect, useState } from "react";
import robotImg from "./assets/img/lunchtime.gif";
import { Tooltip } from "react-tooltip";
import axios from "axios";
type Recipe = {
  recipe_name: string;
  ingredients: string[];
  instructions: string;
};
function App() {
  const [apiReady, setApiReady] = useState(false);
  const [apiFailed, setApiFailed] = useState(false);
  useEffect(() => {
    let timeoutId: number | null = null;
    let isCancelled = false;

    const checkApiReady = async () => {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/health`);
        if (!isCancelled) {
          setApiReady(res.status === 200);
        }
        return res.status === 200;
      } catch (error) {
        return false;
      }
    };

    const startTime = Date.now();
    const maxDuration = 60000; // 1 minute
    const retryInterval = 2000; // 2 seconds

    const retryCheck = async () => {
      if (isCancelled) return;

      const isReady = await checkApiReady();

      if (isReady) {
        return; // API is ready, stop retrying
      }

      const elapsed = Date.now() - startTime;
      if (elapsed < maxDuration && !isCancelled) {
        // Schedule next retry
        timeoutId = setTimeout(retryCheck, retryInterval);
      } else if (!isCancelled) {
        // Timeout reached, API failed to start
        setApiFailed(true);
      }
    };

    // Start the initial check
    retryCheck();

    // Cleanup function
    return () => {
      isCancelled = true;
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, []);
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const onAddIngredient = (ingredient: string) => {
    setIngredients([...ingredients, ingredient]);
  };
  const badgeVariant = (i: number) => {
    const variants = [
      "primary",
      "accent",
      "neutral",
      "info",
      "success",
      "warning",
      "error",
    ];
    return variants[i % variants.length];
  };
  const removeIngredient = (i: number) => {
    setIngredients(ingredients.filter((_, index) => index !== i));
  };
  const submitIngredients = async () => {
    setIsLoading(true);
    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}/recipes/generate`,
        { ingredients },
      );
      setRecipes(res.data.recipes);
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };
  const reset = () => {
    setIngredients([]);
    setRecipes([]);
    setIsLoading(false);
  };
  return (
    <div className="mx-auto max-w-4xl min-h-screen font-pressstart">
      <div className="p-8 mx-auto space-y-6 text-center rounded-b-xl bg-slate-700">
        <h1 className="text-5xl font-bold text-primary font-pressstart">
          Recipe Robot
        </h1>

        {apiReady ? (
          <>
            <img src={robotImg} className="block mx-auto max-w-64" />
            <div className="space-x-4">
              <input
                name="ingredient"
                type="text"
                className="w-full rounded-xl join input input-xl input-primary"
                placeholder={
                  ingredients.length > 2
                    ? "Anything else?"
                    : "What do you got on hand?"
                }
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    if (e.currentTarget.value.trim().length > 0) {
                      onAddIngredient(e.currentTarget.value);
                      e.currentTarget.value = "";
                    }
                    if (e.shiftKey) {
                      submitIngredients();
                    }
                  }
                }}
              />
            </div>
          </>
        ) : apiFailed ? (
          <div className="text-red-500">
            The robots could not be roused :(
            <br />
            Please try again later.
          </div>
        ) : (
          <div className="text-red-500">
            <img
              src="https://media.tenor.com/6PA78Ba9-VUAAAAi/zzz-zzzz.gif"
              className="block mx-auto max-w-48"
            />
            Waking up the robots...
            <div className="loading loading-bars loading-lg"></div>
          </div>
        )}
        {ingredients.length > 0 && (
          <div className="flex relative flex-wrap gap-2 justify-center p-6 border-2 border-dashed border-secondary">
            {ingredients.map((ingredient, i) => (
              <div
                key={`${i}-${ingredient}`}
                className={`items-center badge badge-${badgeVariant(i)}`}
              >
                <span>{ingredient}</span>
                <span
                  className="opacity-50 cursor-pointer hover:opacity-100"
                  onClick={() => removeIngredient(i)}
                >
                  x
                </span>
              </div>
            ))}
            <div className="absolute top-0 right-0 text-xs">
              <button
                className="p-1 rounded-none btn btn-ghost btn-square"
                data-tooltip-id="clear-ingredients"
                data-tooltip-place="bottom"
                data-tooltip-delay-show={500}
                onClick={() => setIngredients([])}
              >
                &times;
              </button>
              <Tooltip id="clear-ingredients" content="Clear Ingredients" />
            </div>
          </div>
        )}
        {ingredients.length > 2 && (
          <button
            className="rounded-full animate-pulse btn btn-secondary btn-xl text-primary font-pressstart"
            onClick={submitIngredients}
          >
            Send It
          </button>
        )}
      </div>

      {isLoading && (
        <div className="mt-6 space-y-2">
          <h3 className="text-center animate-pulse text-secondary">
            Robots are thinking real hard...
          </h3>
          <div className="flex flex-wrap gap-2 justify-center">
            {Array.from({ length: ingredients.length }).map((_, i) => (
              <span
                className={`loading loading-spinner text-${badgeVariant(i)}`}
                key={i}
              ></span>
            ))}
          </div>
        </div>
      )}

      {!isLoading && recipes.length > 0 && (
        <div className="mt-6 space-y-4">
          <h2 className="text-2xl text-center text-secondary">
            How about some:
          </h2>
          <div className="join join-vertical">
            {recipes.map((recipe) => (
              <div
                className="border collapse collapse-arrow join-item border-base-300"
                key={recipe.recipe_name}
              >
                <input
                  type="radio"
                  name="recipe-accordion"
                  defaultChecked={false}
                />
                <div className="font-semibold collapse-title">
                  {recipe.recipe_name}
                </div>
                <div className="space-y-2 text-xs leading-relaxed collapse-content">
                  <h3 className="text-accent">Ingredients</h3>
                  <ul className="list-disc list-inside text-white">
                    {recipe.ingredients.map((ingredient) => (
                      <li key={ingredient}>{ingredient}</li>
                    ))}
                  </ul>
                  <h3 className="text-accent">Instructions</h3>
                  <p className="text-white">{recipe.instructions}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="flex justify-center my-4">
            <button
              className="btn btn-primary btn-sm btn-outline"
              onClick={reset}
            >
              Try Again
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
