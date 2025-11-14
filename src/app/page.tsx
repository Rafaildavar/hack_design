'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { Rubik } from 'next/font/google'

const rubik = Rubik({
  subsets: ['latin', 'cyrillic'],
  weight: ['400', '500', '700'],
})

export default function Home() {
  const router = useRouter()
  const [isLoggedIn] = useState(false) // пока заглушка

  const handleStartClick = () => {
    router.push(isLoggedIn ? '/assistant' : '/login')
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-300 via-pink-300 to-orange-300 flex flex-col items-center justify-center px-6 relative">
      {/* Навигация */}
      <header className="absolute top-0 right-0 p-6 flex gap-4 z-10">
        <button
          onClick={() => router.push('/login')}
          className="text-sm font-medium text-gray-700 hover:text-purple-700 transition"
        >
          Войти
        </button>
        <button
          onClick={() => router.push('/register')}
          className="text-sm font-medium text-white bg-purple-600 px-4 py-2 rounded-full hover:bg-purple-700 transition"
        >
          Регистрация
        </button>
      </header>

      {/* Контент */}
      <h1 className={`${rubik.className} text-5xl ...`}>
        Твой AI-ассистент в учёбе
      </h1>
            
      <p className="text-lg md:text-xl text-gray-700 max-w-xl text-center">
        Поможет разобраться в методичках, следить за расписанием и не пропускать дедлайны.
      </p>

      {/* Стрелка */}
      <div className="animate-bounce mt-8 mb-2 text-3xl text-gray-700">↓</div>

      {/* Кнопка */}
      <button
        onClick={handleStartClick}
        className="text-xl bg-gradient-to-r from-purple-500 to-pink-500 hover:from-pink-600 hover:to-purple-600 text-white px-10 py-4 rounded-full shadow-lg hover:scale-105 transform transition-all duration-300"
      >
        Начать сейчас
      </button>
    </main>
  )
}
