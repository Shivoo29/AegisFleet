import { useEffect } from 'react'
import { AnimatePresence, animate, motion, useMotionValue, useTransform } from 'motion/react'

export const EASE_OUT = [0.2, 0, 0, 1] as const
export const SPRING = { type: 'spring', duration: 0.35, bounce: 0 } as const

/** Staged entrance for a view's first load: children rise 12px out of a 4px blur, 100ms apart. */
export const stage = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
}
export const rise = {
  hidden: { opacity: 0, y: 12, filter: 'blur(4px)' },
  show: { opacity: 1, y: 0, filter: 'blur(0px)', transition: { duration: 0.3, ease: EASE_OUT } },
}

/** A number that counts to its new value, so a change on screen reads as a change. */
export function Ticker({ value, format }: { value: number; format: (n: number) => string }) {
  const mv = useMotionValue(value)
  const text = useTransform(mv, format)
  useEffect(() => {
    const controls = animate(mv, value, { duration: 0.6, ease: EASE_OUT })
    return () => controls.stop()
  }, [mv, value])
  return <motion.span>{text}</motion.span>
}

/** Words that swap (Intact -> Broken) cross-fade through a blur instead of jumping. */
export function SwapText({ text }: { text: string }) {
  return (
    <AnimatePresence mode="popLayout" initial={false}>
      <motion.span
        key={text}
        style={{ display: 'inline-block' }}
        initial={{ opacity: 0, scale: 0.9, filter: 'blur(4px)' }}
        animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
        exit={{ opacity: 0, filter: 'blur(4px)', transition: { duration: 0.15 } }}
        transition={SPRING}
      >
        {text}
      </motion.span>
    </AnimatePresence>
  )
}

/** Rows that arrive or leave a live list: enter from a blur, exit shorter and smaller. */
export const row = {
  initial: { opacity: 0, y: -12, filter: 'blur(4px)' },
  animate: { opacity: 1, y: 0, filter: 'blur(0px)', transition: { duration: 0.3, ease: EASE_OUT } },
  exit: { opacity: 0, y: -12, filter: 'blur(4px)', transition: { duration: 0.15, ease: EASE_OUT } },
}
