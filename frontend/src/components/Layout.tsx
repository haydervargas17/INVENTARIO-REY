import { Outlet, Link } from 'react-router-dom'
import api from '../services/api'
import { clearToken, getToken } from '../services/auth'

export default function Layout() {
  async function logout() {
    try {
      await api.post('/auth/logout')
    } catch {
      // The local session must end even if the network request fails.
    } finally {
      clearToken()
      window.location.href = '/login'
    }
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <h2 className="font-extrabold tracking-tight">KING URBAN</h2>
          <nav className="flex items-center gap-4 text-sm">
            <Link to="/" className="font-medium text-slate-700 hover:text-slate-950">
              Inventario
            </Link>
            {getToken() ? (
              <button onClick={logout} className="font-medium text-red-600 hover:text-red-700">
                Cerrar sesión
              </button>
            ) : (
              <Link to="/login">Login</Link>
            )}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl p-4">
        <Outlet />
      </main>
    </div>
  )
}
