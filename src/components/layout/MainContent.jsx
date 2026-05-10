import { useState, useEffect } from 'react'
import ProductCard from '../common/ProductCard'
import ShoppingCart from '../common/ShoppingCart'
import { fetchProducts } from '../../services/api'
import localProducts from '../../data/products'
import backgroundImg from '../../assets/images/background.jpeg'
import './MainContent.css'

function MainContent() {
  const [products, setProducts] = useState([])
  const [cartItems, setCartItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchProducts()
      setProducts(data.products)
    } catch (err) {
      console.warn('API unavailable, using local data:', err.message)
      setProducts(localProducts)
    } finally {
      setLoading(false)
    }
  }

  const addToCart = (product) => {
    setCartItems([...cartItems, product])
  }

  const removeFromCart = (productId) => {
    const index = cartItems.findIndex(item => item.id === productId)
    if (index !== -1) {
      const newCartItems = [...cartItems]
      newCartItems.splice(index, 1)
      setCartItems(newCartItems)
    }
  }

  const totalPrice = cartItems.reduce((total, item) => total + item.price.min, 0)

  return (
    <div className="main-content" style={{ backgroundImage: `url(${backgroundImg})` }}>
      <header className="header">
        <h1>Koi Fish Store <span className="header-cn">锦鲤商店</span></h1>
        <p className="header-subtitle">Premium Japanese Koi · 日本锦鲤专卖</p>
      </header>

      <div className="content-wrapper">
        <main className="products-section">
          <h2 className="section-title">Our Koi Collection 锦鲤系列</h2>

          {loading && (
            <div className="loading-state">
              <p>Loading products... 加载中...</p>
            </div>
          )}

          {error && (
            <div className="error-state">
              <p>{error}</p>
              <button onClick={loadProducts} className="retry-btn">
                Retry 重试
              </button>
            </div>
          )}

          {!loading && !error && (
            <div className="products-grid">
              {products.map(product => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={addToCart}
                />
              ))}
            </div>
          )}
        </main>

        <aside className="cart-section">
          <ShoppingCart
            cartItems={cartItems}
            onRemoveFromCart={removeFromCart}
            totalPrice={totalPrice}
          />
        </aside>
      </div>
    </div>
  )
}

export default MainContent
