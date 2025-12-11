<template>
  <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-4">
    <div class="bg-gradient-to-r from-slate-800 to-slate-700 px-3 py-2.5">
      <h2 class="text-xl font-bold text-white">
        Sınıf: {{ sinif }}
        <span class="text-sm font-normal text-slate-300 ml-2">({{ icerikler.length }} içerik)</span>
      </h2>
    </div>
    
    <div class="overflow-x-auto">
      <table class="w-full table-fixed">
        <thead class="bg-slate-50 border-b-2 border-slate-200">
          <tr>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-80">Kazanım</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-60">Açıklama</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">1. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">2. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">3. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">4. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">5. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-40">DİĞER</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(icerikler, unite) in uniteGruplari" :key="unite">
            <!-- Ünite başlık satırı - eğer bu ünitede kazanım yoksa, ünite için seçim yapılabilir -->
            <tr class="bg-gradient-to-r from-slate-100 to-slate-50">
              <template v-if="hasKazanim(icerikler)">
                <!-- Sadece ünite başlığı göster -->
                <td colspan="8" class="px-2 py-2">
                  <h3 class="text-xs font-bold text-slate-800">{{ unite }}</h3>
                </td>
              </template>
              <template v-else>
                <!-- Ünite için seçim yapılabilir -->
                <td class="px-2 py-2 align-top">
                  <h3 class="text-xs font-bold text-slate-800">{{ unite }}</h3>
                </td>
                <td class="px-2 py-2 text-xs text-slate-600 align-top">
                  <div 
                    v-if="icerikler[0]?.aciklama"
                    class="line-clamp-3 cursor-pointer hover:text-blue-600 transition-colors" 
                    @click="showAciklama(icerikler[0].aciklama)"
                  >
                    {{ icerikler[0].aciklama }}
                  </div>
                  <span v-else class="text-slate-400">-</span>
                </td>
                <!-- Sütun 1-5 -->
                <td v-for="col in 5" :key="col" class="px-2 py-2 align-top">
                  <TurSecici
                    :icerik="icerikler[0]"
                    :column="col"
                    :turler="turler"
                    :altTurler="altTurler"
                    @save="saveIcerik"
                  />
                </td>
                <!-- Diğer -->
                <td class="px-2 py-2 align-top">
                  <div class="relative">
                    <input
                      v-model="icerikler[0].diger_aciklama"
                      @blur="saveDiger(icerikler[0])"
                      type="text"
                      placeholder="Diğer..."
                      class="w-full text-xs px-2 py-1.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      :class="{
                        'border-yellow-400': digerSaving[icerikler[0].id],
                        'border-green-500': digerSaved[icerikler[0].id],
                        'border-red-500': digerError[icerikler[0].id]
                      }"
                    />
                    <div v-if="digerSaving[icerikler[0].id]" class="absolute right-2 top-1/2 -translate-y-1/2">
                      <svg class="animate-spin h-3 w-3 text-yellow-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                    <div v-if="digerSaved[icerikler[0].id]" class="absolute right-2 top-1/2 -translate-y-1/2 text-green-600 text-xs font-semibold">
                      ✓
                    </div>
                    <div v-if="digerError[icerikler[0].id]" class="absolute right-2 top-1/2 -translate-y-1/2 text-red-600 text-xs font-semibold">
                      ✗
                    </div>
                  </div>
                </td>
              </template>
            </tr>
            <!-- Sadece kazanım olan satırları göster -->
            <template v-for="(icerik, index) in icerikler" :key="icerik.id">
              <tr
                v-if="hasKazanim(icerikler) && icerik.kazanim"
                :class="index % 2 === 0 ? 'bg-white' : 'bg-slate-50'"
                class="hover:bg-blue-50 transition-colors"
              >
                <td class="px-2 py-2 text-xs text-slate-700 align-top">{{ icerik.kazanim }}</td>
                <td class="px-2 py-2 text-xs text-slate-600 align-top">
                  <div 
                    class="line-clamp-3 cursor-pointer hover:text-blue-600 transition-colors" 
                    @click="showAciklama(icerik.aciklama)"
                  >
                    {{ icerik.aciklama || '-' }}
                  </div>
                </td>
                
                <!-- Sütun 1-5 -->
                <td v-for="col in 5" :key="col" class="px-2 py-2 align-top">
                  <TurSecici
                    :icerik="icerik"
                    :column="col"
                    :turler="turler"
                    :altTurler="altTurler"
                    @save="saveIcerik"
                  />
                </td>
                
                <!-- Diğer -->
                <td class="px-2 py-2 align-top">
                  <div class="relative">
                    <input
                      v-model="icerik.diger_aciklama"
                      @blur="saveDiger(icerik)"
                      type="text"
                      placeholder="Diğer..."
                      class="w-full text-xs px-2 py-1.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      :class="{
                        'border-yellow-400': digerSaving[icerik.id],
                        'border-green-500': digerSaved[icerik.id],
                        'border-red-500': digerError[icerik.id]
                      }"
                    />
                    <div v-if="digerSaving[icerik.id]" class="absolute right-2 top-1/2 -translate-y-1/2">
                      <svg class="animate-spin h-3 w-3 text-yellow-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                    <div v-if="digerSaved[icerik.id]" class="absolute right-2 top-1/2 -translate-y-1/2 text-green-600 text-xs font-semibold">
                      ✓
                    </div>
                    <div v-if="digerError[icerik.id]" class="absolute right-2 top-1/2 -translate-y-1/2 text-red-600 text-xs font-semibold">
                      ✗
                    </div>
                  </div>
                </td>
              </tr>
            </template>
          </template>
        </tbody>
      </table>
    </div>

    <!-- Açıklama Modal -->
    <div
      v-if="modalAciklama"
      @click="closeModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
    >
      <div
        @click.stop
        class="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[80vh] overflow-auto"
      >
        <div class="flex items-center justify-between p-4 border-b border-slate-200 sticky top-0 bg-white">
          <h3 class="text-lg font-semibold text-slate-900">Açıklama</h3>
          <button
            @click="closeModal"
            class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <p class="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">{{ modalAciklama }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { supabase } from '../supabase'
import TurSecici from './TurSecici.vue'

export default {
  name: 'SinifTablosu',
  components: {
    TurSecici
  },
  props: {
    sinif: {
      type: String,
      required: true
    },
    icerikler: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      turler: [],
      altTurler: [],
      modalAciklama: null,
      digerSaving: {},
      digerSaved: {},
      digerError: {}
    }
  },
  computed: {
    uniteGruplari() {
      const grouped = {}
      this.icerikler.forEach(icerik => {
        let unite = icerik.unite || 'Ünite Belirtilmemiş'
        unite = unite.replace(/·/g, '').trim()
        
        if (!grouped[unite]) {
          grouped[unite] = []
        }
        grouped[unite].push(icerik)
      })
      
      const sorted = {}
      Object.keys(grouped).sort((a, b) => {
        if (a === 'Ünite Belirtilmemiş') return 1
        if (b === 'Ünite Belirtilmemiş') return -1
        
        const numA = a.match(/\d+/)
        const numB = b.match(/\d+/)
        
        if (numA && numB) {
          return parseInt(numA[0]) - parseInt(numB[0])
        }
        
        return a.localeCompare(b, 'tr')
      }).forEach(key => {
        sorted[key] = grouped[key]
      })
      
      return sorted
    }
  },
  async mounted() {
    await this.loadTurler()
    await this.loadAltTurler()
  },
  methods: {
    hasKazanim(icerikler) {
      return icerikler.some(icerik => icerik.kazanim && icerik.kazanim.trim() !== '')
    },
    async loadTurler() {
      try {
        const { data, error } = await supabase
          .from('icerik_turleri')
          .select('*')
          .order('icerik_turu')

        if (error) throw error
        this.turler = data || []
      } catch (error) {
        console.error('Türler yüklenirken hata:', error)
      }
    },
    
    async loadAltTurler() {
      try {
        const { data, error } = await supabase
          .from('icerik_alt_turleri')
          .select('*')
          .order('alt_tur_adi')

        if (error) throw error
        this.altTurler = data || []
      } catch (error) {
        console.error('Alt türler yüklenirken hata:', error)
      }
    },
    
    showAciklama(aciklama) {
      if (aciklama && aciklama !== '-') {
        this.modalAciklama = aciklama
      }
    },
    
    closeModal() {
      this.modalAciklama = null
    },
    
    async saveDiger(icerik) {
      const id = icerik.id
      this.digerSaving[id] = true
      this.digerSaved[id] = false
      this.digerError[id] = false
      
      try {
        const { error } = await supabase
          .from('icerik_kayitlari')
          .update({
            diger_aciklama: icerik.diger_aciklama || null
          })
          .eq('id', id)

        if (error) throw error
        
        this.digerSaving[id] = false
        this.digerSaved[id] = true
        
        setTimeout(() => {
          this.digerSaved[id] = false
        }, 1000)
        
      } catch (error) {
        console.error('Kayıt hatası:', error)
        this.digerSaving[id] = false
        this.digerError[id] = true
      }
    },
    
    async saveIcerik(icerik) {
      try {
        const { error } = await supabase
          .from('icerik_kayitlari')
          .update({
            tur_1_id: icerik.tur_1_id || null,
            alt_tur_1_id: icerik.alt_tur_1_id || null,
            tur_2_id: icerik.tur_2_id || null,
            alt_tur_2_id: icerik.alt_tur_2_id || null,
            tur_3_id: icerik.tur_3_id || null,
            alt_tur_3_id: icerik.alt_tur_3_id || null,
            tur_4_id: icerik.tur_4_id || null,
            alt_tur_4_id: icerik.alt_tur_4_id || null,
            tur_5_id: icerik.tur_5_id || null,
            alt_tur_5_id: icerik.alt_tur_5_id || null,
            diger_aciklama: icerik.diger_aciklama || null
          })
          .eq('id', icerik.id)

        if (error) throw error
        
      } catch (error) {
        console.error('Kayıt hatası:', error)
        throw error // Hatayı yukarı fırlat
      }
    }
  }
}
</script>

