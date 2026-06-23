import { useForm } from 'react-hook-form'
import api from '../services/api'

type FormValues = {
  quantity: number
  reason: string
}

export default function InventoryExitForm({ inventoryItemId, onCreated }: { inventoryItemId: string; onCreated: () => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ defaultValues: { quantity: 1, reason: 'Venta' } })

  async function onSubmit(values: FormValues) {
    try {
      await api.post(`/inventory/${inventoryItemId}/exits`, values)
      onCreated()
    } catch (err) {
      console.error(err)
      alert('Error registrando salida')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Cantidad</label>
        <input
          type="number"
          min={1}
          {...register('quantity', {
            valueAsNumber: true,
            min: { value: 1, message: 'Mínimo 1' },
          })}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm ${errors.quantity ? 'border-red-300' : 'border-gray-200'}`}
        />
        {errors.quantity && <p className="mt-1 text-sm text-red-600">{errors.quantity.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Motivo</label>
        <input
          {...register('reason', { required: 'El motivo es obligatorio' })}
          className="mt-1 block w-full rounded-md border border-gray-200 px-3 py-2 shadow-sm"
        />
        {errors.reason && <p className="mt-1 text-sm text-red-600">{errors.reason.message}</p>}
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded bg-red-600 px-4 py-2 text-white transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Registrar salida
        </button>
      </div>
    </form>
  )
}
