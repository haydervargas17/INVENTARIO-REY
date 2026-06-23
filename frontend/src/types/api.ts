export type UserRole = 'system_admin' | 'admin'

export type AuthUser = {
  id: string
  username: string
  full_name: string
  role: UserRole
}

export type ApiResponse<T> = {
  success: boolean
  message: string
  data: T
  errors: unknown
}

export type Color = {
  id: string
  name: string
  normalized_name: string
  is_active: boolean
}

export type Product = {
  id: string
  reference: string
  name: string
  brand: string
  description: string
  photo_url: string
  cloudinary_public_id: string | null
  current_purchase_price: number
  current_sale_price: number
  is_active: boolean
}

export type InventoryItem = {
  id: string
  product: Product
  size: number
  color_signature: string
  colors: Color[]
  location_type: 'WAREHOUSE' | 'STORE'
  location_detail: string
  quantity: number
  low_stock_threshold: number
  is_low_stock: boolean
}

export type InventoryMovement = {
  id: string
  movement_type: 'IN' | 'OUT' | 'ADJUSTMENT'
  quantity_delta: number
  previous_quantity: number
  new_quantity: number
  purchase_unit_price: number | null
  sale_unit_price: number | null
  reason: string
  created_at: string
  user_id: string
  username: string | null
  user_full_name: string | null
}
