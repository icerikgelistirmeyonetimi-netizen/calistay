<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
    <header class="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-10">
      <div class="max-w-full mx-auto px-2 sm:px-3 py-3">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-900">EBA DİJİTAL İÇERİK İHTİYAÇ ANALİZİ</h1>
          </div>
          <div class="flex items-center gap-2">
            <!-- Login Formu (giriş yapılmamışsa) -->
            <div v-if="!isLoggedIn" class="flex items-center gap-2 bg-slate-50 px-4 py-2 rounded-lg border border-slate-200">
              <input
                v-model="loginUsername"
                type="text"
                placeholder="Kullanıcı adı"
                class="px-3 py-1.5 text-sm border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent w-32"
                @keyup.enter="handleLogin"
              />
              <input
                v-model="loginPassword"
                type="password"
                placeholder="Şifre"
                class="px-3 py-1.5 text-sm border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent w-32"
                @keyup.enter="handleLogin"
              />
              <button
                @click="handleLogin"
                :disabled="loginLoading"
                class="px-4 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-all disabled:opacity-50"
              >
                {{ loginLoading ? '...' : 'Giriş' }}
              </button>
              <span v-if="loginError" class="text-xs text-red-600">{{ loginError }}</span>
            </div>

            <!-- Kullanıcı bilgisi ve menü (giriş yapılmışsa) -->
            <div v-else class="flex items-center gap-2">
              <span class="text-sm text-slate-600">
                Hoş geldiniz, <strong>{{ currentUserName }}</strong>
              </span>
            <button
              v-if="isAdmin"
              @click="exportToExcel"
              :disabled="exporting"
              class="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all text-sm font-medium shadow-sm disabled:opacity-50"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              {{ exporting ? 'Dışa Aktarılıyor...' : 'Excel\'e Aktar' }}
            </button>
            <button
              v-if="isAdmin"
              @click="exportTurExcel"
              :disabled="exportingTur"
              class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-all text-sm font-medium shadow-sm disabled:opacity-50"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7h18M3 12h12M3 17h6" />
              </svg>
              {{ exportingTur ? 'Türlere Göre...' : 'Türlere Göre Excel' }}
            </button>
            <router-link
              v-if="isAdmin"
              to="/tur-yonetimi"
              class="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-all text-sm font-medium shadow-sm"
            >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Ayarlar
          </router-link>
          <button
              @click="handleLogout"
              class="inline-flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all text-sm font-medium shadow-sm"
            >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Çıkış
          </button>
          </div>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-full mx-auto px-2 sm:px-3 py-4">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-3 border-slate-300 border-t-blue-600"></div>
      </div>

      <div v-else>
        <!-- Tüm Dersler -->
        <div v-if="dogmDersler.length > 0" class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <h2 class="text-lg font-semibold text-slate-900">Dersler</h2>
            <span class="text-sm text-slate-500">({{ dogmDersler.length }} ders)</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            <button
              v-for="ders in dogmDersler"
              :key="ders"
              @click="goDersDetay(ders)"
              class="group bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-300 rounded-xl p-4 transition-all shadow-sm hover:shadow-md text-left relative"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1 min-w-0">
                  <h3 class="text-sm font-semibold text-slate-900 truncate group-hover:text-blue-600 transition-colors">{{ ders }}</h3>
                  <p class="text-xs text-slate-500 mt-1">
                    {{ dersIcerikSayilari[ders] || 0 }} içerik
                  </p>
                  <p 
                    v-if="dersKatilimcilari[ders]"
                    class="text-xs text-slate-400 mt-2"
                    :title="dersKatilimcilari[ders]"
                  >
                    <span class="font-medium text-slate-500">Katılımcılar:</span> {{ dersKatilimcilari[ders] }}
                  </p>
                  <p 
                    v-if="dersModeratorleri[ders]"
                    class="text-xs text-slate-400 mt-1"
                    :title="dersModeratorleri[ders]"
                  >
                    <span class="font-medium text-slate-500">Moderatör:</span> {{ dersModeratorleri[ders] }}
                  </p>
                </div>
                <div class="flex flex-col items-end gap-2">
                  <svg class="w-5 h-5 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                  <!-- Tamamlanma yüzdesi badge -->
                  <div 
                    class="px-2.5 py-1 rounded-full text-xs font-bold shadow-sm"
                    :class="{
                      'bg-green-100 text-green-700': dersTamamlanmaYuzdeleri[ders] === 100,
                      'bg-yellow-100 text-yellow-700': dersTamamlanmaYuzdeleri[ders] >= 50 && dersTamamlanmaYuzdeleri[ders] < 100,
                      'bg-red-100 text-red-700': dersTamamlanmaYuzdeleri[ders] < 50
                    }"
                  >
                    %{{ dersTamamlanmaYuzdeleri[ders] }}
                  </div>
                </div>
              </div>
            </button>
          </div>
        </div>

        <!-- ÖERHGM Dersleri -->
        <div v-if="oerhgmDersler.length > 0" class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <h2 class="text-lg font-semibold text-slate-900">Özel Eğitim ve Rehberlik Hizmetleri Genel Müdürlüğü</h2>
            <span class="text-sm text-slate-500">({{ oerhgmDersler.length }} ders)</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            <button
              v-for="ders in oerhgmDersler"
              :key="ders"
              @click="goDersDetay(ders)"
              class="group bg-white hover:bg-green-50 border border-slate-200 hover:border-green-300 rounded-xl p-4 transition-all shadow-sm hover:shadow-md text-left relative"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1 min-w-0">
                  <h3 class="text-sm font-semibold text-slate-900 truncate group-hover:text-green-600 transition-colors">{{ ders }}</h3>
                  <p class="text-xs text-slate-500 mt-1">
                    {{ dersIcerikSayilari[ders] || 0 }} içerik
                  </p>
                  <p 
                    v-if="dersKatilimcilari[ders]"
                    class="text-xs text-slate-400 mt-2"
                    :title="dersKatilimcilari[ders]"
                  >
                    <span class="font-medium text-slate-500">Katılımcılar:</span> {{ dersKatilimcilari[ders] }}
                  </p>
                  <p 
                    v-if="dersModeratorleri[ders]"
                    class="text-xs text-slate-400 mt-1"
                    :title="dersModeratorleri[ders]"
                  >
                    <span class="font-medium text-slate-500">Moderatör:</span> {{ dersModeratorleri[ders] }}
                  </p>
                </div>
                <div class="flex flex-col items-end gap-2">
                  <svg class="w-5 h-5 text-slate-400 group-hover:text-green-600 group-hover:translate-x-1 transition-all flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                  <!-- Tamamlanma yüzdesi badge -->
                  <div 
                    class="px-2.5 py-1 rounded-full text-xs font-bold shadow-sm"
                    :class="{
                      'bg-green-100 text-green-700': dersTamamlanmaYuzdeleri[ders] === 100,
                      'bg-yellow-100 text-yellow-700': dersTamamlanmaYuzdeleri[ders] >= 50 && dersTamamlanmaYuzdeleri[ders] < 100,
                      'bg-red-100 text-red-700': dersTamamlanmaYuzdeleri[ders] < 50
                    }"
                  >
                    %{{ dersTamamlanmaYuzdeleri[ders] }}
                  </div>
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { supabase } from '../supabase'
import * as XLSX from 'xlsx'

