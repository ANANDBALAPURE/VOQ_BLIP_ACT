import { NextRequest, NextResponse } from 'next/server'
import ZAI from 'z-ai-web-dev-sdk'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { image, question } = body

    if (!image || !question) {
      return NextResponse.json(
        { error: 'Image and question are required' },
        { status: 400 }
      )
    }

    // Initialize ZAI
    const zai = await ZAI.create()

    // Use the VLM (Vision Language Model) to answer questions about the image
    const completion = await zai.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: `You are a helpful Visual Question Answering assistant. Your task is to analyze images and answer questions about them accurately and concisely. 
          
When answering questions:
1. Be specific and direct
2. Describe what you actually see in the image
3. If counting objects, provide an accurate count
4. If describing colors, be specific about what you observe
5. Keep answers concise but informative
6. If you cannot determine something with certainty, say so`
        },
        {
          role: 'user',
          content: [
            {
              type: 'image_url',
              image_url: {
                url: image
              }
            },
            {
              type: 'text',
              text: question
            }
          ]
        }
      ],
      temperature: 0.7,
      max_tokens: 500
    })

    const answer = completion.choices[0]?.message?.content || 'Unable to process the question.'

    return NextResponse.json({ answer })
    
  } catch (error: any) {
    console.error('VQA API Error:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to process the question' },
      { status: 500 }
    )
  }
}
