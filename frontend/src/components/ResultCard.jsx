import React from 'react'
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react'

export default function ResultCard({ title, prediction, confidence, probabilities, variant }) {
  const getPredictionColor = (pred) => {
    if (pred === 'real') return 'result-card-real'
    if (pred === 'fake') return 'result-card-fake'
    if (pred === 'uncertain') return 'result-card-uncertain'
    if (pred === 'ai' || pred === 'deepfake') return 'result-card-fake'
    return 'result-card-real'
  }

  const getPredictionBadgeColor = (pred) => {
    if (pred === 'real') return 'prediction-real'
    if (pred === 'fake') return 'prediction-fake'
    if (pred === 'uncertain') return 'prediction-uncertain'
    if (pred === 'ai' || pred === 'deepfake') return 'prediction-fake'
    return 'prediction-real'
  }

  const getPredictionIcon = (pred) => {
    if (pred === 'real') return <CheckCircle size={24} className="text-green-600" />
    if (pred === 'fake' || pred === 'ai' || pred === 'deepfake') return <XCircle size={24} className="text-red-600" />
    return <AlertCircle size={24} className="text-yellow-600" />
  }

  return (
    <div className={`rounded-xl p-6 ${getPredictionColor(prediction)}`}>
      <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-4 uppercase tracking-wide">
        {title}
      </h3>

      <div className="flex items-center gap-3 mb-4">
        {getPredictionIcon(prediction)}
        <div className={`prediction-badge ${getPredictionBadgeColor(prediction)}`}>
          {prediction.toUpperCase()}
        </div>
      </div>

      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-700 dark:text-gray-300">Confidence</span>
          <span className="font-semibold text-gray-900 dark:text-white">{confidence}%</span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-purple-500 to-purple-600 transition-all duration-500"
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      {/* Probabilities */}
      {probabilities && (
        <div className="space-y-2 pt-4 border-t border-gray-300 dark:border-gray-600">
          {Object.entries(probabilities).map(([label, value]) => (
            <div key={label} className="flex justify-between items-center text-sm">
              <span className="text-gray-700 dark:text-gray-300 capitalize">{label}</span>
              <span className="font-medium text-gray-900 dark:text-white">{value}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
