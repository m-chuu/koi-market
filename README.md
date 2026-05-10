# Koi Fish Store 锦鲤商店

A bilingual (English + Chinese) koi fish retail storefront built with React and Vite. Customers browse fish categories with photos and prices, add items to a cart, and pay via QR code popup.

---

## Features

- Fish catalogue — 7 koi varieties in a 3-column grid with photos, bilingual names, size range, and RM pricing
- Shopping cart sidebar — add / remove items, running total, persistent during the session
- Payment modal — clicking Checkout shows a QR code payment popup centred on screen
- Glassmorphism UI — animated gold shimmer header, koi background photo, backdrop-blur cards

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | React 18 (functional components + hooks) |
| Build tool | Vite |
| Styling | Plain CSS (no framework) |
| Data source | Local JS array (falls back from optional FastAPI backend) |
| Fonts | Google Fonts — Playfair Display + Lato |

---

## Project Structure

```
koi-market/
├── public/
└── src/
    ├── assets/
    │   └── images/
    │       ├── background.jpeg      # Full-page background photo
    │       ├── payment.jpg          # QR code shown in payment modal
    │       ├── kohaku.jpg
    │       ├── benigoi.jpg
    │       ├── ginrin-benigoi.jpg
    │       ├── yamabuki-ogon.jpg
    │       ├── hi-utsuri.jpg
    │       ├── kujaku.jpg
    │       └── mix-koi.jpg
    │
    ├── components/
    │   ├── common/
    │   │   ├── ProductCard.jsx      # Single fish card (image, name, price, button)
    │   │   ├── ProductCard.css
    │   │   ├── ShoppingCart.jsx     # Cart sidebar + payment modal
    │   │   └── ShoppingCart.css
    │   └── layout/
    │       ├── MainContent.jsx      # Root layout, state management
    │       └── MainContent.css
    │
    ├── data/
    │   └── products.js             # Local product array (offline fallback)
    │
    ├── services/
    │   └── api.js                  # Optional FastAPI backend client
    │
    ├── App.jsx                     # Entry component
    ├── App.css
    ├── index.css                   # Global resets + Google Fonts import
    └── main.jsx                    # ReactDOM render
```

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────┐
│                      HEADER (full width)                     │
│    Koi Fish Store 锦鲤商店  |  PREMIUM JAPANESE KOI · ...    │
├──────────────────────────────────────────┬───────────────────┤
│                                          │                   │
│   PRODUCTS SECTION (scrollable)          │   CART SIDEBAR    │
│                                          │                   │
│   ┌────────┐  ┌────────┐  ┌────────┐    │  [payment.jpg]    │
│   │  fish  │  │  fish  │  │  fish  │    │  购物车 banner     │
│   │ photo  │  │ photo  │  │ photo  │    │                   │
│   │ name   │  │ name   │  │ name   │    │  • Item   RM xxx  │
│   │ price  │  │ price  │  │ price  │    │  • Item   RM xxx  │
│   │[+cart] │  │[+cart] │  │[+cart] │    │                   │
│   └────────┘  └────────┘  └────────┘    │  Total:  RM xxx   │
│   ┌────────┐  ┌────────┐  ┌────────┐    │ [CHECKOUT 结账]   │
│   │  ...   │  │  ...   │  │  ...   │    │                   │
│   └────────┘  └────────┘  └────────┘    │                   │
│                                          │                   │
└──────────────────────────────────────────┴───────────────────┘

                On CHECKOUT click:
┌─────────────────────────────────────────────────────────────┐
│                  (blurred overlay)                          │
│            ┌───────────────────────────┐                   │
│            │   Scan to Pay 扫码付款    │                   │
│            │   ┌───────────────────┐   │                   │
│            │   │   [payment.jpg]   │   │                   │
│            │   │    (QR code)      │   │                   │
│            │   └───────────────────┘   │                   │
│            │   Total 总计: RM xxx      │                   │
│            └───────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture

### State Management

All state lives in `MainContent.jsx`:

```
cartItems          []     ← array of product objects currently in cart
addToCart()              ← appends product to cartItems
removeFromCart()         ← removes first occurrence by product ID
totalPrice               ← computed via reduce() on price.min
```

### Data Flow

```
products.js  (local fallback)
      │
      ▼
MainContent.jsx ──── fetchProducts() ──── api.js ──── FastAPI backend (optional)
      │
      ├──▶ ProductCard    receives: product, onAddToCart
      │
      └──▶ ShoppingCart   receives: cartItems, onRemoveFromCart, totalPrice
                │
                └──▶ Payment Modal   shown on Checkout click (useState)
```

### Payment Flow

1. User adds fish via **Add to Cart 加入购物车**
2. Cart sidebar shows items and running RM total
3. User clicks **Checkout 结账**
4. Modal overlays the full page — shows `payment.jpg` (QR code)
5. User scans QR to complete payment; closes modal via ✕ or clicking outside

---

## Product Data Structure

Defined in `src/data/products.js`:

```js
{
  id:        number,
  nameEn:    string,    // e.g. "Kohaku"
  nameCn:    string,    // e.g. "红白"
  sizeRange: string,    // e.g. "15-18cm"
  price: {
    min: number,        // RM — used for cart total calculation
    max: number         // RM — equal to min for fixed price
  },
  image:     string,    // Vite-processed asset path
  currency:  "RM"
}
```

Price display rule: `min === max` → `RM 380` | `min !== max` → `RM 380 - RM 480`

---

## Koi Catalogue

| # | English Name | Chinese | Size | Price (RM) |
|---|---|---|---|---|
| 1 | Kohaku | 红白 | 15–18 cm | 380–480 |
| 2 | Benigoi | 红鲤 | 15–18 cm | 380 |
| 3 | Ginrin Benigoi | 银鳞红鲤 | 15–17 cm | 380 |
| 4 | Yamabuki Ogon | 黄金 | 16–18 cm | 380 |
| 5 | Hi-utsuri | 绯写 | 15–17 cm | 380 |
| 6 | Kujaku | 孔雀 | 15–17 cm | 380 |
| 7 | Mix Koi | 混合锦鲤 | 15–17 cm | 280 |

---

## Commands

```bash
npm install       # install dependencies
npm run dev       # dev server → http://localhost:5173
npm run build     # production build → dist/
npm run preview   # preview production build
```

---

## Adding a New Fish

1. Drop the photo into `src/assets/images/`
2. Import it at the top of `src/data/products.js`
3. Add a new product object to the `products` array
