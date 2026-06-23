import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../services/api'
import { setToken } from '../services/auth'

type Form = {
  username: string
  password: string
}

export default function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<Form>()
  const navigate = useNavigate()
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  async function onSubmit(data: Form) {
    setErrorMsg(null)
    try {
      const response = await api.post('/auth/login', data)
      setToken(response.data.data.access_token)
      navigate('/')
    } catch {
      setErrorMsg('Credenciales inválidas')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-black px-4 text-white">
      <motion.div
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: [0, -6, 0], opacity: 1 }}
        transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
        className="relative z-10 grid w-full max-w-4xl grid-cols-1 overflow-hidden rounded-xl border border-white/10 shadow-2xl md:grid-cols-2"
      >
        <div
          className="hidden flex-col items-start justify-center bg-black/40 p-10 md:flex"
          style={{ backgroundImage: 'linear-gradient(135deg, rgba(0,0,0,0.55) 0%, rgba(99,102,241,0.15) 100%)' }}
        >
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-emerald-300">Inventario</p>
          <h2 className="mt-3 text-4xl font-extrabold tracking-tight">InvElRey</h2>
          <p className="mt-4 max-w-md text-gray-200">Control de referencias, entradas, ventas y ajustes para El Rey de los Zapatos.</p>
          <div className="mt-8 grid grid-cols-3 gap-3 text-xs font-semibold uppercase tracking-widest text-white/70">
            <div className="rounded border border-white/10 bg-white/10 px-3 py-4 text-center">Stock</div>
            <div className="rounded border border-white/10 bg-white/10 px-3 py-4 text-center">Ventas</div>
            <div className="rounded border border-white/10 bg-white/10 px-3 py-4 text-center">Bodega</div>
          </div>
        </div>

        <div className="flex flex-col justify-center bg-white/5 p-8 backdrop-blur-sm md:p-10">
          <h1 className="mb-2 text-2xl font-bold md:text-3xl">Bienvenido de nuevo</h1>
          <p className="mb-6 text-sm text-gray-200">Entra con tu cuenta para acceder al panel.</p>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="text-xs text-gray-300">Usuario</label>
              <input
                {...register('username', { required: 'Usuario requerido' })}
                className={`mt-1 block w-full rounded-md border bg-black/30 px-4 py-3 text-white transition focus:outline-none focus:ring-2 focus:ring-primary-500 ${errors.username ? 'border-red-400' : 'border-transparent'}`}
              />
              {errors.username && <p className="mt-1 text-sm text-red-300">{errors.username.message}</p>}
            </div>

            <div>
              <label className="text-xs text-gray-300">Contraseña</label>
              <input
                type="password"
                {...register('password', { required: 'Contraseña requerida' })}
                className={`mt-1 block w-full rounded-md border bg-black/30 px-4 py-3 text-white transition focus:outline-none focus:ring-2 focus:ring-primary-500 ${errors.password ? 'border-red-400' : 'border-transparent'}`}
              />
              {errors.password && <p className="mt-1 text-sm text-red-300">{errors.password.message}</p>}
            </div>

            {errorMsg && <div className="text-sm text-red-300">{errorMsg}</div>}

            <button
              type="submit"
              disabled={isSubmitting}
              className="inline-flex w-full items-center justify-center gap-2 rounded bg-gradient-to-r from-primary-500 to-accent-500 px-4 py-3 font-semibold text-black transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
            >
              Entrar
            </button>
          </form>
        </div>
      </motion.div>
    </div>
  )
}
