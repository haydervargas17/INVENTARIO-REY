import { useQuery } from '@tanstack/react-query'
import api from '../services/api'
import type { ApiResponse, InventoryMovement } from '../types/api'

async function fetchMovements(inventoryItemId: string) {
  const response = await api.get<ApiResponse<InventoryMovement[]>>(`/inventory/${inventoryItemId}/movements`)
  return response.data.data
}

function formatMovementType(type: InventoryMovement['movement_type']) {
  if (type === 'IN') return 'Entrada'
  if (type === 'OUT') return 'Salida'
  return 'Ajuste'
}

export default function InventoryMovements({ inventoryItemId }: { inventoryItemId: string }) {
  const { data, isLoading, error } = useQuery(['inventory-movements', inventoryItemId], () => fetchMovements(inventoryItemId))

  if (isLoading) return <div className="text-sm text-slate-500">Cargando historial...</div>
  if (error) return <div className="text-sm text-red-600">No se pudo cargar el historial.</div>

  if (!data?.length) {
    return <div className="rounded-md border border-dashed border-slate-300 p-4 text-sm text-slate-500">Sin movimientos registrados.</div>
  }

  return (
    <div className="space-y-3">
      {data.map((movement) => (
        <div key={movement.id} className="rounded-md border border-slate-200 p-3">
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="font-semibold text-slate-900">{formatMovementType(movement.movement_type)}</p>
              <p className="text-sm text-slate-500">{movement.reason}</p>
            </div>
            <span className={`rounded-full px-2 py-1 text-xs font-semibold ${movement.quantity_delta > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {movement.quantity_delta > 0 ? '+' : ''}
              {movement.quantity_delta}
            </span>
          </div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-500">
            <span>Antes: {movement.previous_quantity}</span>
            <span>Después: {movement.new_quantity}</span>
            <span>{new Date(movement.created_at).toLocaleString()}</span>
            <span>{movement.user_full_name || movement.username || 'Usuario'}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