export default {
  name: 'HomePage',
  data() {
    return {
      dersler: [],
      dersIcerikSayilari: {},
      dersGmBilgisi: {},
      dersKatilimcilari: {},
      dersModeratorleri: {},
      dersTamamlanmaYuzdeleri: {},
      loading: true,
      exporting: false,
      exportingTur: false,
      updateInterval: null,
      isModerator: false,
      userModeratorDersler: [],
      isLoggedIn: false,
      isAdmin: false,
      currentUserName: '',
      loginUsername: '',
      loginPassword: '',
      loginError: '',
      loginLoading: false
    }
  },
  computed: {
    dogmDersler() {
      // GM filtresi kaldırıldı - tüm dersler gösteriliyor
      return this.dersler
    },
    oerhgmDersler() {
      // Boş döndür - tüm dersler dogmDersler'de gösterilecek
      return []
    }
  },
  async mounted() {
    this.checkLoginStatus()
    await this.checkModeratorStatus()
    await this.loadDersler()
    
    // Her 30 saniyede bir verileri güncelle
    this.updateInterval = setInterval(() => {
      this.loadDersler()
    }, 30000) // 30000 ms = 30 saniye
  },
  beforeUnmount() {
    // Interval'i temizle
    if (this.updateInterval) {
      clearInterval(this.updateInterval)
    }
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
      this.currentUserName = localStorage.getItem('fullName') || ''
      const username = localStorage.getItem('username') || ''
      this.isAdmin = username === 'admin'
    },
    async handleLogin() {
      if (!this.loginUsername || !this.loginPassword) {
        this.loginError = 'Kullanıcı adı ve şifre gerekli'
        return
      }

      this.loginLoading = true
      this.loginError = ''

      try {
        const { data, error } = await supabase
          .from('login')
          .select('*')
          .eq('username', this.loginUsername)
          .eq('password', this.loginPassword)
          .single()

        if (error || !data) {
          this.loginError = 'Hatalı giriş!'
          setTimeout(() => {
            this.loginError = ''
          }, 3000)
          return
        }

        // Başarılı giriş
        localStorage.setItem('isLoggedIn', 'true')
        localStorage.setItem('username', data.username)
        localStorage.setItem('fullName', data.full_name)
        
        this.isLoggedIn = true
        this.currentUserName = data.full_name
        // Admin kontrolü (username "admin" ise)
        this.isAdmin = data.username === 'admin'
        this.loginUsername = ''
        this.loginPassword = ''
        
        // Moderatör durumunu kontrol et
        await this.checkModeratorStatus()
        
      } catch (error) {
        console.error('Giriş hatası:', error)
        this.loginError = 'Bir hata oluştu'
      } finally {
        this.loginLoading = false
      }
    },
    async checkModeratorStatus() {
      try {
        const fullName = localStorage.getItem('fullName')
        if (!fullName) {
          this.isModerator = false
          this.userModeratorDersler = []
          return
        }

        // Kullanıcının adının moderator sütununda olup olmadığını kontrol et
        const { data, error } = await supabase
          .from('icerik_kayitlari')
          .select('ders_adi, moderator')
          .not('moderator', 'is', null)

        if (error) throw error

        const moderatorDersler = []
        
        // Moderator sütunlarında bu kullanıcının adı var mı kontrol et
        for (const row of data) {
          if (row.moderator) {
            // Virgülle ayrılmış isimleri kontrol et
            const moderators = row.moderator.split(',').map(m => m.trim())
            if (moderators.includes(fullName)) {
              this.isModerator = true
              if (row.ders_adi && !moderatorDersler.includes(row.ders_adi)) {
                moderatorDersler.push(row.ders_adi)
              }
            }
          }
        }

        this.userModeratorDersler = moderatorDersler
        
        if (!this.isModerator) {
          this.userModeratorDersler = []
        }
      } catch (error) {
        console.error('Moderatör kontrolü hatası:', error)
        this.isModerator = false
        this.userModeratorDersler = []
      }
    },
    async loadDersler() {
      try {
        const { data, error } = await supabase
          .from('icerik_kayitlari')
          .select('ders_adi, gm, katilimci, moderator, tur_1_id, tur_2_id, tur_3_id, tur_4_id, tur_5_id')

        if (error) throw error

        // Benzersiz ders adlarını al
        const uniqueDersler = [...new Set(data.map(item => item.ders_adi).filter(Boolean))]
        this.dersler = uniqueDersler.sort()

        // Her ders için içerik sayısını, GM, katılımcı bilgisini ve tamamlanma yüzdesini hesapla
        this.dersler.forEach(ders => {
          const dersVerileri = data.filter(item => item.ders_adi === ders)
          this.dersIcerikSayilari[ders] = dersVerileri.length
          this.dersGmBilgisi[ders] = dersVerileri[0]?.gm || ''
          this.dersKatilimcilari[ders] = dersVerileri[0]?.katilimci || ''
          this.dersModeratorleri[ders] = dersVerileri[0]?.moderator || ''
          
          // En az 1 öncelik girilmiş kazanımları say
          const tamamlananKazanimlar = dersVerileri.filter(item => 
            item.tur_1_id || item.tur_2_id || item.tur_3_id || item.tur_4_id || item.tur_5_id
          ).length
          
          const yuzde = dersVerileri.length > 0 
            ? Math.round((tamamlananKazanimlar / dersVerileri.length) * 100)
            : 0
          this.dersTamamlanmaYuzdeleri[ders] = yuzde
        })
      } catch (error) {
        console.error('Dersler yüklenirken hata:', error)
      } finally {
        this.loading = false
      }
    },
    goDersDetay(dersAdi) {
      this.$router.push({ name: 'dersDetay', params: { dersAdi } })
    },
    handleLogout() {
      if (confirm('Çıkış yapmak istediğinize emin misiniz?')) {
        localStorage.removeItem('isLoggedIn')
        localStorage.removeItem('username')
        localStorage.removeItem('fullName')
        this.isLoggedIn = false
        this.currentUserName = ''
        this.isModerator = false
        this.userModeratorDersler = []
      }
    },
    async exportToExcel() {
      this.exporting = true
      try {
        // Tüm verileri çek
        const { data, error } = await supabase
          .from('icerik_kayitlari')
          .select('*')
          .order('ders_adi')
          .order('sinif')
          .order('unite')

        if (error) throw error

        // Tür isimlerini çek
        const { data: turler } = await supabase.from('icerik_turleri').select('*')
        const { data: altTurler } = await supabase.from('icerik_alt_turleri').select('*')

        console.log('Turler:', turler)
        console.log('Alt Turler:', altTurler)

        const turMap = {}
        const altTurMap = {}
        turler?.forEach(t => turMap[t.id] = t.icerik_turu)
        altTurler?.forEach(at => altTurMap[at.id] = at.alt_tur_adi)
        
        console.log('TurMap:', turMap)
        console.log('AltTurMap:', altTurMap)

        const today = new Date().toISOString().split('T')[0]

        // ========== 1. EXCEL: DERSLER BAZINDA ==========
        const wb1 = XLSX.utils.book_new()

        // Her ders için ayrı sheet
        const dersGruplari = {}
        data.forEach(row => {
          const ders = row.ders_adi || 'Bilinmeyen'
          if (!dersGruplari[ders]) dersGruplari[ders] = []
          dersGruplari[ders].push(row)
        })

        Object.keys(dersGruplari).sort().forEach(dersAdi => {
          const rows = dersGruplari[dersAdi]
          
          // Excel için veri hazırla
          const excelData = rows.map(row => ({
            'Sınıf': row.sinif || '',
            'Ünite/Tema': row.unite || '',
            'Kazanım/Öğrenme Çıktısı': row.kazanim || '',
            'Açıklama': row.aciklama || '',
            'İçerik Türü': row.icerik_turu || '',
            '1. Öncelik Tür': turMap[row.tur_1_id] || '',
            '1. Öncelik Alt Tür': altTurMap[row.alt_tur_1_id] || '',
            '2. Öncelik Tür': turMap[row.tur_2_id] || '',
            '2. Öncelik Alt Tür': altTurMap[row.alt_tur_2_id] || '',
            '3. Öncelik Tür': turMap[row.tur_3_id] || '',
            '3. Öncelik Alt Tür': altTurMap[row.alt_tur_3_id] || '',
            '4. Öncelik Tür': turMap[row.tur_4_id] || '',
            '4. Öncelik Alt Tür': altTurMap[row.alt_tur_4_id] || '',
            '5. Öncelik Tür': turMap[row.tur_5_id] || '',
            '5. Öncelik Alt Tür': altTurMap[row.alt_tur_5_id] || '',
            'Diğer': row.diger_aciklama || '',
            'GM': row.gm || '',
            'Katılımcı': row.katilimci || ''
          }))

          // Sheet adı max 31 karakter olabilir
          let sheetName = dersAdi.substring(0, 31)
          // Geçersiz karakterleri temizle
          sheetName = sheetName.replace(/[\\/*?:\[\]]/g, '')

          const ws = XLSX.utils.json_to_sheet(excelData)
          
          // Sütun genişliklerini ayarla
          ws['!cols'] = [
            { wch: 12 }, { wch: 40 }, { wch: 60 }, { wch: 40 }, { wch: 15 },
            { wch: 20 }, { wch: 25 }, { wch: 20 }, { wch: 25 }, { wch: 20 },
            { wch: 25 }, { wch: 20 }, { wch: 25 }, { wch: 20 }, { wch: 25 },
            { wch: 30 }, { wch: 35 }, { wch: 30 }
          ]

          XLSX.utils.book_append_sheet(wb1, ws, sheetName)
        })

        XLSX.writeFile(wb1, `EBA_Icerik_Analizi_Dersler_${today}.xlsx`)
      } catch (error) {
        console.error('Excel export hatası:', error)
      } finally {
        this.exporting = false
      }
    }
    ,
    async exportTurExcel() {
      this.exportingTur = true
      try {
        const { data, error } = await supabase
          .from('icerik_kayitlari')
          .select('*')
          .order('ders_adi')
          .order('sinif')
          .order('unite')

        if (error) throw error

        const { data: turler } = await supabase.from('icerik_turleri').select('*')
        const { data: altTurler } = await supabase.from('icerik_alt_turleri').select('*')

        const turMap = {}
        const altTurMap = {}
        turler?.forEach(t => turMap[t.id] = t.icerik_turu)
        altTurler?.forEach(at => altTurMap[at.id] = at.alt_tur_adi)

        const today = new Date().toISOString().split('T')[0]

        const wb = XLSX.utils.book_new()
        const icerikTuruGruplari = {}

        data.forEach(row => {
          for (let i = 1; i <= 5; i++) {
            const turId = row[`tur_${i}_id`]
            const altTurId = row[`alt_tur_${i}_id`]

            if (turId) {
              const icerikTuru = turMap[turId] || 'Bilinmeyen'
              const altTur = altTurMap[altTurId] || ''

              if (!icerikTuruGruplari[icerikTuru]) {
                icerikTuruGruplari[icerikTuru] = []
              }

              icerikTuruGruplari[icerikTuru].push({
                ders: row.ders_adi || '',
                sinif: row.sinif || '',
                unite: row.unite || '',
                kazanim: row.kazanim || '',
                oncelik: `${i}. Öncelik`,
                altTur: altTur,
                gm: row.gm || '',
                moderator: row.moderator || ''
              })
            }
          }
        })

        Object.keys(icerikTuruGruplari).sort().forEach(icerikTuru => {
          const rows = icerikTuruGruplari[icerikTuru]
          const excelData = rows.map(row => ({
            'Ders': row.ders,
            'Sınıf': row.sinif,
            'Ünite/Tema': row.unite,
            'Kazanım': row.kazanim,
            'Öncelik': row.oncelik,
            'Alt Tür': row.altTur,
            'GM': row.gm,
            'Moderatör': row.moderator
          }))

          let sheetName = icerikTuru.substring(0, 31)
          sheetName = sheetName.replace(/[\\/*?:\[\]]/g, '')

          const ws = XLSX.utils.json_to_sheet(excelData)
          ws['!cols'] = [
            { wch: 35 },
            { wch: 12 },
            { wch: 40 },
            { wch: 60 },
            { wch: 12 },
            { wch: 25 },
            { wch: 35 },
            { wch: 30 }
          ]

          XLSX.utils.book_append_sheet(wb, ws, sheetName)
        })

        XLSX.writeFile(wb, `EBA_Icerik_Turleri_${today}.xlsx`)
      } catch (error) {
        console.error('Tür bazlı Excel export hatası:', error)
      } finally {
        this.exportingTur = false
      }
    }
  }
}
</script>
