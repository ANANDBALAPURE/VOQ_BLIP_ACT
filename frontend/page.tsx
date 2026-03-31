'use client'

import { useState, useCallback, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { 
  Upload, 
  Image as ImageIcon, 
  Sparkles, 
  Send, 
  Loader2, 
  Trash2, 
  Download,
  Eye,
  MessageCircleQuestion,
  Zap,
  Camera,
  Wand2,
  RotateCcw
} from 'lucide-react'

// Sample questions for users
const sampleQuestions = [
  "What is in the image?",
  "How many objects are there?",
  "Describe the scene.",
  "What colors can you see?",
  "Is there a person in the image?",
  "What is the main subject?",
  "Describe the background.",
  "What time of day is it?"
]

// Gradient color schemes
const gradients = {
  primary: 'from-violet-500 via-purple-500 to-fuchsia-500',
  secondary: 'from-cyan-500 via-blue-500 to-indigo-500',
  accent: 'from-pink-500 via-rose-500 to-red-500',
  success: 'from-emerald-500 via-teal-500 to-cyan-500',
  warm: 'from-orange-500 via-amber-500 to-yellow-500'
}

export default function VQAFrontend() {
  const [image, setImage] = useState<string | null>(null)
  const [imageName, setImageName] = useState<string>('')
  const [question, setQuestion] = useState<string>('')
  const [answer, setAnswer] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [history, setHistory] = useState<Array<{ question: string; answer: string }>>([])
  const [isDragging, setIsDragging] = useState<boolean>(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Handle file selection
  const handleFileSelect = useCallback((file: File) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setImage(e.target?.result as string)
        setImageName(file.name)
        setAnswer('')
        setHistory([])
      }
      reader.readAsDataURL(file)
    }
  }, [])

  // Handle drag events
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFileSelect(file)
  }, [handleFileSelect])

  // Handle question submission
  const handleSubmit = async () => {
    if (!image || !question.trim() || isLoading) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/vqa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image, question })
      })
      
      const data = await response.json()
      
      if (data.answer) {
        setAnswer(data.answer)
        setHistory(prev => [...prev, { question, answer: data.answer }])
      } else {
        setAnswer('Unable to process the question. Please try again.')
      }
    } catch (error) {
      setAnswer('An error occurred. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  // Clear everything
  const handleClear = () => {
    setImage(null)
    setImageName('')
    setQuestion('')
    setAnswer('')
    setHistory([])
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  // Handle sample question click
  const handleSampleQuestion = (q: string) => {
    setQuestion(q)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/30 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-1/2 -left-40 w-80 h-80 bg-pink-500/30 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute -bottom-40 right-1/3 w-80 h-80 bg-cyan-500/30 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/4 right-1/4 w-60 h-60 bg-violet-500/20 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '0.5s' }} />
      </div>

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMtOS45NDEgMC0xOCA4LjA1OS0xOCAxOHM4LjA1OSAxOCAxOCAxOCAxOC04LjA1OSAxOC0xOC04LjA1OS0xOC0xOC0xOHptMCAzMmMtNy43MzIgMC0xNC02LjI2OC0xNC0xNHM2LjI2OC0xNCAxNC0xNCAxNCA2LjI2OCAxNCAxNC02LjI2OCAxNC0xNCAxNHoiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iLjAyIi8+PC9nPjwvc3ZnPg==')] opacity-20" />

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className={`p-3 rounded-2xl bg-gradient-to-r ${gradients.primary} shadow-lg shadow-purple-500/30`}>
              <Eye className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent">
              Visual Question Answering
            </h1>
          </div>
          <p className="text-lg text-purple-200/80 max-w-2xl mx-auto">
            Powered by <span className="font-semibold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">BLIP Model</span> - Ask questions about any image and get instant AI-powered answers
          </p>
          
          {/* Feature Badges */}
          <div className="flex flex-wrap justify-center gap-3 mt-6">
            <Badge className="bg-gradient-to-r from-violet-600 to-purple-600 text-white border-0 px-4 py-1.5 shadow-lg shadow-purple-500/20">
              <Sparkles className="w-3.5 h-3.5 mr-1.5" /> AI-Powered
            </Badge>
            <Badge className="bg-gradient-to-r from-cyan-600 to-blue-600 text-white border-0 px-4 py-1.5 shadow-lg shadow-cyan-500/20">
              <Zap className="w-3.5 h-3.5 mr-1.5" /> Fast Processing
            </Badge>
            <Badge className="bg-gradient-to-r from-pink-600 to-rose-600 text-white border-0 px-4 py-1.5 shadow-lg shadow-pink-500/20">
              <Camera className="w-3.5 h-3.5 mr-1.5" /> Image Understanding
            </Badge>
          </div>
        </header>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Image Upload & Display */}
          <div className="space-y-6">
            {/* Image Upload Card */}
            <Card className="bg-white/5 backdrop-blur-xl border-white/10 shadow-2xl shadow-purple-500/10 overflow-hidden">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-white">
                  <div className={`p-2 rounded-lg bg-gradient-to-r ${gradients.secondary}`}>
                    <Upload className="w-5 h-5 text-white" />
                  </div>
                  Upload Image
                </CardTitle>
                <CardDescription className="text-purple-200/60">
                  Drag and drop or click to upload an image
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 cursor-pointer ${
                    isDragging 
                      ? `border-purple-400 bg-purple-500/20 scale-[1.02]` 
                      : image 
                        ? 'border-green-500/50 bg-green-500/10' 
                        : 'border-white/20 hover:border-purple-400/50 hover:bg-white/5'
                  }`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                  />
                  
                  {image ? (
                    <div className="relative group">
                      <img
                        src={image}
                        alt="Uploaded"
                        className="max-h-80 mx-auto rounded-xl shadow-2xl shadow-purple-500/20 transition-transform duration-300 group-hover:scale-[1.02]"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4">
                        <p className="text-white text-sm font-medium px-3 py-1 bg-black/40 rounded-full">
                          {imageName}
                        </p>
                      </div>
                      <div className="absolute -top-2 -right-2">
                        <div className="p-1.5 bg-green-500 rounded-full shadow-lg animate-pulse">
                          <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="py-8">
                      <div className={`w-20 h-20 mx-auto mb-4 rounded-2xl bg-gradient-to-r ${gradients.primary} flex items-center justify-center shadow-lg shadow-purple-500/30 transition-transform duration-300 ${isDragging ? 'scale-110' : ''}`}>
                        <ImageIcon className="w-10 h-10 text-white" />
                      </div>
                      <p className="text-lg font-medium text-white mb-2">
                        {isDragging ? 'Drop your image here!' : 'Drag & drop your image'}
                      </p>
                      <p className="text-purple-200/60 text-sm mb-4">
                        or click to browse from your device
                      </p>
                      <Badge variant="secondary" className="bg-white/10 text-purple-200 border-white/20">
                        Supports: JPG, PNG, GIF, WebP
                      </Badge>
                    </div>
                  )}
                </div>

                {image && (
                  <div className="mt-4 flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleClear}
                      className="flex-1 bg-white/5 border-white/20 text-white hover:bg-red-500/20 hover:border-red-500/50 hover:text-red-200"
                    >
                      <Trash2 className="w-4 h-4 mr-2" /> Clear
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        const link = document.createElement('a')
                        link.download = imageName || 'image.png'
                        link.href = image
                        link.click()
                      }}
                      className="flex-1 bg-white/5 border-white/20 text-white hover:bg-purple-500/20 hover:border-purple-500/50 hover:text-purple-200"
                    >
                      <Download className="w-4 h-4 mr-2" /> Download
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Q&A History Card */}
            {history.length > 0 && (
              <Card className="bg-white/5 backdrop-blur-xl border-white/10 shadow-2xl shadow-purple-500/10">
                <CardHeader className="pb-2">
                  <CardTitle className="flex items-center gap-2 text-white">
                    <div className={`p-2 rounded-lg bg-gradient-to-r ${gradients.warm}`}>
                      <MessageCircleQuestion className="w-5 h-5 text-white" />
                    </div>
                    Q&A History
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                    {history.map((item, index) => (
                      <div
                        key={index}
                        className="p-3 rounded-xl bg-white/5 border border-white/10 hover:border-purple-500/30 transition-colors"
                      >
                        <p className="text-sm text-purple-200/80 mb-1">
                          <span className="font-medium text-purple-300">Q:</span> {item.question}
                        </p>
                        <p className="text-sm text-emerald-300">
                          <span className="font-medium text-emerald-400">A:</span> {item.answer}
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Question & Answer */}
          <div className="space-y-6">
            {/* Question Input Card */}
            <Card className="bg-white/5 backdrop-blur-xl border-white/10 shadow-2xl shadow-purple-500/10">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-white">
                  <div className={`p-2 rounded-lg bg-gradient-to-r ${gradients.accent}`}>
                    <MessageCircleQuestion className="w-5 h-5 text-white" />
                  </div>
                  Ask a Question
                </CardTitle>
                <CardDescription className="text-purple-200/60">
                  Type your question about the uploaded image
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative">
                  <Textarea
                    placeholder="e.g., What is in the image? How many objects are there?"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault()
                        handleSubmit()
                      }
                    }}
                    className="min-h-[100px] bg-white/5 border-white/20 text-white placeholder:text-purple-200/40 focus:border-purple-500 focus:ring-purple-500/20 resize-none"
                    disabled={!image || isLoading}
                  />
                  <div className="absolute bottom-3 right-3 text-xs text-purple-200/40">
                    Press Enter to submit
                  </div>
                </div>

                <Button
                  onClick={handleSubmit}
                  disabled={!image || !question.trim() || isLoading}
                  className={`w-full py-6 text-lg font-semibold bg-gradient-to-r ${gradients.primary} hover:opacity-90 transition-all duration-300 shadow-lg shadow-purple-500/30 disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Wand2 className="w-5 h-5 mr-2" />
                      Get Answer
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Sample Questions Card */}
            <Card className="bg-white/5 backdrop-blur-xl border-white/10 shadow-2xl shadow-purple-500/10">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-white text-base">
                  <Sparkles className="w-5 h-5 text-yellow-400" />
                  Sample Questions
                </CardTitle>
                <CardDescription className="text-purple-200/60 text-sm">
                  Click on a question to use it
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {sampleQuestions.map((q, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      onClick={() => handleSampleQuestion(q)}
                      disabled={!image || isLoading}
                      className="bg-white/5 border-white/20 text-purple-200 hover:bg-purple-500/20 hover:border-purple-500/50 hover:text-white disabled:opacity-50 transition-all duration-200"
                    >
                      {q}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Answer Display Card */}
            <Card className={`bg-white/5 backdrop-blur-xl border-white/10 shadow-2xl shadow-purple-500/10 ${answer ? 'ring-2 ring-emerald-500/30' : ''}`}>
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-white">
                  <div className={`p-2 rounded-lg bg-gradient-to-r ${gradients.success}`}>
                    <Sparkles className="w-5 h-5 text-white" />
                  </div>
                  Answer
                </CardTitle>
              </CardHeader>
              <CardContent>
                {answer ? (
                  <div className="p-4 rounded-xl bg-gradient-to-r from-emerald-500/10 to-cyan-500/10 border border-emerald-500/30">
                    <p className="text-lg text-white leading-relaxed">{answer}</p>
                  </div>
                ) : (
                  <div className="py-12 text-center">
                    <div className={`w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-r ${gradients.success} flex items-center justify-center opacity-50`}>
                      <Sparkles className="w-8 h-8 text-white" />
                    </div>
                    <p className="text-purple-200/40">
                      Upload an image and ask a question to see the answer
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center">
          <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 backdrop-blur-sm border border-white/10">
            <div className={`p-1.5 rounded-lg bg-gradient-to-r ${gradients.primary}`}>
              <Eye className="w-4 h-4 text-white" />
            </div>
            <span className="text-purple-200/60 text-sm">
              Visual Question Answering powered by <span className="font-semibold text-white">BLIP</span> & <span className="font-semibold text-white">Z.ai</span>
            </span>
          </div>
        </footer>
      </div>

      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: linear-gradient(to bottom, #a855f7, #ec4899);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: linear-gradient(to bottom, #9333ea, #db2777);
        }
      `}</style>
    </div>
  )
}
