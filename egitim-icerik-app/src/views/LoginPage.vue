<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
    <div class="bg-white rounded-xl shadow-lg border border-slate-200 p-8 w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-slate-900 mb-2">EBA Dijital İçerik</h1>
        <p class="text-sm text-slate-600">İhtiyaç Analizi Sistemi</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Kullanıcı Adı</label>
            <input
              v-model="username"
              type="text"
              required
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Kullanıcı adınızı girin"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Şifre</label>
            <input
              v-model="password"
              type="password"
              required
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Şifrenizi girin"
            />
          </div>

          <div v-if="errorMessage" class="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ errorMessage }}</p>
          </div>

          <button
            type="submit"
            class="w-full py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-all shadow-sm"
          >
            Giriş Yap
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { supabase } from '../supabase'

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        // Veritabanından kullanıcıyı kontrol et
        const { data, error } = await supabase
          .from('login')
          .select('*')
          .eq('username', this.username)
          .eq('password', this.password)
          .single()

        if (error || !data) {
          this.errorMessage = 'Kullanıcı adı veya şifre hatalı!'
          setTimeout(() => {
            this.errorMessage = ''
          }, 3000)
          return
        }

        // Başarılı giriş
        localStorage.setItem('isLoggedIn', 'true')
        localStorage.setItem('username', data.username)
        localStorage.setItem('fullName', data.full_name)
        this.$router.push('/')
        
      } catch (error) {
        console.error('Giriş hatası:', error)
        this.errorMessage = 'Bir hata oluştu. Lütfen tekrar deneyin.'
        setTimeout(() => {
          this.errorMessage = ''
        }, 3000)
      }
    }
  }
}
</script>
