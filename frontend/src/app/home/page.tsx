'use client'

import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-pink-100 via-purple-100 to-indigo-100 text-gray-900">
      {/* Header */}
      <header className="flex items-center justify-between px-8 py-4 border-b border-purple-200 shadow-sm bg-white/60 backdrop-blur-lg">
        <h1 className="text-2xl font-bold text-purple-700">AI-Ассистент студента</h1>
        <nav className="flex gap-4 text-sm">
          <Link href="/assistant" className="text-purple-600 hover:underline">Чат</Link>
          <Link href="/planner" className="text-purple-600 hover:underline">Планер</Link>
          <Link href="/login" className="text-gray-500 hover:underline">Выйти</Link>
        </nav>
      </header>

      {/* Main Section */}
      <main className="flex flex-col items-center justify-center flex-1 px-6 py-12 text-center">
        <h2 className="text-4xl font-bold mb-4 text-purple-800">Твой умный помощник в учёбе</h2>
        <p className="text-lg text-gray-700 max-w-2xl mb-10">
          Забудь про дедлайны, запутанные методички и бесконечные вопросы. Наш AI-ассистент поможет тебе учиться проще, быстрее и эффективнее.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl text-left mb-10">
          <div className="p-5 bg-white/70 rounded-xl shadow">
            <h3 className="font-semibold text-purple-700 mb-1">🤖 Отвечает на методички</h3>
            <p className="text-sm text-gray-700">Загрузи PDF и задай вопрос — ассистент найдёт нужное место и объяснит.</p>
          </div>
          <div className="p-5 bg-white/70 rounded-xl shadow">
            <h3 className="font-semibold text-purple-700 mb-1">📅 Строит расписание</h3>
            <p className="text-sm text-gray-700">Введи задачи, дедлайны и расписание — и получи понятный план.</p>
          </div>
          <div className="p-5 bg-white/70 rounded-xl shadow">
            <h3 className="font-semibold text-purple-700 mb-1">📨 Telegram-напоминания</h3>
            <p className="text-sm text-gray-700">Ассистент отправит напоминания о важных дедлайнах прямо в Telegram.</p>
          </div>
          <div className="p-5 bg-white/70 rounded-xl shadow">
            <h3 className="font-semibold text-purple-700 mb-1">🎓 Помогает разобраться</h3>
            <p className="text-sm text-gray-700">Никаких готовых решений — только помощь в понимании и изучении.</p>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col md:flex-row gap-4">
          <Link
            href="/assistant"
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg text-lg shadow"
          >
            Перейти к Чату
          </Link>
          <Link
            href="/scheduler"
            className="bg-pink-500 hover:bg-pink-600 text-white px-6 py-3 rounded-lg text-lg shadow"
          >
            Перейти к Планеру
          </Link>
        </div>
      </main>
    </div>
  )
}