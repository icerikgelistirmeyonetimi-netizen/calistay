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
      <table class="w-full table-fixed">
        <thead class="bg-slate-50 border-b-2 border-slate-200">
          <tr>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 20%;">Öğrenme Çıktısı</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 15%;">Açıklama</th>
            <th class="px-2 py-2 text-center text-xs font-semibold text-slate-700 uppercase" style="width: 8%;">İçerİk Türü</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 9%;">1. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 9%;">2. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 9%;">3. ÖNCELİK</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 9%;">ZENGİNLEŞTİRME</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 9%;">Destekleme</th>
            <th class="px-2 py-2 text-left text-xs font-semibold text-slate-700 uppercase" style="width: 12%;">DİĞER</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(icerikler, unite) in uniteGruplari" :key="unite">
            <!-- Ünite başlık satırı - eğer bu ünitede kazanım yoksa, ünite için seçim yapılabilir -->
            <tr class="bg-gradient-to-r from-slate-100 to-slate-50">
              <template v-if="hasKazanim(icerikler)">
                <!-- Sadece ünite başlığı göster -->
                <td colspan="11" class="px-2 py-2">
                  <div class="flex items-center gap-2">
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
                    <button
                      @click="openUniteBilgiModal(icerikler[0].unite_id)"
                      class="px-2 py-0.5 rounded-md hover:bg-blue-100 transition-colors text-sm text-blue-600 font-medium group"
                      title="Ünite Bilgileri"
                    >
                      <span class="group-hover:text-blue-700">Ünite Bilgileri</span>
                    </button>
                  </div>
                </td>
              </template>
              <template v-else>
                <!-- Ünite için seçim yapılabilir -->
                <td class="px-2 py-2 align-top">
                  <div class="flex items-center gap-2">
                    <h3 class="text-xs font-bold text-slate-800">{{ unite }}</h3>
                    <button
                      @click="openUniteBilgiModal(icerikler[0].unite_id)"
                      class="px-2 py-0.5 rounded-md hover:bg-blue-100 transition-colors text-sm text-blue-600 font-medium group"
                      title="Ünite Bilgileri"
                    >
                      <span class="group-hover:text-blue-700">Ünite Bilgileri</span>
                    </button>
                  </div>
                </td>
                <td class="px-2 py-2 text-xs text-slate-600 align-top">
                  <div 
                    v-if="icerikler[0]?.aciklama"
                    class="cursor-pointer hover:text-blue-600 transition-colors line-clamp-3"
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
                <td v-for="col in 5" :key="col" class="px-2 py-2 align-top">
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
                    class="cursor-pointer hover:text-blue-600 transition-colors line-clamp-3"
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
                <td v-for="col in 5" :key="col" class="px-2 py-2 align-top">
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

    <!-- Ünite Bilgi Modal -->
    <div
      v-if="showUniteBilgiModal"
      @click="closeUniteBilgiModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
    >
      <div
        @click.stop
        class="bg-white rounded-xl shadow-2xl w-[95vw] lg:w-[90vw] max-h-[95vh] overflow-hidden flex flex-col"
      >
        <div class="flex items-center justify-between p-5 border-b border-slate-200 bg-gradient-to-r from-blue-50 to-indigo-50">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-blue-100 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-bold text-slate-900">Ünite Bilgileri</h3>
              <p v-if="uniteBilgi" class="text-sm text-slate-600 mt-0.5">{{ uniteBilgi.unite_adi }}</p>
            </div>
          </div>
          <button
            @click="closeUniteBilgiModal"
            class="p-2 hover:bg-white rounded-lg transition-colors"
          >
            <svg class="w-6 h-6 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div v-if="uniteBilgiLoading" class="flex-1 flex items-center justify-center p-12">
          <div class="text-center">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600"></div>
            <p class="mt-4 text-sm text-slate-600">Ünite bilgileri yükleniyor...</p>
          </div>
        </div>

        <div v-else-if="!uniteBilgi" class="flex-1 flex items-center justify-center p-12">
          <div class="text-center">
            <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-slate-600 font-medium">Ünite bilgisi bulunamadı</p>
          </div>
        </div>

        <div v-else class="flex-1 flex overflow-hidden">
          <!-- Yan Menü -->
          <div class="w-96 border-r border-slate-200 bg-slate-50 overflow-y-auto">
            <div class="p-4">
              <h4 class="text-sm font-semibold text-slate-700 mb-3 uppercase tracking-wide">İÇİNDEKİLER</h4>
              <div class="space-y-1">
                <button
                  v-for="(section, index) in uniteSections"
                  :key="index"
                  @click="scrollToSection(index)"
                  :class="[
                    'w-full text-left px-3 py-2.5 rounded-lg transition-all text-sm',
                    activeSectionIndex === index
                      ? 'bg-blue-600 text-white font-medium shadow-sm'
                      : 'text-slate-700 hover:bg-white hover:shadow-sm'
                  ]"
                >
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                    <span class="line-clamp-2">{{ section.title }}</span>
                  </div>
                </button>
              </div>
            </div>
          </div>

          <!-- İçerik Alanı -->
          <div class="flex-1 overflow-y-auto" ref="uniteBilgiContent">
            <div class="p-6">
              <div v-if="uniteSections.length === 0" class="text-center py-12">
                <p class="text-slate-500">Bu ünite için bölüm bulunamadı.</p>
              </div>
              <div v-else class="space-y-6">
                <div
                  v-for="(section, index) in uniteSections"
                  :key="index"
                  :ref="`section-${index}`"
                  class="scroll-mt-4"
                >
                  <button
                    @click="toggleSection(index)"
                    class="w-full flex items-center justify-between p-4 bg-gradient-to-r from-slate-100 to-slate-50 hover:from-slate-200 hover:to-slate-100 rounded-lg transition-all border border-slate-200"
                  >
                    <h3 class="text-lg font-bold text-slate-900 text-left">{{ section.title }}</h3>
                    <svg
                      :class="[
                        'w-5 h-5 text-slate-600 transition-transform',
                        section.expanded ? 'rotate-180' : ''
                      ]"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  <div
                    v-show="section.expanded"
                    class="mt-3 p-5 bg-white rounded-lg border border-slate-200 shadow-sm"
                  >
                    <div
                      v-html="section.content"
                      class="unite-content text-slate-700 leading-relaxed"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="border-t border-slate-200 p-4 bg-slate-50">
          <button
            @click="closeUniteBilgiModal"
            class="w-full px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
          >
            Kapat
          </button>
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
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Açıklama</label>
            <textarea
              v-model="modalNewAciklama"
              rows="3"
              placeholder="Açıklama girin..."
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
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Açıklama</label>
            <textarea
              v-model="editAciklamaText"
              rows="3"
              placeholder="İsteğe bağlı açıklama"
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
      modalNewAciklama: '',
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
      editAciklamaText: '',
      kazanimSaving: false,
      digerSaving: {},
      digerSaved: {},
      digerError: {},
      newKazanim: {},
      newUnite: {},
      showUniteBilgiModal: false,
      uniteBilgi: null,
      uniteBilgiLoading: false,
      uniteSections: [],
      activeSectionIndex: 0
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

    parseSectionsFromHTML(html) {
      if (!html) return []

      const parser = new DOMParser()
      const doc = parser.parseFromString(html, 'text/html')
      const sections = []
      
      // Genel Bilgiler ve Öğrenme Çıktıları gibi başlıkları POPUP'ta GİZLE
      const genelBilgilerBasliklari = [
        'Ders Saati',
        'Alan Becerileri',
        'Kavramsal Beceriler',
        'Eğilimler',
        'Sosyal-Duygusal Öğrenme Becerileri',
        'Değerler',
        'Okuryazarlık Becerileri',
        'Disiplinler Arası İlişkiler',
        'Beceriler Arası İlişkiler',
        'Anahtar Kavramlar'
      ]

      const otherSections = []

      // .title class'ına sahip elementleri bul
      const titleElements = doc.querySelectorAll('.title')

      titleElements.forEach((titleEl, index) => {
        const title = titleEl.textContent.trim() || `Bölüm ${index + 1}`
        const lower = title.toLowerCase()

        // Gizlenecek başlıklar: Genel Bilgiler listesi veya "öğrenme çıkt" içeren başlıklar
        const isGenelBilgi = genelBilgilerBasliklari.some(baslik => lower.includes(baslik.toLowerCase()))
        const isOgrenme = lower.includes('öğrenme çıkt') || lower.includes('öğrenme çıktıları')

        if (isGenelBilgi || isOgrenme) {
          // Atla (gizle)
          return
        }

        // Bu title'dan sonraki içeriği topla (bir sonraki title'a kadar)
        let content = ''
        let currentEl = titleEl.nextElementSibling

        while (currentEl && !currentEl.classList.contains('title')) {
          content += currentEl.outerHTML
          currentEl = currentEl.nextElementSibling
        }

        otherSections.push({
          title: title,
          content: content,
          expanded: false
        })
      })

      // Diğer bölümleri ekle (gizlenenler artık yok)
      otherSections.forEach((section, index) => {
        sections.push({
          ...section,
          expanded: sections.length === 0 && index === 0 // İlk görünen bölüm açık
        })
      })

      // Eğer hiç .title yoksa veya tüm başlıklar gizlendiyse, HTML'i temizleyip göster
      if (sections.length === 0) {
        const clone = doc.cloneNode(true)
        const tEls = clone.querySelectorAll('.title')
        tEls.forEach(titleEl => {
          const ttl = titleEl.textContent.trim().toLowerCase()
          const isGenel = genelBilgilerBasliklari.some(b => ttl.includes(b.toLowerCase()))
          const isOgr = ttl.includes('öğrenme çıkt') || ttl.includes('öğrenme çıktıları')
          if (isGenel || isOgr) {
            // Başlığı ve takip eden içeriği kaldır
            let next = titleEl.nextElementSibling
            titleEl.remove()
            while (next && !next.classList.contains('title')) {
              const toRemove = next
              next = next.nextElementSibling
              toRemove.remove()
            }
          }
        })

        const cleaned = clone.body ? clone.body.innerHTML : ''
        sections.push({
          title: 'İçerik',
          content: cleaned || html,
          expanded: true
        })
      }

      // Eğer hiç .title yoksa, tüm HTML'i tek bölüm olarak göster
      if (sections.length === 0) {
        sections.push({
          title: 'İçerik',
          content: html,
          expanded: true
        })
      }

      return sections
    },

    async openUniteBilgiModal(uniteId) {
      if (!uniteId) {
        console.warn('Unite ID bulunamadı')
        return
      }

      this.showUniteBilgiModal = true
      this.uniteBilgiLoading = true
      this.uniteBilgi = null
      this.uniteSections = []
      this.activeSectionIndex = 0

      try {
        const { data, error } = await supabase
          .from('unite_bilgileri')
          .select('id, unite_adi, html')
          .eq('id', uniteId)
          .single()

        if (error) throw error
        this.uniteBilgi = data
        this.uniteSections = this.parseSectionsFromHTML(data.html)
      } catch (error) {
        console.error('Ünite bilgisi yüklenirken hata:', error)
        this.uniteBilgi = null
        this.uniteSections = []
      } finally {
        this.uniteBilgiLoading = false
      }
    },

    closeUniteBilgiModal() {
      this.showUniteBilgiModal = false
      this.uniteBilgi = null
      this.uniteBilgiLoading = false
      this.uniteSections = []
      this.activeSectionIndex = 0
    },

    toggleSection(index) {
      this.uniteSections[index].expanded = !this.uniteSections[index].expanded
    },

    scrollToSection(index) {
      this.activeSectionIndex = index
      const sectionRef = this.$refs[`section-${index}`]
      if (sectionRef && sectionRef[0]) {
        sectionRef[0].scrollIntoView({ behavior: 'smooth', block: 'start' })
        // Bölümü aç
        if (!this.uniteSections[index].expanded) {
          this.uniteSections[index].expanded = true
        }
      }
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
      this.modalNewAciklama = ''
    },
    
    closeAddModal() {
      this.showAddModal = false
      this.modalSelectedUnite = ''
      this.modalNewUnite = ''
      this.modalNewKazanim = ''
      this.modalNewAciklama = ''
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
      this.editAciklamaText = icerik.aciklama || ''
    },
    
    closeEditKazanimModal() {
      this.showEditKazanimModal = false
      this.editKazanimIcerik = null
      this.editKazanimText = ''
      this.editAciklamaText = ''
      this.kazanimSaving = false
    },
    
    async saveEditKazanim() {
      const yeniKazanim = this.editKazanimText?.trim()
      if (!yeniKazanim || !this.editKazanimIcerik) return
      
      this.kazanimSaving = true
      
      try {
        const yeniAciklama = this.editAciklamaText?.trim() || null
        const { error } = await supabase
          .from('icerik_kayitlari')
          .update({ 
            kazanim: yeniKazanim,
            aciklama: yeniAciklama
          })
          .eq('id', this.editKazanimIcerik.id)
        
        if (error) throw error
        
        // Local state'i güncelle
        this.editKazanimIcerik.kazanim = yeniKazanim
        this.editKazanimIcerik.aciklama = yeniAciklama
        
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
      const aciklama = this.modalNewAciklama?.trim()
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
          aciklama: aciklama || null,
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
            zenginlestirme: icerik.alt_tur_4_id || null,
            destekleme: icerik.alt_tur_5_id || null,
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

<style scoped>

/* Unite İçerik Styling */
.unite-content :deep(h1),
.unite-content :deep(h2),
.unite-content :deep(h3),
.unite-content :deep(h4) {
  @apply font-bold text-slate-900 mt-6 mb-3;
}

.unite-content :deep(h1) {
  @apply text-2xl;
}

.unite-content :deep(h2) {
  @apply text-xl;
}

.unite-content :deep(h3) {
  @apply text-lg;
}

.unite-content :deep(h4) {
  @apply text-base;
}

.unite-content :deep(p) {
  @apply mb-4 text-slate-700 leading-relaxed;
}

.unite-content :deep(ul),
.unite-content :deep(ol) {
  @apply mb-4 pl-6 space-y-2;
}

.unite-content :deep(ul) {
  @apply list-disc;
}

.unite-content :deep(ol) {
  @apply list-decimal;
}

.unite-content :deep(li) {
  @apply text-slate-700 leading-relaxed;
}

.unite-content :deep(strong),
.unite-content :deep(b) {
  @apply font-semibold text-slate-900;
}

.unite-content :deep(em),
.unite-content :deep(i) {
  @apply italic;
}

.unite-content :deep(table) {
  @apply w-full border-collapse mb-4 shadow-sm rounded-lg overflow-hidden;
}

.unite-content :deep(thead) {
  @apply bg-slate-100;
}

.unite-content :deep(th) {
  @apply px-4 py-2 text-left font-semibold text-slate-900 border border-slate-300;
}

.unite-content :deep(td) {
  @apply px-4 py-2 text-slate-700 border border-slate-200;
}

.unite-content :deep(tbody tr) {
  @apply transition-colors;
}

.unite-content :deep(tbody tr:hover) {
  @apply bg-blue-50;
}

.unite-content :deep(tbody tr td:first-child) {
  @apply bg-slate-50 font-semibold;
}

.unite-content :deep(blockquote) {
  @apply border-l-4 border-blue-500 pl-4 italic text-slate-600 my-4;
}

.unite-content :deep(code) {
  @apply bg-slate-100 px-2 py-1 rounded text-sm font-mono text-slate-800;
}

.unite-content :deep(pre) {
  @apply bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto mb-4;
}

.unite-content :deep(pre code) {
  @apply bg-transparent p-0 text-slate-100;
}

.unite-content :deep(a) {
  @apply text-blue-600 hover:text-blue-700 underline;
}

.unite-content :deep(hr) {
  @apply my-6 border-t-2 border-slate-300;
}

.unite-content :deep(img) {
  @apply max-w-full h-auto rounded-lg shadow-md my-4;
}

/* Scrollbar Styling */
.unite-content::-webkit-scrollbar {
  width: 8px;
}

.unite-content::-webkit-scrollbar-track {
  @apply bg-slate-100 rounded;
}

.unite-content::-webkit-scrollbar-thumb {
  @apply bg-slate-400 rounded hover:bg-slate-500;
}

/* Scroll margin for section anchors */
.scroll-mt-4 {
  scroll-margin-top: 1rem;
}

/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
