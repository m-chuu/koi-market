/**
 * API Client for Koi Market Backend
 */

// Import images so Vite can process them
import kohakuImg from '../assets/images/kohaku.jpg'
import benigoiImg from '../assets/images/benigoi.jpg'
import ginrinBenigoiImg from '../assets/images/ginrin-benigoi.jpg'
import yamabukiOgonImg from '../assets/images/yamabuki-ogon.jpg'
import hiUtsuriImg from '../assets/images/hi-utsuri.jpg'
import kujakuImg from '../assets/images/kujaku.jpg'
import mixKoiImg from '../assets/images/mix-koi.jpg'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Map API image paths to imported assets
const imageMap = {
  '/images/kohaku.jpg': kohakuImg,
  '/images/benigoi.jpg': benigoiImg,
  '/images/ginrin-benigoi.jpg': ginrinBenigoiImg,
  '/images/yamabuki-ogon.jpg': yamabukiOgonImg,
  '/images/hi-utsuri.jpg': hiUtsuriImg,
  '/images/kujaku.jpg': kujakuImg,
  '/images/mix-koi.jpg': mixKoiImg,
}

/**
 * Fetch all products from the API
 * @param {Object} options - Query options
 * @param {number} options.page - Page number (default: 1)
 * @param {number} options.pageSize - Items per page (default: 50)
 * @param {string} options.search - Search term for filtering
 * @returns {Promise<{products: Array, total: number, page: number, pageSize: number}>}
 */
export async function fetchProducts({ page = 1, pageSize = 50, search = '' } = {}) {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  })

  if (search) {
    params.append('search', search)
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/products?${params}`)

  if (!response.ok) {
    throw new Error(`Failed to fetch products: ${response.statusText}`)
  }

  const data = await response.json()

  // Transform API response to match frontend expectations
  return {
    products: data.products.map(transformProduct),
    total: data.total,
    page: data.page,
    pageSize: data.page_size,
  }
}

/**
 * Fetch a single product by ID
 * @param {number} id - Product ID
 * @returns {Promise<Object>}
 */
export async function fetchProduct(id) {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/${id}`)

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Product not found')
    }
    throw new Error(`Failed to fetch product: ${response.statusText}`)
  }

  const data = await response.json()
  return transformProduct(data)
}

/**
 * Transform API product data to frontend format
 * Converts string prices to numbers and handles image paths
 */
function transformProduct(apiProduct) {
  return {
    id: apiProduct.id,
    nameEn: apiProduct.nameEn,
    nameCn: apiProduct.nameCn,
    sizeRange: apiProduct.sizeRange,
    price: {
      min: parseFloat(apiProduct.price.min),
      max: parseFloat(apiProduct.price.max),
    },
    // Map API image path to imported asset
    image: imageMap[apiProduct.image] || apiProduct.image,
    currency: apiProduct.currency,
  }
}

export default {
  fetchProducts,
  fetchProduct,
}
