import React, { useState, useRef } from 'react'
import { Upload, Loader } from 'lucide-react'
import ResultCard from '../ResultCard'

export default function TextTab() {
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [fileName, setFileName] = useState('')
  const [extractedText, setExtractedText] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0]
    if (!selectedFile) return

    const ext = selectedFile.name.split('.').pop().toLowerCase()

    if (!['txt', 'pdf'].includes(ext)) {
      setError('Please upload .txt or .pdf file only')
      return
    }

    setFile(selectedFile)
    setFileName(selectedFile.name)
    setError('')

    const reader = new FileReader()
    reader.onload = (event) => {
      if (ext === 'txt') {
        const content = event.target?.result
        setExtractedText(content)
        setText(content)
      } else if (ext === 'pdf') {
        setExtractedText('PDF file selected. Text will be extracted on the server when you click "Predict".')
      }
    }

    if (ext === 'txt') {
      reader.readAsText(selectedFile)
    } else {
      reader.readAsArrayBuffer(selectedFile)
    }
  }

  const handlePredict = async () => {
    setError('')

    const textToPredict = text.trim()

    if (!textToPredict && !file) {
      setError('Please enter text or upload a file')
      return
    }

    if (textToPredict && textToPredict.length < 10) {
      setError('Please enter at least 10 characters of text')
      return
    }

    setLoading(true)
    try {
      let response

      if (file) {
        const formData = new FormData()
        formData.append('file', file)

        response = await fetch('/predict-text', {
          method: 'POST',
          body: formData,
        })
      } else {
        response = await fetch('/predict-text', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: textToPredict }),
        })
      }

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
      {/* Manual Text Input */}
      <div>
        <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
          ✍️ Type or Paste Text
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste the news article here..."
          className="w-full h-40 glass-input rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none focus:shadow-lg focus:shadow-purple-500/20"
        />
      </div>

      {/* File Upload */}
      <div>
        <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
          📁 Or Upload a File
        </label>
        <div
          onClick={() => fileInputRef.current?.click()}
          className="border-2 border-dashed border-purple-300 dark:border-purple-600 rounded-xl p-8 text-center cursor-pointer file-upload-hover transition-all duration-300 bg-purple-50/30 dark:bg-purple-900/20"
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".txt,.pdf"
            onChange={handleFileChange}
            className="hidden"
          />
          <div className="flex flex-col items-center gap-3">
            <Upload size={32} className="text-purple-500 mx-auto" />
            <p className="text-purple-600 dark:text-purple-400 font-medium">Click or drag .txt/.pdf file here</p>
            {fileName && <p className="text-gray-600 dark:text-gray-400 text-sm">📄 {fileName}</p>}
          </div>
        </div>
      </div>

      {/* Extracted Text Preview */}
      {extractedText && (
        <div className="bg-green-50/50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl p-4">
          <p className="text-xs font-semibold text-green-700 dark:text-green-400 mb-2 uppercase tracking-wide">
            📖 Extracted Text Preview
          </p>
          <div className="bg-white dark:bg-gray-900 rounded-lg p-3 max-h-32 overflow-y-auto text-sm text-gray-700 dark:text-gray-300 border border-green-200 dark:border-green-800/30">
            {extractedText.substring(0, 300)}
            {extractedText.length > 300 && '...'}
          </div>
        </div>
      )}

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
          'Predict Text'
        )}
      </button>

      {/* Results */}
      {results && (
        <div className="space-y-4 mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          {results.source && (
            <div className="text-xs text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 px-3 py-2 rounded-lg">
              📍 Source: {results.source === 'file' ? `File (${results.file_name})` : 'Manual input'}
            </div>
          )}
          <ResultCard
            title="Text Prediction"
            prediction={results.prediction}
            confidence={results.confidence}
            probabilities={results.probabilities}
            variant="text"
          />
        </div>
      )}
    </div>
  )
}
