'use client'

import { useState, useEffect, useCallback } from 'react'

interface TypeWriterProps {
  words: string[]
  className?: string
  typingSpeed?: number
  deletingSpeed?: number
  pauseDuration?: number
}

export function TypeWriter({
  words,
  className = '',
  typingSpeed = 80,
  deletingSpeed = 40,
  pauseDuration = 2000,
}: TypeWriterProps) {
  const [text, setText] = useState('')
  const [wordIndex, setWordIndex] = useState(0)
  const [isDeleting, setIsDeleting] = useState(false)

  const tick = useCallback(() => {
    const currentWord = words[wordIndex]
    if (isDeleting) {
      setText(currentWord.substring(0, text.length - 1))
    } else {
      setText(currentWord.substring(0, text.length + 1))
    }
  }, [text, wordIndex, isDeleting, words])

  useEffect(() => {
    const currentWord = words[wordIndex]

    let timeout: NodeJS.Timeout

    if (!isDeleting && text === currentWord) {
      timeout = setTimeout(() => setIsDeleting(true), pauseDuration)
    } else if (isDeleting && text === '') {
      setIsDeleting(false)
      setWordIndex((prev) => (prev + 1) % words.length)
    } else {
      timeout = setTimeout(tick, isDeleting ? deletingSpeed : typingSpeed)
    }

    return () => clearTimeout(timeout)
  }, [text, isDeleting, wordIndex, words, tick, typingSpeed, deletingSpeed, pauseDuration])

  return (
    <span className={className}>
      {text}
      <span className="animate-pulse text-violet-400">|</span>
    </span>
  )
}
