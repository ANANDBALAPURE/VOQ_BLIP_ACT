# VQA Frontend - Interactive Web Application

A beautiful, modern frontend for the Visual Question Answering system built with Next.js, React, and Tailwind CSS.

## Features

- 🎨 **Beautiful Gradient UI** - Modern, colorful design with animated backgrounds
- 📷 **Drag & Drop Image Upload** - Easy image upload with preview
- 💬 **Interactive Q&A** - Ask questions and get instant AI answers
- 📝 **Sample Questions** - Quick-access sample questions for testing
- 📜 **History Tracking** - Keep track of your Q&A session
- ⚡ **Fast Processing** - Powered by AI for quick responses

## Quick Start

### Prerequisites
- Node.js 18+
- npm or bun

### Installation

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install
# or
bun install

# Run development server
npm run dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Main VQA page
│   │   ├── layout.tsx        # Root layout
│   │   ├── globals.css       # Global styles
│   │   └── api/
│   │       └── vqa/
│   │           └── route.ts  # VQA API endpoint
│   └── components/
│       └── ui/               # UI components (shadcn/ui)
├── public/                   # Static assets
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Usage

1. **Upload Image**: Click or drag & drop an image onto the upload area
2. **Ask Question**: Type your question about the image
3. **Get Answer**: Click "Get Answer" to receive AI-powered response
4. **View History**: See all your Q&A interactions in the history panel

## Technology Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **AI Backend**: z-ai-web-dev-sdk (VLM)

## Customization

### Changing Gradient Colors

Edit the `gradients` object in `page.tsx`:

```typescript
const gradients = {
  primary: 'from-violet-500 via-purple-500 to-fuchsia-500',
  secondary: 'from-cyan-500 via-blue-500 to-indigo-500',
  accent: 'from-pink-500 via-rose-500 to-red-500',
  success: 'from-emerald-500 via-teal-500 to-cyan-500',
  warm: 'from-orange-500 via-amber-500 to-yellow-500'
}
```

### Adding Sample Questions

Edit the `sampleQuestions` array in `page.tsx`:

```typescript
const sampleQuestions = [
  "What is in the image?",
  "How many objects are there?",
  // Add your custom questions here
]
```

## API Integration

The frontend connects to the `/api/vqa` endpoint which processes images and questions using the AI model.

### API Request Format

```typescript
POST /api/vqa
Content-Type: application/json

{
  "image": "data:image/png;base64,...",  // Base64 encoded image
  "question": "What is in the image?"
}
```

### API Response Format

```typescript
{
  "answer": "The image shows..."
}
```

## License

MIT License
