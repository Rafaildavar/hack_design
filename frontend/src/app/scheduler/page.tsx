'use client'

import { useState } from 'react'
import { Paperclip, Send, CheckCircle, Circle } from 'lucide-react'

export default function PlannerPage() {
  const [messages, setMessages] = useState<{ role: 'user' | 'planner'; content: string }[]>([])
  const [input, setInput] = useState('')
  const [tasks, setTasks] = useState<{ id: number; text: string; done: boolean }[]>([])
  const [taskId, setTaskId] = useState(1)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Сохраняем сообщение юзера
    setMessages((prev) => [...prev, { role: 'user', content: input }])

    // Имитация ответа планера (в будущем подключим ИИ)
    const newTask = {
      id: taskId,
      text: input,
      done: false,
    }
    setTasks((prev) => [...prev, newTask])
    setTaskId((prev) => prev + 1)

    setMessages((prev) => [
      ...prev,
      { role: 'planner', content: `Добавлена задача: ${input}` },
    ])

    setInput('')
  }

  const toggleTask = (id: number) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === id ? { ...task, done: !task.done } : task
      )
    )
  }

  return (
    <div className="min-h-screen flex bg-white text-gray-900">
      {/* Левая панель - чат */}
      <aside className="w-1/2 border-r border-gray-200 flex flex-col">
        <header className="p-4 border-b border-gray-100">
          <h1 className="text-lg font-bold text-purple-700">Твой учебный планер</h1>
        </header>

        <section className="flex-1 overflow-y-auto p-4 space-y-2">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`max-w-xl px-3 py-2 rounded-xl text-sm whitespace-pre-wrap ${
                msg.role === 'user'
                  ? 'bg-purple-100 self-end ml-auto'
                  : 'bg-gray-100 self-start mr-auto'
              }`}
            >
              {msg.content}
            </div>
          ))}
        </section>

        <form
          onSubmit={handleSubmit}
          className="border-t border-gray-200 p-4 flex justify-center"
        >
          <div className="flex items-center gap-2 w-full max-w-2xl">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Напиши задачу или расписание..."
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
      </aside>

      {/* Правая панель - задачи */}
      <main className="w-1/2 p-6">
        <h2 className="text-xl font-bold text-purple-700 mb-4">Текущее расписание</h2>
        {tasks.length === 0 ? (
          <p className="text-gray-500 italic">Здесь появится твой план после ввода задач.</p>
        ) : (
          <ul className="space-y-3">
            {tasks.map((task) => (
              <li
                key={task.id}
                className="flex items-center gap-3 cursor-pointer group"
                onClick={() => toggleTask(task.id)}
              >
                {task.done ? (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                ) : (
                  <Circle className="w-5 h-5 text-gray-400 group-hover:text-purple-500" />
                )}
                <span className={task.done ? 'line-through text-gray-400' : ''}>{task.text}</span>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  )
}
