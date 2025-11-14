'use client'

import { useState } from 'react'

const styles = ['Аниме', 'Комикс', 'Акварель', '3D', 'Классический']

export default function GeneratePage() {
  const [prompt, setPrompt] = useState('')
  const [selectedStyle, setSelectedStyle] = useState(styles[0])
  const [loading, setLoading] = useState(false)
  const [story, setStory] = useState('')

  const handleGenerate = async () => {
    if (!prompt) return
    setLoading(true)

    // Временная заглушка, пока нет API
    setTimeout(() => {
      setStory(`🔮 Это волшебная сказка про: ${prompt} в стиле ${selectedStyle}... (тут будет настоящая генерация)`)
      setLoading(false)
    }, 1200)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-pink-100 via-violet-100 to-indigo-100 px-4 py-8 flex flex-col items-center">
      <h1 className="text-3xl md:text-5xl font-bold text-purple-800 text-center mb-10 drop-shadow-lg">
        Генерация вашей сказки
      </h1>

      {/* Ввод запроса */}
      <textarea
        className="w-full max-w-xl h-32 p-4 border-2 border-purple-300 rounded-lg resize-none text-lg shadow-sm focus:outline-none focus:border-purple-500"
        placeholder="Например: «Сказка про лисёнка и дракона»"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      {/* Выбор стиля */}
      <div className="flex flex-wrap gap-3 mt-6 justify-center">
        {styles.map((style) => (
          <button
            key={style}
            className={`px-4 py-2 rounded-full text-sm font-medium border transition-all ${
              selectedStyle === style
                ? 'bg-purple-600 text-white border-purple-700 shadow-md'
                : 'bg-white text-purple-700 border-purple-300 hover:border-purple-500'
            }`}
            onClick={() => setSelectedStyle(style)}
          >
            {style}
          </button>
        ))}
      </div>

      {/* Кнопка генерации */}
      <button
        className="mt-8 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white text-lg rounded-full shadow-md hover:scale-105 transition-transform"
        onClick={handleGenerate}
        disabled={loading || !prompt}
      >
        {loading ? 'Генерация...' : 'Сгенерировать сказку'}
      </button>

      {/* Блок результата */}
      {story && (
        <div className="mt-10 w-full max-w-3xl bg-white p-6 rounded-lg shadow-lg border border-purple-200">
          <h2 className="text-2xl font-semibold mb-4 text-purple-700">Ваша сказка:</h2>
          <p className="text-gray-800 whitespace-pre-line leading-relaxed">{story}</p>
        </div>
      )}
    </main>
  )
}
