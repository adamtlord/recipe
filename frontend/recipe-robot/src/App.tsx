import { useState } from "react";
import robotImg from "./assets/img/lunchtime.gif";
function App() {
  const [ingredients, setIngredients] = useState<string[]>([]);
  const onAddIngredient = (ingredient: string) => {
    setIngredients([...ingredients, ingredient]);
  };
  function badgeVariant(i: number) {
    const variants = ['primary',  'accent', 'neutral', 'info', 'success', 'warning', 'error'];
    return variants[i % variants.length];
  }
  return (
    <div className="min-h-screen font-pressstart">
      <div className="p-8 mx-auto mt-16 space-y-6 max-w-4xl text-center rounded-xl bg-slate-700">
        <h1 className="text-5xl font-bold text-primary font-pressstart">
          Recipe Robot
        </h1>
        <img src={robotImg} className="block mx-auto max-w-64" />
        <div className="space-x-4">
          <input
            className="w-full input input-primary input-xl"
              placeholder={ingredients.length > 2 ? "Anything else?" : "What you got on hand?"}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  onAddIngredient(e.currentTarget.value);
                  e.currentTarget.value = "";
                }
              }}
          />
        </div>
        {ingredients.length > 0 && (
        <div className="flex flex-wrap gap-2 justify-center">
          {ingredients.map((ingredient, i) => (
            <div key={ingredient} className={`badge badge-${badgeVariant(i)}`}>{ingredient}</div>
            ))}
          </div>
        )}
        {ingredients.length > 2 && <button className="rounded-full animate-pulse btn btn-secondary btn-xl text-primary font-pressstart">Send It</button>}
      </div>
    </div>
  );
}

export default App;
