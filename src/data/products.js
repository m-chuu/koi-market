// Koi Fish Product Data
// Images should be placed in src/assets/images/

import kohakuImg from '../assets/images/kohaku.jpg'
import benigoiImg from '../assets/images/benigoi.jpg'
import ginrinBenigoiImg from '../assets/images/ginrin-benigoi.jpg'
import yamabukiOgonImg from '../assets/images/yamabuki-ogon.jpg'
import hiUtsuriImg from '../assets/images/hi-utsuri.jpg'
import kujakuImg from '../assets/images/kujaku.jpg'
import mixKoiImg from '../assets/images/mix-koi.jpg'

const products = [
  {
    id: 1,
    nameEn: "Kohaku",
    nameCn: "红白",
    sizeRange: "15-18cm",
    price: {
      min: 380,
      max: 480
    },
    image: kohakuImg,
    currency: "RM"
  },
  {
    id: 2,
    nameEn: "Benigoi",
    nameCn: "红鲤",
    sizeRange: "15-18cm",
    price: {
      min: 380,
      max: 380
    },
    image: benigoiImg,
    currency: "RM"
  },
  {
    id: 3,
    nameEn: "Ginrin Benigoi",
    nameCn: "银鳞红鲤",
    sizeRange: "15-17cm",
    price: {
      min: 380,
      max: 380
    },
    image: ginrinBenigoiImg,
    currency: "RM"
  },
  {
    id: 4,
    nameEn: "Yamabuki Ogon",
    nameCn: "黄金",
    sizeRange: "16-18cm",
    price: {
      min: 380,
      max: 380
    },
    image: yamabukiOgonImg,
    currency: "RM"
  },
  {
    id: 5,
    nameEn: "Hi-utsuri",
    nameCn: "绯写",
    sizeRange: "15-17cm",
    price: {
      min: 380,
      max: 380
    },
    image: hiUtsuriImg,
    currency: "RM"
  },
  {
    id: 6,
    nameEn: "Kujaku",
    nameCn: "孔雀",
    sizeRange: "15-17cm",
    price: {
      min: 380,
      max: 380
    },
    image: kujakuImg,
    currency: "RM"
  },
  {
    id: 7,
    nameEn: "Mix Koi",
    nameCn: "混合锦鲤",
    sizeRange: "15-17cm",
    price: {
      min: 280,
      max: 280
    },
    image: mixKoiImg,
    currency: "RM"
  }
]

export default products
