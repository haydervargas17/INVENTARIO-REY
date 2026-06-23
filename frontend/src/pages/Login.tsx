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
      setErrorMsg('Credenciales invalidas')
    }
  }

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#131313] text-[#e5e2e1] font-street">
      <div className="fixed inset-0 z-[100] login-grain-overlay" aria-hidden="true" />

      <header className="sticky top-0 z-50 flex w-full items-center justify-between border-b-2 border-[#84967e] bg-[#131313]/80 px-5 py-4 backdrop-blur-md md:px-16">
        <div className="font-blackletter text-4xl uppercase tracking-tight text-[#e5e2e1] md:text-5xl">InvElRey</div>
        <div className="flex items-center gap-4 md:gap-6">
          <span className="hidden font-mono text-xs uppercase text-[#b9ccb2] md:inline">Sistema interno</span>
          <span className="border-b-2 border-[#00e639] font-mono text-xs font-bold uppercase text-[#00e639]">Acceso</span>
        </div>
      </header>

      <main className="relative grid min-h-[calc(100vh-82px)] grid-cols-1 overflow-hidden md:grid-cols-12">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 z-10 bg-gradient-to-r from-black/95 via-black/50 to-transparent" />
          <img
            alt=""
            aria-hidden="true"
            className="h-full w-full object-cover grayscale-[0.4]"
            src="https://lh3.googleusercontent.com/aida/AP1WRLvilb1IuakPBIlIv4OYSh2poCThluOpjOs-PyPh1X6kLRAC7Uw-XGK3fC_ZtVOZcH2u6ABF0osMbWzUfP6r9-muBSLhVn-WO48nD2LmWYSaFk3c0-HoihcidX-l0Zn1olMurZVixQz_2lZZJ1rExwsZcNc1tFMwFEilBu4i87F-ficeE9LtO_0zixOEM81Rm_ZWVKJYjoaKG10mwr6nKk_Ml6iV8PU4akIlTw4cFhYFZce2dcsHqwszGTs"
          />
        </div>

        <motion.section
          initial={{ x: -24, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.45, ease: 'easeOut' }}
          className="login-skew-panel relative z-20 flex min-h-[calc(100vh-82px)] flex-col justify-center border-r-4 border-[#00e639] bg-[#0e0e0e]/85 px-5 py-12 backdrop-blur-md md:col-span-6 md:px-16 lg:col-span-5"
        >
          <div className="login-scanline" aria-hidden="true" />

          <div className="mb-12">
            <div className="flex items-center gap-4">
              <span className="h-[2px] w-12 bg-[#00e639]" />
              <p className="font-mono text-xs uppercase tracking-[0.3em] text-[#00e639]">Nodo_entrada_seguro</p>
            </div>
          </div>

          <div className="mb-10">
            <h1 className="login-text-distressed font-blackletter text-5xl uppercase leading-none tracking-wide text-[#e5e2e1] md:text-6xl">
              Autenticar
              <br />
              inventario
            </h1>
            <p className="mt-3 font-mono text-xs uppercase text-[#b9ccb2]">[ Estado: autorizacion pendiente ]</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="max-w-sm space-y-8" noValidate>
            <div className="group relative">
              <label htmlFor="username" className="mb-1 block font-mono text-xs uppercase text-[#b9ccb2] group-focus-within:text-[#00e639]">
                ID_usuario
              </label>
              <div className={`flex items-center border-b-[3px] transition-all group-focus-within:border-[#00e639] ${errors.username ? 'border-[#ffb4ab]' : 'border-[#e5e2e1]'}`}>
                <span className="material-symbols-outlined pr-2 text-sm text-[#3b4b37]" aria-hidden="true">
                  alternate_email
                </span>
                <input
                  id="username"
                  type="text"
                  autoComplete="username"
                  placeholder="USUARIO"
                  aria-invalid={Boolean(errors.username)}
                  aria-describedby={errors.username ? 'username-error' : undefined}
                  className="w-full border-0 bg-transparent px-0 py-3 font-mono text-[#e5e2e1] placeholder:text-[#84967e]/50 focus:ring-0"
                  {...register('username', { required: 'Usuario requerido' })}
                />
              </div>
              {errors.username && (
                <p id="username-error" className="mt-2 font-mono text-xs uppercase text-[#ffb4ab]">
                  {errors.username.message}
                </p>
              )}
            </div>

            <div className="group relative">
              <label htmlFor="password" className="mb-1 block font-mono text-xs uppercase text-[#b9ccb2] group-focus-within:text-[#00e639]">
                Clave_encriptacion
              </label>
              <div className={`flex items-center border-b-[3px] transition-all group-focus-within:border-[#00e639] ${errors.password ? 'border-[#ffb4ab]' : 'border-[#e5e2e1]'}`}>
                <span className="material-symbols-outlined pr-2 text-sm text-[#3b4b37]" aria-hidden="true">
                  lock_open
                </span>
                <input
                  id="password"
                  type="password"
                  autoComplete="current-password"
                  placeholder="********"
                  aria-invalid={Boolean(errors.password)}
                  aria-describedby={errors.password ? 'password-error' : undefined}
                  className="w-full border-0 bg-transparent px-0 py-3 font-mono text-[#e5e2e1] placeholder:text-[#84967e]/50 focus:ring-0"
                  {...register('password', { required: 'Contrasena requerida' })}
                />
              </div>
              {errors.password && (
                <p id="password-error" className="mt-2 font-mono text-xs uppercase text-[#ffb4ab]">
                  {errors.password.message}
                </p>
              )}
            </div>

            <div className="border-l-2 border-[#00e639] pl-3 font-mono text-xs uppercase text-[#b9ccb2]">
              Token operativo: 8 horas. Acceso solo con credenciales creadas por administracion.
            </div>

            {errorMsg && (
              <div role="alert" className="border border-[#ffb4ab] bg-[#93000a]/30 p-3 font-mono text-xs uppercase text-[#ffdad6]">
                {errorMsg}
              </div>
            )}

            <div className="relative pt-6">
              <div className="absolute -left-4 -top-4 h-8 w-8 border-l-2 border-t-2 border-[#00e639]" aria-hidden="true" />
              <button
                type="submit"
                disabled={isSubmitting}
                className="group login-btn-hover-shift login-text-distressed relative w-full overflow-hidden bg-[#00ff41] py-6 font-blackletter text-4xl uppercase tracking-wider text-[#007117] transition-all active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <span className="relative z-10">{isSubmitting ? 'Validando' : 'Inicializar_enlace'}</span>
                <span className="absolute inset-0 -translate-x-full skew-x-12 bg-white/10 transition-transform duration-500 group-hover:translate-x-full" aria-hidden="true" />
              </button>
            </div>
          </form>

          <div className="pointer-events-none absolute bottom-8 right-12 hidden opacity-20 lg:block">
            <div className="text-right font-mono text-[10px] uppercase leading-tight">
              Terminal_inventario
              <br />
              Rol: admin / system_admin
              <br />
              Sesion: jwt_8h
            </div>
          </div>
        </motion.section>

        <aside className="pointer-events-none z-20 hidden flex-col justify-end p-16 md:col-span-6 md:flex lg:col-span-7">
          <div className="mb-12 max-w-xs border-l-2 border-white/10 pl-6">
            <p className="font-blackletter text-5xl leading-none text-[#00e639] opacity-40">
              EL STOCK
              <br />
              NO DUERME
            </p>
          </div>
        </aside>
      </main>

      <footer className="flex w-full flex-col items-center justify-between gap-4 border-t-2 border-[#84967e] bg-[#0e0e0e] px-5 py-6 md:flex-row md:px-16">
        <div className="flex flex-col items-center gap-3 md:flex-row md:gap-6">
          <div className="origin-left scale-75 font-blackletter text-5xl text-[#e5e2e1]">InvElRey</div>
          <p className="font-mono text-xs uppercase text-[#b4b5b5]">Sistema interno de inventario. Acceso restringido.</p>
        </div>
        <p className="font-mono text-xs uppercase text-[#b4b5b5]">Sin registro publico · sin recuperacion publica</p>
      </footer>
    </div>
  )
}
