// src/app/register/page.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Регистрация:', { name, email, password })
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-200 via-purple-200 to-indigo-200 px-4">
      <div className="bg-white/80 backdrop-blur-lg shadow-xl rounded-2xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-purple-700 mb-6">
          Создать аккаунт
        </h1>
        <form onSubmit={handleRegister} className="space-y-4">
          <input
            type="text"
            placeholder="Имя"
            className="w-full px-4 py-2 rounded-lg text-gray-700 border focus:outline-none focus:ring-2 focus:ring-purple-400"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="email"
            placeholder="Логин"
            className="w-full px-4 py-2 rounded-lg text-gray-700 border focus:outline-none focus:ring-2 focus:ring-purple-400"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Пароль"
            className="w-full px-4 py-2 rounded-lg text-gray-700 border focus:outline-none focus:ring-2 focus:ring-purple-400"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-2 rounded-lg hover:opacity-90 transition"
          >
            Зарегистрироваться
          </button>
        </form>
        <p className="text-center text-sm text-gray-700 mt-4">
          Уже есть аккаунт?{' '}
          <Link href="/login" className="text-purple-600 hover:underline">
            Войти
          </Link>
        </p>
      </div>
    </main>
  )
}
