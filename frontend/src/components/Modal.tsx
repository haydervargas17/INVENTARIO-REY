import { AnimatePresence, motion } from 'framer-motion'

type ModalProps = {
  open: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
}

export default function Modal({ open, onClose, title, children }: ModalProps) {
  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <motion.div
            className="fixed inset-0 bg-black/40 backdrop-blur-sm"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />

          <motion.div
            className="mx-4 max-h-[88vh] w-full max-w-xl overflow-hidden rounded-lg bg-white shadow-xl"
            initial={{ y: 20, opacity: 0, scale: 0.98 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: 10, opacity: 0 }}
            transition={{ duration: 0.18 }}
          >
            <div className="border-b px-6 py-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">{title}</h3>
                <button
                  onClick={onClose}
                  aria-label="Cerrar"
                  className="grid h-8 w-8 place-items-center rounded-md text-gray-500 hover:bg-gray-100 hover:text-gray-700"
                >
                  X
                </button>
              </div>
            </div>
            <div className="max-h-[72vh] overflow-y-auto p-6">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
