import math

class ProbabilityManager:
    def __init__(self, max_duration_min=180):
        """
        최대 사용 시간 설정 (기본값: 3시간 = 180분)
        """
        self.max_duration_min = max_duration_min

    def get_empty_probability(self, elapsed_time_min: int, trust_score: float) -> int:
        """
        시간 경과 + 신뢰도를 받아 빈 강의실일 확률(%) 반환

        Parameters:
        - elapsed_time_min: 사용 후 경과 시간 (분 단위)
        - trust_score: 신뢰도 (0.0 ~ 1.0)

        Returns:
        - 정수형 확률값 (0 ~ 100%)
        """
        trust_score = max(0.0, min(trust_score, 1.0))  # 신뢰도 보정
        elapsed_ratio = min(elapsed_time_min / self.max_duration_min, 1.0)  # 경과 비율
        decay_speed = 2.0 - trust_score  # 신뢰도 낮을수록 빠르게 증가
        probability = (1 - math.exp(-decay_speed * elapsed_ratio)) * 100
        return round(probability)


def convert_point_to_trust_score(points: int) -> float:
    """
    포인트(기본 0~200)를 신뢰도(0.0 ~ 1.0)로 환산
    """
    return max(0.0, min(points / 200, 1.0))
