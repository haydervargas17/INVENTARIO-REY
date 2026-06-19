import React from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../services/api'

async function fetchInventory() {
  const res = await api.get('/inventory')
  return res.data.data
}

export default function Inventory() {
  const { data, isLoading, error } = useQuery(['inventory'], fetchInventory)

  if (isLoading) return <div className="p-6">Cargando...</div>
  if (error) return <div className="p-6">Error al cargar inventario</div>

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Inventario</h1>
      <div className="bg-white rounded shadow p-4">
        <pre className="text-sm">{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  )
}
