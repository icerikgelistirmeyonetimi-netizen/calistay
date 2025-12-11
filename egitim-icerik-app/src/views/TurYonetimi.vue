<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-900">Tür Yönetimi</h1>
            <p class="text-sm text-slate-600 mt-0.5">İçerik türleri ve alt türler</p>
          </div>
          <router-link
            to="/"
            class="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-all text-sm font-medium shadow-sm"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Ana Sayfa
          </router-link>
        </div>
      </div>
    </header>

    <div class="max-w-full mx-auto px-2 sm:px-3 py-4">
      <!-- Yeni Tür Ekleme -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-6">
        <div class="flex gap-3">
          <input
            v-model="yeniTur"
            type="text"
            placeholder="Yeni tür adı..."
            class="flex-1 px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            @keyup.enter="turEkle"
          />
          <button
            @click="turEkle"
            :disabled="!yeniTur.trim()"
            class="px-5 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-all shadow-sm"
          >
            + Tür Ekle
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="yukleniyor" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-3 border-slate-300 border-t-blue-600"></div>
      </div>

      <!-- Türler Grid -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div
          v-for="tur in turler"
          :key="tur.id"
          class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-all"
        >
          <!-- Tür Başlığı -->
          <div class="bg-gradient-to-r from-slate-800 to-slate-700 px-4 py-3">
            <div v-if="duzenleniyorTur === tur.id" class="flex items-center gap-2">
              <input
                v-model="duzenleniyorTurAdi"
                type="text"
                class="flex-1 px-3 py-1.5 text-sm border border-slate-300 rounded-lg"
                @keyup.enter="turGuncelle(tur)"
                @keyup.esc="duzenleniyorTur = null"
              />
              <button
                @click="turGuncelle(tur)"
                class="px-3 py-1.5 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700"
              >
                ✓
              </button>
              <button
                @click="duzenleniyorTur = null"
                class="px-3 py-1.5 bg-slate-600 text-white text-sm rounded-lg hover:bg-slate-700"
              >
                ✕
              </button>
            </div>
            <div v-else class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <h2 class="text-base font-semibold text-white">{{ tur.icerik_turu }}</h2>
                <span class="text-xs text-slate-300 bg-slate-600/50 px-2 py-0.5 rounded-full">
                  {{ altTurlerByTur[tur.id]?.length || 0 }}
                </span>
              </div>
              <div class="flex gap-1.5">
                <button
                  @click="turDuzenleBaslat(tur)"
                  class="p-1.5 text-white/80 hover:text-white hover:bg-white/10 rounded transition-all"
                  title="Düzenle"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="turSil(tur)"
                  class="p-1.5 text-white/80 hover:text-red-300 hover:bg-red-500/20 rounded transition-all"
                  title="Sil"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Alt Tür Ekleme -->
          <div class="px-4 py-2.5 bg-slate-50 border-b border-slate-200">
            <div class="flex gap-2">
              <input
                v-model="yeniAltTur[tur.id]"
                type="text"
                placeholder="Alt tür adı..."
                class="flex-1 px-3 py-1.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                @keyup.enter="altTurEkle(tur.id)"
              />
              <input
                v-model="yeniAltTurAciklama[tur.id]"
                type="text"
                placeholder="Açıklama..."
                class="flex-1 px-3 py-1.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                @keyup.enter="altTurEkle(tur.id)"
              />
              <button
                @click="altTurEkle(tur.id)"
                :disabled="!yeniAltTur[tur.id]?.trim()"
                class="px-3 py-1.5 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-all"
              >
                +
              </button>
            </div>
          </div>

          <!-- Alt Türler -->
          <div class="p-3 max-h-64 overflow-y-auto">
            <div v-if="!altTurlerByTur[tur.id]?.length" class="text-center py-6 text-slate-400 text-sm">
              Alt tür yok
            </div>
            <div v-else class="space-y-1.5">
              <div
                v-for="altTur in altTurlerByTur[tur.id]"
                :key="altTur.id"
                class="group flex items-center justify-between p-2.5 bg-slate-50 rounded-lg hover:bg-slate-100 transition-all"
              >
                <div class="flex-1 min-w-0">
                  <template v-if="duzenleniyorAltTur === altTur.id">
                    <div class="flex gap-2">
                      <input
                        v-model="duzenleniyorAltTurAdi"
                        type="text"
                        class="flex-1 px-2 py-1 text-sm border border-slate-300 rounded"
                        @keyup.enter="altTurGuncelle(altTur)"
                        @keyup.esc="duzenleniyorAltTur = null"
                      />
                      <input
                        v-model="duzenleniyorAltTurAciklama"
                        type="text"
                        placeholder="Açıklama"
                        class="flex-1 px-2 py-1 text-sm border border-slate-300 rounded"
                        @keyup.enter="altTurGuncelle(altTur)"
                        @keyup.esc="duzenleniyorAltTur = null"
                      />
                      <button
                        @click="altTurGuncelle(altTur)"
                        class="px-2 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700"
                      >
                        ✓
                      </button>
                      <button
                        @click="duzenleniyorAltTur = null"
                        class="px-2 py-1 bg-slate-600 text-white text-xs rounded hover:bg-slate-700"
                      >
                        ✕
                      </button>
                    </div>
                  </template>
                  <template v-else>
                    <div class="text-sm font-medium text-slate-800 truncate">{{ altTur.alt_tur_adi }}</div>
                    <div v-if="altTur.aciklama" class="text-xs text-slate-500 truncate mt-0.5">
                      {{ altTur.aciklama }}
                    </div>
                  </template>
                </div>
                <div v-if="duzenleniyorAltTur !== altTur.id" class="flex gap-1 ml-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    @click="altTurDuzenleBaslat(altTur)"
                    class="p-1.5 text-slate-600 hover:text-blue-600 hover:bg-blue-50 rounded transition-all"
                    title="Düzenle"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="altTurSil(altTur)"
                    class="p-1.5 text-slate-600 hover:text-red-600 hover:bg-red-50 rounded transition-all"
                    title="Sil"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { supabase } from '../supabase'

