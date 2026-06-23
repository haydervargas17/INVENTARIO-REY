import { useForm } from 'react-hook-form'
import api from '../services/api'

type FormValues = {
  quantity_delta: number
  reason: string
}

export default function InventoryAdjustmentForm({ inventoryItemId, onCreated }: { inventoryItemId: string; onCreated: () => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ defaultValues: { quantity_delta: 0, reason: '' } })

  async function onSubmit(values: FormValues) {
    try {
      if (values.quantity_delta === 0) {
        alert('El ajuste no puede ser cero')
        return
      }
      await api.post(`/inventory/${inventoryItemId}/adjustments`, values)
      onCreated()
    } catch (err) {
      console.error(err)
      alert('Error registrando ajuste')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Ajuste (+/-)</label>
        <input
          type="number"
          {...register('quantity_delta', { valueAsNumber: true })}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm ${errors.quantity_delta ? 'border-red-300' : 'border-gray-200'}`}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Motivo</label>
        <input
          {...register('reason', { required: 'Motivo requerido' })}
          className="mt-1 block w-full rounded-md border border-gray-200 px-3 py-2 shadow-sm"
        />
        {errors.reason && <p className="mt-1 text-sm text-red-600">{errors.reason.message}</p>}
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded bg-yellow-500 px-4 py-2 text-slate-950 transition hover:bg-yellow-400 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Aplicar ajuste
        </button>
      </div>
    </form>
  )
}
