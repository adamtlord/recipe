import { useState } from "react";
import robotImg from "./assets/img/lunchtime.gif";
function App() {
  const [ingredients, setIngredients] = useState<string[]>([]);
  const onAddIngredient = (ingredient: string) => {
    setIngredients([...ingredients, ingredient]);
  };
  function badgeVariant(i: number) {
    const variants = ['primary', 'secondary', 'accent', 'neutral', 'info', 'success', 'warning', 'error'];
    return variants[i % variants.length];
  }
  return (
    <div className="min-h-screen hero">
      <div className="text-center min-w-4xl bg-slate-700 p-6 rounded-xl space-y-6">
        <h1 className=" text-5xl font-bold text-primary font-pressstart">
          Recipe Robot
        </h1>
        <img src={robotImg} className="block mx-auto rounded-xl max-w-64" />
        <div className="space-x-4">
          <input
            className="input input-primary w-full input-xl"
              placeholder="What you got on hand?"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  onAddIngredient(e.currentTarget.value);
                  e.currentTarget.value = "";
                }
              }}
          />
        </div>
        <div className="flex flex-wrap gap-2 justify-center">
          {ingredients.map((ingredient, i) => (
            <div key={ingredient} className={`badge badge-${badgeVariant(i)}`}>{ingredient}</div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
