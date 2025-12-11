<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
    <header class="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-10">
      <div class="max-w-full mx-auto px-2 sm:px-3 py-3">
        <div class="flex items-center gap-4">
          <button
            @click="$router.push('/')"
            class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div class="flex-1">
            <h1 class="text-2xl font-bold text-slate-900">{{ dersAdi }}</h1>
            <p class="text-sm text-slate-600 mt-0.5">{{ toplamIcerik }} içerik</p>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-full mx-auto px-2 sm:px-3 py-4">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-3 border-slate-300 border-t-blue-600"></div>
      </div>

      <div v-else>
        <div v-for="(icerikler, sinif) in sinifBazindaIcerikler" :key="sinif" class="mb-4">
          <SinifTablosu :sinif="sinif" :icerikler="icerikler" />
        </div>

        <div v-if="Object.keys(sinifBazindaIcerikler).length === 0" class="text-center py-12">
          <div class="text-slate-400 text-sm">Bu ders için içerik bulunamadı.</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { supabase } from '../supabase'
import SinifTablosu from '../components/SinifTablosu.vue'

export default {
  name: 'DersDetay',
  components: {
    SinifTablosu
  },
  props: {
    dersAdi: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      icerikler: [],
      loading: true
    }
  },
  computed: {
    sinifBazindaIcerikler() {
      const grouped = {}
      this.icerikler.forEach(icerik => {
        const sinif = icerik.sinif || 'Belirtilmemiş'
        if (!grouped[sinif]) {
          grouped[sinif] = []
        }
        grouped[sinif].push(icerik)
      })
      
      // Sınıfları sırala
      const sorted = {}
      Object.keys(grouped).sort((a, b) => {
        if (a === 'Belirtilmemiş') return 1
        if (b === 'Belirtilmemiş') return -1
        return a.localeCompare(b, 'tr')
      }).forEach(key => {
        sorted[key] = grouped[key]
      })
      
      return sorted
    },
    toplamIcerik() {
      return this.icerikler.length
    }
  },
  async mounted() {
    await this.loadIcerikler()
  },
  methods: {
    async loadIcerikler() {
      try {
        const { data, error } = await supabase
          .from('icerik_kayitlari')
          .select('*')
          .eq('ders_adi', this.dersAdi)
          .order('sinif', { ascending: true })

        if (error) throw error

        this.icerikler = data || []
      } catch (error) {
        console.error('İçerikler yüklenirken hata:', error)
        alert('İçerikler yüklenirken bir hata oluştu: ' + error.message)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
