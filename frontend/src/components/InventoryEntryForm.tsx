import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import api from '../services/api'
import type { Color, Product } from '../types/api'

type FormValues = {
  product_id: string
  size: number
  color_ids: string[]
  location_type: 'WAREHOUSE' | 'STORE'
  location_detail: string
  quantity: number
  purchase_unit_price: number
  sale_unit_price: number
  reason: string
}

type InventoryEntryFormProps = {
  onCreated: () => void
  products: Product[]
  colors: Color[]
}

export default function InventoryEntryForm({ onCreated, products, colors }: InventoryEntryFormProps) {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    defaultValues: {
      quantity: 1,
      location_type: 'WAREHOUSE',
      reason: 'Ingreso de mercancia',
      color_ids: [],
    },
  })

  const selectedProductId = watch('product_id')
  const selectedProduct = products.find((product) => product.id === selectedProductId)

  useEffect(() => {
    if (selectedProduct) {
      setValue('purchase_unit_price', selectedProduct.current_purchase_price)
      setValue('sale_unit_price', selectedProduct.current_sale_price)
    }
  }, [selectedProduct, setValue])

  async function onSubmit(values: FormValues) {
    try {
      const product = products.find((item) => item.id === values.product_id)
      if (!product) return

      await api.post('/inventory/entries', {
        product: {
          reference: product.reference,
          name: product.name,
          brand: product.brand,
          description: product.description,
          photo_url: product.photo_url,
          cloudinary_public_id: product.cloudinary_public_id,
          current_purchase_price: values.purchase_unit_price,
          current_sale_price: values.sale_unit_price,
        },
        size: values.size,
        color_ids: values.color_ids,
        location_type: values.location_type,
        location_detail: values.location_detail.trim(),
        quantity: values.quantity,
        purchase_unit_price: values.purchase_unit_price,
        sale_unit_price: values.sale_unit_price,
        reason: values.reason.trim(),
      })

      onCreated()
    } catch (err) {
      console.error(err)
      alert('Error registrando entrada')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Referencia</label>
        <select
          {...register('product_id', { required: 'Selecciona una referencia' })}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm ${errors.product_id ? 'border-red-300' : 'border-gray-200'}`}
        >
          <option value="">Selecciona...</option>
          {products.map((product) => (
            <option key={product.id} value={product.id}>
              {product.reference} - {product.name}
            </option>
          ))}
        </select>
        {errors.product_id && <p className="mt-1 text-sm text-red-600">{errors.product_id.message}</p>}
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">Talla euro</label>
          <input
            type="number"
            step="0.5"
            min={1}
            {...register('size', {
              valueAsNumber: true,
              required: 'La talla es obligatoria',
              min: { value: 1, message: 'La talla debe ser positiva' },
            })}
            className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm ${errors.size ? 'border-red-300' : 'border-gray-200'}`}
          />
          {errors.size && <p className="mt-1 text-sm text-red-600">{errors.size.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Cantidad</label>
          <input
            type="number"
            min={1}
            {...register('quantity', {
              valueAsNumber: true,
              min: { value: 1, message: 'La cantidad debe ser al menos 1' },
            })}
            className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm ${errors.quantity ? 'border-red-300' : 'border-gray-200'}`}
          />
          {errors.quantity && <p className="mt-1 text-sm text-red-600">{errors.quantity.message}</p>}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Colores</label>
        <div className="mt-2 grid grid-cols-2 gap-2 sm:grid-cols-3">
          {colors.map((color) => (
            <label key={color.id} className="flex items-center gap-2 rounded-md border border-gray-200 px-3 py-2 text-sm">
              <input
                type="checkbox"
                value={color.id}
                {...register('color_ids', { required: 'Selecciona al menos un color' })}
              />
              {color.name}
            </label>
          ))}
        </div>
        {errors.color_ids && <p className="mt-1 text-sm text-red-600">{errors.color_ids.message}</p>}
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">Ubicación</label>
          <select
            {...register('location_type', { required: true })}
            className="mt-1 block w-full rounded-md border border-gray-200 px-3 py-2 shadow-sm"
          >
            <option value="WAREHOUSE">Bodega</option>
            <option value="STORE">Tienda</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Detalle de ubicación</label>
          <input
            {...register('location_detail', { required: 'Indica dónde está ubicado' })}
            placeholder="Bodega A-01"
            className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm ${errors.location_detail ? 'border-red-300' : 'border-gray-200'}`}
          />
          {errors.location_detail && <p className="mt-1 text-sm text-red-600">{errors.location_detail.message}</p>}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">Precio de entrada</label>
          <input
            type="number"
            min={0}
            {...register('purchase_unit_price', { valueAsNumber: true, min: 0, required: true })}
            className="mt-1 block w-full rounded-md border border-gray-200 px-3 py-2 shadow-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Precio de venta</label>
          <input
            type="number"
            min={0}
            {...register('sale_unit_price', { valueAsNumber: true, min: 0, required: true })}
            className="mt-1 block w-full rounded-md border border-gray-200 px-3 py-2 shadow-sm"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Motivo</label>
        <input
          {...register('reason', { required: 'El motivo es obligatorio' })}
          className="mt-1 block w-full rounded-md border border-gray-200 px-3 py-2 shadow-sm"
        />
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting || products.length === 0}
          className="rounded bg-green-600 px-4 py-2 text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Registrar entrada
        </button>
      </div>
    </form>
  )
}
