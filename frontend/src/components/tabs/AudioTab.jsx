import React, { useState } from 'react'

export default function AudioTab() {

  const [audioFile, setAudioFile] = useState(null)

  const [loading, setLoading] = useState(false)

  const [result, setResult] = useState(null)

  const handleAudioChange = (e) => {
    setAudioFile(e.target.files[0])
  }

  const handlePredict = async () => {

    if (!audioFile) {
      alert('Please upload audio file')
      return
    }

    try {

      setLoading(true)

      const formData = new FormData()

      formData.append('audio', audioFile)

      const response = await fetch(
        'http://127.0.0.1:5000/predict-audio',
        {
          method: 'POST',
          body: formData
        }
      )

      const data = await response.json()

      setResult(data)

    } catch (error) {

      console.error(error)

      alert('Prediction failed')

    } finally {

      setLoading(false)
    }
  }

  return (

    <div className="space-y-6">

      {/* Upload */}
      <div>
        <label className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
          Upload Audio File
        </label>

        <input
          type="file"
          accept=".wav,.mp3"
          onChange={handleAudioChange}
          className="w-full p-3 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white"
        />
      </div>

      {/* Predict Button */}
      <button
        onClick={handlePredict}
        disabled={loading}
        className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-xl transition-all duration-300 font-semibold"
      >
        {loading ? 'Analyzing Audio...' : 'Detect Audio Deepfake'}
      </button>

      {/* Results */}
      {result && (

        <div className="glass-card rounded-2xl p-6 border border-white/20 dark:border-gray-700/30">

          <h2 className="text-xl font-bold mb-4 text-center">
            Prediction Result
          </h2>

          <div className="space-y-3">

            <div className="flex justify-between">
              <span className="font-medium">Prediction:</span>

              <span
                className={`font-bold ${
                  result.prediction === 'real'
                    ? 'text-green-500'
                    : 'text-red-500'
                }`}
              >
                {result.prediction}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="font-medium">Confidence:</span>

              <span className="font-bold">
                {result.confidence}%
              </span>
            </div>

          </div>

        </div>
      )}

    </div>
  )
}