import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://ykmrystcfwjrrgkglyzr.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlrbXJ5c3RjZndqcnJna2dseXpyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5MzQyODIsImV4cCI6MjA4MDUxMDI4Mn0.T4yy_DqaDxilkAW8NMRbYiXiEyQNWknr04TD0sDC_R8'

export const supabase = createClient(supabaseUrl, supabaseKey)
