import { createClient } from '@supabase/supabase-js'
// import { Database } from './database.types'
// export const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
// export const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabaseUrl = "https://yjubwgtvyces.supabase.co" //import.meta.env.VITE_SUPABASE_URL
export const supabaseAnonKey = "hjj"//import.meta.env.VITE_SUPABASE_ANON_KEY
export const service_role_key ="ll" //import.meta.env.VITE_GLOB_APP_PWA
const supabaseAdmin = createClient(supabaseUrl, service_role_key, {
  auth: {
    autoRefreshToken: false,
    persistSession: false
  }
})
// Access auth admin api
export const adminAuthClient = supabaseAdmin.auth.admin
export const supabase = createClient(supabaseUrl, supabaseAnonKey)
export const supabaseUrlImage = `${supabaseUrl}/storage/v1/object/public`
