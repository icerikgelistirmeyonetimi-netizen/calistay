<template>
  <div class="space-y-1.5">
    <!-- Tür Seçimi -->
    <select
      v-if="!isAdded"
      v-model="selectedTur"
      @change="onTurChange"
      :disabled="saving"
      class="w-full text-xs px-2 py-1.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white disabled:bg-slate-100"
    >
      <option :value="null">Seçiniz...</option>
      <option v-for="tur in turler" :key="tur.id" :value="tur.id">
        {{ tur.icerik_turu }}
      </option>
    </select>

    <!-- Alt Tür Seçimi (Tür seçildiğinde gösterilir) -->
    <select
      v-if="selectedTur && !isAdded"
      v-model="selectedAltTur"
      @change="onAltTurChange"
      :disabled="saving"
      class="w-full text-xs px-2 py-1.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white disabled:bg-slate-100"
    >
      <option :value="null">Alt tür seçiniz...</option>
      <option v-for="altTur in filteredAltTurler" :key="altTur.id" :value="altTur.id">
        {{ altTur.alt_tur_adi }}
      </option>
    </select>

    <!-- Ekle Butonu (Alt tür seçildiğinde gösterilir) -->
    <button
      v-if="selectedTur && selectedAltTur && !isAdded"
      @click="onEkle"
      :disabled="saving"
      :class="error ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'"
      class="w-full px-2 py-1.5 text-white text-xs rounded-lg transition-all disabled:bg-slate-400 disabled:cursor-not-allowed"
    >
      {{ saving ? 'Kaydediliyor...' : error ? 'Tekrar Dene' : 'Ekle' }}
    </button>

    <!-- Kaydediliyor durumu -->
    <div
      v-if="saving"
      class="flex items-center gap-2 p-2 bg-yellow-50 border border-yellow-300 rounded-lg"
    >
      <div class="animate-spin h-3 w-3 border-2 border-yellow-600 border-t-transparent rounded-full"></div>
      <span class="text-xs text-yellow-800">Kaydediliyor...</span>
    </div>

    <!-- Hata mesajı -->
    <div
      v-if="error"
      class="flex items-center gap-2 p-2 bg-red-50 border border-red-300 rounded-lg"
    >
      <svg class="w-3.5 h-3.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
      <span class="text-xs text-red-800">Kayıt başarısız</span>
    </div>

    <!-- Kaydedildi mesajı -->
    <div
      v-if="saved"
      class="flex items-center gap-2 p-2 bg-green-50 border border-green-300 rounded-lg"
    >
      <svg class="w-3.5 h-3.5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
      <span class="text-xs text-green-800">Kaydedildi</span>
    </div>

    <!-- Eklenen değer gösterimi -->
    <div
      v-if="isAdded && !saving && !saved && !error"
      class="flex items-center justify-between gap-2 p-2 bg-blue-50 border border-blue-200 rounded-lg"
    >
      <div class="flex-1 min-w-0">
        <div class="text-xs font-medium text-slate-900 truncate">{{ getTurAdi(currentTurId) }}</div>
        <div class="text-xs text-slate-600 truncate">{{ getAltTurAdi(currentAltTurId) }}</div>
      </div>
      <button
        @click="onSil"
        class="flex-shrink-0 p-1 text-red-600 hover:bg-red-100 rounded transition-all"
        title="Sil"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TurSecici',
  props: {
    icerik: {
      type: Object,
      required: true
    },
    column: {
      type: Number,
      required: true
    },
    turler: {
      type: Array,
      required: true
    },
    altTurler: {
      type: Array,
      required: true
    },
    isLoggedIn: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      selectedTur: null,
      selectedAltTur: null,
      saving: false,
      saved: false,
      error: false,
      savedTimer: null
    }
  },
  computed: {
    turFieldName() {
      return `tur_${this.column}_id`
    },
    altTurFieldName() {
      return `alt_tur_${this.column}_id`
    },
    currentTurId() {
      return this.icerik[this.turFieldName]
    },
    currentAltTurId() {
      return this.icerik[this.altTurFieldName]
    },
    isAdded() {
      return this.currentTurId && this.currentAltTurId
    },
    filteredAltTurler() {
      if (!this.selectedTur) return []
      return this.altTurler.filter(at => at.icerik_turu_id === this.selectedTur)
    }
  },
  mounted() {
    // Mevcut değerleri yükle
    if (this.currentTurId) {
      this.selectedTur = this.currentTurId
    }
    if (this.currentAltTurId) {
      this.selectedAltTur = this.currentAltTurId
    }
  },
  beforeUnmount() {
    // Timer'ı temizle
    if (this.savedTimer) {
      clearTimeout(this.savedTimer)
    }
  },
  methods: {
    onTurChange() {
      // Tür değiştiğinde alt türü sıfırla
      this.selectedAltTur = null
    },
    
    onAltTurChange() {
      // Alt tür seçildiğinde otomatik olarak bekle
    },
    
    async onEkle() {
      // İçerik objesini güncelle
      this.icerik[this.turFieldName] = this.selectedTur
      this.icerik[this.altTurFieldName] = this.selectedAltTur
      
      // Kaydet
      await this.saveWithFeedback()
      
      // Seçimleri sıfırla
      this.selectedTur = null
      this.selectedAltTur = null
    },
    
    async onSil() {
      // İçerik objesini güncelle
      this.icerik[this.turFieldName] = null
      this.icerik[this.altTurFieldName] = null
      
      // Kaydet
      await this.saveWithFeedback()
      
      // Seçimleri sıfırla
      this.selectedTur = null
      this.selectedAltTur = null
    },
    
    async saveWithFeedback() {
      // Önceki timer'ı temizle
      if (this.savedTimer) {
        clearTimeout(this.savedTimer)
      }
      
      // Kaydediliyor durumuna geç
      this.saving = true
      this.saved = false
      this.error = false
      
      try {
        // Kaydet
        await this.$emit('save', this.icerik)
        
        // Kaydedildi durumuna geç
        this.saving = false
        this.saved = true
        
        // 1 saniye sonra mesajı gizle
        this.savedTimer = setTimeout(() => {
          this.saved = false
        }, 1000)
      } catch (err) {
        // Hata durumuna geç
        this.saving = false
        this.error = true
        console.error('Kayıt hatası:', err)
      }
    },
    
    getTurAdi(turId) {
      const tur = this.turler.find(t => t.id === turId)
      return tur ? tur.icerik_turu : ''
    },
    
    getAltTurAdi(altTurId) {
      const altTur = this.altTurler.find(at => at.id === altTurId)
      return altTur ? altTur.alt_tur_adi : ''
    }
  }
}
</script>
