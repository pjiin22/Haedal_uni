class TrustScoreManager:
    def __init__(self):
        # 사용자별 신뢰도를 저장하는 딕셔너리
        self.user_scores = {}

    def _init_user(self, user_id):
        # 처음 요청하는 사용자라면 기본값 36.5로 시작
        if user_id not in self.user_scores:
            self.user_scores[user_id] = 36.5

    def update(self, user_id: str, event: str):
        self._init_user(user_id)

        # 행동 이벤트에 따른 신뢰도 변화량 정의
        changes = {
            "on_time_check_in": 0.1,         # 예약 시간 10분 전 이내 인증
            "check_in": 0.05,                # 단순 입실 인증
            "check_out": 0.25,               # 퇴실 인증
            "report_empty_room": 0.5,        # 비어있는 강의실을 잘 신고함
            "no_show": -0.3,                 # 노쇼 (10분 이상 미입실)
            "no_check_out": -0.1,            # 퇴실 인증 안함
        }

        delta = changes.get(event, 0)  # 존재하지 않는 이벤트면 변화 없음
        new_score = self.user_scores[user_id] + delta
        self.user_scores[user_id] = max(0.0, min(100.0, new_score))  # 0~100도 사이 제한

        return round(self.user_scores[user_id], 2)

    def get_score(self, user_id: str):
        self._init_user(user_id)
        return round(self.user_scores[user_id], 2)
