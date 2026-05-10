import { useState } from 'react'
import paymentImg from '../../assets/images/payment.jpg'
import './ShoppingCart.css'

function ShoppingCart({ cartItems, onRemoveFromCart, totalPrice }) {
  const [showPayment, setShowPayment] = useState(false)

  return (
    <>
      <div className="shopping-cart">
        <div className="cart-payment-banner">
          <img src={paymentImg} alt="Payment" className="payment-img" />
          <div className="cart-banner-overlay">
            <div className="cart-banner-title">
              <span>Shopping Cart</span>
              购物车
            </div>
          </div>
        </div>

        {cartItems.length === 0 ? (
          <p className="cart-empty">Your cart is empty<em>购物车是空的</em></p>
        ) : (
          <>
            <ul className="cart-items">
              {cartItems.map((item, index) => (
                <li key={`${item.id}-${index}`} className="cart-item">
                  <div className="cart-item-info">
                    <span className="cart-item-name">
                      {item.nameEn} <span className="cart-item-cn">{item.nameCn}</span>
                    </span>
                    <span className="cart-item-price">
                      {item.currency} {item.price.min}
                    </span>
                  </div>
                  <button
                    className="remove-btn"
                    onClick={() => onRemoveFromCart(item.id)}
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>

            <div className="cart-total">
              <span>Total 总计:</span>
              <span className="total-price">RM {totalPrice}</span>
            </div>
            <button className="checkout-btn" onClick={() => setShowPayment(true)}>
              Checkout 结账
            </button>
          </>
        )}
      </div>

      {showPayment && (
        <div className="payment-modal-overlay" onClick={() => setShowPayment(false)}>
          <div className="payment-modal" onClick={e => e.stopPropagation()}>
            <button className="payment-modal-close" onClick={() => setShowPayment(false)}>✕</button>
            <p className="payment-modal-label">Scan to Pay 扫码付款</p>
            <img src={paymentImg} alt="Payment QR" className="payment-modal-img" />
            <p className="payment-modal-total">Total 总计: <strong>RM {totalPrice}</strong></p>
          </div>
        </div>
      )}
    </>
  )
}

export default ShoppingCart
