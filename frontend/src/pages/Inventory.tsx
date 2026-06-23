import { useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import api from '../services/api'
import InventoryAdjustmentForm from '../components/InventoryAdjustmentForm'
import InventoryEntryForm from '../components/InventoryEntryForm'
import InventoryExitForm from '../components/InventoryExitForm'
import InventoryMovements from '../components/InventoryMovements'
import Modal from '../components/Modal'
import ProductForm from '../components/ProductForm'
import type { ApiResponse, Color, InventoryItem, Product } from '../types/api'

async function fetchInventory() {
  const response = await api.get<ApiResponse<InventoryItem[]>>('/inventory')
  return response.data.data
}

async function fetchProducts() {
  const response = await api.get<ApiResponse<Product[]>>('/products')
  return response.data.data
}

async function fetchColors() {
  const response = await api.get<ApiResponse<Color[]>>('/catalogs/colors')
  return response.data.data
}

function locationLabel(locationType: InventoryItem['location_type']) {
  return locationType === 'WAREHOUSE' ? 'Bodega' : 'Tienda'
}

function money(value: number | null | undefined) {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(value ?? 0)
}

export default function Inventory() {
  const queryClient = useQueryClient()
  const inventoryQuery = useQuery(['inventory'], fetchInventory)
  const productsQuery = useQuery(['products'], fetchProducts, { initialData: [] })
  const colorsQuery = useQuery(['colors'], fetchColors, { initialData: [] })
  const [openProductModal, setOpenProductModal] = useState(false)
  const [openEntryModal, setOpenEntryModal] = useState(false)
  const [openExitModal, setOpenExitModal] = useState(false)
  const [openAdjustmentModal, setOpenAdjustmentModal] = useState(false)
  const [openMovementsModal, setOpenMovementsModal] = useState(false)
  const [selectedItem, setSelectedItem] = useState<InventoryItem | null>(null)

  function refresh() {
    queryClient.invalidateQueries(['inventory'])
    queryClient.invalidateQueries(['products'])
    if (selectedItem) {
      queryClient.invalidateQueries(['inventory-movements', selectedItem.id])
    }
    setOpenProductModal(false)
    setOpenEntryModal(false)
    setOpenExitModal(false)
    setOpenAdjustmentModal(false)
    setSelectedItem(null)
  }

  const inventory = inventoryQuery.data ?? []
  const products = productsQuery.data ?? []
  const colors = colorsQuery.data ?? []
  const totalUnits = inventory.reduce((sum, item) => sum + item.quantity, 0)
  const lowStockCount = inventory.filter((item) => item.is_low_stock).length
  const warehouseUnits = inventory
    .filter((item) => item.location_type === 'WAREHOUSE')
    .reduce((sum, item) => sum + item.quantity, 0)
  const storeUnits = inventory
    .filter((item) => item.location_type === 'STORE')
    .reduce((sum, item) => sum + item.quantity, 0)

  if (inventoryQuery.isLoading) {
    return <div className="p-6 text-slate-500">Cargando inventario...</div>
  }

  if (inventoryQuery.error) {
    return <div className="p-6 text-red-600">Error al cargar inventario.</div>
  }

  return (
    <div className="space-y-6 p-2 sm:p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-emerald-600">Inventario</p>
          <h1 className="text-3xl font-extrabold text-slate-950">Control de calzado</h1>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => setOpenEntryModal(true)}
            disabled={products.length === 0}
            className="rounded bg-green-600 px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Registrar entrada
          </button>
          <button
            onClick={() => setOpenProductModal(true)}
            className="rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-indigo-700"
          >
            Nueva referencia
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <p className="text-sm text-slate-500">Unidades totales</p>
          <p className="mt-2 text-2xl font-bold text-slate-950">{totalUnits}</p>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <p className="text-sm text-slate-500">Stock bajo</p>
          <p className="mt-2 text-2xl font-bold text-amber-600">{lowStockCount}</p>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <p className="text-sm text-slate-500">Bodega</p>
          <p className="mt-2 text-2xl font-bold text-slate-950">{warehouseUnits}</p>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <p className="text-sm text-slate-500">Tienda</p>
          <p className="mt-2 text-2xl font-bold text-slate-950">{storeUnits}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        {inventory.length === 0 && (
          <div className="col-span-full rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center text-slate-500">
            No hay existencias registradas aún.
          </div>
        )}

        {inventory.map((item) => (
          <div key={item.id} className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm transition hover:shadow-md">
            <div className="aspect-[16/10] bg-slate-100">
              <img src={item.product.photo_url} alt={item.product.name} className="h-full w-full object-cover" />
            </div>
            <div className="space-y-4 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-widest text-slate-400">{item.product.reference}</p>
                  <h3 className="mt-1 text-lg font-bold text-slate-950">{item.product.name}</h3>
                  <p className="text-sm text-slate-500">{item.product.brand}</p>
                </div>
                {item.is_low_stock && (
                  <span className="rounded-full bg-amber-100 px-2 py-1 text-xs font-semibold text-amber-700">Stock bajo</span>
                )}
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="rounded-md bg-slate-50 p-3">
                  <p className="text-slate-500">Cantidad</p>
                  <p className="font-semibold text-slate-950">{item.quantity}</p>
                </div>
                <div className="rounded-md bg-slate-50 p-3">
                  <p className="text-slate-500">Talla euro</p>
                  <p className="font-semibold text-slate-950">{item.size}</p>
                </div>
                <div className="rounded-md bg-slate-50 p-3">
                  <p className="text-slate-500">Ubicación</p>
                  <p className="font-semibold text-slate-950">{locationLabel(item.location_type)}</p>
                </div>
                <div className="rounded-md bg-slate-50 p-3">
                  <p className="text-slate-500">Detalle</p>
                  <p className="font-semibold text-slate-950">{item.location_detail}</p>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {item.colors.map((color) => (
                  <span key={color.id} className="rounded-full border border-slate-200 px-2 py-1 text-xs text-slate-600">
                    {color.name}
                  </span>
                ))}
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-slate-500">Entrada</p>
                  <p className="font-semibold">{money(item.product.current_purchase_price)}</p>
                </div>
                <div>
                  <p className="text-slate-500">Venta</p>
                  <p className="font-semibold">{money(item.product.current_sale_price)}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => setOpenEntryModal(true)}
                  className="rounded bg-green-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-green-700"
                >
                  Entrada
                </button>
                <button
                  onClick={() => {
                    setSelectedItem(item)
                    setOpenExitModal(true)
                  }}
                  className="rounded bg-red-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-red-700"
                >
                  Salida
                </button>
                <button
                  onClick={() => {
                    setSelectedItem(item)
                    setOpenAdjustmentModal(true)
                  }}
                  className="rounded bg-yellow-500 px-3 py-2 text-sm font-semibold text-slate-950 transition hover:bg-yellow-400"
                >
                  Ajuste
                </button>
                <button
                  onClick={() => {
                    setSelectedItem(item)
                    setOpenMovementsModal(true)
                  }}
                  className="rounded bg-slate-900 px-3 py-2 text-sm font-semibold text-white transition hover:bg-slate-700"
                >
                  Historial
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <Modal open={openProductModal} onClose={() => setOpenProductModal(false)} title="Crear referencia">
        <ProductForm onCreated={refresh} />
      </Modal>

      <Modal open={openEntryModal} onClose={() => setOpenEntryModal(false)} title="Registrar entrada">
        <InventoryEntryForm onCreated={refresh} products={products} colors={colors} />
      </Modal>

      <Modal
        open={openExitModal}
        onClose={() => {
          setOpenExitModal(false)
          setSelectedItem(null)
        }}
        title="Registrar salida"
      >
        {selectedItem && <InventoryExitForm inventoryItemId={selectedItem.id} onCreated={refresh} />}
      </Modal>

      <Modal
        open={openAdjustmentModal}
        onClose={() => {
          setOpenAdjustmentModal(false)
          setSelectedItem(null)
        }}
        title="Registrar ajuste"
      >
        {selectedItem && <InventoryAdjustmentForm inventoryItemId={selectedItem.id} onCreated={refresh} />}
      </Modal>

      <Modal
        open={openMovementsModal}
        onClose={() => {
          setOpenMovementsModal(false)
          setSelectedItem(null)
        }}
        title="Historial de movimientos"
      >
        {selectedItem && <InventoryMovements inventoryItemId={selectedItem.id} />}
      </Modal>
    </div>
  )
}
