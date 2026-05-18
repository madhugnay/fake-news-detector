import React, { useState } from 'react'
import { Moon, Sun } from 'lucide-react'

import Tabs from './components/Tabs'

import MultimodalTab from './components/tabs/MultimodalTab'
import ImageTab from './components/tabs/ImageTab'
import TextTab from './components/tabs/TextTab'
import AudioTab from './components/tabs/AudioTab'

export default function App() {

  const [darkMode, setDarkMode] = useState(() => {

    // Initialize from localStorage immediately to prevent flicker
    const savedTheme = localStorage.getItem('theme') || 'light'

    const isDark = savedTheme === 'dark'

    if (isDark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }

    return isDark
  })

  const [activeTab, setActiveTab] = useState('multimodal')

  // Toggle dark mode
  const toggleDarkMode = () => {

    const newDarkMode = !darkMode

    setDarkMode(newDarkMode)

    localStorage.setItem(
      'theme',
      newDarkMode ? 'dark' : 'light'
    )

    if (newDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Tabs
  const tabs = [

    {
      id: 'multimodal',
      label: 'Multimodal'
    },

    {
      id: 'image',
      label: 'Image Only'
    },

    {
      id: 'text',
      label: 'Text Only'
    },

    {
      id: 'audio',
      label: 'Audio Only'
    }
  ]

  return (

    <div className="min-h-screen transition-all duration-500 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">

      {/* Theme Toggle Button */}
      <button
        onClick={toggleDarkMode}
        className="fixed top-6 right-6 z-50 p-3 rounded-full glass-card hover:bg-white/30 dark:hover:bg-gray-800/50 transition-all duration-300 shadow-lg"
      >

        {darkMode ? (

          <Sun
            size={24}
            className="text-yellow-400"
          />

        ) : (

          <Moon
            size={24}
            className="text-purple-600"
          />
        )}

      </button>

      {/* Main Container */}
      <div className="flex items-center justify-center min-h-screen px-4 py-8">

        <div className="w-full max-w-2xl">

          {/* Glass Card */}
          <div className="glass-card rounded-2xl shadow-2xl overflow-hidden border border-white/20 dark:border-gray-700/30 p-8 sm:p-10">

            {/* Header */}
            <div className="mb-8 text-center animate-fade-in">

              <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-purple-600 to-purple-900 dark:from-purple-400 dark:to-purple-300 bg-clip-text text-transparent mb-2 font-poppins">

                Fake News Detector

              </h1>

              <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base">

                Analyze image, text, and audio using AI-powered deepfake detection

              </p>

            </div>

            {/* Tabs */}
            <Tabs
              tabs={tabs}
              activeTab={activeTab}
              onTabChange={setActiveTab}
            />

            {/* Tab Content */}
            <div className="mt-8">

              {activeTab === 'multimodal' && (
                <MultimodalTab />
              )}

              {activeTab === 'image' && (
                <ImageTab />
              )}

              {activeTab === 'text' && (
                <TextTab />
              )}

              {activeTab === 'audio' && (
                <AudioTab />
              )}

            </div>

          </div>

          {/* Footer */}
          <div className="text-center mt-6 text-gray-500 dark:text-gray-400 text-xs sm:text-sm">

            <p>
              🔒 All analysis is performed securely on your device & server
            </p>

          </div>

        </div>

      </div>

    </div>
  )
}