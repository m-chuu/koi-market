import './ProductCard.css'

function ProductCard({ product, onAddToCart }) {
  const { nameEn, nameCn, sizeRange, price, image, currency } = product

  // Format price display
  const formatPrice = () => {
    if (price.min === price.max) {
      return `${currency} ${price.min}`
    }
    return `${currency} ${price.min} - ${currency} ${price.max}`
  }

  return (
    <div className="product-card">
      <div className="product-image">
        <img src={image} alt={`${nameEn} ${nameCn}`} />
      </div>
      <div className="product-info">
        <h3 className="product-name">
          {nameEn} <span className="name-cn">{nameCn}</span>
        </h3>
        <p className="product-size">Size 尺寸: {sizeRange}</p>
        <p className="product-price">{formatPrice()}</p>
        <button 
          className="add-to-cart-btn"
          onClick={() => onAddToCart(product)}
        >
          Add to Cart 加入购物车
        </button>
      </div>
    </div>
  )
}

export default ProductCard
