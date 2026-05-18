import React, { useState, useRef } from 'react'
import { Upload, Loader } from 'lucide-react'
import ResultCard from '../ResultCard'

export default function ImageTab() {
  const [image, setImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)

  const handleImageChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      setImage(file)
      const reader = new FileReader()
      reader.onload = (event) => {
        setImagePreview(event.target?.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handlePredict = async () => {
    setError('')

    if (!image) {
      setError('Please upload an image')
      return
    }

    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', image)

      const response = await fetch('/predict-image', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (data.error) {
        setError(data.error)
      } else {
        setResults(data)
      }
    } catch (err) {
      setError(err.message || 'An error occurred during prediction')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Image upload */}
      <div>
        <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
          📷 Upload Image
        </label>
        <div
          onClick={() => fileInputRef.current?.click()}
          className="relative border-2 border-dashed border-purple-300 dark:border-purple-600 rounded-xl p-8 text-center cursor-pointer file-upload-hover transition-all duration-300 bg-purple-50/30 dark:bg-purple-900/20"
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="hidden"
          />
          {imagePreview ? (
            <img src={imagePreview} alt="Preview" className="max-h-48 mx-auto rounded-lg shadow-md" />
          ) : (
            <div className="flex flex-col items-center gap-3">
              <Upload size={32} className="text-purple-500 mx-auto" />
              <p className="text-purple-600 dark:text-purple-400 font-medium">Click or drag image here</p>
            </div>
          )}
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg px-4 py-3 text-red-700 dark:text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* Predict button */}
      <button
        onClick={handlePredict}
        disabled={loading}
        className="w-full gradient-button text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
      >
        {loading ? (
          <>
            <Loader size={20} className="animate-spin" />
            Analyzing...
          </>
        ) : (
          'Predict Image'
        )}
      </button>

      {/* Results */}
      {results && (
        <div className="space-y-4 mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <ResultCard
            title="Image Prediction"
            prediction={results.prediction}
            confidence={results.confidence}
            probabilities={results.probabilities}
            variant="image"
          />
        </div>
      )}
    </div>
  )
}
