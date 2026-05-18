import React, { useState, useRef } from 'react'
import { Upload, Loader } from 'lucide-react'
import ResultCard from '../ResultCard'

export default function MultimodalTab() {

  const [image, setImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)

  const [audio, setAudio] = useState(null)

  const [text, setText] = useState('')

  const [results, setResults] = useState(null)

  const [loading, setLoading] = useState(false)

  const [error, setError] = useState('')

  const fileInputRef = useRef(null)

  const audioInputRef = useRef(null)

  // Image Upload
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

  // Audio Upload
  const handleAudioChange = (e) => {

    const file = e.target.files?.[0]

    if (file) {
      setAudio(file)
    }
  }

  // Predict
  const handlePredict = async () => {

    setError('')

    if (!image) {
      setError('Please upload an image')
      return
    }

    if (!audio) {
      setError('Please upload an audio file')
      return
    }

    if (text.trim().length < 10) {
      setError('Please enter at least 10 characters of text')
      return
    }

    setLoading(true)

    try {

      const formData = new FormData()

      formData.append('image', image)

      formData.append('audio', audio)

      formData.append('text', text)

      const response = await fetch(
        '/predict-multimodal',
        {
          method: 'POST',
          body: formData,
        }
      )

      const data = await response.json()

      if (data.error) {

        setError(data.error)

      } else {

        setResults(data)
      }

    } catch (err) {

      setError(
        err.message ||
        'An error occurred during prediction'
      )

    } finally {

      setLoading(false)
    }
  }

  return (

    <div className="space-y-6 animate-fade-in">

      {/* IMAGE */}
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

            <img
              src={imagePreview}
              alt="Preview"
              className="max-h-48 mx-auto rounded-lg shadow-md"
            />

          ) : (

            <div className="flex flex-col items-center gap-3">

              <Upload
                size={32}
                className="text-purple-500 mx-auto"
              />

              <p className="text-purple-600 dark:text-purple-400 font-medium">

                Click or drag image here

              </p>

            </div>
          )}

        </div>

      </div>

      {/* AUDIO */}
      <div>

        <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">

          🎤 Upload Audio

        </label>

        <div
          onClick={() => audioInputRef.current?.click()}
          className="relative border-2 border-dashed border-purple-300 dark:border-purple-600 rounded-xl p-6 text-center cursor-pointer transition-all duration-300 bg-purple-50/30 dark:bg-purple-900/20"
        >

          <input
            ref={audioInputRef}
            type="file"
            accept=".wav,.mp3"
            onChange={handleAudioChange}
            className="hidden"
          />

          <div className="flex flex-col items-center gap-3">

            <Upload
              size={28}
              className="text-purple-500 mx-auto"
            />

            <p className="text-purple-600 dark:text-purple-400 font-medium">

              {audio
                ? audio.name
                : 'Click or drag audio here'}

            </p>

          </div>

        </div>

      </div>

      {/* TEXT */}
      <div>

        <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">

          ✍️ News Text

        </label>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste the news article here..."
          className="w-full h-32 glass-input rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none"
        />

      </div>

      {/* ERROR */}
      {error && (

        <div className="bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg px-4 py-3 text-red-700 dark:text-red-300 text-sm">

          {error}

        </div>
      )}

      {/* BUTTON */}
      <button
        onClick={handlePredict}
        disabled={loading}
        className="w-full gradient-button text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
      >

        {loading ? (

          <>
            <Loader
              size={20}
              className="animate-spin"
            />

            Analyzing...

          </>

        ) : (

          'Predict Multimodal'
        )}

      </button>

      {/* RESULTS */}
      {results && (

        <div className="space-y-4 mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">

          {/* Image */}
          <ResultCard
            title="Image Analysis"
            prediction={results.image_prediction}
            confidence={results.image_confidence}
            probabilities={results.image_probabilities}
            variant="image"
          />

          {/* Text */}
          <ResultCard
            title="Text Analysis"
            prediction={results.text_prediction}
            confidence={results.text_confidence}
            probabilities={results.text_probabilities}
            variant="text"
          />

          {/* Audio */}
          {/* Audio */}
<ResultCard
  title="Audio Analysis"
  prediction={results.audio_prediction}
  confidence={results.audio_confidence}
  probabilities={results.audio_probabilities}
  variant="audio"
/>

          {/* Final */}
          <div className="bg-gradient-to-r from-purple-600 to-purple-700 dark:from-purple-700 dark:to-purple-800 rounded-xl p-6 text-white shadow-lg">

            <h3 className="text-sm font-semibold text-purple-100 mb-2 uppercase tracking-wide">

              Final Result

            </h3>

            <div className="text-3xl font-bold mb-3 capitalize">

              {results.final_result}

            </div>

            <div className="text-sm text-purple-100 mb-4">

              Confidence:
              {' '}
              {results.final_confidence}%

            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 text-sm">

              <strong>Analysis:</strong>
              {' '}
              {results.reasoning}

            </div>

          </div>

        </div>
      )}

    </div>
  )
}