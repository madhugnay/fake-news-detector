import React from 'react'

export default function Tabs({ tabs, activeTab, onTabChange }) {
  return (
    <div className="flex border-b border-gray-200 dark:border-gray-700 -mx-8 px-8 sm:-mx-10 sm:px-10">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`py-4 px-4 sm:px-6 font-medium text-sm sm:text-base relative transition-all duration-300 whitespace-nowrap ${
            activeTab === tab.id
              ? 'text-purple-600 dark:text-purple-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
          }`}
        >
          {tab.label}
          {activeTab === tab.id && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-purple-600 to-purple-500 dark:from-purple-400 dark:to-purple-300 animate-slide-down" />
          )}
        </button>
      ))}
    </div>
  )
}
