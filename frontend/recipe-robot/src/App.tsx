import { useState } from "react";
import robotImg from "./assets/img/lunchtime.gif";
function App() {
  const [ingredients, setIngredients] = useState<string[]>([]);
  const onAddIngredient = (ingredient: string) => {
    setIngredients([...ingredients, ingredient]);
  };
  const badgeVariant = (i: number) => {
    const variants = ['primary',  'accent', 'neutral', 'info', 'success', 'warning', 'error'];
    return variants[i % variants.length];
  }
  const removeIngredient = (i: number) => {
    setIngredients(ingredients.filter((_, index) => index !== i));
  };
  const submitIngredients = () => {
    alert("oh shit SUBMIT");
  };
  return (
    <div className="min-h-screen font-pressstart">
      <div className="p-8 mx-auto mt-16 space-y-6 max-w-4xl text-center rounded-xl bg-slate-700">
        <h1 className="text-5xl font-bold text-primary font-pressstart">
          Recipe Robot
        </h1>
        <img src={robotImg} className="block mx-auto max-w-64" />
        <div className="space-x-4">
        <label className="w-full rounded-xl join input input-xl input-primary">
          <input
              placeholder={ingredients.length > 2 ? "Anything else?" : "What you got on hand?"}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  if(e.currentTarget.value.trim(). length > 0) {
                    onAddIngredient(e.currentTarget.value);
                    e.currentTarget.value = "";
                  }
                  if(e.shiftKey) {
                   submitIngredients();
                  }
                }
              }}
          />
          <button onClick={() => setIngredients([])} className="text-xl cursor-pointer">&times;</button>
          </label>
        </div>
        {ingredients.length > 0 && (
        <div className="flex flex-wrap gap-2 justify-center">
          {ingredients.map((ingredient, i) => (
            <div key={ingredient} className={`items-center badge badge-${badgeVariant(i)}`}><span>{ingredient}</span><span className="opacity-50 cursor-pointer hover:opacity-100" onClick={() => removeIngredient(i)}>x</span></div>
            ))}
          </div>
        )}
        {ingredients.length > 2 && <button className="rounded-full animate-pulse btn btn-secondary btn-xl text-primary font-pressstart" onClick={submitIngredients}>Send It</button>}
      </div>
    </div>
  );
}

export default App;