export default {
  name: 'TurYonetimi',
  data() {
    return {
      yukleniyor: true,
      turler: [],
      altTurler: [],
      yeniTur: '',
      yeniAltTur: {},
      yeniAltTurAciklama: {},
      duzenleniyorTur: null,
      duzenleniyorTurAdi: '',
      duzenleniyorAltTur: null,
      duzenleniyorAltTurAdi: '',
      duzenleniyorAltTurAciklama: ''
    }
  },
  computed: {
    altTurlerByTur() {
      const grouped = {}
      this.altTurler.forEach(altTur => {
        if (!grouped[altTur.icerik_turu_id]) {
          grouped[altTur.icerik_turu_id] = []
        }
        grouped[altTur.icerik_turu_id].push(altTur)
      })
      return grouped
    }
  },
  async mounted() {
    await this.verileriYukle()
  },
  methods: {
    async verileriYukle() {
      try {
        this.yukleniyor = true

        // Türleri yükle
        const { data: turler, error: turlerError } = await supabase
          .from('icerik_turleri')
          .select('*')
          .order('icerik_turu')

        if (turlerError) throw turlerError
        this.turler = turler

        // Alt türleri yükle
        const { data: altTurler, error: altTurlerError } = await supabase
          .from('icerik_alt_turleri')
          .select('*')
          .order('alt_tur_adi')

        if (altTurlerError) throw altTurlerError
        this.altTurler = altTurler

      } catch (error) {
        console.error('Veriler yüklenirken hata:', error)
        alert('Veriler yüklenirken bir hata oluştu: ' + error.message)
      } finally {
        this.yukleniyor = false
      }
    },

    async turEkle() {
      if (!this.yeniTur.trim()) return

      try {
        const { data, error } = await supabase
          .from('icerik_turleri')
          .insert([{ icerik_turu: this.yeniTur.trim() }])
          .select()

        if (error) throw error

        this.turler.push(data[0])
        this.turler.sort((a, b) => a.icerik_turu.localeCompare(b.icerik_turu, 'tr'))
        this.yeniTur = ''
        alert('Tür başarıyla eklendi!')
      } catch (error) {
        console.error('Tür eklenirken hata:', error)
        alert('Tür eklenirken bir hata oluştu: ' + error.message)
      }
    },

    turDuzenleBaslat(tur) {
      this.duzenleniyorTur = tur.id
      this.duzenleniyorTurAdi = tur.icerik_turu
    },

    async turGuncelle(tur) {
      if (!this.duzenleniyorTurAdi.trim()) return

      try {
        const { error } = await supabase
          .from('icerik_turleri')
          .update({ icerik_turu: this.duzenleniyorTurAdi.trim() })
          .eq('id', tur.id)

        if (error) throw error

        tur.icerik_turu = this.duzenleniyorTurAdi.trim()
        this.duzenleniyorTur = null
        this.turler.sort((a, b) => a.icerik_turu.localeCompare(b.icerik_turu, 'tr'))
        alert('Tür başarıyla güncellendi!')
      } catch (error) {
        console.error('Tür güncellenirken hata:', error)
        alert('Tür güncellenirken bir hata oluştu: ' + error.message)
      }
    },

    async turSil(tur) {
      const altTurSayisi = this.altTurlerByTur[tur.id]?.length || 0
      const mesaj = altTurSayisi > 0
        ? `"${tur.icerik_turu}" türünü ve ${altTurSayisi} alt türünü silmek istediğinize emin misiniz?`
        : `"${tur.icerik_turu}" türünü silmek istediğinize emin misiniz?`

      if (!confirm(mesaj)) return

      try {
        const { error } = await supabase
          .from('icerik_turleri')
          .delete()
          .eq('id', tur.id)

        if (error) throw error

        this.turler = this.turler.filter(t => t.id !== tur.id)
        this.altTurler = this.altTurler.filter(at => at.icerik_turu_id !== tur.id)
        alert('Tür başarıyla silindi!')
      } catch (error) {
        console.error('Tür silinirken hata:', error)
        alert('Tür silinirken bir hata oluştu: ' + error.message)
      }
    },

    async altTurEkle(turId) {
      if (!this.yeniAltTur[turId]?.trim()) return

      try {
        const { data, error } = await supabase
          .from('icerik_alt_turleri')
          .insert([{
            icerik_turu_id: turId,
            alt_tur_adi: this.yeniAltTur[turId].trim(),
            aciklama: this.yeniAltTurAciklama[turId]?.trim() || null
          }])
          .select()

        if (error) throw error

        this.altTurler.push(data[0])
        this.yeniAltTur[turId] = ''
        this.yeniAltTurAciklama[turId] = ''
        alert('Alt tür başarıyla eklendi!')
      } catch (error) {
        console.error('Alt tür eklenirken hata:', error)
        alert('Alt tür eklenirken bir hata oluştu: ' + error.message)
      }
    },

    altTurDuzenleBaslat(altTur) {
      this.duzenleniyorAltTur = altTur.id
      this.duzenleniyorAltTurAdi = altTur.alt_tur_adi
      this.duzenleniyorAltTurAciklama = altTur.aciklama || ''
    },

    async altTurGuncelle(altTur) {
      if (!this.duzenleniyorAltTurAdi.trim()) return

      try {
        const { error } = await supabase
          .from('icerik_alt_turleri')
          .update({
            alt_tur_adi: this.duzenleniyorAltTurAdi.trim(),
            aciklama: this.duzenleniyorAltTurAciklama.trim() || null
          })
          .eq('id', altTur.id)

        if (error) throw error

        altTur.alt_tur_adi = this.duzenleniyorAltTurAdi.trim()
        altTur.aciklama = this.duzenleniyorAltTurAciklama.trim() || null
        this.duzenleniyorAltTur = null
        alert('Alt tür başarıyla güncellendi!')
      } catch (error) {
        console.error('Alt tür güncellenirken hata:', error)
        alert('Alt tür güncellenirken bir hata oluştu: ' + error.message)
      }
    },

    async altTurSil(altTur) {
      if (!confirm(`"${altTur.alt_tur_adi}" alt türünü silmek istediğinize emin misiniz?`)) return

      try {
        const { error } = await supabase
          .from('icerik_alt_turleri')
          .delete()
          .eq('id', altTur.id)

        if (error) throw error

        this.altTurler = this.altTurler.filter(at => at.id !== altTur.id)
        alert('Alt tür başarıyla silindi!')
      } catch (error) {
        console.error('Alt tür silinirken hata:', error)
        alert('Alt tür silinirken bir hata oluştu: ' + error.message)
      }
    }
  }
}
</script>
