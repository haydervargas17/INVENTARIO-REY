import { useForm } from 'react-hook-form'
import api from '../services/api'

type FormValues = {
  reference: string
  name: string
  brand: string
  description: string
  current_purchase_price: number
  current_sale_price: number
  image: FileList
}

export default function ProductForm({ onCreated }: { onCreated: () => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>()

  async function onSubmit(values: FormValues) {
    try {
      const image = values.image?.[0]
      if (!image) {
        alert('Selecciona una foto de la referencia')
        return
      }

      const created = await api.post('/products', {
        reference: values.reference.trim(),
        name: values.name.trim(),
        brand: values.brand.trim(),
        description: values.description.trim(),
        photo_url: 'pending-cloudinary-upload',
        current_purchase_price: values.current_purchase_price,
        current_sale_price: values.current_sale_price,
      })

      const productId = created.data.data.id
      const formData = new FormData()
      formData.append('image', image)
      await api.post(`/products/${productId}/image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      onCreated()
    } catch (err) {
      console.error(err)
      alert('Error creando la referencia')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">Referencia</label>
          <input
            {...register('reference', { required: 'La referencia es obligatoria' })}
            className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300 ${errors.reference ? 'border-red-300' : 'border-gray-200'}`}
          />
          {errors.reference && <p className="mt-1 text-sm text-red-600">{errors.reference.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Marca</label>
          <input
            {...register('brand', { required: 'La marca es obligatoria' })}
            className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300 ${errors.brand ? 'border-red-300' : 'border-gray-200'}`}
          />
          {errors.brand && <p className="mt-1 text-sm text-red-600">{errors.brand.message}</p>}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Nombre del modelo</label>
        <input
          {...register('name', { required: 'El nombre es obligatorio' })}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300 ${errors.name ? 'border-red-300' : 'border-gray-200'}`}
        />
        {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Descripción</label>
        <textarea
          rows={3}
          {...register('description', { required: 'La descripción es obligatoria' })}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300 ${errors.description ? 'border-red-300' : 'border-gray-200'}`}
        />
        {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>}
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">Precio de entrada</label>
          <input
            type="number"
            min={0}
            {...register('current_purchase_price', {
              valueAsNumber: true,
              min: { value: 0, message: 'No puede ser negativo' },
              required: 'Precio requerido',
            })}
            className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300 ${errors.current_purchase_price ? 'border-red-300' : 'border-gray-200'}`}
          />
          {errors.current_purchase_price && <p className="mt-1 text-sm text-red-600">{errors.current_purchase_price.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Precio de venta</label>
          <input
            type="number"
            min={0}
            {...register('current_sale_price', {
              valueAsNumber: true,
              min: { value: 0, message: 'No puede ser negativo' },
              required: 'Precio requerido',
            })}
            className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300 ${errors.current_sale_price ? 'border-red-300' : 'border-gray-200'}`}
          />
          {errors.current_sale_price && <p className="mt-1 text-sm text-red-600">{errors.current_sale_price.message}</p>}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Foto de la referencia</label>
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          {...register('image', { required: 'La foto es obligatoria' })}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm ${errors.image ? 'border-red-300' : 'border-gray-200'}`}
        />
        {errors.image && <p className="mt-1 text-sm text-red-600">{errors.image.message}</p>}
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded bg-indigo-600 px-4 py-2 text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Crear referencia
        </button>
      </div>
    </form>
  )
}
