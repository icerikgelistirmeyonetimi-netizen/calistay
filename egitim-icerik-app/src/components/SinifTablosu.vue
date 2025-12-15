<template>
  <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-4">
    <div class="bg-gradient-to-r from-slate-800 to-slate-700 px-3 py-2.5">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-white">
          Sınıf: {{ sinif }}
          <span class="text-sm font-normal text-slate-300 ml-2">({{ icerikler.length }} içerik)</span>
        </h2>
        <button
          v-if="isLoggedIn"
          @click="openAddModal(null)"
          class="px-3 py-1.5 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Ekle
        </button>
      </div>
    </div>
    
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-slate-50 border-b-2 border-slate-200">
          <tr>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase min-w-[14rem]">Öğrenme Çıktısı</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase min-w-[12rem]">Açıklama</th>
            <th class="px-2 py-2 text-center text-xs font-semibold text-slate-700 uppercase w-28">İçerİk Türü</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">1. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">2. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-32">3. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase w-40">DİĞER</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(icerikler, unite) in uniteGruplari" :key="unite">
            <!-- Ünite başlık satırı - eğer bu ünitede kazanım yoksa, ünite için seçim yapılabilir -->
            <tr class="bg-gradient-to-r from-slate-100 to-slate-50">
              <template v-if="hasKazanim(icerikler)">
                <!-- Sadece ünite başlığı göster -->
                <td colspan="9" class="px-2 py-2">
                  <h3 
                    v-if="isLoggedIn"
                    @click="openUniteModal(unite, icerikler)"
                    class="text-xs font-bold text-slate-800 cursor-pointer hover:text-blue-600 transition-colors"
                  >
                    {{ unite }}
                  </h3>
                  <h3 
                    v-else
                    class="text-xs font-bold text-slate-800"
                  >
                    {{ unite }}
                  </h3>
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
                    class="cursor-pointer hover:text-blue-600 transition-colors whitespace-pre-wrap"
                    @click="showAciklama(icerikler[0].aciklama)"
                  >
                    {{ icerikler[0].aciklama }}
                  </div>
                  <span v-else class="text-slate-400">-</span>
                </td>
                <!-- İçerik Türü -->
                <td class="px-2 py-2 text-xs text-slate-600 align-middle text-center">
                  <span class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full text-xs leading-tight inline-block">
                    {{ icerikler[0]?.icerik_turu || '-' }}
                  </span>
                </td>
                <!-- Sütun 1-3 (eşit ve sabit genişlik) -->
                <td v-for="col in 3" :key="col" class="px-2 py-2 align-top w-32 min-w-[8rem]">
                  <TurSecici
                    :icerik="icerikler[0]"
                    :column="col"
                    :turler="turler"
                    :altTurler="altTurler"
                    :isLoggedIn="isLoggedIn"
                    @save="saveIcerik"
                  />
                </td>
                <!-- Diğer -->
                <td class="px-2 py-2 align-top">
                  <div 
                    @click="isLoggedIn ? openDigerModal(icerikler[0]) : null"
                    class="relative px-2 py-1.5 border border-slate-300 rounded-lg transition-all min-h-[32px] bg-white"
                    :class="[
                      isLoggedIn ? 'cursor-pointer hover:border-blue-400' : 'cursor-default',
                      {
                        'border-yellow-400': digerSaving[icerikler[0].id],
                        'border-green-500': digerSaved[icerikler[0].id],
                        'border-red-500': digerError[icerikler[0].id]
                      }
                    ]"
                  >
                    <div class="text-xs text-slate-700 line-clamp-2">
                      {{ icerikler[0].diger_aciklama || '-' }}
                    </div>
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
                    class="cursor-pointer hover:text-blue-600 transition-colors whitespace-pre-wrap"
                    @click="showAciklama(icerik.aciklama)"
                  >
                    {{ icerik.aciklama || '-' }}
                  </div>
                </td>
                <!-- İçerik Türü -->
                <td class="px-2 py-2 text-xs text-slate-600 align-middle text-center">
                  <span class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full text-xs leading-tight inline-block">
                    {{ icerik.icerik_turu || '-' }}
                  </span>
                </td>
                
                <!-- Sütun 1-3 (eşit ve sabit genişlik) -->
                <td v-for="col in 3" :key="col" class="px-2 py-2 align-top w-32 min-w-[8rem]">
                  <TurSecici
                    :icerik="icerik"
                    :column="col"
                    :turler="turler"
                    :altTurler="altTurler"
                    :isLoggedIn="isLoggedIn"
                    @save="saveIcerik"
                  />
                </td>
                
                <!-- Diğer -->
                <td class="px-2 py-2 align-top">
                  <div 
                    @click="isLoggedIn ? openDigerModal(icerik) : showAciklama(icerik.diger_aciklama)"
                    class="relative px-2 py-1.5 border border-slate-300 rounded-lg transition-all min-h-[32px] bg-white"
                    :class="[
                      isLoggedIn ? 'cursor-pointer hover:border-blue-400' : (icerik.diger_aciklama ? 'cursor-pointer' : 'cursor-default'),
                      {
                        'border-yellow-400': digerSaving[icerik.id],
                        'border-green-500': digerSaved[icerik.id],
                        'border-red-500': digerError[icerik.id]
                      }
                    ]"
                  >
                    <div class="text-xs text-slate-700 line-clamp-2">
                      {{ icerik.diger_aciklama || '-' }}
                    </div>
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

    <!-- Diğer Modal -->
    <div
      v-if="modalDigerIcerik"
      @click="closeDigerModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
    >
      <div
        @click.stop
        class="bg-white rounded-xl shadow-2xl max-w-3xl w-full"
      >
        <div class="flex items-center justify-between p-4 border-b border-slate-200 bg-white">
          <h3 class="text-lg font-semibold text-slate-900">Diğer Açıklama</h3>
          <button
            @click="closeDigerModal"
            class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <textarea
            v-if="isLoggedIn"
            v-model="modalDigerText"
            rows="8"
            class="w-full text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Diğer açıklamaları buraya yazın..."
          ></textarea>
          <div v-else class="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">
            {{ modalDigerText || 'Açıklama yok' }}
          </div>
          <div class="flex justify-end gap-2 mt-4">
            <button
              @click="closeDigerModal"
              class="px-4 py-2 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
            >
              {{ isLoggedIn ? 'İptal' : 'Kapat' }}
            </button>
            <button
              v-if="isLoggedIn"
              @click="saveDigerModal"
              :disabled="digerModalSaving"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50"
            >
              {{ digerModalSaving ? 'Kaydediliyor...' : 'Kaydet' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Yeni Kayıt Ekleme Modal -->
    <div
      v-if="showAddModal"
      @click="closeAddModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
    >
      <div
        @click.stop
        class="bg-white rounded-xl shadow-2xl max-w-2xl w-full"
      >
        <div class="flex items-center justify-between p-4 border-b border-slate-200 bg-white">
          <h3 class="text-lg font-semibold text-slate-900">Yeni Kayıt Ekle</h3>
          <button
            @click="closeAddModal"
            class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Ünite Seçin</label>
            <select
              v-model="modalSelectedUnite"
              class="w-full text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="" disabled>Seçiniz...</option>
              <option v-for="unite in uniteListesi" :key="unite" :value="unite">
                {{ unite }}
              </option>
              <option value="__NEW__">+ Yeni Ünite</option>
            </select>
          </div>
          <div v-if="modalSelectedUnite === '__NEW__'">
            <label class="block text-sm font-medium text-slate-700 mb-2">Yeni Ünite Adı</label>
            <input
              v-model="modalNewUnite"
              type="text"
              placeholder="Yeni ünite adı girin"
              class="w-full text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Kazanım</label>
            <textarea
              v-model="modalNewKazanim"
              rows="3"
              placeholder="Yeni kazanım girin..."
              class="w-full text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            ></textarea>
          </div>
          <div class="flex justify-end gap-2 mt-4">
            <button
              @click="closeAddModal"
              class="px-4 py-2 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
            >
              İptal
            </button>
            <button
              @click="saveAddModal"
              :disabled="!canSaveAdd || addModalSaving"
              class="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors disabled:opacity-50"
            >
              {{ addModalSaving ? 'Ekleniyor...' : 'Ekle' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Ünite Düzenleme/Silme Modal -->
    <div
      v-if="showUniteModal"
      @click="closeUniteModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
    >
      <div
        @click.stop
        class="bg-white rounded-xl shadow-2xl max-w-md w-full"
      >
        <div class="flex items-center justify-between p-4 border-b border-slate-200 bg-white">
          <h3 class="text-lg font-semibold text-slate-900">Ünite İşlemleri</h3>
          <button
            @click="closeUniteModal"
            class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Ünite Adı</label>
            <input
              v-model="editUniteAdi"
              type="text"
              class="w-full text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div class="text-xs text-slate-500">
            Bu ünitede {{ uniteIcerikSayisi }} içerik bulunmaktadır.
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Öğrenme Çıktıları</label>
            <div class="max-h-48 overflow-y-auto border border-slate-200 rounded-lg p-3 space-y-2">
              <div 
                v-for="(icerik, index) in uniteIcerikler" 
                :key="icerik.id"
                class="text-xs text-slate-700 pb-2 border-b border-slate-100 last:border-0 flex items-start gap-2"
              >
                <div class="flex-1">
                  <span class="font-semibold text-slate-500">{{ index + 1 }}.</span> 
                  {{ icerik.kazanim || '(Kazanım belirtilmemiş)' }}
                </div>
                <!-- Kazanım silme butonu kaldırıldı; sadece düzenleme kaldı veya tamamı gizlenebilir -->
                <div v-if="isLoggedIn" class="flex gap-1 flex-shrink-0">
                  <button
                    @click="editKazanim(icerik)"
                    class="p-1 hover:bg-blue-100 rounded transition-colors text-blue-600"
                    title="Düzenle"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="flex gap-2 pt-4">
            <button
              @click="updateUnite"
              :disabled="uniteUpdateSaving || !editUniteAdi || editUniteAdi.trim() === ''"
              class="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              {{ uniteUpdateSaving ? 'Güncelleniyor...' : 'Düzenle' }}
            </button>
            <!-- Ünite silme butonu kaldırıldı -->
          </div>
        </div>
      </div>
    </div>

    <!-- Kazanım Düzenleme Modal -->
    <div
      v-if="showEditKazanimModal"
      @click="closeEditKazanimModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-[60] p-4"
    >
      <div
        @click.stop
        class="bg-white rounded-xl shadow-2xl max-w-2xl w-full"
      >
        <div class="flex items-center justify-between p-4 border-b border-slate-200 bg-white">
          <h3 class="text-lg font-semibold text-slate-900">Kazanım Düzenle</h3>
          <button
            @click="closeEditKazanimModal"
            class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Kazanım</label>
            <textarea
              v-model="editKazanimText"
              rows="4"
              class="w-full text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            ></textarea>
          </div>
          <div class="flex justify-end gap-2">
            <button
              @click="closeEditKazanimModal"
              class="px-4 py-2 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
            >
              İptal
            </button>
            <button
              @click="saveEditKazanim"
              :disabled="!editKazanimText || editKazanimText.trim() === '' || kazanimSaving"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50"
            >
              {{ kazanimSaving ? 'Kaydediliyor...' : 'Kaydet' }}
            </button>
          </div>
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
    },
    isLoggedIn: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      turler: [],
      altTurler: [],
      modalAciklama: null,
      modalDigerIcerik: null,
      modalDigerText: '',
      digerModalSaving: false,
      showAddModal: false,
      modalSelectedUnite: '',
      modalNewUnite: '',
      modalNewKazanim: '',
      addModalSaving: false,
      showUniteModal: false,
      editUniteAdi: '',
      originalUniteAdi: '',
      uniteIcerikler: [],
      uniteUpdateSaving: false,
      uniteDeleteSaving: false,
      showEditKazanimModal: false,
      editKazanimIcerik: null,
      editKazanimText: '',
      kazanimSaving: false,
      digerSaving: {},
      digerSaved: {},
      digerError: {},
      newKazanim: {},
      newUnite: {}
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
      
      // Her ünite grubunda kazanımların sıralamasını stabil tut (id artan)
      Object.keys(grouped).forEach(key => {
        grouped[key] = grouped[key].slice().sort((a, b) => {
          const ida = typeof a.id === 'number' ? a.id : Number.MAX_SAFE_INTEGER
          const idb = typeof b.id === 'number' ? b.id : Number.MAX_SAFE_INTEGER
          return ida - idb
        })
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
    },
    uniteListesi() {
      return Object.keys(this.uniteGruplari)
    },
    canSaveAdd() {
      if (!this.modalNewKazanim || !this.modalNewKazanim.trim()) return false
      if (!this.modalSelectedUnite) return false
      if (this.modalSelectedUnite === '__NEW__' && (!this.modalNewUnite || !this.modalNewUnite.trim())) return false
      return true
    },
    uniteIcerikSayisi() {
      return this.uniteIcerikler.length
    }
  },
  async mounted() {
    await this.loadTurler()
    await this.loadAltTurler()
    this.$nextTick(() => {
      this.resizeAllTextareas()
    })
  },
  updated() {
    this.$nextTick(() => {
      this.resizeAllTextareas()
    })
  },
  methods: {
    resizeAllTextareas() {
      const textareas = this.$el.querySelectorAll('textarea')
      textareas.forEach(textarea => {
        if (textarea.value) {
          textarea.style.height = 'auto'
          textarea.style.height = textarea.scrollHeight + 'px'
        }
      })
    },
    hasKazanim(icerikler) {
      return icerikler.some(icerik => icerik.kazanim && icerik.kazanim.trim() !== '')
    },
    expandTextarea(event) {
      const textarea = event.target
      textarea.style.height = 'auto'
      textarea.style.height = textarea.scrollHeight + 'px'
    },
    autoResize(event) {
      const textarea = event.target
      textarea.style.height = 'auto'
      textarea.style.height = textarea.scrollHeight + 'px'
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
    
    openDigerModal(icerik) {
      this.modalDigerIcerik = icerik
      this.modalDigerText = icerik.diger_aciklama || ''
    },
    
    closeDigerModal() {
      this.modalDigerIcerik = null
      this.modalDigerText = ''
      this.digerModalSaving = false
    },
    
    openAddModal(unite) {
      this.showAddModal = true
      this.modalSelectedUnite = ''
      this.modalNewUnite = ''
      this.modalNewKazanim = ''
    },
    
    closeAddModal() {
      this.showAddModal = false
      this.modalSelectedUnite = ''
      this.modalNewUnite = ''
      this.modalNewKazanim = ''
      this.addModalSaving = false
    },
    
    openUniteModal(unite, icerikler) {
      this.showUniteModal = true
      this.originalUniteAdi = unite
      this.editUniteAdi = unite
      this.uniteIcerikler = icerikler
    },
    
    closeUniteModal() {
      this.showUniteModal = false
      this.originalUniteAdi = ''
      this.editUniteAdi = ''
      this.uniteIcerikler = []
      this.uniteUpdateSaving = false
      this.uniteDeleteSaving = false
    },
    
    async updateUnite() {
      const yeniAd = this.editUniteAdi?.trim()
      if (!yeniAd || yeniAd === this.originalUniteAdi) return
      
      this.uniteUpdateSaving = true
      
      try {
        // Bu üniteye ait tüm kayıtların ünite adını güncelle
        const ids = this.uniteIcerikler.map(i => i.id)
        
        const { error } = await supabase
          .from('icerik_kayitlari')
          .update({ unite: yeniAd })
          .in('id', ids)
        
        if (error) throw error
        
        this.closeUniteModal()
        location.reload()
        
      } catch (error) {
        console.error('Güncelleme hatası:', error)

      } finally {
        this.uniteUpdateSaving = false
      }
    },
    
    confirmDeleteUnite() {
      const onay = confirm(`"${this.originalUniteAdi}" ünitesini ve içindeki ${this.uniteIcerikSayisi} kaydı silmek istediğinizden emin misiniz? Bu işlem geri alınamaz!`)
      if (onay) {
        this.deleteUnite()
      }
    },
    
    async deleteUnite() {
      this.uniteDeleteSaving = true
      
      try {
        // Bu üniteye ait tüm kayıtları sil
        const ids = this.uniteIcerikler.map(i => i.id)
        
        const { error } = await supabase
          .from('icerik_kayitlari')
          .delete()
          .in('id', ids)
        
        if (error) throw error
        
        this.closeUniteModal()
        location.reload()
        
      } catch (error) {
        console.error('Silme hatası:', error)

      } finally {
        this.uniteDeleteSaving = false
      }
    },
    
    editKazanim(icerik) {
      this.showEditKazanimModal = true
      this.editKazanimIcerik = icerik
      this.editKazanimText = icerik.kazanim || ''
    },
    
    closeEditKazanimModal() {
      this.showEditKazanimModal = false
      this.editKazanimIcerik = null
      this.editKazanimText = ''
      this.kazanimSaving = false
    },
    
    async saveEditKazanim() {
      const yeniKazanim = this.editKazanimText?.trim()
      if (!yeniKazanim || !this.editKazanimIcerik) return
      
      this.kazanimSaving = true
      
      try {
        const { error } = await supabase
          .from('icerik_kayitlari')
          .update({ kazanim: yeniKazanim })
          .eq('id', this.editKazanimIcerik.id)
        
        if (error) throw error
        
        // Local state'i güncelle
        this.editKazanimIcerik.kazanim = yeniKazanim
        
        this.closeEditKazanimModal()
        
      } catch (error) {
        console.error('Güncelleme hatası:', error)

      } finally {
        this.kazanimSaving = false
      }
    },
    
    async deleteKazanim(icerik) {
      const onay = confirm(`"${icerik.kazanim || 'Bu kazanım'}" kaydını silmek istediğinizden emin misiniz? Bu işlem geri alınamaz!`)
      if (!onay) return
      
      try {
        const { error } = await supabase
          .from('icerik_kayitlari')
          .delete()
          .eq('id', icerik.id)
        
        if (error) throw error
        
        // Local state'den kaldır
        const index = this.uniteIcerikler.findIndex(i => i.id === icerik.id)
        if (index > -1) {
          this.uniteIcerikler.splice(index, 1)
        }
        
        // Eğer ünite boş kaldıysa modal'ı kapat ve sayfayı yenile
        if (this.uniteIcerikler.length === 0) {
          this.closeUniteModal()
          location.reload()
        }
        
      } catch (error) {
        console.error('Silme hatası:', error)
      }
    },
    
    async saveAddModal() {
      const kazanim = this.modalNewKazanim?.trim()
      const selectedUnite = this.modalSelectedUnite
      const yeniUnite = this.modalNewUnite?.trim()
      
      if (!kazanim || !selectedUnite) return
      if (selectedUnite === '__NEW__' && !yeniUnite) return
      
      this.addModalSaving = true
      
      try {
        // Herhangi bir içeriği referans al (ders adı ve diğer bilgiler için)
        const mevcutIcerik = this.icerikler[0]
        
        const yeniKayit = {
          ders_adi: mevcutIcerik?.ders_adi || '',
          sinif: this.sinif,
          unite: selectedUnite === '__NEW__' ? yeniUnite : selectedUnite,
          kazanim: kazanim,
          aciklama: null,
          icerik_turu: mevcutIcerik?.icerik_turu || null,
          gm: mevcutIcerik?.gm || null,
          katilimci: mevcutIcerik?.katilimci || null
        }
        
        const { data, error } = await supabase
          .from('icerik_kayitlari')
          .insert([yeniKayit])
          .select()
        
        if (error) throw error
        
        this.closeAddModal()
        
        // Sayfayı yenile
        location.reload()
        
      } catch (error) {
        console.error('Ekleme hatası:', error)

      } finally {
        this.addModalSaving = false
      }
    },
    
    async saveDigerModal() {
      if (!this.modalDigerIcerik) return
      
      this.digerModalSaving = true
      const icerik = this.modalDigerIcerik
      
      try {
        const { error } = await supabase
          .from('icerik_kayitlari')
          .update({
            diger_aciklama: this.modalDigerText || null
          })
          .eq('id', icerik.id)

        if (error) throw error
        
        // Değeri güncelle
        icerik.diger_aciklama = this.modalDigerText
        
        this.digerSaved[icerik.id] = true
        setTimeout(() => {
          this.digerSaved[icerik.id] = false
        }, 2000)
        
        this.closeDigerModal()
        
      } catch (error) {
        console.error('Kayıt hatası:', error)
        this.digerError[icerik.id] = true
        setTimeout(() => {
          this.digerError[icerik.id] = false
        }, 2000)
      } finally {
        this.digerModalSaving = false
      }
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

