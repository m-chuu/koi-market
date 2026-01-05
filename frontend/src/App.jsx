import { useState } from 'react';

// --- MOCK DATA (Simulates your future Database) ---
const MOCK_KOI = [
  {
    id: 1,
    name: "Tancho Kohaku",
    price: 1200,
    category: "Kohaku",
    image: "https://placehold.co/400x300/ff7b7b/white?text=Tancho+Kohaku", // Placeholder image
    description: "Pristine white body with a perfect round red spot on the head."
  },
  {
    id: 2,
    name: "Showa Sanshoku",
    price: 850,
    category: "Showa",
    image: "https://placehold.co/400x300/333/white?text=Showa",
    description: "Beautiful balance of red, white, and black patterns."
  },
  {
    id: 3,
    name: "Ogon Yamabuki",
    price: 2500,
    category: "Ogon",
    image: "https://placehold.co/400x300/ffd700/333?text=Ogon+Gold",
    description: "Solid metallic gold color. A symbol of wealth."
  }
];

function App() {
  const [cart, setCart] = useState([]);

  // Simple "Add to Cart" Logic
  const addToCart = (koi) => {
    setCart([...cart, koi]);
    alert(`Added ${koi.name} to cart!`);
  };

  return (
    <div className="min-h-screen">
      
      {/* --- NAVBAR --- */}
      <nav className="bg-white shadow-md p-4 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-red-600">Koi Market 🎏</h1>
          <div className="flex items-center gap-4">
            <button className="bg-slate-100 px-4 py-2 rounded-lg font-medium hover:bg-slate-200 transition">
              Cart ({cart.length})
            </button>
          </div>
        </div>
      </nav>

      {/* --- HERO SECTION --- */}
      <header className="bg-red-50 py-12 text-center">
        <h2 className="text-4xl font-extrabold text-slate-800 mb-2">Premium Japanese Koi</h2>
        <p className="text-slate-600">Hand-selected for quality and elegance.</p>
      </header>

      {/* --- PRODUCT GRID --- */}
      <main className="max-w-6xl mx-auto p-6">
        <h3 className="text-xl font-bold mb-6 text-slate-700">Available Fish</h3>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          {MOCK_KOI.map((koi) => (
            <div key={koi.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-slate-100">
              {/* Image Area */}
              <div className="h-48 overflow-hidden bg-gray-200">
                <img 
                  src={koi.image} 
                  alt={koi.name} 
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
                />
              </div>
              
              {/* Content Area */}
              <div className="p-5">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="text-lg font-bold text-slate-800">{koi.name}</h4>
                  <span className="bg-red-100 text-red-600 text-xs font-bold px-2 py-1 rounded-full">
                    {koi.category}
                  </span>
                </div>
                
                <p className="text-sm text-slate-500 mb-4 line-clamp-2">
                  {koi.description}
                </p>
                
                <div className="flex justify-between items-center mt-4 border-t pt-4 border-slate-100">
                  <span className="text-xl font-bold text-slate-900">
                    ${koi.price}
                  </span>
                  <button 
                    onClick={() => addToCart(koi)}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 active:scale-95 transition"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

    </div>
  );
}

export default App;