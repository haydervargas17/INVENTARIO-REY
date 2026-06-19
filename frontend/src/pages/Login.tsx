import React from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { setToken } from '../services/auth'

type Form = { username: string; password: string }

export default function Login() {
  const { register, handleSubmit } = useForm<Form>()
  const navigate = useNavigate()

  async function onSubmit(data: Form) {
    try {
      const res = await api.post('/auth/login', data)
      const token = res.data.data.access_token
      setToken(token)
      navigate('/')
    } catch (err) {
      alert('Credenciales inválidas')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-6 rounded shadow w-96">
        <h1 className="text-xl font-bold mb-4">Iniciar sesión</h1>
        <div className="mb-3">
          <label className="block text-sm mb-1">Username</label>
          <input className="w-full border p-2 rounded" {...register('username', { required: true })} />
        </div>
        <div className="mb-4">
          <label className="block text-sm mb-1">Contraseña</label>
          <input type="password" className="w-full border p-2 rounded" {...register('password', { required: true })} />
        </div>
        <button className="w-full bg-blue-600 text-white p-2 rounded">Entrar</button>
      </form>
    </div>
  )
}
