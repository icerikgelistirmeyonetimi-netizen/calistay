<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
    <header class="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-10">
      <div class="max-w-full mx-auto px-2 sm:px-3 py-3">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-900">EBA DİJİTAL İÇERİK İHTİYAÇ ANALİZİ</h1>
          </div>
          <router-link
            to="/tur-yonetimi"
            class="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-all text-sm font-medium shadow-sm"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Tür Yönetimi
          </router-link>
        </div>
      </div>
    </header>

    <main class="max-w-full mx-auto px-2 sm:px-3 py-4">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-3 border-slate-300 border-t-blue-600"></div>
      </div>

      <div v-else>
        <div class="mb-4">
          <h2 class="text-lg font-semibold text-slate-900">Dersler</h2>
          <p class="text-sm text-slate-600">{{ dersler.length }} ders</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
          <button
            v-for="ders in dersler"
            :key="ders"
            @click="goDersDetay(ders)"
            class="group bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-300 rounded-xl p-4 transition-all shadow-sm hover:shadow-md text-left"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <h3 class="text-sm font-semibold text-slate-900 truncate group-hover:text-blue-600 transition-colors">{{ ders }}</h3>
                <p class="text-xs text-slate-500 mt-1">
                  {{ dersIcerikSayilari[ders] || 0 }} içerik
                </p>
              </div>
              <svg class="w-5 h-5 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all flex-shrink-0 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { supabase } from '../supabase'

export default {
  name: 'HomePage',
  data() {
    return {
      dersler: [],
      dersIcerikSayilari: {},
      loading: true
    }
  },
  async mounted() {
    await this.loadDersler()
  },
  methods: {
    async loadDersler() {
      try {
        const { data, error } = await supabase
          .from('icerik_kayitlari')
          .select('ders_adi')

        if (error) throw error

        // Benzersiz ders adlarını al
        const uniqueDersler = [...new Set(data.map(item => item.ders_adi).filter(Boolean))]
        this.dersler = uniqueDersler.sort()

        // Her ders için içerik sayısını hesapla
        this.dersler.forEach(ders => {
          this.dersIcerikSayilari[ders] = data.filter(item => item.ders_adi === ders).length
        })
      } catch (error) {
        console.error('Dersler yüklenirken hata:', error)
        alert('Dersler yüklenirken bir hata oluştu: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    goDersDetay(dersAdi) {
      this.$router.push({ name: 'dersDetay', params: { dersAdi } })
    }
  }
}
</script>
