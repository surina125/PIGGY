# 🐷 PIGGY

## 📚 목차
1. [👥 팀원 정보 및 분담 내역](#-팀원-정보-및-분담-내역)
2. [🏗️ 설계 내용(아키텍처 등) 및 실제 구현정도](#-설계-내용아키텍처-등-및-실제-구현-정도)
3. [🗂️ 데이터베이스 모델링(ERD)](#-데이터베이스-모델링erd)
4. [🧠 금융 상품 추천 알고리즘에 대한 기술적 설명](#-금융-상품-추천-알고리즘에-대한-기술적-설명)
5. [🌟 서비스 대표 기능들에 대한 설명](#-서비스-대표-기능들에-대한-설명)
6. [💬 프로젝트 후기(느낀점)](#-프로젝트-후기느낀점)

<br>

## 👥 팀원 정보 및 분담 내역

- **프로젝트 기간**: 2024/05/16 ~ 2024/05/24 (약 9일)

<br>

| 팀원 이름        | 역할 및 분담 내역 |
|------------------|-------------------|
| **정현수 (팀장, BE/FE)** | - **Back End**: 회원 커스터마이징, 추천 알고리즘 구현<br>- **Front End**: 메인페이지, 회원가입, 로그인, 프로필 페이지, 금융상품 비교, 금융상품 추천, 데이터 시각화, AI 챗봇 |
| **고도연 (BE/FE)** | - **Back End**: 금융상품 + 환율 데이터 저장, 금융상품 + 환율 + 게시판 RESTful 구현<br>- **Front End**: 게시판 CRUD, 근처 은행 검색, 환율 계산기 |

> **Note**: ERD 기획과 페이지 설계는 함께 협력하여 진행했습니다.

<br>

### 🛠️ 기술 스택

| 구분   | 기술 스택 |
|--------|------------|
| **Front End** | language: JavaScript<br>framework: Vue 3.4.27, Pinia 2.1.7 (+Pinia-plugin-persistedstate), Axios 1.3.4, Chart.js 4.0.0 |
| **Back End**  | language: Python 3.11.0<br>framework: Django 4.2.13, Pandas 2.0.3<br>database: SQLite 3.21.0 |

<br>

## 🗂️ 데이터베이스 모델링(ERD)
![ERD](https://github.com/surina125/Financial-project/assets/156388715/206a7add-c17a-409d-8c5c-17dca67db368)

<br>

## 📜 API 명세서
- [Swagger 링크](http://127.0.0.1:8000/swagger/)
- ![API](https://github.com/surina125/Financial-project/blob/master/api.png?raw=true)

<br>

## 🧠 금융 상품 추천 알고리즘에 대한 기술적 설명

### 1. 추천 알고리즘 
#### 프로필 정보에 입력된 나이, 연봉, 자산으로 유클리드 거리 측정하여 유사도 판단하기
1. 유저 모델을 쿼리셋 형태로 불러와 필요한 컬럼만 데이터 프레임 형태로 변환
2. 로그인한 사용자와 다른 사용자들 간의 유클리드 거리를 계산하여 정렬
3. 예금, 적금, 대출 상품들의 합이 10개 이상이 될 때까지, 가장 높은 유사도를 가진 사용자들부터 상품 목록에 중복을 제거하여 추가

### 2. 추천 알고리즘
#### 설문조사를 통해 금융상품 추천하기
1. 예금의 경우: 예치기간, 최소한의 금리, 선호하는 은행 선택
    - 1단계: 선택한 은행과 기간, 금리가 조건에 맞는 예금을 필터링
    - 2단계: 결과가 10개 미만일 때 추가 필터링: 기간, 금리가 조건에 맞는 예금을 필터링 후 중복 제거하여 추천목록에 추가
    - 3단계: 1+2단계 결과가 10개 미만일 때 추가 필터링: 기간이 조건에 맞는 예금을 필터링하여 금리가 높은 순으로 정렬 후 추천목록에 추가
    - 4단계: 필터링된 결과를 recommendStore.deposits에 저장. 선택한 기간을 recommendStore.deposits_period에 저장

2. 적금의 경우: 적금 유형(전체/정기/자유), 예치기간, 최소한의 금리, 선호하는 은행 선택
    - 1단계: 선택한 적금 유형, 은행, 기간, 금리가 조건에 맞는 적금을 필터링
    - 2단계: 결과가 10개 미만일 때 추가 필터링: 선택한 적금 유형, 기간, 금리가 조건에 맞는 적금을 필터링 후 중복 제거하여 추천목록에 추가
    - 3단계: 1+2단계 결과가 10개 미만일 때 추가 필터링: 선택한 적금 유형, 기간이 조건에 맞는 적금을 필터링하여 금리가 높은 순으로 정렬 후 추천목록에 추가
    - 4단계: 필터링된 결과를 recommendStore.savings에 저장. 선택한 기간과 적금 유형을 recommendStore.savings_period, recommendStore.savings_type에 저장

3. 주택담보대출의 경우: 담보 유형(아파트/아파트 외), 선호하는 보험사 선택
    - 1단계: 선택한 담보 유형(아파트/아파트 외), 보험사 조건에 맞는 주택담보대출을 필터링
    - 2단계: 결과가 10개 미만일 때 추가 필터링: 선택한 담보 유형에 맞는 대출을 필터링하여 금리가 낮은 순으로 정렬 후 중복 제거하여 추천목록에 추가
    - 3단계: 필터링된 결과를 recommendStore.loans에 저장. 선택한 담보 유형을 recommendStore.loans_type에 저장

### 3. 추천 알고리즘
#### GPT를 이용하여 추천받기
1. 금융상품을 추천받고 싶다고 사용자가 입력하면 [추천] => 예금, 적금, 대출 중 원하는 상품을 질문
2. 예금, 적금, 주택담보대출 중 원하는 상품을 입력하면 [예금, 적금, 대출] => 선호하는 은행 질문
3. 예적금의 경우 은행명/ 적금의 경우 보험사명을 말하면 => 해당 금융회사 상품들 중 관심 상품(like_user로 판단)으로 가장 많이 등록된 상품을 추천

<br>

## 🌟 서비스 대표 기능들에 대한 설명

1. 메인페이지
2. 로그인 회원가입 페이지
3. 프로필 페이지
4. 금융 상품 추천 페이지
5. 금융 상품 조회 페이지
6. 환율 계산기 페이지
7. 주변 은행 검색 페이지
8. 금융 상품 추천 커뮤니티 페이지
9. 재테크 정보 페이지

<br>

## 💬 프로젝트 후기(느낀점)

- **정현수**: 프로젝트를 진행 중간중간에 모델이랑 URL를 수정하면서 기획의 중요성을 깨닫게 되었습니다. 또한 Vue에서 가장 많이 본 에러가 undefined였는데 이를 해결하기 위해 props대신에 store에 저장해서 데이터를 이용하는 방식을 택하면서 시간적으로 동작처리 순서를 공부할 필요성을 느끼게 되었습니다. 삼일 전만해도 에러가 많이 나서 시간 안에 고칠 수 있을 지 걱정되었는데, 에러를 해결하고 그 안에 결과물을 만들어 내어 뿌듯합니다. Vue에서 모달창과 같이 몇 가지 재사용될 수 있는 컴포넌트를 분리 못시킨 점이 아쉽고, 이번 프로젝트를 진행하면서 에러 문구를 보고 해석하는 방법, 그리고 인터넷 검색하는 방법을 배울 수 있었습니다. 프로젝트를 하면서 의견 차이를 보일 때도 있었는데 그러면서 소통하는 방법을 배우게 된 것 같습니다.

- **고도연**: 1학기 동안 빠르게 익혔던 Django, Vue3 내용을 활용할 수 있는 소중한 시간이었습니다. 각각의 프레임워크 사용에 아직 익숙치 않았기 때문에, 프로젝트 기간 동안 다양한 기능을 구현하는 과정이 쉽지 않았습니다. 오류 투성이인 기능들을 보면서 좌절감에 빠지기도 했지만, 덕분에 백엔드와 프론트엔드 간의 전체적 흐름을 제대로 파악할 수 있었습니다. 특히 수업시간에 자세히 다루지 않았던 내용들을 혼자 혹은 팀원과 함께 해결해 나가는 과정에서 이전에 부족했던 문제해결능력이 점차 향상되어간다는 생각이 들었습니다. 또한 프로젝트 진행기간이 짧았기 때문에 부가적인 기능들을 더 구현해보지 않았던 점이 아쉬웠습니다. 

<br>

## 🤔 예상 질문
### 질문 1: 금융상품 추천의 성능 최적화는 어떻게 이루어졌나요?
**답변:**
금융상품 추천의 성능 최적화를 위해 여러 가지 방법을 테스트하고 비교하여 최적의 방안을 채택했습니다. 구체적으로는 다음 두 가지 방법을 고려했습니다:

1. **정렬(Sort) 사용**:
   - 사용자의 금융상품 선호도를 기준으로 전체 사용자 데이터를 정렬하여 가장 유사한 상위 10명의 사용자 데이터를 추출하는 방법을 사용했습니다. 이를 통해 유사한 사용자 그룹에서 추천할 금융상품을 선별하였습니다.
   - 이 방법은 정렬을 한 번 수행한 후 상위 10개의 항목을 추출하기 때문에, 정렬 알고리즘의 시간 복잡도인 O(n log n)을 가지며, 비교적 빠른 성능을 보였습니다.

2. **최소값(Min) 사용**:
   - 유클리드 거리 또는 기타 유사도 측정을 사용하여 현재 사용자와 가장 유사한 사용자를 반복적으로 찾아가는 방법을 사용했습니다. 각 단계에서 가장 유사한 사용자를 찾고, 해당 사용자를 데이터에서 제거한 후 다시 가장 유사한 사용자를 찾는 방식입니다.
   - 이 방법은 반복문을 사용하여 매번 최소값을 찾고 데이터를 갱신하기 때문에, 반복 횟수에 따라 시간이 오래 걸릴 수 있습니다. 특히, 만 명의 사용자 중에서 매번 최소값을 찾아야 하므로 시간 복잡도가 O(n * k)로 증가하게 됩니다.

**성능 비교 결과:**
- 정렬을 사용한 방법이 최소값을 사용하는 방법보다 전체적으로 더 빠르고 효율적임을 확인했습니다. 특히, 데이터셋이 클수록 정렬의 이점이 더 두드러졌습니다.
- 최종적으로, 금융상품 추천에서 정렬을 사용하여 유사도가 높은 사용자를 빠르게 찾아내고, 그 사용자의 금융상품 선호 데이터를 기반으로 추천하는 방식으로 성능을 최적화하였습니다.
- 이 과정을 통해 사용자들에게 더 빠르고 정확하게 맞춤형 금융상품을 추천할 수 있게 되었습니다.

### 질문 2: 금융상품 추천 알고리즘은 어떻게 구현되었나요?
**답변:**
금융상품 추천 알고리즘은 사용자가 입력한 조건을 기반으로 최적의 금융상품을 추천하는 방식으로 구현되었습니다. 이 알고리즘은 Vue.js와 Vuex 스토어를 활용하여 동적으로 작동하며, 다음과 같은 과정을 통해 구현되었습니다.

1. **사용자 입력 조건 처리**
   - 사용자는 다음과 같은 조건을 입력합니다:
     - 상품 유형: 예금, 적금, 주택담보대출 중 선택
     - 기간: 6개월, 12개월, 24개월, 36개월 등
     - 금리: 최소 금리를 슬라이더를 통해 설정
     - 선호하는 은행: 여러 은행 중에서 선택

2. **데이터 초기화 및 가져오기**
   - 사용자가 선택한 상품 유형에 따라 관련 데이터를 스토어에서 가져옵니다. 예를 들어, 사용자가 예금을 선택한 경우, `depositStore.getAll()` 메서드를 호출하여 모든 예금 데이터를 가져옵니다. 가져온 데이터는 `depositStore.deposits`에 저장됩니다.

3. **기본 필터링**
   - 사용자가 선택한 조건을 바탕으로 예금 데이터를 필터링합니다. 이 과정에서는 선택한 은행, 기간, 금리 조건을 모두 만족하는 예금을 추출합니다. 필터링 조건은 다음과 같습니다:
     - 선택한 은행 목록에 포함되는지 확인 (`banks.includes(deposit.kor_co_nm)`)
     - 선택한 기간과 금리를 만족하는 예금 옵션이 있는지 확인 (`option.save_trm === period.value && option.intr_rate >= interestRate.value`)

4. **추가 필터링 (최대 10개까지)**
   - 필터링된 결과가 10개 미만일 경우 추가 조건을 적용하여 최대 10개까지 추천합니다. 이 과정은 단계별로 이루어집니다.
     1. **금리 조건 제외**: 먼저, 금리 조건을 제외하고 필터링하여 조건에 맞는 예금을 추가합니다. 중복을 피하기 위해 기존에 필터링된 결과에 포함되지 않은 예금을 선택합니다.
     2. **은행 조건 제외**: 다음으로, 은행 조건을 제외하고 필터링하여 조건에 맞는 예금을 추가합니다. 이 과정에서도 중복을 피하기 위해 기존에 필터링된 결과에 포함되지 않은 예금을 선택합니다.
     3. **모든 조건 제외**: 마지막으로, 모든 조건을 제외하고 필터링하여 조건에 맞는 예금을 추가합니다. 이 단계에서는 선택한 기간을 만족하는 예금 중에서 금리가 높은 순서대로 정렬하여 추가합니다.

5. **추천 결과 저장 및 페이지 이동**
   - 최종적으로 필터링된 결과를 `recommendStore`에 저장하고, 결과 페이지로 이동합니다. 이렇게 하면 사용자에게 최적의 금융상품을 추천할 수 있습니다.

**요약**
금융상품 추천 알고리즘은 사용자가 입력한 조건(은행, 기간, 금리 등)에 맞는 예금, 적금, 주택담보대출 상품을 필터링하여 추천합니다. 기본 필터링 후 결과가 10개 미만일 경우 추가 조건을 적용하여 최대 10개까지 추천하며, 결과를 저장하고 사용자에게 표시합니다. 이를 통해 사용자에게 최적의 금융상품을 추천하는 기능을 제공합니다. 이 알고리즘은 Vue.js의 반응성과 Vuex 스토어를 활용하여 동적으로 데이터를 처리하고, 사용자에게 최적의 금융상품을 추천하는 시스템을 구현합니다.
