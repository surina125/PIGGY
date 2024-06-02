<template>
  <div class="box custom-box">
    <div>
      <label for="city" class="custom-label">광역시/도</label>
      <select id="city" v-model="selectedCity" @change="updateCountries" class="custom-select">
        <option disabled value="">광역시/도를 선택하세요</option>
        <option v-for="city in mapInfo" :key="city.name" :value="city.name">{{ city.name }}</option>
      </select>
    </div>

    <div>
      <label for="country" class="custom-label">시/군/구</label>
      <select id="country" v-model="selectedCountry" class="custom-select">
        <option disabled value="">시/군/구를 선택하세요</option>
        <option v-for="country in selectedCountries" :key="country">{{ country }}</option>
      </select>
    </div>

    <div>
      <label for="bank" class="custom-label">은행</label>
      <select id="bank" v-model="selectedBank" class="custom-select">
        <option value="">은행을 선택하세요</option>
        <option v-for="bank in bankInfo" :key="bank">{{ bank }}</option>
      </select>
    </div>
    <button @click="findBanks" class="custom-button">찾기</button>
  </div>
  <div class="map custom-map" ref="map"></div>
</template>

<script>
import data from "@/assets/data.json";
const kakaoApiKey = import.meta.env.VITE_APP_KAKAO;
export default {
  data() {
    return {
      mapInfo: [],
      bankInfo: [],
      selectedCity: '',
      selectedCountry: '',
      selectedCountries: [],
      selectedBank: '',
      map: null,
      ps: null,
      geocoder: null
    };
  },
  methods: {
    updateCountries() {
      const city = this.mapInfo.find(c => c.name === this.selectedCity);
      if (city) {
        this.selectedCountries = city.countries;
      } else {
        this.selectedCountries = [];
      }
    },
    findBanks() {
      if (this.selectedBank) {
        const query = `${this.selectedCity} ${this.selectedCountry} ${this.selectedBank}`;
        this.ps.keywordSearch(query, (data, status) => {
          if (status === kakao.maps.services.Status.OK) {
            this.map.setCenter(new kakao.maps.LatLng(data[0].y, data[0].x));
            data.forEach(place => {
              this.displayMarker(place);
            });
          } else {
            alert('검색 결과가 없습니다.');
          }
        });
      } else {
        const address = `${this.selectedCity} ${this.selectedCountry}`;
        this.geocoder.addressSearch(address, (result, status) => {
          if (status === kakao.maps.services.Status.OK) {
            const coords = new kakao.maps.LatLng(result[0].y, result[0].x);
            this.map.setCenter(coords);

            const placesSearchCB = (data, status) => {
              if (status === kakao.maps.services.Status.OK) {
                data.forEach(place => {
                  this.displayMarker(place);
                });
              } else {
                alert('검색 결과가 없습니다.');
              }
            };

            this.ps.categorySearch('BK9', placesSearchCB, {
              location: coords,
              radius: 5000
            });
          } else {
            alert('주소 검색 결과가 없습니다.');
          }
        });
      }
    },
    displayMarker(place) {
      const marker = new kakao.maps.Marker({
        map: this.map,
        position: new kakao.maps.LatLng(place.y, place.x)
      });

      kakao.maps.event.addListener(marker, 'click', () => {
        const infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
        infowindow.setContent(`
          <div style="display: flex; justify-content: center; align-items: center; padding: 18px;">
            <div style="padding: 15px; font-size: 13px; text-align: center;">
              <strong>${place.place_name}</strong><br>
              도로명 주소: ${place.road_address_name || '정보 없음'}<br>
              전화번호: ${place.phone || '정보 없음'}
            </div>
          </div>
        `);
        infowindow.open(this.map, marker);
      });
    },
    initMap() {
      const container = this.$refs.map;
      const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      };
      this.map = new kakao.maps.Map(container, options);
      this.ps = new kakao.maps.services.Places();
      this.geocoder = new kakao.maps.services.Geocoder();
    }
  },
  mounted() {
    this.mapInfo = data.mapInfo;
    this.bankInfo = data.bankInfo;

  
    if (!window.kakao || !window.kakao.maps) {
      const script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${kakaoApiKey}&libraries=services`;

      script.addEventListener('load', () => {
        kakao.maps.load(() => {
          this.initMap();
        });
      });
      document.head.appendChild(script);
    } else {
      this.initMap();
    }
  }
};
</script>

<style scoped>
.custom-box {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.custom-label {
  margin-right: 10px;
  font-weight: bold;
}

.custom-select {
  margin: 5px 10px;
  padding: 10px;
  border-radius: 5px;
}

.custom-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #333;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.custom-button:hover {
  background-color: #1a1a1a;
}

.custom-map {
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  width: 100%;
  max-width: 800px;
  height: 500px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
