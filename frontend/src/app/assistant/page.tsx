'use client'

import { useState } from 'react'
import { Paperclip, Send } from 'lucide-react'

export default function AssistantPage() {
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([])
  const [input, setInput] = useState('')
  const [pdfName, setPdfName] = useState<string | null>(null)

  // В будущем сюда можно подгружать данные из БД
  const chatHistory: { id: string; title: string }[] = []

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    setMessages([...messages, { role: 'user', content: input }, { role: 'assistant', content: 'Ответ от ассистента...' }])
    setInput('')
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type === 'application/pdf') {
      setPdfName(file.name)
      console.log('Загружен PDF:', file)
    } else {
      alert('Допустим только PDF-файл')
    }
  }

  return (
    <div className="min-h-screen flex bg-white text-gray-900">
      {/* Сайдбар слева */}
      <aside className="w-64 bg-purple-50 border-r border-gray-200 p-4 flex flex-col">
        <h2 className="text-xl font-bold text-purple-700 mb-4">История</h2>
        {chatHistory.length === 0 ? (
          <p className="text-sm text-gray-500 italic">Нет сохранённых чатов</p>
        ) : (
          <ul className="space-y-2 text-sm">
            {chatHistory.map((chat) => (
              <li
                key={chat.id}
                className="p-2 bg-purple-100 rounded-lg cursor-pointer hover:bg-purple-200"
              >
                {chat.title}
              </li>
            ))}
          </ul>
        )}
      </aside>

      {/* Контент справа */}
      <main className="flex-1 flex flex-col">
        {/* Хедер */}
        <header className="p-4 border-b border-gray-200 shadow-sm">
          <h1 className="text-xl font-bold text-purple-700">AI-Ассистент студента</h1>
        </header>

        {/* Чат */}
        <section className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`max-w-xl px-4 py-2 rounded-xl ${
                msg.role === 'user'
                  ? 'bg-purple-100 self-end ml-auto'
                  : 'bg-gray-100 self-start mr-auto'
              }`}
            >
              {msg.content}
            </div>
          ))}
          {pdfName && (
            <div className="text-sm text-gray-500 italic">
              📎 Прикреплён файл: {pdfName}
            </div>
          )}
        </section>

        {/* Поле ввода */}
        <form
          onSubmit={handleSubmit}
          className="border-t border-gray-200 p-4 flex justify-center"
        >
          <div className="flex items-center gap-2 w-full max-w-3xl">
            <label className="cursor-pointer">
              <Paperclip className="w-5 h-5 text-purple-500" />
              <input
                type="file"
                accept="application/pdf"
                onChange={handleFileUpload}
                className="hidden"
              />
            </label>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Задай вопрос или прикрепи PDF"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-300"
            />
            <button
              type="submit"
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </form>
      </main>
    </div>
  )
}
