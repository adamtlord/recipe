import robotImg from "./assets/img/lunchtime.gif";

function App() {
  return (
    <div className="min-h-screen hero">
      <div className="text-center min-w-4xl bg-slate-700 p-6 rounded-xl">
        <h1 className="mb-6 text-5xl font-bold text-primary font-pressstart">Recipe Robot</h1>
        <img src={robotImg} className="block mx-auto rounded-xl max-w-64" />
        <div className="pt-6 space-x-4">
          <input
            className="w-full input input-xl input-primary"
            placeholder="Enter some ingredients"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
