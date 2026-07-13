<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()

type Tab = 'atracoes' | 'compras' | 'gastronomia' | 'passeios'
const activeTab = ref<Tab>('atracoes')

const tabs = computed<{ key: Tab; label: string }[]>(() => [
  { key: 'atracoes', label: t('turismo.tabAttractions') },
  { key: 'compras', label: t('turismo.tabShopping') },
  { key: 'gastronomia', label: t('turismo.tabFood') },
  { key: 'passeios', label: t('turismo.tabTrips') },
])

const freeLabel = computed(() => t('turismo.free'))
const paidLabel = computed(() => t('turismo.paid'))

const atracoes = computed(() => {
  const data = {
    pt: [
      { nome: 'Bellagio Fountains', local: 'Bellagio Hotel', preco: 'Gratuito', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Fountains+of+Bellagio/@36.1126,-115.1767,17z' },
      { nome: 'The Sphere (exterior)', local: 'Venetian', preco: 'Gratuito', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Sphere/@36.1208,-115.1656,17z' },
      { nome: 'High Roller', local: 'The LINQ', preco: '$25–37', tipo: 'pago', maps: 'https://www.google.com/maps/place/High+Roller/@36.1173,-115.1685,17z' },
      { nome: 'Fremont Street Experience', local: 'Downtown', preco: 'Gratuito', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Fremont+Street+Experience/@36.1700,-115.1426,17z' },
      { nome: 'The Strat Tower', local: 'Norte da Strip', preco: '$25-35', tipo: 'pago', maps: 'https://www.google.com/maps/place/The+STRAT+Hotel/@36.1474,-115.1558,17z', descricao: 'Observatório de 350m com vista 360° de Las Vegas inteira. Brinquedos radicais no topo.' },
      { nome: 'Cirque du Soleil (O, KÀ, Beatles)', local: 'Vários hotéis', preco: '$80–200', tipo: 'pago' },
      { nome: 'Madame Tussauds', local: 'Venetian', preco: '$30–40', tipo: 'pago' },
      { nome: 'Shark Reef Aquarium', local: 'Mandalay Bay', preco: '$25–30', tipo: 'pago' },
      { nome: 'Welcome to Las Vegas Sign', local: 'South Strip', preco: 'Gratuito', tipo: 'gratuito' },
    ],
    en: [
      { nome: 'Bellagio Fountains', local: 'Bellagio Hotel', preco: 'Free', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Fountains+of+Bellagio/@36.1126,-115.1767,17z' },
      { nome: 'The Sphere (exterior)', local: 'Venetian', preco: 'Free', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Sphere/@36.1208,-115.1656,17z' },
      { nome: 'High Roller', local: 'The LINQ', preco: '$25–37', tipo: 'pago', maps: 'https://www.google.com/maps/place/High+Roller/@36.1173,-115.1685,17z' },
      { nome: 'Fremont Street Experience', local: 'Downtown', preco: 'Free', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Fremont+Street+Experience/@36.1700,-115.1426,17z' },
      { nome: 'The Strat Tower', local: 'North Strip', preco: '$25-35', tipo: 'pago', maps: 'https://www.google.com/maps/place/The+STRAT+Hotel/@36.1474,-115.1558,17z', descricao: 'Observatory at 350m with 360° views of all Las Vegas. Thrill rides on top.' },
      { nome: 'Cirque du Soleil (O, KÀ, Beatles)', local: 'Various hotels', preco: '$80–200', tipo: 'pago' },
      { nome: 'Madame Tussauds', local: 'Venetian', preco: '$30–40', tipo: 'pago' },
      { nome: 'Shark Reef Aquarium', local: 'Mandalay Bay', preco: '$25–30', tipo: 'pago' },
      { nome: 'Welcome to Las Vegas Sign', local: 'South Strip', preco: 'Free', tipo: 'gratuito' },
    ],
    es: [
      { nome: 'Bellagio Fountains', local: 'Bellagio Hotel', preco: 'Gratis', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Fountains+of+Bellagio/@36.1126,-115.1767,17z' },
      { nome: 'The Sphere (exterior)', local: 'Venetian', preco: 'Gratis', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Sphere/@36.1208,-115.1656,17z' },
      { nome: 'High Roller', local: 'The LINQ', preco: '$25–37', tipo: 'pago', maps: 'https://www.google.com/maps/place/High+Roller/@36.1173,-115.1685,17z' },
      { nome: 'Fremont Street Experience', local: 'Downtown', preco: 'Gratis', tipo: 'gratuito', maps: 'https://www.google.com/maps/place/Fremont+Street+Experience/@36.1700,-115.1426,17z' },
      { nome: 'The Strat Tower', local: 'Norte de la Strip', preco: '$25-35', tipo: 'pago', maps: 'https://www.google.com/maps/place/The+STRAT+Hotel/@36.1474,-115.1558,17z', descricao: 'Observatorio de 350m con vista 360° de todo Las Vegas. Juegos extremos en la cima.' },
      { nome: 'Cirque du Soleil (O, KÀ, Beatles)', local: 'Varios hoteles', preco: '$80–200', tipo: 'pago' },
      { nome: 'Madame Tussauds', local: 'Venetian', preco: '$30–40', tipo: 'pago' },
      { nome: 'Shark Reef Aquarium', local: 'Mandalay Bay', preco: '$25–30', tipo: 'pago' },
      { nome: 'Welcome to Las Vegas Sign', local: 'South Strip', preco: 'Gratis', tipo: 'gratuito' },
    ],
  }
  return data[locale.value] || data.en
})

const lojasEssenciais = computed(() => {
  const data = {
    pt: [
      { nome: 'Target Las Vegas Showcase', endereco: '3767 Las Vegas Blvd S, Las Vegas, NV 89109', distancia: '15 min a pé do Venetian (na Strip!)', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Target/@36.1040,-115.1724,17z', descricao: 'Loja de departamentos americana com eletrônicos, roupas, cosméticos e snacks. Fica NA Strip, fácil de ir a pé!' },
      { nome: 'Best Buy Maryland Parkway', endereco: '3820 S Maryland Pkwy, Las Vegas, NV 89119', distancia: '10 min de Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Best+Buy/@36.1080,-115.1350,17z', descricao: 'Maior loja de eletrônicos dos EUA. Notebooks, câmeras, fones, gadgets. Preços melhores que no Brasil.' },
      { nome: 'Walmart Supercenter (Tropicana)', endereco: '3615 S Rainbow Blvd, Las Vegas, NV 89103', distancia: '10 min de Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Walmart+Supercenter/@36.1012,-115.2080,17z', descricao: 'Hipermercado completo. Ótimo para comprar água, snacks, remédios e itens do dia a dia com preços baixos.' },
    ],
    en: [
      { nome: 'Target Las Vegas Showcase', endereco: '3767 Las Vegas Blvd S, Las Vegas, NV 89109', distancia: '15 min walk from Venetian (on the Strip!)', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Target/@36.1040,-115.1724,17z', descricao: 'American department store with electronics, clothes, cosmetics and snacks. Located ON the Strip, easy walk!' },
      { nome: 'Best Buy Maryland Parkway', endereco: '3820 S Maryland Pkwy, Las Vegas, NV 89119', distancia: '10 min Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Best+Buy/@36.1080,-115.1350,17z', descricao: 'Largest electronics store in the US. Laptops, cameras, headphones, gadgets. Better prices than abroad.' },
      { nome: 'Walmart Supercenter (Tropicana)', endereco: '3615 S Rainbow Blvd, Las Vegas, NV 89103', distancia: '10 min Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Walmart+Supercenter/@36.1012,-115.2080,17z', descricao: 'Complete hypermarket. Great for buying water, snacks, medicine and daily items at low prices.' },
    ],
    es: [
      { nome: 'Target Las Vegas Showcase', endereco: '3767 Las Vegas Blvd S, Las Vegas, NV 89109', distancia: '15 min a pie del Venetian (en la Strip!)', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Target/@36.1040,-115.1724,17z', descricao: 'Tienda departamental americana con electrónica, ropa, cosméticos y snacks. ¡Está EN la Strip, fácil caminar!' },
      { nome: 'Best Buy Maryland Parkway', endereco: '3820 S Maryland Pkwy, Las Vegas, NV 89119', distancia: '10 min de Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Best+Buy/@36.1080,-115.1350,17z', descricao: 'Mayor tienda de electrónica de EE.UU. Notebooks, cámaras, audífonos, gadgets. Mejores precios.' },
      { nome: 'Walmart Supercenter (Tropicana)', endereco: '3615 S Rainbow Blvd, Las Vegas, NV 89103', distancia: '10 min de Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Walmart+Supercenter/@36.1012,-115.2080,17z', descricao: 'Hipermercado completo. Ideal para comprar agua, snacks, medicinas y artículos diarios a bajo precio.' },
    ],
  }
  return data[locale.value] || data.en
})

const shoppings = computed(() => {
  const data = {
    pt: [
      { nome: 'Las Vegas North Premium Outlets', endereco: '875 S Grand Central Pkwy, Las Vegas, NV 89106', distancia: '15 min de Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Las+Vegas+North+Premium+Outlets/@36.1612,-115.1570,17z', descricao: '175+ lojas outlet com 25-65% desconto: Nike, Adidas, Coach, Calvin Klein, Tommy Hilfiger, Michael Kors.' },
      { nome: 'Grand Canal Shoppes (Venetian)', distancia: 'Dentro do Venetian!', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Grand+Canal+Shoppes/@36.1215,-115.1700,17z', descricao: 'Shopping de luxo DENTRO do Venetian. Burberry, Kate Spade, Michael Kors. Perfeito para intervalos do evento.' },
      { nome: 'Fashion Show Mall', distancia: '5 min a pé', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Fashion+Show+Las+Vegas/@36.1269,-115.1699,17z', descricao: 'Shopping tradicional em frente ao Wynn. Nordstrom, Macy\'s, Zara, H&M, Apple Store. 5 min do Venetian.' },
      { nome: 'Forum Shops at Caesars', distancia: '10 min a pé', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/The+Forum+Shops+at+Caesars+Palace/@36.1172,-115.1728,17z', descricao: 'Maior shopping de luxo da Strip com ambientação romana. Gucci, Louis Vuitton, Versace.' },
    ],
    en: [
      { nome: 'Las Vegas North Premium Outlets', endereco: '875 S Grand Central Pkwy, Las Vegas, NV 89106', distancia: '15 min Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Las+Vegas+North+Premium+Outlets/@36.1612,-115.1570,17z', descricao: '175+ outlet stores with 25-65% off: Nike, Adidas, Coach, Calvin Klein, Tommy Hilfiger, Michael Kors.' },
      { nome: 'Grand Canal Shoppes (Venetian)', distancia: 'Inside the Venetian!', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Grand+Canal+Shoppes/@36.1215,-115.1700,17z', descricao: 'Luxury mall INSIDE the Venetian. Burberry, Kate Spade, Michael Kors. Perfect for event breaks.' },
      { nome: 'Fashion Show Mall', distancia: '5 min walk', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Fashion+Show+Las+Vegas/@36.1269,-115.1699,17z', descricao: 'Traditional mall across from Wynn. Nordstrom, Macy\'s, Zara, H&M, Apple Store. 5 min from Venetian.' },
      { nome: 'Forum Shops at Caesars', distancia: '10 min walk', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/The+Forum+Shops+at+Caesars+Palace/@36.1172,-115.1728,17z', descricao: 'Largest luxury mall on the Strip with Roman-themed setting. Gucci, Louis Vuitton, Versace.' },
    ],
    es: [
      { nome: 'Las Vegas North Premium Outlets', endereco: '875 S Grand Central Pkwy, Las Vegas, NV 89106', distancia: '15 min de Uber', distanciaCor: 'bg-blue-100 text-blue-800', maps: 'https://www.google.com/maps/place/Las+Vegas+North+Premium+Outlets/@36.1612,-115.1570,17z', descricao: '175+ tiendas outlet con 25-65% descuento: Nike, Adidas, Coach, Calvin Klein, Tommy Hilfiger, Michael Kors.' },
      { nome: 'Grand Canal Shoppes (Venetian)', distancia: 'Dentro del Venetian!', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Grand+Canal+Shoppes/@36.1215,-115.1700,17z', descricao: 'Shopping de lujo DENTRO del Venetian. Burberry, Kate Spade, Michael Kors. Perfecto para descansos del evento.' },
      { nome: 'Fashion Show Mall', distancia: '5 min a pie', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/Fashion+Show+Las+Vegas/@36.1269,-115.1699,17z', descricao: 'Shopping tradicional frente al Wynn. Nordstrom, Macy\'s, Zara, H&M, Apple Store. 5 min del Venetian.' },
      { nome: 'Forum Shops at Caesars', distancia: '10 min a pie', distanciaCor: 'bg-green-100 text-green-800', maps: 'https://www.google.com/maps/place/The+Forum+Shops+at+Caesars+Palace/@36.1172,-115.1728,17z', descricao: 'El mayor shopping de lujo de la Strip con ambientación romana. Gucci, Louis Vuitton, Versace.' },
    ],
  }
  return data[locale.value] || data.en
})

const shoppingTip = computed(() => {
  const data = {
    pt: 'Faça compras ANTES ou DEPOIS do evento (Black Friday é perto!). Durante o re:Invent não dá tempo — dinâmica é das 8h às 22h. Vá de Uber XL rachado até Target/Best Buy, compre tudo de uma vez.',
    en: 'Shop BEFORE or AFTER the event (Black Friday is close!). During re:Invent there is no time — it runs 8am-10pm. Take a shared Uber XL to Target/Best Buy, buy everything at once.',
    es: 'Haz compras ANTES o DESPUÉS del evento (¡Black Friday está cerca!). Durante el re:Invent no hay tiempo — va de 8am a 10pm. Ve en Uber XL compartido a Target/Best Buy, compra todo de una vez.',
  }
  return data[locale.value] || data.en
})

const essentialStoresTitle = computed(() => {
  const data = { pt: '🏪 Lojas Essenciais', en: '🏪 Essential Stores', es: '🏪 Tiendas Esenciales' }
  return data[locale.value] || data.en
})

const shoppingsTitle = computed(() => {
  const data = { pt: '🛍️ Shoppings', en: '🛍️ Shopping Malls', es: '🛍️ Centros Comerciales' }
  return data[locale.value] || data.en
})

const jantaresEspeciais = computed(() => {
  const data = {
    pt: [
      { nome: 'Hell\'s Kitchen', local: 'Caesars Palace', preco: '$60–120', tipo: 'Gordon Ramsay' },
      { nome: 'Nobu', local: 'Caesars Palace', preco: '$80–150', tipo: 'Japonês premium' },
      { nome: 'SW Steakhouse', local: 'Wynn', preco: '$80–150', tipo: 'Steakhouse' },
      { nome: 'Bacchanal Buffet', local: 'Caesars Palace', preco: '$70–90', tipo: 'Buffet premium' },
      { nome: 'Joël Robuchon', local: 'MGM Grand', preco: '$100–200', tipo: 'Francês (3 Michelin)' },
    ],
    en: [
      { nome: 'Hell\'s Kitchen', local: 'Caesars Palace', preco: '$60–120', tipo: 'Gordon Ramsay' },
      { nome: 'Nobu', local: 'Caesars Palace', preco: '$80–150', tipo: 'Premium Japanese' },
      { nome: 'SW Steakhouse', local: 'Wynn', preco: '$80–150', tipo: 'Steakhouse' },
      { nome: 'Bacchanal Buffet', local: 'Caesars Palace', preco: '$70–90', tipo: 'Premium Buffet' },
      { nome: 'Joël Robuchon', local: 'MGM Grand', preco: '$100–200', tipo: 'French (3 Michelin)' },
    ],
    es: [
      { nome: 'Hell\'s Kitchen', local: 'Caesars Palace', preco: '$60–120', tipo: 'Gordon Ramsay' },
      { nome: 'Nobu', local: 'Caesars Palace', preco: '$80–150', tipo: 'Japonés premium' },
      { nome: 'SW Steakhouse', local: 'Wynn', preco: '$80–150', tipo: 'Steakhouse' },
      { nome: 'Bacchanal Buffet', local: 'Caesars Palace', preco: '$70–90', tipo: 'Buffet premium' },
      { nome: 'Joël Robuchon', local: 'MGM Grand', preco: '$100–200', tipo: 'Francés (3 Michelin)' },
    ],
  }
  return data[locale.value] || data.en
})

const opcoesAcessiveis = computed(() => {
  const data = {
    pt: [
      { nome: 'In-N-Out Burger', local: 'Strip (LINQ)', preco: '$8–12', tipo: 'Fast food icônico' },
      { nome: 'Secret Pizza', local: 'Cosmopolitan (3º andar)', preco: '$5–8/fatia', tipo: 'Pizza escondida' },
      { nome: 'Tacos El Gordo', local: 'Strip', preco: '$3–8/taco', tipo: 'Mexicano autêntico' },
      { nome: 'Earl of Sandwich', local: 'Planet Hollywood', preco: '$8–12', tipo: 'Sanduíches' },
      { nome: 'Food Courts (hotéis)', local: 'Venetian, MGM, Luxor', preco: '$12–20', tipo: 'Variedade rápida' },
    ],
    en: [
      { nome: 'In-N-Out Burger', local: 'Strip (LINQ)', preco: '$8–12', tipo: 'Iconic fast food' },
      { nome: 'Secret Pizza', local: 'Cosmopolitan (3rd floor)', preco: '$5–8/slice', tipo: 'Hidden pizza spot' },
      { nome: 'Tacos El Gordo', local: 'Strip', preco: '$3–8/taco', tipo: 'Authentic Mexican' },
      { nome: 'Earl of Sandwich', local: 'Planet Hollywood', preco: '$8–12', tipo: 'Sandwiches' },
      { nome: 'Food Courts (hotels)', local: 'Venetian, MGM, Luxor', preco: '$12–20', tipo: 'Quick variety' },
    ],
    es: [
      { nome: 'In-N-Out Burger', local: 'Strip (LINQ)', preco: '$8–12', tipo: 'Fast food icónico' },
      { nome: 'Secret Pizza', local: 'Cosmopolitan (3er piso)', preco: '$5–8/porción', tipo: 'Pizza escondida' },
      { nome: 'Tacos El Gordo', local: 'Strip', preco: '$3–8/taco', tipo: 'Mexicano auténtico' },
      { nome: 'Earl of Sandwich', local: 'Planet Hollywood', preco: '$8–12', tipo: 'Sándwiches' },
      { nome: 'Food Courts (hoteles)', local: 'Venetian, MGM, Luxor', preco: '$12–20', tipo: 'Variedad rápida' },
    ],
  }
  return data[locale.value] || data.en
})

const foodSpecialTitle = computed(() => {
  const data = { pt: '🍽️ Jantares Especiais ($50–150)', en: '🍽️ Special Dinners ($50–150)', es: '🍽️ Cenas Especiales ($50–150)' }
  return data[locale.value] || data.en
})

const foodAffordableTitle = computed(() => {
  const data = { pt: '🌮 Opções Acessíveis ($15–40)', en: '🌮 Affordable Options ($15–40)', es: '🌮 Opciones Accesibles ($15–40)' }
  return data[locale.value] || data.en
})

const foodTableHeaders = computed(() => {
  const data = {
    pt: { restaurant: 'Restaurante', location: 'Local', price: 'Preço', type: 'Tipo' },
    en: { restaurant: 'Restaurant', location: 'Location', price: 'Price', type: 'Type' },
    es: { restaurant: 'Restaurante', location: 'Ubicación', price: 'Precio', type: 'Tipo' },
  }
  return data[locale.value] || data.en
})

const passeios = computed(() => {
  const data = {
    pt: [
      { nome: 'Grand Canyon (West Rim)', distancia: '2h de carro', custo: '$30–300', descricao: 'Skywalk de vidro, vistas épicas. Helicóptero opcional ($200-300).', maps: 'https://www.google.com/maps/place/Grand+Canyon+National+Park/@36.1069,-112.1129,11z' },
      { nome: 'Red Rock Canyon', distancia: '30 min', custo: '$15 (carro)', descricao: 'Scenic drive de 20km no deserto. Trilhas fáceis com vistas incríveis.', maps: 'https://www.google.com/maps/place/Red+Rock+Canyon/@36.1353,-115.4294,13z' },
      { nome: 'Hoover Dam', distancia: '45 min', custo: '$10–30', descricao: 'Represa histórica. Tour guiado dentro da barragem disponível.', maps: 'https://www.google.com/maps/place/Hoover+Dam/@36.0160,-114.7377,15z' },
      { nome: 'Fremont Street (Downtown)', distancia: '15 min', custo: 'Gratuito', descricao: 'Teto de LED de 460m, shows de luzes, zip line, vibe retrô de Vegas.', maps: 'https://www.google.com/maps/place/Fremont+Street+Experience/@36.1700,-115.1426,17z' },
    ],
    en: [
      { nome: 'Grand Canyon (West Rim)', distancia: '2h drive', custo: '$30–300', descricao: 'Glass skywalk, epic views. Optional helicopter ($200-300).', maps: 'https://www.google.com/maps/place/Grand+Canyon+National+Park/@36.1069,-112.1129,11z' },
      { nome: 'Red Rock Canyon', distancia: '30 min', custo: '$15 (car)', descricao: '20km scenic drive in the desert. Easy trails with incredible views.', maps: 'https://www.google.com/maps/place/Red+Rock+Canyon/@36.1353,-115.4294,13z' },
      { nome: 'Hoover Dam', distancia: '45 min', custo: '$10–30', descricao: 'Historic dam. Guided tour inside the dam available.', maps: 'https://www.google.com/maps/place/Hoover+Dam/@36.0160,-114.7377,15z' },
      { nome: 'Fremont Street (Downtown)', distancia: '15 min', custo: 'Free', descricao: '460m LED canopy, light shows, zip line, retro Vegas vibe.', maps: 'https://www.google.com/maps/place/Fremont+Street+Experience/@36.1700,-115.1426,17z' },
    ],
    es: [
      { nome: 'Grand Canyon (West Rim)', distancia: '2h en auto', custo: '$30–300', descricao: 'Skywalk de vidrio, vistas épicas. Helicóptero opcional ($200-300).', maps: 'https://www.google.com/maps/place/Grand+Canyon+National+Park/@36.1069,-112.1129,11z' },
      { nome: 'Red Rock Canyon', distancia: '30 min', custo: '$15 (auto)', descricao: 'Scenic drive de 20km en el desierto. Senderos fáciles con vistas increíbles.', maps: 'https://www.google.com/maps/place/Red+Rock+Canyon/@36.1353,-115.4294,13z' },
      { nome: 'Hoover Dam', distancia: '45 min', custo: '$10–30', descricao: 'Represa histórica. Tour guiado dentro de la represa disponible.', maps: 'https://www.google.com/maps/place/Hoover+Dam/@36.0160,-114.7377,15z' },
      { nome: 'Fremont Street (Downtown)', distancia: '15 min', custo: 'Gratis', descricao: 'Techo LED de 460m, shows de luces, zip line, vibra retro de Vegas.', maps: 'https://www.google.com/maps/place/Fremont+Street+Experience/@36.1700,-115.1426,17z' },
    ],
  }
  return data[locale.value] || data.en
})

const financialTips = computed(() => {
  const data = {
    pt: [
      { label: 'Sales Tax Nevada:', text: '8,375% adicionado em todas as compras (não aparece na etiqueta)' },
      { label: 'Câmbio:', text: 'Use cartão de crédito internacional — melhor taxa que casas de câmbio. Leve $100-200 em espécie para emergências' },
      { label: 'IOF:', text: '4,38% no cartão de crédito internacional / 1,1% em compra de moeda. Cartões como Wise e C6 Global têm IOF menor' },
      { label: 'Gorjetas:', text: 'Restaurantes 18-20%, bares $1-2/drink, Uber/táxi 15%, hotel (valet $2-5, housekeeping $2-5/dia)' },
      { label: 'Dica:', text: 'Outlets (Premium Outlets North/South) oferecem 25-65% off em marcas americanas — melhor custo-benefício para compras' },
    ],
    en: [
      { label: 'Nevada Sales Tax:', text: '8.375% added to all purchases (not shown on price tags)' },
      { label: 'Currency:', text: 'Use an international credit card — better rate than exchange offices. Bring $100-200 cash for emergencies' },
      { label: 'IOF (Brazil tax):', text: '4.38% on international credit card / 1.1% on currency purchase. Cards like Wise and C6 Global have lower IOF' },
      { label: 'Tipping:', text: 'Restaurants 18-20%, bars $1-2/drink, Uber/taxi 15%, hotel (valet $2-5, housekeeping $2-5/day)' },
      { label: 'Tip:', text: 'Outlets (Premium Outlets North/South) offer 25-65% off on American brands — best value for shopping' },
    ],
    es: [
      { label: 'Sales Tax Nevada:', text: '8,375% agregado a todas las compras (no aparece en la etiqueta)' },
      { label: 'Cambio:', text: 'Usa tarjeta de crédito internacional — mejor tasa que casas de cambio. Lleva $100-200 en efectivo para emergencias' },
      { label: 'IOF:', text: '4,38% en tarjeta de crédito internacional / 1,1% en compra de moneda. Tarjetas como Wise y C6 Global tienen IOF menor' },
      { label: 'Propinas:', text: 'Restaurantes 18-20%, bares $1-2/trago, Uber/taxi 15%, hotel (valet $2-5, housekeeping $2-5/día)' },
      { label: 'Tip:', text: 'Outlets (Premium Outlets North/South) ofrecen 25-65% off en marcas americanas — mejor costo-beneficio para compras' },
    ],
  }
  return data[locale.value] || data.en
})
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">🎰 {{ t('turismo.title') }}</h1>

    <!-- Tabs -->
    <div class="flex flex-wrap gap-1 mb-6 border-b border-gray-200 pb-2">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="[
          'px-4 py-2 rounded-t-lg text-sm font-medium transition-colors',
          activeTab === tab.key
            ? 'bg-aws-orange text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
        ]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab: Atrações -->
    <div v-if="activeTab === 'atracoes'" class="mb-10">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div
          v-for="a in atracoes"
          :key="a.nome"
          class="bg-white border border-gray-200 rounded-xl p-4"
        >
          <div class="flex justify-between items-start">
            <h3 class="font-bold text-aws-dark text-sm">{{ a.nome }}</h3>
            <span
              :class="[
                a.tipo === 'gratuito' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800',
                'text-xs px-2 py-0.5 rounded-full font-medium',
              ]"
            >
              {{ a.tipo === 'gratuito' ? freeLabel : a.preco }}
            </span>
          </div>
          <p class="text-xs text-gray-500 mt-1">📍 {{ a.local }}</p>
          <p v-if="a.descricao" class="text-xs text-gray-600 mt-1">{{ a.descricao }}</p>
          <a
            v-if="a.maps"
            :href="a.maps"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-block mt-2 text-xs text-aws-orange hover:text-aws-orange-hover font-medium"
          >
            📍 Google Maps →
          </a>
        </div>
      </div>
    </div>

    <!-- Tab: Compras -->
    <div v-if="activeTab === 'compras'" class="mb-10">
      <!-- Dica da Comunidade -->
      <div class="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-6">
        <p class="text-sm text-amber-900 font-medium">
          🛍️ {{ shoppingTip }}
        </p>
      </div>

      <!-- Lojas Essenciais -->
      <h3 class="font-bold text-aws-dark text-lg mb-4">{{ essentialStoresTitle }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <div
          v-for="loja in lojasEssenciais"
          :key="loja.nome"
          class="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-2">
            <h4 class="font-bold text-aws-dark text-sm">{{ loja.nome }}</h4>
            <span :class="[loja.distanciaCor, 'text-xs px-2 py-0.5 rounded-full font-medium whitespace-nowrap ml-2']">
              {{ loja.distancia }}
            </span>
          </div>
          <p v-if="loja.endereco" class="text-xs text-gray-400 mb-2">{{ loja.endereco }}</p>
          <p class="text-sm text-gray-600 mb-3">{{ loja.descricao }}</p>
          <a
            :href="loja.maps"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-block text-xs text-aws-orange hover:text-aws-orange-hover font-medium"
          >
            📍 Google Maps →
          </a>
        </div>
      </div>

      <!-- Shoppings -->
      <h3 class="font-bold text-aws-dark text-lg mb-4">{{ shoppingsTitle }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="s in shoppings"
          :key="s.nome"
          class="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-2">
            <h4 class="font-bold text-aws-dark text-sm">{{ s.nome }}</h4>
            <span :class="[s.distanciaCor, 'text-xs px-2 py-0.5 rounded-full font-medium whitespace-nowrap ml-2']">
              {{ s.distancia }}
            </span>
          </div>
          <p v-if="s.endereco" class="text-xs text-gray-400 mb-2">{{ s.endereco }}</p>
          <p class="text-sm text-gray-600 mb-3">{{ s.descricao }}</p>
          <a
            :href="s.maps"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-block text-xs text-aws-orange hover:text-aws-orange-hover font-medium"
          >
            📍 Google Maps →
          </a>
        </div>
      </div>
    </div>

    <!-- Tab: Gastronomia -->
    <div v-if="activeTab === 'gastronomia'" class="mb-10">
      <!-- Jantares Especiais -->
      <h3 class="font-bold text-aws-dark mb-3">{{ foodSpecialTitle }}</h3>
      <div class="overflow-x-auto mb-6">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.restaurant }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.location }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.price }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.type }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(r, i) in jantaresEspeciais"
              :key="r.nome"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium">{{ r.nome }}</td>
              <td class="px-3 py-2 text-gray-500">{{ r.local }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ r.preco }}</td>
              <td class="px-3 py-2 text-xs text-gray-600">{{ r.tipo }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Opções Acessíveis -->
      <h3 class="font-bold text-aws-dark mb-3">{{ foodAffordableTitle }}</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.restaurant }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.location }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.price }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.type }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(r, i) in opcoesAcessiveis"
              :key="r.nome"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium">{{ r.nome }}</td>
              <td class="px-3 py-2 text-gray-500">{{ r.local }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ r.preco }}</td>
              <td class="px-3 py-2 text-xs text-gray-600">{{ r.tipo }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab: Passeios -->
    <div v-if="activeTab === 'passeios'" class="mb-10">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="p in passeios"
          :key="p.nome"
          class="bg-white border border-gray-200 rounded-xl p-5"
        >
          <h3 class="font-bold text-aws-dark">{{ p.nome }}</h3>
          <div class="flex gap-3 mt-2 text-xs">
            <span class="bg-aws-light text-gray-600 px-2 py-0.5 rounded-full">📍 {{ p.distancia }}</span>
            <span class="bg-aws-orange/10 text-aws-orange-hover px-2 py-0.5 rounded-full">💰 {{ p.custo }}</span>
          </div>
          <p class="text-sm text-gray-600 mt-3">{{ p.descricao }}</p>
          <a
            v-if="p.maps"
            :href="p.maps"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-block mt-2 text-xs text-aws-orange hover:text-aws-orange-hover font-medium"
          >
            📍 Google Maps →
          </a>
        </div>
      </div>
    </div>

    <!-- Dicas Financeiras -->
    <section class="mt-10 mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">💸 {{ t('turismo.financialTips') }}</h2>
      <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-3 text-sm text-gray-700">
        <div
          v-for="(tip, i) in financialTips"
          :key="i"
          class="flex items-start gap-2"
        >
          <span class="text-aws-orange font-bold">•</span>
          <span><strong>{{ tip.label }}</strong> {{ tip.text }}</span>
        </div>
      </div>
    </section>
  </div>
</template>
