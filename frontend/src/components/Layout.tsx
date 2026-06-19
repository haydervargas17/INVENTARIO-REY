import React from 'react'
import { Outlet, Link } from 'react-router-dom'
import { clearToken, getToken } from '../services/auth'

export default function Layout() {
  function logout() {
    clearToken()
    window.location.href = '/login'
  }

  return (
    <div className="min-h-screen">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h2 className="font-bold">InvElRey</h2>
          <nav>
            <Link to="/" className="mr-4">Inventario</Link>
            {getToken() ? <button onClick={logout} className="text-sm text-red-600">Cerrar sesión</button> : <Link to="/login">Login</Link>}
          </nav>
        </div>
      </header>
      <main className="max-w-6xl mx-auto p-4">
        <Outlet />
      </main>
    </div>
  )
}
